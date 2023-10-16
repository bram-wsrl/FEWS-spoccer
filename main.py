import os
from pprint import pprint  # noqa

from fews_spoccer.spoc.spoccer import Spoccer
from fews_spoccer.modules.imports import opvlwater, h2go, cgoo  # noqa


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
pprint(spoccer.hl.param_value_matches('HL000001', True))
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

tag_iwa_muted = r'<<!~SCX.~Watersysteem.Objecten.De Baanbreker.Complex Meiweg.Tags.2.NL*09*001057 wtSTs--2001.s--2001_SD.Historic>>>'
tag_iwa = r'~SCX.~Watersysteem.Objecten.De Baanbreker.Complex Meiweg.Tags.2.NL*09*001057 wtSTs--2001.s--2001_SD.Historic'
tag_iwa_ = r'~SCX.~Watersysteem.Objecten.De Baanbreker.Complex Meiweg.Tags.NL*09*001057 wtSTs--2001.s--2001_SD.Historic'

tag_pbh_muted = r'<<<~SCX.Pbh.BomWa.Hurwenen (Gml).DI.0318 Pomp in bedrijf.Historic>>>'
tag_pbh = r'~SCX.Pbh.BomWa.Hurwenen (Gml).DI.0318 Pomp in bedrijf.Historic'

tag_invalid = r'~SCX.~Keringen.Objecten.De Baanbreker.Complex Meiweg.Tags.2.NL*09*001057 wtSTs--2001.s--2001_SD.Historic'

tag1 = cgoo.Tag(tag_iwa_muted)
tag2 = cgoo.Tag(tag_iwa)
tag3 = cgoo.Tag(tag_iwa_)
tag4 = cgoo.Tag(tag_pbh_muted)
tag5 = cgoo.Tag(tag_pbh)
tag6 = cgoo.Tag(tag_invalid)
