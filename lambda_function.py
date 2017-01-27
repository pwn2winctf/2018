# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
     absolute_import
from nizkctf.repohost import RepoHost
from nizkctf.six import to_bytes
import os
import json


def handle_payload(payload, context):
    print(repr(payload))


def handle_apigw(event, context):
    headers = event['params']['header']
    raw_payload = event['body']

    # autenticate the message
    secret = to_bytes(os.getenv('WEBHOOK_SECRET_TOKEN'))
    RepoHost.webhook.auth(secret, headers, raw_payload)

    payload = json.loads(raw_payload)
    handle_payload(payload, context)


def handle_sns(event, context):
    raw_payload = event['Records'][0]['Sns']['Message']
    payload = json.loads(raw_payload)

    # no way to authenticate, but also no need to
    # (publishing to the SNS topic should already be authenticated)

    handle_payload(payload, context)


def lambda_handler(event, context):
    if 'Records' in event:
        handle_sns(event, context)
    elif 'body-json' in event:
        handle_apigw(event, context)
    raise ValueError("Did not recognize a valid event originated by SNS nor "
                     "by API Gateway. Did you configure it correctly?")
