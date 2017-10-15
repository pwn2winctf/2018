# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
                       absolute_import
import hashlib
import os
import json
import codecs
import pysodium
import base64
from . import log
from .teamsecrets import write_team_secrets
from ..team import Team
from ..subrepo import SubRepo
from ..six import to_unicode


def register(team_name, countries):
    team_name = to_unicode(team_name)

    log.info('updating subrepo')
    SubRepo.pull()

    log.info('registering new team: %s' % team_name)
    team = Team(name=team_name)

    if team.exists():
        log.fail('team is already registered')
        return False

    log.info('generating encryption keypair')
    crypt_pk, crypt_sk = pysodium.crypto_box_keypair()

    log.info('generating signature keypair')
    sign_pk, sign_sk = pysodium.crypto_sign_keypair()

    team.update({'countries': countries,
                 'crypt_pk': crypt_pk,
                 'sign_pk': sign_pk})
    team.validate()
    team.save()

    SubRepo.push(commit_message='Register team %s' % team_name)
    log.success('team %s added successfully' % team_name)

    write_team_secrets(team.id, crypt_sk, sign_sk)

    return True
