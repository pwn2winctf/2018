# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
     absolute_import
import os
import time
from .six import text_type
from .subrepo import SubRepo
from .serializable import SerializableDict
from .scoring import compute_points


ACCEPTED_SUBMISSIONS_FILE = 'accepted-submissions.json'


class AcceptedSubmissions(SerializableDict):
    pretty_print = True

    def __init__(self):
        super(AcceptedSubmissions, self).__init__()
        self.setdefault('tasks', [])
        self.setdefault('standings', [])

    def path(self):
        return SubRepo.get_path(ACCEPTED_SUBMISSIONS_FILE)

    def get_team_standing(self, team_name):
        for team_standing in self['standings']:
            if team_standing['team'] == team_name:
                return team_standing

        team_standing = {'team': team_name,
                         'taskStats': {},
                         'score': 0}
        self['standings'].append(team_standing)
        return team_standing

    def get_solves(self, chall_id):
        solves = set()
        for team_standing in self['standings']:
            if chall_id in team_standing['taskStats']:
                solves.add(team_standing['team'])
        return solves

    def compute_points(self, chall, additional_solves=0):
        num_solves = len(self.get_solves(chall.id)) + additional_solves
        return compute_points(chall, num_solves)

    def recompute_score(self, chall):
        points = self.compute_points(chall)
        chall_id = chall.id
        # update affected team's standings
        for team_standing in self['standings']:
            task_stats = team_standing['taskStats']
            if chall_id in task_stats:
                task_stats[chall_id]['points'] = points
                team_standing['score'] = sum(task['points']
                                             for task in task_stats.values())

    def rank(self):
        standings = self['standings']
        standings.sort(key=lambda standing: (standing['score'],
                                             -standing['lastAccept']),
                       reverse=True)
        for i, standing in enumerate(standings):
            standing['pos'] = i + 1

    def add(self, chall, team):
        chall_id = chall.id
        team_name = team['name']

        if chall_id not in self['tasks']:
            self['tasks'].append(chall_id)

        team_standing = self.get_team_standing(team_name)

        if chall_id in team_standing['taskStats']:
            # Challenge already submitted by team
            return

        accepted_time = int(time.time())
        team_standing['taskStats'][chall_id] = {'points': 0,
                                                'time': accepted_time}
        team_standing['lastAccept'] = accepted_time

        self.recompute_score(chall)
        self.rank()
        self.save()
