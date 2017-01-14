# -*- encoding: utf-8 -*-


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
