import os
os.environ['RAISE'] = "0"                                  # $env:RAISE='0'

import logging                                            # noqa
logger = logging.getLogger(__name__)

import datetime as dt                                     # noqa
from pprint import pprint                                 # noqa
from dotenv import load_dotenv                            # noqa

if not load_dotenv():
    logger.warn('Evironment variables not loaded')

import numpy as np   # noqa
import pandas as pd  # noqa

from fews_spoccer.spoc.spoccer import Spoccer                                   # noqa
from fews_spoccer.spoc.dtypes import Tag                                        # noqa
from fews_spoccer.modules.imports.opvlwater import OpvlWaterModule, ParamMatch  # noqa
from fews_spoccer.modules.imports.h2go import H2GO                              # noqa
from fews_spoccer.modules.imports.cgoo import CGOO                              # noqa


read_kw = {
    'sep': ';',
    'index_col': False,
    'dtype': object,        # all data is initially read as strings
    'na_values': '',        # empty strings are classified 'NaN'
    'encoding': 'cp1252',
}
write_kw = {
    'sep': ';',
    'index': False,
    'encoding': 'cp1252'
    }

srcdir = './tests/data/maplayerfiles'
dstdir = './tests/output/maplayerfiles'

spoccer = Spoccer(srcdir, dstdir, read_kw, write_kw)
spoccer.load()
spoccer.validate()
spoccer.save()

# ########################### MODULES ##########################

modules = {
    'imports': {
        'h2go': {
            'srcpath': './tests/data/imports',
            'dstpath': './tests/output/imports',
            'read_kw': {
            },
            'write_kw': {
                'index': False
            },
        },
        'cgoo': {
            'dstpath': './tests/output/imports',
            'credentials': {
                'server': os.environ.get('DB_SERVER'),
                'driver': os.environ.get('DB_DRIVER'),
                'database': os.environ.get('DB_DATABASE'),
                'username': os.environ.get('DB_USERNAME'),
                'password': os.environ.get('DB_PASSWORD')
            },
            'write_kw': {
                'index': False
            }
        }
    }
}

param_matches = spoccer.hl.get_param_matches('HL000562')
param_matches.append({'id': 'OW001380', 'param': 'QM',
                      'ws_tags': np.nan, 'ws_ti_h2go_tags': '6677_46052'})

tag1 = Tag.parse(r'''~SCX.~Watersysteem.Objecten.De Baanbreker.Ronde Morgen.'''
                 r'''Tags.NL*09*001049 wtSTs--1001.s--1001_SD.Historic''')
tag2 = Tag.parse(r'''~SCX.~Watersysteem.Objecten.Vijfheerenlanden.Kikkert'''
                 r''', de.Tags.NL*09*001596 wtSTLT-1002.LT-1002_SI.Historic''')

'''
param_matches.append({'id': 'OW001380', 'param': 'QM',
                      'ws_tags': tag1, 'ws_ti_h2go_tags': np.nan})
'''

startdate = dt.datetime(2023, 1, 1)
enddate = dt.datetime(2023, 3, 1)


h2go_config = modules['imports']['h2go']
cgoo_config = modules['imports']['cgoo']

h2go = H2GO(**h2go_config)
cgoo = CGOO(**cgoo_config)

opvl_mod = OpvlWaterModule(h2go_config, cgoo_config)
