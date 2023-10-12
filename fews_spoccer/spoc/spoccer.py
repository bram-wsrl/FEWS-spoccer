import logging

from .maplayerfiles import HL


logger = logging.getLogger(__name__)


class Spoccer:
    def __init__(self, srcpath, dstpath, read_kw, write_kw):
        self.srcpath = srcpath
        self.dstpath = dstpath
        self.read_kw = read_kw
        self.write_kw = write_kw

        self.hl = HL()

    def __iter__(self):
        for indexfile in self.hl:
            for relation in indexfile:
                yield relation

    def __getattr__(self, k):
        for obj in self:
            if k == str(obj).lower():
                return obj

        raise AttributeError

    def load(self):
        for relation in self:
            relation.read(self.srcpath, **self.read_kw)

        logger.info(self.srcpath)

    def save(self):
        for relation in self:
            relation.write(self.dstpath, **self.write_kw)

        logger.info(self.dstpath)

    def validate(self):
        for relation in self:
            relation.validate()

        logger.info('OK')