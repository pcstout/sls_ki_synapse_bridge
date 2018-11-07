import pytest
import os
import boto3
from moto import mock_sqs
import functions.dispatchers.dispatcher as dispatcher
import core.post_schema as ps

SQS_DISPATCH_QUEUE_NAME = 'mock-aws-sqs-dispatcher'


@pytest.fixture
def sqs_client():
    return boto3.client('sqs')


@mock_sqs
def test_handler(monkeypatch, sqs_client):
    queue = sqs_client.create_queue(QueueName=SQS_DISPATCH_QUEUE_NAME)
    monkeypatch.setenv('SQS_DISPATCH_QUEUE_URL', queue.get('QueueUrl'))

    for operation in ps.operations():
        payload = ps.example_json(operation)
        resp = dispatcher.handler(payload, None)
        assert resp.get('statusCode') == 200

    with pytest.raises(Exception):
        dispatcher.handler('{}', None)


@mock_sqs
def test__publish_sqs_message(monkeypatch, sqs_client):
    queue = sqs_client.create_queue(QueueName=SQS_DISPATCH_QUEUE_NAME)
    monkeypatch.setenv('SQS_DISPATCH_QUEUE_URL', queue.get('QueueUrl'))

    for operation in ps.operations():
        payload = ps.example_json(operation)
        assert dispatcher._publish_sqs_message(payload) == True
