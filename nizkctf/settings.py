# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
                       absolute_import
import os
import json
from .six import viewitems


class Settings(object):
    pass


def load():
    """ Load settings from json file """
    thisdir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(thisdir, os.pardir, 'settings.json')) as f:
        settings = json.load(f)
        assert isinstance(settings, dict)
        for k, v in viewitems(settings):
            setattr(Settings, k, v)


load()
