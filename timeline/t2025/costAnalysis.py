import htmlDB import htmlDB
class MyTransactions:
    def set_file(self, file):
        from FileDatabase import File
        self.set_content(File.getFileContent(file))
    def set_content(self, content):
        self._content = content
        self._pdata = htmlDB.getParsedData(content)
        self.rows = list(filter(lambda x: "class" in x.attrs and "hasSEPADetails" in x.attrs["class"], bfs_soup(self._pdata.tbody, 1)))
        self.parsed_row = list(map(self.getKeyVal, self.rows))
    def get_from_clipboard(self):
        from jupyterDB import jupyterDB
        self.set_content(jupyterDB.clip().copy())
    def getKeyVal(self, rowTd):
        res = {}
        for v in htmlDB.bfs_soup(rowTd, 1, True):
            if v.name == "td":
                ke = v.get("headers")
                if len(ke) > 0:
                    k = ke[0]
                    res[k] = v.text.strip()
        return res
    def getTotalPaid(self):
        k = "bTdebit"
        k2 = "Direct Debit return"
        filterFunc = lambda x: x[k] != ""
        fl = sorted(filter(filterFunc, self.parsed_row), key = lambda x: float(x[k].replace(",", "").replace(k2, "") ))
        rows = list(map(lambda x: float(x[k].replace(",", "").replace(k2, "")), fl ))
        self._state = locals()
        return sum(rows)
    def getTotalReceived(self):
        k = "bTcredit"
        fl = list(filter(lambda x: x[k] != "", self.parsed_row))
        rows = list(map(lambda x: float(x[k].replace(",", "")),fl ))
        self._state = locals()
        return sum(rows)
    def getPaid(self):
        k = "bTdebit"
        k2 = "Direct Debit return"
        filterFunc = lambda x: k2 not in x[k]
        fl = list(filter(filterFunc, self.parsed_row))
        rows = list(map(lambda x:  x[k] != "" and float(x[k].replace(",", "") ), fl ))
        self._state = locals()
        return sum(rows)
    def getAutoDeduced(self):
        k = "bTdebit"
        k2 = "Direct Debit return"
        filterFunc = lambda x: k2 in x[k]
        fl = list(filter(filterFunc, self.parsed_row))
        rows = list(map(lambda x: float(x[k].replace(",", "").replace(k2, "")), fl ))
        self._state = locals()
        return sum(rows)