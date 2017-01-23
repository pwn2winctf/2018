# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
import os
import pysodium
from base64 import b64encode, b64decode
from .challenge import Challenge


def proof_open(team, proof):
    proof = b64decode(proof)

    claimed_chall = proof[2*64:].decode('utf-8')
    chall_pk = Challenge(claimed_chall).pk
    team_pk = team['sign_pk']

    membership_proof = pysodium.crypto_sign_open(proof, chall_pk)
    chall_id = pysodium.crypto_sign_open(membership_proof,
                                         team_pk).decode('utf-8')

    if claimed_chall != chall_id:
        raise ValueError('invalid proof')

    return chall_id

