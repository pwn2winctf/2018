# -*- encoding: utf-8 -*-

import hashlib
import os
import json
import codecs
from . import log

PLACEHOLDER_SUB_DIR='submissions/'

def hashf(s):
    '''placeholder. remove when hash is defined'''
    return hashlib.sha1(s).hexdigest()

def write_team_config(team_name, priv_key, public_key):
    log.info('overriding team_key.json')
    with codecs.open('team_key.json', 'w', 'utf8') as f:
        f.write(json.dumps({
            'name': team_name,
            'private_key': priv_key,
            'public_key': public_key,
        }))
    log.success('new team key ready, share it with your team')

def register(team_name, public_key):
    log.info('registering new team: %s'%(team_name))
    team_hash = hashf(team_name)
    team_dir = os.path.join(PLACEHOLDER_SUB_DIR, team_hash)

    if os.path.exists(team_dir):
        log.fail('team is already registered')
        return False

    team_data = {
        'name': team_name,
        'public_key': public_key,
    }

    os.mkdir(team_dir)
    with codecs.open(os.path.join(team_dir, 'team.json'), 'w', 'utf8') as f:
        f.write(json.dumps(team_data))

    log.success('team %s successfully added'%(team_name))

    return True

