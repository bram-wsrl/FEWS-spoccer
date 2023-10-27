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


class H2GOFileNotFoundException(SpoccerException):
    pass


class H2GOMultipleFilesFoundException(SpoccerException):
    pass


class H2GOFileContentException(SpoccerException):
    pass


class MutedTagException(SpoccerException):
    pass


class TagNotInViewException(SpoccerException):
    pass
