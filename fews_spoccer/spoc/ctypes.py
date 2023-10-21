import logging

import pandas as pd

from ..utils import catch, log
from .dtypes import BaseField, IndexField, HLField, SLField, OWField, Tag
from .etypes import (NonUniqueException, EmptyFieldException)


logger = logging.getLogger(__name__)


class BaseColumn:
    '''
    Abstraction of a column in a SpocFile Object
    '''
    dtype = object
    instance = BaseField
    empty = True
    unique = False

    def __init__(self, name, **kwargs):
        self.name = name
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __call__(self, *args, **kwargs):
        return self.name

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name})'

    @catch(logger)
    def _check_instance(self, v):
        return self.instance(v)

    @catch(logger)
    def _check_empty(self, v):
        if pd.isna(v):
            raise EmptyFieldException(self, v)

    @log(logger)
    def check_instance(self, series):
        for _, v in enumerate(series):
            self._check_instance(v)

    @log(logger)
    def check_empty(self, series):
        for _, v in enumerate(series):
            self._check_empty(v)

    @log(logger)
    def check_unique(self, series):
        if not series.is_unique:
            raise NonUniqueException(self)

    def validate(self, series):
        self.check_instance(series.dropna())
        if self.unique:
            self.check_unique(series.dropna())
        if not self.empty:
            self.check_empty(series)


class Column(BaseColumn):
    pass


class IDColumn(Column):
    instance = IndexField
    empty = False
    unique = True


class HLColumn(Column):
    instance = HLField
    empty = False
    unique = True


class SLColumn(Column):
    instance = SLField
    empty = False
    unique = True


class WSColumn(Column):
    instance = OWField
    empty = False
    unique = True


class Param(Column):
    def __init__(self, name, param, **kwargs):
        super().__init__(name, **kwargs)
        self.param = param

    def __repr__(self):
        return f'{self.__class__.__name__}({self.param})'


class TagParam(Param):
    instance = Tag.parse


class FileParam(Param):
    pass


class CRSColumn(Column):
    dtype = int
    empty = False


class XColumn(CRSColumn):
    pass


class YColumn(CRSColumn):
    pass
