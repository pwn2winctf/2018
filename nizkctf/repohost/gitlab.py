# -*- encoding: utf-8 -*-

import requests
import re
from ..settings import Settings
from .common import BaseRepoHost, APIError, quote_plus


class GitLab(BaseRepoHost):
    @staticmethod
    def get_token(username, password):
        auth = {'login': username,
                'password': password}

        r = self.s.post(Settings.gitlab_api_endpoint +
                        'session',
                        json=auth)
        GitLab._raise_for_status(r)

        data = r.json()
        return data['private_token']

    @staticmethod
    def get_public_url(proj):
        return Settings.gitlab_base_url + proj

    def fork(self, source):
        r = self.s.post(Settings.gitlab_api_endpoint +
                        'projects/fork/' + quote_plus(source))

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

    def merge_request(self, source, target,
                      source_branch='master',
                      target_branch='master',
                      title='Merge Request'):
        target_id = self._get_project(target)['id']

        merge_request = {'source_branch': source_branch,
                         'target_branch': target_branch,
                         'title': title,
                         'target_project_id': target_id}

        r = self.s.post(Settings.gitlab_api_endpoint +
                        'projects/' + quote_plus(source) + '/merge_requests',
                        json=merge_request)
        self._raise_for_status(r)
        return r.json()

    def _get_user_namespace(self):
        return (n['path'] for n in self._get_namespaces()
                if n['kind'] == 'user').next()

    def _get_namespaces(self):
        r = self.s.get(Settings.gitlab_api_endpoint +
                       'namespaces')
        self._raise_for_status(r)
        return r.json()

    def _get_project(self, proj):
        r = self.s.get(Settings.gitlab_api_endpoint +
                       'projects/' + quote_plus(proj))
        self._raise_for_status(r)
        return r.json()

    def _init_session(self):
        self.s.headers.update({'PRIVATE-TOKEN': self.token})

    @staticmethod
    def _has_error(data, key, msg):
        return msg in data.get('message', {}).get(key, [])
