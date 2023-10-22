import os
os.environ['RAISE'] = "0"                                  # $env:RAISE='0'

from pprint import pprint  # noqa

import numpy as np   # noqa
import pandas as pd  # noqa

from fews_spoccer.spoc.spoccer import Spoccer             # noqa
from fews_spoccer.spoc.dtypes import Tag                  # noqa
from fews_spoccer.modules.imports import opvlwater, h2go  # noqa


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
            'dstpath': './tests/output',
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

h2go_config = modules['imports']['h2go']
cgoo_config = modules['imports']['cgoo']

h2go_obj = h2go.H2GO(**h2go_config)

opvl_mod = opvlwater.OpvlWaterModule(h2go_config, cgoo_config)
