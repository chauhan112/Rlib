import ipywidgets as widgets
from timeline.t2023.generic_logger.components import SingleButtonController
from basic import BasicController, NameSpace
import datetime
class SubTasksView:
    def __init__(self):
        self.task_info = widgets.Text(placeholder = "tasks name/ description", layout={"width":"200px"})
        self.deleteBtn = SingleButtonController(icon="trash", layout={"width":"auto"}, button_style="danger")
        self.done_btn = SingleButtonController(description="done", layout={"width":"auto", "background_color": "red"})
        self.add_btn = SingleButtonController(description="+", layout={"width":"auto"})
        self.confirm_btn = SingleButtonController(description="confirm", layout={"width":"auto"})
        self.done_btn.layout.style.button_color = "#adebff"
        self.parentID=widgets.IntText(layout={"width":"60px"})
        self.tasksID = widgets.IntText(layout={"width":"60px"})
        self.displayer = widgets.Textarea(layout={"width":"auto"})
        self.opsRow = widgets.HBox([self.parentID, self.tasksID, self.task_info, self.add_btn.layout, 
                                    self.done_btn.layout,self.deleteBtn.layout,self.confirm_btn.layout])
        self.layout = widgets.VBox([self.opsRow, self.displayer])
class SubtaskModel:
    def __init__(self):
        self.set_dic({})
    def set_dic(self, dic):
        #{data: {}, relation: {parentId: {childId, ..}}, currentId: 0}
        self._data = dic
        if "relation" not in self._data:
            self._data["relation"] = {}
        if "currentId" not in self._data:
            self._data["currentId"]= 0
        if "data" not in self._data:
            self._data["data"] ={}
    def add(self, value, parentId = None, currentId = None):
        if currentId is None:
            currentId = self._data["currentId"]
            self._data["currentId"] += 1
        else:
            self.delete(currentId)
        if self.doesIDexists(currentId):
            currentId = self.get_maxId() +1 
        self._data["data"][currentId] = {"description": value, "status": "open", "creation-date": datetime.datetime.now()}
        if parentId not in self._data["relation"]:
            self._data["relation"][parentId] = set()
        self._data["relation"][parentId].add(currentId)
            
    def delete(self, taskId):
        if taskId in self._data["data"]:
            del self._data["data"][taskId]
        rel = self._data["relation"]
        for p in rel:
            if taskId in rel[p]:
                rel[p].remove(taskId)
    def doesIDexists(self, taskId):
        return taskId in self._data["data"]
    def get_maxId(self):
        return max(self._data["data"])
    def read(self, taskID):
        return self._data["data"][taskID]
class SubtaskController:
    def set_up(self, ):
        self._bsc.views.stv.displayer.disabled = True
        self._bsc.views.stv.parentID.value = -1
        self._bsc.views.stv.tasksID.value = -1
        self._bsc.views.stv.add_btn.set_clicked_func(self._def_add_clicked)
        self._bsc.views.stv.deleteBtn.set_clicked_func(self._def_delete_btn_clicked)
        self._bsc.views.stv.done_btn.set_clicked_func(self._def_done_btn_clicked)
        self._bsc.views.stv.tasksID.observe(self._task_id_changed, ["value"])
    def set_basic(self, bsc):
        self._bsc = bsc
    def _def_add_clicked(self, btn):
        valu = self._bsc.views.stv.task_info.value.strip()
        keyFunc = lambda x: None if x < 0 else x
        if valu:
            self._bsc._model.add(valu, keyFunc(self._bsc.views.stv.parentID.value), keyFunc(self._bsc.views.stv.tasksID.value))
        self._bsc.views.stv.displayer.value = self._bsc.controllers.td.get_txt()
        self._bsc.views.stv.task_info.value = ""
    def _def_delete_btn_clicked(self, btn):
        if self._bsc.views.stv.tasksID.value >= 0:
            self._bsc._model.delete(self._bsc.views.stv.tasksID.value)
        self._bsc.views.stv.displayer.value = self._bsc.controllers.td.get_txt()
    def _def_confirm_btn_clicked(self, btn):
        pass
    def _def_done_btn_clicked(self, btn):
        idd = self._bsc.views.stv.tasksID.value
        if self._bsc._model.doesIDexists(idd):
            val =self._bsc._model.read(idd)
            val["status"] = "close"
        self._bsc.views.stv.displayer.value = self._bsc.controllers.td.get_txt()
    def _task_id_changed(self, ui):
        self._bsc.views.stv.task_info.value = ""
        if self._bsc._model.doesIDexists(self._bsc.views.stv.tasksID.value):
            self._bsc.views.stv.task_info.value = self._bsc._model.read(self._bsc.views.stv.tasksID.value)["description"]
class TaskDisplayer:
    def __init__(self):
        self.set_get_txt_func(self._def_get_text)
    def set_get_txt_func(self, func):
        self._get_txt_func = func
    def set_basic(self, bsc):
        self._bsc = bsc
    def chlGetter(self,dirpath):
        if dirpath == "root":
            if None in self._bsc._model._data["relation"]:
                return list(self._bsc._model._data["relation"][None])
            return []
        return list(self._bsc._model._data["relation"][dirpath])
    def nameGetter(self, i, p):
        return str(p) + " " + self._bsc._model._data['data'][p]["description"] +" - " + self._bsc._model._data['data'][p]["status"] 
    def dirChecker(self, path):
        return path in self._bsc._model._data["relation"]
    def set_up(self):
        from timeline.t2023.treeOps import DynamicTreeRenderer
        dtr = DynamicTreeRenderer()
        dtr.set_dic({})
        dtr.set_children_getter(self.chlGetter)
        dtr.set_name_getter(self.nameGetter)
        dtr.set_dir_checker(self.dirChecker)
        dtr.set_depth_level(10)
        self._tree = dtr
    def get_txt(self):
        return self._get_txt_func(self)
    def _def_get_text(self, *param):
        return self._tree.getAsText()
class Main:
    def subtasks():
        bsc = BasicController()
        stv = SubTasksView()
        bsc.views.stv = stv
        stc = SubtaskController()
        stc.set_basic(bsc)
        bsc.controllers.stc = stc
        bsc.set_model(SubtaskModel())
        stc.set_up()
        
        td = TaskDisplayer()
        td.set_basic(bsc)
        td.set_up()
        bsc.controllers.td = td
        return bsc