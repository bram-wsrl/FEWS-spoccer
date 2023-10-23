import itertools as it
import logging

import numpy as np
import pandas as pd

from .h2go import H2GO
from .cgoo import CGOO


logger = logging.getLogger(__name__)


class ParamMatch:
    groups = {
        0: 'empty',
        1: 'h2go_only',
        2: 'tag_only',
        3: 'h2go_tag',
        4: 'forbidden state'
    }

    def __init__(self, param_match):
        self.map = param_match
        self.group = 4
        self.assign_group()

    def __repr__(self):
        return f'{self.__class__.__name__}({self.groups[self.group]})'

    def __gt__(self, other):
        return self.group > other.group

    @property
    def group_name(self):
        return ParamMatch.groups[self.group]

    @property
    def get_h2go(self):
        return self.map.get('sl_ti_h2go_tags',
                            self.map.get('ws_ti_h2go_tags', np.nan))

    @property
    def get_tag(self):
        return self.map.get('sl_tags', self.map.get('ws_tags', np.nan))

    @property
    def h2go_exists(self):
        return not pd.isna(self.get_h2go)

    @property
    def tag_exists(self):
        return not pd.isna(self.get_tag)

    @property
    def is_empty(self):
        return not self.h2go_exists and not self.tag_exists

    @property
    def h2go_only(self):
        return self.h2go_exists and not self.tag_exists

    @property
    def tag_only(self):
        return not self.h2go_exists and self.tag_exists

    @property
    def h2go_tag(self):
        return self.h2go_exists and self.tag_exists

    def assign_group(self):
        if self.is_empty:
            self.group = 0
        elif self.h2go_only:
            self.group = 1
        elif self.tag_only:
            self.group = 2
        else:
            self.group = 3


class OpvlWaterModule:
    def __init__(self, h2go_config, cgoo_config):
        self.h2go_config = h2go_config
        self.cgoo_config = cgoo_config

        self.cgoo = CGOO(**cgoo_config)
        self.cgoo.connect()

    def load_h2go(self, pattern):
        h2go = H2GO(**self.h2go_config)
        h2go.load(pattern)
        return h2go

    def tag_in_view(self, tag):
        return tag.tag in self.cgoo.get_unique_tags(tag.location)

    def validate_h2go(self, param_matches: list[ParamMatch]):
        for param_match in param_matches:
            pattern = param_match.get_h2go
            if not pd.isna(pattern):
                param_match.map['h2go'] = self.load_h2go(pattern)

    def validate_tag(self, param_matches: list[ParamMatch]):
        for param_match in param_matches:
            tag = param_match.get_tag
            if not pd.isna(tag):
                if tag.is_muted:
                    raise ValueError('Tag muted')
                if not self.tag_in_view(tag):
                    raise ValueError('Tag nog in view')

    def run(self, param_matches: list):
        param_matches = sorted([ParamMatch(i) for i in param_matches])

        self.validate_h2go(param_matches)
        self.validate_tag(param_matches)

        for key, group in it.groupby(param_matches, lambda x: x.h2go_only):
            if key:
                logger.info(10*'=' + 'H2GO only' + 10*'=')

                for g in group:
                    g.map['h2go'].save()

        for key, group in it.groupby(param_matches, lambda x: x.h2go_tag | x.tag_only):
            if key:
                group = sorted(group, key=lambda x: x.get_tag.location)
                for loc, group in it.groupby(group, lambda x: x.get_tag.location):
                    group = list(group)

                    if any(g.tag_only for g in group):
                        logger.info(10*'=' + 'Tag only' + 10*'=')
                        self.cgoo.get_timeseries(loc)
                        for g in group:
                            self.cgoo.save(g.get_tag)

                    else:
                        logger.info(10*'=' + 'H2GO + TAG' + 10*'=')
                        startdatetime = min(g.map['h2go'].enddatetime for g in group)
                        self.cgoo.get_timeseries(loc, startdatetime)
                        for g in group:
                            g.map['h2go'].save()
                            self.cgoo.save(g.get_tag)
