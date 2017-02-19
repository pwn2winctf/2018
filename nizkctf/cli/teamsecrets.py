# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
                       absolute_import
import os
import shutil
import time
from . import log
from ..serializable import SerializableDict


TEAMSECRETS_FILE = 'team-secrets.json'


class DefaultTeamSecrets(SerializableDict):
    def path(self):
        thisdir = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(thisdir, os.pardir, os.pardir, TEAMSECRETS_FILE)

    @staticmethod
    def _binary_field(k):
        return k.endswith('_sk')


TeamSecrets = DefaultTeamSecrets()


def write_team_secrets(team_id, crypt_sk, sign_sk):
    if TeamSecrets.exists():
        log.info('overriding %s' % TEAMSECRETS_FILE)

        backup = TeamSecrets.path() + time.strftime('.%Y-%m-%d-%H-%M-%S')
        shutil.copy(TeamSecrets.path(), backup)

    TeamSecrets['id'] = team_id
    TeamSecrets['crypt_sk'] = crypt_sk
    TeamSecrets['sign_sk'] = sign_sk
    TeamSecrets.save()

    log.success('ready, share %s with your team!' % TEAMSECRETS_FILE)
