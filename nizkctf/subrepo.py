# -*- encoding: utf-8 -*-

import os
import subprocess
from .settings import Settings
from .repohost import RepoHost


SUBREPO_NAME = 'submissions'

thisdir = os.path.dirname(os.path.realpath(__file__))
repohost = RepoHost.get_instance()


class SubRepo(object):
    path = os.path.realpath(os.path.join(thisdir, '..', SUBREPO_NAME))

    @classmethod
    def get_path(cls, subpath=''):
        if os.path.exists(cls.path):
            return os.path.join(cls.path, subpath)
        raise EnvironmentError("The subrepository path ('%s') was not created "
                               "yet. Please call 'ctf login' to get it cloned "
                               "before performing any further actions." %
                               cls.path)

    @classmethod
    def clone(cls, fork=True):
        if fork:
            pass

        pass

    @classmethod
    def sync(cls, commit_message='commit', merge_request=True):
        cls.git(['add', '-A'])
        cls.git(['commit', '-m', commit_message])
        cls.git(['pull', 'upstream', 'master'])
        cls.git(['push', '-u', 'origin', 'master'])

        if merge_request:
            pass

    @classmethod
    def git(cls, args, **kwargs):
        p = subprocess.Popen(['git'] + args, cwd=cls.get_path(), **kwargs)
        returncode = p.wait()
        if returncode != 0:
            raise GitError(returncode)


class GitError(Exception):
    def __init__(self, returncode, *args):
        self.returncode = returncode
        super(GitError, self).__init__(*args)
