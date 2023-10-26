import itertools as it

import pandas as pd


class Index:
    def __init__(self, id, name, spocfiles=None):
        self.id = id
        self.name = name
        self.spocfiles = spocfiles or []

        # [{'id': '', 'spocfile1': '', 'spocfile2': '', ...}]
        self.data = []

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id})'

    def __call__(self, *args, **kwargs):
        return self.id

    def __iter__(self):
        return iter(self.data)

    @property
    def indexfile(self):
        return self.name

    @property
    def spocfiles(self):
        return self._spocfiles

    @spocfiles.setter
    def spocfiles(self, spocfiles):
        self._spocfiles = sorted(list(spocfiles))

    def is_empty(self, field):
        return not any(self.has_field(field, s) for s in self.spocfiles)

    def has_field(self, field, spocfile):
        return not pd.isna(field.get(spocfile))

    def has_field_all(self, field):
        return all(self.has_field(field, s) for s in self.spocfiles)

    def has_field_only(self, field, spocfile):
        return self.has_field(field, spocfile) and\
            not self.has_field_all(field)


class Indexer:
    def __init__(self, hl: Index, sl: list[Index], ws: list[Index]):
        self.hl = hl
        self.sl = sl
        self.ws = ws

    def __repr__(self):
        return f'{self.__class__.__name__}({self.hl.id})'

    def __iter__(self):
        return it.chain(self.sl, self.ws)

    def fields(self):
        for index in self:
            for field in index:
                yield index, field
