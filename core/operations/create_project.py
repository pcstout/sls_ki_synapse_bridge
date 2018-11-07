from core.synapse import Synapse
from synapseclient import Project


class CreateProject:
    """
    Creates a new Project in Synapse.
    """

    def execute(self, payload):
        project_name = payload.get('data').get('projectName')
        project = Synapse.client().store(Project(project_name))
        return project
