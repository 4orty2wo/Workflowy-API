from workflowy_transport import WorkFlowyTransport

class WorkFlowyAccount:
    """Class to represent and interact with a Workflowy account.

    Attributes:
        email (str): The email associated with the account.
        name (str): The full name of the account owner.
        registration_date (str): The date when the account was created.
        monthly_item_quota (int): The maximum number of items allowed to be created in a month.
        items_created_this_month (int): The number of items created in the current month.
        invite_link (str): The invite link for the account.
    """

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
        """Get the email associated with the account.

        Returns:
            str: The email associated with the account.
        """
        return self.email
    

    def get_name(self):
        """Get the full name of the account owner.

        Returns:
            str: The full name of the account owner.
        """
        return self.name
    

    def get_registration_date(self):
        """Get the date when the account was created.

        Returns:
            str: The date when the account was created.
        """
        return self.registration_date
    

    def get_monthly_item_quota(self):
        """Get the maximum number of items allowed to be created in a month.

        Returns:
            int: The maximum number of items allowed to be created in a month.
        """
        return self.monthly_item_quota
    

    def get_items_created_this_month(self):
        """Get the number of items created in the current month.

        Returns:
            int: The number of items created in the current month.
        """
        return self.items_created_this_month
    

    def get_invite_link(self):
        """Get the invite link for the account.

        Returns:
            str: The invite link for the account.
        """
        return self.invite_link
