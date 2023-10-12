import logging
from pathlib import Path

import pandas as pd

from .dtypes import Column, Param
from .mixins import SelectorMixin, ValidatorMixin


logger = logging.getLogger(__name__)


class SpocFile(SelectorMixin, ValidatorMixin):
    _validation_rules = ['columns_exist']

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
        if classes:
            attrs = {}
            for k, v in cls.__dict__.items():
                if isinstance(v, classes):
                    attrs.update({k: v})
            return attrs
        return cls.__dict__

    @classmethod
    @property
    def columns(cls):
        return cls.cls_attrs(Column)

    @classmethod
    @property
    def params(cls):
        return cls.cls_attrs(Param)

    def read(self, srcpath, **read_kw):
        self._df = pd.read_csv(Path(srcpath) / self.filename, **read_kw)
        logger.debug(self.filename)

    def write(self, dstpath, **write_kw):
        self.df.to_csv(Path(dstpath) / self.filename, **write_kw)
        logger.debug(self.filename)

    def validate(self):
        rules = set(self._validation_rules + SpocFile._validation_rules)
        for rule in sorted(rules):
            getattr(self, rule)()
            logger.debug(f'{rule} - {self}')
