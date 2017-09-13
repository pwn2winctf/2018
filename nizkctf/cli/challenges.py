# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
                       absolute_import
import os
import codecs
import json
import pysodium
import base64
import textwrap

from . import log
from .teamsecrets import TeamSecrets
from ..team import my_team
from ..proof import proof_create
from ..challenge import Challenge, lookup_flag
from ..subrepo import SubRepo
from ..acceptedsubmissions import AcceptedSubmissions


def submit_flag(flag, chall_id=None):
    chall, chall_sk = lookup_flag(flag, chall_id)

    if chall_sk is None:
        return False, 'This is not the correct flag.'

    SubRepo.pull()

    submissions = my_team().submissions()
    if chall in submissions.challs():
        return False, 'Your team already solved %s.' % chall.id

    proof = proof_create(chall.id, chall_sk)
    submissions.submit(proof)
    SubRepo.push(commit_message='Proof: found flag for %s' % chall.id)

    return True, 'Congratulations! You found the right flag for %s.' % chall.id


LINE_WIDTH = 72


def pprint():
    print('')
    print('-'*LINE_WIDTH)
    print('')
    submissions = AcceptedSubmissions()
    for chall_id in Challenge.index():
        chall = Challenge(chall_id)
        print('ID: %s        (%d points)        [%s]' % (
            chall.id,
            submissions.compute_points(chall, additional_solves=1),
            ', '.join(chall['tags'])))
        print('')
        print(chall['title'])
        print('')
        print('\n'.join(textwrap.wrap(chall['description'],
                                      LINE_WIDTH)))
        print('')
        print('-'*LINE_WIDTH)
        print('')
