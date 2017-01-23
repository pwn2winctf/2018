# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
import os
import json
from base64 import b64encode, b64decode


class SerializableDict(dict):
    @staticmethod
    def _binary_field(k):
        return False

    def path(self):
        return ''

    def load(self):
        path = self.path()
        if os.path.exists(path):
            with open(path) as f:
                self.update(json.load(f))
            self._unserialize_inplace()

    def save(self):
        with open(self.path(), 'w') as f:
            json.dump(self._serialize(), f)

    def _unserialize_inplace(self):
        for k, v in self.items():
            if self._binary_field(k):
                self[k] = b64decode(v)

    def _serialize(self):
        return {k: b64encode(v).decode('utf-8') if self._binary_field(k) else v
                for k, v in self.items()}
