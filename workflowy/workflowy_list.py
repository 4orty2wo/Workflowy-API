from workflowy_transport import WorkFlowyTransport
from workflowy_exception import WorkFlowyException
import re
import random

class WorkFlowyList:
    """
    Represents a list in WorkFlowy.

    Attributes:
    - id: The unique identifier of the list (string).
    - name: The name of the list (string).
    - description: The description of the list (string).
    - level: The level of the list in the hierarchy (integer).
    - creation_time: The timestamp of when the list was created (integer).
    - last_modified_time: The timestamp of when the list was last modified (integer).
    - completed_time: The timestamp of when the list was completed (integer).
    - sublists: The sublists contained within the list (list of WorkFlowyList objects).
    - main_list: The main list to which the list belongs (WorkFlowyProject object).
    - transport: The transport object used for making API requests (WorkFlowyTransport object).
    """

    def __init__(self, id, name, description, level, creation_time, last_modified_time, completed_time, sublists, main_list, transport):
        """
        Initializes a WorkFlowyList object.

        Parameters:
        - id: The unique identifier of the list (string).
        - name: The name of the list (string).
        - description: The description of the list (string).
        - level: The level of the list in the hierarchy (integer).
        - creation_time: The timestamp of when the list was created (integer).
        - last_modified_time: The timestamp of when the list was last modified (integer).
        - completed_time: The timestamp of when the list was completed (integer).
        - sublists: The sublists contained within the list (list of WorkFlowyList objects).
        - main_list: The main list to which the list belongs (WorkFlowyProject object).
        - transport: The transport object used for making API requests (WorkFlowyTransport object).
        """
        self.id = id if isinstance(id, str) else ''
        self.name = name if isinstance(name, str) else ''
        self.description = description if isinstance(description, str) else ''
        self.level = level if isinstance(level, int) else -1
        self.creation_time = creation_time if isinstance(creation_time, int) else 0
        self.last_modified_time = last_modified_time if isinstance(last_modified_time, int) else 0
        self.completed_time = completed_time if isinstance(completed_time, int) else 0
        self.sublists = []

        # Check sublists
        if isinstance(sublists, list):
            for sublist in sublists:
                if isinstance(sublist, WorkFlowyList):
                    self.sublists.append(sublist)
                else:
                    raise WorkFlowyException('Sublists must be a WorkFlowyList object')

        # Check list
        if main_list.__class__.__name__ == 'WorkFlowyProject':
            self.main_list = main_list
        else:
            raise WorkFlowyException('List must be a WorkFlowyProject object')
        
        # Check transport
        if isinstance(transport, WorkFlowyTransport):
            self.transport = transport
        else:
            raise WorkFlowyException('Transport must be a WorkFlowyTransport object')
        

    def search_sublist(self, expression: str, get_all: bool = False, exact_match: bool = False) -> list:
        """
        Search for a sublist by name using regular expression.

        Args:
            expression (str): The search expression to match against sublist names.
            get_all (bool, optional): If True, returns all sublists with matching names. 
                                      If False, returns the first sublist with a matching name. 
                                      Defaults to False.
            exact_match (bool, optional): If True, performs an exact match against sublist names. 
                                          If False, performs a case-insensitive search using regular expression. 
                                          Defaults to False.

        Returns:
            list: A list of matching sublists. If no matches are found, returns an empty list.
        """
        
        # Check name
        if not isinstance(expression, str):
            raise WorkFlowyException('Search expression must be a string')
        
        matches = []
        if (exact_match and expression == self.name) or (not exact_match and re.search(expression, self.name, re.IGNORECASE)):
            matches.append(self)
            if not get_all:
                return matches
            
        for sublist in self.sublists:
            match = sublist.search_sublist(expression, get_all, exact_match)
            if match:
                matches.extend(match)
                if not get_all and len(matches) > 0:
                    return matches
            
        return matches if matches else False


    def get_id(self):
        """
        Get the unique identifier of the list.

        Returns:
            str: The unique identifier of the list.
        """
        return self.id
    

    def get_name(self):
        """
        Get the name of the list.

        Returns:
            str: The name of the list.
        """
        return self.name
    

    def get_description(self):
        """
        Get the description of the list.

        Returns:
            str: The description of the list.
        """
        return self.description
    

    def get_creation_time(self):
        """
        Get the timestamp of when the list was created.

        Returns:
            int: The timestamp of when the list was created.
        """
        return self.creation_time
    

    def get_last_modified_time(self):
        """
        Get the timestamp of when the list was last modified.

        Returns:
            int: The timestamp of when the list was last modified.
        """
        return self.last_modified_time
    

    def get_completed_time(self):
        """
        Get the timestamp of when the list was completed.

        Returns:
            int: The timestamp of when the list was completed.
        """
        return self.completed_time
    

    def get_parent(self):
        """
        Get the parent list of the current list.

        Returns:
            WorkFlowyList: The parent list of the current list.
        """
        return self.main_list.get_list_parent(self.id)


    def is_completed(self):
        """
        Check if the list is completed.

        Returns:
            bool: True if the list is completed, False otherwise.
        """
        return self.completed_time != 0
    

    def get_level(self):
        """
        Get the level of the list in the hierarchy.

        Returns:
            int: The level of the list in the hierarchy.
        """
        return self.level
    
    # TODO: Implement getting OPML of the list 
    def get_opml(self):
        """
        Get the OPML representation of the list.

        Returns:
            str: The OPML representation of the list.
        """
        pass


    def get_sublists(self):
        """
        Get the sublists contained within the list.

        Returns:
            list: A list of WorkFlowyList objects representing the sublists.
        """
        return self.sublists
    

    def get_list(self, id: str):
        """
        Get the list with the given ID.

        Args:
            id (str): The ID of the list to retrieve.

        Returns:
            WorkFlowyList: The list with the given ID.

        Raises:
            WorkFlowyException: If the list with the given ID is not found.
        """
        if id in self.main_list.all_lists:
            return self.main_list.all_lists[id]
        else:
            raise WorkFlowyException(f"List {id} not found")
        

    # Setters

    def set_name(self, name: str):
        """
        Set the name of the list.

        Args:
            name (str): The new name of the list.
        """
        self.name = name
        self.transport.listRequest('edit', {
            'projectid': self.id,
            'name': name
        })
        
    
    def set_description(self, description: str):
        """
        Set the description of the list.

        Args:
            description (str): The new description of the list.
        """
        self.description = description
        self.transport.listRequest('edit', {
            'projectid': self.id,
            'description': description
        })
        

    def set_complete(self, complete: bool):
        """
        Set the completion status of the list.

        Args:
            complete (bool): True to mark the list as completed, False to mark it as incomplete.
        """
        if complete:
            self.transport.listRequest('complete', {
                'projectid': self.id
            })
        else:
            self.transport.listRequest('uncomplete', {
                'projectid': self.id
            })
            self.completed_time = 0


    def move(self, destination, priority: int = 0):
        """
        Move the list to a new destination.

        Args:
            destination (WorkFlowyList): The new destination list.
            priority (int, optional): The priority of the list in the new destination. Defaults to 0.

        Raises:
            WorkFlowyException: If the destination is not a WorkFlowyList object, is the same as self, or is the root.
        """
        if not isinstance(destination, self.__class__):
            raise WorkFlowyException('Destination must be a WorkFlowyList object')
        
        # Check that the destination is not self
        if destination.id == self.id:
            raise WorkFlowyException('Destination cannot be self')
        
        # Check that the destination is not root
        if destination.level == 0:
            raise WorkFlowyException('Moving to root is not currently supported')
        
        source_parent = self.get_parent()
        # Check that the destination is not a child of self. Break if the destination is the root.
        parent = destination.get_parent()
        while self.level < parent.level:
            if parent.id == self.id:
                raise WorkFlowyException('Destination cannot be a child of self')
            parent = parent.get_parent()
            # Break if the parent is the root
            if not parent:
                break
        
        self.transport.listRequest('move', {
            'projectid': self.id,
            'parentid': destination.id,
            'priority': priority
        })

        # Update the levels
        self.__update_levels(destination.level + 1)
        
        
        # Update the main list
        self.main_list.all_lists[self.id] = self
        # Update the parent_ids
        self.main_list.parent_ids[self.id] = destination.get_id()

        # Update the sublists
        source_parent.sublists.remove(self)
        destination.sublists.insert(priority, self)


    def delete(self):
        """
        Delete the list.

        Raises:
            WorkFlowyException: If the list is the root.
        """
        if self.level == 0:
            raise WorkFlowyException('Deleting the root is not currently supported')

        self.transport.listRequest('delete', {
            'projectid': self.id
        })
        self.get_parent().sublists.remove(self)
        self.main_list.all_lists.pop(self.id)
        self.main_list.parent_ids.pop(self.id)


    def create_sublist(self, name: str = None, description: str = None, priority: int = 0):
        """
        Create a new sublist within the current list.

        Args:
            name (str, optional): The name of the new sublist. Defaults to None.
            description (str, optional): The description of the new sublist. Defaults to None.
            priority (int, optional): The priority of the new sublist. Defaults to 0.
        """
        new_id = self.__generate_id()

        self.transport.listRequest('create', {
            'projectid': new_id,
            'parentid': self.id,
            'priority': priority,
        })

        properties = {}

        if name:
            properties['name'] = name
        if description:
            properties['description'] = description
        
        if properties: # Only send the request if there are properties to set
            self.transport.listRequest('edit', {
                'projectid': new_id,
                **properties # Merge the properties into the request
            })
    
        # Update the main list
        new_list = WorkFlowyList(
            id=new_id,
            name=name,
            description=description,
            level=self.level + 1,
            creation_time=0,
            last_modified_time=0,
            completed_time=0,
            sublists=[],
            main_list=self.main_list,
            transport=self.transport
        )
        self.main_list.all_lists[new_id] = new_list
        self.main_list.parent_ids[new_id] = self.id
        self.sublists.insert(priority, new_list)


    def __generate_id(self):
        """
        Generate a unique identifier for the list.

        Returns:
            str: The generated unique identifier.
        """
        id_parts = []
        for _ in range(2):
            id_part = format(int((1 + random.random()) * 65536) | 0, 'x')[1:]
            id_parts.append(id_part)
        id_parts.append('-')

        for _ in range(3):
            id_part = format(int((1 + random.random()) * 65536) | 0, 'x')[1:]
            id_parts.append(id_part)
            id_parts.append('-')

        for _ in range(3):
            id_part = format(int((1 + random.random()) * 65536) | 0, 'x')[1:]
            id_parts.append(id_part)

        return ''.join(id_parts)


    def __update_levels(self, level: int):
        """
        Update levels for self and all its sublists recursively.

        Args:
            level (int): The new level to set for the list and its sublists.
        """
        self.level = level
        for sublist in self.sublists:
            sublist.__update_levels(level + 1)