import json

from channels import Channel
from channels.sessions import channel_session
from .models import Room, GameUser
from .events import CreateGameEvent, CreateGameResponseEvent, JoinGameEvent, JoinGameResponseEvent, GameInfoRequest, GameInfoResponse, UserJoinEvent, UserLeftEvent
from .tasks import start_game_countdown

@channel_session
def ws_connect(message):
    print("Client connecting")
    message.reply_channel.send({"accept": True})


@channel_session
def ws_disconnect(message):
    # Get the user from the reply_channel
    user = GameUser.objects.filter(reply_channel=message['reply_channel']).first()
    if user is not None:
        # find the room the user is in
        room = user.room_set.first()
        # If the room only has this user left in it, delete otherwise delete the user
        if room is not None:
            if len(room.users.all()) == 1:
                room.delete()
            else:
                user.delete()
                room.websocket_group.discard(message['reply_channel'])
                room.send_message(UserLeftEvent(user.to_dict()).to_json)


@channel_session
def ws_receive(message):

    print("We got a message!")

    # Load the message['text'] array as our new payload
    payload = json.loads(message['text'])
    # Steal the payload type from the text, easier to move it than deal with it java side
    payload['type'] = payload['event']['type']
    # Remove it from the original location because it doesnt need to be there
    payload['event'].pop('Type', None)
    # Retain reply_channel
    payload['reply_channel'] = message.content['reply_channel']
    # Shoot off to channels
    Channel("trivia.receive").send(payload)


@channel_session
def create_room(message):
    print("Received create room packet")

    event = CreateGameEvent.from_message(message)

    for room in Room.objects.all():
        if room.title == event.room_name:
            Channel(message['reply_channel'])\
                .send(CreateGameResponseEvent(False, message="This room name is already taken!").to_json)
            return

    for user in GameUser.objects.all():
        if user.name == event.username:
            Channel(message['reply_channel']) \
                .send(CreateGameResponseEvent(False, message="This username is already taken!").to_json)
            return

    user = GameUser()
    user.name = event.username
    user.reply_channel = message['reply_channel']
    user.creator = True
    user.save()

    room = Room.create()
    room.title = event.room_name
    room.capacity = event.players
    room.rounds = event.rounds
    room.time = event.time
    room.started = False
    room.save()  # we need to save to make the weird many to many table jazz
    room.users.add(user)
    room.websocket_group.add(user.reply_channel)
    room.save()

    Channel(message['reply_channel']).send(CreateGameResponseEvent(True, room.code).to_json)


@channel_session
def join_room(message):
    print("We got a join room request!")

    event = JoinGameEvent.from_message(message)
    code = event.code
    room = Room.objects.filter(code=code).first()

    if room is not None:

        if room.started:
            Channel(message['reply_channel']) \
                .send(JoinGameResponseEvent(False, message="The game has already started!").to_json)
            return

        for user in room.users.all():
            if user.name == event.username:
                Channel(message['reply_channel'])\
                    .send(JoinGameResponseEvent(False, message="This username is already taken!").to_json)
                return

        if len(room.users.all()) >= room.capacity:
            Channel(message['reply_channel']).send(JoinGameResponseEvent(False, message="This room is already full!").to_json)
            return

        user = GameUser()
        user.name = event.username
        user.reply_channel = message['reply_channel']
        user.creator = False
        user.save()

        room.send_message(UserJoinEvent(user.to_dict()).to_json)

        room.users.add(user)
        room.websocket_group.add(user.reply_channel)
        room.save()

        Channel(message['reply_channel']).send(JoinGameResponseEvent(True, room.code).to_json)

        if len(room.users) == 2:
            start_game_countdown.delay(room.id)

    else:
        Channel(message['reply_channel']).send(JoinGameResponseEvent(False, message="Room does not exist!").to_json)


@channel_session
def game_info_request(message):

    event = GameInfoRequest.from_message(message)

    room = Room.objects.filter(code=event.code).first()

    if room is not None:
        players = [x.to_dict() for x in room.users.all()]
        Channel(message['reply_channel']).send(GameInfoResponse(room.title, room.capacity,
                                                                room.rounds, room.time, players).to_json)
    else:
        Channel(message['reply_channel']).send(GameInfoResponse(False).to_json)
