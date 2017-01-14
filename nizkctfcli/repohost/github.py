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

        if GitHub._has_error(data, 'already_exists'):
            raise APIError("Please visit https://github.com/settings/tokens "
                           "and make sure you do not already have a personal "
                           "access token called '%s'" % Settings.ctf_name)
        GitHub._raise_for_status(r)

        return data['token']

    def fork(self, source):
        r = requests.post(Settings.github_api_endpoint +
                          'repos/' + source + '/forks',
                          params=self._params())
        self._raise_for_status(r)
        data = r.json()
        return data['full_name'], data['ssh_url']

    def _params(self):
        return {'access_token': self.token}

    @staticmethod
    def _has_error(data, err_code):
        return any(err.get('code') == err_code
                   for err in data.get('errors', []))
