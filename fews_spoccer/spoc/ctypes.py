from .dtypes import IndexCode


class BaseColumn:
    '''Abstraction of a column in a SpocFile Object'''

    def __init__(self, name):
        self.name = name

    def __call__(self, *args, **kwargs):
        return self.name

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name})'


class Column(BaseColumn):
    def __init__(self, name, exists=True, unique=False, dtypes=None,
                 format=None):
        super().__init__(name)
        self.exists = exists
        self.unique = unique
        self.dtypes = dtypes
        self.format = format

        if format is not None:
            if isinstance(self.format, type):
                self.format = self.format()

    def check_exists(self, columns):
        if self.exists:
            return self.name in columns
        return True

    def check_unique(self, series):
        if self.unique:
            return series.is_unique
        return True

    def check_dtypes(self, series):
        if self.dtypes is not None:
            for v in series:
                return isinstance(v, tuple(self.dtypes))
        return True

    def check_format(self, series):
        if self.format is not None:
            for v in series:
                return self.format(v)
        return True


class ID(Column):
    def __init__(self, name, exists=True, unique=True, dtypes=None,
                 format=IndexCode):
        super().__init__(name, exists, unique, dtypes, format)


class Param(Column):
    def __init__(self, name, param, exists=True, unique=False, dtypes=None,
                 format=None):
        super().__init__(name, exists, unique, dtypes, format)
        self.param = param

    def __repr__(self):
        return f'{self.__class__.__name__}({self.param})'

    def is_valid(self):
        return True
