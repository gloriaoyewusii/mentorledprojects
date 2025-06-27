
class ExistingUserError(Exception):
    def __init__(self, message="User exists already"):
        super().__init__(message)