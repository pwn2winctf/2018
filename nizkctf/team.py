# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
import os
import json
import pysodium
from binascii import hexlify, unhexlify
from .subrepo import SubRepo
from .serializable import SerializableDict


TEAM_FILE = 'team.json'
MEMBERS_FILE = 'members.json'
SUBMISSIONS_FILE = 'submissions.csv'


class Team(SerializableDict):
    def __init__(self, name=None, id=None):
        if name:
            id = self.name_to_id(name)
            self.update({'name': name})
        if id:
            self.id = id
        else:
            raise ValueError('Either name or id are required')
        self.load()

    def dir(self):
        return SubRepo.get_path(self.id)

    def path(self):
        return os.path.join(self.dir(), TEAM_FILE)

    def save(self):
        dir = self.dir()
        if not os.path.exists(dir):
            os.makedirs(dir)
        super(Team, self).save()

    @staticmethod
    def name_to_id(name):
        sha = hexlify(pysodium.crypto_hash_sha256(name)).decode('utf-8')
        return sha[0:1] + '/' + sha[1:4] + '/' + sha[4:]

    @staticmethod
    def _binary_field(k):
        return k.endswith('_pk')
