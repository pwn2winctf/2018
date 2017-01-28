# -*- encoding: utf-8 -*-
# a subset of the six module

from __future__ import unicode_literals, division, print_function,\
                       absolute_import
import operator
import sys


PY2 = sys.version_info[0] == 2

text_type = type('')


if PY2:
    viewitems = operator.methodcaller("viewitems")
else:
    viewitems = operator.methodcaller("items")


def to_bytes(s):
    if isinstance(s, text_type):
        return s.encode('utf-8')
    return s


def to_unicode(s):
    if isinstance(s, text_type):
        return s
    encoding = sys.getfilesystemencoding()
    s = s.decode(encoding)
    return s
