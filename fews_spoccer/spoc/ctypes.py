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
    unique = False
    empty = True
    pattern = r''

    def __init__(self, name, **kwargs):
        self.name = name
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __call__(self, *args, **kwargs):
        return self.name

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name})'

    def check_unique(self, series):
        if not series.is_unique:
            raise NonUniqueException(self)

        logger.debug(self)

    def check_empty(self, series):
        if len(series.dropna()) != len(series):
            raise EmptyFieldException(self)

        logger.debug(self)

    def check_pattern(self, series):
        if not all(series.str.fullmatch(self.pattern)):
            raise InvalidPatternException(self)

        logger.debug(self)

    def validate(self, series):
        if self.unique:
            self.check_unique(series)
        if not self.empty:
            self.check_empty(series)
        if self.pattern:
            self.check_pattern(series)


class Column(BaseColumn):
    pass


class IDColumn(Column):
    unique = True
    empty = False
    pattern = r'((HL)|(SL)|(OW))[0-9]{6}'


class HLColumn(Column):
    unique = True
    empty = False
    pattern = r'HL[0-9]{6}'


class SLColumn(Column):
    unique = True
    empty = False
    pattern = r'SL[0-9]{6}'


class WSColumn(Column):
    unique = True
    empty = False
    pattern = r'OW[0-9]{6}'


class Param(Column):
    def __init__(self, name, param, **kwargs):
        super().__init__(name, **kwargs)
        self.param = param

    def __repr__(self):
        return f'{self.__class__.__name__}({self.param})'


class TagParam(Param):
    pattern = r'^(.*)(~SCX\..*.Historic)(.*)'

    @staticmethod
    def is_taglike(series):
        return series[series.str.len() > 20]

    def check_pattern(self, series):
        super().check_pattern(self.is_taglike(series))


class FileParam(Param):
    pass


class CRSColumn(Column):
    dtype = int
    empty = False


class XColumn(CRSColumn):
    pass


class YColumn(CRSColumn):
    pass
