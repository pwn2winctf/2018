# -*- encoding: utf-8 -*-

import requests
import urllib
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
        GitLab._raise_for_status(r)

        data = r.json()
        return data['private_token']

    def fork(self, source):
        data = self._post_data()
        r = requests.post(Settings.gitlab_api_endpoint +
                          'projects/fork/' + quote_plus(source),
                          json=data)
        self._raise_for_status(r)
        # ssh_url_to_repo
        # id or path_with_namespace
        return r.json()

    def _post_data(self):
        return {'private_token': self.token}


if hasattr(urllib, 'quote_plus'):
    quote_plus = urllib.quote_plus
else:
    quote_plus = urllib.parse.quote_plus
