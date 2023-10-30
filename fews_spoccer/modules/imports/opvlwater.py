import itertools as it

from .h2go import H2GO
from .cgoo import CGOO


class OpvlWaterModule:
    sync_level = 'LIVE'

    def __init__(self, h2go_config, cgoo_config):
        self.h2go_config = h2go_config
        self.cgoo_config = cgoo_config

        self.cgoo = CGOO(**cgoo_config)
        self.cgoo.connect()

    def pre(self, indexer):
        return indexer.spoccer.hl.get_param_matches(indexer)

    def validate_h2go(self, indexer):
        for i, f in indexer.fields():
            if f.exists(i.spocfiles[1]):
                h2go_field = i.spocfiles[1]
                f[h2go_field] = H2GO.load(f[h2go_field], self.h2go_config)

    def validate_tags(self, indexer):
        for i, f in indexer.fields():
            if f.exists(i.spocfiles[0]):
                tag = f[i.spocfiles[0]]
                self.cgoo.validate(tag)

    def validate(self, indexer):
        self.validate_h2go(indexer)
        self.validate_tags(indexer)

    def run(self, indexer):
        self.validate(indexer)

        # unmatches h2go objects
        for i, f in indexer.fields():
            if f.exists(i.spocfiles[1]) and not f.exists(i.spocfiles[0]):
                h2go_obj = f[i.spocfiles[1]]
                h2go_obj.save()

        # matches and unmatches tags
        has_tag = [(i, f) for i, f in indexer.fields()
                   if f.exists(i.spocfiles[0])]

        def groupkey(x):
            '''group tags by location for efficient db query'''
            return x[1][x[0].spocfiles[0]].location

        has_tag.sort(key=groupkey)
        for location, group in it.groupby(has_tag, key=groupkey):
            g = list(group)

            # unmatched tags
            if any(f.exists(i.spocfiles[0]) and not f.exists(i.spocfiles[1])
                   for i, f in g):

                self.cgoo.get_timeseries(location)
                for i, f in g:
                    self.cgoo.save(f[i.spocfiles[0]])

            # matched tags
            else:
                enddatetime = min(f[i.spocfiles[1]].enddatetime for i, f in g)
                self.cgoo.get_timeseries(location, startdatetime=enddatetime)

                for i, f in g:
                    f[i.spocfiles[1]].save()
                    self.cgoo.save(f[i.spocfiles[0]])
