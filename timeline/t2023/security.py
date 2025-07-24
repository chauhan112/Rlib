from useful.SerializationDB import SerializationDB
from useful.PickleCRUDDB import PickleCRUDOps
from useful.ListDB import ListDB
from useful.LibsDB import LibsDB
import ipywidgets as widgets
from timeline.t2023.generic_logger.components import SingleButtonController

class SecuritySystem:
    def __init__(self):
        self._LogLvlLabel = "loggers_level"
        self._curLvlLabel = "current_level"
    def set_logger_file(self, file):
        self._logger_file = file
        self._loggers = list(SerializationDB.readPickle(self._logger_file).keys())
    def set_security_file(self, file):
        self._security_file = file
        mod = PickleCRUDOps()
        mod.set_pickle_file(self._security_file)
        mod.set_always_sync(True)
        self.set_security_model(mod)
    def sync(self):
        try:
            self._model.read(self._LogLvlLabel)
        except Exception as e:
            self._model.add(self._LogLvlLabel, {}, True)
            self._model.add(self._curLvlLabel, 5, True)
        content = self._model.read(self._LogLvlLabel)
        for ln in self._loggers:
            if ln not in content:
                content[ln] = 5
        self._model.add(self._LogLvlLabel, content, True)
    def set_security_model(self, model):
        self._model = model
    def update(self, logger_name, value):
        content = self._model.read(self._LogLvlLabel)
        content[logger_name] = value
        self._model.add(self._LogLvlLabel, content, True)
    def read(self, log):
        content = self._model.read(self._LogLvlLabel)
        return content[log]
    def read_current_level(self):
        return self._model.read(self._curLvlLabel)
    def get_loggers_above(self, val=None):
        if val is None:
            val = self.read_current_level()
        content = self._model.read(self._LogLvlLabel)
        rs = []
        for l in content:
            if content[l] >= val:
                rs.append(l)
        return rs
class NewPickleModelWithSecurity:
    def __init__(self):
        self._model = PickleCRUDOps()
        self._key = "log-dumper"
        self._make_default_log()
        self.set_log_size(20)
    def set_log_size(self, size):
        self._log_size = size
    def _make_default_log(self):
        pco = PickleCRUDOps()
        pco.set_always_sync(True)
        pco.set_pickle_file(LibsDB.picklePath("temps"))
        pco.set_base_location(["2023"])
        self.set_history_model(pco)
    def delete(self, key: str):
        self._model.delete(key)
    def read(self, key: str):
        return self._model.read(key)
    def readAll(self):
        content = self._model.readAll()
        fl = self._auth.get_loggers_above()
        newContent = {l: content[l] for l in fl if l in content}
        return newContent
    def set_root(self, root_loc: list):
        self._model.set_root(root_loc)
    def set_base_location(self, base_loc: list, relative=False):
        self._model.set_base_location(base_loc, relative)
    def set_always_sync(self, sync: bool):
        self._model.set_always_sync(sync)
    def set_pickle_file(self, file:str):
        self._model.set_pickle_file(file)
    def set_security(self, sec):
        self._auth= sec
    def add(self, key:str, value, overwrite=False):
        self._model.add(key, value, overwrite)
        self._add_to_history(key, value, "add", overwrite)
    def _add_to_history(self, key, value, ops, overwrite):
        val = self._history_model.read(self._key)
        val.append((self._model._basepath,ops, key, value, overwrite))
        if len(val) > 20:
            val.pop(0)
        self._history_model.add(self._key, val, True)
    def delete(self, key: str):
        val = self._model.read(key)
        self._model.delete(key)
        self._add_to_history(key, val, "delete")
    def set_add_history_file(self, filepath):
        pco = PickleCRUDOps()
        pco.set_always_sync(True)
        pco.set_pickle_file(filepath)#
        pco.add(self._key, [])
        self.set_history_model(pco)
    def set_history_model(self, model):
        self._history_model = model
class Main:
    def model_with_security(filename, security_file=None):
        npms = NewPickleModelWithSecurity()
        npms.set_pickle_file(filename)
        ss = Main._securti(filename, security_file)
        npms.set_security(ss)
        npms.set_always_sync(True)
        return npms
    def _securti(filename, security_file=None):
        ss = SecuritySystem()
        ss.set_logger_file(filename)
        if not security_file:
            pco = PickleCRUDOps()
            pco.set_pickle_file(LibsDB.picklePath("temps"))
            pco.set_base_location(["2023","loggerState"])
            pco.set_always_sync(True)
            ss.set_security_model(pco)
        else:
            ss.set_security_file(security_file)
        ss.sync()
        return ss
    def security_setting_ui(filename, security_file=None):
        ss = Main._securti(filename, security_file)
        levelsWidg = widgets.Dropdown(description="levels",options=[1,2,3,4,5], layout={"width":"auto"})
        loggersWid = widgets.Dropdown(description="loggers",options=ss._loggers, layout={"width":"auto"})
        currentLevelWid = widgets.Dropdown(description="current level",options=[1,2,3,4,5], layout={"width":"300px"})
        setBtn = SingleButtonController(description="set", layout ={"width":"auto"})
        showAllBtn = SingleButtonController(description="show All", layout ={"width":"auto"})
        crtBtnSet = SingleButtonController(description="set", layout ={"width":"auto"})
        out = widgets.Output()

        def set_log_level(wid, *param):
            out.clear_output()
            ss.update(loggersWid.value, levelsWidg.value)
        def log_selected(wid):
            cnt = ss._model.read(ss._LogLvlLabel)
            levelsWidg.value = cnt[loggersWid.value]
        def showAllBtnClicked(wid, *param):
            cnt = ss._model.readAll()
            out.clear_output()
            with out:
                print(cnt)
        def set_current_level(wid, *param):
            ss._model.add(ss._curLvlLabel, currentLevelWid.value, True)
            
        showAllBtn.set_clicked_func(showAllBtnClicked)
        loggersWid.observe(log_selected)
        setBtn.set_clicked_func(set_log_level)
        crtBtnSet.set_clicked_func(set_current_level)
        currentLevelWid.value = ss._model.read(ss._curLvlLabel)
        return widgets.VBox([widgets.HBox([loggersWid, levelsWidg, setBtn.layout,showAllBtn.layout]), 
            widgets.HBox([currentLevelWid, crtBtnSet.layout]), out])