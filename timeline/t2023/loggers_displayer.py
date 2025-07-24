from timeline.t2023.generic_logger import IModifier
import datetime
from modules.SearchSystem.modular import HideableWidget

class AssignedOps:
    def __init__(self):
        self._make_view()
        self.ASSIGNED = "assigned"
    def _make_view(self):
        import ipywidgets as widgets
        from useful.basic import NameSpace 
        from timeline.t2023.generic_logger.components import SingleButtonController 
        self._view = NameSpace()
        self._view.people = widgets.Dropdown(layout = {"width": "auto"})
        self._view.ops = widgets.TagsInput(allow_duplicates=False )
        self._view.ok_btn = SingleButtonController(description="ok", layout = {"width": "auto"})
        self._view.layout = widgets.HBox([self._view.people, self._view.ops, self._view.ok_btn.layout])
    def set_up(self):
        from jupyterDB import jupyterDB
        self._view.people.options = jupyterDB.pickle().read("temps")["2023"]["coders"]
        self._bsc._bc.views.ev.opsSec.opsDrop.options = list(self._bsc._bc.views.ev.opsSec.opsDrop.options) + [self.ASSIGNED]
        self._view.people.value = "me"
        x = set(self._bsc._bc.views.ev.opsSec.opsDrop.options)
        x.remove(self.ASSIGNED)
        self._view.ops.allowed_tags= list(x)
        self._view.ops.value = ['Open']
        self._bsc.set_ops(self.ASSIGNED, self._on_assigned_clicked)
        self._bsc.set_always_run_after(self._runAdfter)
        self._view.ok_btn.set_clicked_func(self._clicked)
    def _on_assigned_clicked(self, ctx):
        ctx._lr._bc.views.ev.opsSec.out1.display(self._view.layout, clear=True)
    def set_basic_controller(self, cnt):
        self._bsc = cnt
    def _clicked(self, btn):
        ops = self._view.ops.value
        for op in ops:
            if op in self._bsc._ops_mapper:
                self._bsc._use_last_result = True
                self._bsc._ops_mapper[op](self._bsc)
        opts = self._bsc._lr._bc.views.ev.fileFoldersListWid.options
        if self._view.people.value != "any":
            opts = list(filter(self._filter_by_assigned, opts))
        self._bsc._lr._bc.views.ev.fileFoldersListWid.options = opts
        self._bsc._default_always_run_after_func(self._bsc)
    def _filter_by_assigned(self, x):
        ppl = self._view.people.value
        
        vals = self._bsc._lr._bc._model._data[x[1]]
        if self.ASSIGNED in vals["more info"]:
            return vals["more info"][self.ASSIGNED].lower() == ppl
        else:
            if ppl == "me":
                return True
        return False
    def _runAdfter(self, ctx):
        ctx._default_always_run_after_func(ctx)
        opla = ctx._bc.views.ev.opsSec.opsDrop.value 
        if opla != self.ASSIGNED:
            ctx._lr._bc.views.ev.opsSec.out1.clear()
        if opla != OpsEnumString.CLOSEIT:
            ctx._lr._bc.views.ev.opsSec.out2.clear()
class OpsEnumString:
    ALL = "All"
    OPEN = "Open"
    DONE = "Done"
    FILTER = "Filter"
    OPENIT = "OpenIt"
    CLOSEIT = "CloseIt"

class DefaultOpsFunc:
    def __init__(self):
        self.set_name_getter(self._default_name_getter)
        self.set_status_getter(self._default_status_getter)
        self.set_status_adder(self._default_status_adder)
        self.set_extra_info_reader(self._default_info_getter)
        self.set_extra_info_value(self._default_info_setter)
    def get_list(self, cnt, use_last=False):
        if cnt._use_last_result and use_last:
            return cnt._lr._bc.views.ev.fileFoldersListWid.options
        opts = cnt._lr._bc._model.dirList()[1]
        return opts
    def all_func(self, cnt):
        opts = self.get_list(cnt)
        cnt._lr._bc.views.ev.fileFoldersListWid.options = opts
    def open_func(self, cnt):
        opts = self.get_list(cnt)
        fopts = list(filter(lambda x: self._sgetter(cnt._lr._bc._model._data[x[1]]) != "done", opts))
        cnt._lr._bc.views.ev.fileFoldersListWid.options = fopts
    def close_func(self, cnt):
        opts = self.get_list(cnt)
        fopts = list(filter(lambda x: self._sgetter(cnt._lr._bc._model._data[x[1]]) == "done", opts))
        cnt._lr._bc.views.ev.fileFoldersListWid.options = fopts
    def filter_func(self, cnt):
        opts = self.get_list(cnt, True)
        fwith = cnt._lr._bc.views.ev.headerWid.currentPath.value
        if fwith:
            fopts = list(filter(lambda x: fwith in self._ngetter(cnt._lr._bc._model._data[x[1]]), opts))
            cnt._lr._bc.views.ev.fileFoldersListWid.options = fopts
    def openIt_func(self, cnt):
        ldcc = cnt._lr._basic_cont.controllers.ldcc
        indexNr = cnt._lr._bc.views.ev.fileFoldersListWid.value
        cotnent = cnt._lr._basic_cont._model.read(ldcc._cur_btn.description)
        taskContent = cotnent["data"][indexNr]
        stat = self._sgetter(taskContent)
        if stat != "open":
            self._ssetter(taskContent, "open")
            cnt._lr._basic_cont._model.add(ldcc._cur_btn.description, cotnent, True)
            cnt._lr._bc._model.update_data()
            cnt._remove_from_opts(indexNr)
    def closeIt_func(self, cnt):
        ldcc = cnt._lr._basic_cont.controllers.ldcc
        indexNr = cnt._lr._bc.views.ev.fileFoldersListWid.value
        cotnent = cnt._lr._basic_cont._model.read(ldcc._cur_btn.description)
        taskContent = cotnent["data"][indexNr]
        stat = self._sgetter(taskContent)
        if stat != "done":
            self._ssetter(taskContent, "done")
            self._ei_setter(taskContent, "completed-time", datetime.datetime.now())
            cnt._lr._basic_cont._model.add(ldcc._cur_btn.description, cotnent, True)
            cnt._lr._bc._model.update_data()
            cnt._remove_from_opts(indexNr)
    def set_name_getter(self, func):
        self._ngetter = func
    def set_status_getter(self, func):
        self._sgetter = func
    def set_status_adder(self, func):
        self._ssetter = func
    def set_extra_info_reader(self, func):
        self._ei_getter = func
    def set_extra_info_value(self, func):
        self._ei_setter = func
    def _default_status_getter(self, data):
        if "status" in data:
            return data["status"]
        return None
    def _default_status_adder(self, data, value):
        data["status"] = value
    def _default_info_getter(self, data):
        return data["more info"]
    def _default_info_setter(self, data, key, value):
        data["more info"][key] = value
    def _default_name_getter(self, data):
        return data["name"]
    
class TasksDisplayer(IModifier):
    def __init__(self):
        from timeline.t2023.generic_logger.tools import LogReader
        self._lr = LogReader()
        self._use_last_result = False
        self._bc = self._lr._bc
        self._cur_version = None
        self._ops_mapper = {}
        self.set_default_funcs(DefaultOpsFunc())
        self.set_always_run_after(self._default_always_run_after_func)
        self.set_setUp_func(self._default_set_up)
        
        from timeline.t2023.tools import Confirmer
        self._conf = Confirmer()
        
    def set_default_funcs(self, dfops):
        self._df_ops = dfops
        self.set_ops(OpsEnumString.ALL, self._df_ops.all_func)
        self.set_ops(OpsEnumString.OPEN, self._df_ops.open_func)
        self.set_ops(OpsEnumString.DONE, self._df_ops.close_func)
        self.set_ops(OpsEnumString.FILTER, self._df_ops.filter_func)
        self.set_ops(OpsEnumString.OPENIT, self._df_ops.openIt_func)
        self.set_ops(OpsEnumString.CLOSEIT, self._df_ops.closeIt_func)
    def _show_all(self):
        opts = self._lr._bc._model.dirList()[1]
        self._lr._bc.views.ev.fileFoldersListWid.options = opts
    def _remove_from_opts(self, key):
        ops = self._lr._bc.views.ev.fileFoldersListWid.options
        ne =[]
        for v, k in ops:
            if k != key:
                ne.append((v, k))
        self._lr._bc.views.ev.fileFoldersListWid.options = ne
    def _clciked(self, wid):
        val = self._lr._bc.views.ev.opsSec.opsDrop.value
        if val in self._ops_mapper:
            self._use_last_result = False
            if val == OpsEnumString.CLOSEIT:
                self._conf.set_callback_function(self._ops_mapper[val])
                self._conf.set_params(self)
                self._lr._bc.views.ev.opsSec.out2.display(self._conf.get_layout(), True, True)
            else:
                self._ops_mapper[val](self)
        else:
            print("ops is not defined")
        self._always_run_after_ops(self)
    def set_always_run_after(self, func):
        self._always_run_after_ops = func
    def _default_always_run_after_func(self, ctx):
        ttl = self._lr._bc.views.ev.headerWid.title.value
        self._lr._bc.views.ev.headerWid.title.value = ttl.split("//-")[0]+ "//-" + str(len(self._lr._bc.views.ev.fileFoldersListWid.options))
    def get_layout(self):
        return self._lr.get_layout()
    def _default_set_up(self):
        self._lr.set_up()
        self._lr._bsc.controllers.exp.views.ev.left_side.children = list(self._lr._bsc.controllers.exp.views.ev.left_side.children) + [self._lr._bsc.controllers.exp.views.ev.opsRow]
        self._lr._bc.views.ev.headerWid.currentPath.disabled = False
        self._lr._bc.views.ev.headerWid.currentPath.placeholder = "filter by name"
        HideableWidget.hideIt(self._lr._bc.views.ev.opsSec.opsDropSec)
        self._lr._bc.views.ev.opsSec.opsDrop.options = list(map(lambda x: OpsEnumString.__dict__[x], 
                                                             filter(lambda x: x[0] != "_", OpsEnumString.__dict__)))
        self._lr._bc.views.ev.opsSec.opsDrop.value = "All"
        self._lr._bc.views.ev.opsSec.okBtn.set_clicked_func(self._clciked)
    def set_basic_controller(self, bsc):
        self._lr.set_basic_controller(bsc)
    def update_data(self, versionNr):
        if self._cur_version != versionNr:
            self._lr._bc._model.update_data()
            self._cur_version = versionNr
    def set_ops(self, key, func):
        self._ops_mapper[key] = func
    def set_up(self):
        self._bc.views.ev.headerWid.title.value = self._lr._basic_cont.controllers.ldcc._cur_btn.description
        self._set_up_func()
    def set_setUp_func(self, func):
        self._set_up_func = func