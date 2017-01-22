# -*- encoding: utf-8 -*-

import os
import json
import pysodium
import base64
from . import log

OPSLIMIT = 33554432
MEMLIMIT = 1073741824
class ChallError(Exception):
    pass

def generate_keypair(flag, salt):
    assert len(salt) == pysodium.crypto_pwhash_scryptsalsa208sha256_SALTBYTES
    chall_seed = pysodium.crypto_pwhash_scryptsalsa208sha256(
        pysodium.crypto_sign_SEEDBYTES,
        flag,
        salt,
        OPSLIMIT,
        MEMLIMIT)

    return pysodium.crypto_sign_seed_keypair(chall_seed)

def check_flag_key(flag_pk, salt, flag):
    calc_pk, _ = generate_keypair(flag, salt)
    return flag_pk == calc_pk

def check_flag(chall_stream, chall_id, flag):
    challs = json.load(chall_stream)
    for chall in challs:
        if chall['id'] == chall_id:
            return check_flag_key(base64.b64decode(chall['pk']),
                    base64.b64decode(chall['salt']), flag)
    raise ChallError('Invalid challenge id: %s'%(chall_id))

