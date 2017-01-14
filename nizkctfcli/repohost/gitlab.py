# -*- encoding: utf-8 -*-

import requests
from ..settings import Settings
from . import RepoHost, APIError


class GitLab(RepoHost):
    @staticmethod
    def get_token(username, password):
        auth = {'login': username,
                'password': password}

        r = requests.post(Settings.gitlab_api_endpoint +
                          'session',
                          json=auth)
        r.raise_for_status()

        data = r.json()
        return data['private_token']
