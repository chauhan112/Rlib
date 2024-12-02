from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from basic import Main as ObjMaker
from timeline.t2024.generic_logger.generic_loggerV3 import SearchComponent, KeyValueComponent,ResultDisplayers, FieldComponent
from timeline.t2023.generic_logger import FieldsManagerV2, SupportedTypes, NewRenderer, LoggerSearch, LoggerButtonNameDecider 
from timeline.t2023.generic_logger.UIComponents import CrudViewV2, SingleField, MetaCRUDUI, UpdateMenu, GenericDateTime
from SearchSystem import MultilineStringSearch
from TimeDB import TimeDB
from CryptsDB import CryptsDB
from timeline.t2023.sql_crud import SqlCRUD
from timeline.t2024.ui_lib.refactored_key_value_adder import DicListCRUD
from timeline.t2024.antif import ExecFilterers

def FilterCreate():
    title = Utils.get_comp({"placeholder":"filter title"}, IpywidgetsComponentsEnum.Text, className="w-auto", bind=False)
    searchType = Utils.get_comp({"options": ["any", "reg", "case", "word", "concatenated", "fields", "loc"]}, 
        IpywidgetsComponentsEnum.Dropdown, className="w-auto", bind = False)
    searchContent = Utils.get_comp({"placeholder":"search word"}, IpywidgetsComponentsEnum.Text, className="w-auto", bind = False)
    createBtn = Utils.get_comp({"description":"create"}, IpywidgetsComponentsEnum.Button, className="w-auto")
    def values():
        return title.outputs.layout.value, searchType.outputs.layout.value, searchContent.outputs.layout.value
    def reset():
        title.outputs.layout.value = ""
        searchContent.outputs.layout.value = ""
    def set_values(titl, typ, content):
        title.outputs.layout.value = titl
        searchType.outputs.layout.value=typ 
        searchContent.outputs.layout.value = content
    container = Utils.container([title, searchType, searchContent, createBtn])
    s = ObjMaker.uisOrganize(locals())
    return s
def SingleFilterRead():
    index = None
    title = Utils.get_comp({"placeholder":"filter title"}, IpywidgetsComponentsEnum.Text, className="w-auto", bind=False)
    editBtn = Utils.get_comp({"icon":"edit"}, IpywidgetsComponentsEnum.Button, className="w-auto")
    delBtn = Utils.get_comp({"icon":"trash"}, IpywidgetsComponentsEnum.Button, className="w-auto")
    okButton = Utils.get_comp({"description":"ok"}, IpywidgetsComponentsEnum.Button, className="w-auto")
    def set_title(val):
        title.outputs.layout.value = val
    container = Utils.container([title, editBtn, delBtn,okButton])
    okButton.hide()
    s = ObjMaker.uisOrganize(locals())
    return s
def FilterReadPage():
    createBtn = Utils.get_comp({"description":"create new"}, IpywidgetsComponentsEnum.Button)
    filtersComponent = Utils.container([], className = "flex flex-column")
    container = Utils.container([createBtn, filtersComponent], className = "flex flex-column")

    filters = []
    uniqueTitles = set()
    def add_a_filter(title, typ, content):
        if s.handlers.title_exists(title):
            raise IOError("title already exists")
        s.process.filters.append((title, typ, content))
        s.process.uniqueTitles.add(title)
    def update_a_filter(title, typ, content):
        if not s.handlers.title_exists(title):
            raise IOError("title does not exist")
        i = s.handlers.get_index(title)
        s.process.filters[i] = (title, typ, content)
    def get_index(title):
        for i, (t,_,_) in enumerate(s.process.filters):
            if t == title:
                return i
        raise IOError("does not exist")
    def title_exists(title):
        return title in s.process.uniqueTitles
    def delete_filter(title):
        i = s.handlers.get_index(title)
        del s.process.filters[i]
    def read(title):
        i = s.handlers.get_index(title)
        return s.process.filters[i]
    s = ObjMaker.uisOrganize(locals())
    return s
def FilterPage():
    readPage = FilterReadPage()
    filterCreate = FilterCreate()
    container = Utils.get_comp({}, ComponentsLib.CustomOutput)
    def load():
        i = -1
        for i in range(len(readPage.views.filtersComponent.outputs.renderedStates)):
            comp = readPage.views.filtersComponent.outputs.renderedStates[i]
            if i < len(readPage.process.filters):
                title = readPage.process.filters[i][0]
                comp.show()
                comp.state.parent.views.editBtn.state.index = i
                comp.state.parent.views.delBtn.state.index = i
                comp.state.parent.handlers.set_title(title)
            else:
                comp.hide()
        remainings = i
        for i in range(remainings+1, len(readPage.process.filters)):
            title = readPage.process.filters[i][0]
            singleField = SingleFilterRead()
            singleField.handlers.set_title(title)
            singleField.views.editBtn.state.index = i
            singleField.views.editBtn.handlers.handle = s.handlers.edit_filter
            singleField.views.delBtn.state.index = i
            singleField.views.delBtn.handlers.handle = s.handlers.delete_filter_intermediate
            singleField.views.delBtn.state.parent = singleField
            singleField.views.container.state.parent = singleField
            readPage.views.filtersComponent.append(singleField.views.container)
    def create_new_c(w):
        container.state.controller.display(filterCreate.views.container.outputs.layout, True, True)
    def create_a_filter(w):
        readPage.handlers.add_a_filter(*filterCreate.handlers.values())
        filterCreate.handlers.reset()
        s.handlers.showReadPage()
        s.handlers.load()
        s.handlers.update_db()
    def edit_filter(w):
        container.state.controller.display(filterCreate.views.container.outputs.layout, True, True)
        filterCreate.handlers.set_values(*readPage.process.filters[w._parent.state.index])
        filterCreate.views.createBtn.handlers.handle = s.handlers.update_a_filter
        filterCreate.views.createBtn.outputs.layout.description = "update"
        readPage.process.current_index = w._parent.state.index
    def update_a_filter(w):
        filterCreate.views.createBtn.handlers.handle = create_a_filter
        filterCreate.views.createBtn.outputs.layout.description = "create"
        readPage.process.filters[readPage.process.current_index] = filterCreate.handlers.values()
        filterCreate.handlers.reset()
        s.handlers.showReadPage()
        s.handlers.load()
        s.handlers.update_db()
    def delete_filter_intermediate(w):
        w._parent.state.parent.views.okButton.show()
        w._parent.state.parent.views.okButton.handlers.handle = s.handlers.delete_filter
        w._parent.state.parent.views.okButton.state.index = w._parent.state.index
    def delete_filter(w):
        del readPage.process.filters[w._parent.state.index]
        w._parent.hide()
        readPage.views.filtersComponent.outputs.renderedStates[w._parent.state.index].hide()
        s.handlers.load()
        s.handlers.update_db()
    def showReadPage():
        container.state.controller.display(readPage.views.container.outputs.layout, True, True)
    def update_db():
        logger = s.process.parent.process.logger
        K = logger.process.K
        uuid = logger.handlers.tableNameToId(s.process.parent.process.current_button.description)
        logger.process.model.write([K.meta, uuid, K.filterStr], readPage.process.filters, True)
    def read_from_db():
        logger = s.process.parent.process.logger
        K = logger.process.K
        uuid = logger.handlers.tableNameToId(s.process.parent.process.current_button.description)
        if logger.process.model.exists([K.meta, uuid, K.filterStr]):
            readPage.process.filters = logger.process.model.read([K.meta, uuid, K.filterStr])
        else:
            readPage.process.filters = []
        return readPage.process.filters
    def read_for_current_logger(firstKey, afterUuidLoc):
        logger = s.process.parent.process.logger
        K = logger.process.K
        uuid = logger.handlers.tableNameToId(s.process.parent.process.current_button.description)
        loc = [firstKey, uuid] + afterUuidLoc
        if logger.process.model.exists(loc):
            return logger.process.model.read(loc)
    def write_to_db(firstKey, afterUuidLoc, value, overwrite=True):
        logger = s.process.parent.process.logger
        K = logger.process.K
        uuid = logger.handlers.tableNameToId(s.process.parent.process.current_button.description)
        loc = [firstKey, uuid] + afterUuidLoc
        logger.process.model.write(loc, value, overwrite)
    def read_with_logger_name(firstKey, loggerName, afterUuidLoc):
        logger = s.process.parent.process.logger
        K = logger.process.K
        uuid = logger.handlers.tableNameToId(loggerName)
        loc = [firstKey, uuid] + afterUuidLoc
        if logger.process.model.exists(loc):
            return logger.process.model.read(loc)
    showReadPage()
    readPage.views.createBtn.handlers.handle = create_new_c
    filterCreate.views.createBtn.handlers.handle = create_a_filter
    s = ObjMaker.uisOrganize(locals())
    return s
def CustomDisplayRenderer():
    rendered = {}
    def load_func(content):
        exp = {}
        exec(content, None, exp)
        res = exp["res"]
        res.set_parent(s.process.parent)
        return res
    def get_layout():
        table = s.process.parent.process.current_button.description
        ops = s.process.parent.process.container.process.crudView.views.crudView.outputs.layout.value
        if table in rendered:
            return rendered[table].get_layout()
        content = s.process.parent.process.updateForm.handlers.read()
        res = s.handlers.load_func(content)
        rendered[table] = res
        return rendered[table].get_layout()
    def remove(loggerName):
        if loggerName in rendered:
            del rendered[loggerName]
    s = ObjMaker.uisOrganize(locals())
    return s
def UpdateMenu():
    from timeline.t2024.ui_lib.refactored_key_value_adder import Main as KeyValMain
    toogleButtons = Utils.get_comp({"options":["structure", "meta", "filters", "global meta"]}, IpywidgetsComponentsEnum.ToggleButtons)
    outArea = Utils.get_comp({}, ComponentsLib.CustomOutput)
    fieldsCrud = FieldCrudForm()
    metaCrud = MetaCRUDUI()
    filterPage = FilterPage()
    globalMetaUi = KeyValMain.key_val_normal()
    globalMetaUi.process.container.process.addCancelBtns.views.container.show()
    globalMetaUi.process.container.process.addCancelBtns.views.cancelBtn.hide()
    overrides = ObjMaker.namespace()
    def toggled(wid):
        opt = s.views.toogleButtons.outputs.layout.value
        if opt == "meta":
            s.views.outArea.state.controller.display(s.process.metaCrud.views.container.outputs.layout, True, True)
            if hasattr(s.process, "parent"):
                s.handlers.update_uis(1)
                if not hasattr(s.process.overrides, "previous_btn_res_clicker"):
                    s.process.overrides.previous_btn_res_clicker = s.process.parent.process.resultDisplayer.views.btns.handlers.handle
                    s.process.parent.process.resultDisplayer.views.btns.handlers.handle = s.handlers.res_button_clicker_parent
        elif opt == "filters":
            s.views.outArea.state.controller.display(s.process.filterPage.views.container.outputs.layout, True, True)
            s.process.filterPage.handlers.showReadPage()
            s.process.filterPage.handlers.read_from_db()
            s.process.filterPage.handlers.load()
        elif opt == "structure":
            s.views.outArea.state.controller.display(s.process.fieldsCrud.views.container.outputs.layout, True, True)
        elif opt == "global meta":
            s.views.outArea.state.controller.display(s.process.globalMetaUi.process.container.views.container.outputs.layout, True, True)
            s.process.globalMetaUi.handlers.set_dictionary(s.process.parent.process.logger.process.model.read(["meta", "global"]))
    def add_intermediate(w):
        s.process.metaCrud.views.okBtn.show()
        s.process.metaCrud.views.okBtn.handlers.handle = s.handlers.add
    def delete_intermediate(w):
        s.process.metaCrud.views.okBtn.show()
        s.process.metaCrud.views.okBtn.handlers.handle = s.handlers.delete
    def add(w):
        logger, K = s.handlers.logger_n_k()
        content = s.process.metaCrud.views.contentWid.outputs.layout.value
        uuid = logger.handlers.tableNameToId(s.process.parent.process.current_button.description)
        logger.process.model.write([K.meta, uuid, K.customRender], content, True)
        s.process.metaCrud.views.okBtn.hide()
    def delete(w):
        logger, K = s.handlers.logger_n_k()
        uuid = logger.handlers.tableNameToId(s.process.parent.process.current_button.description)
        logger.process.model.delete([K.meta, uuid, K.customRender])
        s.process.metaCrud.views.okBtn.hide()
        s.process.metaCrud.views.delBtn.hide()
        s.process.metaCrud.views.contentWid.outputs.layout.value = ""
    def exists():
        logger, K = s.handlers.logger_n_k()
        uuid = logger.handlers.tableNameToId(s.process.parent.process.current_button.description)
        return logger.process.model.exists([K.meta, uuid, K.customRender])
    def read():
        logger, K = s.handlers.logger_n_k()
        uuid = logger.handlers.tableNameToId(s.process.parent.process.current_button.description)
        return logger.process.model.read([K.meta, uuid, K.customRender])
    def logger_n_k():
        logger = s.process.parent.process.logger
        K = logger.process.K
        return logger, K
    def update_uis(w):
        if s.handlers.exists():
            content = s.handlers.read()
            s.process.metaCrud.views.contentWid.outputs.layout.value = content
            s.process.metaCrud.views.delBtn.show()
        else:
            s.process.metaCrud.views.delBtn.hide()
            s.process.metaCrud.views.contentWid.outputs.layout.value = ""
    def res_button_clicker_parent(w):
        s.process.overrides.previous_btn_res_clicker(w)
        crd = s.process.parent.process.container.process.crudView.views.crudView.outputs.layout.value
        if crd == "u":
            s.handlers.toggled(1)
    def set_parent(parent):
        s.process.parent = parent
        s.process.filterPage.process.parent = parent
    def save_global_meta(w):
        cnt = s.process.parent
        content = s.process.globalMetaUi.handlers.readAll()
        cnt.process.logger.process.model.write(["meta", "global"], content, True)
        s.process.globalMetaUi.process.container.process.addCancelBtns.views.confirmBtn.hide()
    def model_changed():
        s.process.globalMetaUi.process.container.process.addCancelBtns.views.confirmBtn.show()
    metaCrud.views.addBtn.handlers.handle = add_intermediate
    metaCrud.views.delBtn.handlers.handle = delete_intermediate
    container = Utils.container([toogleButtons, outArea], className = "flex flex-column")
    toogleButtons.handlers.handle = toggled
    s = ObjMaker.uisOrganize(locals())
    toggled(1)
    globalMetaUi.handlers.model_changed = model_changed
    globalMetaUi.process.container.process.addCancelBtns.views.confirmBtn.handlers.handle = save_global_meta
    return s
def SqliteDictDB():
    model  = SqlCRUD()
    def read(key):
        base, lastKey = s.handlers._loc(key)
        s.process.model.set_base_location(base + [lastKey])
        return s.process.model.value()
    def set_file(file):
        s.process.model._sqlddb.set_file(file)
    def write(key, value, overwrite=False):
        base, lastKey = s.handlers._loc(key)
        if not overwrite and s.handlers.exists(key):
            raise IOError(f"{key} aleady exists")
        s.process.model.set_base_location(base)
        s.process.model.addEvenKeyError(lastKey, value)
    def delete(key):
        base, lastKey = s.handlers._loc(key)
        s.process.model.set_base_location(base)
        s.process.model.delete(lastKey)
    def _loc(key):
        if type(key) == str:
            return [], key
        newKey = key.copy()
        lasE = newKey.pop()
        return newKey, lasE
    def exists(key):
        base, lastKey = s.handlers._loc(key)
        s.process.model.set_base_location(base)
        try:
            return s.process.model.alreadyExists(lastKey)
        except:
            pass
        return False
    def set_table_name(tableName):
        s.process.model._sqlddb.set_table_name(tableName)
    def readAll():
        return s.process.model._sqlddb.get_content_as_dict()
    s = ObjMaker.variablesAndFunction(locals())
    s.handlers.s = s
    return s
def Constants():
    structure = "structure"
    uuid = "uuid"
    key_index = "key-index"
    meta = "meta"
    data = "data"
    table2Id = "table-name-to-uuid"
    id2TableName = "uuid-to-table-name"
    tables = "tables"
    customRender ="custom-render"
    filterStr = "filter"
    current_filter_value = "current-filter-value"
    s = ObjMaker.variablesAndFunction(locals())
    return s.process
def LoggerData():
    tableCrud = LoggerCrud()
    K = Constants()
    def create(tableName, vals):
        uuid = s.process.tableCrud.handlers.tableNameToId(tableName)
        key = s.handlers.getCurrentKey(tableName)
        s.process.tableCrud.process.model.write([K.data, uuid, key], vals)
        s.handlers.increaseKey(tableName)
    def read(tableName, id):
        uuid = s.process.tableCrud.handlers.tableNameToId(tableName)
        return s.process.tableCrud.process.model.read([K.data, uuid, id])
    def delete(tableName, id):
        uuid = s.process.tableCrud.handlers.tableNameToId(tableName)
        s.process.tableCrud.process.model.delete([K.data, uuid, id])
    def update(tableName, id, newVals):
        uuid = s.process.tableCrud.handlers.tableNameToId(tableName)
        return s.process.tableCrud.process.model.write([K.data, uuid, id], newVals, True)
    def readAll(tableName):
        uuid = s.process.tableCrud.handlers.tableNameToId(tableName)
        if s.process.tableCrud.process.model.exists([K.data, uuid]):
            return s.process.tableCrud.process.model.read([K.data, uuid])
        return {}
    def increaseKey(tableName):
        uuid = s.process.tableCrud.handlers.tableNameToId(tableName)
        val = s.handlers.getCurrentKey(tableName)
        s.process.tableCrud.process.model.write([K.meta, uuid, K.key_index], val + 1, True)
    def getCurrentKey(tableName):
        uuid = s.process.tableCrud.handlers.tableNameToId(tableName)
        return s.process.tableCrud.process.model.read([K.meta, uuid, K.key_index])
    s = ObjMaker.variablesAndFunction(locals())
    return s
def LoggerCrud():
    model = DicListCRUD()
    K = Constants()
    def create(tableName, vals):
        if s.process.model.exists([K.tables, K.table2Id, tableName]):
            raise IOError("value already exists")
        uuid = CryptsDB.generateUniqueId()
        s.process.model.write([K.tables, K.table2Id, tableName], uuid)
        s.process.model.write([K.tables, K.id2TableName, uuid], tableName)
        s.process.model.write([K.meta, uuid, K.structure], vals)
        s.process.model.write([K.meta, uuid, K.key_index], 0)
    def read(tableName):
        uuid = s.handlers.tableNameToId(tableName)
        return s.process.model.read([K.meta, uuid, K.structure])
    def delete(tableName):
        uuid = s.handlers.tableNameToId(tableName)
        s.process.model.delete([K.meta, uuid])
        s.process.model.delete([K.tables, K.table2Id, tableName])
        s.process.model.delete([K.tables, K.id2TableName, uuid])
    def update(oldName, newName,newVals):
        uuid = s.handlers.tableNameToId(oldName)
        s.process.model.write([K.tables, K.id2TableName, uuid], newName, True)
        s.process.model.delete([K.tables, K.table2Id, oldName])
        s.process.model.write([K.tables, K.table2Id, newName], uuid)
        s.process.model.write([K.meta, uuid, K.structure], newVals, True)
    def exists(loggerName):
        return s.process.model.exists([K.tables, K.table2Id, loggerName])
    def readAll():
        vals = s.process.model.read([K.tables, K.table2Id])
        return list(vals.keys())
    def tableNameToId(tableName):
        return s.process.model.read([K.tables, K.table2Id, tableName])
    s = ObjMaker.variablesAndFunction(locals())
    return s
def SearchAndCrudView():
    searchComponent = SearchComponent()
    crudView = CrudViewV2()
    keysOut = Utils.get_comp({}, ComponentsLib.CustomOutput, bind=False)
    resultsOut = Utils.get_comp({}, ComponentsLib.CustomOutput, bind=False)
    searchWithResults = Utils.container([searchComponent.views.container, keysOut], className="flex flex-column w-100")
    css = Utils.get_comp({}, ComponentsLib.CSSAdder, customCss= """.selected {background-color: var(--jp-widgets-input-focus-border-color);}""")
    container = Utils.container([Utils.container([crudView.views.container, searchWithResults, css]), 
        resultsOut], className="flex flex-column overflow-unset")
    s = ObjMaker.uisOrganize(locals())
    return s
def FieldCrudForm():
    loggerName  = Utils.get_comp({"description": "logger name"}, IpywidgetsComponentsEnum.Text, bind=False)
    fieldName   = Utils.get_comp({"placeholder": "field name"}, IpywidgetsComponentsEnum.Text, bind=False,className="w-auto")
    fieldType   = Utils.get_comp({}, IpywidgetsComponentsEnum.Dropdown, bind=False, className="w-auto")
    moreInfoAdd = Utils.get_comp({"indent":False, "description": "add more info"}, IpywidgetsComponentsEnum.Checkbox,className="w-auto")
    addBtn      = Utils.get_comp({"icon":"plus"}, IpywidgetsComponentsEnum.Button, className="w-auto")
    createBtn   = Utils.get_comp({"description":"create logger"}, IpywidgetsComponentsEnum.Button)
    htmlCom = Utils.get_comp({},IpywidgetsComponentsEnum.HTML,bind=False)
    keyValueComp = KeyValueComponent()
    
    fieldsList = Utils.container([], className="flex flex-column")
    fieldsManager = FieldsManagerV2()
    def showOrhide(wid):
        if moreInfoAdd.outputs.layout.value:
            keyValueComp.views.container.show()
        else:
            keyValueComp.views.container.hide()
    def info(msg, isWarning = False):
        if isWarning:
            htmlCom.outputs.layout.value = f"<font face='comic sans ms' color ='red'>{msg}</font>"
        else:
            htmlCom.outputs.layout.value = f"<font face='comic sans ms' color ='blue'>{msg}</font>"
        def disapp():
            htmlCom.outputs.layout.value=""
        TimeDB.setTimer().oneTimeTimer(5, disapp)
    def editing(wid):
        key = wid._parent.inputs.parent.inputs.parent.state.key
        vals = s.process.fieldsManager.process.fields[key]
        s.views.fieldType.outputs.layout.value = vals["type"]
        s.views.fieldName.outputs.layout.value = key
        s.process.keyValueComp.handlers.set_dictionary(vals["info"])
        s.views.addBtn.handlers.handle = s.handlers.overwriteField
        s.process.oldKey = key
    def overwriteField(wid):
        s.views.addBtn.handlers.handle = s.handlers.add_field_handler
        key = s.views.fieldName.outputs.layout.value
        typ = s.views.fieldType.outputs.layout.value
        moreInfos = s.process.keyValueComp.views.moreInfoLay.state.controller._basic._model.content.copy()
        s.process.fieldsManager.handlers.update_field(s.process.oldKey, key, typ, moreInfos)
        s.handlers.reset_form_values()
        s.handlers.syncViewList()
    def reset_form_values():
        s.views.fieldName.outputs.layout.value = ""
        s.process.keyValueComp.handlers.set_dictionary({})
    def syncViewList():
        notDelete = []
        for sf in s.views.fieldsList.outputs.renderedStates:
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
        s.views.loggerName.outputs.layout.value =""
        s.process.fieldsManager.handlers.reset()
        s.handlers.reset_form_values()
        s.views.fieldsList.clear()
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
        key = s.views.fieldName.outputs.layout.value
        typ = s.views.fieldType.outputs.layout.value
        moreInfos = s.process.keyValueComp.views.moreInfoLay.state.controller._basic._model.content.copy()
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
        s.views.fieldsList.append(sf.views.container)

    container = Utils.container([loggerName, fieldsList, Utils.container([fieldName, fieldType, moreInfoAdd, addBtn, keyValueComp.views.container, htmlCom] ),
                                 createBtn], className ="flex flex-column" )
    showOrhide(1)
    moreInfoAdd.handlers.handle = showOrhide
    addBtn.handlers.handle = add_field_handler
    s = ObjMaker.uisOrganize(locals())
    fieldType.outputs.layout.options = list(map(lambda x: x.name, SupportedTypes))
    return s
def GenericLoggerDataView():
    container = SearchAndCrudView()
    searcher = LoggerSearch()
    lastValue = None
    resultDisplayer = ResultDisplayers()
    rendered_forms = {}
    nameMaker = LoggerButtonNameDecider()
    parent_button_clicked_changed = False
    undoers =[]
    overrides = ObjMaker.namespace()
    current_button = None
    res_undoers = []
    current_form = None
    formMaker = lambda : FormGeneratorV2()
    searchHandlePrevFunc = None
    def result_button_clicked_undo(w):
        for func in s.process.res_undoers:
            func(w)
        s.process.res_undoers.clear()
    def btnMaker(ele):
        return Utils.get_comp({"description": s.process.resultDisplayer.handlers.name_getter(ele)}, 
                              IpywidgetsComponentsEnum.Button, className="mw-100px w-auto")
    def name_maker(ele):
        if ele == "":
            return "a"
        s.process.nameMaker.set_info(s.process.searcher._data[ele], ele)
        return s.process.nameMaker.get_name()
    def radioSelect(wid):
        for fun in s.process.undoers:
            fun(wid)
        s.process.undoers.clear()
        crd = container.process.crudView.views.crudView.outputs.layout.value
        s.process.container.views.resultsOut.state.controller.clear()
        if crd == "c":
            container.process.searchComponent.views.container.hide()
            form =  s.handlers.get_form()
            ly = form.handlers.get_layout()
            form.btn = form.handlers.get_update_button()
            s.process.current_form = form
            form.handlers.add_clicked = s.handlers.add_data
            container.views.keysOut.state.controller.display(ly, True,True)
            s.process.undoers.append(s.handlers.showSearchComponent)
            s.process.undoers.append(s.handlers.clear_key)
        elif crd == "r" and  s.process.parent.process.updateForm.handlers.exists():
            ly = s.process.parent.process.customRenderer.handlers.get_layout()
            s.process.container.views.keysOut.state.controller.display(ly, True, True)
            cnt = s.process.parent
            cnt.process.res_undoers.append(s.handlers.showSearchComponent)
            s.process.undoers.append(s.handlers.showSearchComponent)
            s.process.undoers.append(s.handlers.clear_key)
        s.process.parent.process.history.append("ops selected for logger data",crd)
        s.process.lastValue = crd
    def showSearchComponent(w):
        s.process.container.process.searchComponent.views.container.show()
    def hideSearchComponent(w):
        s.process.container.process.searchComponent.views.container.hide()
    def clear_key(wid):
        s.process.container.views.keysOut.state.controller.clear()
    def clear_results(wid):
        s.process.container.views.resultsOut.state.controller.clear()
    def get_form():
        current_logger = s.process.parent.process.current_button.description
        if current_logger in s.process.rendered_forms:
            form = s.process.rendered_forms[current_logger]
        else:
            form = s.handlers.formMaker()
            logger_struct = s.process.parent.process.logger.handlers.read(current_logger)
            form.handlers.set_structure(logger_struct)
            ly = form.handlers.get_layout()
            form.handlers.add_clicked = s.handlers.add_data
            s.process.rendered_forms[current_logger] = form
        return form
    def get_log_data_index():
        btnIndex = s.process.current_button._parent.state.index
        return s.process.resultDisplayer.process.data[btnIndex]
    def update_logger_data(w):
        form = s.handlers.get_form()
        vals = form.handlers.value()
        current_logger = s.process.parent.process.current_button.description
        index = s.handlers.get_log_data_index()
        s.process.parent.process.logger_data.handlers.update(current_logger, index, vals)
        s.process.searcher._data[index] = vals
        s.handlers.update_inbetween_undo(w)
        s.process.nameMaker.set_info(vals, s.handlers.get_log_data_index())
        s.process.current_button.description = s.process.nameMaker.get_name()
    def update_inbetween_undo(w):
        form = s.handlers.get_form()
        form.handlers.get_layout().children[-1].description = "log"
        s.process.container.views.resultsOut.state.controller.clear()
        form.handlers.reset()
    def update_state(w):
        form = s.handlers.get_form()
        vals = s.process.searcher._data[s.handlers.get_log_data_index()]
        form.handlers.set_values(vals)
        ly = form.handlers.get_layout()
        if ly.children[-1].description != "update":
            ly.children[-1].description = "update"
            s.process.container.views.resultsOut.state.controller.display(ly, True, True)
        form.handlers.add_clicked = s.handlers.update_logger_data
        s.process.undoers.append(s.handlers.update_inbetween_undo)
    def delete_inbetween(w):
        s.process.container.process.searchComponent.views.searchBtn.outputs.layout.description = "confirm"
        s.process.searchHandlePrevFunc = s.process.container.process.searchComponent.views.searchBtn.handlers.handle
        s.process.container.process.searchComponent.views.searchBtn.handlers.handle = s.handlers.delete
        s.process.undoers.append(s.handlers.delete_inbetween_undo)
    def delete_inbetween_undo(w):
        s.process.container.process.searchComponent.views.searchBtn.outputs.layout.description = "search"
        s.process.container.process.searchComponent.views.searchBtn.handlers.handle = s.process.searchHandlePrevFunc
    def delete(w):
        current_logger = s.process.parent.process.current_button.description
        s.process.parent.process.logger_data.handlers.delete(current_logger, s.handlers.get_log_data_index())
        s.process.current_button._parent.hide()
        s.handlers.delete_inbetween_undo(w)
    def read_logger_data(w):
        current_logger = s.process.parent.process.current_button.description
        vals = s.process.searcher._data[s.handlers.get_log_data_index()]
        logger_struct = s.process.parent.process.logger.handlers.read(current_logger)
        sortedKeys = sorted(logger_struct, key = lambda x: logger_struct[x]["order"])
        res = ""
        for ke in sortedKeys:
            if ke in vals:
                res +=  ke + ": " +  str(vals[ke]) + "\n"
                res += ("-"*40) + "\n"
        s.process.container.views.resultsOut.state.controller.clear()
        with s.process.container.views.resultsOut.state.controller._out:
            print(res)
    def result_button_clicked(w):
        s.handlers.result_button_clicked_undo(w)
        s.process.current_button = w
        s.process.current_button.add_class("selected")
        s.process.res_undoers.append(s.handlers.remove_btn_css)
        crd = s.handlers.current_ops_value()
        s.process.parent.process.history.append("results btn clicked in logger data for ops", crd, 
            s.process.current_button.description)
        if crd == "u":
            s.handlers.update_state(w)
        elif crd == "d":
            s.handlers.delete_inbetween(w)
        elif crd == "r":
            s.handlers.read_logger_data(w)
    def remove_btn_css(w):
        if s.process.current_button is not None:
            s.process.current_button.remove_class("selected")
    def result_button_clicked_parent(w):
        s.process.overrides.previous_btn_res_clicker(w)
        s.process.undoers.clear()
        s.handlers.radioSelect(w)
        crd = s.handlers.current_ops_value()
        if crd != "r":
            s.handlers.clear_key(w)
    def add_data(w):
        current_logger = s.process.parent.process.current_button.description
        dataForm = s.handlers.get_form()
        vals = dataForm.handlers.value()
        s.process.parent.process.logger_data.handlers.create(current_logger, vals)
        container.process.crudView.views.crudView.outputs.layout.value = "r"
        dataForm.handlers.reset()
    def set_up_searcher():
        current_logger = s.process.parent.process.current_button.description
        data = s.process.parent.process.logger_data.handlers.readAll(current_logger)
        logger_struct = s.process.parent.process.logger.handlers.read(current_logger)
        s.process.searcher.set_container(data)
        s.process.searcher.set_structure(logger_struct)
        s.process.nameMaker.set_structure(logger_struct)
        s.process.searcher.set_indices_to_search(s.process.nameMaker._indicesForName)
    def searchBtnClicked(w):
        s.handlers.set_up_searcher()
        s.process.searcher.set_indices_to_search(s.process.nameMaker._indicesForName)
        typ = s.process.container.process.searchComponent.views.searchType.outputs.layout.value
        word = s.process.container.process.searchComponent.views.inputText.outputs.layout.value
        reg = False
        case = False
        s.process.searcher.set_search_type(typ)
        if typ == "case":
            case = True
        elif typ == "reg":
            reg = True
        res = s.process.searcher.search(word, case, reg)
        s.handlers.display_search_results(res)
        s.process.parent.process.history.append("logger data search btn clicked", typ, word)
    def display_search_results(res):
        s.process.resultDisplayer.handlers.set_results(res, reverseIt = False)
        container.views.keysOut.state.controller.display(s.process.resultDisplayer.views.container.outputs.layout, True,True)
        s.process.parent.process.res_undoers.append(s.handlers.clear_key)
        if not s.process.parent_button_clicked_changed:
            s.process.overrides.previous_btn_res_clicker = s.process.parent.process.resultDisplayer.views.btns.handlers.handle
            s.process.parent.process.resultDisplayer.views.btns.handlers.handle = s.handlers.result_button_clicked_parent
            s.process.parent_button_clicked_changed = True
    def current_ops_value():
        return s.process.container.process.crudView.views.crudView.outputs.layout.value
    resultDisplayer.handlers.name_getter = name_maker
    resultDisplayer.handlers.btnMaker = btnMaker
    resultDisplayer.views.btns.handlers.handle = result_button_clicked
    container.process.crudView.views.crudView.handlers.handle = radioSelect
    container.process.searchComponent.views.searchBtn.handlers.handle = searchBtnClicked
    s = ObjMaker.uisOrganize(locals())
    return s
def HistoryTracers():
    data = []
    def append(*value):
        s.process.data.append((TimeDB.today(), value))
    def clear():
        s.process.data.clear()
    s = ObjMaker.variablesAndFunction(locals())
    s.handlers.s = s
    return s.handlers
def GenericLoggerView():
    history = HistoryTracers()
    container = SearchAndCrudView()
    fieldCrud = FieldCrudForm()
    updateForm = UpdateMenu()
    updateForm.process.fieldsCrud = fieldCrud
    logger_data = LoggerData()
    logger = logger_data.process.tableCrud
    searcher = MultilineStringSearch([], True)
    resultDisplayer = ResultDisplayers()
    lastValue = None
    loggerDataView = GenericLoggerDataView()
    customRenderer = CustomDisplayRenderer()
    undoers = []
    current_button = None
    res_undoers = []
    searchHandlePrevFunc = None
    createButtonPrevFunc = None
    def result_button_clicked_undo(w):
        for fun in s.process.res_undoers:
            fun(w)
        s.process.res_undoers.clear()
    def name_getter(ele):
        if ele == "":
            return "a"
        return s.process.searcher.container[ele]
    def radioSelect(wid):
        for fun in undoers:
            fun(wid)
        undoers.clear()
        crd = container.process.crudView.views.crudView.outputs.layout.value
        s.process.container.views.resultsOut.state.controller.clear()
        s.process.history.append("ops selected ", crd)
        if crd == "c":
            s.process.lastValue = "c"
            container.process.searchComponent.views.container.hide()
            container.views.keysOut.state.controller.display(fieldCrud.views.container.outputs.layout, True,True)
        else:
            if s.process.lastValue == "c":
                container.views.keysOut.state.controller.clear()
            s.process.lastValue = None
            container.process.searchComponent.views.container.show()
            if crd == "u" and s.process.current_button:
                s.process.updateForm.handlers.update_uis(1)
    def create_logger(wid):
        name = fieldCrud.views.loggerName.outputs.layout.value.strip()
        fields = fieldCrud.process.fieldsManager.handlers.get_fields_sorted()
        if name == "":
            return
        if len(fields) == 0:
            return
        s.process.logger.handlers.create(fieldCrud.views.loggerName.outputs.layout.value, fieldCrud.process.fieldsManager.handlers.get_fields_sorted())
        fieldCrud.handlers.clear_fields()
    def searchBtnClicked(wid):
        typ = s.process.container.process.searchComponent.views.searchType.outputs.layout.value
        word = s.process.container.process.searchComponent.views.inputText.outputs.layout.value
        case = False
        reg = False
        if typ == "reg":
            reg = True
        elif typ == "word":
            word = "\b" + word + "\b"
            reg = True
        elif typ == "case":
            case = True
        s.process.history.append("search for logger", typ, word)
        allLoggers = s.process.logger.handlers.readAll()
        s.process.searcher.set_container(allLoggers)
        s.process.resultDisplayer.handlers.set_results(s.process.searcher.search(word, case, reg), reverseIt = False)
        container.views.keysOut.state.controller.display(s.process.resultDisplayer.views.container.outputs.layout, True,True)
    def result_button_clicked(w):
        s.handlers.result_button_clicked_undo(w)
        s.process.loggerDataView.handlers.result_button_clicked_undo(w)
        s.process.current_button = w
        s.process.current_button.add_class("selected")
        s.process.res_undoers.append(s.handlers.remove_btn_css)
        crd = s.handlers.current_ops_value()
        s.process.history.append("result btn clicked for logger for operations", crd, 
            s.process.current_button.description)
        if crd == "u":
            s.handlers.update_state(w)
        elif crd == "d":
            s.handlers.delete_inbetween(w)
        elif s.process.updateForm.handlers.exists():
            s.handlers.read_logger(w)
            s.process.loggerDataView.handlers.radioSelect(1)
        elif crd == "r":
            s.handlers.read_logger(w)
    def remove_btn_css(w):
        if s.process.current_button is not None:
            s.process.current_button.remove_class("selected")
    def update_logger(w):
        s.process.fieldCrud.views.createBtn.handlers.handle = s.handlers.create_logger
        name = s.process.fieldCrud.views.loggerName.outputs.layout.value.strip()
        fields = s.process.fieldCrud.process.fieldsManager.handlers.get_fields_sorted()
        if name == "":
            return
        if len(fields) == 0:
            return
        old_name = s.process.current_button.description
        newName = s.process.fieldCrud.views.loggerName.outputs.layout.value
        s.process.logger.handlers.update(old_name, newName,
                                s.process.fieldCrud.process.fieldsManager.handlers.get_fields_sorted())
        s.handlers.update_inbetween_undo(w)
        s.process.current_button.description = newName
    def update_inbetween_undo(w):
        s.process.fieldCrud.views.createBtn.outputs.layout.description = "create logger"
        s.process.container.views.resultsOut.state.controller.clear()
        s.process.fieldCrud.handlers.clear_fields()
        s.process.fieldCrud.views.createBtn.handlers.handle = s.process.createButtonPrevFunc
    def update_state(w):
        s.process.fieldCrud.handlers.clear_fields()
        current_logger = s.process.current_button.description
        logger_struct = s.process.logger.handlers.read(current_logger)
        s.process.fieldCrud.handlers.set_fields(logger_struct.copy())
        s.process.container.views.resultsOut.state.controller.display(s.process.updateForm.views.container.outputs.layout, True, True)
        s.process.fieldCrud.views.loggerName.outputs.layout.value = current_logger
        s.process.fieldCrud.views.createBtn.outputs.layout.description = "update logger"
        s.process.createButtonPrevFunc = s.process.fieldCrud.views.createBtn.handlers.handle
        s.process.fieldCrud.views.createBtn.handlers.handle = s.handlers.update_logger
        s.process.undoers.append(s.handlers.update_inbetween_undo)
        s.process.updateForm.handlers.toggled(1)
    def delete_inbetween(w):
        s.process.container.process.searchComponent.views.searchBtn.outputs.layout.description = "confirm"
        s.process.searchHandlePrevFunc = s.process.container.process.searchComponent.views.searchBtn.handlers.handle
        s.process.container.process.searchComponent.views.searchBtn.handlers.handle = s.handlers.delete
        s.process.undoers.append(s.handlers.delete_inbetween_undo)
    def delete_inbetween_undo(w):
        s.process.container.process.searchComponent.views.searchBtn.outputs.layout.description = "search"
        s.process.container.process.searchComponent.views.searchBtn.handlers.handle = s.process.searchHandlePrevFunc
    def delete(w):
        current_logger = s.process.current_button.description
        s.process.logger.handlers.delete(current_logger)
        s.process.current_button._parent.hide()
        s.process.current_button = None
        s.handlers.delete_inbetween_undo(w)
    def read_logger(w):
        s.process.container.views.resultsOut.state.controller.display(loggerDataView.process.container.views.container.outputs.layout, True, True)
    def read_current_structure():
        return s.process.logger.process.model.read(["meta",
            s.process.logger.handlers.tableNameToId(s.process.current_button.description)])
    def menu_add_update(w):
        updateForm.handlers.defs.add(w)
        loggerName = s.process.current_button.description
        customRenderer.handlers.remove(loggerName)
    def current_ops_value():
        return s.process.container.process.crudView.views.crudView.outputs.layout.value
    resultDisplayer.views.btns.handlers.handle = result_button_clicked
    fieldCrud.views.createBtn.handlers.handle = create_logger
    resultDisplayer.handlers.name_getter = name_getter
    container.process.searchComponent.views.searchBtn.handlers.handle = searchBtnClicked
    s = ObjMaker.uisOrganize(locals())
    container.process.crudView.views.crudView.handlers.handle = radioSelect
    updateForm.handlers.set_parent(s)
    loggerDataView.process.parent = s
    customRenderer.process.parent = s
    updateForm.process.metaCrud.views.okBtn.hide()
    updateForm.handlers.add = menu_add_update
    return s
def FormGeneratorV2():
    viewGenerator = NewRenderer.creator()
    viewGenerator.set_scope({})
    structure = {}
    def _add_clicked_wrapper(*w):
        s.handlers.add_clicked(w)
    def add_clicked(*w):
        pass
    def set_structure(dic):
        s.process.structure = dic
        s.process.viewGenerator._structure = dic
    def get_layout():
        return s.process.viewGenerator.render()
    def get_update_button():
        return s.process.viewGenerator._rendered.children[-1]
    def reset():
        for k in s.process.structure:
            c = s.process.viewGenerator._key_view_map[k]
            c.clear()
    def value():
        res = {}
        for k in s.process.structure:
            c = s.process.viewGenerator._key_view_map[k]
            res[k] = c.value()
        return res
    def set_values(values):
        for k in s.process.viewGenerator._key_view_map:
            if k in values:
                val = values[k]
                c = s.process.viewGenerator._key_view_map[k]
                c.set_value(val)
            else:
                s.process.viewGenerator._key_view_map[k].clear()
    def is_empty():
        res = True
        for k in s.process.structure:
            c = s.process.viewGenerator._key_view_map[k]
            res = res and c.is_empty()
        return res
    def fieldUi(fieldName):
        return s.process.viewGenerator._key_view_map[fieldName]
    def reinitialize():
        s.process.viewGenerator._rendered = None
        s.process.viewGenerator.render()
    def make_instance(typ, **kwargs):
        gdt = GenericDateTime()
        gdt.handlers.set_type(typ)
        gdt.handlers.set_up(**kwargs)
        return gdt.handlers
    def set_up():
        s.process.viewGenerator._creator_map[SupportedTypes.Date.name] = lambda **x: s.handlers.make_instance("date", **x)
        s.process.viewGenerator._creator_map[SupportedTypes.Time.name] = lambda **x: s.handlers.make_instance("time", **x)
        s.process.viewGenerator._creator_map[SupportedTypes.DateTime.name] = lambda **x: s.handlers.make_instance("both", **x)
    viewGenerator.set_adder_func(_add_clicked_wrapper)
    s = ObjMaker.uisOrganize(locals())
    set_up()
    return s
def FilterLogger():
    parent = None
    prevFuncs = ObjMaker.namespace()
    justSetup = True
    options = []
    undoers = []
    dropdown = Utils.get_comp({"options": []}, IpywidgetsComponentsEnum.Dropdown, className="w-auto")
    ef = ExecFilterers()
    prev_values = {}
    def setup():
        cnt = s.process.parent
        cnt.process.container.process.searchComponent.views.container.append(s.views.dropdown)
        s.views.dropdown.handlers.handle = s.handlers.on_change
        filers = cnt.process.logger.process.model.read(["meta", "global", "options"])
        if "filters" in filers:
            keys = ["--"] + list(filers["filters"].keys())
            if len(keys) == 1:
                s.views.dropdown.hide()
                s.views.dropdown.handlers.handle = lambda x: x
                s.handlers.undoReadAll()
                return
            s.views.dropdown.show()
            s.views.dropdown.outputs.layout.options = keys 
            if "selected" in filers:
                s.views.dropdown.outputs.layout.value = filers["selected"]
        else:
            s.views.dropdown.hide()
        s.process.prevFuncs.onSearchFunc = cnt.process.container.process.searchComponent.views.searchBtn.handlers.handle
        cnt.process.container.process.searchComponent.views.searchBtn.handlers.handle = s.handlers.onSearch
    def readAll():
        allVals = s.process.prevFuncs.readAll()
        return list(filter(lambda x: x in s.process.options, allVals))
    def emptyFields():
        cnt = s.process.parent
        cnt.process.container.process.searchComponent.views.inputText.outputs.layout.value = ""
        cnt.process.container.process.searchComponent.views.searchType.outputs.layout.value = "any"
    def undoReadAll():
        cnt = s.process.parent
        cnt.process.logger.handlers.readAll = s.process.prevFuncs.readAll
    def onSearch(w):
        cnt = s.process.parent
        val = s.views.dropdown.outputs.layout.value
        s.process.prev_values[val] = cnt.process.container.process.searchComponent.views.inputText.outputs.layout.value
        s.process.prevFuncs.onSearchFunc(w)
    def on_change(w):
        cnt = s.process.parent
        val = s.views.dropdown.outputs.layout.value
        for func in s.process.undoers:
            func()
        s.process.undoers.clear()
        cnt.process.container.process.searchComponent.views.inputText.outputs.layout.value = ""
        if val in s.process.prev_values:
            cnt.process.container.process.searchComponent.views.inputText.outputs.layout.value = s.process.prev_values[val]
        if val is None:
            return 
        elif val == "--":
            pass
        else:
            setting = cnt.process.logger.process.model.read(["meta", "global", "options","filters" , val])
            if setting["type"] == "group":
                s.process.options = setting["value"]
                s.process.prevFuncs.readAll = cnt.process.logger.handlers.readAll
                cnt.process.logger.handlers.readAll = s.handlers.readAll
                s.process.undoers.append(s.handlers.undoReadAll)
            elif setting["type"] == "search":
                cnt.process.container.process.searchComponent.views.inputText.outputs.layout.value = setting["value"]["text"]
                cnt.process.container.process.searchComponent.views.searchType.outputs.layout.value = setting["value"]["type"]
                s.process.undoers.append(s.handlers.emptyFields)
            elif setting["type"] == "exec":
                s.process.prevFuncs.readAll = cnt.process.logger.handlers.readAll
                cnt.process.logger.handlers.readAll = s.handlers.customReadAll
                s.process.undoers.append(s.handlers.undoReadAll)
        if not s.process.justSetup:
            cnt = s.process.parent
            cnt.process.logger.process.model.write(["meta", "global", "options", "selected"], val, True)
        s.process.justSetup = False
    def customReadAll():
        cnt = s.process.parent
        val = s.views.dropdown.outputs.layout.value
        setting = cnt.process.logger.process.model.read(["meta", "global", "options","filters" , val])
        content = setting["value"]
        res = s.process.ef.handlers.execute(val, content, s)
        return res
    s = ObjMaker.uisOrganize(locals())
    return s
class Main:
    def generic_logger(fileName):
        from timeline.t2024.generic_logger.newSearch import NewSearchSystem
        glv = GenericLoggerView()
        sqdb = SqliteDictDB()
        sqdb.handlers.set_file(fileName)
        sqdb.handlers.set_table_name("logger")
        glv.process.logger.process.model = sqdb.handlers
        filter_func_setup(glv)
        filterLogger = FilterLogger()
        filterLogger.process.parent = glv
        glv.process.filterLogger = filterLogger
        filterLogger.handlers.setup()
        nss = NewSearchSystem()
        nss.process.parent = glv
        nss.handlers.set_up()
        glv.process.loggerDataView.process.newSearchSys = nss
        glv.process.container.views.container.outputs.layout
        return glv
def filter_func_setup(glv):
    filters = Utils.get_comp({"options": []}, IpywidgetsComponentsEnum.Dropdown, className="w-auto")
    def result_btn_clicked(w):
        K = glv.process.logger.process.K
        filters.handlers.previous_res_button_clicked(w)
        filtersSuggestionList = glv.process.updateForm.process.filterPage.handlers.read_from_db()
        fields = glv.process.loggerDataView.process.container.process.searchComponent.views
        if len(filtersSuggestionList) == 0:
            filters.hide()
            fields.inputText.outputs.layout.value = ""
            fields.searchType.outputs.layout.value = "any"
            filters.outputs.layout.value = None
        else:
            filters.show()
            filters.state.updateIt = False
            filters.outputs.layout.options = ["--"] + list(map(lambda x: x[0], filtersSuggestionList))
            val = glv.process.updateForm.process.filterPage.handlers.read_for_current_logger(K.meta, [K.current_filter_value])
            if val and val in filters.outputs.layout.options:
                filters.outputs.layout.value = val
    def selected(w):
        K = glv.process.logger.process.K
        fields = glv.process.loggerDataView.process.container.process.searchComponent.views
        title = filters.outputs.layout.value
        if title is None:
            return 
        if title == "--":
            fields.inputText.outputs.layout.value = ""
            fields.searchType.outputs.layout.value = "any"
        else:
            title, typ, content = glv.process.updateForm.process.filterPage.process.readPage.handlers.read(filters.outputs.layout.value)
            fields.inputText.outputs.layout.value = content
            fields.searchType.outputs.layout.value = typ
        if filters.state.updateIt:
            glv.process.updateForm.process.filterPage.handlers.write_to_db(K.meta, [K.current_filter_value], title)
        filters.state.updateIt = True
    glv.process.loggerDataView.process.container.process.searchComponent.views.container.append(filters)
    filters.handlers.handle = selected
    filters.handlers.previous_res_button_clicked = glv.process.resultDisplayer.views.btns.handlers.handle
    glv.process.loggerDataView.process.filters = filters
    glv.process.resultDisplayer.views.btns.handlers.handle = result_btn_clicked
