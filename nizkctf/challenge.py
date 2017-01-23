# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from base64 import b64decode
import pysodium
from .settings import Settings


class Challenge(object):
    def __init__(self, chall_id):
        """ stub """
        self.pk = b''
        self.salt = b''


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
