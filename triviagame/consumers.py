import json
from channels.sessions import channel_session


@channel_session
def ws_connect(message):
    print("Client connecting")
    message.reply_channel.send({"accept": True})


@channel_session
def ws_receive(message):
    print("recieved " + message.content)
    message.reply_channel.send("Got your message!")