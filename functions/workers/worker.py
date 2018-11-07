import json
import core.log
import logging
import json as JSON
from core.param_store import ParamStore
import core.post_schema as ps


def handler(event, context):
    """
    Handles the worker event.
    """
    logging.debug('Event received: {}'.format(JSON.dumps(event)))

    if not ps.validate(event):
        raise Exception('Invalid JSON object schema.')

    if not ps.execute(event):
        raise Exception('Failed to execute.')

    response = {
        "statusCode": 200
    }

    logging.debug('Event received: {}'.format(JSON.dumps(event)))
    return response
