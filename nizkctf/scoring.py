# -*- encoding: utf-8 -*-

from .settings import Settings
from math import acosh, log


def compute_points(chall, num_solves):
    if not Settings.dynamic_scoring:
        return chall['points']

    return int(max(50, round(1402.86 - 1.82*log(num_solves)
                             - 113.94*acosh(1045.71 + 335.59*num_solves))))
