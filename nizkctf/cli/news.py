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


TIME_DISPLAY_FORMAT = '%Y-%m-%d %H:%M:%S'


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

    def decrypt_news(news_item):
        assert('to' in news_item)

        # Message was sent to a team, so we need to decode and decrypt it
        decoded_msg = b64decode(news_item['msg'].encode("utf-8"))
        try:
            team_pk, team_sk = team['crypt_pk'], TeamSecrets['crypt_sk']
            decrypted_msg = pysodium.crypto_box_seal_open(decoded_msg,
                                                          team_pk,
                                                          team_sk)
        except:
            decrypted_msg = b'<Failed to decrypt>'

        news_item['msg'] = decrypted_msg.decode("utf-8")
        return news_item

    def filter_news(news):
        # Filter items based on team_only flag, applying decryptionif needed
        to_filter = [team['name']] + ([] if team_only else [None])
        for news_item in news:
            to = news_item.get('to')
            if to in to_filter:
                yield decrypt_news(news_item) if to else news_item

    news = filter_news(news)

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

    def fmtime(timestamp):
        return time.strftime(TIME_DISPLAY_FORMAT, time.localtime(timestamp))

    print('')
    print(sep)
    print(fmt('Date', 'To', 'Message'))
    print(sep)

    for news_item in news:
        print(fmt(fmtime(news_item['time']),
                  news_item.get('to', 'all'), news_item['msg']))

    print(sep)
    print('')
