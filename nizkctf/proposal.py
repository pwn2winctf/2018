# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
     absolute_import
import os
import re
import subprocess
from .settings import Settings
from .repohost import RepoHost
from .subrepo import SubRepo
from .team import Team, TEAM_FILE, SUBMISSIONS_FILE
from .acceptedsubmissions import AcceptedSubmissions


DIFF_MAX_SIZE = 5000
PUSH_RETRIES = 3


def consider_proposal(merge_info):
    # Clone official repository
    SubRepo.clone(fork=False)

    # Fetch proposal
    add_proposal_remote(merge_info)

    # Get commits between which to compute diffs
    commit = merge_info['source_commit']
    merge_base = get_merge_base(commit)

    # Check if there is a single commit in the merge request
    check_rev_count(merge_base, commit)
    # Check if the diff is not too big
    check_diff_size(merge_base, commit)
    # Check if only allowed ops were done (add/modify)
    check_no_unallowed_ops(merge_base, commit)
    # Validate and get files added/modified
    added_file = get_added_file(merge_base, commit)
    modified_file = get_modified_file(merge_base, commit)

    if added_file and modified_file:
        raise ValueError("We only allow commits doing a single operation")

    changed_file = added_file or modified_file
    if not changed_file:
        raise ValueError("You managed to make a commit which does nothing")
    changed_basename = os.path.basename(changed_file)

    if added_file and changed_basename == TEAM_FILE:
        team_registration(merge_info, added_file)
    elif changed_file and changed_basename == SUBMISSIONS_FILE:
        flag_submission(merge_info, changed_file)
    else:
        raise ValueError("unrecognized operation")


def team_registration(merge_info, added_file):
    # Checkout first to get the new team file
    commit = merge_info['source_commit']
    checkout(commit)

    team = filename_owner(added_file)
    team.validate()

    # Back to branch, do local modifications
    checkout('master')
    add_member(team, merge_info)

    accept_proposal(merge_info)

    retry_push('Add member who registered team')


def flag_submission(merge_info, modified_file):
    team = filename_owner(modified_file)
    challs_before = set(team.submissions().challs())

    # Checkout to get the newly submitted challenge
    commit = merge_info['source_commit']
    checkout(commit)

    challs_after = set(team.submissions().challs())

    new_challs = challs_after - challs_before
    assert len(new_challs) == 1
    chall, = new_challs

    # Back to branch, do local modifications
    checkout('master')
    add_member(team, merge_info)

    AcceptedSubmissions().add(chall.id, chall['points'], team.id)

    accept_proposal(merge_info)

    retry_push('Accept challenge solution')


def add_member(team, merge_info):
    team_dir = team.dir()
    if not os.path.exists(team_dir):
        os.makedirs(team_dir)

    team.members().add(id=merge_info['user_id'],
                       username=merge_info['username'])


def accept_proposal(merge_info):
    proj = Settings.submissions_project
    mr_id = merge_info['mr_id']
    commit = merge_info['source_commit']

    repohost = RepoHost.instance()
    repohost.mr_accept(proj, mr_id, commit)


def retry_push(commit_message, retries=PUSH_RETRIES):
    for retry in range(retries):
        try:
            SubRepo.pull()
            SubRepo.push(commit_message, merge_request=False)
            break
        except:
            if retry == retries - 1:
                raise


def filename_owner(filename):
    team_id, basename = os.path.split(filename)
    return Team(id=team_id)


def add_proposal_remote(merge_info):
    url = merge_info['source_ssh_url']
    SubRepo.git(['remote', 'add', 'proposal', url])
    SubRepo.git(['fetch', 'proposal'])


def checkout(commit):
    SubRepo.git(['checkout', commit])


def get_added_file(src, dest):
    return get_file(src, dest, 'A', {TEAM_FILE, SUBMISSIONS_FILE})


def get_modified_file(src, dest):
    return get_file(src, dest, 'M', {SUBMISSIONS_FILE})


def get_file(src, dest, filt, whitelist):
    stats = diff_stats(src, dest, ['--diff-filter=' + filt])
    if len(stats) == 0:
        return None
    if len(stats) != 1:
        raise ValueError("We only allow a single file to be added or modified "
                         "per commit")

    stat, = stats
    lines_added, lines_removed, filename = stat
    if lines_removed != 0:
        raise ValueError("We do not allow lines to be removed from files")
    if lines_added != 1:
        raise ValueError("Changes can only add a single line to a file")

    check_whitelist(filename, whitelist)
    return filename


def check_no_unallowed_ops(src, dest):
    stats = diff_stats(src, dest, ['--diff-filter=am'])
    if len(stats) != 0:
        raise ValueError("We only allow files to be added or modified")


def check_whitelist(filename, whitelist):
    basename = os.path.basename(filename)
    if basename not in whitelist:
        raise ValueError("Filename '%s' not in the whitelist" % basename)


def diff_stats(src, dest, args=[]):
    stats = SubRepo.git(['diff', '--numstat'] + args + [src, dest],
                        stdout=subprocess.PIPE)
    lines = [re.split(r'\s+', line.strip(), 2) for line in
             stats.split('\n')]
    lines = [line for line in lines if line != ['']]
    return [(int(lines_added), int(lines_removed), filename)
            for lines_added, lines_removed, filename
            in lines]


def check_rev_count(src, dest):
    revs = int(SubRepo.git(['rev-list', '--count', src+'...'+dest],
                           stdout=subprocess.PIPE).strip())

    if revs != 1:
        raise ValueError("We only accept a single commit per merge request")


def check_diff_size(src, dest):
    diff = SubRepo.git(['diff', '--no-color', '-U0', src, dest],
                       stdout=subprocess.PIPE)

    if len(diff) > DIFF_MAX_SIZE:
        raise ValueError("Diff size (%d bytes) is above the maximum permitted "
                         "(%d bytes)" % (len(diff), DIFF_MAX_SIZE))


def get_merge_base(commit):
    merge_base = SubRepo.git(['merge-base', 'origin/master', commit],
                             stdout=subprocess.PIPE).strip()
    return merge_base
