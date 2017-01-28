# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
     absolute_import
from nizkctf.settings import Settings
from nizkctf.subrepo import SubRepo
from nizkctf.repohost import RepoHost
from nizkctf.proposal import consider_proposal
from nizkctf.six import to_bytes
import os
import json
import base64
import tempfile
import traceback


def run(merge_info):
    SubRepo.set_clone_into(tempfile.mkdtemp())

    # Prepare git and ssh for usage inside the container
    setup_environment()

    # Merge proposal if changes are valid
    consider_proposal(merge_info)


def handle_payload(payload, context):
    merge_info = RepoHost.webhook.adapt_payload(payload)

    if not merge_info:
        # Message not of our interest (e.g. merge request closed)
        return

    try:
        run(merge_info)
    except:
        # Do not re-raise, we do not want automatic retries
        traceback.print_exc()
        # Send tracking number to the user
        send_cloudwatch_info(merge_info, context)


def send_cloudwatch_info(merge_info, context):
    proj = Settings.submissions_project
    mr_id = merge_info['mr_id']

    comment = "Sorry. A failure has occurred when processing your proposal. " \
              "Please contact support and present the following info:\n\n" \
              "**Stream name**: %s\n" \
              "**Request ID**: %s\n" % \
              (context.log_stream_name, context.aws_request_id)

    repohost = RepoHost.instance()
    repohost.mr_comment(proj, mr_id, comment)
    repohost.mr_close(proj, mr_id)


def handle_apigw(event, context):
    headers = event['params']['header']
    raw_payload = event['body']

    # autenticate the message
    secret = to_bytes(os.getenv('WEBHOOK_SECRET_TOKEN'))
    RepoHost.webhook.auth(secret, headers, to_bytes(raw_payload))
    del os.environ['WEBHOOK_SECRET_TOKEN']

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
