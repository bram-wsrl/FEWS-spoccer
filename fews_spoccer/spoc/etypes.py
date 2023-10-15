class BaseColumnException(Exception):
    pass


class NonUniqueException(BaseColumnException):
    pass


class InvalidPatternException(BaseColumnException):
    pass


class EmptyFieldException(BaseColumnException):
    pass
