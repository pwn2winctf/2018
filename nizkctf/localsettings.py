# -*- encoding: utf-8 -*-

import os
import json
import threading


thisdir = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(thisdir, '..', 'local-settings.json')


class DefaultLocalSettings(object):
    __lock__ = threading.Lock()

    def __init__(self):
        if os.path.exists(path):
            with open(path) as f:
                self.__dict__.update(json.load(f))

    def __setattr__(self, k, v):
        self.__dict__[k] = v
        with self.__lock__:
            with open(path, 'w') as f:
                json.dump(self.__dict__, f)


LocalSettings = DefaultLocalSettings()
