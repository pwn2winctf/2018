# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
                       absolute_import
import os
import subprocess
import base64
import pysodium
from .settings import Settings
from .localsettings import LocalSettings
from .repohost import RepoHost


SUBREPO_NAME = 'submissions'

thisdir = os.path.dirname(os.path.realpath(__file__))


class SubRepo(object):
    clone_into = os.path.realpath(os.path.join(thisdir, '..'))
    path = os.path.join(clone_into, SUBREPO_NAME)

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
        repohost = RepoHost.instance()
        upstream_url = repohost.get_ssh_url(Settings.submissions_project)

        if fork:
            forked_project, origin_url = \
                repohost.fork(Settings.submissions_project)
            LocalSettings.forked_project = forked_project
        else:
            origin_url = upstream_url

        cls.git(['clone', origin_url, SUBREPO_NAME], cwd=cls.clone_into)
        cls.git(['remote', 'add', 'upstream', upstream_url])

    @classmethod
    def pull(cls):
        cls.git(['checkout', 'master'])
        cls.git(['pull', '--rebase', 'upstream', 'master'])

    @classmethod
    def push(cls, commit_message='commit', merge_request=True):
        branch = 'master'
        if merge_request:
            branch = cls.random_branch()
            cls.git(['checkout', '-b', branch, 'master'])

        cls.git(['add', '-A'])
        cls.git(['commit', '-m', commit_message],
                returncodes={0, 1})  # do not fail on 'nothing to commit'
        cls.git(['push', '-u', 'origin', branch])

        if merge_request:
            repohost = RepoHost.instance()
            repohost.merge_request(LocalSettings.forked_project,
                                   Settings.submissions_project,
                                   source_branch=branch,
                                   title=commit_message)

    @staticmethod
    def random_branch():
        return base64.b32encode(pysodium.randombytes(10))\
               .decode('utf-8').lower()

    @classmethod
    def git(cls, args, **kwargs):
        returncodes = kwargs.pop('returncodes', {0})
        if 'cwd' not in kwargs:
            kwargs['cwd'] = cls.get_path()

        p = subprocess.Popen(['git'] + args, **kwargs)

        r = None
        if 'stdout' in kwargs:
            r = p.stdout.read()

        returncode = p.wait()
        if returncode not in returncodes:
            raise GitError(returncode)

        return r


class GitError(Exception):
    def __init__(self, returncode, *args):
        self.returncode = returncode
        super(GitError, self).__init__(*args)
