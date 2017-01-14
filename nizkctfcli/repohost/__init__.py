# -*- encoding: utf-8 -*-

from .github import GitHub
from .gitlab import GitLab

from ..settings import Settings
RepoHost = globals()[Settings.repository_host]
