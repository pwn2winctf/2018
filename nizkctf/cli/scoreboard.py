# -*- encoding: utf-8 -*-

import sys
import json
import operator
import tempfile
import subprocess

def rank(f):
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

    data = json.load(f)

    submissions = {}
    scores = {}
    for subm in data:
        team = subm['team']
        if team in scores:
            scores[team] += subm['points']
            submissions[team].append(subm)
        else:
            scores[team] = subm['points']
            submissions[team] = [subm]

    return (sorted(scores.items(), key=operator.itemgetter(1),
            reverse = True), submissions)

def pprint(ranking, top=0):
    '''
    Pretty print scoreboard in terminal.

    Args:
        ranking (list): List of tuples containing teams and scores.
        top (int): Number of teams to show in scoreboard.

    '''

    if top == 0: top = len(ranking)
    team_max_len = 10
    for team, score in ranking[0:top]:
        if len(team) > team_max_len:
            team_max_len = len(team)
    team_max_len += 1 # add breathing space

    fmt = ' %-7s| %-' + str(team_max_len) + 's| %-8s'
    # fix for utf8 crown
    fmtfst = ' %-8s| %-' + str(team_max_len) + 's| %-8s'
    sep = '-'*8+'+' + '-'*(team_max_len+1)+'+' + '-'*8+'-'

    print('')
    print(sep)
    print(fmt%('Pos', 'Team', 'Score'))
    print(sep)

    for idx, (team, score) in enumerate(ranking[0:top]):
        pos = str(idx+1)
        if idx == 0:
            pos += u' \U0001F451 '
            print(fmtfst%(pos, team, str(score)))
        else:
            print(fmt%(pos, team, str(score)))

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

    # generate temporary files with data points
    fnames = []
    for team, _ in ranking[0:top]:
        f = tempfile.NamedTemporaryFile(suffix='-%s.dat'%(team),
            prefix='nizkctf-', delete=True)
        partial = 0
        for subm in submissions[team]:
            partial += subm['points']
            f.write('%s, %d\n'%(subm['time'], partial))
        f.flush()
        fnames.append((team, f))

    # generate gnuplot file
    f = tempfile.NamedTemporaryFile(suffix='.gp',
        prefix='nizkctf-', delete=True)
    f.write('set terminal dumb 120 30\n')
    f.write('set xdata time\n')
    f.write('set datafile sep \',\'\n')
    f.write('set timefmt "%Y-%m-%dT%H:%M:%S"\n')
    f.write('set style data steps\n')
    f.write('plot ')
    fmt = '\'%s\' using 1:2 title \'%s\''
    f.write(fmt%(fnames[0][1].name, fnames[0][0]))
    for team, ft in fnames[1:]:
        f.write(', ')
        f.write(fmt%(ft.name, team))
    f.flush()

    # plot in terminal
    p = subprocess.Popen(['gnuplot', f.name],
        stderr = sys.stderr,
        stdout = sys.stdout)
    p.wait()

    # close/delete files
    f.close()
    for nm, f in fnames:
        f.close()



