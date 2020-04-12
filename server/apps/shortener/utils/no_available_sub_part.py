class NoAvailableSubPartException(Exception):
    def __init__(self, message):
        super(NoAvailableSubPartException, self).__init__(message)
