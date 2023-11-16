from workflowy_transport import WorkFlowyTransport
from workflowy_exception import WorkFlowyException
import re

class WorkFlowySublist:
    

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
                if isinstance(sublist, WorkFlowySublist):
                    self.sublists.append(sublist)
                else:
                    raise WorkFlowyException('Sublists must be a WorkFlowySublist object')

        # Check list
        if main_list.__class__.__name__ == 'WorkFlowyList':
            self.list = main_list
        else:
            raise WorkFlowyException('List must be a WorkFlowyList object')
        
        # Check transport
        if isinstance(transport, WorkFlowyTransport):
            self.transport = transport
        else:
            raise WorkFlowyException('Transport must be a WorkFlowyTransport object')
        

    '''
    Recursively searches for a sublist by name
    @param name: The name of the sublist to search for
    @param get_all: Whether to return all sublists with matching names or just the first found instance
    @param exact_match: Whether to search for an exact match or a partial match
    @return: A list of matching sublists
    '''
    def search_sublist(self, expression: str, get_all: bool = False, exact_match: bool = False):
        # Search for a sublist by name using regular expression
        # Returns a list of matching sublists
        # If get_all is true, returns all sublists with matching names
        # Otherwise, returns the first sublist with a matching name

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
        return self.list.get_sublist_parent(self.id)


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
    Get the sublist with the given ID
    '''
    def get_sublist(self, id: str):
        if id in self.list.sublists:
            return self.list.sublists[id]
        else:
            raise WorkFlowyException(f"Sublist {id} not found")
    




    