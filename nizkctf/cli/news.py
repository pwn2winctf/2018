# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
                       absolute_import
import os
import sys
import time
import json
import pysodium
from base64 import b64decode
from ..news import News
from ..team import my_team
from ..text import width

from .teamsecrets import TeamSecrets
from ..team import Team

def pprint(news, team_only):
    '''
    Pretty print news in terminal.

    Args:
        news (list): List of news.
        team_only (bool): whether to display only team directed news or not.
    '''

    if len(news) == 0:
        print('No news yet.')
        return

    team = my_team()

    # FIXME improve filtering
    if team_only:
        news = [n for n in news if n.get('to') == team['name']]
    else:
        news = [n for n in news if 'to' not in n] + [n for n in news if n.get('to') == team['name']]
    
    def decrypt_msg(msg):
        team_pk, team_sk = team['crypt_pk'], TeamSecrets['crypt_sk']
        
        # TODO Check if that's the better approach
        # reference: https://download.libsodium.org/doc/public-key_cryptography/sealed_boxes.html
        return pysodium.crypto_box_seal_open(msg, team_pk, team_sk)

    def decode_news(news):
        # News messages are always in base 64
        news['msg'] = b64decode(news['msg'])
        if 'to' in news:
            # Message was sent to a team, so we need to decrypt it
            news['msg'] = decrypt_msg(news['msg'])

        news['msg'] = news['msg'].decode('utf-8')
        return news
    
    news = [decode_news(n) for n in news]

    to_len = max(width(team['name']), 10)

    # FIXME test formatting
    time_len = msg_len = 20

    def hyph(n):
        return '-'*(n + 2)

    sep = hyph(time_len) + '+' + hyph(to_len) + '+' + hyph(msg_len)

    def fmtcol(s, n):
        return ' ' + s + ' '*(n - width(s) + 1)

    def fmt(time, to, msg):
        return fmtcol(time, time_len) + '|' + \
               fmtcol(to, to_len) + '|' + \
               fmtcol(msg, msg_len)

    print('')
    print(sep)
    print(fmt('Date', 'To', 'Message'))
    print(sep)

    for n in news:
        print(fmt(n['time'], n.get('to', u'all'), n['msg']))

    print(sep)
    print('')