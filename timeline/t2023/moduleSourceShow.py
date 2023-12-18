import inspect
from timeline.t2023.generic_logger import SearchView
from WidgetsDB import WidgetsDB
from ModuleDB import ModuleDB
class ShowSource:
    def __init__(self):
        self.searchView = SearchView()
        WidgetsDB.hide(self.searchView.isRegWid)
        WidgetsDB.hide(self.searchView.isCase)
        self.searchView.btn.description = "show source"
        self.searchView.textWid.placeholder = "module or class name"
    def set_up(self):
        self.searchView.btn.set_clicked_func(self._displaySource)
    def _displaySource(self, w):
        val = self.searchView.textWid.value.strip()
        if not val:
            return
        res = inspect.findsource(self._scope[val])
        x = ModuleDB.colorPrint("python","".join(res[0]))
        self.searchView.couput.display(res[1], True)
        self.searchView.btnOutput.display(x, True)
    def set_scope(self, scope):#
        self._scope = scope
class Main:
    def show(scope):
        ss = ShowSource()
        ss.set_up()
        ss.set_scope(scope)
        return ss