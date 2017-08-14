# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
                       absolute_import
import os
import re
import hashlib
import pysodium
from .six import text_type
from .settings import Settings
from .subrepo import SubRepo
from .serializable import SerializableDict, SerializableList
from .proof import proof_open
from .cli.teamsecrets import TeamSecrets


TEAM_FILE = 'team.json'
MEMBERS_FILE = 'members.json'
SUBMISSIONS_FILE = 'submissions.csv'


class Team(SerializableDict):
    def __init__(self, name=None, id=None):
        if name:
            id = self.name_to_id(name)
            self.update({'name': name})
        if id:
            self.validate_id(id)
            self.id = id
        else:
            raise ValueError('Either name or id are required')

        super(Team, self).__init__()

        if self.exists():
            self.validate()

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
        assert isinstance(name, text_type)
        sha = hashlib.sha256(name.encode('utf-8')).hexdigest()
        return sha[0:1] + '/' + sha[1:4] + '/' + sha[4:]

    @staticmethod
    def validate_id(id):
        assert isinstance(id, text_type)
        if not re.match(r'^[0-9a-f]/[0-9a-f]{3}/[0-9a-f]{60}$', id):
            raise ValueError('Invalid Team ID')

    @staticmethod
    def _binary_field(k):
        return k.endswith('_pk')

    def validate(self):
        expected_keys = {'name', 'crypt_pk', 'sign_pk'}
        if set(self.keys()) != expected_keys:
            raise ValueError("Team should contain, and only contain: %s" %
                             ', '.join(expected_keys))

        assert isinstance(self['name'], text_type)
        if len(self['name']) > Settings.max_size_team_name:
            raise ValueError("Team name must have at most %d chars." %
                             Settings.max_size_team_name)
        if self.name_to_id(self['name']) != self.id:
            raise ValueError("Team name does not match its ID")

        assert isinstance(self['crypt_pk'], bytes)
        if len(self['crypt_pk']) != pysodium.crypto_box_PUBLICKEYBYTES:
            raise ValueError("Team's crypt_pk has incorrect size")

        assert isinstance(self['sign_pk'], bytes)
        if len(self['sign_pk']) != pysodium.crypto_sign_PUBLICKEYBYTES:
            raise ValueError("Team's sign_pk has incorrect size")


class TeamMembers(SerializableList):
    pretty_print = True

    def __init__(self, team):
        self.team = team
        self.team_dir = team.dir()
        super(TeamMembers, self).__init__()

    def path(self):
        return os.path.join(self.team_dir, MEMBERS_FILE)

    def projection(self, attr):
        return [member[attr] for member in self]

    def add(self, id=None, username=None):
        assert isinstance(id, int) or isinstance(id, long)
        assert isinstance(username, text_type)

        another_team = lookup_member(id=id)
        if another_team:
            if another_team != self.team:
                raise ValueError("User '%s' is already member of team '%s'" %
                                 (username, another_team['name']))
            else:
                # do nothing, but do not fail if it is the same team
                return

        self.append({'id': id, 'username': username})
        self.save()


class TeamSubmissions(object):
    def __init__(self, team):
        self.team = team
        self.path = os.path.join(team.dir(), SUBMISSIONS_FILE)

    def submit(self, proof):
        assert isinstance(proof, bytes)
        with open(self.path, 'ab') as f:
            f.write(proof + b'\n')

    def challs(self):
        r = []
        if os.path.exists(self.path):
            with open(self.path, 'rb') as f:
                for proof in f:
                    r.append(proof_open(self.team, proof.strip()))
        if len(set(r)) != len(r):
            raise ValueError('Team submissions contain repeated challenges')
        return r


def my_team():
    return Team(id=TeamSecrets['id'])


def all_teams():
    root = SubRepo.get_path()
    for path, dirs, files in os.walk(root):
        if TEAM_FILE in files:
            assert path.startswith(root)
            id = path[len(root):].strip('/')
            yield Team(id=id)


def lookup_member(id=None, username=None):
    if id:
        attr = 'id'
        value = id
    elif username:
        attr = 'username'
        value = username
    else:
        raise ValueError('Provide either an id or an username')

    for team in all_teams():
        if value in team.members().projection(attr):
            return team

    return None
