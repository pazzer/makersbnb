
class MakersBnbException(Exception):
    """Base class for project exceptions"""

class EmailAlreadyExistsError(MakersBnbException):
    def __init__(self, message, *args):
        super().__init__(*args)
        self.message = message
        super(EmailAlreadyExistsError, self).__init__(message, *args)


class MalformedEmailError(MakersBnbException):
    def __init__(self, message, *args):
        super().__init__(*args)
        self.message = message
        super(MalformedEmailError, self).__init__(message, *args)


class MalformedPasswordError(MakersBnbException):
    def __init__(self, message, *args):
        self.message = message
        super(MalformedPasswordError, self).__init__(message, *args)

class UnrecognisedIdError(MakersBnbException):
    def __init__(self, message, *args):
        self.message = message
        super(UnrecognisedIdError, self).__init__(message, *args)
