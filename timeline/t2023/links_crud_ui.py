from modules.SearchSystem.modular import HideableWidget
from modules.Explorer.personalizedWidgets import VRBox
import ipywidgets as widgets
from PickleCRUDDB import PickleCRUDOps
from SearchSystem import ISearch, DicSearch
class CustomOutput:
    def __init__(self):
        self._layout = None
        self.set_base_layout(VRBox())
    def set_base_layout(self, base):
        self._base_container = base
    def display(self,layout, clear= False, ipy= False):
        if ipy:
            if clear:
                self._base_container.clear()
                self._out.clear_output()
            self._base_container.add_widget(layout)
        else:
            if clear:
                self._base_container.clear()
                self._out.clear_output()
            with self._out:
                display(layout)
    def get_layout(self):
        if self._layout is None:
            self._out = widgets.Output()
            self._layout = widgets.VBox([self._base_container.get(), self._out])
        return self._layout
    def get_out(self):
        return self._out
class LinksManagerView:
    def __init__(self):
        self._layout =None
    def _make_layout(self):
        self.keysDrpWid = widgets.Dropdown(layout = {"width":"auto" })
        self.opsDrpWid = widgets.Dropdown(options =["read", "delete", "add"],layout = {"width":"auto" })
        self.selectBtn = widgets.Button(description="select", layout = {"width":"auto" })
        self.addKeyWid = widgets.Text(placeholder = "key", layout={"width":"auto"})
        self.addValueWid = widgets.Text(placeholder = "value", layout={"width":"auto"})
        self.addIsVarWid = widgets.Checkbox(description="is var", indent =False, layout={"width":"auto"})
        self.addAddBtn = widgets.Button(description="add", layout={"width":"auto"})
        self.addRowWid = widgets.HBox([self.addKeyWid, self.addValueWid, self.addIsVarWid, self.addAddBtn])
        self.deleteConfirmBtn = widgets.Button(description="confirm")
        self.cout = CustomOutput()
        self._layout = widgets.VBox([widgets.HBox([self.keysDrpWid, self.opsDrpWid, self.selectBtn]),self.addRowWid, self.cout.get_layout(), self.deleteConfirmBtn])
    @property
    def layout(self):
        if self._layout is None:
            self._make_layout()
        return self._layout
class LinksManagerController:
    def set_searcher(self, searcher):
        self._searcher = searcher
    def set_view(self, view):
        self._view = view
        self._hideable = HideableWidget()
    def setup(self):
        self._view.selectBtn.on_click(self._show_elements)
        self._view.keysDrpWid.options = list(self._pcrud.readAll().keys())
        self._view.addAddBtn.on_click(self._add_new)
        self._view.deleteConfirmBtn.on_click(self._delete_entry_confirmed)
        self.hide(self._view.addRowWid)
        self.hide(self._view.deleteConfirmBtn)
    def _delete_entry_confirmed(self, btn):
        if self._delele_last_key is not None:
            self._pcrud.delete(self._delele_last_key)
            self.hide(self._view.deleteConfirmBtn)
        self._delele_last_key = None
        self._view.selectBtn.click()
    def _add_new(self, btn):
        name = self._view.addKeyWid.value.strip()
        val = self._view.addValueWid.value.strip()
        if self._view.addIsVarWid.value:
            from jupyterDB import jupyterDB
            val = jupyterDB._params[val]
        for v in [name, val]:
            if v == "":
                return
        self._pcrud.add(name,val)
        self._view.addKeyWid.value = ""
        self._view.addValueWid.value = ""
    def hide(self, wid):
        self._hideable.set_widget(wid)
        self._hideable.hide()
    def show(self, wid):
        self._hideable.set_widget(wid)
        self._hideable.show()
    def _show_elements(self, btn):
        if self._view.keysDrpWid.value is None:
            return
        self._pcrud.set_base_location([self._view.keysDrpWid.value], relative = True)
        self._searcher._engine.set_container(self._pcrud.readAll())
        self.hide(self._view.deleteConfirmBtn)
        self.hide(self._view.cout.get_layout())
        self.hide(self._view.addRowWid)
        if self._view.opsDrpWid.value == "read":
            self.show(self._view.cout.get_layout())
            self._searcher._result_handler.set_btn_click_func(self._link_open)
            out = self._searcher.search("")
            self._view.cout.display(out, ipy=True, clear=True)
        elif self._view.opsDrpWid.value == "add":
            self.show(self._view.addRowWid)
        elif self._view.opsDrpWid.value == "delete":
            self.show(self._view.cout.get_layout())
            self._searcher._result_handler.set_btn_click_func(self._delete_entry)
            out = self._searcher.search("")
            self._view.cout.display(out, ipy=True, clear=True)
    def set_pickle_file(self, file):
        self._pcrud = PickleCRUDOps()
        self._pcrud.set_pickle_file(file)
        self._pcrud.set_always_sync(True)
    def _delete_entry(self, btn):
        self.show(self._view.deleteConfirmBtn)
        self._delele_last_key = btn.description
    def _link_open(self, btn):
        from TreeDB import TreeDB
        TreeDB.openWebLink(self._pcrud.read(btn.description))
class IResultRenderer:
    def get_layout(self):
        pass
    def display(self):
        pass
    def set_container(self):
        pass
class ButtonsClickView(IResultRenderer):
    def __init__(self):
        box_layout = widgets.Layout(width='100%', flex_flow='wrap', display='flex')
        self._onclick_func = None
        self._base = widgets.HBox(layout = box_layout)
        self.set_element_maker(self._make_btn)#
    def set_btn_click_func(self, func):
        self._onclick_func = func
    def set_element_maker(self, element_maker):
        self._maker = element_maker
    def set_container(self, container):
        self._container = container
        res = []
        for el in self._container:
            res.append(self._maker(el, self._onclick_func))
        self._base.children = res
    def get_layout(self):
        return self._base
    def display(self):
        display(self.get_layout())
    def _make_btn(self, btnDes, clickFunc=None):
        btn = widgets.Button(description= btnDes, layout= {"width":"auto"})
        if clickFunc is not None:
            btn.on_click(clickFunc)
        return btn
class SearchEngine:
    def __init__(self):
        self.default_display()
    def search(self, key, reg=False, case=False):
        res = self._engine.search(key, case = case, reg = reg)
        self._result_handler.set_container(res)
        if not self._display:
            return self._result_handler.get_layout()
        self._result_handler.display()
    def set_engine(self, engine: ISearch):
        self._engine = engine
    def set_result_maker(self, res_cap: IResultRenderer):
        self._result_handler = res_cap
    def default_display(self, activate=True):
        self._display = activate
class Main:
    def links_crud(file):
        lmv = LinksManagerView()
        lmv._make_layout()
        lmc = LinksManagerController()
        lmc.set_view(lmv)
        lmc.set_pickle_file(file)
        see =SearchEngine()
        see.set_engine(DicSearch([]))
        see.set_result_maker(ButtonsClickView())
        see.default_display(False)
        lmc.set_searcher(see)
        lmc.setup()
        return lmc
