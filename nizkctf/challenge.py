# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from base64 import b64decode
import os
import re
import json
import pysodium
from .serializable import SerializableDict
from .settings import Settings


CHALLENGES_DIR = 'challenges'


class Challenge(object):
    thisdir = os.path.dirname(os.path.realpath(__file__))
    dir = os.path.realpath(os.path.join(thisdir, '..', CHALLENGES_DIR))

    def __init__(self, id):
        self.validate_id(id)
        self.id = id
        super(Challenge, self).__init__()

    def path(self):
        return os.path.join(self.dir, self.id + '.json')

    @staticmethod
    def validate_id(id):
        if len(id) > 15 or not re.match(r'^[a-zA-Z0-9-_]+$', id):
            raise ValueError('invalid challenge ID')

    @staticmethod
    def index():
        # fixme: put thisdir and dir in a better place
        thisdir = os.path.dirname(os.path.realpath(__file__))
        dir = os.path.realpath(os.path.join(thisdir, '..', CHALLENGES_DIR))
        with open(os.path.join(dir, 'index.json'), 'r') as f:
            return json.load(f)


def derive_keypair(salt, flag):
    flag = flag.encode('utf-8')
    assert isinstance(salt, bytes)
    assert isinstance(flag, bytes)
    assert len(salt) == pysodium.crypto_pwhash_scryptsalsa208sha256_SALTBYTES

    chall_seed = pysodium.crypto_pwhash_scryptsalsa208sha256(
        pysodium.crypto_sign_SEEDBYTES,
        flag,
        salt,
        Settings.scrypt_ops_limit,
        Settings.scrypt_mem_limit)

    return pysodium.crypto_sign_seed_keypair(chall_seed)
