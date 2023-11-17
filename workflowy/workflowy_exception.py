class WorkFlowyException(Exception):
    """Custom exception class for Workflowy API errors."""

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"WorkFlowyException: {self.message}"
