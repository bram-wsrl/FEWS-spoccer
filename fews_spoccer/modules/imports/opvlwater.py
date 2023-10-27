import itertools as it


class OpvlWaterModule:
    def __init__(self):
        pass

    def validate_tags(self, indexer):
        for i, f in indexer.fields():
            if f.exists(i.spocfiles[0]):
                print(i, f, f[i.spocfiles[0]])

    def validate_h2go(self, indexer):
        for index, field in indexer.fields():
            if field.exists(index.spocfiles[1]):
                print(index, field, field[index.spocfiles[1]])

    def run(self, indexer):

        # unmatches h2go objects
        for i, f in indexer.fields():
            if f.exists(i.spocfiles[1]) and not f.exists(i.spocfiles[0]):
                print(i, f[i.spocfiles[1]])

        # matches and unmatches tags
        has_tag = [(i, f) for i, f in indexer.fields()
                   if f.exists(i.spocfiles[0])]

        def groupkey(x):
            '''group tags by location for efficient db query'''
            return x[1][x[0].spocfiles[0]].location

        has_tag.sort(key=groupkey)
        for location, group in it.groupby(has_tag, key=groupkey):
            group = list(group)

            # unmatched tags
            if any(f.exists(i.spocfiles[0]) and not f.exists(i.spocfiles[1])
                   for i, f in group):

                print('only', location, group)

            # matches tags
            else:
                print('matched', location, group)
