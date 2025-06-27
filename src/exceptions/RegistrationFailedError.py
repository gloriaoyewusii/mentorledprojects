class RegistrationFailedError(Exception):
    def __init__(self, message="Registration failed"):
        super().__init__(message)
