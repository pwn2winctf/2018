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
    pretty_print = True

    def __init__(self):
        super(AcceptedSubmissions, self).__init__()
        self.setdefault('tasks', [])
        self.setdefault('standings', [])

    def path(self):
        return SubRepo.get_path(ACCEPTED_SUBMISSIONS_FILE)

    def rank(self):
        standings = self['standings']
        standings.sort(key=lambda standing: (standing['score'],
                                             -standing['lastAccept']),
                       reverse=True)
        for i, standing in enumerate(standings):
            standing['pos'] = i + 1

    def add(self, chall, points, team):
        chall_id = chall.id
        team_name = team['name']

        if chall_id not in self['tasks']:
            self['tasks'].append(chall_id)

        def get_team_standing():
            for team_standing in self['standings']:
                if team_standing['team'] == team_name:
                    return team_standing

            self['standings'].append({'team': team_name,
                                      'taskStats': {},
                                      'score': 0})
            return self['standings'][-1]

        team_standing = get_team_standing()

        if chall_id in team_standing['taskStats']:
            # Challenge already submitted by team
            return

        accepted_time = int(time.time())
        team_standing['taskStats'][chall_id] = {'points': points,
                                                'time': accepted_time}
        team_standing['lastAccept'] = accepted_time
        team_standing['score'] += points

        self.rank()
        self.save()
