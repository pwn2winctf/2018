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
        if to is None:
            message = { "msg": msg_text, "time": current_time() }
        else:
            team_pk = Team(name=to)['crypt_pk']
            encrypted_msg = pysodium.crypto_box_seal(msg_text.encode("utf-8"), team_pk)
            encoded_msg = b64encode(encrypted_msg)

            message = { "msg": encoded_msg.decode("utf-8"),
                        "to": to,
                        "time": current_time() }
        
        self.append(message)
        self.save()

        dest = message["to"] if "to" in message else "all"
        SubRepo.push(commit_message='Added news to %s' % dest, merge_request=False)
    
def current_time():
    # TODO duplicated from scoreboard.py
    return time.strftime(TIME_FORMAT)