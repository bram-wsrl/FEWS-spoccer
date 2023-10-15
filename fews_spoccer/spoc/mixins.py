import logging

import pandas as pd


logger = logging.getLogger(__name__)


class SelectorMixin:
    def row(self, *ids: str) -> pd.DataFrame:
        return self.df.loc[ids,]

    def column(self, column: str) -> pd.Series:
        return self.df[column]

    def field(self, id: str, column: str) -> str:
        return self.df.loc[id, column]

    def join_fields(self, id: str, *columns: str) -> str:
        fields = [self.field(id, c) for c in columns]
        return '_'.join(str(v) for v in fields if v != '')

    def ids_by_pids(self, *pids: str) -> pd.Index:
        return self.df[self.df[self.pid].isin(pids)].index

    def ids_by_area(self, *areas: str) -> pd.Index:
        return self.df[self.df[self.area].isin(areas)].index
