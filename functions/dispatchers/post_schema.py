import core.log
import json as JSON
import jsonschema
import logging

OPERATIONS = ['CREATE_PROJECT', 'SYNC_USERS']


def validate(payload):
    """
    Validates a payload against the POST schema.
    """
    try:
        jsonschema.validate(payload, schema())
        return True
    except jsonschema.ValidationError as e:
        logging.exception(e)
        return False


def example_json(operation):
    """
    Gets some example JSON
    """
    with open('functions/dispatchers/schemas/examples/{0}.json'.format(operation.lower())) as f:
        return JSON.load(f)


def schema():
    """
    Gets the JSON schema.
    """
    with open('functions/dispatchers/schemas/post_schema.json') as f:
        return JSON.load(f)
