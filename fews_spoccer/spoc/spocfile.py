import logging
from pathlib import Path

import pandas as pd

from .mixins import SelectorMixin, ValidatorMixin


logger = logging.getLogger(__name__)


class SpocFile(SelectorMixin, ValidatorMixin):
    _validation_rules = []

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

    @property
    def params(self):
        params = {}
        for k, v in self.__class__.__dict__.items():
            if k.startswith('param_'):
                param = k.split('_')[-1]
                params.update({param: v})
        return params

    def read(self, srcpath, **read_kw):
        self._df = pd.read_csv(Path(srcpath) / self.filename, **read_kw)
        logger.debug(self.filename)

    def write(self, dstpath, **write_kw):
        self.df.to_csv(Path(dstpath) / self.filename, **write_kw)
        logger.debug(self.filename)

    def validate(self):
        for rule in self._validation_rules:
            getattr(self, rule)()
            logger.debug(rule)
