# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
                       absolute_import


def info(s):
    print('\033[93m[*]\033[00m %s' % s)


def success(s):
    print('\033[92m[+]\033[00m %s' % s)


def fail(s):
    print('\033[91m[!]\033[00m %s' % s)
