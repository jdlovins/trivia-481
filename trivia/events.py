import json
from .utils import to_camel_case


class BaseEvent(object):

    @property
    def to_json(self):
        t = self.__dict__
        for key in t:
            t[to_camel_case(key)] = t.pop(key)
        return {"text": json.dumps(t, default=lambda o: o.__dict__, sort_keys=True, indent=4)}


class CreateGameEvent(BaseEvent):
    def __init__(self, username, room_name, time, rounds, players):
        self.username = username
        self.room_name = room_name
        self.time = time
        self.rounds = rounds
        self.players = players

    @classmethod
    def from_message(cls, message):
        event = message['event']
        return cls(event['userName'], event['roomName'], event['time'], event['rounds'], event['players'])


class CreateGameResponseEvent(BaseEvent):
    def __init__(self, success, message=""):
        self.type = "CREATE_GAME_RESPONSE"
        self.success = success
        self.message = message


class JoinGameEvent(BaseEvent):
    def __init__(self, username, code):
        self.username = username
        self.code = code

    @classmethod
    def from_message(cls, message):
        event = message['event']
        return cls(event['userName'], event['code'])


class JoinGameResponseEvent(BaseEvent):
    def __init__(self, success, message=""):
        self.type = "JOIN_GAME_RESPONSE"
        self.success = success
        self.message = message

