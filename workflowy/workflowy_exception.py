class WorkFlowyException(Exception):
    """Custom exception class for Workflowy API errors.

    Args:
        message (str): The error message.

    Attributes:
        message (str): The error message.

    """

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"WorkFlowyException: {self.message}"
