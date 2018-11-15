# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
                       absolute_import
import requests
import hashlib
import hmac
from ..settings import Settings
from ..six import to_bytes
from .common import BaseRepoHost, APIError, WebhookAuthError


class GitHubWebhook(object):
    @staticmethod
    def auth(secret, headers, raw_payload):
        received_sig = to_bytes(headers['X-Hub-Signature'])

        h = hmac.new(secret, raw_payload, hashlib.sha1).hexdigest()
        correct_sig = b'sha1=' + to_bytes(h)

        if not hmac.compare_digest(received_sig, correct_sig):
            raise WebhookAuthError()

    @staticmethod
    def adapt_payload(payload):
        # filtering
        if 'pull_request' not in payload:
            return None
        if payload['action'] not in {'opened', 'reopened'}:
            return None
        if payload['pull_request']['base']['repo']['full_name'] != \
           Settings.submissions_project:
            return None
        if payload['pull_request']['base']['ref'] != 'master':
            return None
        # mappings
        return {"mr_id": payload['pull_request']['number'],
                "source_ssh_url": payload['pull_request']['head']['repo']
                                         ['ssh_url'],
                "source_commit": payload['pull_request']['head']['sha'],
                "user_id": payload['pull_request']['user']['id'],
                "username": payload['pull_request']['user']['login']}


class GitHub(BaseRepoHost):
    webhook = GitHubWebhook

    @classmethod
    def get_token(cls, username, password, OTP):
        authorization = {'scopes': 'public_repo',
                         'note': Settings.ctf_name}
        if OTP is None:
            headers = None
        else:
            headers = {'X-GitHub-OTP': OTP}

        r = requests.post(Settings.github_api_endpoint +
                          'authorizations',
                          json=authorization,
                          auth=(username, password),
                          headers=headers)

        data = r.json()

        try:
            if cls._has_error(data, 'already_exists'):
                raise APIError
            if cls._has_error(data, 'Bad credentials'):
                raise BadCreds("Bad Credentials: Please certify that your login and password are correct")
        except APIError:
            print("API Error: Please visit https://github.com/settings/tokens "
                  "and make sure you do not already have a personal "
                  "access token called '%s'" % Settings.ctf_name)
        #except BadCreds:
        #    print("Bad Credentials: Please certify that your login and password are correct")

        cls._raise_for_status(r)

        return data['token']

    @staticmethod
    def get_ssh_url(proj):
        return Settings.github_ssh_url % proj

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

    def mr_comment(self, proj, mr_id, contents):
        r = self.s.post(Settings.github_api_endpoint +
                        'repos/' + proj + '/issues/%d' % mr_id + '/comments',
                        json={'body': contents})
        self._raise_for_status(r)
        return r.json()

    def mr_close(self, proj, mr_id):
        r = self.s.patch(Settings.github_api_endpoint +
                         'repos/' + proj + '/pulls/%d' % mr_id,
                         json={'state': 'closed'})
        self._raise_for_status(r)
        return r.json()

    def mr_accept(self, proj, mr_id, sha):
        r = self.s.put(Settings.github_api_endpoint +
                       'repos/' + proj + '/pulls/%d' % mr_id + '/merge',
                       json={'sha': sha})
        self._raise_for_status(r)
        return r.json()

    def _init_session(self):
        self.s.headers.update({'Authorization': 'token ' + self.token})

    @staticmethod
    def _has_error(data, err_code):
        return any(err.get('code') == err_code
                   for err in data.get('errors', []))
