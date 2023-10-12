import pandas as pd


class SelectorMixin:
    def row(self, *ids: str) -> pd.DataFrame:
        return self.df.loc[self.df[self.id].isin(ids), :]

    def column(self, column: str) -> pd.DataFrame:
        return self.df.loc[:, column]

    def field(self, ids: str | list[str], column: str) -> pd.DataFrame:
        return self.df.loc[self.df[self.id].isin(ids), column]

    def ids_by_pids(self, *pids: str) -> pd.DataFrame:
        return self.df.loc[self.df[self.pid].isin(pids), self.id]

    def ids_by_area(self, *areas: str) -> pd.DataFrame():
        return self.df.loc[self.df[self.area].isin(areas), self.id]


class ValidatorMixin:
    def columns_exist(self):
        assert set(self.df.columns) == set(
            c.name for c in self.columns.values()), self

    def unique_ids(self):
        assert self.column(self.id).squeeze().is_unique, self
