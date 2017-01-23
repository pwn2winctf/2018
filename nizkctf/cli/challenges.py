# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
import os
import codecs
import json
import pysodium
import base64

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

