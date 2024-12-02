from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from basic import Main as ObjMaker
from LibsDB import LibsDB
from timeline.t2024.tailwind.twcrudOps import DictionaryModel
from timeline.t2024.generic_logger.generic_loggerV3 import ResultDisplayers
import os
from timeline.t2024.Array import Array
from timeline.t2024.osExplorer import Main as OSMain
from datetime import datetime
from timeline.t2024.tools import ConversionTool

def RlibExplorer():
    keyWid = Utils.get_comp({"placeholder":"Name of the path or last folder name will be taken"}, IpywidgetsComponentsEnum.Text, className="w-auto", bind = False)
    valWid = Utils.get_comp({"placeholder":"path location"}, IpywidgetsComponentsEnum.Text, className="w-auto", bind = False)
    addBtn = Utils.get_comp({"description":"add"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    openBtn = Utils.get_comp({"description":"open"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    okBtn = Utils.get_comp({"description":"ok"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    removeBtn = Utils.get_comp({"description":"remove"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    readAllBtn = Utils.get_comp({"description":"readAll"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    outArea = Utils.get_comp({},ComponentsLib.CustomOutput)
    resultDis = ResultDisplayers()
    opsBtn = Utils.container([openBtn, addBtn, removeBtn, readAllBtn])
    container = Utils.container([opsBtn, outArea],className = "flex flex-column")
    exp = OSMain.osExplorer()
    exp.views.buttons.outputs.layout.add_class("flex-wrap")
    model = DictionaryModel()
    model.set_file(LibsDB.picklePath("globals"))
    key = "explorer-paths"
    addView = Utils.container([keyWid, valWid, okBtn])
    current_btn = None
    
    ct = ConversionTool()
    def onAdd(w):
        s.views.outArea.state.controller.display(s.views.addView.outputs.layout, True, True)
        s.views.okBtn.handlers.handle = s.handlers.onAddOkClicked
    def onAddOkClicked(w):
        s.views.outArea.state.controller.clear()
        key = s.views.keyWid.outputs.layout.value.strip()
        val = s.views.valWid.outputs.layout.value.strip()
        if key and val:
            arr = s.process.model.read(s.process.key)
            arr.append((key, val))
            s.process.model.changed()
        s.views.keyWid.outputs.layout.value = ""
        s.views.valWid.outputs.layout.value = ""
    def render():
        arr = Array(s.process.model.read(s.process.key)).filter(lambda x: os.path.exists(x[1])).array
        s.process.resultDis.handlers.set_results(arr)
    def onRemove(w):
        s.views.outArea.state.controller.display(s.process.resultDis.views.container.outputs.layout, True, True)
        s.process.resultDis.views.btns.handlers.handle = s.handlers.onRemoveConfirm
    def onReadAll(w):
        s.views.outArea.state.controller.display(s.process.resultDis.views.container.outputs.layout, True, True)
        s.process.resultDis.handlers.set_results(s.process.model.read(s.process.key))
        s.process.resultDis.views.btns.handlers.handle = s.handlers.showPath
    def showPath(w):
        s.views.outArea.state.controller.clear()
        with s.views.outArea.state.controller._out:
            index = w._parent.state.index
            val = s.process.resultDis.process.data[index]
            print(val)
    def onRemoveConfirm(w):
        s.process.current_btn = w
        s.views.outArea.state.controller.display(s.views.okBtn.outputs.layout, True, True)
        s.views.okBtn.handlers.handle = s.handlers.onRemoveOkBtn
    def onRemoveOkBtn(w):
        index = s.process.current_btn._parent.state.index
        val = s.process.resultDis.process.data[index]
        arr = Array(s.process.model.read(s.process.key)).filter(lambda x: x != val).array
        s.process.model.update([s.process.key], arr)
        s.views.openBtn.outputs.layout.click()
    def onOpen(w):
        s.views.outArea.state.controller.display(s.process.resultDis.views.container.outputs.layout, True, True)
        s.process.resultDis.views.btns.handlers.handle = s.handlers.onPathClickedToDisplay
        s.handlers.render()
    def onPathClickedToDisplay(w):
        index = w._parent.state.index
        val = s.process.resultDis.process.data[index]
        name, folder = val
        s.process.exp.handlers.set_path(folder)
        s.views.outArea.state.controller.display(s.process.exp.views.container.outputs.layout, True, True)
    def nameGetter(x):
        if type(x) == str:
            return x
        return x[0]
    def infos(filepath):
        s = os.stat(filepath)
        bn = os.path.basename(filepath)
        sb = s.st_size
        ft = filepath.split(".")[-1]
        return bn, sb, ft, s.st_mtime
    def infoStr(name, size, typ, lastModified):
        return f"name: {name}\nsize: {s.process.ct.handlers.sizeReduce(size) }\ntype: {typ}\nmodified: {datetime.fromtimestamp(lastModified)}"
    def onFileSelected(selected):
        path = os.sep.join([s.process.exp.process.model.path, selected])
        with s.process.exp.views.outputDisplayer.outputs.layout:
            print(s.handlers.infoStr(*s.handlers.infos(path)))
    resultDis.handlers.name_getter = nameGetter
    openBtn.handlers.handle = onOpen
    addBtn.handlers.handle = onAdd
    removeBtn.handlers.handle = onRemove
    readAllBtn.handlers.handle = onReadAll
    exp.handlers.fileSelected = onFileSelected
    s = ObjMaker.uisOrganize(locals())
    return s
