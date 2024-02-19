# Workflowy-API
A Python API for Workflowy, a nested note taking application. I've created this in abscence of an official API from Workflowy. This is primarily a python wrapper for the REST operations that are performed on the backend of the web application. 

Inspiration was drawn from another unofficial API created in PHP by another user here: [workflowy-php](https://github.com/johansatge/workflowy-php).

## Installation
A PyPi package will be released once I test with recent changes as of February 2024.

## Usage
### Client
You will need to provide your login credentials since there is no official API to handle key distribution. Password login must be enabled on your Workflowy account.
```python
session_id = WorkFlowyClient.login('username@email.com', 'password')
client = WorkFlowyClient(session_id)
```
The `client` variable will be used to perform requests to read/write from your lists or account information.

The `session_id` is not perpetually valid, but in the time that it is active, it can be used multiple times for as many requests as you want to use it for. Best to utilize this as a rolling API key in replacement after passing the unencoded password once. Take care to not have your password hardcoded in your python file.

### Lists
Get the root list with the `get_main_list()` client method. 
```list = client.get_main_list()```
This will return a list object that allows for execution of list operations.

#### Get the information of a list

| Function | Returns | Description |
| --- | --- | --- |
| `get_id()` | `str` | Returns the unique identifier of the list. |
| `get_name()` | `str` | Returns the name of the list. |
| `get_description()` | `str` | Returns the description of the list. |
| `get_creation_time()` | `int` | Returns the timestamp of when the list was created. |
| `get_last_modified_time()` | `int` | Returns the timestamp of when the list was last modified. |
| `get_completed_time()` | `int` | Returns the timestamp of when the list was completed. |
| `get_parent()` | `WorkFlowyList` | Returns the parent list of the current list. |
| `is_completed()` | `bool` | Returns `True` if the list is completed, `False` otherwise. |
| `get_level()` | `int` | Returns the level of the list in the hierarchy. |
| `get_opml()` | `str` | Returns the OPML representation of the list. |
| `get_sublists()` | `list` | Returns a list of `WorkFlowyList` objects representing the sublists. |
| `get_list(id)` | `WorkFlowyList` | Returns the list with the given ID. Raises `WorkFlowyException` if not found. |

#### Editing lists

| Function | Returns | Description |
| --- | --- | --- |
| `set_name(name)` | None | Sets the name of the list. |
| `set_description(description)` | None | Sets the description of the list. |
| `set_complete(complete)` | None | Sets the completion status of the list. |
| `move(destination, priority=0)` | None | Moves the list to a new destination. Raises `WorkFlowyException` under certain conditions. |
| `delete()` | None | Deletes the list. Raises `WorkFlowyException` if the list is the root. |
| `create_sublist(name=None, description=None, priority=0)` | None | Creates a new sublist within the current list. |

### Account
Get the account with the `get_account_info()` client method.
`account = client.get_account_info()`
This will return an account object for use in getting account info.

| Function | Returns | Description |
| --- | --- | --- |
| `get_email()` | `str` | Returns the email associated with the account. |
| `get_name()` | `str` | Returns the full name of the account owner. |
| `get_registration_date()` | `str` | Returns the date when the account was created. |
| `get_monthly_item_quota()` | `int` | Returns the maximum number of items allowed to be created in a month. |
| `get_items_created_this_month()` | `int` | Returns the number of items created in the current month. |
| `get_invite_link()` | `str` | Returns the invite link for the account. |

## Credits
- [Workflowy](https://workflowy.com/)
- [Johan Satgé](https://github.com/johansatge)
