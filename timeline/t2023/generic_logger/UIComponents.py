from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from timeline.t2024.ui_lib.generic_loggerV3 import SearchComponent, KeyValueComponent, SingleField
from basic import Main as ObjMaker
def MetaCRUD():
    loggerName = None
    def get_current_logger_name(bsc):
        return bsc.nms2024.ldcc._cur_btn.description
    def add_meta_info(key, value, overwrite=True):
        loggerInfos = state.process.bsc._model.read(state.process.loggerName)
        if "meta" not in loggerInfos:
            loggerInfos["meta"] = {}
        if key in loggerInfos["meta"] and not overwrite:
            raise IOError("value already exists")
        loggerInfos["meta"][key] = value
        state.handlers.saveInfos(loggerInfos)
    def delete_meta(key):
        loggerInfos = state.process.bsc._model.read(state.process.loggerName)
        del loggerInfos["meta"][key]
        state.handlers.saveInfos(loggerInfos)
    def saveInfos(infos, overwrite=True):
        state.process.bsc._model.add(state.process.loggerName, infos, overwrite)
    def exists(key):
        loggerInfos = state.process.bsc._model.read(state.process.loggerName)
        if "meta" not in loggerInfos:
            return False
        return key in loggerInfos["meta"]
    def read_meta(key):
        loggerInfos = state.process.bsc._model.read(state.process.loggerName)
        return loggerInfos["meta"][key]
    def update_logger_name(bsc):
        state.process.bsc = bsc
        if hasattr(bsc.nms2024.ldcc, "_cur_btn"):
            state.process.loggerName = get_current_logger_name(bsc)
    def set_logger_name(name):
        state.process.loggerName = name
    state  = ObjMaker.variablesAndFunction(locals())
    return state
def MetaCRUDUI():
    opsType = Utils.get_comp({"options": ["create", "read", "update", "delete"]}, IpywidgetsComponentsEnum.Dropdown, className="w-auto")
    contentWid = Utils.get_comp({"placeholder": "content"}, IpywidgetsComponentsEnum.Textarea, bind=False, className="w-auto")
    addBtn = Utils.get_comp({"icon": "plus", "button_style": "success"}, IpywidgetsComponentsEnum.Button, className="w-auto")
    delBtn = Utils.get_comp({"icon": "trash", "button_style": "danger"}, IpywidgetsComponentsEnum.Button, className="w-auto")
    showOrHide = Utils.get_comp({"description": "show", "indent":False}, IpywidgetsComponentsEnum.Checkbox, className="w-auto")
    model = MetaCRUD()
    def hideOrShow(wid):
        
        if state.views.showOrHide.outputs.layout.value:
            formContainer.show()
        else:
            formContainer.hide()
    def doNothing(wid):
        pass
    def ops_selected_v2(wid, inst=None, runParentFunc= True):
        val = state.views.glv.crudOps.options.wid.value
        if val == "u":
            container.show()
        else:
            container.hide()
        if state.process.model.process.loggerName is None:
            container.hide()
        if runParentFunc:
            state.process.bsc.nms2024.lsc._ops_selected(wid, inst)
    formContainer = Utils.container([opsType, contentWid, addBtn,delBtn])
    container = Utils.container([showOrHide, formContainer], className ="flex flex-column")
    state = ObjMaker.uisOrganize(locals())
    showOrHide.handlers.handle = hideOrShow
    addBtn.handlers.handle = doNothing
    delBtn.handlers.handle = doNothing
    opsType.handlers.handle = doNothing
    hideOrShow(1)
    
    return state
def CrudViewV2():
    classes = """.RadioButtonsV2 div {
        flex-flow: row wrap;
        max-width: 90px;
        overflow:auto;
    }
    .RadioButtonsV2 input{
        border-radius: 10px;
        padding: 8px;
        margin-right: 2px;
    }
    .RadioButtonsV2 label{
        width: 30px;
        border-radius: 10px;
        padding: 2px;
        margin : 1px;
        box-shadow: 0 0 8px 3px rgba(0, 0, 0, 0.1);
    }
    .RadioButtonsV2{
        width: auto;
    }"""
    crudView = Utils.get_comp({"options": ['r', 'c', 'u', 'd']}, IpywidgetsComponentsEnum.RadioButtons,className="RadioButtonsV2")
    cssCompon = Utils.get_comp({}, ComponentsLib.CSSAdder, customCss= classes)
    container = Utils.container([crudView, cssCompon])
    state = ObjMaker.uisOrganize(locals())
    return state
def FieldCrudForm():
    loggerName  = Utils.get_comp({"description": "logger name"}, IpywidgetsComponentsEnum.Text, bind=False)
    fieldName   = Utils.get_comp({"placeholder": "field name"}, IpywidgetsComponentsEnum.Text, bind=False,className="w-auto")
    fieldType   = Utils.get_comp({}, IpywidgetsComponentsEnum.Dropdown, bind=False, className="w-auto")
    moreInfoAdd = Utils.get_comp({"indent":False, "description": "add more info"}, IpywidgetsComponentsEnum.Checkbox,className="w-auto")
    addBtn      = Utils.get_comp({"icon":"plus"}, IpywidgetsComponentsEnum.Button, className="w-auto")
    createBtn   = Utils.get_comp({"description":"create logger"}, IpywidgetsComponentsEnum.Button)
    htmlCom = Utils.get_comp({},IpywidgetsComponentsEnum.HTML,bind=False)
    keyValueComp = KeyValueComponent()
    outArea = Utils.get_comp({}, IpywidgetsComponentsEnum.Output, bind=False)
    fieldsList = Utils.container([], className="flex flex-column")
    def showOrhide(wid):
        if moreInfoAdd.outputs.layout.value:
            keyValueComp.views.container.show()
        else:
            keyValueComp.views.container.hide()
    container = Utils.container([loggerName, fieldsList, Utils.container([fieldName, fieldType, moreInfoAdd, addBtn, keyValueComp.views.container, htmlCom] ),
                                 createBtn, outArea], className ="flex flex-column" )
    showOrhide(1)
    moreInfoAdd.handlers.handle = showOrhide
    state = ObjMaker.uisOrganize(locals())
    return state

class Main:
    def appendToGlv(bsc):
        glv = bsc.nms2024.glv
        mcrudUi= MetaCRUDUI()
        children = list(glv.layout.children )
        x = children.pop()
        children.append(mcrudUi.views.container.outputs.layout)
        children.append(x)
        glv.layout.children = children
        mcrudUi.views.container.inputs.parent = glv
        mcrudUi.process.bsc = bsc
        mcrudUi.views.glv = glv
        glv.crudOps.options.set_select_func(mcrudUi.handlers.defs.ops_selected_v2)
        mcrudUi.handlers.defs.ops_selected_v2(1,runParentFunc=False)
        glv.mcrudUi = mcrudUi