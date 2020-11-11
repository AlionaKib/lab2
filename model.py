# -*- coding: utf-8 -*-

import json

END_CHARACTER = "\0"
MESSAGE_PATTERN = "{username}>{message}"
TARGET_ENCODING = "utf-8"


class Message(object):

    def __init__(self, **kwargs):
        self.username = None
        self.message = None
        self.quit = False
        self.__dict__.update(kwargs)

    def __str__(self):
        return MESSAGE_PATTERN.format(**self.__dict__)

    def marshal(self):
        return (json.dumps(self.__dict__) + END_CHARACTER).encode(TARGET_ENCODING)