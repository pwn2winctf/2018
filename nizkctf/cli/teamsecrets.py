# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
import os
from . import log
from ..serializable import SerializableDict


TEAMSECRETS_FILE = 'team-secrets.json'


class DefaultTeamSecrets(SerializableDict):
    def path(self):
        thisdir = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(thisdir, '..', '..', TEAMSECRETS_FILE)

    @staticmethod
    def _binary_field(k):
        return k.endswith('_sk')


TeamSecrets = DefaultTeamSecrets()


def write_team_secrets(team_id, crypt_sk, sign_sk):
    log.info('overriding %s' % TEAMSECRETS_FILE)

    TeamSecrets['id'] = team_id
    TeamSecrets['crypt_sk'] = crypt_sk
    TeamSecrets['sign_sk'] = sign_sk
    TeamSecrets.save()

    log.success('new team secrets ready, share them with your team')
