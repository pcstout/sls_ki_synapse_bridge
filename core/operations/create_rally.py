from core.synapse import Synapse
import kirallymanager.manager as krm


class CreateRally:
    """
    Creates a Rally in Synapse.
    """

    def execute(self, payload):
        rally_data = payload['data']
        rally_number = rally_data['rallyNumber']
        project = krm.createRally(Synapse.client(), rally_number, rally_data)
        return project
