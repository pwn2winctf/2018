# -*- encoding: utf-8 -*-

from __future__ import absolute_import, division, print_function
import os
import hashlib
from .text import text_type
from .subrepo import SubRepo
from .serializable import SerializableDict, SerializableList


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
        super(Team, self).__init__()

    def dir(self):
        return SubRepo.get_path(self.id)

    def path(self):
        return os.path.join(self.dir(), TEAM_FILE)

    def save(self):
        if not self.exists():
            os.makedirs(self.dir())
        super(Team, self).save()

    def members(self):
        return TeamMembers(self)

    def submissions(self):
        return TeamSubmissions(self)

    @staticmethod
    def name_to_id(name):
        sha = hashlib.sha256(name.encode('utf-8')).hexdigest()
        return sha[0:1] + '/' + sha[1:4] + '/' + sha[4:]

    @staticmethod
    def _binary_field(k):
        return k.endswith('_pk')


class TeamMembers(SerializableList):
    def __init__(self, team):
        self.team_dir = team.dir()
        super(TeamMembers, self).__init__()

    def path(self):
        return os.path.join(self.team_dir, MEMBERS_FILE)

    def projection(self, attr):
        return [member[attr] for member in self]

    def add(self, id=None, username=None):
        assert isinstance(id, int) or isinstance(id, long)
        assert isinstance(username, text_type)
        self.append({'id': id, 'username': username})
        self.save()


class TeamSubmissions(object):
    def __init__(self, team):
        self.team = team
        self.path = os.path.join(team.dir(), SUBMISSIONS_FILE)

    def submit(self, proof):
        with open(self.path, 'a') as f:
            f.write(proof + b'\n')
