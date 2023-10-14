from pprint import pprint  # noqa

from fews_spoccer.spoc.spoccer import Spoccer


read_kw = {
    'sep': ';',
    'index_col': False,
    'dtype': object,
    'keep_default_na': False,
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
spoccer.validate_raising()
spoccer.save()
