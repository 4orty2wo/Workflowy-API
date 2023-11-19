from workflowy_transport import WorkFlowyTransport
from workflowy_exception import WorkFlowyException
import re
import random

class WorkFlowyList:


    def __init__(self, id, name, description, level, creation_time, last_modified_time, completed_time, sublists, main_list, transport):
        self.id = id if isinstance(id, str) else ''
        self.name = name if isinstance(name, str) else ''
        self.description = description if isinstance(description, str) else ''
        self.level = level if isinstance(level, int) else -1
        # Time based values
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
        if main_list.__class__.__name__ == 'WorkFlowyTree':
            self.main_list = main_list
        else:
            raise WorkFlowyException('List must be a WorkFlowyTree object')
        
        # Check transport
        if isinstance(transport, WorkFlowyTransport):
            self.transport = transport
        else:
            raise WorkFlowyException('Transport must be a WorkFlowyTransport object')
        

    '''
    Recursively searches for a list by name
    @param name: The name of the list to search for
    @param get_all: Whether to return all lists with matching names or just the first found instance
    @param exact_match: Whether to search for an exact match or a partial match
    @return: A list of matching lists
    '''
    def search_sublist(self, expression: str, get_all: bool = False, exact_match: bool = False) -> list:
        # Search for a list by name using regular expression
        # Returns a list of matching list
        # If get_all is true, returns all list with matching names
        # Otherwise, returns the first list with a matching name

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
        return self.id
    

    def get_name(self):
        return self.name
    

    def get_description(self):
        return self.description
    

    def get_creation_time(self):
        return self.creation_time
    

    def get_last_modified_time(self):
        return self.last_modified_time
    

    def get_completed_time(self):
        return self.completed_time
    

    def get_parent(self):
        return self.main_list.get_list_parent(self.id)


    def is_completed(self):
        return self.completed_time != 0
    

    def get_level(self):
        return self.level
    

    # Implement this 
    def get_opml(self):
        pass


    def get_sublists(self):
        return self.sublists
    

    '''
    Get the list with the given ID
    '''
    def get_list(self, id: str):
        if id in self.main_list.all_lists:
            return self.main_list.all_lists[id]
        else:
            raise WorkFlowyException(f"List {id} not found")
        

    # Setters

    def set_name(self, name: str):
        self.name = name
        self.transport.listRequest('edit', {
            'projectid': self.id,
            'name': name
        })
        
    
    def set_description(self, description: str):
        self.description = description
        self.transport.listRequest('edit', {
            'projectid': self.id,
            'description': description
        })
        

    def set_complete(self, complete: bool):
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


        # self.list.parent_ids[self.id] = destination.get_id()


    def delete(self):
        if self.level == 0:
            raise WorkFlowyException('Deleting the root is not currently supported')

        self.transport.listRequest('delete', {
            'projectid': self.id
        })
        self.get_parent().sublists.remove(self)
        self.main_list.all_lists.pop(self.id)
        self.main_list.parent_ids.pop(self.id)


    '''
    Creates a new sublist within the current list
    @param name: The name of the new sublist
    @param description: The description of the new sublist
    @param priority: The priority of the new sublist
    '''
    def create_sublist(self, name: str = None, description: str = None, priority: int = 0):
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
    

    def __generate_id(self):
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


    '''
    Update levels for self and all its sublists recursively
    '''
    def __update_levels(self, level: int):
        self.level = level
        for sublist in self.sublists:
            sublist.__update_levels(level + 1)

    