# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
     absolute_import
import os
import time
from .six import viewitems, text_type, to_bytes, to_unicode, PY2
from .subrepo import SubRepo
from .serializable import SerializableDict


ACCEPTED_SUBMISSIONS_FILE = 'accepted-submissions.json'
TIME_FORMAT = '%s'  # unix timestamp


class AcceptedSubmissions(SerializableDict):
    def __init__(self):
        super(AcceptedSubmissions, self).__init__()

    def path(self):
        return SubRepo.get_path(ACCEPTED_SUBMISSIONS_FILE)

    def add(self, chall_id, points, team_id):
        if chall_id not in self['tasks']:
            self['tasks'].append(chall_id)

        def get_team():
            for team in self['standings']:
                if team['team'] == team_id:
                    return team

            self['standings'].append({ 'team': team_id,
                                       'taskStats': {},
                                       'score': 0 })
            return self['standings'][-1]

        team = get_team()

        if chall_id in team['taskStats']:
            # Challenge already submitted by team
            return

        accepted_time = current_time()
        team['taskStats'][chall_id] = { 'points': points,
                                        'time':  accepted_time }
        team['lastAccept'] = accepted_time
        team['score'] += points

        self.save()

    # TODO Unicode symbols in team names should be converted to unicode notation (\uXXXX).
    #      reference: https://ctftime.org/json-scoreboard-feed
    def _unserialize_inplace(self):
        self.setdefault('tasks', [])
        self.setdefault('standings', [])

        for team in self['standings']:
            #team['team'] = team['team'].encode('utf-8').decode('unicode_escape')
            team['team'] = to_bytes(team['team']).decode('unicode_escape')

    def _serialize(self):
        from copy import deepcopy
        serialized = deepcopy(self)

        for team in serialized['standings']:
            #team['team'] = team['team'].encode('unicode_escape').decode('utf-8')
            team['team'] = to_unicode(team['team'].encode('unicode_escape'))
        return serialized

def current_time():
    return int(time.strftime(TIME_FORMAT))
