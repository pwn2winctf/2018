# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
import os
import hashlib
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

    def exists(self):
        return os.path.exists(self.dir())

    def path(self):
        return os.path.join(self.dir(), TEAM_FILE)

    def save(self):
        if not self.exists():
            os.makedirs(self.dir())
        super(Team, self).save()

    @staticmethod
    def name_to_id(name):
        sha = hashlib.sha256(name.encode()).hexdigest()
        return sha[0:1] + '/' + sha[1:4] + '/' + sha[4:]

    @staticmethod
    def _binary_field(k):
        return k.endswith('_pk')
