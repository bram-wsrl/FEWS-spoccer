import itertools as it

import numpy as np
import pandas as pd


class IndexField(dict):
    def __init__(self, map):
        self.update(map)

    def exists(self, spocfile):
        return not pd.isna(self.get(spocfile))

    def is_empty(self, spocfiles):
        return not any(self.exists(s) for s in spocfiles)

    def exists_all(self, spocfiles):
        return all(self.exists(s) for s in spocfiles)


class Index:
    def __init__(self, id, indexfile):
        self.id = id
        self.indexfile = indexfile

        self._spocfiles = []
        self._data = []

    def __iter__(self):
        return iter(self.data)

    def __call__(self, *args, **kwargs):
        return self.id

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id})'

    @property
    def spocfiles(self):
        return self._spocfiles

    @spocfiles.setter
    def spocfiles(self, spocfiles):
        self._spocfiles = sorted(list(spocfiles))

    @property
    def data(self):
        return self._data

    def set_data(self, map: list[dict]):
        self._data = [IndexField(m) for m in map]

    def extend_data(self, map: list[dict]):
        self._data.extend(IndexField(m) for m in map)


class Indexer:
    levels = {
        np.nan: -1,
        'LIVE': 0,
        'VALIDATIE': 1,
        'INTERPOLATIE': 2,
        'DEBIET': 3
    }

    def __init__(self, spoccer, hl: list[Index], sl: list[Index],
                 ws: list[Index]):
        self.hl = hl
        self.sl = sl
        self.ws = ws

        self.spoccer = spoccer

    def __iter__(self):
        return it.chain(self.hl, self.sl, self.ws)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.hl[0].id})'

    def sublocations(self):
        for index in it.chain(self.sl, self.ws):
            yield index

    def fields(self):
        for index in self.sublocations():
            for field in index:
                yield index, field

    def get_sync_level(self, column: str):
        levels = []
        for index in self:
            spoc_obj = getattr(self.spoccer, index.indexfile)
            field = getattr(spoc_obj, column).field(index)
            levels.append(field)
            for spocfile in index.spocfiles:
                spoc_obj = getattr(self.spoccer, spocfile)
                field = getattr(spoc_obj, column).field(index)
                levels.append(field)

        if not all(level == levels[0] for level in levels):
            raise ValueError('Inconsistent sync levels')
        return levels[0].value

    def check_sync_level(self, level, sync_column):
        current_sync_level = self.get_sync_level(sync_column)
        if self.levels[level] - self.levels[current_sync_level] != 1:
            raise ValueError('Cannot skip sync levels')

    def set_sync_level(self, level: str, sync_column: str):
        self.check_sync_level(level, sync_column)

        for index in self:
            spoc_obj = getattr(self.spoccer, index.indexfile)
            getattr(spoc_obj, sync_column).set_field(index, level)
            for spocfile in index.spocfiles:
                spoc_obj = getattr(self.spoccer, spocfile)
                getattr(spoc_obj, sync_column).set_field(index, level)
