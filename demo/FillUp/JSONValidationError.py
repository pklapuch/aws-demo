class JSONValidationError(Exception):
    """Invalid JSON

    Attributes:
        description -- debug explanation of error
    """

    def __init__(self, reason):
        self.reason = reason
        super().__init__(self.reason)