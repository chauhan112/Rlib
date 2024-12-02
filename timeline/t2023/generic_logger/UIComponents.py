from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from timeline.t2024.generic_logger.generic_loggerV3 import SearchComponent, KeyValueComponent, SingleField
from basic import Main as ObjMaker
from TimeDB import TimeDB
from timeline.t2023.generic_logger.components import DateInput, TimeInput, DateTimeInput
from typing import Union
import datetime
import ipywidgets as widgets

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
    def set_logger_name(name):
        state.process.loggerName = name
    state  = ObjMaker.variablesAndFunction(locals())
    return state
def MetaCRUDUI():
    contentWid = Utils.get_comp({"placeholder": "content"}, IpywidgetsComponentsEnum.Textarea, bind=False, className="w-auto")
    addBtn = Utils.get_comp({"icon": "plus", "button_style": "success"}, IpywidgetsComponentsEnum.Button, className="w-auto")
    delBtn = Utils.get_comp({"icon": "trash", "button_style": "danger"}, IpywidgetsComponentsEnum.Button, className="w-auto")
    okBtn = Utils.get_comp({"description": "ok"}, IpywidgetsComponentsEnum.Button, className="w-auto")
    model = MetaCRUD()
    def doNothing(wid):
        pass
    def initialize():
        pass
    container = Utils.container([contentWid, addBtn,delBtn, okBtn])
    state = ObjMaker.uisOrganize(locals())
    addBtn.handlers.handle = doNothing
    delBtn.handlers.handle = doNothing

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
        min-width: 90px;
    }"""
    crudView = Utils.get_comp({"options": ['r', 'c', 'u', 'd']}, IpywidgetsComponentsEnum.RadioButtons,className="RadioButtonsV2")
    cssCompon = Utils.get_comp({}, ComponentsLib.CSSAdder, customCss= classes)
    container = Utils.container([crudView, cssCompon], className="overflow-unset")
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
    fieldsList = Utils.container([], className="flex flex-column")
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
    container = Utils.container([loggerName, fieldsList, Utils.container([fieldName, fieldType, moreInfoAdd, addBtn, keyValueComp.views.container, htmlCom] ),
                                 createBtn], className ="flex flex-column" )
    showOrhide(1)
    moreInfoAdd.handlers.handle = showOrhide
    state = ObjMaker.uisOrganize(locals())
    return state
def UpdateMenu():
    toogleButtons = Utils.get_comp({"options":["structure", "meta"]}, IpywidgetsComponentsEnum.ToggleButtons)
    outArea = Utils.get_comp({}, ComponentsLib.CustomOutput)
    fieldsCrud = FieldCrudForm()
    metaCrud = MetaCRUDUI()
    def toggled(wid):
        opt = s.views.toogleButtons.outputs.layout.value
        if opt == "meta":
            s.views.outArea.state.controller.display(s.process.metaCrud.views.container.outputs.layout, True, True)
        else:
            s.views.outArea.state.controller.display(s.process.fieldsCrud.views.container.outputs.layout, True, True)
    container = Utils.container([toogleButtons, outArea], className = "flex flex-column")
    toogleButtons.handlers.handle = toggled
    
    s = ObjMaker.uisOrganize(locals())
    toggled(1)
    return s
def GenericDateTime():
    typ = ""
    component = None
    prev_funcs = ObjMaker.namespace()
    def keyExists(key, dic):
        return  key in dic and dic[key]
    def set_type(typ: Union["time", "date", "both"]="both"):
        s.process.typ = typ
    def get_state():
        return s
    def clear():
        if s.handlers.keyExists("auto", s.process.infos):
            now = datetime.datetime.now()
            s.process.component.value = now
        else:
            s.process.component.value = None
    def value():
        return s.process.component.value
    def set_info(infos):
        s.process.infos = infos
    def process_info():
        s.handlers.clear()
        if "disabled" in s.process.infos:
            s.process.component.disabled = s.process.infos["disabled"]
    def layout():
        return s.process.component
    def set_value(value):
        key1 = "auto-edit"
        key2 = "auto-update"
        infos = s.process.infos
        if s.handlers.keyExists(key1, infos) or s.handlers.keyExists(key2, infos):
            now = datetime.datetime.now()
            s.process.component.value = now
        else:
            s.process.component.value = value
    def is_empty():
        return True
    def set_up(**kwargs):
        a = None
        typ = s.process.typ
        if typ == "date":
            a = widgets.DatePicker(**kwargs)
        elif typ == "time":
            a = widgets.TimePicker(**kwargs)
        elif typ == "both":
            a = widgets.NaiveDatetimePicker(**kwargs)
        else:
            raise IOError("unknown type detected")
        s.process.component = a
    s = ObjMaker.variablesAndFunction(locals())
    return s
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
