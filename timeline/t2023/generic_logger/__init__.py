import ipywidgets as widgets
import datetime
from modules.SearchSystem.modular import HideableWidget
from modules.Explorer.personalizedWidgets import CustomOutput
from timeline.t2023.advance_pickle_crud import Main as KeyValueAdderView
from timeline.t2023.searchSystem import Main as SearchWithPagination
from TimeDB import TimeDB
from PickleCRUDDB import PickleCRUDOps
from enum import Enum
from SearchSystem import ISearch
from ComparerDB import ComparerDB
from SerializationDB import SerializationDB
from LibsDB import LibsDB
from CryptsDB import CryptsDB
from timeline.t2023.generic_logger.components import TextInput, TextAreaInput, BooleanOptionInput, DropdownInput, DateInput, TimeInput, DateTimeInput, MultipleSelect, KeyValueInput, SingleButtonController
from basic import BasicController, NameSpace, LoggerSystem

from timeline.t2023.generic_logger.UIComponents import GLViewV2
class IModifier:
    def set_basic_controller(self, bsc):
        pass
    def get_layout(self):
        pass
    def set_up(self):
        pass
    def update_data(self, version: int):
        pass
class SearchView:
    def __init__(self):
        self.textWid = widgets.Text(placeholder = "word", layout={"width":"auto"})
        self.isRegWid = widgets.Checkbox(description="is reg", indent =False, layout={"width":"auto"})
        self.isCase = widgets.Checkbox(description="case", indent =False, layout={"width":"auto"})
        self.btn = SingleButtonController(description="search", layout={"width":"auto"})
        self.couput = CustomOutput()
        self.btnOutput = CustomOutput()
        self.searchRow = widgets.HBox([self.textWid, self.isRegWid, self.isCase, self.btn.layout])
        self.layout = widgets.VBox([self.searchRow,self.couput.get_layout(), self.btnOutput.get_layout()])
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
class CrudView:
    def __init__(self):
        design=widgets.HTML("""
            <style>
                .RadioButtons div {
                    flex-flow: row wrap;
                    max-width: 90px;
                    overflow:auto;
                }
                .RadioButtons input{
                    border-radius: 10px;
                    padding: 8px;
                    margin-right: 2px;
                }
                .RadioButtons label{
                    width: 30px;
                    border-radius: 10px;
                    padding: 2px;
                    margin : 1px;
                    box-shadow: 0 0 8px 3px rgba(0, 0, 0, 0.1);
                }
                .RadioButtons{
                    width: auto;
                    min-width: 90px;
                }
                .widget-box{
                    width: fit-content;
                    overflow: hidden;
                }
                .widget-textarea textarea, .jupyter-widget-textarea textarea {
                    min-height: 120px;
                }
            </style>""")
        self.wid = widgets.RadioButtons( options=['r', 'c', 'u', 'd'])
        self.wid.add_class("RadioButtons")
        self.layout = widgets.HBox([self.wid, design])
        self.wid.observe(self._selected, names=["value"])
        self.set_select_func(self._default_on_selected)
    def _default_on_selected(self, infos, *param):
        pass
    def set_select_func(self, func):
        self._func = func
    def _selected(self, infos):
        self._func(infos, self)
class FieldInfoView:
    def __init__(self):
        self.textWid = widgets.Text(placeholder = "field name", layout={"width":"auto"})
        self.typeOfWid = widgets.Dropdown(options=[], layout =widgets.Layout(width="auto"))
        self.checkBox = widgets.Checkbox(description="add more info", indent =False, layout={"width":"auto"})
        self.displayInfoWid = widgets.Textarea(disabled=True,layout= widgets.Layout(height='auto'))
        self.editBtn = widgets.Button(icon="edit", layout={"width":"auto"}, button_style="success")
        self.deleteBtn = widgets.Button(icon="trash", layout={"width":"auto"}, button_style="danger")
        self.layout = widgets.HBox([self.textWid, self.typeOfWid, self.checkBox, self.displayInfoWid, self.editBtn, self.deleteBtn], disabled=True)
class GLView:
    def __init__(self):
        self.fieldInfo = NameSpace()
        self.loggerInfo = NameSpace()
        self.moreInfo = KeyValueAdderView.keyValueCrud({})
        self.logSearch = SearchView()
        self.crudOps = NameSpace()
        self.crudOps.options = CrudView()
        self.crudOps.layout = widgets.HBox([self.crudOps.options.layout, self.logSearch.layout])
        self.loggerInfo.out = widgets.HTML()
        self.loggerInfo.nameWid = widgets.Text(description="logger name")
        self.loggerInfo.createBtn = SingleButtonController(description="create logger")
        self.fieldInfo.listWid = widgets.VBox()
        self.fieldInfo.textWid = widgets.Text(placeholder = "field name", layout={"width":"auto"})
        self.fieldInfo.typeOfWid = widgets.Dropdown(options=[], layout =widgets.Layout(width="auto"))
        self.fieldInfo.checkBox = widgets.Checkbox(description="add more info", indent =False, layout={"width":"auto"})
        self.fieldInfo.fieldAddBtn = SingleButtonController(icon="plus-circle", layout={"width":"auto"})
        self.addRowLay = widgets.HBox([self.fieldInfo.textWid, self.fieldInfo.typeOfWid,self.fieldInfo.checkBox, self.fieldInfo.fieldAddBtn.layout, self.moreInfo[0]])
        self.crudopsWid = widgets.VBox([self.loggerInfo.nameWid, self.fieldInfo.listWid, self.addRowLay, self.loggerInfo.createBtn.layout, self.loggerInfo.out])
        self.out = CustomOutput()
        self.layout = widgets.VBox([self.crudOps.layout,self.crudopsWid, self.out.get_layout()])
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
class FieldsManager:
    def __init__(self):
        self.reset()
        self._order_number = 0
    def reset(self):
        self._fields = {}
        self._fields_view_map = {}
    def add_field(self, val, typ, info, order =None):
        if order is None:
            order = self._order_number
            self._order_number += 1
        self._fields[val]= {StringEnums.TYPE: typ, StringEnums.INFO: info, StringEnums.ORDER: order}
        fvi = FieldInfoView()
        fvi.checkBox.disabled = True
        fvi.textWid.disabled = True
        fvi.typeOfWid.disabled = True
        fvi.typeOfWid.options = list(map(lambda x: x.name, SupportedTypes))
        fvi.displayInfoWid.disabled = True
        fvi.textWid.value = val
        fvi.typeOfWid.value = typ
        self._fields_view_map[val] = fvi
        return fvi
    def delete_field(self, fieldKey):
        del self._fields[fieldKey]
        del self._fields_view_map[fieldKey]
    def update_field(self, oldFieldKey, newKey, newType, newInfo):
        order = self._fields[oldFieldKey][StringEnums.ORDER]
        self.delete_field(oldFieldKey)
        return self.add_field(newKey, newType, newInfo, order)
    def get_ordered_fields(self):
        return {key: self._fields[key] for key in sorted(self._fields, key= lambda y: self._fields[y]['order'])}
    def read_field(self, fieldKey):
        return self._fields[fieldKey]
    def get_layout(self):
        return [self._fields_view_map[ta].layout for ta in self.get_ordered_fields()]
class GLController:
    def __init__(self):
        self._override = False
        self._key_val = {}
        self.set_field_manager(FieldsManager())
    def set_field_manager(self, mng):
        self._fields_manager = mng
    def set_basic_controller(self, bsc):
        self._bsc = bsc
    def set_up(self):
        HideableWidget.hideIt(self._bsc.views.glv.crudopsWid)
        HideableWidget.hideIt(self._bsc.views.glv.moreInfo[0])
        self._bsc.views.glv.fieldInfo.typeOfWid.options = list(map(lambda x: x.name, SupportedTypes))
        self._bsc.views.glv.fieldInfo.checkBox.observe(self._showKeyValAddOps, names="value")
        self._bsc.views.glv.fieldInfo.fieldAddBtn.set_clicked_func(self._add_clicked)
        self._bsc.views.glv.loggerInfo.createBtn.set_clicked_func(self._logger_creator)
        self._update_keys(self._key_val)
    def _showKeyValAddOps(self, wd):
        HideableWidget.hideIt(self._bsc.views.glv.moreInfo[0])
        if self._bsc.views.glv.fieldInfo.checkBox.value:
            HideableWidget.showIt(self._bsc.views.glv.moreInfo[0])
            if self._key_val:
                self._update_keys(self._key_val)
    def _add_clicked(self, btn):
        val = self._bsc.views.glv.fieldInfo.textWid.value.strip()
        typ = self._bsc.views.glv.fieldInfo.typeOfWid.value
        if not val:
            self._info("please add field name", True)
            return
        if not typ:
            self._info("please select a type", True)
            return
        self._bsc.views.glv.fieldInfo.textWid.value = ""
        self._add_field(val, typ)
        self._override = False
    def _add_field(self, val, typ):
        if val in self._fields_manager.get_ordered_fields() and not self._override:
            self._info("Title already exists")
            return
        if self._override:
            fvi = self._fields_manager.update_field(self._old_key, val, typ, self._key_val)
        else:
            fvi = self._fields_manager.add_field(val, typ, self._key_val)
        HideableWidget.hideIt(fvi.displayInfoWid)
        fvi.editBtn.on_click(lambda x: self._editing_field(fvi))
        fvi.deleteBtn.on_click(lambda x: self._delete_field(fvi))
        self._update_keys({})
        self._bsc.views.glv.fieldInfo.listWid.children = self._fields_manager.get_layout()
    def _editing_field(self, field):
        self._override = True
        self._old_key = field.textWid.value
        self._bsc.views.glv.fieldInfo.textWid.value = field.textWid.value
        self._bsc.views.glv.fieldInfo.typeOfWid.value = field.typeOfWid.value
        fieldContent = self._fields_manager.read_field(field.textWid.value)
        self._update_keys(fieldContent['info'])
    def _delete_field(self, field):
        self._fields_manager.delete_field(field.textWid.value)
        self._bsc.views.glv.fieldInfo.listWid.children = self._fields_manager.get_layout()
    def _info(self, msg, isWarning = False):
        if isWarning:
            self._bsc.views.glv.loggerInfo.out.value = f"<font face='comic sans ms' color ='red'>{msg}</font>"
        else:
            self._bsc.views.glv.loggerInfo.out.value = f"<font face='comic sans ms' color ='blue'>{msg}</font>"
        def disapp():
            self._bsc.views.glv.loggerInfo.out.value=""
        TimeDB.setTimer().oneTimeTimer(5, disapp)
    def _logger_creator(self, btn):
        val = self._bsc.views.glv.loggerInfo.nameWid.value.strip()
        if not val:
            self._info("give a logger name", True)
            return
        if len(self._fields_manager.get_ordered_fields())== 0:
            self._info("add some fields", True)
            return
        self._info("adding logger")
        self._bsc._model.add(val, {'structure': self._fields_manager.get_ordered_fields(), 'data': {}, 
            StringEnums.UUID: CryptsDB.generateUniqueId()})
        self.reset()
    def reset(self):
        self._override = False
        self._fields_manager.reset()
        self._update_keys({})
        self._bsc.views.glv.loggerInfo.nameWid.value = ""
        self._bsc.views.glv.fieldInfo.listWid.children = self._fields_manager.get_layout()
    def _update_keys(self, keys):
        self._key_val = keys
        cnt = self._bsc.views.glv.moreInfo[1]
        cnt._basic._model.set_dictionary(self._key_val)
        cnt._update_keys()
class CRUPOps(Enum):
    READ= "r"
    CREATE= "c"
    UPDATE= "u"
    DELETE = "d"
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
        self._bsc.views.glv.logSearch.btn.set_clicked_func(self._on_search_clicked)
        self._bsc.views.glv.crudOps.options.set_select_func(self._ops_selected)
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
        word = self._bsc.views.glv.logSearch.textWid.value.strip()
        reg = self._bsc.views.glv.logSearch.isRegWid.value
        case = self._bsc.views.glv.logSearch.isCase.value
        self._tasks_names = self._active_loggers_keys()
        self._searcher._engine.set_container(self._tasks_names)
        layo = self._searcher.search(word, reg =reg, case=case)
        self._bsc.views.glv.logSearch.couput.display(layo,True, True)
    def _btn_click_func(self, btn):
        self._bsc.debug = btn
        self._clicked_func(btn, self)
    def _opIt(self, btn, *param):
        self._bsc.views.glv.out.display(self._bsc.views.ldcv.layout, True, True)
        self._bsc.controllers.ldcc.set_current_btn(btn)
        self._bsc.views.ldcv.searchView.couput.clear()
        self._bsc.controllers.ldcc._ops_selected(None)
    def _delete_logger_intermediate(self, btn, *param):
        self._clicked = btn.description
        self._bsc.views.glv.logSearch.btn.layout.description = "confirm"
        self._bsc.views.glv.logSearch.btn.set_clicked_func(self._delete_logger)
    def _delete_logger(self, btn, *param):
        taskName = self._clicked
        self._bsc.views.glv.logSearch.btn.set_clicked_func(self._on_search_clicked)
        if taskName:
            self._bsc.views.glv.logSearch.btn.layout.description = "search"
            st = self._bsc._model.read(taskName)
            st["status"] = "deleted"
            self._bsc._model.add(taskName, st, True)
            self._clicked = None
    def _default_update_logger(self, btn, *param):  
        self._bsc.controllers.glc.reset()
        st = self._bsc._model.read(btn.description)
        self._bsc.views.glv.loggerInfo.nameWid.value = btn.description
        struc = st["structure"]
        for k in struc:
            typ = struc[k]['type']
            self._bsc.controllers.glc._key_val = struc[k]['info']
            self._bsc.controllers.glc._add_field(k, typ)
        HideableWidget.showIt(self._bsc.views.glv.crudopsWid)
    def _btn_maker(self, des, func):
        btn = widgets.Button(description = self._tasks_names[des], layout= {"width":"auto"})
        btn.on_click(func)
        return btn
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
        self._bsc.views.glv.logSearch.btn.set_clicked_func(self._on_search_clicked)
        val = self._bsc.views.glv.crudOps.options.wid.value
        HideableWidget.hideIt(self._bsc.views.glv.crudopsWid)
        HideableWidget.showIt(self._bsc.views.glv.logSearch.layout)
        self._bsc.views.glv.out.clear()
        if val == CRUPOps.READ.value:
            self.set_button_click_func(self._opIt)
        elif val == CRUPOps.UPDATE.value:
            self.set_button_click_func(self._default_update_logger)
            self._bsc.views.glv.loggerInfo.createBtn.set_clicked_func(self._update_logger_structure)
        elif val == CRUPOps.DELETE.value:
            self.set_button_click_func(self._delete_logger_intermediate)
        elif val == CRUPOps.CREATE.value:
            self._bsc.views.glv.loggerInfo.createBtn.set_clicked_func(self._bsc.controllers.glc._logger_creator)
            HideableWidget.hideIt(self._bsc.views.glv.logSearch.layout)
            HideableWidget.showIt(self._bsc.views.glv.crudopsWid)
            self._bsc.controllers.glc.reset()
    def _update_logger_structure(self, btn):
        val = self._bsc.views.glv.loggerInfo.nameWid.value.strip()
        if not val:
            self._bsc.controllers.glc._info("give a logger name", True)
            return
        if len(self._bsc.controllers.glc._fields_manager.get_ordered_fields())== 0:
            self._bsc.controllers.glc._info("add some fields", True)
            return
        self._bsc.controllers.glc._info("updating logger")
        content = self._bsc._model.read(val)
        content['structure'] = self._bsc.controllers.glc._fields_manager.get_ordered_fields()
        self._bsc._model.add(val, content, True)
        self._bsc.controllers.glc.reset()
        HideableWidget.hideIt(self._bsc.views.glv.crudopsWid)
    def set_logged_data_crud_operator(self, oper):
        self._bsc.controllers.ldcc = oper
class LoggerDataCRUDOpsView:
    def __init__(self):
        self.opsWid = CrudView()
        self.searchView = AdvanceSearchView()
        self.out = CustomOutput()
        self.layout = widgets.VBox([widgets.HBox([self.opsWid.layout, self.searchView.layout]), self.out.get_layout()])
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
            return self.search_in_fields(word, reg, case)
        elif self._stype == "word" and word != "":
            reg = True
            word = "\\b" + word + "\\b"
        elif self._stype == "concatenated":
            return self.concatenated_search(word, reg, case)
        return self._search_in_index(word, reg, case, self._data)
    def _search_in_index(self, word, reg, case, container):
        res = []
        for i in container:
            val = self._data[i]
            for ke in self._indices2search:
                if ke not in val and word == "":
                    res.append(i)
                    break
                if ComparerDB.has(word, val[ke],case,reg):
                    res.append(i)
                    break
        return res[::-1]
    def set_indices_to_search(self, indices):
        self._indices2search = indices
    def set_search_type(self, search_type):
        self._stype = search_type
    def search_in_fields(self, dicFields, reg, case):
        asdndn = {}
        exec(f"dfsdfda={dicFields}",None,asdndn)
        tosearch = asdndn['dfsdfda']
        return self._search_in_fields(tosearch, reg, case, self._data)
    def _search_in_fields(self, tosearch, reg, case, container):
        res  = []
        for i in container:
            val = self._data[i]
            for ke in tosearch:
                if ke not in val:
                    res.append(i)
                    break
                fieldContent = val[ke]
                if ComparerDB.has(tosearch[ke], str(val[ke]),case,reg):
                    res.append(i)
                    break
        return res
    def date_filter(self, ):
        pass
    def concatenated_search(self, listOfDicFilters, reg, case):
        res = self._data
        asdndn = {}
        exec(f"dfsdfda={listOfDicFilters}",None,asdndn)
        tosearch = asdndn['dfsdfda']
        for val in tosearch:
            if type(val) == str:
                res = self._search_in_index(val, reg, case, res)
            elif type(val) == dict:
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
        res = ""
        for ke  in vals:
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
        self._bsc.views.ldcv.opsWid.set_select_func(self._ops_selected)
    def _ops_selected(self, wid, *param):
        HideableWidget.showIt(self._bsc.views.ldcv.searchView.searchType)
        HideableWidget.showIt(self._bsc.views.ldcv.searchView.textWid)
        HideableWidget.showIt(self._bsc.views.ldcv.searchView.searchRow)
        val = self._bsc.views.ldcv.opsWid.wid.value
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
    def _default_render_func(self, btn, *param):
        if self._cur_btn.description not in self._view_map:
            lrc = self._rendererCreator()
            lrc.set_scope(self._bsc._scope)
            lrc.set_model(self._cur_btn.description, self._bsc._model)
            out = lrc.render()
            self._view_map[self._cur_btn.description] = lrc
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
        bsc.views.glv = glv
        glc = GLController()
        glc.set_basic_controller(bsc)
        bsc.controllers.glc = glc
        glc.set_up()
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
            glv.moreInfo[1]._basic.set_scope(scope)
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
        return glv.layout, bsc