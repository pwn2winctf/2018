# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
                       absolute_import
import os
import json
import threading


LOCALSETTINGS_FILE = 'local-settings.json'


class DefaultLocalSettings(object):
    __lock__ = threading.Lock()

    def path(self):
        thisdir = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(thisdir, os.pardir, LOCALSETTINGS_FILE)

    def __init__(self):
        if os.path.exists(self.path()):
            with open(self.path()) as f:
                self.__dict__.update(json.load(f))

    def __setattr__(self, k, v):
        self.__dict__[k] = v
        with self.__lock__:
            with open(self.path(), 'w') as f:
                json.dump(self.__dict__, f)


LocalSettings = DefaultLocalSettings()
