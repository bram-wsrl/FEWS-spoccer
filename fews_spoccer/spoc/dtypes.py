class IndexCode:
    startswith = ('HL', 'SL', 'OW')

    def __call__(self, value):
        if len(value) == 8:
            if value[:2] in self.startswith:
                if value[2:].isnumeric():
                    return True
        return False


class HLIndex(IndexCode):
    startswith = ('HL',)


class SLIndex(IndexCode):
    startswith = ('SL',)


class OWIndex(IndexCode):
    startswith = ('OW',)


class Tag:
    pass
