import re
from typing import Self

import numpy as np
import pandas as pd

from .etypes import InvalidPatternException, InvalidTagPatternException
from .regexp import iwa_tag, pbh_tag, avic_tag, vaarweg_tag


class BaseField:
    regexp = r''

    def __init__(self, value):
        self.value = value
        self.validate()

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'

    def validate(self):
        if self.regexp:
            self.parse()

    def parse(self):
        if not re.match(self.regexp, self.value):
            raise InvalidPatternException


class ColumnField(BaseField):
    def concat(self, *fields, sep='_'):
        values = [i.value for i in (self, *fields)]
        if not any(pd.isna(v) for v in values):
            return sep.join(values)
        return np.nan


class IndexField(ColumnField):
    regexp = re.compile(r'((HL)|(SL)|(OW))[0-9]{6}')


class HLField(IndexField):
    regexp = re.compile(r'HL[0-9]{6}')


class SLField(IndexField):
    regexp = re.compile(r'SL[0-9]{6}')


class OWField(IndexField):
    regexp = re.compile(r'OW[0-9]{6}')


class FileParamField(ColumnField):
    def __iadd__(self, other):
        if not any(pd.isna(i.value) for i in (self, other)):
            return self.__class__(f'{self.value}_{other.value}')
        return np.nan


class Tag:
    patterns = (
        re.compile(iwa_tag),
        re.compile(pbh_tag),
        re.compile(avic_tag),
        re.compile(vaarweg_tag)
    )

    def __init__(self, tag: str, map=None):
        self.tag = tag
        self.map = map

    def __repr__(self):
        return f"{self.__class__.__name__}({self.tag})"

    @property
    def location(self):
        return self.map.get('legger_code', self.map['name'])

    @property
    def is_muted(self):
        return self.map['marker1'] != '' or self.map['marker2'] != ''

    def filename(self):
        exclude = ('marker1', 'prefix', 'tag_type', 'suffix', 'marker2')
        stem = ''.join(v for k, v in self.map.items() if k not in exclude)
        return ''.join(i for i in stem if i.isalnum() or i == '_') + '.csv'

    @staticmethod
    def is_taglike(tag: str) -> bool:
        if isinstance(tag, str):
            return len(tag) > 25 and tag.count('.') > 4
        return False

    @classmethod
    def parse(cls, tag: str) -> Self:
        if not cls.is_taglike(tag):
            return np.nan

        for pattern in cls.patterns:
            match = re.match(pattern, tag)
            if match:
                return cls(tag, match.groupdict())
        else:
            raise InvalidTagPatternException(tag)
