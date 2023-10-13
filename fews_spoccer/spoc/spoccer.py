import logging

from .maplayerfiles import HL


logger = logging.getLogger(__name__)


class Spoccer:
    '''SpocFile tree manager'''

    def __init__(self, srcpath, dstpath, read_kw, write_kw):
        self.srcpath = srcpath
        self.dstpath = dstpath
        self.read_kw = read_kw
        self.write_kw = write_kw

        self.hl = HL()

    def __iter__(self):
        '''Iterate over SpocFiles'''
        for indexfile in self.hl:
            for relation in indexfile:
                yield relation

    def __getattr__(self, k):
        '''Convenience method to assess SpocFile directly'''
        for obj in self:
            if k == str(obj).lower():
                return obj

        raise AttributeError

    def load(self):
        '''Load SpocFiles in tree'''
        for relation in self:
            relation.read(self.srcpath, **self.read_kw)
            relation.set_index()

        logger.info(self.srcpath)

    def save(self):
        '''Save SpocFiles in tree'''
        for relation in self:
            relation.write(self.dstpath, **self.write_kw)

        logger.info(self.dstpath)

    def validate_raising(self):
        '''Validate SpocFiles'''
        for relation in self:
            relation.validate_raising()

        logger.info('OK')
