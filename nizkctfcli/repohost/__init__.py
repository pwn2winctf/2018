# -*- encoding: utf-8 -*-

import urllib


class RepoHost(object):
    def __init__(self, token):
        self.token = token

    @staticmethod
    def _raise_for_status(r):
        try:
            r.raise_for_status()
        except Exception as e:
            raise APIError(r.json(), e)


class APIError(Exception):
    pass


quote_plus = urllib.quote_plus if hasattr(urllib, 'quote_plus') else \
    urllib.parse.quote_plus
