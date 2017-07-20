# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
     absolute_import
import os
import time
import pysodium
from base64 import b64encode
from .team import Team
from .six import text_type
from .subrepo import SubRepo
from .serializable import SerializableList


NEWS_FILE = 'news.json'

# TODO duplicated from scoreboard.py
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'

class News(SerializableList):
    def __init__(self):
        super(News, self).__init__()

    def path(self):
        return SubRepo.get_path(NEWS_FILE)

    def add(self, msg_text, to=None):
        # TODO where should this function be inserted?
        # TODO how do we do commit/push?
        
        if to is None:
            # TODO do we really encode public messages?
            encoded_msg = b64encode(msg_text)
            message = { "msg": encoded_msg,
                        "time": current_time() }
        else:
            team = Team(name=to)
            team_pk = team['crypt_pk']
            # TODO check if msg really needs to be encoded before encrypted
            #       (and encoded after encrypted too)
            msg_text = b64encode(msg_text)
            encrypted_msg = pysodium.crypto_box_seal(msg, team_pk)
            encoded_msg = b64encode(encrypted_msg)

            message = { "msg": encoded_msg,
                        "to": team['name'],
                        "time": current_time() }
        self.append(message)

        self.save()

        dest = message["to"] if "to" in message else "all"
        SubRepo.push(commit_message='Added news to %s' % dest)
    
def current_time():
    # TODO duplicated from scoreboard.py
    return time.strftime(TIME_FORMAT)