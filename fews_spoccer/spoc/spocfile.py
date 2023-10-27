import logging
from typing import Self
from pathlib import Path

import pandas as pd

from ..utils import log
from .indexer import Index
from .ctypes import Column, Param


logger = logging.getLogger(__name__)


class SpocFile:
    '''
    Abstraction of a single maplayerfile

    Use this class by subclassing it with
    the exact same name as the file to be read.
    '''
    def __init__(self):
        self._df = None

        # assign owner instance to descriptor
        for name in self.__class__.__dict__:
            _ = getattr(self, name)

    def __str__(self):
        return self.__class__.__name__.lower()

    def __repr__(self):
        return f'<{self.__class__.__name__}>'

    @property
    def df(self):
        return self._df

    @property
    def filename(self):
        return str(self).upper() + '.csv'

    @classmethod
    def cls_attrs(cls, *classes):
        '''
        Assess class attributes conveniently
        '''
        if classes:
            attrs = {}
            for k, v in cls.__dict__.items():
                if isinstance(v, classes):
                    attrs.update({k: v})
            return attrs
        return cls.__dict__

    @classmethod
    @property
    def Columns(cls):
        return cls.cls_attrs(Column).values()

    @classmethod
    @property
    def Params(cls):
        return cls.cls_attrs(Param).values()

    @log(logger)
    def read(self, srcpath, **read_kw):
        self._df = pd.read_csv(Path(srcpath) / self.filename, **read_kw)

    @log(logger)
    def write(self, dstpath, **write_kw):
        self.df.to_csv(Path(dstpath) / self.filename, **write_kw)

    @log(logger)
    def set_index(self):
        self._df = self.df.set_index(self.df[self.id])

    @log(logger)
    def convert_dtypes(self):
        for column in self.Columns:
            if self.df[column].dtype != column.dtype:
                self.df[column] = self.df[column].astype(column.dtype)

                logger.debug(f'{self}@{column} to {column.dtype}')

    @log(logger)
    def validate(self):
        logger.debug(f'Validating {self} ...')
        for column in self.Columns:
            column.validate(self.df[column])

    def field(self, id, column):
        return column.field(id)

    def ids_by_pids(self, *pids: str) -> pd.Index:
        return self.df[self.df[self.pid].isin(pids)].index

    def ids_by_area(self, *areas: str) -> pd.Index:
        return self.df[self.df[self.area].isin(areas)].index

    def get_param_matches(self, spocfile: Self, index: Index) -> list[dict]:
        matches = []
        for p in spocfile.Params:
            match = {}
            match['id'] = index.id
            match['param'] = p.param

            file_value = p.owner_instance.get_param_value(index, p)
            match[str(p.owner_instance)] = file_value

            if p.relation is not None:
                p = p.relation
                tag_value = p.owner_instance.get_param_value(index, p)
                match[str(p.owner_instance)] = tag_value
            matches.append(match)
        return matches
