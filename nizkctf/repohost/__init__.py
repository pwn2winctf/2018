# -*- encoding: utf-8 -*-

from __future__ import absolute_import, division, print_function
from .github import GitHub
from .gitlab import GitLab

from ..settings import Settings
RepoHost = globals()[Settings.repository_host]
