import ipywidgets as widgets
from modules.Explorer.personalizedWidgets import CustomOutput
from modules.SearchSystem.modular import HideableWidget
from modules.GUIs.PickleOps import PickleOpsModel
from timeline.t2023.links_crud_ui import ButtonViewWithPagination
from timeline.t2023.viewsCollection import Main as ViewsCollection

class NameSpace:
    pass
class MutuallyExclusiveWidget:
    def __init__(self, widgs = None):
        self.set_index(0)
        if widgs is not None:
            self.set_widgets(widgs)
    def set_widgets(self, widg: list):
        self._widgets = widg
        self._hbox = widgets.HBox(widg)
    def set_index(self, index):
        self._index = index
    def get_layout(self):
        self.update()
        return self._hbox
    def get(self):
        return self._widgets[self._index % len(self._widgets)]
    def update(self):
        for el in self._widgets:
            HideableWidget.hideIt(el)
        HideableWidget.showIt(self.get())
class LoggerViews:
    def __init__(self):
        self.fileView = NameSpace()
        self.locationView = NameSpace()
        self.keysView = NameSpace()
        self.opsView = NameSpace()
        self.opsView.nothing = NameSpace()
        self.opsView.create = NameSpace()
        self.opsView.delete = NameSpace()
        self.opsView.update = NameSpace()

        self.fileView.labelWidg = widgets.Label("File:", layout=widgets.Layout(width ="30px"))
        self.fileView.pathDropWidg = widgets.Dropdown(options=[], layout=widgets.Layout(width ="auto"))
        self.fileView.pathTextWidg = widgets.Text(disabled=True, value="path/to/file", layout= {"width":"auto"})
        self.fileView.pathWidg = MutuallyExclusiveWidget([self.fileView.pathDropWidg, self.fileView.pathTextWidg])
        self.fileView.opsCheckbox = widgets.Checkbox(description="ops",indent=False,layout= widgets.Layout(width="20%"))
        self.fileOpsRow = widgets.HBox([self.fileView.labelWidg, self.fileView.pathWidg.get_layout(), self.fileView.opsCheckbox])

        self.locationView.labelWidg = widgets.Label("Loc:", layout=widgets.Layout(width ="30px"))
        self.locationView.locationWidg = widgets.Text(value="/",disabled= True, layout=widgets.Layout(width="auto",))
        self.locationView.lastKeyWidg = widgets.Text(value="",disabled= True, layout=widgets.Layout(width="10%",))
        self.locationView.gobackWidg = widgets.Button(icon="arrow-circle-left", layout={"width":"auto"})
        self.locRow = widgets.HBox([self.locationView.labelWidg, self.locationView.locationWidg, self.locationView.lastKeyWidg, self.locationView.gobackWidg])

        self.keysView.labelWidg = widgets.Label("keys:", layout=widgets.Layout(width ="30px"))
        self.keysView.displayerWidg = CustomOutput()
        self.keyRow = widgets.HBox([self.keysView.labelWidg, self.keysView.displayerWidg.get_layout()])

        self.opsView.labelWidg = widgets.Label("ops:", layout={"width":"30px"})
        self.opsView.opsWidg = widgets.Dropdown(options=[], layout =widgets.Layout(width="auto"))
        self.opsView.okBtn = widgets.Button(description="ok", layout={'width':"70px"})
        self.opsView.keyWidg = widgets.Text(placeholder="key", layout={"width":"auto"})
        self.opsView.valueWidg = widgets.Text(placeholder="value or variable", layout={"width":"auto"})
        self.opsView.valueTextareaWidg = widgets.Textarea(placeholder="content", layout={"width":"auto"})
        self.opsView.value = MutuallyExclusiveWidget([self.opsView.valueWidg, self.opsView.valueTextareaWidg])
        self.opsView.moreOps = widgets.Dropdown(options=["none","eval","is var","textarea", "empty list", "empty dict"], layout =widgets.Layout(width="auto"))
        self.opsView.overriderChe = widgets.Checkbox(description="overwrite",indent=False, layout={'width':"auto"})
        self.opsRow = widgets.HBox([self.opsView.labelWidg, self.opsView.opsWidg, self.opsView.keyWidg, self.opsView.moreOps,
            self.opsView.value.get_layout(), self.opsView.overriderChe, self.opsView.okBtn], justify_content='space-between')

        self.outputSection = CustomOutput()
        self.layout = widgets.VBox([self.fileOpsRow, self.locRow, self.keyRow, self.opsRow, self.outputSection.get_layout()],
                                   layout=widgets.Layout( display='flex',  flex_flow='column',  border='solid 2px BurlyWood',
                                                         align_items='stretch', min_height="200px", padding="3px")) 
class BasicController:
    def set_model(self, model):
        self._model = model
    def set_view(self, view):
        self._view = view
    def set_scope(self, dic):
        self._scope = dic
    def set_parent(self, parent):
        self._parent = parent
class LoggerController:
    def __init__(self):
        self._status = {}
        self.set_key_views(ButtonViewWithPagination())
        self._key_view._key_manager.set_limit_per_page(20)
        self.set_mode_selector(self._mode_change)
        self.set_key_selected_func(self._key_clicked_default)
        self.set_goback_func(self._goback_default)
        self.set_file_dropdown_observe_func(self._dropdown_file_selected_default)
        self.set_key_updator(self._update_keys_default)
    def set_key_updator(self, upd):
        self._update_keys = upd
    def set_list_manager(self, listOps):
        self._list_operator = listOps
        self._list_operator.set_cruded_ops(self._cruded_ops_in_list)
        self._current_key = None
    def set_ops_controller(self, opsCont):
        self._opsController = opsCont
    def set_file_dropdown_observe_func(self, func):
        self._drp_file_func = func
    def _observed_file_change(self, change):
        self._drp_file_func(change, self)
    def _dropdown_file_selected_default(self, wid, *params):
        self._basic._model.loadFileFromDB(wid['new'])
        self._update_keys()
    def set_goback_func(self, func):
        self._goback_func = func
    def _goback_default(self, btn, *param):
        sizeBefore = len(self._basic._model._loc)
        self._basic._model.goback()
        self._basic._view.locationView.locationWidg.value = "/".join(self._basic._model._loc)
        if len(self._basic._model._loc) != sizeBefore:
            self._update_keys()
        self._basic._view.outputSection.clear()
    def _on_go_back_clicked(self, tn):
        self._goback_func(tn, self)
    def set_key_selected_func(self, func):
        self._key_clicked_func = func
        self._key_view.set_btn_click_func(func)
    def _key_clicked_default(self, btn, *param):
        self._current_key = None
        self._basic._view.outputSection.clear()
        if self._basic._model.isDic():
            self._basic._model.goForward(btn.description)
            self._basic._view.locationView.locationWidg.value = "/".join(self._basic._model._loc)
            self._basic._view.opsView.keyWidg.value = btn.description
        val = self._basic._model.value()
        if self._basic._model.isDic():
            self._update_keys()
        else:
            if type(val) == list:
                self._list_operator.set_model(val)
                self._list_operator.update()
                self._basic._view.outputSection.display(self._list_operator._view.layout, ipy=True, clear=True)
                self._current_key = btn.description
            elif type(val) == str:
                self._basic._view.outputSection.clear()
                with self._basic._view.outputSection._out:
                    print(val)
            else:
                self._basic._view.outputSection.display(val, ipy=False, clear=True)
            self._basic._model.goback()
    def _cruded_ops_in_list(self, btn, cnt):
        if self._current_key is None:
            return
        self._basic._model.add(self._current_key, self._list_operator._model)
    def set_mode_selector(self, func):
        self._mode_func = func
    def set_file(self, file:str):
        self._basic._view.fileView.pathTextWidg.value = file
        self._basic._view.fileView.pathWidg.set_index(1)
        self._basic._view.fileView.pathWidg.update()
        self._basic._model.loadFile(file)
        self._update_keys()
    def _update_keys_default(self):
        self._key_view.set_container(self._basic._model.getKeys())
        self._basic._view.keysView.displayerWidg.display(self._key_view.get_layout(),ipy=True, clear=True)
    def setup(self):
        HideableWidget.hideIt(self._basic._view.opsRow)
        self._basic._view.fileView.opsCheckbox.observe(self._showOpsMode, names="value")
        self._basic._view.locationView.gobackWidg.on_click(self._on_go_back_clicked)
        self._update_keys()
    def _showOpsMode(self, change):
        self._mode_func(change)
    def _mode_change(self, change):
        if change['new']:
            HideableWidget.showIt(self._basic._view.opsRow)
        else:
            HideableWidget.hideIt(self._basic._view.opsRow)
    def _ok_clicked(self, btn):
        self._ok_clicked_func()
    def loadFromPickleFolder(self):
        from jupyterDB import jupyterDB
        self._basic._view.fileView.pathWidg.set_index(0)
        self._basic._view.fileView.pathWidg.update()
        self._basic._view.fileView.pathDropWidg.options = jupyterDB.pickle().listDir()
        self._basic._view.fileView.pathDropWidg.observe(self._observed_file_change, names="value")
    def set_key_views(self, keyView):
        self._key_view = keyView
    def set_basic_controller(self, cont):
        self._basic = cont
class OpsController:
    def __init__(self):
        self.set_ops_func(self._default_ops_func)
        self.set_add_func(self._default_add_func)
        self.set_delete_func(self._default_delete_func)
        self.set_ok_func(self._default_ok_func)
    def set_add_func(self, func):
        self._add_func = func
    def set_delete_func(self, func):
        self._delete_func = func
    def _default_ok_func(self, btn, *param):
        print("ok btn clicked. It does not do anything")
    def _default_add_func(self, btn, *param):
        key = self._basic._view.opsView.keyWidg.value.strip()
        value = self._basic._view.opsView.valueWidg.value.strip()
        
        mo = self._basic._view.opsView.moreOps.value
        if mo == "textarea":
            value = self._basic._view.opsView.valueTextareaWidg.value.strip()
        elif mo == "empty list":
            value = []
        elif mo == "empty dict":
            value = {}
        elif mo == "is var":
            value = self._basic._scope[value]
        elif mo == "eval":
            value = eval(self._basic._view.opsView.valueTextareaWidg.value.strip())
            
        override = self._basic._view.opsView.overriderChe.value
        added = False
        if key != "":
            if not self._basic._model.alreadyExists(key) or override:
                added = True
                self._basic._model.add(key, value)
                self._basic._parent._update_keys()
        if not added:
            print("key could not not be added")
    
    def _default_delete_func(self, btn, *param):
        key = self._basic._view.opsView.keyWidg.value.strip()
        if self._basic._model.alreadyExists(key):
            self._basic._model.delete(key)
            self._basic._parent._update_keys()
        else:
            print("key does not exist")
    def set_ok_func(self, ok_func):
        self._ok_func = ok_func
    def set_ops_func(self, func):
        self._ops_func = func
    def _default_ops_func(self, wid, *param):
        self._basic._view.outputSection.clear()
        opsName = wid["new"]
        HideableWidget.hideIt(self._basic._view.opsView.keyWidg)
        HideableWidget.hideIt(self._basic._view.opsView.valueWidg)
        HideableWidget.hideIt(self._basic._view.opsView.overriderChe)
        HideableWidget.hideIt(self._basic._view.opsView.okBtn)
        HideableWidget.hideIt(self._basic._view.opsView.value.get_layout())
        HideableWidget.hideIt(self._basic._view.opsView.moreOps)
        if opsName == "..":
            pass
        elif opsName == "add":
            HideableWidget.showIt(self._basic._view.opsView.keyWidg)
            HideableWidget.showIt(self._basic._view.opsView.valueWidg)
            HideableWidget.showIt(self._basic._view.opsView.overriderChe)
            HideableWidget.showIt(self._basic._view.opsView.okBtn)
            HideableWidget.showIt(self._basic._view.opsView.value.get_layout())
            HideableWidget.showIt(self._basic._view.opsView.moreOps)
            self.set_ok_func(self._add_func)
        elif opsName == "delete":
            HideableWidget.showIt(self._basic._view.opsView.keyWidg)
            HideableWidget.showIt(self._basic._view.opsView.okBtn)
            self.set_ok_func(self._delete_func)
    def setup(self):
        self._basic._view.opsView.opsWidg.options = ["..","add", "delete"]
        self._basic._view.opsView.opsWidg.observe(self._ops, names="value")
        self._basic._view.opsView.moreOps.observe(self._ops_more, names="value")
        self._basic._view.opsView.opsWidg.value = ".."
        self._basic._view.opsView.okBtn.on_click(self._ok_clicked)
    def _ok_clicked(self, btn):
        if btn.description == "confirm":
            self._ok_func(btn, self)
            btn.description = "ok"
        else:
            btn.description = "confirm"
    def _ops(self, wid):
        self._ops_func(wid, self)
    def _ops_more(self, wid):
        val = self._basic._view.opsView.moreOps.value
        HideableWidget.showIt(self._basic._view.opsView.value.get_layout())
        if val in ["none", "is var"]:
            self._basic._view.opsView.value.set_index(0)
            self._basic._view.opsView.value.update()
        elif val in ["textarea", "eval"]:
            self._basic._view.opsView.value.set_index(1)
            self._basic._view.opsView.value.update()
        else:
            HideableWidget.hideIt(self._basic._view.opsView.value.get_layout())
    def set_basic_controller(self, cont):
        self._basic = cont
class Main:
    def pickleCrud(file):
        bc = Main._ins()
        lc = bc._parent
        lv = bc._view
        bc.set_model(PickleOpsModel())
        lc.setup()
        lc.set_file(file)
        opscont = lc._opsController
        opscont.setup()
        return lv.layout, lc
    def keyValueCrud(dic):
        bc = Main._ins()
        lc = bc._parent
        opscont = lc._opsController
        lv = bc._view
        model =PickleOpsModel()
        model.set_dictionary(dic)
        bc.set_model(model)
        lc.setup()
        opscont.setup()
        bc._view.fileView.pathWidg.set_index(1)
        bc._view.fileView.pathWidg.update()
        bc._view.fileView.pathWidg._widgets[1].value = "reading from dictionary"
        bc._view.fileView.labelWidg.value = "Stru:"
        return lv.layout, lc
    def _ins():
        lv = LoggerViews()
        lc = LoggerController()
        bc = BasicController()
        bc.set_view(lv)
        bc.set_parent(lc)
        lc.set_basic_controller(bc)
        opscont = OpsController()
        opscont.set_basic_controller(bc)
        lc.set_ops_controller(opscont)
        _, list_cnt = ViewsCollection.get_list_maker()
        lc.set_list_manager(list_cnt)
        return bc
    def withSqlModel(file, tableName):
        from timeline.t2023.sql_crud import SqlCRUD, SQLiteDictDB
        bc = Main._ins()
        model = SqlCRUD()
        db = SQLiteDictDB()
        db.set_file(file)
        db.set_table_name(tableName)
        model.set_db(db)
        bc.set_model(model)
        bc._parent.setup()
        bc._parent._opsController.setup()
        return bc