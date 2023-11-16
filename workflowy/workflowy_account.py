from workflowy_transport import WorkFlowyTransport

class WorkFlowyAccount:
    """Class to represent and interact with a Workflowy account."""

    def __init__(self, session_id):
        self.transport = WorkFlowyTransport(session_id)
        init_data = self.transport.get_initialization_data()
        self.user = init_data['user']
            

    def get_user_info(self):
        return self.user
