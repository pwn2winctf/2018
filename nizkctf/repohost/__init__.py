# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from .github import GitHub
from .gitlab import GitLab

from ..settings import Settings
RepoHost = globals()[Settings.repository_host]
