# -*- encoding: utf-8 -*-

import requests
from ..settings import Settings
from .common import BaseRepoHost, APIError


class GitHub(BaseRepoHost):
    @classmethod
    def get_token(cls, username, password):
        authorization = {'scopes': 'public_repo',
                         'note': Settings.ctf_name}

        r = self.s.post(Settings.github_api_endpoint +
                        'authorizations',
                        json=authorization,
                        auth=(username, password))

        data = r.json()

        if cls._has_error(data, 'already_exists'):
            raise APIError("Please visit https://github.com/settings/tokens "
                           "and make sure you do not already have a personal "
                           "access token called '%s'" % Settings.ctf_name)
        cls._raise_for_status(r)

        return data['token']

    @staticmethod
    def get_public_url(proj):
        return Settings.github_base_url + proj

    def fork(self, source):
        r = self.s.post(Settings.github_api_endpoint +
                        'repos/' + source + '/forks')
        self._raise_for_status(r)
        data = r.json()
        return data['full_name'], data['ssh_url']

    def merge_request(self, source, target,
                      source_branch='master',
                      target_branch='master',
                      title='Pull Request'):
        source_branch = source.split('/', 2)[0] + ':' + source_branch

        pull_request = {'head': source_branch,
                        'base': target_branch,
                        'title': title}

        r = self.s.post(Settings.github_api_endpoint +
                        'repos/' + target + '/pulls',
                        json=pull_request)
        self._raise_for_status(r)
        return r.json()

    def _init_session(self):
        self.s.headers.update({'Authorization': 'token ' + self.token})

    @staticmethod
    def _has_error(data, err_code):
        return any(err.get('code') == err_code
                   for err in data.get('errors', []))
