import json
from channels.sessions import channel_session
from channels.auth import  channel_session_user
from pprint import pprint

user = None

@channel_session
@channel_session_user
def ws_connect(message):
    pprint(vars(message))
    print("Client connecting")
    message.reply_channel.send({"accept": True})


@channel_session
@channel_session_user
def ws_receive(message):
    pprint(vars(message))
    print(f'Recieved {message.content["text"]}')
    message.reply_channel.send({"text": "Got your message!" + message.content["text"]})