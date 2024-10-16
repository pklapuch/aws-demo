class ProcessingError(Exception):
    """Processing failed due to an error

    Attributes:
        errorCode -- server error code
        description -- debug explanation of error
    """

    def __init__(self, errorCode, reason):
        self.errorCode = errorCode
        self.reason = reason
        super().__init__(self.errorCode, self.reason)