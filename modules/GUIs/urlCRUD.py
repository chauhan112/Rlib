from modules.Explorer.personalizedWidgets import GenerateNRowsBox
import ipywidgets as widgets
from PickleCRUDDB import PickleCRUDOps
from SearchSystem import DicSearchEngine,UrlSearchEngine
class IUrlOps:
    def display(self):
        pass
class GUrlOps(IUrlOps):
    def set_parent(self, parent):
        self._parent = parent
class ReadOps(GUrlOps):
    def __init__(self):
        self._dic_engine = UrlSearchEngine({})
    def display(self):
        self._dic_engine.searchSys.set_container(self._parent._pcrud.readAll())
        self._dic_engine.search("")
class DeleteOps(GUrlOps):
    def __init__(self):
        self._confirm_btn = widgets.Button(description="confirm")
        self._confirm_btn.on_click(self._confirm)
        self._dic_engine = DicSearchEngine({})
        self._dic_engine.setCallback(self._delete)
    def display(self):
        self._set_and_display()
    def _set_and_display(self):
        self._dic_engine.searchSys.set_container(self._parent._pcrud.readAll())
        self._parent._gnrb.get_child(2).get_child(0).clear_output()
        self._parent._gnrb.get_child(1).get_child(0).clear_output()
        self._dic_engine.search("")
    def _delete(self, key, val):
        self._last_key = key
        out = self._parent._gnrb.get_child(2).get_child(0)
        out.clear_output()
        with out:
            display(self._confirm_btn)
    def _confirm(self, btn ):
        self._parent._pcrud.delete(self._last_key)
        self._set_and_display()
class AddOps(GUrlOps):
    def __init__(self):
        self._url_anme = widgets.Text(placeholder="key")
        self._url = widgets.Text(placeholder="value")
        self._is_var = widgets.Checkbox(description="is var", indent =False)
        self._add_btn = widgets.Button(description="add")
        self._add_btn.on_click(self._click)
    def display(self):
        self._url_anme.value = ""
        self._url.value = ""
        display(widgets.HBox([self._url_anme, self._url, self._is_var, self._add_btn]))
    def _click(self,btn ):
        name = self._url_anme.value.strip()
        val = self._url.value.strip()
        if self._is_var.value:
            from jupyterDB import jupyterDB
            val = jupyterDB._params[val]
        for v in [name, val]:
            if v == "":
                return
        self._parent._pcrud.add(name,val)
        self._parent._out.clear_output()
class CategoryGUICrud:
    def __init__(self):
        self._ops_map = {
            'add': AddOps(),
            'delete': DeleteOps(),
            'read': ReadOps()
        }
        for v in self._ops_map.values():
            v.set_parent(self)
        self._gnrb = None
    def _on_cat_selected(self, btn):
        self.change_category(self._gnrb.get_child(0).get_child(0).value)
        self._out.clear_output()
        self._gnrb.get_child(2).get_child(0).clear_output()
        with self._out:
            self._ops_map[self._gnrb.get_child(0).get_child(1).value].display()
    def set_category_func(self, func):
        self._func = func
    def set_pickle_file(self, file):
        self._pcrud = PickleCRUDOps()
        self._pcrud.set_pickle_file(file)
        self._pcrud.set_always_sync(True)
    def _make_layout(self):
        self._gnrb = GenerateNRowsBox(3)
        self._gnrb.get_child(0).add_widget(widgets.Dropdown(options=self._func(self), layout= {'width': 'auto'}))
        self._gnrb.get_child(0).add_widget(widgets.Dropdown(options=['read', "delete", 'add'],
                                                            layout= {'width': 'auto'}))
        self._gnrb.get_child(0).add_widget(widgets.Button(description="select", layout= {'width': 'auto'}))
        self._out = widgets.Output()
        self._gnrb.get_child(1).add_widget(self._out)
        self._gnrb.get_child(0).get_child(-1).on_click(self._on_cat_selected)
        self._gnrb.get_child(2).add_widget(widgets.Output())
    def display(self):
        if self._gnrb is None:
            self._make_layout()
        return self._gnrb.get()
    def change_category(self, key):
        self._pcrud.set_base_location([key], relative = True)
class Main:
    def url_crud_gui(pkl_file, base_loc: list = []):
        ugu = CategoryGUICrud()
        ugu.set_pickle_file(pkl_file)
        ugu._pcrud.set_root(base_loc)
        ugu.set_category_func(lambda self: self._pcrud.readAll().keys())
        display(ugu.display())
        return ugu