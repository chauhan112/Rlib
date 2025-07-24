from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from useful.basic import Main as ObjMaker
from timeline.t2024.Array import Array
from timeline.t2024.ui_lib.refactored_key_value_adder import Main as KVMain
from timeline.t2024.tailwind.twcrudOps import DictionaryModel
from jupyterDB import jupyterDB

def NewRlib():
    dicModel = DictionaryModel()
    dicModel.set_file("_rajaDB/GAp2LXsZlzHawym.pkl")
    keyValCom = KVMain.key_val_normal()
    keyValCom.handlers.set_dictionary(dicModel.read(["rlib"]))
    prevFunc = ObjMaker.namespace()
    kvs = keyValCom.process.mkvp.process.kvsForMeta
    def btnClicked(w):
        kd = s.process.kvs.process.keysDisplayer
        info = kd.process.data[w._parent.state.index]
        isFolder = info[-1]
        if not isFolder:
            s.process.kvs.process.current_btn = w
            s.process.kvs.process.opsComp.handlers.set_value(info[1][0])
            s.process.kvs.process.opsComp.views.keyInp.outputs.layout.value = info[0]
            kvs.views.outputArea.outputs.layout.clear_output()
            with kvs.views.outputArea.outputs.layout:
                content = info[1][0]
                exec(content, jupyterDB._params, locals())
        else:
            s.process.prevFunc.onResultsBtnClicked(w)
    def newDirList():
        vals = s.process.prevFunc.prevDirList()
        searchWord = s.process.kvs.views.pathText.outputs.layout.value.strip()
        return Array(vals).filter(lambda x: searchWord in x[0]).array
    def onFilter(w):
        s.process.kvs.handlers.render_and_update_ops_comp()
    def newPasteFunc(w):
        s.process.prevFunc.prevPasteFunc(w)
        s.process.dicModel.changed()
    def setup():
        s.process.prevFunc.onResultsBtnClicked = s.process.kvs.process.keysDisplayer.views.btns.handlers.handle
        s.process.prevFunc.prevDirList = s.process.keyValCom.process.mkvp.process.model.dirList
        s.process.prevFunc.prevPasteFunc = s.process.keyValCom.process.mkvp.process.kvsForMeta.process.operationManager.handlers.paste_handler
        
        s.process.kvs.views.pathText.outputs.layout.observe(onFilter, ["value"])
        s.process.kvs.process.keysDisplayer.views.btns.handlers.handle = s.handlers.btnClicked
        s.process.kvs.views.container.outputs.layout.remove_class("border-2px-burlywood")
        s.process.kvs.views.pathText.outputs.layout.disabled = False
        s.process.kvs.views.pathText.outputs.layout.value =""
        s.process.kvs.views.pathText.outputs.layout.continuous_update = False
        s.process.kvs.views.pathText.outputs.layout.placeholder ="filter keys"
        s.process.keyValCom.process.mkvp.process.model.dirList = s.handlers.newDirList
        s.process.kvs.process.operationManager.handlers.paste_handler = s.handlers.newPasteFunc
    container = keyValCom.process.container.views.container
    s = ObjMaker.uisOrganize(locals())
    return s

class Main:
    def rlibNew():
        nr = NewRlib()
        nr.handlers.setup()
        return nr