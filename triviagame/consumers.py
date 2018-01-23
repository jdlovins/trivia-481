import json
from channels.sessions import channel_session
from pprint import pprint

@channel_session
def ws_connect(message):
    print("Client connecting")
    message.reply_channel.send({"accept": True})


@channel_session
def ws_receive(message):
    pprint(vars(message))
    message.reply_channel.send("Got your message!")