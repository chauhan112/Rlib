import inspect
from useful.WidgetsDB import WidgetsDB
from useful.ModuleDB import ModuleDB
import ipywidgets as widgets
from modules.Explorer.personalizedWidgets import CustomOutput
from timeline.t2023.generic_logger.components import SingleButtonController

class SearchView:
    def __init__(self):
        self.textWid = widgets.Text(placeholder = "word", layout={"width":"auto"})
        self.isRegWid = widgets.Checkbox(description="is reg", indent =False, layout={"width":"auto"})
        self.isCase = widgets.Checkbox(description="case", indent =False, layout={"width":"auto"})
        self.btn = SingleButtonController(description="search", layout={"width":"auto"})
        self.couput = CustomOutput()
        self.btnOutput = CustomOutput()
        self.searchRow = widgets.HBox([self.textWid, self.isRegWid, self.isCase, self.btn.layout])
        self.layout = widgets.VBox([self.searchRow,self.couput.get_layout(), self.btnOutput.get_layout()])
class ShowSource:
    def __init__(self):
        self.searchView = SearchView()
        WidgetsDB.hide(self.searchView.isRegWid)
        WidgetsDB.hide(self.searchView.isCase)
        self.searchView.btn.description = "show source"
        self.searchView.textWid.placeholder = "module or class name"
    def set_up(self):
        #self.searchView.btn.set_clicked_func(self._displaySource)
        self.searchView.btn.set_clicked_func(self._display_with_line_numbers)
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
    def _display_with_line_numbers(self,w):
        if not hasattr(self, "chl"):
            from timeline.t2024.code_highlight import CodeHighlighter
            self.chl = CodeHighlighter()
        val = self.searchView.textWid.value.strip()
        if not val:
            return
        res = inspect.findsource(self._scope[val])
        content = "".join(res[0])
        self.chl.handlers.set_content(content)
        self.searchView.couput.display(res[1] + 1, True)
        self.searchView.btnOutput.display(self.chl.views.container.outputs.layout, True)
class Main:
    def show(scope):
        ss = ShowSource()
        ss.set_up()
        ss.set_scope(scope)
        return ss