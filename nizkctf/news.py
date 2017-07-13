# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
     absolute_import
import os
import time
from .six import text_type
from .subrepo import SubRepo
from .serializable import SerializableList


NEWS_FILE = 'news.json'
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'

class News(SerializableList):
    def __init__(self):
        super(News, self).__init__()

    def path(self):
        # TODO set path properly
        p = os.path.join(NEWS_FILE)
        if os.path.exists(p):
            return p
        raise EnvironmentError("The news file (%s) was not found" % p)
