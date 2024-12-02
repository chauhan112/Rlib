from timeline.t2023.searchSystem import Main as SearchWithPagination
from timeline.t2023.advance_searcher import Main as AdvanceSearchEngine
from timeline.t2023.generic_logger.components import SingleButtonController
from SearchSystem import DicSearch
from modules.Explorer.personalizedWidgets import CustomOutput
from ModuleDB import ModuleDB
from modules.SearchSystem.modular import HideableWidget
from IPython.display import display
import ipywidgets as widgets
from PickleCRUDDB import PickleCRUDOps
from ClipboardDB import ClipboardDB
from LibsDB import LibsDB
from SerializationDB import SerializationDB
import os

class DicSearchAndResultSorted:
    def __init__(self):
        ds = DicSearch({})
        ds.set_search_in_type("key")
        self.set_engine(ds)
        self._data = None
    def search(self, word, case=False, reg = False):
        res = self._engine.search(word, case=case, reg = reg)
        sres = sorted(res, key = self._key, reverse=True)
        return sres
    def set_engine(self, engine):
        self._engine = engine
    def set_counter(self, counter: PickleCRUDOps):
        self._counter = counter
    def _key(self, v):
        self._data = self._counter.readAll()
        if v in self._data:
            return self._data[v]
        return 0
    def set_container(self, cont):
        self._engine.set_container({k: cont[k] for k in filter(lambda x: not self._is_archived(x), cont)})
    def set_archiviable_reader(self,reder: PickleCRUDOps):
        self._archive_reader = reder
    def _is_archived(self, v):
        self._data = self._archive_reader.readAll()
        if v in self._data:
            return self._data[v]
        return False
class NewInstructionTable:
    def __init__(self):
        from DataStorageSystem import _Tools
        self._table_name = "instructions"
        self.set_pickle_file(_Tools.advanceDBNameGenerator())
        d1 = DicSearchAndResultSorted()
        d2 = DicSearchAndResultSorted()
        self.set_search_engine(SearchWithPagination.searchWithPagination(d1, self._btn_maker, self._run_content))
        self.set_display_engine(SearchWithPagination.searchWithPagination(d2, self._btn_maker, self._op_runner))
        
        pcrud = self._pickle_creator("temps", ["2023", "rlib.it.counts"])
        self.set_counter(pcrud)
        d1.set_counter(pcrud)
        d2.set_counter(pcrud)
        
        arch = self._pickle_creator("temps", ["2023", "rlib.archiveState"])
        d1.set_archiviable_reader(arch)
        d2.set_archiviable_reader(arch)
        
        self.set_op_runner(self._code_displayer)
        self._current_btn = None
        self._group_view = None
        
    def _pickle_creator(self, name, loc):
        pcrud = PickleCRUDOps()
        pcrud.set_pickle_file(LibsDB.picklePath(name))
        pcrud.set_always_sync(True)
        pcrud.set_base_location(loc)
        return pcrud
    def _op_runner(self, wid):
        self._op(self, wid)
    def set_op_runner(self, opR):
        self._op = opR
    def set_search_engine(self, engine):
        self._sengine = engine
        self._search_cnt = AdvanceSearchEngine.search_with_advance_options(self._sengine)
        self._searchView = self._search_cnt._view
    def set_display_engine(self, engine):
        self._dengine = engine
        self._dengine_cnt = AdvanceSearchEngine.search_with_advance_options(self._dengine)
    def set_pickle_file(self, file):
        self._pkl_file = file
        if not os.path.exists(file):
            SerializationDB.pickleOut({}, file)
        self._pcrud = PickleCRUDOps()
        self._pcrud.set_pickle_file(file)
        self._pcrud.set_always_sync(True)
        if self._table_name not in self._pcrud.readAll():
            self._pcrud.add(self._table_name, {})
        self._pcrud.set_base_location([self._table_name])
    def search(self, word, reg=False, case =False):
        self._pcrud._read_from_file(self._pkl_file)
        self._content = self._pcrud.readAll()
        self._sengine._engine.set_container(self._content)
        res_lay = self._sengine.search(word, reg, case)
        self._searchView.couput.display(res_lay, True, True)
        return self._searchView.layout
    def set_scope(self, param):
        self._scope = param
    def add(self, key, val = None):
        if(val is None):
            val = ClipboardDB.getText()
        self._pcrud.add(key, val, overwrite=True)
    def opsRunner(self):
        self._pcrud._read_from_file(self._pkl_file)
        self._content = self._pcrud.readAll()
        self._dengine._engine.set_container(self._content)
        self._searchView.btnOutput.display(widgets.VBox([widgets.Label(self._current_btn.description), 
                self._dengine_cnt._view.layout]), True, True)
        return self._searchView.layout
    def _btn_maker(self, des, onclick):
        btn = SingleButtonController(description=des, layout= {"width": "auto", "max_width": "150px"})
        btn.set_clicked_func(onclick)
        return btn.layout
    def _code_displayer(self, ctx, wid):
        self._dengine_cnt._view.btnOutput.display(ModuleDB.colorPrint("python", self._content[wid.description]), True)
    def _run_content(self, wid):
        self._current_btn = wid
        self._searchView.btnOutput.clear()
        with self._searchView.btnOutput._out:
            exec(self._content[wid.description], self._scope, locals())
        self._increase_count(wid.description)
        self._scope.update(locals())
    def get_search_ui(self):
        HideableWidget.showIt(self._searchView.searchRow)
        HideableWidget.showIt(self._searchView.layout)
        HideableWidget.showIt(self._searchView.couput.get_layout())
        self._pcrud._read_from_file(self._pkl_file)
        self._content = self._pcrud.readAll()
        self._sengine._engine.set_container(self._content)
        return self._searchView.layout
    def set_counter(self, counter: PickleCRUDOps):
        self._counter_pcrud = counter
    def _increase_count(self, key):
        try:
            val = self._counter_pcrud.read(key)
        except:
            val = 0
        val += 1
        self._counter_pcrud.add(key, val, True)
    def get_group_view(self, file = None):
        self._content = self._pcrud.readAll()
        HideableWidget.hideIt(self._searchView.searchRow)
        HideableWidget.hideIt(self._searchView.couput.get_layout())
        cgr = {}
        if file is not None:
            cgr = SerializationDB.readPickle(file)
        if hasattr(self, "_groupController"):
            self._groupController._cnt._basic._model.set_dictionary(cgr)
        if self._group_view is not None:
            self._groupController._cnt._basic._model.set_dictionary(cgr)
            self._groupController._update_keys()
            return self._group_view
        
        from timeline.t2023.groupMaker import GrouperController
        gc = GrouperController()
        gc.set_group_dic(cgr)
        gc.set_up()
        gc.set_additional_sorter(lambda res: sorted(res, key = self._dengine._engine._key, reverse=True))
        gc._update_keys()
        def cclc(btn):
            HideableWidget.hideIt(self._searchView.searchRow)
            HideableWidget.showIt(self._searchView.layout)
            HideableWidget.hideIt(self._searchView.couput.get_layout())
            self._run_content(btn)
        def not_leaf(btn):
            HideableWidget.hideIt(self._searchView.searchRow)
            HideableWidget.hideIt(self._searchView.couput.get_layout())
            HideableWidget.hideIt(self._searchView.layout)
        def goback(btn, *param):
            HideableWidget.hideIt(self._searchView.searchRow)
            HideableWidget.hideIt(self._searchView.couput.get_layout())
            HideableWidget.hideIt(self._searchView.layout)
            gc._cnt._goback_default(btn, *param)
        gc.set_not_leaf_fun(not_leaf)
        gc.set_leaf_click_func(cclc)
        gc._cnt.set_goback_func(goback)
        HideableWidget.hideIt(gc._cnt._basic._view.fileOpsRow)
        HideableWidget.hideIt(gc._cnt._basic._view.locationView.lastKeyWidg)
        gc._cnt._basic._view.locationView.locationWidg.disabled = False
        gc._cnt._basic._view.locationView.locationWidg.placeholder = "filter and search command"
        gc._cnt._basic._view.locationView.labelWidg.value ="filter:"
        gc._cnt._basic._view.locationView.locationWidg.continuous_update = False
        def changed(wdi):
            val = gc._cnt._basic._view.locationView.locationWidg.value.strip()
            if val == "":
                HideableWidget.hideIt(self._searchView.layout)
                HideableWidget.hideIt(self._searchView.couput.get_layout())
                return
            HideableWidget.showIt(self._searchView.layout)
            HideableWidget.showIt(self._searchView.couput.get_layout())
            self.search(val)
        def goback(btn, *oaram):
            sizeBefore = len(gc._cnt._basic._model._loc)
            gc._cnt._basic._model.goback()
            gc._cnt._basic._view.locationView.locationWidg.value = ""
            if len(gc._cnt._basic._model._loc) != sizeBefore:
                gc._cnt._update_keys()
            gc._cnt._basic._view.outputSection.clear()
        gc._cnt.set_goback_func(goback)
        gc._cnt._basic._view.locationView.locationWidg.observe(changed, names=["value"])
        self._groupController = gc
        self._group_view = widgets.VBox([gc._view.layout, self._searchView.layout])
        return self._group_view