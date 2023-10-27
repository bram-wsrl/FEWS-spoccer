import time
import logging
import functools
import datetime as dt
from pathlib import Path

import pyodbc
import pandas as pd

from ...utils import catch, log
from ...spoc.etypes import MutedTagException, TagNotInViewException


logger = logging.getLogger(__name__)


class CGOOBase:
    '''Connect to CGOO database'''

    def __init__(self, credentials):
        self.credentials = credentials

        self._connection = None
        self._cursor = None

    def __repr__(self):
        return f'<{self.__class__.__name__}(connected={self.is_connected})>'

    @property
    def connection_string(self):
        c = self.credentials
        return (f'''DRIVER={{{c['driver']}}};'''
                f'''SERVER={c['server']};DATABASE={c['database']};'''
                f'''UID={c['username']};PWD={c['password']}''')

    @property
    def is_connected(self):
        return bool(self._connection)

    @log(logger, level=logging.INFO)
    def connect(self):
        self._connection = pyodbc.connect(self.connection_string)
        self._cursor = self._connection.cursor()

    def query(self, sql_statement, *args):
        self._cursor.execute(sql_statement, *args)

        logger.debug(f'cgoo - query - {", ".join(args)}')


class CGOO(CGOOBase):
    sql_stmt_fmt = 'exec [dbo].SP_sub_Long_Hist ?, ?, ?'
    default_time_window = dt.timedelta(days=31)
    query_delay_seconds = 1
    global_startdatetime = dt.datetime(2023, 6, 1)  # test setting

    def __init__(self, dstpath, write_kw, credentials):
        super().__init__(credentials)

        self.dstpath = Path(dstpath)
        self.write_kw = write_kw

        self._df = pd.DataFrame()
        self.query_args = ()
        self.query_response = None

    @property
    def df(self):
        return self._df

    @catch(logger)
    @log(logger, level=logging.INFO)
    def validate(self, tag):
        if tag.is_muted:
            raise MutedTagException(tag)
        if tag.tag not in self.get_unique_tags(tag.location):
            raise TagNotInViewException(tag)

    @staticmethod
    def dt2str(datetime, fmt="%Y-%m-%d %H:%M:%S"):
        return dt.datetime.strftime(datetime, fmt)

    def get_tag_df(self, tag, startdatetime=None):
        startdatetime = startdatetime or self.global_startdatetime

        return self.df[
            (self.df.TagName == tag.tag) &
            (self.df.DateTime > startdatetime + dt.timedelta(seconds=1))]\
            .sort_values('DateTime')

    def datetimeperiod(self, tag):
        tag_df = self.get_tag_df(tag)
        startdatetime = tag_df.iloc[0][0]
        enddatetime = tag_df.iloc[-1][0]
        return startdatetime, enddatetime

    def query(self, location, startdatetime, enddatetime):
        time.sleep(self.query_delay_seconds)

        self.query_args = (
            location,
            self.dt2str(startdatetime),
            self.dt2str(enddatetime)
            )

        super().query(self.sql_stmt_fmt, *self.query_args)
        self.query_response = self._cursor.fetchall()
        return self.query_response

    def empty_response(self):
        tags, values = [], []
        for _, tag, value in self.query_response:
            tags.append(tag)
            values.append(value)

        all_None = all(isinstance(v, type(None)) for v in values)
        if len(set(tags)) == len(tags) and all_None:
            return True
        return False

    @functools.lru_cache(maxsize=10)
    def get_unique_tags(self, location):
        future_start = future_end = dt.datetime.now() + dt.timedelta(days=1)
        response = self.query(location, future_start, future_end)
        return set(i[1] for i in response)

    def get_timeseries(self, location, startdatetime=None, enddatetime=None):
        t_start = startdatetime or self.global_startdatetime
        t_end = enddatetime or dt.datetime.now()
        t_i = t_end - self.default_time_window

        logger.info(f'{location=} from={str(t_start)} to={str(t_end)} ...')

        df_data = []
        while True:
            if t_i < t_start:
                df_data += self.query(location, t_start, t_end)
                break
            else:
                df_data += self.query(location, t_i, t_end)

            t_end = t_i
            t_i = t_i - self.default_time_window

            if self.empty_response():
                break

        header = [i[0] for i in self._cursor.description]
        self._df = pd.DataFrame.from_records(df_data, columns=header)

    def save(self, tag, startdatetime=None, reldir=''):
        dstpath = self.dstpath / reldir
        filepath = dstpath / tag.filename()
        startdatetime = startdatetime or self.global_startdatetime

        self.get_tag_df(tag, startdatetime).to_csv(filepath, **self.write_kw)

        logger.info(f'{filepath.name}')
