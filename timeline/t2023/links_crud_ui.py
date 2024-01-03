from modules.SearchSystem.modular import HideableWidget
from modules.Explorer.personalizedWidgets import CustomOutput
import ipywidgets as widgets
from PickleCRUDDB import PickleCRUDOps
from SearchSystem import ISearch, DicSearch
from modules.GUIs.model import KeyManager
class LinksManagerView:
    def __init__(self):
        self._layout =None
    def _make_layout(self):
        self.keysDrpWid = widgets.Dropdown(layout = {"width":"auto" })
        self.opsDrpWid = widgets.Dropdown(options =["search", "delete", "add"],layout = {"width":"auto" })
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
    def __init__(self):
        self.set_add_btn_func(self._add_new)
    def set_add_btn_func(self, func):
        self._ok_func = func
    def _search_func(self, btn, *params):
        self._pcrud.set_base_location([self._view.keysDrpWid.value], relative = True)
        self._searcher._engine.set_container(self._pcrud.readAll())
        reg = self._view.addIsVarWid.value
        val = self._view.addValueWid.value.strip()
        out = self._searcher.search(val, reg =reg)
        self._view.cout.display(out, ipy=True, clear=True)
    def set_searcher(self, searcher):
        self._searcher = searcher
    def set_view(self, view):
        self._view = view
    def setup(self):
        self._view.selectBtn.on_click(self._show_elements)
        self._view.keysDrpWid.options = list(self._pcrud.readAll().keys())
        self._view.addAddBtn.on_click(self._btn_clicked)
        self._view.deleteConfirmBtn.on_click(self._delete_entry_confirmed)
        HideableWidget.hideIt(self._view.deleteConfirmBtn)
    def _delete_entry_confirmed(self, btn):
        if self._delele_last_key is not None:
            self._pcrud.delete(self._delele_last_key)
            HideableWidget.hideIt(self._view.deleteConfirmBtn)
        self._delele_last_key = None
        self._view.selectBtn.click()
    def _btn_clicked(self, btn):
        self._ok_func(btn)
    def _add_new(self, btn,*params):
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
    def _show_elements(self, btn):
        if self._view.keysDrpWid.value is None:
            return
        self._pcrud.set_base_location([self._view.keysDrpWid.value], relative = True)
        self._searcher._engine.set_container(self._pcrud.readAll())
        HideableWidget.hideIt(self._view.deleteConfirmBtn)
        HideableWidget.hideIt(self._view.cout.get_layout())
        HideableWidget.showIt(self._view.addRowWid)
        if self._view.opsDrpWid.value == "search":
            HideableWidget.showIt(self._view.cout.get_layout())
            self._view.cout.clear()
            self._searcher._result_handler.set_btn_click_func(self._link_open)
            self._view.addIsVarWid.description = "reg"
            self._view.addValueWid.placeholder = "search word"
            self._view.addAddBtn.description = "search"
            self.set_add_btn_func(self._search_func)
            HideableWidget.hideIt(self._view.addKeyWid)
        elif self._view.opsDrpWid.value == "add":
            self._view.addIsVarWid.description = "is var"
            self._view.addValueWid.placeholder = "value"
            self._view.addValueWid.value = ""
            self._view.addAddBtn.description = "add"
            self.set_add_btn_func(self._add_new)
            HideableWidget.showIt(self._view.addKeyWid)
        elif self._view.opsDrpWid.value == "delete":
            HideableWidget.showIt(self._view.cout.get_layout())
            self._searcher._result_handler.set_btn_click_func(self._delete_entry)
            out = self._searcher.search("")
            self._view.cout.display(out, ipy=True, clear=True)
    def set_pickle_file(self, file):
        self._pcrud = PickleCRUDOps()
        self._pcrud.set_pickle_file(file)
        self._pcrud.set_always_sync(True)
    def _delete_entry(self, btn):
        HideableWidget.showIt(self._view.deleteConfirmBtn)
        self._delele_last_key = btn.description
    def _link_open(self, btn):
        from TreeDB import TreeDB
        urlAdd = self._pcrud.read(btn.description)
        TreeDB.openWebLink(urlAdd)
        self._view.cout.clear()
        with self._view.cout._out:
            print(urlAdd) 
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
        self._key = key
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
class PagerView:
    def __init__(self):
        from modules.SearchSystem.modular import PageSelectioOpsWidget
        self.pagination = PageSelectioOpsWidget()
        box_layout = widgets.Layout(width='100%', flex_flow='wrap', display='flex')
        self.display_area = widgets.HBox(layout = box_layout)
        self.layout = widgets.VBox([self.pagination.get(),self.display_area])
    def get(self):
        return self.layout
class ButtonViewWithPagination(IResultRenderer):
    def __init__(self):
        self._onclick_func = None
        self.set_element_maker(self._make_btn)
        self._pv = PagerView()
        self._key_manager = KeyManager()
        self._key_manager.set_limit_per_page(30)
        self._memoization = {}
        
        for ch in self._pv.pagination._bn.children:
            ch.on_click(self._pagination_selected)
        self._pv.pagination._gotoPage.on_click(self._goto)
    def _goto(self, btn):
        pageNr = self._pv.pagination._pageTxt.value
        self._key_manager.setCurrentPageIndex(pageNr)
        self._update_pagination_btns()
        self._update_content()
    def _pagination_selected(self, btn):
        self._key_manager.setCurrentPageIndex(int(btn.description))
        self._update_pagination_btns()
        self._update_content()
    def _update_content(self):
        vals = self._key_manager.getKeysForCurrentPageIndex()
        index = self._key_manager.currentPageIndex
        if index not in self._memoization:
            self._memoization[index] = [self._maker(v, self._clicked) for v in vals]
        self._pv.display_area.children = self._memoization[index]
    def set_container(self, res):
        self._memoization.clear()
        self._res  = res
        self._key_manager.set_keys(res)
        for ch in self._pv.pagination._bn.children:
            HideableWidget.showIt(ch)
        if len(res) <= self._key_manager.nrPerPage:
            HideableWidget.hideIt(self._pv.pagination.get())
        else:
            HideableWidget.showIt(self._pv.pagination.get())
            nr = self._key_manager.totalNrOfPages()
            for i in range(nr, 5):
                HideableWidget.hideIt(self._pv.pagination._bn.children[i])
            self._pv.pagination._pageMax.value = str(nr)
            self._pv.pagination._pageTxt.min = 1
            self._pv.pagination._pageTxt.max = nr
            self._update_pagination_btns()
        self._update_content()
    def _update_pagination_btns(self):
        bts = self._key_manager.getButtonIndices()
        for i, vl in enumerate(bts):
            self._pv.pagination._bn.children[i].description = str(vl)
        if bts[0] != 1:
            HideableWidget.showIt(self._pv.pagination._pageLeft)
        else:
            HideableWidget.hideIt(self._pv.pagination._pageLeft)
        if bts[-1] != self._key_manager.totalNrOfPages():
            HideableWidget.showIt(self._pv.pagination._pageRight)
        else:
            HideableWidget.hideIt(self._pv.pagination._pageRight)
    def _make_btn(self, btnDes, clickFunc=None):
        btn = widgets.Button(description= btnDes, layout= {"width":"auto"})
        if clickFunc is not None:
            btn.on_click(clickFunc)
        return btn
    def set_element_maker(self, amker):
        self._maker = amker
    def set_btn_click_func(self, func):
        self._onclick_func = func
    def _clicked(self, wid):
        self._onclick_func(wid)
    def get_layout(self):
        return self._pv.get()
class Main:
    def links_crud(file):
        lmv = LinksManagerView()
        lmv._make_layout()
        lmc = LinksManagerController()
        lmc.set_view(lmv)
        lmc.set_pickle_file(file)
        see =SearchEngine()
        see.set_engine(DicSearch([]))
        see.set_result_maker(ButtonViewWithPagination())
        see.default_display(False)
        lmc.set_searcher(see)
        lmc.setup()
        return lmc
