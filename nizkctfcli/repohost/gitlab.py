# -*- encoding: utf-8 -*-

import requests
import re
from ..settings import Settings
from . import RepoHost, APIError, quote_plus


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
        r = requests.post(Settings.gitlab_api_endpoint +
                          'projects/fork/' + quote_plus(source),
                          params=self._params())

        data = r.json()
        if self._has_error(data, 'name', 'has already been taken'):
            # Simulate GitHub API behaviour (return already existing fork)
            username = self._get_user_namespace()
            sink = username + '/' + source.split('/', 2)[1]
            sink_proj = self._get_project(sink)
            forked_from = sink_proj.get('forked_from_project', {})\
                                   .get('path_with_namespace')
            if forked_from != source:
                raise APIError("Project '%s' already exists and is not a fork "
                               "from '%s'. Please remove or rename it to "
                               "allow a fork to be made." % (sink, source))
            data = sink_proj
        else:
            self._raise_for_status(r)

        return data['path_with_namespace'], data['ssh_url_to_repo']

    def _get_user_namespace(self):
        return (n['path'] for n in self._get_namespaces()
                if n['kind'] == 'user').next()

    def _get_namespaces(self):
        r = requests.get(Settings.gitlab_api_endpoint +
                         'namespaces',
                         params=self._params())
        self._raise_for_status(r)
        return r.json()

    def _get_project(self, proj):
        r = requests.get(Settings.gitlab_api_endpoint +
                         'projects/' + quote_plus(proj),
                         params=self._params())
        self._raise_for_status(r)
        return r.json()

    def _params(self):
        return {'private_token': self.token}

    @staticmethod
    def _has_error(data, key, msg):
        return msg in data.get('message', {}).get(key, [])
