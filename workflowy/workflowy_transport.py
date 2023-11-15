import requests
from workflowy_exception import WorkFlowyException
import re

class WorkFlowyTransport:

    LOGIN_URL = "https://workflowy.com/ajax_login"  # Login Endpoint URL
    API_URL = "https://workflowy.com/%s"
    TIMEOUT = 5

    def __init__(self, session_id=False):
        self.session = requests.Session()

        if (session_id is not False and 
            (not isinstance(session_id, str) or not re.match('^[a-z0-9]{32}$', session_id))):

            raise WorkFlowyException('Invalid session ID')
        self.session_id = session_id


    def listRequest(self, endpoint, data={}):
        # if not isinstance(endpoint, str) or isinstance(data, dict):
        #     raise WorkFlowyException('Invalid API request')
        
        # data = {
        #     'client_id': 
        # }

        # self.api_request('push_and_poll', )
        pass

    def api_request(self, endpoint, data={}):
        if self.session_id is False:
            raise WorkFlowyException('A session ID is needed to make API calls.')

        
        if not isinstance(endpoint, str) or not isinstance(data, dict):
            raise WorkFlowyException('Invalid API request')

        url = self.API_URL % endpoint
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json',
            'Cookie': 'sessionid=%s' % self.session_id
        }

        try:
            response = self.session.post(url, data=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise WorkFlowyException(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            raise WorkFlowyException(f"Error during request: {e}")


    # Returns session ID on successful login, False otherwise
    def login_request(self, username, password):

        if not username or not password:
            raise WorkFlowyException("Username or password not provided.\n")

        data = {
            'username': username,
            'password': password
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json'
        }

        try:
            response = self.session.post(self.LOGIN_URL, data=data, headers=headers)
            response.raise_for_status()

            if 'set-cookie' in response.headers:
                # Split the string to get the sessionid
                set_cookie_header = response.headers['set-cookie']

                # Split the Set-Cookie header into individual cookies
                cookies = set_cookie_header.split(', ')

                # Loop through the cookies to find the sessionid cookie
                for cookie in cookies:
                    if 'sessionid' in cookie:
                        # Extract the sessionid value from the cookie
                        sessionid = cookie.split(';')[0].split('=')[1]
                        print("Session ID:", sessionid)
                        return sessionid
            return False

        except requests.exceptions.HTTPError as e:
            raise WorkFlowyException(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            raise WorkFlowyException(f"Error during request: {e}")

# Example usage:
# transport = WorkflowyTransport('your_username', 'your_password')
# transport.login()
