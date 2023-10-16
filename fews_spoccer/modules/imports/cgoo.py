import re

from .regexp import iwa_tag, pbh_tag


class CGOO:
    pass


class Tag:
    patterns = (
        re.compile(iwa_tag),
        re.compile(pbh_tag)
    )

    def __init__(self, tag):
        self.raw = tag
        self.parse()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.raw})"

    def parse(self):
        for pattern in self.patterns:
            match = re.match(pattern, self.raw)
            if match:
                self.tag = match.groupdict()
                break
        else:
            # raise TypeError('WEWEWE')
            print('WEWEWE', self.raw[:35])
