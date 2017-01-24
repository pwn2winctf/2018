# -*- encoding: utf-8 -*-

from __future__ import absolute_import, division, print_function
import unicodedata


text_type = type('')


def width(s):
    asian = sum(unicodedata.east_asian_width(c) in {'W', 'F'} for c in s)
    return len(s) + asian
