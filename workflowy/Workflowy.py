from workflowy_account import WorkFlowyAccount
from workflowy_transport import WorkFlowyTransport
from workflowy_exception import WorkFlowyException

class WorkFlowy:


    def login(username, password):
        # Login logic using WorkFlowyTransport
        # Gets a session ID on successful login, False otherwise
        transport = WorkFlowyTransport()
        response = transport.login_request(username, password)
        if response:
            return response
        else:
            raise WorkFlowyException("Login failed")


    def get_account_info(self):
        return self.account.get_info()

    # def get_lists(self):
    #     # Retrieve and return lists
    #     return WorkFlowyList(self.transport).get_main_list()

    # def export_opml(self, list_id):
    #     return WorkFlowyOPML(self.transport).export_list(list_id)
