import json

from channels import Channel
from channels.sessions import channel_session
from .models import Room, GameUser
from .events import CreateGameEvent, JoinGameEvent, JoinGameResponseEvent


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
                # send a user left event


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
                .send(JoinGameResponseEvent(False, "This room name is already taken!").to_json)
            return

    for user in GameUser.objects.all():
        if user.name == event.username:
            Channel(message['reply_channel']) \
                .send(JoinGameResponseEvent(False, "This username is already taken!").to_json)
            return

    user = GameUser()
    user.name = event.username
    user.reply_channel = message['reply_channel']
    user.creator = True
    user.save()

    r = Room.create()
    r.title = event.room_name
    r.capacity = event.players
    r.rounds = event.rounds
    r.time = event.time
    r.started = False
    r.save()  # we need to save to make the weird many to many table jazz
    r.users.add(user)
    r.websocket_group.add(user.reply_channel)
    r.save()

    Channel(message['reply_channel']).send(JoinGameResponseEvent(True).to_json)


@channel_session
def join_room(message):
    print("We got a join room request!")

    event = JoinGameEvent.from_message(message)
    code = event.code
    room = Room.objects.filter(code=code).first()

    if room is not None:

        if room.started:
            Channel(message['reply_channel']) \
                .send(JoinGameResponseEvent(False, "The game has already started!").to_json)
            return

        for user in room.Users.all():
            if user.Name == event.username:
                Channel(message['reply_channel'])\
                    .send(JoinGameResponseEvent(False, "This username is already taken!").to_json)
                return

        if len(room.Users.all()) >= room.capacity:
            Channel(message['reply_channel']).send(JoinGameResponseEvent(False, "This room is already full!").to_json)
            return

        user = GameUser()
        user.name = event.username
        user.reply_channel = message['reply_channel']
        user.creator = False
        user.save()

        room.Users.add(user)
        room.websocket_group.add(user.reply_channel)
        room.save()

        resp = JoinGameResponseEvent(True)
        Channel(message['reply_channel']).send(resp.to_json)

    else:
        resp = JoinGameResponseEvent(False, "Room does not exist!")
        Channel(message['reply_channel']).send(resp.to_json)
