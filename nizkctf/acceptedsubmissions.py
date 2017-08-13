# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
     absolute_import
import os
import time
from .six import text_type
from .subrepo import SubRepo
from .serializable import SerializableDict


ACCEPTED_SUBMISSIONS_FILE = 'accepted-submissions.json'


class AcceptedSubmissions(SerializableDict):
    def __init__(self):
        super(AcceptedSubmissions, self).__init__()
        self.setdefault('tasks', [])
        self.setdefault('standings', [])

    def path(self):
        return SubRepo.get_path(ACCEPTED_SUBMISSIONS_FILE)

    def add(self, chall_id, points, team_id):
        if chall_id not in self['tasks']:
            self['tasks'].append(chall_id)

        def get_team():
            for team in self['standings']:
                if team['team'] == team_id:
                    return team

            self['standings'].append({'team': team_id,
                                      'taskStats': {},
                                      'score': 0})
            return self['standings'][-1]

        team = get_team()

        if chall_id in team['taskStats']:
            # Challenge already submitted by team
            return

        accepted_time = int(time.time())
        team['taskStats'][chall_id] = {'points': points,
                                       'time':  accepted_time}
        team['lastAccept'] = accepted_time
        team['score'] += points

        self.save()
