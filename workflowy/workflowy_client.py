from workflowy_account import WorkFlowyAccount
from workflowy_transport import WorkFlowyTransport
from workflowy_exception import WorkFlowyException
from workflowy_project import WorkFlowyProject
import re

class WorkFlowyClient:

    
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


    '''
    Calls the login endpoint and returns a session ID on successful login
    @param username: The username of the user
    @param password: The password of the user
    @return: The session ID of the user
    '''
    def login(username: str, password: str):
        # Login logic using WorkFlowyTransport
        # Gets a session ID on successful login, False otherwise
        transport = WorkFlowyTransport()
        response = transport.login_request(username, password)
        if response:
            return response
        else:
            raise WorkFlowyException("Login failed")
        
    
    def get_main_list(self):
        # Retrieve and return project
        return self.project.build_list()


    def get_account_info(self):
        return self.account.get_account()


    def export_opml(self, list_id):
        pass
