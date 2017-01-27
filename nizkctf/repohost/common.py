# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
                       absolute_import
import os
import requests
import urllib
import codecs
from ..localsettings import LocalSettings


class BaseRepoHost(object):
    @classmethod
    def login(cls, username=None, password=None, token=None):
        if not token and (username and password):
            token = cls.get_token(username, password)
        if not token:
            raise ValueError("Pass either a token or an username/password")
        LocalSettings.token = token

    @classmethod
    def instance(cls):
        return cls(LocalSettings.token)

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


class APIError(Exception):
    pass


class WebhookAuthError(Exception):
    pass


quote_plus = urllib.quote_plus if hasattr(urllib, 'quote_plus') else \
    urllib.parse.quote_plus
