# -*- encoding: utf-8 -*-

import os
import json
import threading


class LocalSettings(object):
    def __init__(self):
        self.data = None
        self.lock = threading.Lock()
        self._load()

    def __setitem__(self, k, v):
        self.data[k] = v
        with self.lock:
            self._store()

    def __getitem__(self, k):
        return self.data[k]

    def _load(self):
        tdir = os.path.dirname(os.path.realpath(__file__))
        try:
            with open(os.path.join(tdir, '..', 'local-settings.json')) as f:
                self.data = json.load(f)
        except IOError:
            self.data = {}

    def _store(self):
        tdir = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(tdir, '..', 'local-settings.json'), 'w') as f:
            json.dump(self.data, f)

