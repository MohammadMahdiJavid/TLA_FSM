class AutomatonException(Exception):
    pass


class RejectionError(AutomatonException):
    pass


class InvalidStateError(AutomatonException):
    pass


class MissingStateError (AutomatonException):
    pass
