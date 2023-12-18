from timeline.t2023.generic_logger import AdvanceSearchView
from timeline.t2023.links_crud_ui import SearchEngine
class AdvanceSearcher:
    def __init__(self):
        self._concatenated_search = None
        self._fields_search = None
    def set_view(self, view: AdvanceSearchView):
        self._view = view
    def set_up(self):
        self._view.btn.set_clicked_func(self._searched)
    def set_searcher(self, searcher: SearchEngine):
        self._searcher = searcher
    def _searched(self, wid):
        word = self._view.textWid.value
        mmp = {"any":[False, False], "reg":[True, False], "case": [False, True]}
        val = self._view.searchType.value
        if val in ["case","reg", "any"]:
            reg, case = mmp[val]
            res = self._searcher.search(word, reg=reg, case=case)
            self._view.couput.display(res, clear=True, ipy=True)
        elif val == "word":
            reg = True
            word = f"\\b{word}\\b"
            res = self._searcher.search(word, reg=reg, case=case)
            self._view.couput.display(res, clear=True, ipy=True)
        elif val == "concatenated" and self._concatenated_search:
            res = self._concatenated_search(word, reg=reg, case=case)
            self._view.couput.display(res, clear=True, ipy=True)
        else:
            print(val, "is not implemented")

    def set_concatenated_searcher(self, concaten):
        self._concatenated_search = concaten
class Main:
    def search_with_advance_options(searcher: SearchEngine, concat=None):
        ass = AdvanceSearcher()
        ass.set_searcher(searcher)
        ass.set_view(AdvanceSearchView())
        ass.set_up()
        if concat:
            ass.set_concatenated_searcher(concat)
        return ass
