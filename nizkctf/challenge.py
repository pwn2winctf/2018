# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from base64 import b64decode
import os
import re
import json
import pysodium
from .serializable import SerializableDict, SerializableList
from .settings import Settings


CHALLENGES_DIR = 'challenges'
INDEX_FILE = 'index.json'

thisdir = os.path.dirname(os.path.realpath(__file__))
chall_dir = os.path.realpath(os.path.join(thisdir, '..', CHALLENGES_DIR))


class Challenge(SerializableDict):
    def __init__(self, id):
        self.validate_id(id)
        self.id = id
        super(Challenge, self).__init__()

    def path(self):
        return os.path.join(chall_dir, self.id + '.json')

    @staticmethod
    def validate_id(id):
        if len(id) > 15 or not re.match(r'^[a-zA-Z0-9-_]+$', id):
            raise ValueError('invalid challenge ID')

    @staticmethod
    def _binary_field(k):
        return k in {'salt', 'pk'}

    @staticmethod
    def index():
        return ChallengeIndex()


class ChallengeIndex(SerializableList):
    def path(self):
        return os.path.join(chall_dir, INDEX_FILE)


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


def lookup_flag(flag, chall_id=None):
    if chall_id:
        # challenge provided, only try it
        try_challenges = [chall_id]
    else:
        # try every challenge
        try_challenges = Challenge.index()

    try_challenges = map(Challenge, try_challenges)
    try_salts = set(chall['salt'] for chall in try_challenges)
    pk_chall = {chall['pk']: chall for chall in try_challenges}

    for salt in try_salts:
        pk, sk = derive_keypair(salt, flag)
        match = pk_chall.get(pk)

        if match:
            return chall, sk

    return None, None
