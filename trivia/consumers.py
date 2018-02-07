import json

from channels import Channel
from channels.sessions import channel_session
from channels.auth import  channel_session_user
from pprint import pprint

@channel_session
def ws_connect(message):
    print("Client connecting")
    message.reply_channel.send({"accept": True})

@channel_session
def ws_receive(message):
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
    print("we make room")