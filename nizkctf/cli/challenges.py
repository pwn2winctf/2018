# -*- encoding: utf-8 -*-

from __future__ import absolute_import, division, print_function
import os
import codecs
import json
import pysodium
import base64
import textwrap

from . import log
from .teamsecrets import TeamSecrets, my_team
from ..proof import proof_create
from ..challenge import Challenge, lookup_flag
from ..subrepo import SubRepo


def submit_flag(flag, chall_id=None):
    chall, chall_sk = lookup_flag(flag, chall_id)

    if chall_sk is None:
        return False

    proof = proof_create(chall.id, chall_sk)
    my_team().submissions().submit(proof)

    SubRepo.sync(commit_message='Proof: found flag for %s' % chall.id)

    return True


LINE_WIDTH = 72


def pprint():
    print('')
    print('-'*LINE_WIDTH)
    print('')
    for chall_id in Challenge.index():
        chall = Challenge(chall_id)
        print('%s        (%d points)        [%s]' % (
            chall['id'],
            chall['points'],
            ', '.join(chall['tags'])))
        print('')
        print('\n'.join(textwrap.wrap(chall['description'],
                                      LINE_WIDTH)))
        print('')
        print('-'*LINE_WIDTH)
        print('')
