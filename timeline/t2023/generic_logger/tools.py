from IPython.display import HTML
from timeline.t2023.generic_logger import IModifier
from useful.basic import NameSpace
from modules.SearchSystem.modular import HideableWidget
from modules.Explorer.personalizedWidgets import CustomOutput
class ModelData:
    def __init__(self):
        self._loc = []
        self.set_label_func(lambda data: data["name"])
    def dirList(self):
        vals = []
        for k in self._data:
            vals.append((self._label_func(self._data[k]), k)) 
        return [], vals
    def set_data(self, data):
        self._data = data
    def cd(self, key):
        if key == "..":
            self.goback()
        elif key == ".":
            pass
        else:
            self._loc.append(key)
    def goback(self):
        if len(self._loc) != 0:
            self._loc.pop()
    @property
    def path(self):
        return "/".join(self._loc)
    def set_label_func(self, func):
        self._label_func = func
    def set_controller(self, cnt):
        self._controller = cnt
    def update_data(self):
        self._data = self._controller._model.read(self._controller.controllers.ldcc._cur_btn.description)
        self.set_data(self._data["data"])
class LogReader(IModifier):
    def __init__(self):
        from timeline.t2023.explorer import Main
        self._bc = Main.basic_explorer()
        md = ModelData()
        self._bc.set_model(md)
        self.set_select_func(self._default_select_func)
    def set_select_func(self, func):
        self._file_selected_func = func
    def _prepare_views(self):
        self._bsc.views = NameSpace()
        self._bsc.views.out = CustomOutput()
        self._bsc.views.layout = self._bc.views.ev.layout
        self._bc.views.ev.left_side.children = list(self._bc.views.ev.left_side.children)[:-1] + [self._bsc.views.out.get_layout()]
    def set_up(self):
        self._bsc = NameSpace()
        self._bsc.controllers = NameSpace()
        self._bsc.controllers.exp = self._bc
        self._bsc.controllers.generic = self._basic_cont
        self._prepare_views()
        self._bc._model.set_controller(self._basic_cont)
        self._bc._model.update_data()
        ec = self._bc.controllers.ec
        ec.set_up()
        ec.set_file_selected_func(self.on_selected_ele)
    def set_basic_controller(self, bsc):
        self._basic_cont = bsc
    def get_layout(self):
        return self._bc.views.ev.layout
    def _default_select_func(self, wid, *param):
        self._bc.views.ev.outputDisplay.clear()
        with self._bc.views.ev.outputDisplay.get_out():
            val = self._bc.views.ev.fileFoldersListWid.value
            display(self._get_html_view(self._bc._model._data[val]))
    def on_selected_ele(self, wid, *param):
        self._file_selected_func(wid, self)
    def _get_html_view(self, vals):
        forma = lambda x: f"""<font face='comic sans ms' color ='darkcyan'>{x}</font>"""
        res = ""
        for ke  in vals:
            content = str(vals[ke])
            if type(vals[ke]) == str:
                content = "<br>".join(vals[ke].splitlines())
            res +=  forma(ke) + ": " + content + "<br>"
            res += ("-"*40) + "<br>"
        return (HTML(res))
class Main:
    def example(bsc, label_func = None):
        lr = LogReader()
        lr.set_basic_controller(bsc)
        if label_func:
            lr._bc._model.set_label_func(label_func)
        return lr.get_layout(), lr
