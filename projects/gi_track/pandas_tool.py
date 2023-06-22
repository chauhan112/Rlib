import pandas as pd
class DataframeSetable:
    def set_dataframe(self, df: pd.DataFrame):
        self.df = df

class CellsCrud(DataframeSetable):
    def update_cells(self, rows_indices: list, columns: list, value):
        """
        Eg: data.iloc[[0,1,3,6],[0]] = 100
        """
        self.df.iloc[rows_indices, columns] = value
    def update_cell(self, row_index, column, value):
        self.df.at[row_index, column] = value
class RowCrud(DataframeSetable):
    def delete_row(self, indices: list):
        if type(indices) not in (list, tuple):
            indices = [indices]
        self.df.drop(indices)
    def update_rows(self, row_indices: list, values):
        self.df.iloc[row_indices] = values
    def filter_rows(self, bit_filter: list[bool]):
        return self.df[bit_filter]
    def filter_row_with_func(self, func):
        bit_filter = self.df.apply(func, axis= 1)
        return self.filter_rows(bit_filter)

class ColumnCrud(DataframeSetable):
    def add_new_column(self, colname, values: list):
        return self.df.assign(**{colname:values})
    def delete_column(self, cols: list[str]):
        if type(cols) not in (tuple, list):
            cols = [cols]
        cols = set(cols)
        columns = set(self.read_columns())
        rems = list(columns.difference(cols))
        return self.df[rems]
    def update_column(self, column_name, func):
        self.df[column_name] = self.df[column_name].apply(func)
    def update_col_values(self, colname, values:list):
        self.df[colname] = values
    def read_columns(self):
        return self.df.columns.to_list()
    def rename(self,old_index, new_index):
#         cols = {c: c for c in self.read_columns()}
#         cols[old_index] = new_index
        return self.df.rename(columns={old_index:new_index})
class DataframeOps:
    def add_dataframes_rowwise(dfs: list[pd.DataFrame]):
        """they must have same column"""
        return pd.concat(dfs)
    def add_dataframes_column_wise(dfs: list[pd.DataFrame]):
        """they must have same number of rows"""
        return pd.concat(dfs, axis=1)
    def create_new_df(cols, values):
        return pd.DataFrame(values, columns=cols)


class PandasOps(DataframeSetable):
    def __init__(self):
        self._row_ops = RowCrud()
        self._col_ops = ColumnCrud()
    @property
    def rows_ops(self):
        self._row_ops.set_dataframe(self.df)
        return self._row_ops
    @property
    def cols_ops(self):
        self._col_ops.set_dataframe(self.df)
        return self._col_ops
    def save(self, name:str):
        if not name.endswith('.csv'):
            name += ".csv"
        self.df.to_csv(name)