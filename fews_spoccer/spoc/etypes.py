class SpoccerException(Exception):
    pass


class SpoccerColumnException(SpoccerException):
    pass


class EmptyFieldException(SpoccerColumnException):
    pass


class NonUniqueException(SpoccerColumnException):
    pass


class InvalidPatternException(SpoccerColumnException):
    pass


class InvalidTagPatternException(InvalidPatternException):
    pass
