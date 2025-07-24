from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum
from basic import Main as ObjMaker
import os
from useful.LibsDB import LibsDB
from timeline.t2024.ui_lib.refactored_key_value_adder import Main as KVSMain
from useful.SerializationDB import SerializationDB

def PickleExplorer():
    opsWid = Utils.get_comp({"options": os.listdir(LibsDB.picklePath()) },IpywidgetsComponentsEnum.Dropdown, className = "w-auto")
    kvs = KVSMain.key_val_normal()
    btn = Utils.get_comp({"description":"save"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    pathWid = Utils.get_comp({"placeholder":"add word"}, IpywidgetsComponentsEnum.Text, className="w-auto", bind = False)
    loadBtn = Utils.get_comp({"description":"load"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    filepath = None
    def onSave(w):
        if s.process.filepath:
            SerializationDB.pickleOut(s.process.kvs.handlers.readAll(), s.process.filepath)
        s.views.btn.hide()
    def get_path():
        val = s.views.opsWid.outputs.layout.value
        if val is None:
            return 
        return LibsDB.picklePath(val)
    def onChange(w):
        s.process.filepath = s.handlers.get_path()
        s.handlers.load()
    def onContentChanged():
        s.views.btn.show()
    def onLoad(w):
        if os.path.exists(s.views.pathWid.outputs.layout.value.strip()):
            s.process.filepath = s.views.pathWid.outputs.layout.value.strip()
            s.handlers.load()
    def load():
        s.process.kvs.handlers.set_dictionary(SerializationDB.readPickle(s.process.filepath))
        s.views.btn.hide()
    btn.hide()
    container = Utils.container([Utils.container([opsWid, btn]),
                                 Utils.container([pathWid, loadBtn]),
                                 kvs.process.container.views.container], className ="flex flex-column")
    opsWid.handlers.handle = onChange
    kvs.process.container.process.model._model_changed = onContentChanged
    btn.handlers.handle = onSave
    loadBtn.handlers.handle = onLoad
    s = ObjMaker.uisOrganize(locals())
    return s