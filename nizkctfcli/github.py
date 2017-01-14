# -*- encoding: utf-8 -*-

import requests
import json
from .settings import Settings
from .repohost import RepoHost


class GitHub(RepoHost):
    @staticmethod
    def get_token(username, password):
        authorization = {'scopes': 'repo',
                         'note': Settings.ctf_name}
        requests.post(Settings.github_api_endpoint + 'authorizations',
                      data=json.dumps(authorization),
                      auth=(username, password))
