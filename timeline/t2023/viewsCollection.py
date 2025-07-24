from WidgetsDB import WidgetsDB
import ipywidgets as widgets
from modules.Explorer.personalizedWidgets import CustomOutput
from timeline.t2023.links_crud_ui import SearchEngine, ButtonViewWithPagination
from SearchSystem import MultilineStringSearch
from useful.ComparerDB import ComparerDB

class ListContentSearch(MultilineStringSearch):
    def __init__(self, content, allRes = False):
        self.allRes = allRes
        if(type(content) == str):
            content = content.splitlines()
        self.set_container(content)
    def wordSearch(self, word, case = False):
        return self._iterator(lambda val: ComparerDB.inCompare(leftIn=str(word), right=str(val), case=case))
    def pattern(self, patt):
        return self._iterator(lambda val: ComparerDB.regexSearch(regex=patt, word=str(val)))
class ListSearcher:
    def __init__(self):
        self.set_btn_click_func(lambda x,y : x)
    def _btn_maker(self, des, func):
        btn = widgets.Button(description = str(self._see._engine.container[des]), layout= {"width":"auto", "max_width":"300px"}, 
            tooltip= str(self._see._engine.container[des]))
        btn.on_click(func)
        btn._key = des
        return btn
    def set_up(self):
        see = SearchEngine()
        bvvp = ButtonViewWithPagination()
        bvvp._key_manager.set_limit_per_page(20)
        bvvp.set_element_maker(self._btn_maker)
        bvvp.set_btn_click_func(self._btn_click_func)
        see.set_result_maker(bvvp)
        mss = ListContentSearch([], True)
        see.set_engine(mss)
        see.default_display(False)
        self._see = see
    def set_btn_click_func(self, func):
        self._clicked_func = func
    def _btn_click_func(self, btn):
        self._clicked_func(btn, self)
    def set_container(self, con):
        self._see._engine.set_container(con)
class ManualListView: # like tags
    def __init__(self):
        self.opsWid = widgets.Dropdown(options=["add",'update',"delete"], layout =widgets.Layout(width="auto"))
        self.btn = widgets.Button(description="add", layout={"width":"auto"})
        self.textWid = widgets.Text(placeholder = "add word", layout={"width":"auto"})
        self.output = CustomOutput()
        self.confirmBtn = widgets.Button(description="confirm", layout={"width":"auto"})
        self.layout = widgets.VBox([widgets.HBox([self.opsWid, self.textWid, self.btn, self.confirmBtn]), self.output.get_layout()])
class ListAdderController:
    def __init__(self):
        self.set_model([])
        self.set_btn_click_func(self._add_func)
        self.set_ops_manager(self._def_ops_manager)
        self.set_cruded_ops(lambda *x: x)
    def set_cruded_ops(self, func):
        self._cruded_ops = func
        self._has_cruded = False
    def set_view(self, view):
        self._view = view
    def set_up(self):
        WidgetsDB.hide(self._view.confirmBtn)
        self._view.opsWid.observe(self._opsChanged, names="value")
        self._view.btn.on_click(self._btn_clicked)
    def set_ops_manager(self, opsManager):
        self._ops_manager = opsManager
    def _opsChanged(self, wid):
        self._ops_manager(wid,self)
    def _def_ops_manager(self, wid, *param):
        val = self._view.opsWid.value
        self._view.textWid.value = ""
        self._view.output.clear()
        self._has_cruded = False
        if val == "add":
            self._view.btn.description ="add"
            self.set_btn_click_func(self._add_func)
        elif val == "update":
            self._view.btn.description ="search"
            self.set_btn_click_func(self._searched_func)
            self._engine._see._result_handler.set_btn_click_func(self._update_ops)
        elif val == "delete":
            self._view.btn.description ="search"
            self.set_btn_click_func(self._searched_func)
            self._engine._see._result_handler.set_btn_click_func(self._delete_it)
        else:
            pass
    def _btn_clicked(self, btn):
        self._btn_func(btn, self)
        if self._has_cruded:
            self._cruded_ops(btn, self)
    def set_btn_click_func(self, func):
        self._btn_func = func
    def _add_func(self, btn, *param):
        self._has_cruded = False
        val = self._view.textWid.value.strip()
        if val == "":
            return
        self._model.append(val)
        self._view.output.display(str(self._model), True)
        self._view.textWid.value = ""
        self._has_cruded = True
    def _delete_it(self, btn, *param):
        if self._view.btn.description == "confirm" and btn.description == "confirm":
            del self._model[self._last_btn._key]
            self._last_btn = None
            self._opsChanged(btn)
            self._searched_func(btn)
            self._has_cruded = True
            return 
        self._last_btn = btn
        self._view.btn.description ="confirm"
        self.set_btn_click_func(self._delete_it)
    def _searched_func(self, btn, *param):
        self._has_cruded = False
        self._engine.set_container(self._model)
        res = self._engine._see.search(self._view.textWid.value.strip())
        self._view.output.display(res, True, True)
    def set_search_engine(self, engine):
        self._engine = engine
    def _update_ops(self, wid, *param):
        self._view.textWid.value = self._model[wid._key]
        self._view.btn.description ="update"
        self._last_btn = wid
        self.set_btn_click_func(self._update)
    def _update(self, btn, *param):
        self._model[self._last_btn._key] = self._view.textWid.value.strip()
        self._view.textWid.value = ""
        self._last_btn = None
        self._opsChanged(btn)
        self._searched_func(btn)
        self._has_cruded = True
    def set_model(self,model):
        self._model = model
    def reset(self):
        self._model.clear()
        self._view.output.clear()
        self._view.textWid.value = ""
    def update(self):
        self._view.output.display(str(self._model), True)
        self._view.textWid.value = ""
class Main:
    def get_list_maker():
        mlv = ManualListView()
        lac = ListAdderController()
        lac.set_view(mlv)
        lac.set_up()
        ls = ListSearcher()
        ls.set_up()
        lac.set_search_engine(ls)
        return mlv.layout, lac
