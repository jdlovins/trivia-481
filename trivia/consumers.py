import json

from channels import Channel
from channels.sessions import channel_session
from channels.auth import  channel_session_user
from pprint import pprint
from .decorators import json_to_dict
from .models import Room, GameUser


@channel_session
def ws_connect(message):
    print("Client connecting")
    message.reply_channel.send({"accept": True})


@channel_session
def ws_disconnect(message):
    # Get the user from the reply_channel
    user = GameUser.objects.filter(Reply_Channel=message['reply_channel']).first()
    if user is not None:
        # find the room the user is in
        room = user.room_set.first()
        # If the room only has this user left in it, delete otherwise delete the user
        if len(room.Users.all()) == 1:
            room.delete()
        else:
            user.delete()


@channel_session
def ws_receive(message):

    print("We got a message!")

    # Load the message['text'] array as our new payload
    payload = json.loads(message['text'])
    # Steal the payload type from the text, easier to move it than deal with it java side
    payload['Type'] = payload['Event']['Type']
    # Remove it from the original location because it doesnt need to be there
    payload['Event'].pop('Type', None)
    # Retain reply_channel
    payload['reply_channel'] = message.content['reply_channel']
    # Shoot off to channels
    Channel("trivia.receive").send(payload)


@channel_session
def create_room(message):

    print("Recieved create room packet")
    user = GameUser()
    user.Name = message['Event']['Username']
    user.Reply_Channel = message['reply_channel']
    user.Creator = True
    user.save()

    r = Room.create()
    r.save()
    r.Title = message['Event']['RoomName']
    r.Users.add(user)
    r.websocket_group.add(user.Reply_Channel)
    r.save()


@channel_session
def join_room(message):
    print("We got a join room request!")

    code = message['Event']['Code']

    room = Room.objects.filter(Code=code).first()

    if room is not None:
        user = GameUser()
        user.Name = message['Event']['Username']
        user.Reply_Channel = message['reply_channel']
        user.Creator = False
        user.save()

        room.Users.add(user)
        room.websocket_group.add(user.Reply_Channel)
        room.save()

        # check for room space
        # check if the game is running already
        # send back response codes




    pass

    #r = Room()
    #r.title = message['RoomName']
    #r.websocket_group.add(message.reply_channel)
