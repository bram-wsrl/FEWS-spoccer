import logging
import re

import pandas as pd

from ..utils import catch, log
from .dtypes import Tag
from .etypes import (
    NonUniqueException, EmptyFieldException, InvalidPatternException)


logger = logging.getLogger(__name__)


class BaseColumn:
    '''
    Abstraction of a column in a SpocFile Object
    '''
    dtype = object
    unique = False
    empty = True
    pattern = False

    def __init__(self, name, **kwargs):
        self.name = name
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __call__(self, *args, **kwargs):
        return self.name

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name})'

    @catch(logger)
    def _check_empty(self, v):
        if pd.isna(v):
            raise EmptyFieldException(self, v)

    @catch(logger)
    def _check_pattern_regex(self, v):
        if not re.match(self.pattern, v):
            raise InvalidPatternException(self, v)

    @catch(logger)
    def _check_pattern_func(self, v):
        return self.pattern(v)

    @log(logger)
    @catch(logger)
    def check_unique(self, series):
        if not series.is_unique:
            raise NonUniqueException(self)

    @log(logger)
    @catch(logger)
    def check_empty(self, series):
        for _, v in enumerate(series):
            self._check_empty(v)

    @log(logger)
    def check_pattern(self, series):
        if isinstance(self.pattern, re.Pattern):
            for _, v in enumerate(series):
                self._check_pattern_regex(v)

        elif callable(self.pattern):
            for _, v in enumerate(series):
                self._check_pattern_func(v)

    def validate(self, series):
        if self.unique:
            self.check_unique(series.dropna())
        if not self.empty:
            self.check_empty(series)
        if isinstance(self.pattern, re.Pattern) or callable(self.pattern):
            self.check_pattern(series.dropna())


class Column(BaseColumn):
    pass


class IDColumn(Column):
    unique = True
    empty = False
    pattern = re.compile(r'((HL)|(SL)|(OW))[0-9]{6}')


class HLColumn(Column):
    unique = True
    empty = False
    pattern = re.compile(r'HL[0-9]{6}')


class SLColumn(Column):
    unique = True
    empty = False
    pattern = re.compile(r'SL[0-9]{6}')


class WSColumn(Column):
    unique = True
    empty = False
    pattern = re.compile(r'OW[0-9]{6}')


class Param(Column):
    def __init__(self, name, param, **kwargs):
        super().__init__(name, **kwargs)
        self.param = param

    def __repr__(self):
        return f'{self.__class__.__name__}({self.param})'


class TagParam(Param):
    pattern = Tag.parse

    def check_pattern(self, series):
        super().check_pattern(series)


class FileParam(Param):
    pass


class CRSColumn(Column):
    dtype = int
    empty = False


class XColumn(CRSColumn):
    pass


class YColumn(CRSColumn):
    pass
