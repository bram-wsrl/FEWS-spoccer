import unittest
import filecmp
from pathlib import Path


from fews_spoccer.spoc.spoccer import Spoccer


read_kw = {
    'sep': ';',
    'index_col': False,
    'dtype': object,            # all data is initially read as strings
    'na_values': [''],          # empty strings are classified 'NaN'
    'keep_default_na': False,   # only empty fields are set 'NaN'
    'encoding': 'cp1252',
}
write_kw = {
    'sep': ';',
    'index': False,
    'encoding': 'cp1252'
    }

srcdir = './tests/data/maplayerfiles'
dstdir = './tests/output/maplayerfiles'


class TestSpoccer(unittest.TestCase):
    def test_save(self):
        '''MapLayerFiles should not change on save'''
        self.spoccer = Spoccer(srcdir, dstdir, read_kw, write_kw)
        self.spoccer.load()
        self.spoccer.validate()
        self.spoccer.save()

        srcfiles = sorted(list(Path(srcdir).iterdir()))
        dstfiles = sorted(list(Path(dstdir).iterdir()))
        for srcfile, dstfile in zip(srcfiles, dstfiles):
            self.assertTrue(filecmp.cmp(srcfile, dstfile))
