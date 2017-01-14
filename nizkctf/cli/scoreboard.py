# -*- encoding: utf-8 -*-

import json
import operator

def pprint(f, top=0):
    '''
    Pretty print scoreboard in terminal.

    Args:
        f (file): File-like object with the scoreboard json.
        top (int): Number of teams to show in scoreboard.

    '''

    data = json.load(f)

    team_max_len = 10
    scores = {}
    for subm in data:
        team = subm['team']
        if team in scores:
            scores[team] += subm['points']
        else:
            scores[team] = subm['points']
        if len(team) > team_max_len:
            team_max_len = len(team)

    team_max_len += 1 # add breathing space
    ranking = sorted(scores.items(), key=operator.itemgetter(1),
            reverse = True)
    fmt = ' %-7s| %-' + str(team_max_len) + 's| %-8s'
    # fix for utf8 crown
    fmtfst = ' %-8s| %-' + str(team_max_len) + 's| %-8s'
    sep = '-'*8+'+' + '-'*(team_max_len+1)+'+' + '-'*8+'-'

    print('')
    print(sep)
    print(fmt%('Pos', 'Team', 'Score'))
    print(sep)

    if top == 0: top = len(ranking)
    for idx, (team, score) in enumerate(ranking[0:top]):
        pos = str(idx+1)
        if idx == 0:
            pos += u' \U0001F451 '
            print(fmtfst%(pos, team, str(score)))
        else:
            print(fmt%(pos, team, str(score)))

    print(sep)
    print('')




