import itertools as it

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
    def __init__(self, hl: Index, sl: list[Index], ws: list[Index]):
        self.hl = hl
        self.sl = sl
        self.ws = ws

    def __iter__(self):
        return it.chain(self.sl, self.ws)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.hl.id})'

    def fields(self):
        for index in self:
            for field in index:
                yield index, field
