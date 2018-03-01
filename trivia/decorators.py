import json
from collections import namedtuple


def json_to_dict(func):
    def _new_func(message=None):

        if message is not None:
            d = json.load(message, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            return func(d)
        return func(message)
    return _new_func
