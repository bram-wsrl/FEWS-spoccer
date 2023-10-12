class Column:
    def __init__(self, name):
        self.name = name

    def __call__(self, *args, **kwargs):
        return self.name

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name})'


class ID(Column):
    def __init__(self, name):
        super().__init__(name)


class Param(Column):
    def __init__(self, name, param):
        super().__init__(name)
        self.param = param

    def __repr__(self):
        return f'{self.__class__.__name__}({self.param})'
