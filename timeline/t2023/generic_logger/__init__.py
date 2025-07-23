import ipywidgets as widgets
from modules.SearchSystem.modular import HideableWidget
from modules.Explorer.personalizedWidgets import CustomOutput
from timeline.t2023.searchSystem import Main as SearchWithPagination
from PickleCRUDDB import PickleCRUDOps
from enum import Enum
from SearchSystem import ISearch
from ComparerDB import ComparerDB
from SerializationDB import SerializationDB
from LibsDB import LibsDB
from CryptsDB import CryptsDB
from timeline.t2023.generic_logger.components import TextInput, TextAreaInput, BooleanOptionInput, DropdownInput, DateInput, TimeInput, DateTimeInput, MultipleSelect, KeyValueInput, SingleButtonController
from basic import BasicController, LoggerSystem
from timeline.t2023.generic_logger.UIComponents import CrudViewV2, SearchComponent, ObjMaker, SingleField, UpdateMenu
from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib

class StringEnums:
    DISABLED = "disabled"
    AUTO = "auto"
    OPTIONS ="options"
    TYPE ="type"
    INFO ="info"
    KEY_NR = "key-index"
    ORDER = "order"
    STATUS = "status"
    DELETED = "deleted"
    UUID = "uuid"
class IModifier:
    def set_basic_controller(self, bsc):
        pass
    def get_layout(self):
        pass
    def set_up(self):
        pass
    def update_data(self, version: int):
        pass
class SupportedTypes(Enum):
    Text = 1
    LargeText = 2
    Checkbox = 3
    Options = 4
    Date = 5
    Time = 6
    DateTime = 7
    KeyValuesPair = 8
    MultipleSelect = 9
    Boolean = 10
    Crud = 11

class CRUPOps(Enum):
    READ= "r"
    CREATE= "c"
    UPDATE= "u"
    DELETE = "d"

def FieldsManagerV2():
    fields = {}
    order_number = 0
    def get_fields_sorted():
        return {key: s.process.fields[key] for key in s.handlers.get_ordered_fields()}
    def set_fields(fieldsStruct):
        s.process.fields = fieldsStruct
        s.process.order_number = max(map(lambda x: fieldsStruct[x][StringEnums.ORDER], fieldsStruct)) + 1
    def reset():
        s.process.fields = {}
        s.process.order_number = 0
    def add_field(val, typ, info, order =None):
        if order is None:
            order = s.process.order_number
            s.process.order_number += 1
        s.process.fields[val]= {StringEnums.TYPE: typ, StringEnums.INFO: info, StringEnums.ORDER: order}
    def moveDown(key):
        val = s.process.fields[key]
        ordered = s.handlers.get_ordered_fields()
        index = None
        for i, ke in enumerate(ordered):
            if key == ke:
                index = i
                break
        if index is not None and index < (len(ordered) - 1):
            otherKey = ordered[index + 1]
            otherVal = s.process.fields[otherKey]
            m = val[StringEnums.ORDER]
            val[StringEnums.ORDER] = otherVal[StringEnums.ORDER]
            otherVal[StringEnums.ORDER] = m
    def moveUp(key):
        val = s.process.fields[key]
        ordered = s.handlers.get_ordered_fields()
        index = None
        for i, ke in enumerate(ordered):
            if key == ke:
                index = i
                break
        if index is not None and index > 0:
            otherKey = ordered[index - 1]
            otherVal = s.process.fields[otherKey]
            m = val[StringEnums.ORDER]
            val[StringEnums.ORDER] = otherVal[StringEnums.ORDER]
            otherVal[StringEnums.ORDER] = m
    def delete_field(fieldKey):
        del s.process.fields[fieldKey]
    def update_field(oldFieldKey, newKey, newType, newInfo):
        order = s.process.fields[oldFieldKey][StringEnums.ORDER]
        s.handlers.delete_field(oldFieldKey)
        return s.handlers.add_field(newKey, newType, newInfo, order)
    def get_ordered_fields():
        return sorted(s.process.fields, key= lambda y: s.process.fields[y][StringEnums.ORDER])
    def read_field(fieldKey):
        return s.process.fields[fieldKey]
    s = ObjMaker.variablesAndFunction(locals())
    return s
def GLViewV2():
    crudView = CrudViewV2()
    searchComponent = SearchComponent()
    updatePage = UpdateMenu()
    fieldCrudForm = updatePage.process.fieldsCrud
    fieldsManager = FieldsManagerV2()
    keysOut = Utils.get_comp({}, ComponentsLib.CustomOutput, bind=False)
    resultsOut = Utils.get_comp({}, ComponentsLib.CustomOutput, bind=False)
    def editing(wid):
        key = wid._parent.inputs.parent.inputs.parent.state.key
        vals = s.process.fieldsManager.process.fields[key]
        s.process.fieldCrudForm.views.fieldType.outputs.layout.value = vals["type"]
        s.process.fieldCrudForm.views.fieldName.outputs.layout.value = key
        s.process.fieldCrudForm.process.keyValueComp.handlers.set_dictionary(vals["info"])
        s.process.fieldCrudForm.views.addBtn.handlers.handle = s.handlers.overwriteField
        s.process.oldKey = key
    def overwriteField(wid):
        s.process.fieldCrudForm.views.addBtn.handlers.handle = s.handlers.add_field_handler
        key = s.process.fieldCrudForm.views.fieldName.outputs.layout.value
        typ = s.process.fieldCrudForm.views.fieldType.outputs.layout.value
        moreInfos = s.process.fieldCrudForm.process.keyValueComp.views.moreInfoLay.state.controller._basic._model.content.copy()
        s.process.fieldsManager.handlers.update_field(s.process.oldKey, key, typ, moreInfos)
        s.handlers.reset_form_values()
        s.handlers.syncViewList()
    def reset_form_values():
        s.process.fieldCrudForm.views.fieldName.outputs.layout.value = ""
        s.process.fieldCrudForm.process.keyValueComp.handlers.set_dictionary({})
    def syncViewList():
        notDelete = []
        for sf in s.process.fieldCrudForm.views.fieldsList.outputs.renderedStates:
            if not sf.state.deleted:
                notDelete.append(sf)
        fields = s.process.fieldsManager.handlers.get_ordered_fields()
        for sf, key in zip(notDelete, fields):
            sf.state.parent.views.fieldName.outputs.layout.value = key
            sf.state.parent.views.fieldType.outputs.layout.value = s.process.fieldsManager.process.fields[key]["type"]
            sf.state.parent.views.container.state.key = key
    def set_fields(keyVals):
        s.process.fieldsManager.handlers.set_fields(keyVals)
        fields = s.process.fieldsManager.handlers.get_ordered_fields()
        for key in fields:
            s.handlers.add_a_field(key, s.process.fieldsManager.process.fields[key]["type"])
    def clear_fields():
        s.process.fieldsManager.handlers.reset()
        s.handlers.reset_form_values()
        s.process.fieldCrudForm.views.fieldsList.clear()
    def delete_clicked(wid):
        key = wid._parent.inputs.parent.inputs.parent.state.key
        wid._parent.inputs.parent.inputs.parent.hide()
        s.process.fieldsManager.handlers.delete_field(key)
        wid._parent.inputs.parent.inputs.parent.state.deleted = True
    def moveUp(wid):
        key = wid._parent.inputs.parent.inputs.parent.state.key
        s.process.fieldsManager.handlers.moveUp(key)
        s.handlers.syncViewList()
    def moveDown(wid):
        key = wid._parent.inputs.parent.inputs.parent.state.key
        s.process.fieldsManager.handlers.moveDown(key)
        s.handlers.syncViewList()
    def add_field_handler(wid):
        key = s.process.fieldCrudForm.views.fieldName.outputs.layout.value
        typ = s.process.fieldCrudForm.views.fieldType.outputs.layout.value
        moreInfos = s.process.fieldCrudForm.process.keyValueComp.views.moreInfoLay.state.controller._basic._model.content.copy()
        if not (key and typ):
            return
        if key in s.process.fieldsManager.process.fields:
            return
        s.handlers.add_a_field(key, typ)
        s.process.fieldsManager.handlers.add_field(key, typ, moreInfos)
        s.handlers.reset_form_values()
    def add_a_field(key, typ):
        sf = SingleField()
        sf.views.fieldName.outputs.layout.value = key
        sf.views.fieldType.outputs.layout.value = typ
        sf.views.fieldName.outputs.layout.add_class("w-auto")
        sf.views.fieldType.outputs.layout.add_class("w-auto")
        sf.views.container.state.parent = sf
        sf.views.container.state.key = key
        sf.views.container.state.deleted = False
        sf.views.deleteButton.handlers.handle = delete_clicked
        sf.views.editButton.handlers.handle = s.handlers.editing
        sf.views.upIcon.handlers.handle = moveUp
        sf.views.downIcon.handlers.handle = moveDown
        s.process.fieldCrudForm.views.fieldsList.append(sf.views.container)
    def radioSelected(wid):
        val = s.process.crudView.views.crudView.outputs.layout.value
        if val == "c":
            s.process.updatePage.views.container.show()
            s.process.searchComponent.views.container.hide()
        else:
            s.process.updatePage.views.container.hide()
            s.process.searchComponent.views.container.show()
    searchWithResults = Utils.container([searchComponent.views.container, keysOut], className="flex flex-column")

    container = Utils.container([Utils.container([crudView.views.container, searchWithResults]),
        updatePage.views.container, resultsOut ], className="flex flex-column")
    
    s = ObjMaker.uisOrganize(locals())
    fieldCrudForm.views.addBtn.handlers.handle = add_field_handler
    crudView.views.crudView.handlers.handle = radioSelected
    radioSelected(1)
    return s
class LoggerSearcherController:
    def __init__(self):
        self._clicked = None
        self.set_searcher(self.get_default_searcher())
    def set_searcher(self, searcher):
        self._searcher = searcher
    def set_button_click_func(self, func):
        self._clicked_func = func
    def set_basic_controller(self, bsc):
        self._bsc = bsc
    def set_up(self):
        self._bsc.views.glv.process.searchComponent.views.searchBtn.handlers.handle = self._on_search_clicked
        self._bsc.views.glv.process.crudView.views.crudView.handlers.handle = self._ops_selected
        self.set_button_click_func(self._opIt)
    def _active_loggers_keys(self):
        allContent = self._bsc._model.readAll()
        keys = []
        for x in allContent:
            if StringEnums.STATUS not in allContent[x]:
                keys.append(x)
            elif allContent[x][StringEnums.STATUS] != StringEnums.DELETED:
                keys.append(x)
        return keys
    def _on_search_clicked(self, btn):
        word = self._bsc.views.glv.process.searchComponent.views.inputText.outputs.layout.value.strip()
        val = self._bsc.views.glv.process.searchComponent.views.searchType.outputs.layout.value
        reg = False
        case = False
        if val == "reg":
            reg = True
        elif val == "case":
            case = True
        self._tasks_names = self._active_loggers_keys()
        self._searcher._engine.set_container(self._tasks_names)
        layo = self._searcher.search(word, reg =reg, case=case)
        self._bsc.views.glv.views.keysOut.state.controller.display(layo, True, True)
    def _btn_click_func(self, btn):
        self._bsc.debug = btn
        self._clicked_func(btn, self)
    def _opIt(self, btn, *param):
        self._current_btn = btn
        self._bsc.views.glv.views.resultsOut.state.controller.display(self._bsc.views.ldcv.layout, True, True)
        self._bsc.controllers.ldcc.set_current_btn(btn)
        self._bsc.views.ldcv.searchView.couput.clear()
        self._bsc.controllers.ldcc._ops_selected(None)
    def _delete_logger_intermediate(self, btn, *param):
        self._clicked = btn
        self._bsc.views.glv.process.searchComponent.views.searchBtn.outputs.layout.description = "confirm"
        self._bsc.views.glv.process.searchComponent.views.searchBtn.handlers.handle = self._delete_logger
    def _delete_logger(self, btn, *param):
        taskName = self._clicked.description
        self._bsc.views.glv.process.searchComponent.views.searchBtn.handlers.handle = self._on_search_clicked
        if taskName:
            self._bsc.views.glv.process.searchComponent.views.searchBtn.outputs.layout.description = "search"
            st = self._bsc._model.read(taskName)
            st["status"] = "deleted"
            self._bsc._model.add(taskName, st, True)
            self._clicked._parent.hide()
            self._clicked = None
    def _default_update_logger(self, btn, *param):
        self._bsc.views.glv.handlers.clear_fields()
        st = self._bsc._model.read(btn.description)
        self._bsc.views.glv.process.fieldCrudForm.views.loggerName.outputs.layout.value = btn.description
        struc = st["structure"]
        self._bsc.views.glv.handlers.set_fields(struc)
        self._bsc.views.glv.process.updatePage.views.container.show()
        
    def _btn_maker(self, des, func):
        btn = Utils.get_comp({"description":self._tasks_names[des]}, IpywidgetsComponentsEnum.Button, className="w-auto")
        btn.handlers.handle = func
        return btn.outputs.layout
    def get_default_searcher(self):
        from timeline.t2023.links_crud_ui import SearchEngine, ButtonViewWithPagination
        from SearchSystem import MultilineStringSearch
        see = SearchEngine()
        bvvp = ButtonViewWithPagination()
        bvvp.set_element_maker(self._btn_maker)
        bvvp.set_btn_click_func(self._btn_click_func)
        see.set_result_maker(bvvp)
        self._container = []
        mss = MultilineStringSearch(self._container, True)
        see.set_engine(mss)
        see.default_display(False)
        return see
    def _ops_selected(self, wid, *param):
        self._bsc.views.glv.handlers.radioSelected(wid)
        self._bsc.views.glv.process.searchComponent.views.searchBtn.handlers.handle = self._on_search_clicked
        val = self._bsc.views.glv.process.crudView.views.crudView.outputs.layout.value
        self._bsc.views.glv.process.searchComponent.views.container.show()
        self._bsc.views.glv.views.resultsOut.state.controller.clear()
        if val == CRUPOps.READ.value:
            self.set_button_click_func(self._opIt)
        elif val == CRUPOps.UPDATE.value:
            self.set_button_click_func(self._default_update_logger)
            self._bsc.views.glv.process.fieldCrudForm.views.createBtn.handlers.handle = self._update_logger_structure
        elif val == CRUPOps.DELETE.value:
            self.set_button_click_func(self._delete_logger_intermediate)
        elif val == CRUPOps.CREATE.value:
            self._bsc.views.glv.process.fieldCrudForm.views.createBtn.handlers.handle = self._create_logger
            self._bsc.views.glv.process.searchComponent.views.container.hide()
            self._bsc.views.glv.handlers.clear_fields()
            self._bsc.views.glv.views.keysOut.state.controller.clear()
    def _update_logger_structure(self, btn):
        val = self._bsc.views.glv.process.fieldCrudForm.views.loggerName.outputs.layout.value.strip()
        if not val:
            self._bsc.views.glv.process.fieldCrudForm.handlers.info("give a logger name", True)
            return
        if len(self._bsc.views.glv.process.fieldsManager.handlers.get_fields_sorted())== 0:
            self._bsc.views.glv.process.fieldCrudForm.handlers.info("add some fields", True)
            return
        self._bsc.views.glv.process.fieldCrudForm.handlers.info("updating logger")
        content = self._bsc._model.read(val)
        content['structure'] = self._bsc.views.glv.process.fieldsManager.handlers.get_fields_sorted()
        self._bsc._model.add(val, content, True)
        self._bsc.views.glv.handlers.clear_fields()
        self._bsc.views.glv.process.updatePage.views.container.hide()
        self._current_btn._parent.state.updated = True
    def set_logged_data_crud_operator(self, oper):
        self._bsc.controllers.ldcc = oper
    def _create_logger(self, btn):
        val = self._bsc.views.glv.process.fieldCrudForm.views.loggerName.outputs.layout.value.strip()
        if not val:
            self._bsc.views.glv.process.fieldCrudForm.handlers.info("give a logger name", True)
            return
        if len(self._bsc.views.glv.process.fieldsManager.handlers.get_fields_sorted())== 0:
            self._bsc.views.glv.process.fieldCrudForm.handlers.info("add some fields", True)
            return
        self._bsc.views.glv.process.fieldCrudForm.handlers.info("adding logger")
        self._bsc._model.add(val, {'structure': self._bsc.views.glv.process.fieldsManager.handlers.get_fields_sorted(), 'data': {},
            StringEnums.UUID: CryptsDB.generateUniqueId()})
        self._bsc.views.glv.handlers.clear_fields()
class LoggerDataCRUDOpsView:
    def __init__(self):
        self.opsWid = CrudViewV2()
        self.searchView = AdvanceSearchView()
        self.out = CustomOutput()
        self.layout = widgets.VBox([widgets.HBox([self.opsWid.views.container.outputs.layout, self.searchView.layout]), self.out.get_layout()])
class AdvanceSearchView:
    def __init__(self):
        self.textWid = widgets.Text(placeholder = "word", layout={"width":"auto"})
        self.searchType = widgets.Dropdown(options=["any", "reg", "case", "word", "concatenated", "fields"], layout ={"width":"auto"})
        self.btn = SingleButtonController(description="search", layout={"width":"auto"})
        self.couput = CustomOutput()
        self.btnOutput = CustomOutput()
        self.searchRow = widgets.HBox([self.textWid, self.searchType, self.btn.layout])
        self.layout = widgets.VBox([self.searchRow,self.couput.get_layout(), self.btnOutput.get_layout()])
class NewRenderer:
    def __init__(self):
        self._key_view_map = {}
        self._rendered = None
        self.set_creator_map( self.default_map() )
    def set_creator_map(self, map_func):
        self._creator_map = map_func
    def set_scope(self, scope):
        self._scope = scope
    def default_map(self):
        def keyCVal(**x):
            kvi = KeyValueInput(**x)
            kvi._controller._basic.set_scope(self._scope)
            return kvi
        dic = {
            SupportedTypes.Text.name: lambda **x: TextInput(**x),
            SupportedTypes.LargeText.name: lambda **x: TextAreaInput(**x, layout = {"width": "auto"}),
            SupportedTypes.Checkbox.name: lambda **x: BooleanOptionInput(**x),
            SupportedTypes.Options.name: lambda **x: DropdownInput(**x),
            SupportedTypes.Date.name: lambda **x: DateInput(**x),
            SupportedTypes.Time.name: lambda **x: TimeInput(**x),
            SupportedTypes.DateTime.name: lambda **x: DateTimeInput(**x),
            SupportedTypes.KeyValuesPair.name: keyCVal,
            SupportedTypes.MultipleSelect.name: lambda **x: MultipleSelect(**x),
            SupportedTypes.Boolean.name: lambda **x: BooleanOptionInput(**x)
        }
        return dic
    def set_adder_func(self, func):
        self._on_log_func = func
    def set_model(self, name, model):
        self._name = name
        self._model = model
        self._structure = model.read(name)['structure']
    def creator():
        return NewRenderer()
    def render(self):
        if self._rendered:
            return self._rendered
        res = []
        for key in self._structure:
            typ = self._structure[key][StringEnums.TYPE]
            infos = self._structure[key][StringEnums.INFO]
            wid = self._creator_map[typ](description=key)
            wid.set_info(infos)
            wid.process_info()
            res.append(wid.layout())
            self._key_view_map[key] = wid
        btn = widgets.Button(description="log")
        btn.on_click(self._log_func)
        res.append(btn)
        self._rendered = widgets.VBox(res)
        return self._rendered
    def _log_func(self, btn):
        self._on_log_func(btn, self)
class LoggerButtonNameDecider:
    def set_info(self, info, index):
        self._info = info
        self._index = index
    def get_name(self):
        if len(self._indicesForName) == 0:
            return str(self._index)
        eky = self._indicesForName[0]
        if eky not in self._info:
            return str(self._index)
        content = self._info[eky][:30]
        if content.strip() == "":
            return str(self._index)
        return content
    def set_structure(self, struc):
        self._structure = struc
        self._indicesForName = list(filter(lambda x: struc[x]["type"] in [SupportedTypes.Text.name,
            SupportedTypes.LargeText.name, SupportedTypes.Options.name], struc))
class LoggerSearch(ISearch):
    def set_structure(self, dic):
        self._struct = dic
    def set_container(self, data):
        self._data = data
    def search(self, word, case = False, reg = False):
        if self._stype == "fields":
            return self.search_in_fields(word, reg, case)[::-1]
        elif self._stype == "word" and word != "":
            reg = True
            word = "\\b" + word + "\\b"
        elif self._stype == "concatenated":
            return self.concatenated_search(word, reg, case)[::-1]
        return self._search_in_index(word, reg, case, self._data)[::-1]
    def _search_in_index(self, word, reg, case, container):
        res = []
        for i in container:
            val = self._data[i]
            for ke in self._indices2search:
                if ke not in val and word == "":
                    res.append(i)
                    break
                if ke in val:
                    if ComparerDB.has(word, val[ke],case,reg):
                        res.append(i)
                        break
        return res
    def set_indices_to_search(self, indices):
        self._indices2search = indices
    def set_search_type(self, search_type):
        self._stype = search_type
    def search_in_fields(self, dicFields, reg, case):
        return self._search_in_fields(eval(dicFields), reg, case, self._data)
    def _search_in_fields(self, tosearch, reg, case, container):
        res  = []
        for i in container:
            val = self._data[i]
            found = True
            for ke in tosearch:
                if ke not in val:
                    found = True
                    break
                fieldContent = val[ke]
                found = found and ComparerDB.has(tosearch[ke], str(val[ke]),case,reg)
            if found:
                res.append(i)
        return res
    def date_filter(self, ):
        pass
    def concatenated_search(self, listOfDicFilters, reg, case):
        res = self._data
        tosearch = eval(listOfDicFilters)
        for val in tosearch:
            if isinstance(val, str):
                res = self._search_in_index(val, reg, case, res)
            elif isinstance(val, dict):
                res = self._search_in_fields(val, reg, case, res)
        return res
class LoggerDataCRUDController:
    def __init__(self):
        self._view_map ={}
        self.set_renderer(NewRenderer.creator)
        self.set_data_reader(SearchWithPagination.searchWithPagination(LoggerSearch(), self._btn_maker, self._result_btn_clicked))
        self.set_button_name_maker(LoggerButtonNameDecider())
        self.set_result_btn_click_func(self._default_res_btn_clicked_for_read)
        self._data_btn_key = None
        self._changed_tracker = 0
        self.set_search_func(self._def_search_btn_click)
    def _default_res_btn_clicked_for_create(self, btn, *param):
        is_empty = True
        nr = self._view_map[self._cur_btn.description]
        for ke in nr._key_view_map:
            cont = nr._key_view_map[ke]
            is_empty = is_empty and cont.is_empty()
        if is_empty:
            return
        vals = {}
        for ke in nr._key_view_map:
            cont = nr._key_view_map[ke]
            vals[ke] = cont.value()
        cotnent = nr._model.read(nr._name)
        kindex = 0
        if StringEnums.KEY_NR in cotnent:
            kindex = cotnent[StringEnums.KEY_NR]
        elif len(cotnent["data"]) != 0:
            kindex = max(cotnent["data"])
        cotnent[StringEnums.KEY_NR] = kindex + 1
        # cotnent[StringEnums.UUID] = CryptsDB.generateUniqueId()
        cotnent["data"][kindex] = vals
        nr._model.add(nr._name, cotnent, True)
        for ke in nr._key_view_map:
            cont = nr._key_view_map[ke]
            cont.clear()
        self._changed_tracker += 1
        self._update_reader_data()
    def _default_res_btn_clicked_for_read(self, btn, *param):
        HideableWidget.showIt(self._bsc.views.ldcv.out.get_layout())
        vals = self._data[btn._key] 
        structures = self._bsc._model.read(self._cur_btn.description)["structure"] 
        sortedKeys = sorted(structures,key = lambda x: structures[x]["order"])
        res = ""
        for ke in sortedKeys:
            if ke in vals:
                res +=  ke + ": " +  str(vals[ke]) + "\n"
                res += ("-"*40) + "\n"
        self._bsc.views.ldcv.out.clear()
        with self._bsc.views.ldcv.out._out:
            print(res)
    def _default_res_btn_clicked_for_update(self, btn, *param):
        self._default_render_func(btn)
        vals = self._data[btn._key]
        nr = self._view_map[self._cur_btn.description]
        for k in vals:
            val = vals[k]
            nr._key_view_map[k].set_value(val)
        nr.set_adder_func(self._overwrite_data)
        self._data_btn_key = btn._key
    def _default_res_btn_clicked_for_delete(self, btn, *param):
        self._bsc.views.ldcv.searchView.btn.layout.description = "confirm"
        self._bsc.views.ldcv.searchView.btn.set_clicked_func(self._delete_data_of_logger)
        self._data_btn_key = btn._key
    def _delete_data_of_logger(self, btn, *param):
        info=self._bsc._model.read(self._cur_btn.description)
        del info["data"][self._data_btn_key]
        self._bsc._model.add(self._cur_btn.description, info, True)
        self._changed_tracker += 1
        self._bsc.views.ldcv.searchView.btn.layout.description = "search"
        self._bsc.views.ldcv.searchView.btn.set_clicked_func(self._search_btn_click)
        self._update_reader_data()
        self._bsc.views.ldcv.searchView.btn.layout.click()
    def _overwrite_data(self, btn, *param):
        nr = self._view_map[self._cur_btn.description]
        vals = {}
        for ke in nr._key_view_map:
            cont = nr._key_view_map[ke]
            vals[ke] = cont.value()
        cotnent = nr._model.read(nr._name)
        cotnent["data"][self._data_btn_key]= vals
        nr._model.add(nr._name, cotnent, True)
        self._changed_tracker += 1
        for ke in nr._key_view_map:
            cont = nr._key_view_map[ke]
            cont.clear()
        self._update_reader_data()
        HideableWidget.hideIt(self._bsc.views.ldcv.out.get_layout())
    def set_data_reader(self, reader):
        self._reader = reader
    def set_basic_controller(self, basic_cont):
        self._bsc = basic_cont
    def set_up(self):
        self._bsc.views.ldcv.searchView.btn.set_clicked_func(self._search_btn_click)
        self._bsc.views.ldcv.opsWid.views.crudView.handlers.handle = self._ops_selected
    def _ops_selected(self, wid, *param):
        HideableWidget.showIt(self._bsc.views.ldcv.searchView.searchType)
        HideableWidget.showIt(self._bsc.views.ldcv.searchView.textWid)
        HideableWidget.showIt(self._bsc.views.ldcv.searchView.searchRow)
        val = self._bsc.views.ldcv.opsWid.views.crudView.outputs.layout.value
        self._bsc.views.ldcv.searchView.btn.set_clicked_func(self._search_btn_click)
        self._bsc.views.ldcv.searchView.btn.layout.description = "search"
        HideableWidget.hideIt(self._bsc.views.ldcv.searchView.couput.get_layout())
        HideableWidget.hideIt(self._bsc.views.ldcv.out.get_layout())
        if self._bsc.controllers.cdr.has_different_display(val):
            self._bsc.controllers.cdr.display(val)
        elif val == CRUPOps.CREATE.value:
            self._bsc.views.ldcv.searchView.btn.layout.description = "ok"
            self._bsc.views.ldcv.searchView.btn.set_clicked_func(self._default_render_func)
            HideableWidget.hideIt(self._bsc.views.ldcv.searchView.searchType)
            HideableWidget.hideIt(self._bsc.views.ldcv.searchView.textWid)
        elif val == CRUPOps.READ.value:
            HideableWidget.showIt(self._bsc.views.ldcv.searchView.couput.get_layout())
            self.set_result_btn_click_func(self._default_res_btn_clicked_for_read)
        elif val == CRUPOps.UPDATE.value:
            HideableWidget.showIt(self._bsc.views.ldcv.searchView.couput.get_layout())
            self.set_result_btn_click_func(self._default_res_btn_clicked_for_update)
        elif val == CRUPOps.DELETE.value:
            HideableWidget.showIt(self._bsc.views.ldcv.searchView.couput.get_layout())
            self.set_result_btn_click_func(self._default_res_btn_clicked_for_delete)
    def set_renderer(self, rendererCreator):
        self._rendererCreator = rendererCreator
    def _renderIt(self):
        if hasattr(self._cur_btn._parent.state, "updated"):
            if self._cur_btn._parent.state.updated:
                return True
        return self._cur_btn.description not in self._view_map
    def _default_render_func(self, btn, *param):
        if self._renderIt():
            lrc = self._rendererCreator()
            lrc.set_scope(self._bsc._scope)
            lrc.set_model(self._cur_btn.description, self._bsc._model)
            out = lrc.render()
            self._view_map[self._cur_btn.description] = lrc
            self._cur_btn._parent.state.updated = False
        else:
            out = self._view_map[self._cur_btn.description].render()
        self._view_map[self._cur_btn.description].set_adder_func(self._default_res_btn_clicked_for_create)
        HideableWidget.showIt(self._bsc.views.ldcv.out.get_layout())
        self._bsc.views.ldcv.out.display(out, True, True)
    def set_current_btn(self, btn):
        self._cur_btn = btn
        self._update_reader_data()
        self._name_maker.set_structure(self._structure)
        self._reader._engine.set_indices_to_search(self._name_maker._indicesForName)
    def _update_reader_data(self):
        infos = self._bsc._model.read(self._cur_btn.description)
        self._data = infos['data']
        self._structure = infos["structure"]
        self._reader._engine.set_container(self._data)
        self._reader._engine.set_structure(self._structure)
    def _btn_maker(self, des, func):
        self._name_maker.set_info(self._data[des], des)
        btn = SingleButtonController(description = self._name_maker.get_name(), layout= {"width":"auto", "max_width":"100px"})
        btn.set_clicked_func(func)
        btn.layout._key = des
        return btn.layout
    def set_result_btn_click_func(self, func):
        self._res_btn_click = func
    def _search_btn_click(self, btn):
        self._search_func(btn,self)
    def _def_search_btn_click(self, btn, *param):
        word = self._bsc.views.ldcv.searchView.textWid.value.strip()
        reg = False
        case = False
        ops = self._bsc.views.ldcv.searchView.searchType.value
        self._reader._engine.set_search_type(ops)
        if ops == "case":
            case = True
        elif ops == "reg":
            reg = True
        layo = self._reader.search(word, reg =reg, case=case)
        HideableWidget.showIt(self._bsc.views.ldcv.searchView.couput.get_layout())
        HideableWidget.hideIt(self._bsc.views.ldcv.out.get_layout())
        self._bsc.views.ldcv.searchView.couput.display(layo,True, True)
    def set_search_func(self, func):
        self._search_func = func
    def _result_btn_clicked(self, btn):
        self._bsc.debugLogDataBtn = btn
        self._res_btn_click(btn, self)
    def set_button_name_maker(self, name_maker):
        self._name_maker = name_maker
class CustomDisplayRenderer:
    def __init__(self):
        self._modifiers = {}
        self.set_load_func(self._def_load)
    def display(self, opsname):
        log_name = self._bsc.controllers.ldcc._cur_btn.description
        key = self._get_key(opsname)
        if key not in self._modifiers:
            self._modifiers[key] = self._load_func(opsname)
        displ = self._modifiers[key]
        cnt = self._bsc.controllers.ldcc
        displ.update_data(cnt._changed_tracker)
        HideableWidget.hideIt(self._bsc.views.ldcv.searchView.searchRow)
        HideableWidget.showIt(self._bsc.views.ldcv.searchView.couput.get_layout())
        self._bsc.views.ldcv.searchView.couput.display(displ.get_layout(), True, True)
    def set_load_func(self, loadfunc):
        self._load_func = loadfunc
    def _def_load(self, opsname):
        code_content = SerializationDB.readPickle(LibsDB.picklePath("codes"))["generic-logger"]
        res: IModifier = None
        key = self._get_key(opsname)
        content = code_content[key]
        exp = {}
        exec(content, None, exp)
        res = exp["res"]
        res.set_basic_controller(self._bsc)
        res.set_up()
        return res
    def has_different_display(self, opsname):
        ke = self._get_key(opsname)
        code_content = SerializationDB.readPickle(LibsDB.picklePath("codes"))["generic-logger"]
        return ke in code_content
    def _get_key(self, opsname):
        btnName = self._bsc.controllers.ldcc._cur_btn.description
        iid = self._bsc._model.read(btnName)["uuid"]
        key = f"{iid}{btnName}/{opsname}"
        return key
    def set_basic_controller(self, bsc):
        self._bsc = bsc
    def set_reader(self, reader):
        self._content_reader = reader
class DropdownFieldValueRestore:
    def __init__(self):
        self._values_map = {}
    def set_controller(self, bsc):
        self._bsc = bsc
    def set_up(self):
        self._bsc.views.ldcv.searchView.searchType.observe(self._dd_observed, "value")
        self._bsc.controllers.ldcc.set_search_func(self._new_search_func)
    def _new_search_func(self, btn, *param):
        ins = param[0]
        ins._def_search_btn_click(btn, ins)
        self._values_map[self._bsc.views.ldcv.searchView.searchType.value] = self._bsc.views.ldcv.searchView.textWid.value
    def _dd_observed(self, wid):
        key = self._bsc.views.ldcv.searchView.searchType.value
        if key in self._values_map:
            self._bsc.views.ldcv.searchView.textWid.value = self._values_map[key]
class Main:
    def generic_logger(filepath, scope=None, readPickleFile=True):
        bsc = BasicController()
        bsc.logger = LoggerSystem()
        glv = GLViewV2()
        glv.process.fieldCrudForm.views.fieldType.outputs.layout.options = list(map(lambda x: x.name, SupportedTypes))
        bsc.views.glv = glv
        pcrud = PickleCRUDOps()
        if readPickleFile:
            pcrud.set_pickle_file(filepath)
            pcrud.set_always_sync(True)
        bsc.set_model(pcrud)
        lsc = LoggerSearcherController()
        lsc.set_basic_controller(bsc)
        bsc.controllers.lsc = lsc
        lsc.set_up()
        if scope:
            bsc.set_scope(scope)
            glv.process.fieldCrudForm.process.keyValueComp.views.moreInfoLay.state.controller._basic.set_scope(scope)
        ldcv = LoggerDataCRUDOpsView()
        bsc.views.ldcv = ldcv
        ldcc = LoggerDataCRUDController()
        ldcc.set_basic_controller(bsc)
        bsc.controllers.ldcc = ldcc
        ldcc.set_up()
        cdr = CustomDisplayRenderer()
        cdr.set_basic_controller(bsc)
        bsc.controllers.cdr = cdr
        dfvr = DropdownFieldValueRestore()
        dfvr.set_controller(bsc)
        dfvr.set_up()
        bsc.controllers.dfvr = dfvr
        return bsc
