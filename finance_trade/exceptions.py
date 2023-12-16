
class CustomException(Exception):
    pass


class NotAuthorized(CustomException ):
    def __init__(self, message="Not authorized"):
        self.message = message
        self.code = 401
        super().__init__(self.message)


class UserAlreadyExists(CustomException ):
    def __init__(self, message="User already exists"):
        self.message = message
        self.code = 409
        super().__init__(self.message)