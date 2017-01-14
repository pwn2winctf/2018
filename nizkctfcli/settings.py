# -*- encoding: utf-8 -*-

import os
import json


class Settings(object):
    # Placeholders for autocompletion
    ctf_name = ''
    repository_host = ''
    submissions_project = ''
    github_api_endpoint = ''
    github_base_url = ''
    gitlab_api_endpoint = ''
    gitlab_base_url = ''


def load():
    """ Load settings from json file """
    thisdir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(thisdir, '..', 'settings.json')) as f:
        settings = json.load(f)
        assert isinstance(settings, dict)
        for k, v in settings.items():
            setattr(Settings, k, v)

load()
