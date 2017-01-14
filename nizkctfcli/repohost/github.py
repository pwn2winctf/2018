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

        data = r.json()

        if any(err.get('code') == 'already_exists'
               for err in data.get('errors', [])):
            raise APIError("Please visit https://github.com/settings/tokens "
                           "and make sure you do not already have a personal "
                           "access token called '%s'" % Settings.ctf_name)

        GitHub._raise_for_status(r)

        return data['token']

    def fork(self, source):
        params = self._params()
        r = requests.post(Settings.github_api_endpoint +
                          'repos/' + source + '/forks',
                          params=params)
        self._raise_for_status(r)
        # ssh_url
        # id or full_name
        return r.json()

    def _params(self):
        return {'access_token': self.token}
