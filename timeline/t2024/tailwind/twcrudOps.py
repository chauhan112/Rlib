from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from useful.basic import Main as ObjMaker
from timeline.t2024.generic_logger.generic_loggerV3 import ResultDisplayers, AddCancelBtns
from timeline.t2023.dep_extractor.dependency_extractor import DicOps
from useful.ComparerDB import ComparerDB
from SerializationDB import SerializationDB
def DictionaryModel():
    model = {}
    main_loc = []
    def changed():
        pass
    def goback():
        if len(s.process.main_loc) > 0:
            s.process.main_loc.pop()
    def goForward(key):
        s.process.main_loc.append(key)
    def add(loc, val):
        if not s.handlers.exists(loc):
            s.handlers.update(loc, val)
            s.handlers.changed()
    def read(loc = None):
        newLoc = s.handlers._get_loc(loc)
        return DicOps.get(s.process.model, newLoc)
    def update(loc, newValue):
        newLoc = s.handlers._get_loc(loc)
        DicOps.addEventKeyError(s.process.model, newLoc, newValue)
        s.handlers.changed()
    def delete(loc):
        if len(loc) == 0:
            return
        elif type(loc) == str:
            loc = [loc]
        newLoc = loc.copy()
        lastKey = newLoc.pop()
        vals = s.handlers.read(newLoc)
        del vals[lastKey]
        s.handlers.changed()
    def exists(loc):
        try:
            s.handlers.read(loc)
            return True
        except:
            return False
    def readAll():
        return s.process.model
    def set_file(file):
        s.process.filePath = file
        s.process.model = SerializationDB.readPickle(file)
        def sync():
            SerializationDB.pickleOut(s.process.model, s.process.filePath)
        s.handlers.changed = sync
    def export(file):
        SerializationDB.pickleOut(s.process.model, file)
    def _get_loc(loc):
        newLoc = loc
        if newLoc is None:
            newLoc = s.process.main_loc
        elif type(newLoc) == str:
            newLoc = s.process.main_loc.copy() + [loc]
        return newLoc
    s = ObjMaker.uisOrganize(locals())
    s.handlers.s = s
    return s.handlers
def TailWindCRUDOps():
    keyWid = Utils.get_comp({"placeholder":"add Key like .w-10px"}, IpywidgetsComponentsEnum.Text, className="w-auto", bind = False)
    valueContent = Utils.get_comp({"placeholder":"content without parenthesis for example: padding:10px; font-size:10px"}, 
                                  IpywidgetsComponentsEnum.Textarea, className="w-auto", bind = False)
    searchText = Utils.get_comp({"placeholder":"search in value"}, IpywidgetsComponentsEnum.Text, className="w-auto", bind=False)
    searchBtn = Utils.get_comp({"description":"search"}, IpywidgetsComponentsEnum.Button, className="w-auto")
    addBtn = Utils.get_comp({"description":"add"}, IpywidgetsComponentsEnum.Button, className="w-auto")
    delBtn = Utils.get_comp({"description":"delete"}, IpywidgetsComponentsEnum.Button, className="w-auto")
    updateBtn = Utils.get_comp({"description":"update"}, IpywidgetsComponentsEnum.Button, className="w-auto")
    okBtn = Utils.get_comp({"description":"ok"}, IpywidgetsComponentsEnum.Button, className="w-auto")
    refreshBtn = Utils.get_comp({"description":"refresh"}, IpywidgetsComponentsEnum.Button, className="w-auto")
    model = DictionaryModel()
    adderContainer = Utils.container([keyWid, valueContent, okBtn])
    cancelConfirms = AddCancelBtns()
    resultDisp = ResultDisplayers()
    outArea = Utils.get_comp({}, ComponentsLib.CustomOutput)
    opsRow = Utils.container([searchText, searchBtn, addBtn, delBtn, updateBtn, refreshBtn])
    container = Utils.container([opsRow, resultDisp.views.container, outArea], className="flex flex-column")
    debug = None
    currentSelectedBtn = None
    addOrUpdateFunc = None
    def onAdd(w):
        s.views.outArea.state.controller.clear()
        s.views.outArea.state.controller.display(s.views.adderContainer.outputs.layout, True, True)
        s.process.addOrUpdateFunc = s.process.model.add
    def onAddOk(w):
        key = s.views.keyWid.outputs.layout.value.strip()
        value = s.views.valueContent.outputs.layout.value
        s.process.addOrUpdateFunc(key, value)
        s.views.keyWid.outputs.layout.value = ""
        s.views.valueContent.outputs.layout.value = ""
        s.views.outArea.state.controller.clear()
    def onSearch(w):
        word = s.views.searchText.outputs.layout.value
        res = s.handlers.search(s.process.model.s.process.model, word)
        s.process.resultDisp.handlers.set_results(res, reverseIt = False)
        s.process.resultDisp.views.container.show()
        s.process.resultDisp.views.btns.handlers.handle = s.handlers.showContent
    def onDelete(w):
        s.process.resultDisp.views.btns.handlers.handle = s.handlers.onDeleteResultBtn
    def onDeleteResultBtn(w):
        s.views.outArea.state.controller.clear()
        s.views.outArea.state.controller.display(s.process.cancelConfirms.views.container.outputs.layout, True, True)
        s.process.cancelConfirms.views.cancelBtn.handlers.handle = s.handlers.onDeleteCancel
        s.process.cancelConfirms.views.confirmBtn.handlers.handle= s.handlers.onDeleteConfirm
        s.process.currentSelectedBtn = w
    def showContent(w):
        s.views.outArea.state.controller.clear()
        with s.views.outArea.state.controller._out:
            key = s.process.resultDisp.process.data[w._parent.state.index]
            print(f"{key} {{\n{s.process.model.s.process.model[key]} \n }}")
    def search(dic, word, case=False, reg =False):
        res = []
        for key in dic:
            value = dic[key]
            if ComparerDB.has(word, value, case, reg):
                res.append(key)
        return res
    def nameGetter(key):
        return key
    def onRefresh(w):
        s.process.CSSMain.loaded.content = s.handlers.toText()
    def onDeleteConfirm(w):
        s.views.outArea.state.controller.clear()
        if s.process.currentSelectedBtn is None:
            return 
        key = s.process.resultDisp.process.data[s.process.currentSelectedBtn._parent.state.index]
        s.process.model.delete(key)
        s.process.currentSelectedBtn._parent.hide()
        s.process.currentSelectedBtn = None
    def onDeleteCancel(w):
        s.process.resultDisp.views.btns.handlers.handle = s.handlers.showContent
        s.views.outArea.state.controller.clear()
        s.process.currentSelectedBtn = None
    def onUpdate(w):
        s.process.resultDisp.views.btns.handlers.handle = s.handlers.onUpdateResultButton
    def onUpdateResultButton(w):
        s.handlers.onAdd(w)
        s.process.addOrUpdateFunc = s.process.model.update
        key = s.process.resultDisp.process.data[w._parent.state.index]
        value = s.process.model.read(key)
        s.views.keyWid.outputs.layout.value = key
        s.views.valueContent.outputs.layout.value =value
    def toText():
        from timeline.t2024.Array import Array
        values = s.process.model.readAll()
        tabSize = 4
        space = " "* tabSize
        res = ""
        for key in values:
            content = values[key]
            contentLines = Array(content.splitlines()).map(lambda x: space + x.strip()).array
            newIndentedContent = "\n".join(contentLines)
            res += f"{key}{{\n{newIndentedContent}\n}}\n"
        return res
    resultDisp.views.btns.handlers.handle = showContent
    searchBtn.handlers.handle = onSearch
    okBtn.handlers.handle = onAddOk
    addBtn.handlers.handle = onAdd
    delBtn.handlers.handle = onDelete
    updateBtn.handlers.handle = onUpdate
    refreshBtn.handlers.handle = onRefresh
    resultDisp.views.container.hide()
    resultDisp.handlers.name_getter = nameGetter
    s = ObjMaker.uisOrganize(locals())
    return s