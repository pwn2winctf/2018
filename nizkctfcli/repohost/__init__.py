# -*- encoding: utf-8 -*-


class RepoHost(object):
    def __init__(self, token):
        self.token = token


class APIError(Exception):
    pass
