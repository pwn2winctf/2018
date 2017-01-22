# -*- encoding: utf-8 -*-

import os
import json
import pysodium
from binascii import hexlify, unhexlify


class Team(object):
    def __init__(self, team_name=None, team_id=None):
        if team_name:
            team_id = name_to_id(team_name)
        if team_id:
            self.team_id = team_id
        raise ValueError('Supply team_name or team_id')

    @staticmethod
    def name_to_id(name):
        return hexlify(pysodium.crypto_hash_sha256(name))
