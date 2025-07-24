from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from useful.basic import Main as ObjMaker
from timeline.t2024.tailwind.twcrudOps import DictionaryModel
from timeline.t2024.generic_logger.generic_loggerV3 import ResultDisplayers
import json
def RowForm():
    keyWid = Utils.get_comp({"placeholder":"key"}, IpywidgetsComponentsEnum.Text, className="w-auto", bind = False)
    valWid = Utils.get_comp({"placeholder":"value"}, IpywidgetsComponentsEnum.Text, className="w-auto", bind = False)
    deleteBtn = Utils.get_comp({"icon":"trash", "button_style": "danger"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    editBtn = Utils.get_comp({"icon":"pencil", "button_style": "success"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    okBtn = Utils.get_comp({"description":"ok"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    okBtn.hide()
    container = Utils.container([keyWid, valWid, deleteBtn, editBtn, okBtn])
    def read():
        return (s.views.keyWid.outputs.layout.value.strip(), 
        s.views.valWid.outputs.layout.value.strip(), )
    def onPencil(w):
        s.views.keyWid.outputs.layout.disabled = not s.views.keyWid.outputs.layout.disabled
        s.views.valWid.outputs.layout.disabled = not s.views.valWid.outputs.layout.disabled
        s.views.deleteBtn.outputs.layout.disabled = not s.views.deleteBtn.outputs.layout.disabled
    def onDelete(w):
        s.views.okBtn.show()
    def onOk(w):
        s.views.okBtn.hide()
    okBtn.handlers.handle = onOk
    deleteBtn.handlers.handle = onDelete
    editBtn.handlers.handle = onPencil
    s = ObjMaker.uisOrganize(locals())
    return s
def TaskCreateForm():
    from timeline.t2024.generic_logger.generic_loggerV3 import AddCancelBtns
    from timeline.t2024.ui_lib.refactored_key_value_adder import Main as KVMain
    acb = AddCancelBtns()
    acb.views.container.outputs.layout.add_class("jc-end")
    kv = KVMain.key_val_normal()
    kv.handlers.set_dictionary({"attrs": dict(important = 0, status="open"), "description": "\n"})
    kv.process.mkvp.process.kvsForMeta.views.container.outputs.layout.remove_class("border-2px-burlywood") 
    kv.process.mkvp.process.kvsForMeta.views.container.outputs.layout.add_class("br-dashed")
    kv.process.mkvp.process.kvsForMeta.views.fileLabel.hide()
    kv.process.mkvp.process.kvsForMeta.views.pathText.hide()
    kv.process.mkvp.process.kvsForMeta.views.locRow.hide()
    prehand = kv.process.mkvp.process.kvsForMeta.views.goBackBtn.handlers.handle
    kv.process.mkvp.process.kvsForMeta.views.fileOpsRow.append(kv.process.mkvp.process.kvsForMeta.views.locInput)
    kv.process.mkvp.process.kvsForMeta.views.fileOpsRow.append(kv.process.mkvp.process.kvsForMeta.views.goBackBtn)
    kv.process.mkvp.process.kvsForMeta.views.goBackBtn.handlers.handle = prehand
    kv.process.container.views.container.outputs.layout
    textWid = Utils.get_comp({"placeholder":"task name"}, IpywidgetsComponentsEnum.Text, className="w-auto", bind = False)
    container = Utils.container([textWid, kv.process.container.views.container,acb.views.container], className="flex flex-column" )
    
    def get_vals():
        return s.views.textWid.outputs.layout.value, s.process.kv.handlers.readAll()
    def clear():
        s.process.kv.handlers.set_dictionary({})
        s.views.textWid.outputs.layout.value = ""
    def set_vals(name, attrs):
        s.process.kv.handlers.set_dictionary(attrs)
        s.views.textWid.outputs.layout.value = name
    s = ObjMaker.uisOrganize(locals())
    return s
def KeyValueForm():
    multiLineValues = Utils.get_comp({"placeholder": "content"}, IpywidgetsComponentsEnum.Textarea, bind=False, className="w-100 textarea-h-150px p0")
    keyInp = Utils.get_comp({"placeholder": "key"},IpywidgetsComponentsEnum.Text, bind=False, className="w-auto")
    textInp = Utils.get_comp({"placeholder": "value"},IpywidgetsComponentsEnum.Text, bind=False, className="w-250px")
    inpType = Utils.get_comp({"options": ["raw", "json", "textarea"]}, IpywidgetsComponentsEnum.Dropdown, className="w-auto")
    okBtn = Utils.get_comp({"description": "ok"}, IpywidgetsComponentsEnum.Button, className="w-auto")
    container = Utils.container([Utils.container([keyInp, inpType, textInp, okBtn]), multiLineValues],
                                className="flex flex-column")
    multiLineValues.hide()
    def onTypeSelected(w):
        inpTypeValue = s.views.inpType.outputs.layout.value
        if inpTypeValue == "raw":
            s.views.multiLineValues.hide()
            s.views.textInp.show()
        elif inpTypeValue in ["textarea", "json"]:
            s.views.multiLineValues.show()
            s.views.textInp.hide()
    def get_key_value():
        inpTypeValue = inpType.outputs.layout.value
        key = keyInp.outputs.layout.value
        value = None
        if inpTypeValue == "raw":
            value = s.views.textInp.outputs.layout.value
        elif inpTypeValue == "json":
            value = json.loads(s.views.multiLineValues.outputs.layout.value)
        elif inpTypeValue == "textarea":
            value = s.views.multiLineValues.outputs.layout.value
        return key, value
    def set_value(val):
        
        if type(val) == str:
            if  "\n" in val:
                s.views.inpType.outputs.layout.value = "textarea"
                s.views.multiLineValues.outputs.layout.value= val
            else:
                s.views.inpType.outputs.layout.value = "raw"
                s.views.textInp.outputs.layout.value = val
        else:
            s.views.inpType.outputs.layout.value = "json"
            s.views.multiLineValues.outputs.layout.value= json.dumps(val)
    def clearFields():
        keyInp.outputs.layout.value =""
        textInp.outputs.layout.value = ""
        s.views.multiLineValues.outputs.layout.value = ""
    inpType.handlers.handle = onTypeSelected
    s = ObjMaker.uisOrganize(locals())
    return s
def ScheduleMaker():
    dm = DictionaryModel()
    dm.set_file( "schedule_maker.pkl")
    dm.readAll()
    opsWid = Utils.get_comp({"options": ["add",'update',"delete"]},IpywidgetsComponentsEnum.Dropdown, className = "w-auto")
    textWid = Utils.get_comp({"placeholder":"add word"}, IpywidgetsComponentsEnum.Text, className="w-auto", bind = False)
    btn = Utils.get_comp({"description":"add"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    s = ObjMaker.uisOrganize(locals())
    return s