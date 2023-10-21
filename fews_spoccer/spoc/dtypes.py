import re
from typing import Self

import numpy as np

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


class IndexField(BaseField):
    regexp = re.compile(r'((HL)|(SL)|(OW))[0-9]{6}')


class HLField(IndexField):
    regexp = re.compile(r'HL[0-9]{6}')


class SLField(IndexField):
    regexp = re.compile(r'SL[0-9]{6}')


class OWField(IndexField):
    regexp = re.compile(r'OW[0-9]{6}')


class Tag:
    patterns = (
        re.compile(iwa_tag),
        re.compile(pbh_tag),
        re.compile(avic_tag),
        re.compile(vaarweg_tag)
    )

    def __init__(self, tag: str, mapping=None):
        self.tag = tag
        self.mapping = mapping

    def __repr__(self):
        return f"{self.__class__.__name__}({self.tag})"

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
