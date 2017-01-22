# -*- encoding: utf-8 -*-

import os
import json


class Settings(object):
    pass


def load():
    """ Load settings from json file """
    thisdir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(thisdir, '..', 'settings.json')) as f:
        settings = json.load(f)
        assert isinstance(settings, dict)
        for k, v in settings.items():
            setattr(Settings, k, v)

load()
