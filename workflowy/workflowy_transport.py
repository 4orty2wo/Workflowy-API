import requests
from workflowy_exception import WorkFlowyException
import re, json, uuid

class WorkFlowyTransport:
    """
    A class representing the transport layer for interacting with the WorkFlowy API.

    Attributes:
        LOGIN_URL (str): The URL for the login endpoint.
        API_URL (str): The base URL for the API.
        TIMEOUT (int): The timeout value for API requests.

    Methods:
        __init__(self, session_id=False): Initializes a new instance of the WorkFlowyTransport class.
        listRequest(self, action: str, data: dict = {}): Handles push_and_poll requests.
        get_initialization_data(self): Retrieves the initialization data from the API.
        __api_request(self, endpoint, data={}): Sends an API request to the specified endpoint.
        login_request(self, username, password): Sends a login request to the API.
        __generate_uuid(self): Generates an 8-character UUID.
    """

    LOGIN_URL = "https://workflowy.com/ajax_login"  # Login Endpoint URL
    API_URL = "https://workflowy.com/%s"
    TIMEOUT = 5

    def __init__(self, session_id=False):
        """
        Initializes a new instance of the WorkFlowyTransport class.

        Args:
            session_id (str, optional): The session ID for making API calls. Defaults to False.

        Raises:
            WorkFlowyException: If an invalid session ID is provided.
        """
        self.session = requests.Session()

        if (
            session_id is not False
            and (
                not isinstance(session_id, str)
                or not re.match("^[a-z0-9]{32}$", session_id)
            )
        ):
            raise WorkFlowyException("Invalid session ID")
        self.session_id = session_id
        self.client_version = 21
        self.client_id = None
        self.most_recent_operation_transaction_id = None

    def listRequest(self, action: str, data: dict = {}):
        """
        Handles push_and_poll requests.

        Args:
            action (str): The action type for the request.
            data (dict, optional): The data for the request. Defaults to {}.

        Raises:
            WorkFlowyException: If an invalid API request is provided.
        """
        if not isinstance(action, str) or not isinstance(data, dict):
            raise WorkFlowyException("Invalid API request")

        request_data = {
            "client_id": self.client_id,
            "client_version": self.client_version,
            "push_poll_id": self.__generate_uuid(),
            "push_poll_data": json.dumps(
                [
                    {
                        "most_recent_operation_transaction_id": self.most_recent_operation_transaction_id,
                        "operations": [{"type": action, "data": data}],
                    }
                ]
            ),
        }

        self.__api_request("push_and_poll", request_data)

    def get_initialization_data(self):
        """
        Retrieves the initialization data from the API.

        Returns:
            dict: The initialization data.

        Raises:
            WorkFlowyException: If an invalid API request is provided or a session ID is not available.
        """
        return self.__api_request("get_initialization_data", {})

    def __api_request(self, endpoint, data={}):
        """
        Sends an API request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint.
            data (dict, optional): The data for the request. Defaults to {}.

        Returns:
            dict: The response from the API.

        Raises:
            WorkFlowyException: If an invalid API request is provided or a session ID is not available.
            WorkFlowyException: If an HTTP error occurs during the request.
            WorkFlowyException: If an error occurs during the request.
        """
        if self.session_id is False:
            raise WorkFlowyException("A session ID is needed to make API calls.")

        if not isinstance(endpoint, str) or not isinstance(data, dict):
            raise WorkFlowyException("Invalid API request")

        url = self.API_URL % endpoint
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json",
            "Cookie": "sessionid=%s" % self.session_id,
        }

        try:
            response = self.session.post(url, data=data, headers=headers)
            response.raise_for_status()
            response = response.json()
            return response

        except requests.exceptions.HTTPError as e:
            raise WorkFlowyException(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            raise WorkFlowyException(f"Error during request: {e}")

    def login_request(self, username, password):
        """
        Sends a login request to the API.

        Args:
            username (str): The username for the login.
            password (str): The password for the login.

        Returns:
            str: The session ID on successful login, False otherwise.

        Raises:
            WorkFlowyException: If the username or password is not provided.
            WorkFlowyException: If an HTTP error occurs during the request.
            WorkFlowyException: If an error occurs during the request.
        """
        if not username or not password:
            raise WorkFlowyException("Username or password not provided.\n")

        data = {"username": username, "password": password}
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json",
        }

        try:
            response = self.session.post(self.LOGIN_URL, data=data, headers=headers)
            response.raise_for_status()

            if "set-cookie" in response.headers:
                # Split the string to get the sessionid
                set_cookie_header = response.headers["set-cookie"]

                # Split the Set-Cookie header into individual cookies
                cookies = set_cookie_header.split(", ")

                # Loop through the cookies to find the sessionid cookie
                for cookie in cookies:
                    if "sessionid" in cookie:
                        # Extract the sessionid value from the cookie
                        sessionid = cookie.split(";")[0].split("=")[1]
                        return sessionid
            return False

        except requests.exceptions.HTTPError as e:
            raise WorkFlowyException(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            raise WorkFlowyException(f"Error during request: {e}")

    def __generate_uuid(self):
        """
        Generates an 8-character UUID.

        Returns:
            str: The generated UUID.
        """
        return str(uuid.uuid4())[:8]