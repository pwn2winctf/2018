# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
import os
import codecs
import json
import pysodium
import base64
import textwrap

from . import log
from .teamsecrets import TeamSecrets, my_team
from ..proof import proof_create
from ..challenge import lookup_flag
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
    index = Challenge.index()
    print('')
    print('-'*LINE_WIDTH)
    print('')
    for chall_id in index:
        chall_dt = Challenge(chall_id)
        with open(chall_dt.path(), 'r') as f:
            chall = json.load(f)
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
