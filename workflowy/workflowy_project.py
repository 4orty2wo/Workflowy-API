from workflowy_transport import WorkFlowyTransport
from workflowy_list import WorkFlowyList

class WorkFlowyProject:
    '''
    Represents a WorkFlowy project.

    Attributes:
        dateJoinedTimestampInSeconds (int): The timestamp when the user joined the project.
        transport (WorkFlowyTransport): The transport object used for communication with the WorkFlowy API.

    Methods:
        __init__(session_id): Initializes a WorkFlowyProject object with the given session ID.
        build_list(): Retrieves the main list of the project.
        __parse_tree(raw_list, parent_id, level): Parses the given list and builds a WorkFlowyList object.
        get_list_parent(id): Retrieves the parent list of the list with the given ID.
    '''

    dateJoinedTimestampInSeconds = 0

    def __init__(self, session_id):
        '''
        Constructor for WorkFlowyProject.

        Args:
            session_id (str): The session ID of the user.
        '''
        self.transport = WorkFlowyTransport(session_id=session_id)

    def build_list(self):
        '''
        Retrieves the main list of the project.

        Returns:
            WorkFlowyList: The main list of the project.
        '''
        init_data = WorkFlowyTransport.get_initialization_data(self.transport)
        raw_list = []
        self.parent_ids = {}
        self.all_lists = {}

        if init_data['projectTreeData']['mainProjectTreeInfo']['rootProjectChildren']:
            raw_list = init_data['projectTreeData']['mainProjectTreeInfo']['rootProjectChildren']

        if init_data['projectTreeData']['mainProjectTreeInfo']['dateJoinedTimestampInSeconds']:
            self.dateJoinedTimestampInSeconds = init_data['projectTreeData']['mainProjectTreeInfo']['dateJoinedTimestampInSeconds']

        if init_data['projectTreeData']['clientId']:
            self.transport.client_id = init_data['projectTreeData']['clientId']

        if init_data['projectTreeData']['mainProjectTreeInfo']['initialMostRecentOperationTransactionId']:
            self.transport.most_recent_operation_transaction_id = init_data['projectTreeData']['mainProjectTreeInfo']['initialMostRecentOperationTransactionId']

        return self.__parse_tree(raw_list={
                                    'id': None,
                                    'nm': None,
                                    'no': None,
                                    'ct': None,
                                    'lm': 0,
                                    'ch': raw_list
                                 }, parent_id=False, level=0)

    def __parse_tree(self, raw_list, parent_id: str, level: int):
        '''
        Parses the given list and builds a WorkFlowyList object.

        Args:
            raw_list (dict): The raw list data to be parsed.
            parent_id (str): The ID of the parent list.
            level (int): The level of the current list in the hierarchy.

        Returns:
            WorkFlowyList: The parsed WorkFlowyList object.
        '''
        id = raw_list['id'] if 'id' in raw_list else ''
        name = raw_list['nm'] if 'nm' in raw_list else ''
        description = raw_list['no'] if 'no' in raw_list else ''
        raw_sublists = raw_list['ch'] if 'ch' in raw_list else []
        creation_time = self.dateJoinedTimestampInSeconds + raw_list['ct'] if raw_list['ct'] is not None else 0
        last_modified_time = self.dateJoinedTimestampInSeconds + raw_list['lm'] if raw_list['lm'] is not None else 0
        if 'cp' in raw_list.keys() and raw_list['cp'] is not None:
            completed_time = self.dateJoinedTimestampInSeconds + raw_list['cp']
        else:
            completed_time = 0
        processed_sublists = []

        for raw_sublist in raw_sublists:
            processed_sublists.append(self.__parse_tree(raw_sublist, id, level + 1))

        sublist = WorkFlowyList(
            id=id,
            name=name,
            description=description,
            level=level,
            creation_time=creation_time,
            last_modified_time=last_modified_time,
            completed_time=completed_time,
            sublists=processed_sublists,
            main_list=self,
            transport=self.transport
        )

        if parent_id:
            self.parent_ids[id] = parent_id

        self.all_lists[id] = sublist
        return sublist

    def get_list_parent(self, id):
        '''
        Retrieves the parent list of the list with the given ID.

        Args:
            id (str): The ID of the list.

        Returns:
            WorkFlowyList or False: The parent list of the given ID, or False if the parent list does not exist.
        '''
        parent_id = self.parent_ids[id] if isinstance(id, str) and id in self.parent_ids else None
        return self.all_lists[parent_id] if self.all_lists[parent_id] else False

        