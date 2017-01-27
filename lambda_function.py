# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
     absolute_import
from nizkctf.repohost import RepoHost
from nizkctf.six import to_bytes
import os
import json
import base64
import tempfile


def handle_payload(payload, context):
    print('Payload recognized correctly:\n')
    print(repr(payload))
    print('\nAfter adapted:\n')
    print(repr(RepoHost.webhook.adapt_payload(payload)))
    print()

    setup_environment()


def handle_apigw(event, context):
    headers = event['params']['header']
    raw_payload = event['body']

    # autenticate the message
    secret = to_bytes(os.getenv('WEBHOOK_SECRET_TOKEN'))
    RepoHost.webhook.auth(secret, headers, raw_payload)

    payload = json.loads(raw_payload)
    return handle_payload(payload, context)


def handle_sns(event, context):
    raw_payload = event['Records'][0]['Sns']['Message']
    payload = json.loads(raw_payload)

    # no way to authenticate, but also no need to
    # (publishing to the SNS topic should already be authenticated)

    return handle_payload(payload, context)


def setup_environment():
    root = os.getenv('LAMBDA_TASK_ROOT')
    bin_dir = os.path.join(root, 'bin')
    os.environ['PATH'] += ':' + bin_dir
    os.environ['GIT_EXEC_PATH'] = bin_dir

    ssh_dir = tempfile.mkdtemp()

    ssh_identity = os.path.join(ssh_dir, 'identity')
    with os.fdopen(os.open(ssh_identity, os.O_WRONLY | os.O_CREAT, 0o600),
                   'w') as f:
        f.write(base64.b64decode(os.getenv('SSH_IDENTITY')))
    del os.environ['SSH_IDENTITY']

    ssh_config = os.path.join(ssh_dir, 'config')
    with open(ssh_config, 'w') as f:
        f.write('StrictHostKeyChecking yes\n'
                'IdentityFile %s\n'
                'UserKnownHostsFile %s\n' %
                (ssh_identity, os.path.join(root, 'known_hosts')))

    os.environ['GIT_SSH_COMMAND'] = 'ssh -F %s' % ssh_config


def lambda_handler(event, context):
    if 'Records' in event:
        return handle_sns(event, context)
    elif 'body' in event:
        return handle_apigw(event, context)
    raise ValueError("Did not recognize a valid event originated by SNS nor "
                     "by API Gateway. Did you configure it correctly?")
