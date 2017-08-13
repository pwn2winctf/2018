# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
                       absolute_import
import sys
import json
import operator
import tempfile
import subprocess
import codecs
from ..team import Team
from ..text import width
from ..six import viewitems
from ..acceptedsubmissions import AcceptedSubmissions


def rank():
    '''
    Compute ranking given a submissions file.

    Args:
        f (file): File-like object with the submissions json.

    Returns:
        List containing the computed ranking for the submission list.
        The result is in the following format:

        (team, score)

        And a map containing submissions sorted by team.
    '''

    submissions = {}
    scores = []
    for team in AcceptedSubmissions()['standings']:
        team_id = Team(name=team['team']).id
        submissions[team_id] = [sub for sub in team['taskStats'].values()]
        submissions[team_id] = sorted(submissions[team_id],
                                      key=operator.itemgetter('time'))
        scores.append((team_id, team['score']))

    return (scores, submissions)


def pprint(ranking, top=0, show_names=False):
    '''
    Pretty print scoreboard in terminal.

    Args:
        ranking (list): List of tuples containing teams and scores.
        top (int): Number of teams to show in scoreboard.

    '''

    if top == 0:
        top = len(ranking)

    if len(ranking) == 0:
        print('Nobody scored yet.')
        return

    ranking = ranking[:top]

    if show_names:
        ranking = [(Team(id=team)['name'], score) for team, score in ranking]

    team_len = max(width(team) for team, score in ranking)
    team_len = max(team_len, 10)

    pos_len = score_len = 6

    def hyph(n):
        return '-'*(n + 2)

    sep = hyph(pos_len) + '+' + hyph(team_len) + '+' + hyph(score_len)

    def fmtcol(s, n):
        return ' ' + s + ' '*(n - width(s) + 1)

    def fmt(pos, team, score):
        return fmtcol(pos, pos_len) + '|' + \
               fmtcol(team, team_len) + '|' + \
               fmtcol(score, score_len)

    print('')
    print(sep)
    print(fmt('Pos', 'Team', 'Score'))
    print(sep)

    for idx, (team, score) in enumerate(ranking):
        pos = '%d' % (idx + 1)
        print(fmt(pos, team, '%d' % score))

    print(sep)
    print('')


def plot(ranking, submissions, top=3):
    '''
    Plot points for top teams.

    Args:
        ranking (list): List containing teams and scores sorted in
            descending order.
        submissions (dict): Dict [team] -> submission list.
        top (int): Number of teams to appear in chart.
    '''
    if len(ranking) == 0:
        return

    # generate temporary files with data points
    fnames = []
    for team, _ in ranking[0:top]:
        f = tempfile.NamedTemporaryFile(suffix='.dat',
                                        prefix='nizkctf-', delete=True)
        w = codecs.getwriter('utf-8')(f)
        partial = 0
        for subm in submissions[team]:
            partial += subm['points']
            w.write('%s, %d\n' % (subm['time'], partial))
        w.flush()
        fnames.append((team, f))

    # generate gnuplot file
    f = tempfile.NamedTemporaryFile(suffix='.gp',
                                    prefix='nizkctf-', delete=True)
    w = codecs.getwriter('utf-8')(f)
    w.write('set terminal dumb 120 30\n')
    w.write('set xdata time\n')
    w.write('set datafile sep \',\'\n')
    w.write('set timefmt "%s"\n')
    w.write('set style data steps\n')
    w.write('plot ')
    fmt = '\'%s\' using 1:2 title \'%s\''
    w.write(fmt % (fnames[0][1].name, fnames[0][0]))
    for team, ft in fnames[1:]:
        w.write(', ')
        w.write(fmt % (ft.name, team))
    w.flush()

    # plot in terminal
    p = subprocess.Popen(['gnuplot', f.name],
                         stderr=sys.stderr,
                         stdout=sys.stdout)
    p.wait()

    # close/delete files
    f.close()
    for nm, f in fnames:
        f.close()
