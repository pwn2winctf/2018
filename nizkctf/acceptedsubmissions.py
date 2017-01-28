# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
     absolute_import
import os
import time
from .six import text_type
from .subrepo import SubRepo
from .serializable import SerializableList


ACCEPTED_SUBMISSIONS_FILE = 'accepted-submissions.json'
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'


class DefaultAcceptedSubmissions(SerializableList):
    def __init__(self):
        super(DefaultAcceptedSubmissions, self).__init__()

    def path(self):
        return SubRepo.get_path(ACCEPTED_SUBMISSIONS_FILE)

    def add(self, chall_id, points, team_id):
        self.append({"chall": chall_id,
                     "points": points,
                     "team": team_id,
                     "time": current_time()})
        self.save()


def current_time():
    return time.strftime(TIME_FORMAT)


AcceptedSubmissions = DefaultAcceptedSubmissions()
