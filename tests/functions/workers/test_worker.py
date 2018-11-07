import pytest
import functions.workers.worker as worker
import core.post_schema as ps


def test_handler(mock_success_operations):
    for operation in ps.operations():
        payload = ps.example_json(operation)
        resp = worker.handler(payload, None)
        assert resp.get('statusCode') == 200

    with pytest.raises(Exception):
        worker.handler('{}', None)
