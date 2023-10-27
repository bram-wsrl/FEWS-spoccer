import logging
from pathlib import Path
import datetime as dt

import pandas as pd

from fews_spoccer.utils import log, catch
from ...spoc.etypes import (
    H2GOFileNotFoundException, H2GOMultipleFilesFoundException,
    H2GOFileContentException)


logger = logging.getLogger(__name__)


class H2GO:
    fmt = '%d-%m-%Y %H:%M:%S'

    def __init__(self, srcpath, dstpath, read_kw, write_kw):
        self.srcpath = Path(srcpath)
        self.dstpath = Path(dstpath)
        self.read_kw = read_kw
        self.write_kw = write_kw

        self.pattern = None
        self.filepath = None

        self._df = pd.DataFrame()

    def __repr__(self):
        return f'{self.__class__.__name__}({self.filepath.name})'

    @property
    def df(self):
        return self._df

    @property
    def is_empty(self):
        return self.df.empty

    def concat_dt(self, idx, fmt):
        return dt.datetime.strptime(
            ' '.join((
                self.df.iloc[idx]['DATUM'],
                self.df.iloc[idx]['TIJD'])), fmt)

    @property
    def startdatetime(self):
        return self.concat_dt(0, self.fmt)

    @property
    def enddatetime(self):
        return self.concat_dt(-1, self.fmt)

    @log(logger)
    def file_exists(self, pattern):
        filetree = self.srcpath.rglob('*.csv')
        filepath = [p for p in filetree if p.name.startswith(pattern)]

        if len(filepath) == 1:
            self.pattern = pattern
            self.filepath = filepath[0]
            return True

        elif len(filepath) == 0:
            raise H2GOFileNotFoundException(pattern)
        else:
            raise H2GOMultipleFilesFoundException(filepath, pattern)

    @log(logger)
    def read(self):
        self._df = pd.read_csv(self.filepath, **self.read_kw)

    @log(logger)
    def check_content(self):
        locid, mptid = self.pattern.split('_')
        if not all(self.df.LOCATIEID.astype(str) == locid):
            raise H2GOFileContentException(self.filepath, locid)

        if not all(self.df.MEETPUNTID.astype(str) == mptid):
            raise H2GOFileContentException(self.filepath, mptid)

    @log(logger)
    def convert_tz(self, tz_in='utc', tz_out='Europe/Amsterdam'):
        datum_tijd = self.df.DATUM + ' ' + self.df.TIJD

        tz_in_naive = pd.to_datetime(datum_tijd, dayfirst=True)
        tz_in_aware = pd.Index(tz_in_naive).tz_localize(tz_in)

        tz_out_aware = tz_in_aware.tz_convert(tz_out)
        tz_out_naive = pd.Series(tz_out_aware.strftime('%d-%m-%Y %H:%M:%S'))

        self._df[['DATUM', 'TIJD']] = tz_out_naive.str.split(expand=True)

    @log(logger)
    def write(self):
        self.df.to_csv(self.dstpath / self.filepath.name, **self.write_kw)

    @catch(logger)
    @log(logger, level=logging.INFO)
    def validate(self, pattern):
        self.file_exists(pattern)
        self.read()
        self.check_content()
        self.convert_tz()

    @classmethod
    def load(cls, pattern, config):
        obj = cls(**config)
        obj.validate(pattern)
        return obj

    @log(logger, level=logging.INFO)
    def save(self):
        self.write()
