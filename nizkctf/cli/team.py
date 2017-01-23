# -*- encoding: utf-8 -*-

import hashlib
import os
import json
import codecs
import pysodium
import base64
from . import log
from ..team import Team
from ..teamsecrets import write_team_secrets
from ..subrepo import SubRepo


def register(team_name):
    log.info('registering new team: %s' % team_name)
    team = Team(name=team_name)

    if team.exists():
        log.fail('team is already registered')
        return False

    log.info('generating crypto keypair')
    crypt_pk, crypt_sk = pysodium.crypto_box_keypair()

    log.info('generating signature keypair')
    sign_pk, sign_sk = pysodium.crypto_sign_keypair()

    team.update({'name': team_name,
                 'crypt_pk': crypt_pk,
                 'sign_pk': sign_pk})
    team.save()

    SubRepo.sync()
    log.success('team %s added successfully' % team_name)

    write_team_secrets(team_name, crypt_pk, crypt_sk, sign_pk, sign_sk)

    return True
