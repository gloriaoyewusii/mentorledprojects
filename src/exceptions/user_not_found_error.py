class UserNotFoundError(Exception):
    def __init__(self, message="User does not exist"):
        super().__init__(message)