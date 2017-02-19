# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
     absolute_import
import os
try:
    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler
except ImportError:
    from http.server import SimpleHTTPRequestHandler, HTTPServer
from ..settings import Settings
from ..subrepo import SubRepo


def handler(routes, root_redir=None):
    class RequestHandler(SimpleHTTPRequestHandler):
        protocol_version = 'HTTP/1.0'

        def do_GET(self):
            if root_redir and self.path == '/':
                self.send_response(301)
                self.send_header("Location", root_redir)
                self.end_headers()
                return
            SimpleHTTPRequestHandler.do_GET(self)

        def translate_path(self, path):
            path = path.split('?', 1)[0]
            path = path.split('#', 1)[0]

            root = None
            for url_prefix, cur_root in routes:
                if path.startswith(url_prefix):
                    root = cur_root
                    path = path[len(url_prefix):]
                    break

            if root:
                os.chdir(root)
                return SimpleHTTPRequestHandler.translate_path(self, path)

            return ''

    return RequestHandler


def main(port=8000):
    thisdir = os.path.dirname(os.path.realpath(__file__))
    rootdir = os.path.realpath(os.path.join(thisdir, os.pardir, os.pardir))
    subdir = SubRepo.get_path()

    ctf = os.path.basename(rootdir)
    submissions = os.path.basename(Settings.submissions_project)

    routes = [
        ('/%s' % ctf, rootdir),
        ('/%s' % submissions, subdir),
    ]

    HandlerClass = handler(routes, '/%s' % ctf)

    server_address = ('', port)
    httpd = HTTPServer(server_address, HandlerClass)
    sa = httpd.socket.getsockname()
    print("Serving HTTP on", sa[0], "port", sa[1], "...")
    httpd.serve_forever()
