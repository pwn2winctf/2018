# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
import os
import codecs
import json
import pysodium
import base64
import textwrap

from . import log
from .teamsecrets import TeamSecrets
from ..team import Team
from ..challenge import Challenge, derive_keypair
from ..subrepo import SubRepo

def check_flag_key(flag_pk, salt, flag):
    calc_pk, calc_sk = derive_keypair(salt, flag)
    if flag_pk == calc_pk:
        return calc_sk
    else:
        return None

def check_flag(chall_id, flag):
    chall = Challenge(chall_id)
    chall_data = json.load(codecs.open(chall.path(), 'r', 'utf8'))
    chall_sk = check_flag_key(base64.b64decode(chall_data['pk']),
            base64.b64decode(chall_data['salt']), flag)
    if chall_sk != None:
        team = Team(id=TeamSecrets['id'])

        team_proof = pysodium.crypto_sign(chall_id, TeamSecrets['sign_sk'])
        proof = pysodium.crypto_sign(team_proof, chall_sk)

        subs = team.submissions()
        subs.submit(proof)

        SubRepo.sync(commit_message='Proof of finding %s flag' %
                chall_id)

        return True
    else:
        return False

LINE_WIDTH=72
def pprint():
    index = Challenge.index()
    print('')
    print('-'*LINE_WIDTH)
    print('')
    for chall_id in index:
        chall_dt = Challenge(chall_id)
        with open(chall_dt.path(), 'r') as f:
            chall = json.load(f)
            print('%s        (%d points)        [%s]'%(chall['id'],
                chall['points'], ', '.join(chall['tags'])))
            print('')
            print('\n'.join(textwrap.wrap(chall['description'],
                LINE_WIDTH)))
            print('')
            print('-'*LINE_WIDTH)
            print('')

