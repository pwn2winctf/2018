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
NEWS_DIR = '.'

thisdir = os.path.dirname(os.path.realpath(__file__))
news_dir = os.path.realpath(os.path.join(thisdir, os.pardir, NEWS_DIR))

# TODO duplicated from scoreboard.py
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'

class News(SerializableList):
    def __init__(self):
        super(News, self).__init__()

    def path(self):
        return os.path.join(news_dir, NEWS_FILE)

    def add(self, msg, to=None):
        # TODO where should this function be inserted?
        # TODO how do we do commit/push?
        if to is None:
            # TODO do we really encode public messages?
            encoded_msg = b64encode(msg)
            self.append({"msg": encoded_msg,
                         "time": current_time()})
        else:
            team = Team(name=to)
            team_pk = team['crypt_pk']
            # TODO check if msg really needs to be encoded before encrypted
            #       (and encoded after encrypted too)
            msg = b64encode(msg)
            encrypted_msg = pysodium.crypto_box_seal(msg, team_pk)
            encoded_msg = b64encode(encrypted_msg)

            self.append({"msg": encoded_msg,
                         "to": team['name'],
                         "time": current_time()})
        self.save()
    
def current_time():
    # TODO duplicated from scoreboard.py
    return time.strftime(TIME_FORMAT)