# -*- encoding: utf-8 -*-

from .settings import Settings
from math import floor, log


def compute_points(chall, num_solves):
    num_solves = max(1, num_solves)

    params = Settings.dynamic_scoring
    if not params:
        return chall['points']

    # Google CTF 2017's formula
    K, V, minpts, maxpts = params['K'], params['V'], \
        params['minpts'], params['maxpts']
    return int(max(minpts, floor(maxpts - K*log((num_solves + V)/(1 + V), 2))))
