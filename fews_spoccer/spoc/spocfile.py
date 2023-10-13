import logging
from pathlib import Path

import pandas as pd

from .ctypes import Column, ID, Param
from .mixins import SelectorMixin, RaisingValidatorMixin, ProcessValidatorMixin


logger = logging.getLogger(__name__)


class SpocFile(SelectorMixin, RaisingValidatorMixin, ProcessValidatorMixin):
    '''Abstraction of a single maplayerfile'''

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
    def Ids(cls):
        return cls.cls_attrs(ID).values()

    @classmethod
    @property
    def Params(cls):
        return cls.cls_attrs(Param).values()

    def read(self, srcpath, **read_kw):
        self._df = pd.read_csv(Path(srcpath) / self.filename, **read_kw)
        logger.debug(self.filename)

    def set_index(self):
        self._df = self.df.set_index(self.df[self.id])
        logger.debug(self.filename)

    def write(self, dstpath, **write_kw):
        self.df.to_csv(Path(dstpath) / self.filename, **write_kw)
        logger.debug(self.filename)

    def validate_raising(self):
        self.run_raising_validation()
        logger.debug(f'{self} OK')
