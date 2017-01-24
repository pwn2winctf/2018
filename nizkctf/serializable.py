# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
                       absolute_import
import os
import json
from base64 import b64encode, b64decode
from .six import viewitems


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
        for k, v in viewitems(self):
            if self._binary_field(k):
                self[k] = b64decode(v)

    def _serialize(self):
        return {k: b64encode(v).decode('utf-8') if self._binary_field(k) else v
                for k, v in viewitems(self)}


class SerializableList(Serializable, list):
    def clear(self):
        del self[:]

    def update(self, l):
        self += l
