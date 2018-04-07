import json
from .utils import to_camel_case


class BaseEvent(object):

    @property
    def to_json(self):
        t = self.__dict__
        for key in t:
            t[to_camel_case(key)] = t.pop(key)
        return {"text": json.dumps(t, default=lambda o: o.__dict__, sort_keys=True)}


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
    def __init__(self, success, code, message=""):
        self.type = "CREATE_GAME_RESPONSE"
        self.success = success
        self.message = message
        self.code = code


class JoinGameEvent(BaseEvent):
    def __init__(self, username, code):
        self.username = username
        self.code = code

    @classmethod
    def from_message(cls, message):
        event = message['event']
        return cls(event['userName'], event['code'])


class JoinGameResponseEvent(BaseEvent):
    def __init__(self, success, code=-1, message=""):
        self.type = "JOIN_GAME_RESPONSE"
        self.success = success
        self.message = message
        self.code = code


class GameInfoRequest(BaseEvent):
    def __init__(self, code):
        self.code = code

    @classmethod
    def from_message(cls, message):
        event = message['event']
        return cls(event['code'])


class GameInfoResponse(BaseEvent):
    def __init__(self, title="", max_players="", rounds="", time="", players="", success=True):
        self.type = "GAME_INFO_RESPONSE"
        self.title = title
        self.max_players = max_players
        self.rounds = rounds
        self.time = time
        self.players = players
        self.success = success


class UserJoinEvent(BaseEvent):
    def __init__(self, player):
        self.type = "USER_JOIN"
        self.player = player


class UserLeftEvent(BaseEvent):
    def __init__(self, player):
        self.type = "USER_LEFT"
        self.player = player


class UpdateProgressEvent(BaseEvent):
    def __init__(self, progress):
        self.type = "UPDATE_PROGRESS"
        self.progress = progress


class GameCountdownEvent(BaseEvent):
    def __init__(self):
        self.type = "GAME_COUNTDOWN_STARTED"


class GameStartedEvent(BaseEvent):
    def __init__(self):
        self.type = "GAME_STARTED"


class QuestionInfoEvent(BaseEvent):
    def __init__(self, question, pk, category, answers):
        self.type = "QUESTION_INFO"
        self.question = question
        self.pk = pk
        self.category = category
        self.answers = answers


class HandleAnswerEvent(BaseEvent):
    def __init__(self, question_pk, answer_pk):
        self.question_pk = question_pk
        self.answer_pk = answer_pk

    @classmethod
    def from_message(cls, message):
        event = message['event']
        return cls(event['questionPK'], event['answerPK'])


class UpdatePlayerListEvent(BaseEvent):
    def __init__(self, players):
        self.type = "UPDATE_PLAYER_LIST"
        self.players = players


class UpdateProgressMaxEvent(BaseEvent):
    def __init__(self, max_progress):
        self.type = "UPDATE_PROGRESS_MAX"
        self.max = max_progress


class UpdateStatusMessageEvent(BaseEvent):
    def __init__(self, message):
        self.type = "UPDATE_STATUS_MESSAGE"
        self.message = message


class RoundOverEvent(BaseEvent):
    def __init__(self):
        self.type = "ROUND_OVER"
