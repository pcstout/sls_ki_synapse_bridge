import pytest
import tempfile
import os
import json
from tests.synapse_test_helper import SynapseTestHelper
from core.param_store import ParamStore
from core.operations import create_project, create_rally, sync_users
from core.synapse import Synapse

# Load Environment variables.
with open('private.test.env.json') as f:
    config = json.load(f).get('test')

    # Validate required properties are present
    for prop in['SYNAPSE_USERNAME', 'SYNAPSE_PASSWORD']:
        if not prop in config or not config[prop]:
            raise Exception(
                'Property: "{0}" is missing in private.test.env.json'.format(prop))

    for key, value in config.items():
        os.environ[key] = value


@pytest.fixture(scope='session')
def syn_client():
    return Synapse.client()


@pytest.fixture
def syn_test_helper():
    """
    Provides the SynapseTestHelper as a fixture.
    """
    helper = SynapseTestHelper()
    yield helper
    helper.dispose()


@pytest.fixture
def operation_classes():
    """
    Provides all the core.operations classes.
    Make sure to update this list when new operations are added.
    """
    return [create_project.CreateProject, create_rally.CreateRally, sync_users.SyncUsers]


@pytest.fixture
def mock_success_operations(mocker, operation_classes):
    """
    Mocks all the core.operations so they return successfully.
    """
    mocks = []
    for c in operation_classes:
        mock = mocker.patch.object(c, 'execute')
        mock.return_value = object()
        mocks.append(mock)
    return mocks


@pytest.fixture
def temp_file(syn_test_helper):
    """
    Generates a temp file containing the SynapseTestHelper.uniq_name
    """
    fd, tmp_filename = tempfile.mkstemp()
    with os.fdopen(fd, 'w') as tmp:
        tmp.write(syn_test_helper.uniq_name())
    return tmp_filename
