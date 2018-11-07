import pytest
from core.operations.create_project import CreateProject
import core.post_schema as ps


def test_execute(syn_test_helper):
    payload = ps.example_json('CREATE_PROJECT')
    payload['data']['projectName'] = syn_test_helper.uniq_name(
        prefix='Test Project-')
    project = CreateProject().execute(payload)
    syn_test_helper.dispose_of(project)
