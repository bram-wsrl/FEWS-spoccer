import logging

from .etypes import (
    NonUniqueException, InvalidPatternException, EmptyFieldException)


logger = logging.getLogger(__name__)


class BaseColumn:
    '''
    Abstraction of a column in a SpocFile Object

    Methods marked with @abstractmethod have to be
    defined at least once in the method resolution order.
    '''
    dtype = object

    def __init__(self, name, **kwargs):
        self.name = name
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __call__(self, *args, **kwargs):
        return self.name

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name})'


class Column(BaseColumn):
    unique = False
    empty = True
    pattern = False

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

    def check_unique(self, series):
        if not series.is_unique:
            raise NonUniqueException(self)

        logger.debug(self)

    def check_empty(self, series):
        if any(series.eq('')):
            raise EmptyFieldException(self)

        logger.debug(self)

    def check_pattern(self, series):
        return

    def validate(self, series):
        if self.unique:
            self.check_unique(series)
        if not self.empty:
            self.check_empty(series)
        if self.pattern:
            self.check_pattern(series)


class IDColumn(Column):
    unique = True
    empty = False
    pattern = True

    startswith = ('HL', 'SL', 'OW')
    length = 8

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

    def valid_pattern(self, value):
        if len(value) == self.length:
            if value[:2] in self.startswith:
                if value[2:].isnumeric():
                    return True
        return False

    def check_pattern(self, series):
        if not all(series.apply(self.valid_pattern)):
            raise InvalidPatternException(self)

        logger.debug(self)


class HLColumn(IDColumn):
    startswith = ('HL',)

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


class SLColumn(Column):
    startswith = ('SL',)

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


class WSColumn(Column):
    startswith = ('OW',)

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


class Param(Column):
    def __init__(self, name, param, **kwargs):
        super().__init__(name, **kwargs)
        self.param = param

    def __repr__(self):
        return f'{self.__class__.__name__}({self.param})'


class CRSColumn(Column):
    dtype = int
    empty = False

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


class XColumn(CRSColumn):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


class YColumn(CRSColumn):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
