# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
import unicodedata


def width(s):
    asian = sum(unicodedata.east_asian_width(c) in {'W','F'} for c in s)
    return len(s) + asian
