from workflowy_transport import WorkFlowyTransport

class WorkFlowyAccount:
    """Class to represent and interact with a Workflowy account."""

    def __init__(self, session_id):
        self.transport = WorkFlowyTransport(session_id)
        init_data = self.transport.get_initialization_data()
        self.email = init_data['user']
        self.name = init_data['fullName']
        self.registration_date = init_data['dateJoined']
        self.monthly_item_quota = init_data['monthlyItemQuota']
        self.items_created_this_month = init_data['itemsCreated']
        self.invite_link = init_data['inviteLink']


    def get_email(self):
        return self.email
    

    def get_name(self):
        return self.name
    

    def get_registration_date(self):
        return self.registration_date
    

    def get_monthly_item_quota(self):
        return self.monthly_item_quota
    

    def get_items_created_this_month(self):
        return self.items_created_this_month
    

    def get_invite_link(self):
        return self.invite_link
