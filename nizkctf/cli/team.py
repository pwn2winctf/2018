# -*- encoding: utf-8 -*-

import hashlib
import os
import json
import codecs
import pysodium
import base64
from . import log

PLACEHOLDER_SUB_DIR='submissions/'

def write_team_config(team_name, crypt_pk, crypt_sk, sign_pk, sign_sk):
    log.info('overriding team_key.json')
    with codecs.open('team_key.json', 'w', 'utf8') as f:
        f.write(json.dumps({
            'name': team_name,
            'crypt_pk': base64.b64encode(crypt_pk),
            'crypt_sk': base64.b64encode(crypt_sk),
            'sign_pk': base64.b64encode(sign_pk),
            'sign_sk': base64.b64encode(sign_sk),
        }))
    log.success('new team key ready, share it with your team')

def register(team_name):
    log.info('registering new team: %s'%(team_name))
    team_hash = hashlib.sha256(team_name).hexdigest()
    team_dir = os.path.join(PLACEHOLDER_SUB_DIR, team_hash)

    if os.path.exists(team_dir):
        log.fail('team is already registered')
        return False

    log.info('generating crypt keypair')
    crypt_pk, crypt_sk = pysodium.crypto_box_keypair()

    log.info('generating signature keypair')
    sign_pk, sign_sk = pysodium.crypto_sign_keypair()

    team_data = {
        'name': team_name,
        'crypt_pk': base64.b64encode(crypt_pk),
        'sign_pk': base64.b64encode(sign_pk),
    }

    os.mkdir(team_dir)
    with codecs.open(os.path.join(team_dir, 'team.json'), 'w', 'utf8') as f:
        f.write(json.dumps(team_data))

    log.success('team %s successfully added'%(team_name))

    write_team_config(team_name, crypt_pk, crypt_sk, sign_pk, sign_sk)

    return True

