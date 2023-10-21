import pandas as pd

from .ctypes import Column


class SelectorMixin:
    def row(self, *ids: str) -> pd.DataFrame:
        return self.df.loc[ids,]

    def column(self, column: str) -> pd.Series:
        return self.df[column]

    def field(self, id: str, column: Column) -> str:
        return column.instance(self.df.loc[id, column])

    def join_fields(self, id: str, *columns: str) -> str:
        fields = [self.field(id, c) for c in columns]
        return '_'.join(str(v) for v in fields if pd.notna(v))

    def ids_by_pids(self, *pids: str) -> pd.Index:
        return self.df[self.df[self.pid].isin(pids)].index

    def ids_by_area(self, *areas: str) -> pd.Index:
        return self.df[self.df[self.area].isin(areas)].index
