import logging

from .maplayerfiles import HL
from ..utils import log


logger = logging.getLogger(__name__)


class Spoccer:
    '''
    SpocFile tree manager

    Use the lower case class name as
    instance attribute to include a tree relation.
    '''
    def __init__(self, srcpath, dstpath, read_kw, write_kw):
        self.srcpath = srcpath
        self.dstpath = dstpath
        self.read_kw = read_kw
        self.write_kw = write_kw

        self.hl = HL(self)

        self.module = None

    def __repr__(self):
        return f'<{self.__class__.__name__}()>'

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

    @log(logger, logging.INFO)
    def load(self):
        '''Load SpocFiles in tree'''
        for relation in self:
            relation.read(self.srcpath, **self.read_kw)
            relation.set_index()
            relation.convert_dtypes()

    @log(logger, logging.INFO)
    def save(self):
        '''Save SpocFiles in tree'''
        for relation in self:
            relation.write(self.dstpath, **self.write_kw)

    @log(logger, logging.INFO)
    def validate(self):
        '''Validate SpocFiles'''
        for relation in self:
            relation.validate()

    def pre(self, id, sync_column):
        indexer = self.hl.sublocations(id)
        indexer.check_sync_level(self.module.sync_level, sync_column)
        indexer = self.module.pre(indexer)
        return indexer

    def post(self, indexer, sync_column):
        indexer.set_sync_level(self.module.sync_level, sync_column)
        self.save()

    def load_module(self, module, **module_config):
        self.module = module(**module_config)

    def validate_module(self, id, sync_column):
        indexer = self.pre(id, sync_column)
        self.module.validate(indexer)

    def run_module(self, id, sync_column):
        indexer = self.pre(id, sync_column)
        self.module.run(indexer)
        self.post(indexer, sync_column)
        return indexer
