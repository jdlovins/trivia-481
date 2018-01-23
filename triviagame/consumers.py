import json
from channels.sessions import channel_session


@channel_session
def ws_connect(message):
    print("Client connecting")


@channel_session
def ws_receive(message):
    pass