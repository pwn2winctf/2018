# -*- encoding: utf-8 -*-

import os
import requests
import urllib
import codecs


TOKENFILE_NAME = '.token'

thisdir = os.path.dirname(os.path.realpath(__file__))


class BaseRepoHost(object):
    @classmethod
    def login(cls, username=None, password=None, token=None):
        if not token and (username and password):
            token = cls.get_token(username, password)
        if not token:
            raise ValueError("Pass either a token or an username/password")
        TokenFile.create(token)

    @classmethod
    def get_instance(cls):
        return cls(TokenFile.get())

    def __init__(self, token):
        self.token = token
        self.s = requests.Session()
        self._init_session()

    def _init_session(self):
        pass

    @classmethod
    def get_token(cls, username, password):
        pass

    @staticmethod
    def _raise_for_status(r):
        try:
            r.raise_for_status()
        except Exception as e:
            raise APIError(r.text, e)


class TokenFile(object):
    path = os.path.join(thisdir, '..', '..', TOKENFILE_NAME)

    @classmethod
    def create(cls, token):
        with codecs.open(cls.path, 'w', 'utf-8') as f:
            f.write(token + '\n')

    @classmethod
    def get(cls):
        if not os.path.exists(cls.path):
            raise EnvironmentError("The token file ('%s') was not created yet "
                                   "Please call 'ctf login' to get it created "
                                   "before performing any further actions." %
                                   cls.path)

        with codecs.open(cls.path, 'w', 'utf-8') as f:
            return f.read().strip()


class APIError(Exception):
    pass


quote_plus = urllib.quote_plus if hasattr(urllib, 'quote_plus') else \
    urllib.parse.quote_plus
