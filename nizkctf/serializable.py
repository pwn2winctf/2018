# -*- encoding: utf-8 -*-

from __future__ import absolute_import, division, print_function
import os
import json
from base64 import b64encode, b64decode


class Serializable(object):
    def __init__(self):
        self.load()

    def load(self):
        if self.exists():
            self.clear()
            with open(self.path()) as f:
                self.update(json.load(f))
            self._unserialize_inplace()

    def save(self):
        with open(self.path(), 'w') as f:
            json.dump(self._serialize(), f)

    def exists(self):
        return os.path.exists(self.path())

    def _unserialize_inplace(self):
        pass

    def _serialize(self):
        return self


class SerializableDict(Serializable, dict):
    @staticmethod
    def _binary_field(k):
        return False

    def _unserialize_inplace(self):
        for k, v in self.items():
            if self._binary_field(k):
                self[k] = b64decode(v)

    def _serialize(self):
        return {k: b64encode(v).decode('utf-8') if self._binary_field(k) else v
                for k, v in self.items()}


class SerializableList(Serializable, list):
    def clear(self):
        del self[:]

    def update(self, l):
        self += l
