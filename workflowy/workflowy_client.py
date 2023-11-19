from workflowy_account import WorkFlowyAccount
from workflowy_transport import WorkFlowyTransport
from workflowy_exception import WorkFlowyException
from workflowy_project import WorkFlowyProject
import re

class WorkFlowyClient:
    """
    A client for interacting with the WorkFlowy API.

    Attributes:
        session_id (str): The session ID for the authenticated user.
        project (WorkFlowyProject): The project associated with the authenticated user.
        account (WorkFlowyAccount): The account associated with the authenticated user.
    """

    def __init__(self, session_id=None):
        self.session_id = None
        self.project = None
        self.account = None

        if session_id is not None:
            if not re.match('^[a-z0-9]{32}$', session_id):
                raise WorkFlowyException('Invalid session Id')
            self.session_id = session_id
            self.project = WorkFlowyProject(self.session_id)
            self.account = WorkFlowyAccount(self.session_id)


    def login(username: str, password: str):
        """
        Logs in to WorkFlowy using the provided username and password.

        Args:
            username (str): The username for the WorkFlowy account.
            password (str): The password for the WorkFlowy account.

        Returns:
            str: The session ID on successful login.

        Raises:
            WorkFlowyException: If the login fails.
        """
        # Login logic using WorkFlowyTransport
        # Gets a session ID on successful login, False otherwise
        transport = WorkFlowyTransport()
        response = transport.login_request(username, password)
        if response:
            return response
        else:
            raise WorkFlowyException("Login failed")


    def get_main_list(self):
        """
        Retrieves and returns the main list associated with the authenticated user.

        Returns:
            list: The main list.
        """
        return self.project.build_list()


    def get_account_info(self):
        """
        Retrieves and returns the account information associated with the authenticated user.

        Returns:
            dict: The account information.
        """
        return self.account.get_account()


    # TODO: Implement exporting OPML of a list
    '''
    Returns an OPML string of the given list. If no list is given, returns an OPML string of the main list.
    '''
    def export_opml(self, list_id):
        """
        Returns an OPML string of the given list. If no list is given, returns an OPML string of the main list.

        Args:
            list_id (str): The ID of the list to export.

        Returns:
            str: The OPML string.
        """
        pass
