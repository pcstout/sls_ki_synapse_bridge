import core.log
import json as JSON
import jsonschema
import logging
import importlib


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


def execute(payload):
    """
    Executes the payload in the correct operation worker.
    """
    if not validate(payload):
        raise Exception('Invalid JSON object schema.')

    operation = payload['operation']
    module_name = operation.lower()
    class_name = operation.title().replace('_', '')
    cls = getattr(importlib.import_module(
        "core.operations.{0}".format(module_name)), class_name)
    instance = cls()
    return instance.execute(payload)


def example_json(operation):
    """
    Gets the example JSON for a specific operation.
    """
    with open('core/schemas/examples/{0}.json'.format(operation.lower())) as f:
        return JSON.load(f)


def schema():
    """
    Gets the JSON schema.
    """
    with open('core/schemas/post_schema.json') as f:
        return JSON.load(f)


def operations():
    """
    Gets the supported operations from the JSON schema.
    """
    return schema()['properties']['operation']['enum']
