# -*- encoding: utf-8 -*-

import requests
import urllib


class BaseRepoHost(object):
    def __init__(self, token):
        self.token = token
        self.s = requests.Session()
        self._init_session()

    def _init_session(self):
        pass

    @staticmethod
    def _raise_for_status(r):
        try:
            r.raise_for_status()
        except Exception as e:
            raise APIError(r.text, e)


class APIError(Exception):
    pass


quote_plus = urllib.quote_plus if hasattr(urllib, 'quote_plus') else \
    urllib.parse.quote_plus
