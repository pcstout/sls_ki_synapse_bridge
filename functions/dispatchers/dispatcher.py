import os
import core.log
import logging
import json as JSON
import boto3
from core.param_store import ParamStore
import core.post_schema as ps


def handler(event, context):
    """
    Handles the dispatch event.
    """
    logging.debug('Event received: {}'.format(JSON.dumps(event)))

    if not ps.validate(event):
        raise Exception('Invalid JSON object schema.')

    if not _publish_sqs_message(event):
        raise Exception('Failed to publish SQS message.')

    response = {
        "statusCode": 200
    }

    logging.debug('Event received: {}'.format(JSON.dumps(event)))
    return response


def _publish_sqs_message(message):
    """
    Publishes a message to SQS so it can trigger a worker.
    """
    sqs_response = None
    try:
        message_json = JSON.dumps(message)

        logging.debug('Publish SQS Message: {}'.format(message_json))

        client = boto3.client('sqs')
        sqs_response = client.send_message(
            QueueUrl=ParamStore.SQS_DISPATCH_QUEUE_URL(), MessageBody=message_json)

        logging.debug('Publish SQS Response: {}'.format(
            JSON.dumps(sqs_response)))
    except Exception as e:
        logging.exception(e)

    return sqs_response and sqs_response.get('ResponseMetadata').get('HTTPStatusCode') == 200
