class LibreOffice:
    def set_file(self, filepath: str):
        import pandas as pd
        self._file_path = filepath
        self._data = pd.read_excel(self._file_path, engine="odf", sheet_name= None)
    def set_sheet(self, sheetName: str):
        self._sheet = sheetName
    def read(self, asList=True):
        if self._sheet is None:
            self._sheet = list(self._data.keys())[0]
        df = self._data[self._sheet]
        if asList:
            return df.values.tolist()
        return df
    def get_all_sheets(self):
        return list(self._data.keys())
class Main:
    def read(name, sheet=None, asList = True):
        lo = LibreOffice()
        lo.set_file(name)
        lo.set_sheet(sheet)
        return lo.read(asList)
    def get_sheets(name):
        lo = LibreOffice()
        lo.set_file(name)
        return lo.get_all_sheets()
