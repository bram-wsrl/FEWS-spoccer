from .h2go import H2GO
from .cgoo import CGOO, Tag


class OpvlWaterModule:
    def __init__(self, h2go_config, cgoo_config):
        self.h2go_config = h2go_config
        self.cgoo_config = cgoo_config

    def validate_h2go(self, pattern):
        h2go = H2GO(**self.h2go_config)
        h2go.load(pattern)
        return h2go

    def validate_cgoo(self, tag):
        # parse tag for validity
        # tag is muted?
        # tag in view?
        # return Tag_obj
        pass
