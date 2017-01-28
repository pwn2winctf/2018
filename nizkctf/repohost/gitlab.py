# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
                       absolute_import
import requests
import hmac
import re
from ..settings import Settings
from ..six import to_bytes
from .common import BaseRepoHost, APIError, WebhookAuthError, quote_plus


class GitLabWebhook(object):
    @staticmethod
    def auth(secret, headers, raw_payload):
        received_token = to_bytes(headers['X-Gitlab-Token'])
        if not hmac.compare_digest(secret, received_token):
            raise WebhookAuthError()

    @staticmethod
    def adapt_payload(payload):
        # filtering
        if payload['object_kind'] != 'merge_request':
            return None
        if payload['object_attributes']['action'] not in {'open', 'reopen'}:
            return None
        if payload['object_attributes']['target']['path_with_namespace'] != \
           Settings.submissions_project:
            return None
        if payload['object_attributes']['target_branch'] != 'master':
            return None
        # mappings
        return {"mr_id": payload['object_attributes']['id'],
                "source_ssh_url": payload['object_attributes']['source']
                                         ['git_ssh_url'],
                "source_commit": payload['object_attributes']['last_commit']
                                        ['id'],
                "user_id": payload['object_attributes']['author_id'],
                "username": payload['user']['username']}


class GitLab(BaseRepoHost):
    webhook = GitLabWebhook

    @classmethod
    def get_token(cls, username, password):
        auth = {'login': username,
                'password': password}

        r = requests.post(Settings.gitlab_api_endpoint +
                          'session',
                          json=auth)
        cls._raise_for_status(r)

        data = r.json()
        return data['private_token']

    @staticmethod
    def get_ssh_url(proj):
        return Settings.gitlab_ssh_url % proj

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

    def mr_comment(self, proj, mr_id, contents):
        r = self.s.post(Settings.gitlab_api_endpoint +
                        'projects/' + quote_plus(proj) +
                        '/merge_requests/%d' % mr_id + '/notes',
                        json={'body': contents})
        self._raise_for_status(r)
        return r.json()

    def mr_close(self, proj, mr_id):
        r = self.s.put(Settings.gitlab_api_endpoint +
                       'projects/' + quote_plus(proj) +
                       '/merge_requests/%d' % mr_id,
                       json={'state_event': 'close'})
        self._raise_for_status(r)
        return r.json()

    def mr_accept(self, proj, mr_id, sha):
        r = self.s.put(Settings.gitlab_api_endpoint +
                       'projects/' + quote_plus(proj) +
                       '/merge_requests/%d' % mr_id + '/merge',
                       json={'sha': sha})
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
