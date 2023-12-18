from timeline.t2023.generic_logger import FieldInfoView, GLView, SupportedTypes, FieldsManager, LoggerButtonNameDecider, LoggerSearch,LoggerDataCRUDOpsView, NewRenderer
from modules.SearchSystem.modular import HideableWidget
from TimeDB import TimeDB
from timeline.t2023.generic_logger.components import SingleButtonController
from basic import NameSpace
from SearchSystem import MultilineStringSearch
from timeline.t2023.searchSystem import Main as SearchWithPagination
from CryptsDB import CryptsDB
import ipywidgets as widgets

class NewLoggerNewWay:
    def generic_logger_default_state(self):
        self.app.controllers.utils.hideUi(self.app.views.groups.crud.create.layout)
        self.app.views.groups.crud.create.fields_props.typeOfWid.options = list(map(lambda x: x.name, SupportedTypes))
        self.app.controllers.utils.hideUi(self.app.views.groups.crud.create.fields_props.moreInfo.layout)
        self.app.controllers.searcher.logger.searcher = self.app.controllers.searcher.search_maker(
            self.app.controllers.searcher.logger.btn_maker,
            self.app.controllers.searcher.logger.btn_clicked_wrapper,
            self.app.controllers.searcher.logger.search_engine)
    def hide_ui(wid):
        HideableWidget.hideIt(wid)
    def show_ui(wid):
        HideableWidget.showIt(wid)
    def generic_radio_crud_func(self, *params):
        self.app.controllers.utils.showUi(self.app.views.groups.search.generic.layout)
        self.app.views.glv.out.clear()
        if self.app.views.groups.radio.crudView.wid.value == "c":
            self.app.views.groups.crud.create.logger_name_text.value = ""
            self.app.controllers.utils.hideUi(self.app.views.groups.search.generic.layout)
            self.app.controllers.utils.showUi(self.app.views.groups.crud.create.layout)
            self.app.model.fields_lookup.reset()
            self.app.views.groups.crud.create.fields_props.listWid.children = self.app.model.fields_lookup.get_layout()
        else:
            self.app.controllers.utils.hideUi(self.app.views.groups.crud.create.layout)
    def create_field_check_box_wrapper(self, wid):
        self.app.controllers.glv.field_checkbox_func(wid)
    def create_field_checkbox_func(self, *param):
        if self.app.views.groups.crud.create.fields_props.checkBox.value:
            self.app.controllers.utils.showUi(self.app.views.groups.crud.create.fields_props.moreInfo.layout)
        else:
            self.app.controllers.utils.hideUi(self.app.views.groups.crud.create.fields_props.moreInfo.layout)
    def create_logger(self, btn):
        val = self.app.views.groups.crud.create.logger_name_text.value.strip()
        if val == "":
            self.app.controllers.utils.showInfo_create_logger("give table name", True)
            return
        if len(self.app.model.fields_lookup._fields) == 0:
            self.app.controllers.utils.showInfo_create_logger("please give at least one field name", True)
            return
        self.app.model.tableOps.add(val, self.app.model.fields_lookup._fields)
        self.app.model.view_model.logger.updated_structure = True
        self.app.model.fields_lookup.reset()
        self.app.views.groups.crud.create.fields_props.listWid.children = self.app.model.fields_lookup.get_layout()
        self.app.views.groups.crud.create.logger_name_text.value = ""
    def plus_btn_clicked(self, btn):
        fields = self.app.views.groups.crud.create.fields_props
        key = fields.textWid.value.strip()
        typ = fields.typeOfWid.value
        options = fields.moreInfo.utils.get_value()

        if key == "":
            self.app.controllers.utils.showInfo_create_logger("give key name",isWarning=True)
            return
        if typ is None:
            self.app.controllers.utils.showInfo_create_logger("select a type",isWarning=True)
            return
        fields.textWid.value =""
        if self.app.model.fields_lookup.key:
            self.app.model.fields_lookup.update_field(self.app.model.fields_lookup.key, key, typ, options)
        else:
            self.app.model.fields_lookup.add_field(key,typ, options)
        self.app.model.fields_lookup.key = None
        self.app.views.groups.crud.create.fields_props.moreInfo.utils.set_value({})
        ly = self.app.model.fields_lookup._fields_view_map[key]
        self.app.controllers.utils.hideUi(ly.displayInfoWid)
        ly.editBtn._key = key
        ly.deleteBtn._key = key
        ly.editBtn.on_click(self.app.controllers.glv.field_edit_btn_wrapper)
        ly.deleteBtn.on_click(self.app.controllers.glv.field_delete_btn_wrapper)
        self.app.views.groups.crud.create.fields_props.listWid.children = self.app.model.fields_lookup.get_layout()
    def value_func(self):
        return self.app.views.groups.crud.create.fields_props.moreInfo.controller._basic._model.value()
    def crud_info(self, msg, isWarning = False):
        if isWarning:
            self.app.views.glv.loggerInfo.out.value = f"<font face='comic sans ms' color ='red'>{msg}</font>"
        else:
            self.app.views.glv.loggerInfo.out.value = f"<font face='comic sans ms' color ='blue'>{msg}</font>"
        def disapp():
            self.app.views.glv.loggerInfo.out.value=""
        TimeDB.setTimer().oneTimeTimer(5, disapp)
    def edit(self, btn):
        key = btn._key
        ike = self.app.model.fields_lookup.read_field(key)
        self.app.views.groups.crud.create.fields_props.textWid.value = key
        self.app.views.groups.crud.create.fields_props.typeOfWid.value = ike["type"]
        self.app.views.groups.crud.create.fields_props.moreInfo.utils.set_value(ike["info"])
        self.app.model.fields_lookup.key = key
    def delete(self, btn):
        key = btn._key
        self.app.model.fields_lookup.delete_field(key)
        self.app.views.groups.crud.create.fields_props.listWid.children = self.app.model.fields_lookup.get_layout()
        if self.app.model.fields_lookup.key == key:
            self.app.model.fields_lookup.key = None
    def editWrapper(self, btn):
        self.app.controllers.glv.field_edit_btn(btn)
    def deleteWrapper(self, btn):
        self.app.controllers.glv.field_delete_btn(btn)
    def update_keys(self, keys):
        cnt = self.app.views.groups.crud.create.fields_props.moreInfo.controller
        cnt._basic._model.set_dictionary(keys)
        cnt._update_keys()
    def logger_button_maker(self, key, fun):
        des = self.app.controllers.searcher.logger.search_engine.container[key]
        btn = SingleButtonController(description = des, layout= {"width":"auto", "max_width":"100px"})
        btn.set_clicked_func(fun)
        btn.layout._key = des
        return btn.layout
    def button_click_func(self, btn):
        typ = self.app.views.groups.radio.crudView.wid.value
        if not hasattr(self.app.model.view_model.logger, "logger_btn"):
            self.app.model.view_model.data_curr_state_key += 1
        elif self.app.model.view_model.logger.logger_btn.description != btn.description:
            self.app.model.view_model.data_curr_state_key += 1
        self.app.model.view_model.logger.logger_btn = btn
        if typ == "r":
            self.app.controllers.ops.logger.read_render(btn)
        elif typ == "d":
            self.app.controllers.ops.logger.delete(btn)
        elif typ == "u":
            self.app.controllers.ops.logger.update(btn)
    def button_click_func_wrapper(self, btn):
        self.app.controllers.searcher.logger.btn_clicked(btn)
    def logger_btn_clicked_result_wrapper(self, btn):
        self.app.controllers.glv.read_result_button(btn)
    def search_maker(maker, callback_func, searchEngine):
        return SearchWithPagination.searchWithPagination(searchEngine, maker, callback_func)
    def searching(self, btn):
        vals = self.app.model.tableOps.readAll()
        self.app.controllers.searcher.logger.search_engine.set_container(list(vals.keys()))
        wid =self.app.views.groups.search.generic
        word = wid.textWid.value
        ly = self.app.controllers.searcher.logger.searcher.search(word, wid.isRegWid.value, wid.isCase.value)
        self.app.views.groups.search.generic.couput.display(ly, True, True)
    def delete_logger(self, btn):
        name = btn._key
        self.app.model.tableOps.delete(name)
        self.app.controllers.utils.hideUi(btn)
    def update_logger(self, btn):
        table_name = btn._key
        self.app.controllers.utils.hideUi(self.app.views.groups.search.generic.layout)
        self.app.controllers.utils.showUi(self.app.views.groups.crud.create.layout)
        abc = self.app.model.tableOps.read(table_name)

        if table_name == self.app.views.groups.crud.create.logger_name_text.value and len(self.app.model.fields_lookup._fields) != 0:
            self.app.views.groups.crud.create.fields_props.listWid.children = self.app.model.fields_lookup.get_layout()
            return
        self.app.views.groups.crud.create.logger_name_text.value = table_name
        s = self.app.model.strings.structure
        for prp in abc[s]:
            yp = abc[s][prp]["type"]
            info = abc[s][prp]["info"]
            order = abc[s][prp]["order"]
            ly = self.app.model.fields_lookup.add_field(prp, yp, info, order)
            self.app.controllers.utils.hideUi(ly.displayInfoWid)
        self.app.views.groups.crud.create.fields_props.listWid.children = self.app.model.fields_lookup.get_layout()
    def logger_renderer(self, btn):
        self.app.model.view_model.currentLogger = btn._key
        self.app.views.glv.out.display(self.app.views.ldcv.layout,clear=True)
    def set_app(self, app):
        self.app = app
    def confirmed(self, btn):
        self.app.controllers.ops.confirmer.func(self.app.controllers.ops.confirmer.btn)
        self.app.controllers.ops.confirmer.out.clear()
    def delete_logger_confirmer(self, ads):
        self.app.views.btn.layout.description = "confirm"
        self.app.views.btn.set_clicked_func(self.app.controllers.ops.confirmer.def_func)

        self.app.controllers.ops.confirmer.out = self.app.views.glv.out
        self.app.controllers.ops.confirmer.btn = ads
        self.app.controllers.ops.confirmer.func = self.app.controllers.ins.nlnw.delete_logger

        self.app.controllers.ops.confirmer.out.display(self.app.views.btn.layout, True, True)
class ModelFunc:
    def __init__(self):
        self._logger = {}
        self.strings = NameSpace()
        self.strings.structure = "structure"
        self.strings.uuid = "uuid"
        self.strings.key_index = "key-index"
        self.strings.data = "data"

    def add(self, tablename, struc):
        if tablename not in self._logger:
            val = {self.strings.uuid: CryptsDB.generateUniqueId(), self.strings.data: {}}
        else:
            val = self._logger[tablename]
        val[self.strings.structure] = struc
        self._logger[tablename] = val
    def readAll(self):
        return self._logger
    def read(self, name):
        return self._logger[name]
    def delete(self, name):
        del self._logger[name]
    def add_data(self, tableName, data):
        tableContent = self.read(tableName)
        if self.strings.key_index not in tableContent:
            tableContent[self.strings.key_index] = 0

        key = tableContent[self.strings.key_index]

        if self.strings.data not in tableContent:
            tableContent[self.strings.key_index] = {}
        tableContent[self.strings.data][key] = data
        tableContent[self.strings.key_index] = key + 1

    def delete_data(self, idd):
        tableContent = self.read(tableName)
        del tableContent[self.strings.data][idd]
    def read_all_data(self, table_name):
        return self._logger[table_name][self.strings.data]
class InProcess:
    def __init__(self):
        self.clear()
    def clear(self):
        self._order = 0
        self._pending = {}
    def add(self, key, val, order = None):
        if self.has_key(key):
            return IOError("key already exists")
        if order is None:
            self._pending[self._order] = {"key": key,"val": val}
            self._order += 1
        else:
            self._pending[order] = {"key": key,"val": val}
    def read(self):
        return self._pending
    def has_key(self, key):
        for order in self._pending:
            val = self._pending[order]
            if key == val["key"]:
                return True
        return False
class LoggerDataOps:
    def dropdown(self, wdi):
        oldKey = wdi["old"]
        value = self.app.views.groups.ldcv.search.text.value
        key = self.app.views.groups.ldcv.search.dropdown.value
        if value != "":
            self.app.model.view_model.loggerData_dropdown[oldKey] = value
        if key not in self.app.model.view_model.loggerData_dropdown:
            self.app.views.groups.ldcv.search.text.value = ""
        else:
            self.app.views.groups.ldcv.search.text.value = self.app.model.view_model.loggerData_dropdown[key]
    def checkbox_data_wrapper(self, info):
        self.app.controllers.ldcv.check_box_func(info)
    def dropdown_wrapper(self, wid):
        self.app.controllers.ldcv.search_drop_func(wid)
    def checkbox_data_func(self, info):
        opstype = self.app.views.groups.ldcv.checkbox.value
        if opstype == "c":
            self.app.controllers.utils.hideUi(self.app.views.ldcv.searchView.layout)
            if self.app.controllers.ops.data.should_create_new_renderer():
                nr = self.app.controllers.ops.data.renderer_creator(self.app.model.view_model.currentLogger)
                layout = nr.render()
                self.app.model.view_model.logger.updated_structure = False
            else:
                nr = self.app.model.view_model.create_state[self.app.model.view_model.currentLogger]
                layout = nr._rendered
                if self.app.model.view_model.logger_data.check_box_prev_state == "u":
                    self.app.controllers.ldcv.data_reset(nr)
            self.app.views.ldcv.out.display(layout, clear=True)
        else:
            self.app.controllers.utils.showUi(self.app.views.ldcv.searchView.layout)
            self.app.views.ldcv.out.clear()
        self.app.model.view_model.logger_data.check_box_prev_state = opstype
    def search_clicked_data(self, btn):
        self.app.controllers.ldcv.update_data()
        self.app.controllers.btn_name_decider.set_structure(self.app.controllers.ldcv.read_structure())
        self.app.controllers.searcher.data.engine.set_indices_to_search(self.app.controllers.btn_name_decider._indicesForName)
        word = self.app.views.ldcv.searchView.textWid.value.strip()
        reg = False
        case = False
        ops = self.app.views.ldcv.searchView.searchType.value
        self.app.controllers.searcher.data.engine.set_search_type(ops)
        if ops == "case":
            case = True
        elif ops == "reg":
            reg = True
        layo = self.app.controllers.searcher.data.searcher.search(word, reg =reg, case=case)

        self.app.views.ldcv.searchView.couput.display(layo, True, True)
    def logged_btn_func(self, *params):
        nr = self.app.model.view_model.create_state[self.app.model.view_model.currentLogger]
        data = self.app.controllers.ldcv.data_from_rendered(nr)
        self.app.controllers.ldcv.data_reset(nr)
        self.app.model.tableOps.add_data(self.app.model.view_model.currentLogger, data)
    def data_from_rendered(nr):
        data = {}
        for ke in nr._key_view_map:
            com = nr._key_view_map[ke]
            data[ke] = com.value()
        return data
    def reset_rendered_state(nr):
        for ke in nr._key_view_map:
            com = nr._key_view_map[ke]
            com.clear()
    def logger_data_btn_maker(self, des, func):
        self.app.controllers.btn_name_decider.set_info(self.app.controllers.ldcv.read_data(des), des)
        btn = SingleButtonController(description = self.app.controllers.btn_name_decider.get_name(), layout= {"width":"auto", "max_width":"100px"})
        btn.set_clicked_func(func)
        btn.layout._key = des
        return btn.layout
    def read_data(self, key):
        data = self.app.model.tableOps.read_all_data(self.app.model.view_model.currentLogger)
        return data[key]
    def data_btn_clicked(self, btn):
        self.app.model.view_model.current_data_btn =  btn
        val = self.app.views.groups.ldcv.checkbox.value
        if val == "r":
            self.app.views.ldcv.out.clear()
            with self.app.views.ldcv.out._out:
                print(self.app.controllers.ldcv.read_data(btn._key))
        elif val == "d":
            self.app.controllers.ldcv.delete_data(btn)
        elif val == "u":
            self.app.controllers.ldcv.data_update_radio_selected(btn)
    def data_btn_clicked_wrapper(self, btn):
        self.app.controllers.searcher.data.btn_clicked(btn)
    def read_structure(self):
        return self.app.model.tableOps.read(self.app.model.view_model.currentLogger)[self.app.model.strings.structure]
    def update_data(self):
        if self.app.model.view_model.data_prev_state_key != self.app.model.view_model.data_curr_state_key:
            self.app.controllers.searcher.data.engine.set_container(self.app.model.tableOps.read_all_data(self.app.model.view_model.currentLogger))
            self.app.model.view_model.data_prev_state_key += 1
            self.app.model.view_model.data_curr_state_key = self.app.model.view_model.data_prev_state_key
    def delete_it(self, btn):
        self.app.controllers.ops.data.delete(btn._key)
        self.app.controllers.utils.hideUi(btn)
    def delete_data(self, idd):
        del self.app.model.tableOps.read(self.app.model.view_model.currentLogger)[self.app.model.strings.data][idd]
    def update_value(self, idd, new_val):
        infos = self.app.model.tableOps.read(self.app.model.view_model.currentLogger)
        infos[self.app.model.strings.data][idd] = new_val
    def update_btn_clicked(self, btn):
        values = self.app.controllers.ldcv.data_from_rendered(self.app.model.view_model.create_state[self.app.model.view_model.currentLogger])
        idd = self.app.model.view_model.current_data_btn._key
        self.app.controllers.btn_name_decider.set_info(values, idd)
        self.app.controllers.ops.data.update(idd, values)
        self.app.views.ldcv.out.clear()
        self.app.model.view_model.current_data_btn.description = self.app.controllers.btn_name_decider.get_name()
    def update_callback_on_data_btn_clicked(self, btn):
        if self.app.controllers.ops.data.should_create_new_renderer():
            nr = self.app.controllers.ops.data.renderer_creator(self.app.model.view_model.currentLogger)
            self.app.model.view_model.logger.updated_structure = False
            nr.render()
        else:
            nr = self.app.model.view_model.create_state[self.app.model.view_model.currentLogger]

        vals  = self.app.controllers.ldcv.read_data(btn._key)
        self.app.controllers.ldcv.update_view_state(nr, vals)
        fields = nr._rendered.children[:-1]
        self.app.views.btn.layout.description = "update"
        self.app.views.btn.set_clicked_func(self.app.controllers.ldcv.data_update_clicked)
        ly = widgets.VBox(list(fields) + [self.app.views.btn.layout])
        self.app.views.ldcv.out.display(ly, True, True)
    def update_state(nr, values):
        fields = nr._key_view_map
        for k in fields:
            field_view = fields[k]
            if k in values:
                field_view.set_value(values[k])
            else:
                field_view.clear()
    def create_renderer(self, table_name):
        nr = NewRenderer()
        nr._structure = self.app.model.tableOps.read(table_name)[self.app.model.strings.structure]
        nr._scope = self.app.model.scope
        self.app.model.view_model.create_state[table_name] = nr
        nr.set_adder_func(self.app.controllers.ldcv.generic_data_logger)
        return nr
    def newRequire(self):
        return self.app.model.view_model.logger.updated_structure or self.app.model.view_model.currentLogger not in self.app.model.view_model.create_state
    def set_app(self, app):
        self.app = app

    def delete_data_confirmer(self,btn):
        self.app.controllers.ops.confirmer.out = self.app.views.ldcv.out
        self.app.controllers.ops.confirmer.btn = btn
        self.app.controllers.ops.confirmer.func = self.app.controllers.ins.ldo.delete_it

        self.app.views.btn.layout.description = "confirm"
        self.app.views.btn.set_clicked_func(self.app.controllers.ops.confirmer.def_func)

        self.app.controllers.ops.confirmer.out.display(self.app.views.btn.layout, True, True)
class Main:
    def logger(scope = None, callSetUp=True):
        if scope is None:
            scope = {}
        glv = GLView()
        app = NameSpace()
        nlnw = NewLoggerNewWay()
        nlnw.set_app(app)

        ldo = LoggerDataOps()
        ldo.set_app(app)

        app.controllers = NameSpace()
        app.views = NameSpace()
        app.model = NameSpace()
        app.model.scope = scope
        app.model.tableOps = ModelFunc()
        app.model.fields_lookup = FieldsManager()
        app.model.fields_lookup.key = None
        app.views.groups = NameSpace()
        app.controllers.btn_name_decider = LoggerButtonNameDecider()
        app.views.groups.crud = NameSpace()
        app.views.groups.crud.create = NameSpace()
        app.views.groups.crud.create.layout = glv.crudopsWid
        app.views.groups.crud.create.logger_name_text = glv.loggerInfo.nameWid
        app.views.groups.crud.create.fields_props = glv.fieldInfo
        app.views.groups.radio = NameSpace()
        app.views.groups.search = NameSpace()
        app.views.groups.search.generic = glv.logSearch
        app.views.groups.radio.crudView = glv.crudOps.options
        app.views.glv = glv
        app.controllers.utils = NameSpace()
        app.controllers.utils.hideUi = NewLoggerNewWay.hide_ui
        app.controllers.utils.showUi = NewLoggerNewWay.show_ui
        app.views.groups.crud.create.create_btn = glv.loggerInfo.createBtn
        app.views.groups.crud.create.fields_props.moreInfo = NameSpace()
        app.views.groups.crud.create.fields_props.moreInfo.layout = glv.moreInfo[0]
        app.views.groups.crud.create.fields_props.moreInfo.controller = glv.moreInfo[1]
        app.views.groups.crud.create.info_display = glv.loggerInfo.out
        app.controllers.glv = NameSpace()
        app.controllers.glv.radio = NameSpace()
        app.controllers.glv.radio.wrapper = nlnw.generic_radio_crud_func
        app.controllers.glv.field_checkbox_wrapper = nlnw.create_field_check_box_wrapper
        app.controllers.glv.field_checkbox_func = nlnw.create_field_checkbox_func
        app.controllers.set_up = nlnw.generic_logger_default_state
        app.views.groups.crud.create.fields_props.moreInfo.utils = NameSpace()
        app.views.groups.crud.create.fields_props.moreInfo.utils.set_value = nlnw.update_keys
        app.views.groups.crud.create.fields_props.moreInfo.utils.get_value = nlnw.value_func
        app.controllers.utils.showInfo_create_logger = nlnw.crud_info
        app.controllers.glv.field_edit_btn  = nlnw.edit
        app.controllers.glv.field_delete_btn = nlnw.delete
        app.controllers.glv.field_edit_btn_wrapper = nlnw.editWrapper
        app.controllers.glv.field_delete_btn_wrapper = nlnw.deleteWrapper
        app.views.groups.crud.create.fields_props.moreInfo.controller._basic.set_scope(app.model.scope)
        app.controllers.searcher = NameSpace()
        app.controllers.searcher.search_maker = NewLoggerNewWay.search_maker
        app.controllers.searcher.logger = NameSpace()
        app.controllers.searcher.logger.search_engine = MultilineStringSearch([], allRes=True)
        app.controllers.searcher.logger.btn_maker = nlnw.logger_button_maker
        app.controllers.searcher.logger.btn_clicked = nlnw.button_click_func
        app.controllers.searcher.logger.btn_clicked_wrapper = nlnw.button_click_func_wrapper
        app.controllers.ops = NameSpace()
        app.controllers.ops.logger = NameSpace()
        app.controllers.ops.logger.read_render = nlnw.logger_renderer
        app.controllers.ops.logger.delete = nlnw.delete_logger
        app.controllers.ops.logger.update = nlnw.update_logger
        app.model.view_model = NameSpace()
        app.model.view_model.loggerData_dropdown = {}
        app.views.groups.ldcv = NameSpace()
        app.views.ldcv = LoggerDataCRUDOpsView()
        app.views.groups.ldcv.search = NameSpace()
        app.controllers.ldcv = NameSpace()
        app.controllers.ldcv.search_drop_func = ldo.dropdown
        app.views.groups.ldcv.search.text = app.views.ldcv.searchView.textWid
        app.views.groups.ldcv.search.dropdown = app.views.ldcv.searchView.searchType
        app.model.view_model.currentLogger = None
        app.model.view_model.create_state = {}
        app.controllers.ldcv.search_drop_wrap = ldo.dropdown_wrapper
        app.views.groups.ldcv.checkbox = app.views.ldcv.opsWid.wid
        app.controllers.ldcv.check_box_func = ldo.checkbox_data_func
        app.controllers.ldcv.data_from_rendered = LoggerDataOps.data_from_rendered
        app.controllers.ldcv.data_reset = LoggerDataOps.reset_rendered_state
        app.controllers.ldcv.generic_data_logger = ldo.logged_btn_func
        app.controllers.searcher.data = NameSpace()
        app.controllers.searcher.data.btn_maker = ldo.logger_data_btn_maker
        app.controllers.searcher.data.engine = LoggerSearch()
        app.controllers.searcher.data.btn_clicked_wrapper = ldo.data_btn_clicked_wrapper
        app.controllers.searcher.data.btn_clicked = ldo.data_btn_clicked
        app.controllers.searcher.data.searcher = app.controllers.searcher.search_maker(
            app.controllers.searcher.data.btn_maker, app.controllers.searcher.data.btn_clicked_wrapper, app.controllers.searcher.data.engine)
        app.controllers.ldcv.read_data = ldo.read_data
        app.controllers.ldcv.read_structure = ldo.read_structure
        app.model.view_model.data_prev_state_key = -1
        app.model.view_model.data_curr_state_key = 0
        app.controllers.ldcv.update_data = ldo.update_data
        app.controllers.ldcv.delete_data = ldo.delete_it
        app.controllers.ops.data = NameSpace()
        app.controllers.ops.data.delete = ldo.delete_data
        app.controllers.ldcv.update_view_state = LoggerDataOps.update_state
        app.controllers.ldcv.data_update_clicked =ldo.update_btn_clicked
        app.controllers.ops.data.update = ldo.update_value
        app.controllers.ldcv.data_update_radio_selected = ldo.update_callback_on_data_btn_clicked
        app.views.btn = SingleButtonController()
        app.model.view_model.logger = NameSpace()
        app.model.view_model.logger.updated_structure = False
        app.controllers.ops.data.should_create_new_renderer = ldo.newRequire
        app.controllers.ops.data.renderer_creator = ldo.create_renderer
        app.controllers.ldcv.wrappers = NameSpace()
        app.controllers.ldcv.wrappers.searchbtn = ldo.search_clicked_data
        app.controllers.ldcv.wrappers.checkbox = ldo.checkbox_data_wrapper
        app.controllers.glv.wrappers = NameSpace()
        app.controllers.glv.wrappers.searchbtn = nlnw.searching
        app.controllers.glv.wrappers.create_log_btn = nlnw.create_logger
        app.controllers.glv.wrappers.plusbtn = nlnw.plus_btn_clicked
        app.model.view_model.logger_data = NameSpace()
        app.model.view_model.logger_data.check_box_prev_state = None
        app.controllers.ins = NameSpace()
        app.controllers.ins.ldo = ldo
        app.controllers.ins.nlnw = nlnw
        app.controllers.ops.logger.delete = nlnw.delete_logger_confirmer
        app.controllers.ldcv.delete_data = ldo.delete_data_confirmer
        app.controllers.ops.confirmer = NameSpace()
        app.controllers.ops.confirmer.out = None
        app.controllers.ops.confirmer.def_func = nlnw.confirmed
        app.controllers.ops.confirmer.func = None
        app.controllers.ops.confirmer.btn = None

        app.controllers.modelWrapper = NameSpace()
        app.controllers.modelWrapper.read_tables = None
        app.controllers.modelWrapper.read_structure = None
        app.controllers.modelWrapper.read_all_data = None
        #app.controllers.modelWrapper.read_with_pagination = None
        #app.controllers.modelWrapper.read_with_filter = None
        app.controllers.modelWrapper.delete_table = None
        app.controllers.modelWrapper.delete_data = None
        app.controllers.modelWrapper.update_structure = None
        app.controllers.modelWrapper.update_data =None
        app.controllers.modelWrapper.create_new_table = None
        app.model.strings = NameSpace()
        app.model.strings.structure = "structure"
        app.model.strings.uuid = "uuid"
        app.model.strings.key_index = "key-index"
        app.model.strings.data = "data"

        app.views.groups.crud.create.create_btn.set_clicked_func(app.controllers.glv.wrappers.create_log_btn)
        app.views.groups.crud.create.fields_props.fieldAddBtn.set_clicked_func(app.controllers.glv.wrappers.plusbtn)
        app.views.groups.crud.create.fields_props.checkBox.observe(app.controllers.glv.field_checkbox_wrapper, ["value"])
        app.views.groups.radio.crudView.set_select_func(app.controllers.glv.radio.wrapper)
        app.views.groups.search.generic.btn.set_clicked_func(app.controllers.glv.wrappers.searchbtn)
        app.views.groups.ldcv.search.dropdown.observe(app.controllers.ldcv.search_drop_wrap, ["value"])
        app.views.groups.ldcv.checkbox.observe(app.controllers.ldcv.wrappers.checkbox, ["value"])
        app.views.ldcv.searchView.btn.set_clicked_func(app.controllers.ldcv.wrappers.searchbtn)
        if callSetUp:
            app.controllers.set_up()
        return app
