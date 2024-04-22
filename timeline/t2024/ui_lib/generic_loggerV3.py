from timeline.t2024.tailwind_react_tool import addToNameSpace
from timeline.t2024.ui_lib.IpyComponents import IpywidgetsComponentsEnum, Utils, ComponentsLib
import math
from timeline.t2024.experiments.namespace_generic_logger import DictionaryCRUD
from CryptsDB import CryptsDB
from basic import NameSpace
def Constants():
    constants = NameSpace()
    constants.strings = NameSpace()
    constants.strings.structure = "structure"
    constants.strings.uuid = "uuid"
    constants.strings.key_index = "key-index"
    constants.strings.global_str = "globals"
    constants.strings.data = "data"
    constants.lists = NameSpace()
    constants.lists.loc_tables2uuid = ['global', 'table-name-to-uuid']
    constants.lists.loc_tables = ['tables-info']
    constants.lists.loc_tables_data = ['table_data']
    return constants
class ModelFuncsDictionary:
    def __init__(self):
        self.set_model(DictionaryCRUD())
        self.set_constants(Constants())
    def set_model(self, model):
        self.model = model
    def set_constants(self, constants):
        self.constants = constants
    def loggerData_create(self, tableName, key, value):
        uuid = self.logger_get_uuid(tableName)
        self.global_meta_create(key, value, loc=self.constants.lists.loc_tables_data + [uuid])
    def loggerData_delete(self, tableName, key):
        uuid = self.logger_get_uuid(tableName)
        self.global_meta_delete(key, loc=self.constants.lists.loc_tables_data + [uuid])
    def loggerData_update(self, tableName, key, new_val):
        uuid = self.logger_get_uuid(tableName)
        self.global_meta_update(key, new_val, loc=self.constants.lists.loc_tables_data + [uuid])
    def loggerData_read(self, tableName, key):
        uuid = self.logger_get_uuid(tableName)
        return self.global_meta_read(key, loc=self.constants.lists.loc_tables_data + [uuid])
    def loggerData_readAll(self, tableName):
        uuid = self.logger_get_uuid(tableName)
        return self.global_meta_read(uuid, loc=self.constants.lists.loc_tables_data)
    def metaInfo_create(self, tableName, key, value):
        uuid = self.logger_get_uuid(tableName)
        self.global_meta_create(key, value, loc=self.constants.lists.loc_tables + [uuid])
    def metaInfo_delete(self, tableName, key):
        uuid = self.logger_get_uuid(tableName)
        self.global_meta_delete(key, loc=self.constants.lists.loc_tables + [uuid])
    def metaInfo_update(self, tableName, key, old_value, new_value):
        uuid = self.logger_get_uuid(tableName)
        self.global_meta_update(key, new_value, loc=self.constants.lists.loc_tables + [uuid])
    def metaInfo_read(self, tableName, key):
        uuid = self.logger_get_uuid(tableName)
        return self.global_meta_read(key, loc=self.constants.lists.loc_tables + [uuid])
    def metaInfo_readAll(self, tableName):
        uuid = self.logger_get_uuid(tableName)
        return self.global_meta_read(name, uuid, loc=self.constants.lists.loc_tables + [uuid])
    def metaInfo_exists(self,tableName, key):
        uuid = self.logger_get_uuid(tableName)
        return self.global_meta_exists(key, loc=self.constants.lists.loc_tables + [uuid])
    def logger_create(self, name):
        if not self.logger_exists(name):
            uuid = CryptsDB.generateUniqueId()
            self.global_meta_create(name, uuid, loc=self.constants.lists.loc_tables2uuid)
            self.global_meta_create(uuid, {"name": name}, loc=self.constants.lists.loc_tables)
    def logger_delete(self, name):
        if self.logger_exists(name):
            uuid = self.global_meta_read(name, loc=self.constants.lists.loc_tables2uuid)
            self.global_meta_delete(uuid, loc=self.constants.lists.loc_tables)
            self.global_meta_delete(name, loc=self.constants.lists.loc_tables2uuid)
    def logger_update(self, old_name, newname):
        oldExists = self.logger_exists(old_name)
        newDoesNotExist = not self.logger_exists(newname)
        if oldExists and newDoesNotExist:
            uuid = self.global_meta_read(old_name, loc=self.constants.lists.loc_tables2uuid)
            tableInfos = self.global_meta_read(uuid, loc=self.constants.lists.loc_tables)
            tableInfos["name"]= newname
            self.global_meta_delete(old_name, loc=self.constants.lists.loc_tables2uuid)
            self.global_meta_update(uuid, tableInfos, loc=self.constants.lists.loc_tables)
            self.global_meta_create(newname, uuid, loc=self.constants.lists.loc_tables2uuid)
    def logger_exists(self, name):
        return self.global_meta_exists(name, loc=self.constants.lists.loc_tables2uuid)
    def logger_get_uuid(self, name):
        return self.global_meta_read(name, loc=self.constants.lists.loc_tables2uuid)
    def logger_read(self, name):
        uuid = self.global_meta_read(name, loc=self.constants.lists.loc_tables2uuid)
        return self.global_meta_read(uuid, loc=self.constants.lists.loc_tables)
    def logger_readAll(self):
        return self.global_meta_readAll(loc=self.constants.lists.loc_tables)
    def global_meta_create(self, key, value,loc = None):
        if loc is None:
            loc = []
        self.model.set_baseloc(loc)
        self.model.write(key, value)
    def global_meta_delete(self, key, loc=None):
        if loc is None:
            loc = []
        self.model.set_baseloc(loc)
        self.model.delete(key)
    def global_meta_update(self, key, value, loc =None):
        if loc is None:
            loc = []
        self.model.set_baseloc(loc)
        self.model.write(key, value, True)
    def global_meta_read(self, key, loc = None):
        if loc is None:
            loc = []
        self.model.set_baseloc(loc)
        return self.model.read(key)
    def global_meta_exists(self, key, loc = None):
        if loc is None:
            loc = []
        self.model.set_baseloc(loc)
        return self.model.exists(key)
    def global_meta_readAll(self, loc = None):
        if loc is None:
            loc = []
        self.model.set_baseloc(loc)
        return self.model.readAll()
class ControllerModel:
    def __init__(self):
        self.set_model(ModelFuncsDictionary())
    def read_structure(self, tableName = None):
        if tableName is None:
            tableName = self.get_table_name()
        return self.model.metaInfo_read(tableName, self.model.constants.strings.structure)
    def add_attribute(self, fieldName, value):
        tableName = self.get_table_name()
        self.model.metaInfo_create(tableName, fieldName, value)
    def read_field(self, fieldName):
        tableName = self.get_table_name()
        return self.model.metaInfo_read(tableName, fieldName)
    def set_table_name(self, name):
        self._table_name = name
    def get_table_name(self):
        return self._table_name
    def delete_attribute(self, fieldName):
        tableName = self.get_table_name()
        self.model.metaInfo_delete(tableName, fieldName)
    def create_table(self, name, fields):
        if self.model.logger_exists(name):
            self.update_structure(name, fields)
            return
        self.model.logger_create(name)
        self.model.metaInfo_create(name, self.model.constants.strings.structure, fields)
    def update_structure(self, name, fields):
        self.model.metaInfo_update(name, self.model.constants.strings.structure, fields)
    def table_exists(self, name):
        return self.model.logger_exists(name)
    def read_table_names(self):
        tables = self.model.logger_readAll()
        res = []
        for uuid in tables:
            res.append(tables[uuid]["name"])
        return res
    def delete_table_name(self, table_name):
        self.model.logger_delete(table_name)
    def logger_data_add(self, data):
        tableName = self.get_table_name()
        if not self.model.metaInfo_exists(tableName, self.model.constants.strings.key_index):
            self.model.metaInfo_create(tableName, self.model.constants.strings.key_index, 0)
        idd = self.model.metaInfo_read(tableName, self.model.constants.strings.key_index)
        self.model.loggerData_create(tableName, idd, data)
    def logger_data_read(self, idd):
        tableName = self.get_table_name()
        return self.model.loggerData_read(tableName, idd)
    def logger_data_delete(self, idd):
        tableName = self.get_table_name()
        self.model.loggerData_delete(tableName, idd)
    def logger_data_update(self, idd, new_val):
        tableName = self.get_table_name()
        self.model.loggerData_update(tableName, idd, new_val)
    def logger_data_readAll(self):
        tableName = self.get_table_name()
        return self.model.loggerData_readAll(tableName)
    def set_model(self, model):
        self.model = model
def SearchComponent():
    def _searchComp(state):
        inputText = Utils.get_comp({"placeholder": "search word or reg"}, IpywidgetsComponentsEnum.Text, bind=False)
        searchType = Utils.get_comp({"options":["any", "reg", "case", "word", "concatenated", "fields"]}, IpywidgetsComponentsEnum.Dropdown,
                                    bind=False, className="w-auto")
        searchBtn = Utils.get_comp({"description": "search"}, IpywidgetsComponentsEnum.Button, className = "w-auto br-5px")
        layout = Utils.container([inputText, searchType, searchBtn], className="w-100")
        addToNameSpace(state, locals(), ["state"])
    state = NameSpace()
    _searchComp(state)
    return state
def RadioButtons():
    def _menus(state):
        radioBtns = Utils.get_comp({"options": "rcud"}, IpywidgetsComponentsEnum.RadioButtons, bind =False, className = "RadioButtons")
        radioBtns.outputs.layout
        addToNameSpace(state, locals(), ["state"])
    rb = NameSpace()
    _menus(rb)
    return rb
def Menus():
    def _menus(state):
        createBtn = Utils.get_comp({"description":"create"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
        deleteBtn = Utils.get_comp({"description":"delete"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
        updateBtn = Utils.get_comp({"description":"update"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
        readBtn = Utils.get_comp({"description":"read"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
        container = Utils.container([readBtn, createBtn, deleteBtn, updateBtn], className="flex flex-column w-fc")
        addToNameSpace(state, locals(), ["state"])
    menusState = NameSpace()
    _menus(menusState)
    return menusState
def Pagination():
    def _pagination(state):
        btnsContainer = Utils.container([Utils.get_comp({"description":str(i+1)}, IpywidgetsComponentsEnum.Button,
                                                        className ="w-auto bg-color-unset color-light") for i in range(5)])
        label = Utils.get_comp({"value":"max"}, IpywidgetsComponentsEnum.Label, className ="w-auto", bind =False)
        pageInput = Utils.get_comp({"min":1, "max": 5}, IpywidgetsComponentsEnum.BoundedIntText, className ="w-auto", bind =False)
        goBtn = Utils.get_comp({"description":"go"}, IpywidgetsComponentsEnum.Button, className ="w-auto bg-color-unset color-light")
        prev = Utils.get_comp({"description":"prev"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
        nextBtn = Utils.get_comp({"description":"next"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
        layout = Utils.container([prev, btnsContainer,nextBtn, label, pageInput, goBtn])
        def selected(wid):
            state.handlers.selectWithVal(wid.description)
        def selectWithVal(des):
            update_buttons_description(int(des))
            for btn in btnsContainer.outputs.renderedStates:
                if btn.outputs.layout.description == des:
                    state.vals.currentBtnSelected = btn
                    btn.outputs.layout.add_class("bg-blue-light")
                    btn.outputs.layout.add_class("color-white")
                else:
                    btn.outputs.layout.remove_class("bg-blue-light")
                    btn.outputs.layout.remove_class("color-white")
        def goBtnFunc(wid):
            state.handlers.selectWithVal(str(pageInput.outputs.layout.value))
        def prev_clicked(info):
            val = int(state.vals.currentBtnSelected.outputs.layout.description)
            if val == 1:
                val = pageInput.outputs.layout.max
            else:
                val -= 1
            state.handlers.selectWithVal(str(val))
        def next_clicked(info):
            val = int(state.vals.currentBtnSelected.outputs.layout.description)
            if val == pageInput.outputs.layout.max:
                val = 1
            else:
                val += 1
            state.handlers.selectWithVal(str(val))
        def update_buttons_description(nr):
            pagesNr = windowCalc(nr, state.process.maxPageSize)
            for i, btn in enumerate(btnsContainer.outputs.renderedStates):
                if i < len(pagesNr):
                    btn.outputs.layout.description = str(pagesNr[i])
                    btn.show()
                else:
                    btn.hide()
        def windowCalc(n, total):
            t = total
            if n < 3:
                res = range(6)
            elif n > (t-3):
                res = range(t-4, t+1)
            else:
                res = range(n-2, n+3)
            return list(filter(lambda x: x > 0 and x < t+1, res))

        def update_total_pages(total):
            state.process.maxPageSize = total
            state.handlers.update_buttons_description(int(state.vals.currentBtnSelected.outputs.layout.description))
            if state.process.maxPageSize != 0:
                pageInput.outputs.layout.max = state.process.maxPageSize
            label.outputs.layout.value = str(state.process.maxPageSize)
            if total <= 1:
                nextBtn.hide()
                prev.hide()
            else:
                nextBtn.show()
                prev.show()
            if total < 6:
                pageInput.hide()
                goBtn.hide()
                label.hide()
            else:
                pageInput.show()
                goBtn.show()
                label.show()

        maxPageSize = 3
        state.vals = NameSpace()

        btnsContainer.handlers.handle = selected
        btnsContainer.handlers.defs.handle = selected
        goBtn.handlers.handle = goBtnFunc
        goBtn.handlers.defs.handle = goBtnFunc
        nextBtn.handlers.handle = next_clicked
        nextBtn.handlers.defs.handle = next_clicked
        prev.handlers.handle = prev_clicked
        prev.handlers.defs.handle = prev_clicked
        addToNameSpace(state, locals(), ["state", "addToNameSpace"])
        selectWithVal("1")
        update_total_pages(maxPageSize)
    state = NameSpace()
    _pagination(state)
    return state
def ResultDisplayers():
    def _resultDisplayers(state):
        data = []
        sizeCount = 20
        pageNr = 1
        totalPagesNr = 3
        def name_getter(ele):
            return "name"
        def set_size_count(countNr):
            state.process.sizeCount = countNr
            state.process.totalPagesNr = math.ceil(len(state.process.data)/countNr)
            state.handlers.render()
        def set_results(results, newPageNr = 1, reverseIt = True):
            state.process.data = results
            if reverseIt:
                state.process.data = results[::-1]
            state.process.totalPagesNr = math.ceil(len(state.process.data)/state.process.sizeCount)
            state.process.pageNr = newPageNr
            state.handlers.render()
        def btnMaker(ele):
            return Utils.get_comp({"description": state.handlers.name_getter(ele)}, IpywidgetsComponentsEnum.Button, className ="w-auto")
        def initializeButtons():
            state.views.btns.outputs.renderedStates.clear()
            for i in range(state.process.sizeCount):
                state.views.btns.append(state.handlers.btnMaker(""))
        def render():
            if len(state.views.btns.outputs.renderedStates) == 0:
                state.handlers.initializeButtons()
            if state.process.totalPagesNr == 1:
                state.process.paginations.views.layout.hide()
            else:
                state.process.paginations.views.layout.show()
            data = state.handlers.data_for_currentPage()
            for i in range(state.process.sizeCount):
                btn = state.views.btns.outputs.renderedStates[i]
                if i < len(data):
                    state.handlers.button_state_update(btn, data[i])
                    btn.show()
                else:
                    btn.hide()
            state.process.paginations.handlers.update_total_pages(state.process.totalPagesNr)
        def button_state_update(btn, info):
            index, ele = info
            btn.outputs.layout.description = state.handlers.name_getter(ele)
            btn.state.index = index
        def data_for_currentPage():
            res = []
            fromStart = state.process.sizeCount * (state.process.pageNr-1)
            till = state.process.sizeCount * (state.process.pageNr)
            for i in range(fromStart, till):
                if i >= len(state.process.data):
                    break
                res.append((i, state.process.data[i]))
            return res
        def page_changed(valStr):
            state.process.pageNr = int(valStr)
            state.process.paginations.handlers.defs.selectWithVal(valStr)
            state.handlers.render()
        btns  = Utils.container([], className="flex flex-wrap")
        paginations = Pagination()
        paginations.handlers.selectWithVal = page_changed
        layout = Utils.container([paginations.views.layout, btns], className="flex flex-column")
        addToNameSpace(state, locals(), ["state", "addToNameSpace"])
    state = NameSpace()
    _resultDisplayers(state)
    return state
def TabComponent():
    def tabElement(state):
        tabTitle = Utils.get_comp({"description": "tab 1"}, IpywidgetsComponentsEnum.Button, className="flex")
        closeBtn = Utils.get_comp({"description": "x"}, IpywidgetsComponentsEnum.Button, className="w-auto bg-color-unset")
        tabElement = Utils.container([tabTitle, closeBtn], className = "bg-blue-light w-fit br-5px p0")
        assert tabTitle.inputs.parent == tabElement, "after container"
        tabElement.handlers.handle = lambda x: None
        addToNameSpace(state, locals(), ["state", "addToNameSpace"])
        assert tabTitle.inputs.parent == tabElement, "after adding to namespace"
    state = NameSpace()
    tabElement(state)
    return state
def TabBar():
    def _tabBar(state):
        tabElementCount = 5
        tabs = []
        for i in range(tabElementCount):
            tabCom = TabComponent()
            tabCom.views.tabElement.state.index = i
            tabCom.views.tabTitle.outputs.layout.description = "tab " + str(i+1)
            tabs.append(tabCom.views.tabElement)
        tabbar = Utils.container(tabs)

        def tabClicked(wid):
            print("opening")
        def closed(wid):
            curIndex =wid._parent.inputs.parent.state.index
            state.views.tabbar.outputs.renderedStates = list(filter(lambda x: x.state.index != curIndex, state.views.tabbar.outputs.renderedStates))
            state.views.tabbar.outputs.layout.children = [ele.outputs.layout for ele in state.views.tabbar.outputs.renderedStates]
        def clicked (wid):
            if wid.description == "x":
                state.handlers.closed(wid)
            else:
                state.handlers.tabClicked(wid)
        def addNewTab(index):
            pass
        tabbar.handlers.handle = clicked
        tabbar.handlers.defs.closed = closed
        addToNameSpace(state, locals(), ["state", "addToNameSpace"])
    state = NameSpace()
    _tabBar(state)
    return state
def ConfirmationDialog():
    def _dialog(state):
        title = Utils.get_comp({"value": "Dialog title"}, IpywidgetsComponentsEnum.Label, className="flex")
        descriptions = Utils.get_comp({"value": "Dialog descriptions"}, IpywidgetsComponentsEnum.Label, className="flex")
        confirmBtn = Utils.get_comp({"description": "cancel"}, IpywidgetsComponentsEnum.Button, className="w-auto")
        cancelBtn = Utils.get_comp({"description": "confirm"}, IpywidgetsComponentsEnum.Button, className="w-auto")
        container = Utils.container([title, descriptions, Utils.container([confirmBtn, cancelBtn])], className = "flex flex-column")
        container.handlers.handle = lambda x: None
        addToNameSpace(state, locals(), ["state", "addToNameSpace"])
    state = NameSpace()
    _dialog(state)
    return state
def Sections():
    def _sections(state):
        title = Utils.get_comp({"value": "section title"}, IpywidgetsComponentsEnum.Label, className="flex")
        components = Utils.container([])
        container = Utils.container([title, components])
        addToNameSpace(state, locals(), ["state", "addToNameSpace"])
    state = NameSpace()
    _sections(state)
    return state
def HomePage():
    def _homepage(state):
        menu = Menus()
        tabs = TabBar()
        sec = Sections()
        searchComp = SearchComponent()
        bodyContent = Utils.container([searchComp.views.container, Utils.container([sec.views.container])],  className= "flex flex-column")
        bodyContentArea = Utils.container([bodyContent])
        body = Utils.container([tabs.views.tabbar, bodyContentArea], className= "flex flex-column")
        container = Utils.container([ menu.views.container, body])
        tabs.views.tabbar.handlers.handle = tabs.handlers.clicked
        addToNameSpace(state, locals(), ["state", "addToNameSpace"])
    state = NameSpace()
    _homepage(state)
    return state
def AddCancelBtns():
    def _temp(state):
        cancelBtn = Utils.get_comp({"description": "cancel"}, IpywidgetsComponentsEnum.Button, className="w-auto")
        confirmBtn = Utils.get_comp({"description": "confirm"}, IpywidgetsComponentsEnum.Button, className="w-auto")
        container = Utils.container([cancelBtn, confirmBtn], className="w-100")
        addToNameSpace(state, locals(), ["state", "addToNameSpace"])
    state = NameSpace()
    _temp(state)
    return state
def FieldComponent(name, component):
    def _field(state):
        label = Utils.get_comp({"value": name}, IpywidgetsComponentsEnum.Label, bind=False)
        container = Utils.container([label, component], className="flex flex-column")
        addToNameSpace(state, locals(), ["state", "addToNameSpace"])
    state = NameSpace()
    _field(state)
    return state
def FieldsReadSection():
    def _field(state):
        upIcon = Utils.get_comp({"icon": "angle-up"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
        downIcon = Utils.get_comp({"icon": "angle-down"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
        deleteButton = Utils.get_comp({"icon": "trash", "button_style": "danger"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
        editButton = Utils.get_comp({"icon": "edit", "button_style": "success"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
        container = Utils.container([editButton, deleteButton, downIcon, upIcon])
        addToNameSpace(state, locals(), ["state", "addToNameSpace"])
    state = NameSpace()
    _field(state)
    return state
def FieldCreatePage():
    def _temp(state):
        fieldName = FieldComponent("field name", Utils.get_comp({"placeholder": "field name"}, IpywidgetsComponentsEnum.Text, bind=False))
        fieldType = FieldComponent("field type", Utils.get_comp({"placeholder": "field type"}, IpywidgetsComponentsEnum.Dropdown, bind=False))
        keyValueComp = KeyValueComponent()
        keyValueComp.views.txtarea.outputs.layout.disabled = True
        moreInfo = FieldComponent("more info", keyValueComp.views.container)
        saveOrCancel = AddCancelBtns()
        container = Utils.container([fieldName.views.container, fieldType.views.container,
                                     moreInfo.views.container, saveOrCancel.views.container], className="flex flex-column")

        def reset():
            fieldName.views.component.outputs.layout.value = ""
            fieldType.views.component.outputs.layout.value = None
            keyValueComp.handlers.set_dictionary({})
        addToNameSpace(state, locals(), ["state", "addToNameSpace"])
        from timeline.t2023.generic_logger import SupportedTypes
        fieldType.views.component.outputs.layout.options = list(map(lambda x: x.name, SupportedTypes))
    state = NameSpace()
    _temp(state)
    return state
def KeyValueComponent():
    def _temp(state):
        moreInfoLay = Utils.get_comp({}, ComponentsLib.ListAndJsonNavigator)
        txtarea = Utils.get_comp({}, IpywidgetsComponentsEnum.Textarea, bind=False, className="w-500px h-min-200px h-100")
        editMoreInfoBtn = Utils.get_comp({"icon": "edit", "button_style": "success"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
        components = Utils.container([moreInfoLay, txtarea], className="flex flex-column")

        classes = """
        .w-500px{
            width: 500px;
        }
        .h-300px{
            min-height: 300px;
        }
        .h-min-200px{
            min-height: 200px;
        }
        .h-200px{
            height: 200px;
        }
        """
        import json
        def set_dictionary(dic):
            moreInfoLay.state.controller._basic._model.set_dictionary(dic)
            moreInfoLay.state.controller._update_keys()
            txtarea.outputs.layout.value = json.dumps(moreInfoLay.state.controller._basic._model.content)
        def editing(wid):
            if editMoreInfoBtn.outputs.layout.button_style == "success":
                editMoreInfoBtn.outputs.layout.button_style = "danger"
                moreInfoLay.show()
                txtarea.hide()
            else:
                editMoreInfoBtn.outputs.layout.button_style = "success"
                moreInfoLay.hide()
                txtarea.show()
                txtarea.outputs.layout.value = json.dumps(moreInfoLay.state.controller._basic._model.content)
        customCss = Utils.get_comp({}, ComponentsLib.CSSAdder)
        customCss.outputs.layout.content = classes
        container = Utils.container([components, editMoreInfoBtn,customCss], className="w-100")
        moreInfoLay.hide()
        txtarea.show()
        editMoreInfoBtn.handlers.handle = editing
        addToNameSpace(state, locals(), ["state", "addToNameSpace"])
    state = NameSpace()
    _temp(state)
    return state
def SingleField():
    def _temp(state):
        fieldName = Utils.get_comp({"value": "name", "disabled":True}, IpywidgetsComponentsEnum.Text, bind=False, className = "w-200px")
        fieldType = Utils.get_comp({"value": "type", "disabled":True}, IpywidgetsComponentsEnum.Text, bind=False, className = "w-200px")
        upIcon = Utils.get_comp({"icon": "angle-up"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
        downIcon = Utils.get_comp({"icon": "angle-down"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
        deleteButton = Utils.get_comp({"icon": "trash", "button_style": "danger"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
        editButton = Utils.get_comp({"icon": "edit", "button_style": "success"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
        operations = Utils.container([editButton, deleteButton, downIcon, upIcon])
        container = Utils.container([fieldName, fieldType, operations])
        addToNameSpace(state, locals(), ["state", "addToNameSpace"])
    state = NameSpace()
    _temp(state)
    return state
def LoggerCreatePage():
    def _temp(state):
        loggerName = FieldComponent("logger name", Utils.get_comp({}, IpywidgetsComponentsEnum.Text, bind=False, className="w-500px"))
        fields = FieldComponent("fields", Utils.container([], className ="flex flex-column"))
        addCancelBtns = AddCancelBtns()
        plusIcon = Utils.get_comp({"icon": "plus", "button_style": "success"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
        container = Utils.container([loggerName.views.container, Utils.container([fields.views.container, plusIcon], className="w-100 jc-sb"),
                                     addCancelBtns.views.container], className= "flex flex-column")
        addToNameSpace(state, locals(), ["state", "addToNameSpace"])
    state = NameSpace()
    _temp(state)
    return state

classes = """
.w-300px{
    width:300px
}
.w-200px{
    width:200px
}
.w-150px{
    width:150px
}
.MenuSelected{
    border: var(--jp-border-width) solid var(--jp-cell-editor-active-border-color);
}
"""


def creating(wid):
    name = "creatingLogger"
    if hp.process.state.currentPage == name:
        return
    hp.views.bodyContentArea.pop()
    hp.views.bodyContentArea.append(lcp.views.container)
    hp.process.state.currentPage =  name
    if hp.process.menu.process.lastMenuClicked:
        hp.process.menu.process.lastMenuClicked.remove_class("MenuSelected")
    hp.process.menu.process.lastMenuClicked = hp.process.menu.views.createBtn.outputs.layout
    hp.process.menu.views.createBtn.outputs.layout.add_class("MenuSelected")
def reading(wid):
    name = "homepage"
    if hp.process.state.currentPage == name:
        return
    hp.views.bodyContentArea.pop()
    hp.views.bodyContentArea.append(hp.views.bodyContent)
    hp.process.state.currentPage =  name
    if hp.process.menu.process.lastMenuClicked:
        hp.process.menu.process.lastMenuClicked.remove_class("MenuSelected")
    hp.process.menu.process.lastMenuClicked = hp.process.menu.views.readBtn.outputs.layout
    hp.process.menu.views.readBtn.outputs.layout.add_class("MenuSelected")
def add_field(wid):
    name = "creatingField"
    if hp.process.state.currentPage == name:
        return
    fcp.handlers.reset()
    hp.views.bodyContentArea.pop()
    hp.views.bodyContentArea.append(fcp.views.container)
    fcp.process.fieldType.views.component.outputs.layout.value = "Text"
    hp.process.state.currentPage =  name
def editing(wid, state):
    name = "editingAField"
    if hp.process.state.currentPage == name:
        return
    key = state.parent.views.fieldName.outputs.layout.value
    typ = state.parent.views.fieldType.outputs.layout.value
    moreInfo = state.moreInfos
    fcp.process.fieldName.views.component.outputs.layout.value = key
    fcp.process.fieldType.views.component.outputs.layout.value = typ
    fcp.process.keyValueComp.handlers.set_dictionary(moreInfo)
    fcp.process.index = state.index
    fcp.handlers.savePrev = fcp.process.saveOrCancel.views.confirmBtn.handlers.handle
    fcp.handlers.cancelPrev = fcp.process.saveOrCancel.views.cancelBtn.handlers.handle
    fcp.process.saveOrCancel.views.confirmBtn.handlers.handle = editSave
    fcp.process.saveOrCancel.views.cancelBtn.handlers.handle = editCancel
    hp.views.bodyContentArea.pop()
    hp.views.bodyContentArea.append(fcp.views.container)
    hp.process.state.currentPage =  name
def editSave(wid):
    key = fcp.process.fieldName.views.component.outputs.layout.value
    typ = fcp.process.fieldType.views.component.outputs.layout.value
    moreInfos = fcp.process.keyValueComp.views.moreInfoLay.state.controller._basic._model.content
    fcp.process.saveOrCancel.views.confirmBtn.handlers.handle = fcp.handlers.savePrev
    fcp.process.saveOrCancel.views.cancelBtn.handlers.handle = fcp.handlers.cancelPrev
    index = fcp.process.index
    sf = lcp.process.fields.views.component.outputs.renderedStates[index].state.parent
    sf.views.fieldName.outputs.layout.value = key
    sf.views.fieldType.outputs.layout.value = typ
    sf.views.container.state.moreInfos = moreInfos
    creating(wid)
def editCancel(wid):
    fcp.process.saveOrCancel.views.confirmBtn.handlers.handle = fcp.handlers.savePrev
    fcp.process.saveOrCancel.views.cancelBtn.handlers.handle = fcp.handlers.cancelPrev
    fcp.handlers.cancelPrev(wid)
    creating(wid)
def delete_clicked(wid, state):
    state.parent.views.container.hide()
    state.parent.views.container.state.deleted = True
def getUpper(index):
    newIndex = index-1
    while newIndex >= 0:
        sf = lcp.process.fields.views.component.outputs.renderedStates[newIndex].state.parent
        if not sf.views.container.state.deleted:
            return sf
        newIndex -= 1
def getLower(index):
    newIndex = index+1
    total = len(lcp.process.fields.views.component.outputs.renderedStates)
    while newIndex < total:
        sf = lcp.process.fields.views.component.outputs.renderedStates[newIndex].state.parent
        if not sf.views.container.state.deleted:
            return sf
        newIndex += 1
def moveUp(wid, state):
    upper = getUpper(state.index)
    if upper:
        swap(upper, state.parent)
def moveDown(wid, state):
    lower = getLower(state.index)
    if lower:
        swap(lower, state.parent)
def swap(sf1, sf2):
    key1 = sf1.views.fieldName.outputs.layout.value
    typ1 = sf1.views.fieldType.outputs.layout.value
    moreInfos1 = sf1.views.container.state.moreInfos
    sf1.views.fieldName.outputs.layout.value = sf2.views.fieldName.outputs.layout.value
    sf1.views.fieldType.outputs.layout.value = sf2.views.fieldType.outputs.layout.value
    sf1.views.container.state.moreInfos = sf2.views.container.state.moreInfos
    sf2.views.fieldName.outputs.layout.value = key1
    sf2.views.fieldType.outputs.layout.value = typ1
    sf2.views.container.state.moreInfos = moreInfos1
def addAFieldConfirm(wid):
    key = fcp.process.fieldName.views.component.outputs.layout.value
    typ = fcp.process.fieldType.views.component.outputs.layout.value
    moreInfos = fcp.process.keyValueComp.views.moreInfoLay.state.controller._basic._model.content
    if not (key and typ):
        return
    sf = SingleField()
    sf.views.fieldName.outputs.layout.value = key
    sf.views.fieldType.outputs.layout.value = typ
    sf.views.container.state.parent = sf
    sf.views.container.state.index = len(lcp.process.fields.views.component.outputs.renderedStates)
    sf.views.container.state.moreInfos = moreInfos
    sf.views.container.state.deleted =False
    sf.views.deleteButton.handlers.handle = lambda x: delete_clicked(x, sf.views.container.state)
    sf.views.editButton.handlers.handle = lambda x: editing(x, sf.views.container.state)
    sf.views.upIcon.handlers.handle = lambda x: moveUp(x, sf.views.container.state)
    sf.views.downIcon.handlers.handle = lambda x: moveDown(x, sf.views.container.state)
    lcp.process.fields.views.component.append(sf.views.container)
    creating(wid)
def extractKeysAndValue():
    res = []
    for comp in lcp.process.fields.views.component.outputs.renderedStates:
        if comp.state.deleted:
            continue
        parent    = comp.state.parent
        fieldName = parent.views.fieldName.outputs.layout.value
        fieldTyp  = parent.views.fieldType.outputs.layout.value
        moreInfo  = comp.state.moreInfos
        res.append([fieldName, fieldTyp, moreInfo])
    return res
def resetKeysAndValue():
    lcp.process.fields.views.component.outputs.renderedStates.clear()
    lcp.process.fields.views.component.outputs.layout.children = []
    lcp.process.loggerName.views.component.outputs.layout.value = ""
def createLoggerSave(wid):
    name = lcp.process.loggerName.views.component.outputs.layout.value.strip()
    fields = extractKeysAndValue()
    if name:
        cm.create_table(name, fields)
        resetKeysAndValue()
        reading(wid)
def main():
    cm = ControllerModel()
    hp = HomePage()
    lcp = LoggerCreatePage()
    lcp.process.addCancelBtns.views.confirmBtn.outputs.layout.description = "save"
    fcp = FieldCreatePage()
    fcp.process.saveOrCancel.views.confirmBtn.outputs.layout.description = "add"
    hp.process.state = NameSpace()
    hp.process.state.currentPage = ""
    fcp.process.saveOrCancel.views.confirmBtn.handlers.handle  = addAFieldConfirm
    fcp.process.saveOrCancel.views.cancelBtn.handlers.handle  = creating
    hp.process.menu.process = NameSpace()
    hp.process.menu.views.createBtn.handlers.handle  = creating
    hp.process.menu.views.readBtn.handlers.handle  = reading
    lcp.views.plusIcon.handlers.handle =  add_field
    hp.process.menu.process.lastMenuClicked = None
    lcp.process.addCancelBtns.views.cancelBtn.handlers.handle = reading
    lcp.process.addCancelBtns.views.confirmBtn.handlers.handle = createLoggerSave
