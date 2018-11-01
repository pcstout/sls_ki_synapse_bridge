import tests.test_helper
import pytest
import json as JSON
import functions.dispatchers.post_schema as ps


def test_schema():
    schema = ps.schema()
    assert schema != None


def test_operations():
    assert ps.operations() == ["CREATE_RALLY", "CREATE_PROJECT", "SYNC_USERS"]


def test_example_json():
    for operation in ps.operations():
        example = ps.example_json(operation)
        assert example != None


def test_validate():
    payload = '{ "f": true  }'
    assert ps.validate(payload) == False

    for operation in ps.operations():
        payload = ps.example_json(operation)
        assert ps.validate(payload) == True

        payload['operation'] = 'FAIL'
        assert ps.validate(payload) == False
