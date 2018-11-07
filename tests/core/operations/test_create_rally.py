import pytest
from core.operations.create_rally import CreateRally
import core.post_schema as ps
import kirallymanager.manager as krm
from synapseclient import EntityViewSchema, Schema, Column, Table, Row, RowSet
import time


def test_execute(syn_client, syn_test_helper, mocker):
    mock = mocker.patch.object(krm, 'createRally')
    return_obj = object()
    mock.return_value = return_obj

    payload = ps.example_json('CREATE_RALLY')
    project = CreateRally().execute(payload)
    assert project == return_obj
    mock.assert_called_once_with(
        syn_client, payload['data']['rallyNumber'], payload['data'])


def test_execute_int(syn_client, syn_test_helper, temp_file):
    master_project = syn_test_helper.create_project(prefix='Master Project ')

    master_wiki_template = syn_test_helper.create_file(
        parent=master_project, path=temp_file)
    master_task_wiki_template = syn_test_helper.create_file(
        parent=master_project, path=temp_file)
    master_rally_wiki_template = syn_test_helper.create_file(
        parent=master_project, path=temp_file)

    rally_table_schema = syn_client.store(EntityViewSchema(
        name=syn_test_helper.uniq_name(prefix='Rally View '),
        parent=master_project,
        scopes=[master_project],
        columns=[Column(name='rally', columnType='INTEGER')])
    )

    task_table_schema = syn_client.store(EntityViewSchema(name=syn_test_helper.uniq_name(
        prefix='Task View '), parent=master_project, scopes=[master_project]))

    all_files_schema = syn_client.store(EntityViewSchema(name=syn_test_helper.uniq_name(
        prefix='Master All Files View '), parent=master_project, scopes=[master_project]))

    rally_admin_team = syn_test_helper.create_team(prefix='Rally Admin Team ')

    rally_admin_project = syn_test_helper.create_project(
        prefix='Rally Admin Project ',
        rallyAdminTeamId=rally_admin_team.id,
        rallyTableId=rally_table_schema.id,
        wikiMasterTemplateId=master_wiki_template.id,
        taskTableTemplateId=task_table_schema.id
    )

    payload = ps.example_json('CREATE_RALLY')

    payload['data']['rallyNumber'] = round(time.time())
    payload['data']['rallyAdminProjectId'] = rally_admin_project.id
    payload['data']['wikiTaskTemplateId'] = master_task_wiki_template.id
    payload['data']['wikiRallyTemplateId'] = master_rally_wiki_template.id
    payload['data']['allFilesSchemaId'] = all_files_schema.id
    payload['data']['defaultRallyTeamMembers'] = []

    rally_project = CreateRally().execute(payload)
    assert rally_project != None

    syn_test_helper.dispose_of(rally_project)

    syn_proj = syn_client.get(rally_project.id)
    assert syn_proj.id == rally_project.id
