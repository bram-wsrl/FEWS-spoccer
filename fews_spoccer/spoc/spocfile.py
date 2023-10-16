from typing import Self

import logging
from pathlib import Path

import pandas as pd
import numpy as np

from .ctypes import Column, Param
from .mixins import SelectorMixin


logger = logging.getLogger(__name__)


class SpocFile(SelectorMixin):
    '''
    Abstraction of a single maplayerfile

    Use this class by subclassing it with
    the exact same name as the file to be read.
    '''
    def __init__(self):
        self._df = None

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return f'<{self.__class__.__name__}>'

    @property
    def df(self):
        return self._df

    @property
    def filename(self):
        return str(self) + '.csv'

    @classmethod
    def cls_attrs(cls, *classes):
        '''assess class attributes conveniently'''
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

    def read(self, srcpath, **read_kw):
        self._df = pd.read_csv(Path(srcpath) / self.filename, **read_kw)
        logger.debug(self.filename)

    def write(self, dstpath, **write_kw):
        self.df.to_csv(Path(dstpath) / self.filename, **write_kw)
        logger.debug(self.filename)

    def set_index(self):
        self._df = self.df.set_index(self.df[self.id])
        logger.debug(self.filename)

    def convert_dtypes(self):
        for column in self.Columns:
            if self.df[column].dtype != column.dtype:
                self.df[column] = self.df[column].astype(column.dtype)

                logger.debug(f'{self}@{column} to {column.dtype}')

    def validate(self):
        logger.debug(f'Validating {self} ...')
        for column in self.Columns:
            column.validate(self.df[column])

        logger.debug(f'{self} OK')

    def construct_param(self, id, *columns) -> str | float:
        return self.join_fields(id, *columns) or np.nan

    def param_matches(self, *spocfiles: Self) -> dict[str, dict[str, Param]]:
        '''
        Connect columns that share the same parameter
        '''
        matches = {}
        for spocfile in spocfiles:
            for P in spocfile.Params:
                matches.setdefault(P.param, {}).update({str(spocfile): P})
        return matches

    def param_value_matches(self,
                            param_matches: dict[str, dict[str, Param]],
                            id: str,
                            exclude_empty: bool
                            ) -> dict[str, dict[str, str]]:
        '''
        Connect values that share the same parameter
        '''
        matches = {}
        for param_id in param_matches:
            for spocfile in param_matches[param_id]:
                P = param_matches[param_id][spocfile]
                value = getattr(
                    self, spocfile.lower()).construct_param(id, P)
                matches.setdefault(
                    param_id, {}).update({spocfile: value})

            if exclude_empty:
                if all(pd.isna(v) for v in matches[param_id].values()):
                    _ = matches.pop(param_id)
        return matches
