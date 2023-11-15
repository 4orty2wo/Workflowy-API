from workflowy_transport import WorkFlowyTransport

class WorkFlowyAccount:
    """Class to represent and interact with a Workflowy account."""

    def __init__(self, session_id):
        self.transport = WorkFlowyTransport(session_id)
        init_data = self.transport.api_request('get_initialization_data', {})

        self.user = init_data['user']

        self.username = init_data['settings']['username'] if init_data['settings']['username'] else ''
        self.email = init_data['settings']['email'] if init_data['settings']['email'] else ''
        self.itemsCreated = init_data['user']['itemsCreated'] if init_data['user']['itemsCreated'] else ''
        self.monthlyItemQuota = init_data['user']['monthlyItemQuota'] if init_data['user']['monthlyItemQuota'] else ''
        self.dateJoined = init_data['user']['dateJoined'] if init_data['user']['dateJoined'] else ''
            

    def get_user_info(self):
        return self.user


    def get_info(self):
        return {
            'username': self.username,
            'email': self.email,
            'itemsCreated': self.itemsCreated,
            'monthlyItemQuota': self.monthlyItemQuota,
            'dateJoined': self.dateJoined
        }

    # Add additional methods for other account-related functionalities as needed.
