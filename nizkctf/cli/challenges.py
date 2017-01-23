# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
import os
import codecs
import json
import pysodium
import base64
from . import log
from ..challenge import Challenge, derive_keypair


OPSLIMIT = 33554432
MEMLIMIT = 1073741824


class ChallError(Exception):
    pass

def check_flag_key(flag_pk, salt, flag):
    calc_pk, _ = derive_keypair(salt, flag)
    return flag_pk == calc_pk

def check_flag(chall_id, flag):
    chall = Challenge(chall_id)
    chall_data = json.load(codecs.open(chall.path(), 'r', 'utf8'))
    return check_flag_key(base64.b64decode(chall_data['pk']),
                    base64.b64decode(chall_data['salt']), flag)
    raise ChallError('Invalid challenge id: %s'%(chall_id))

