# -*- encoding: utf-8 -*-

import requests
from ..settings import Settings
from . import RepoHost, APIError


class GitHub(RepoHost):
    @staticmethod
    def get_token(username, password):
        authorization = {'scopes': 'public_repo',
                         'note': Settings.ctf_name}

        r = requests.post(Settings.github_api_endpoint +
                          'authorizations',
                          json=authorization,
                          auth=(username, password))

        if r.status_code == 422:
            raise APIError("Please visit https://github.com/settings/tokens "
                           "and make sure you do not already have a personal "
                           "access token called '%s'" % Settings.ctf_name)

        r.raise_for_status()

        data = r.json()
        return data['token']
