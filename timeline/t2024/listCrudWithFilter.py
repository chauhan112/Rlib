from basic import Main as ObjMaker
from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from timeline.t2024.generic_logger.generic_loggerV3 import ResultDisplayers
import json
from useful.ComparerDB import ComparerDB
from useful.SerializationDB import SerializationDB
from timeline.t2024.tailwind.twcrudOps import DictionaryModel
from timeline.t2024.Array import Array
from useful.CryptsDB import CryptsDB

def SearchComplex():
    values = []
    def default_val_func(k, v):
        return v
    valFunc = default_val_func
    dm = DictionaryModel()
    renderedMap = {}
    def search(typ, word, vals=None):
        if vals is None:
            vals = s.process.values
        res  = []
        if type(s.process.values) == list:
            for i, val in enumerate(vals):
                if s.handlers.compare(typ, word, i, s.handlers.valFunc(i, val)):
                    res.append(i)
        elif type(s.process.values) == dict:
            for key in vals:
                val = s.handlers.valFunc(key, s.process.values[key]) 
                if s.handlers.compare(typ, word, key, val):
                    res.append(key)
        return res
    def compare(typ, word, key, targetWord):
        """
            typ = reg|in|word|equal|caseless
        """
        if typ == "reg":
            return ComparerDB.has(word, targetWord, reg=True)
        elif typ == "in":
            return word in targetWord
        elif typ == "word":
            return ComparerDB.has(f"\b{word}\b", targetWord, reg=True)
        elif typ == "equal":
            return word == targetWord
        elif typ == "caseless":
            return ComparerDB.inCompare(word, targetWord)
        elif typ == "lesser":
            return word < targetWord
        elif typ == "greater":
            return word > targetWord
        elif typ == "exec":
            f = s.handlers.getFunc(word)
            return f(key, targetWord, s)
        return False
    def sort(vals=None, reverse=False):
        if vals is None:
            vals = s.process.values
        if type(s.process.values) == dict:
            return sorted(vals, key = lambda x: s.handlers.valFunc(x, s.process.values[x]), reverse=reverse)
        return sorted(vals, key = lambda x: s.handlers.valFunc(x, vals[x]), reverse=reverse)
    def getFunc(funcText):
        if funcText in s.process.renderedMap:
            return s.process.renderedMap[funcText]
        else:
            xx = {}
            exec(funcText, xx)
            f = (xx["f"])
            s.process.renderedMap[funcText] = f
            return f
    def sortWithExec( funcText, vals=None ):
        f = s.handlers.getFunc(funcText)
        return sorted(vals, key = lambda x: f((x, s.handlers.valFunc(x, s.process.values[x])), s))
    def opsList(searches):
        """
        opTyp = search|sort
        search
            typ, word
            typ = reg|in|word|equal|caseless
        sort 
            reverse=False
        """
        s.handlers.valFunc = s.handlers.default_val_func
        res = s.process.values
        for opTyp, params in searches:
            if opTyp == "search":
                styp, word = params
                res = s.handlers.search(styp, word, res)
            elif opTyp == "sort":
                res = s.handlers.sort(res, params)
        return res
    def valFromLoc(val, loc):
        dm = s.process.dm
        dm.s.process.model = val
        if dm.exists(loc):
            return dm.read(loc)
        return ""
    def valFromLocOpt(val, loc,key):
        if loc is None:
            return key
        return s.handlers.valFromLoc(s.process.values, [key] + loc)
    def locSearch(searches, getValues=True):
        res = s.process.values
        searched = False
        for opTyp, params in searches:
            if opTyp == "search":
                loc, styp, word, invertResult = params
                s.handlers.valFunc = lambda k, v: s.handlers.valFromLocOpt(v, loc, k)
                res = s.handlers.search(styp, word, res)
                if invertResult:
                    res = s.handlers.invertIt(res)
                searched = True
            elif opTyp == "sort":
                loc, reverseIt = params
                s.handlers.valFunc = lambda k, v: s.handlers.valFromLocOpt(v, loc, k)
                res = s.handlers.sort(res, reverseIt)
            elif opTyp == "sortExec":
                s.handlers.valFunc = s.handlers.default_val_func
                res = s.handlers.sortWithExec(params, res)
        if not searched and type(s.process.values) == list:
            return res
        if getValues:
            return Array(res).map(lambda x: s.process.values[x]).array
        return res
    def invertIt(res):
        if type(s.process.values) == dict:
            return Array(s.process.values).filter(lambda x: x not in res).array
        listRes = []
        resSet = set(res)
        for i, val in enumerate(s.process.values):
            if i not in resSet:
                listRes.append(i)
        return listRes
        
    s = ObjMaker.variablesAndFunction(locals())
    return s
def JsonCrud():
    cancelBtn = Utils.get_comp(dict(description="cancel"), IpywidgetsComponentsEnum.Button, className="w-auto")
    okBtn = Utils.get_comp(dict(description="ok"), IpywidgetsComponentsEnum.Button, className="w-auto")
    confirm = Utils.container([cancelBtn, okBtn], className="w-100 right")
    xx = {'filter': {'options': [['not done',
        ['search', [['attrs', 'done'], 'equal', True, True]]]],
      'selected': 'not done'}}
    import pprint
    
    txtarea = Utils.get_comp(dict(placeholder=pprint.pformat(xx)), IpywidgetsComponentsEnum.Textarea, className="p0 w-100 hmin-200px textarea")
    label = Utils.get_comp(dict(), IpywidgetsComponentsEnum.Label, bind=False)
    container = Utils.container([txtarea, label, confirm], className="flex flex-column")
    model = {}
    def check():
        s.views.txtarea.outputs.layout.value = json.dumps(s.process.model, indent=2)
    def set_content(dic):
        s.process.model = dic
        s.handlers.check()
    def onChange(w):
        try:
            s.process.model = json.loads(s.views.txtarea.outputs.layout.value)
            s.handlers.check()
            s.views.label.hide()
        except Exception as e:
            s.views.label.show()
            s.views.label.outputs.layout.value = "invalid json"
    txtarea.outputs.layout.continuous_update = False
    txtarea.handlers.handle = onChange
    s = ObjMaker.uisOrganize(locals())
    return s
def ResultButtonOps():
    p = None
    def handle(w):
        typ = s.process.p.views.opsWid.outputs.layout.value
        index = s.process.p.process.resultDisplayer.process.data[w._parent.state.index]
        s.process.p.process.currentIndex = index
        s.process.p.process.current_btn = w
        if typ in s.process.opsMap:
            s.process.opsMap[typ]()
    def attrs():
        index = s.process.p.process.currentIndex
        val = s.process.p.process.model[index]
        if "attrs" in val:
            s.process.p.process.jc.handlers.set_content(val["attrs"])
        else:
            s.process.p.process.jc.handlers.set_content({})
        s.process.p.views.output.state.controller.display(s.process.p.process.jc.views.container.outputs.layout, True, True)
        s.process.p.process.jc.views.okBtn.handlers.handle = s.handlers.onAttrOk
        s.process.p.process.jc.views.cancelBtn.handlers.handle = s.handlers.onAttrCancel
    def update():
        index = s.process.p.process.currentIndex
        val = s.process.p.process.model[index]
        s.process.p.views.textWid.outputs.layout.value = s.process.p.handlers.nameFunc(val)
        s.process.p.views.addConfirm.handlers.handle = s.handlers.update_confirm
        s.process.p.views.addConfirm.outputs.layout.description = "confirm"
    def delete():
        s.process.p.views.addConfirm.handlers.handle = s.handlers.delete_confirm
        s.process.p.views.addConfirm.outputs.layout.description = "confirm"
    def update_confirm(w):
        val = s.process.p.views.textWid.outputs.layout.value
        oldval = s.process.p.process.model[s.process.p.process.currentIndex]
        oldval["name"]= val
        s.process.p.process.model[s.process.p.process.currentIndex] = oldval
        s.process.p.views.textWid.outputs.layout.value  = ""
        s.process.p.views.opsWid.outputs.layout.value = "add"
        s.process.p.process.currentIndex = None
        s.process.p.process.current_btn = None
        s.process.p.handlers.modelChanged()
    def delete_confirm(w):
        valUuid = s.process.p.process.model[s.process.p.process.currentIndex]["uuid"]
        del s.process.p.process.model[s.process.p.process.currentIndex]
        s.process.p.process.allValues = list(filter(lambda x: x["uuid"] != valUuid, s.process.p.process.allValues))
        s.process.p.views.addConfirm.outputs.layout.description = "search"
        s.process.p.views.addConfirm.handlers.handle = s.process.p.handlers.onSearch
        s.process.p.handlers.onSearch(w)
        s.process.p.handlers.modelChanged()
    def onAttrCancel(w):
        s.process.p.views.output.state.controller.display(s.process.p.process.resultDisplayer.views.container.outputs.layout, True, True)
    def onAttrOk(w):
        s.process.p.process.jc.process.model
        index = s.process.p.process.currentIndex
        val = s.process.p.process.model[index]
        val["attrs"] = s.process.p.process.jc.process.model
        s.process.p.process.jc.handlers.set_content({} )
        s.handlers.onAttrCancel(1)
        s.process.p.handlers.modelChanged()
    opsMap = {"attrs": attrs, "delete": delete, "update": update}
    s = ObjMaker.variablesAndFunction(locals())
    return s
def OpsDropdown():
    p = None
    def update():
        s.process.p.views.addConfirm.outputs.layout.description = "search"
        s.process.p.views.addConfirm.handlers.handle = s.process.p.handlers.onSearch
    def delete():
        s.handlers.update()
    def add():
        s.process.p.views.addConfirm.outputs.layout.description = "add"
        s.process.p.views.addConfirm.handlers.handle = s.process.p.handlers.onAdd
        s.process.p.handlers.displayModelValue()
    def attrs():
        s.handlers.update()
    def handle(w):
        for func in s.process.p.views.opsWid.state.undoers:
            func()
        s.process.p.views.opsWid.state.undoers.clear()
        typ = s.process.p.views.opsWid.outputs.layout.value
        if typ in s.process.opsMap:
            s.process.opsMap[typ]()
    def metaAttrs():
        s.process.p.process.jc.handlers.set_content(s.process.p.process.metaInfo)
        s.process.p.views.output.state.controller.display(s.process.p.process.jc.views.container.outputs.layout, True, True)
        s.process.p.process.jc.views.okBtn.handlers.handle = s.handlers.onMetaAttrsOk
        s.process.p.process.jc.views.cancelBtn.handlers.handle = s.handlers.onMetaAttrsCancel
    def onMetaAttrsOk(w):
        s.process.p.process.metaInfo = s.process.p.process.jc.process.model
        s.process.p.process.jc.handlers.set_content({})
        s.handlers.onMetaAttrsCancel(1)
        s.process.p.handlers.modelChanged()
        s.process.p.handlers.checkFilters()
    def onMetaAttrsCancel(w):
        s.process.p.views.opsWid.outputs.layout.value = "add"
    opsMap = {"add": add, "attrs": attrs, "delete": delete, "update": update, "metaAttrs": metaAttrs}
    s = ObjMaker.variablesAndFunction(locals())
    return s
def ListCRUDWithAttrsAndFilter():
    opsWid = Utils.get_comp({"options": ["add",'update',"delete", "attrs", "metaAttrs"]},IpywidgetsComponentsEnum.Dropdown, className = "w-auto")
    filterWid = Utils.get_comp({"options": ["--no-filter--"]},IpywidgetsComponentsEnum.Dropdown, className = "w-auto")
    textWid = Utils.get_comp({"placeholder":"add word"}, IpywidgetsComponentsEnum.Text, className="w-auto", bind = False)
    addConfirm = Utils.get_comp({"description":"add"}, IpywidgetsComponentsEnum.Button, className="w-auto")
    output = Utils.get_comp({}, ComponentsLib.CustomOutput)
    container = Utils.container([Utils.container([opsWid, textWid, addConfirm, filterWid]), output], className="flex flex-column")
    searcher = SearchComplex()
    resultDisplayer = ResultDisplayers()
    currentIndex = None
    rbo = ResultButtonOps()
    jc = JsonCrud()
    jc.views.label.hide()
    od = OpsDropdown()
    opsWid.state.undoers = []
    metaInfo = {}
    dm = DictionaryModel()
    model = []
    allValues = []
    noFilter = "--no-filter--"
    errorVerbose = False
    def modelChanged():
        pass
    def values():
        return {"values": s.process.allValues, "meta": s.process.metaInfo}
    def set_values(model):
        vals = model["values"]
        for val in vals:
            if "uuid" not in val:
                val["uuid"] = CryptsDB.generateUniqueId()
        s.process.model = vals
        s.process.allValues = s.process.model
        s.process.metaInfo = model["meta"]
        s.handlers.displayModelValue()
        try:
            s.handlers.checkFilters()
        except Exception as e: 
            if s.process.errorVerbose:
                print(e)
            
    def nameFunc(k):
        return k["name"]
    def displayableForm():
        return str([s.handlers.nameFunc(v) for v in s.process.model])
    def displayModelValue():
        s.views.output.state.controller.display(s.handlers.displayableForm(), True)
    def onSearch(w):
        val = s.views.textWid.outputs.layout.value.strip()
        s.process.searcher.process.values = s.process.model
        s.process.searcher.handlers.valFunc = lambda k, v: s.handlers.nameFunc(v)
        res = s.process.searcher.handlers.search("caseless", val, s.process.model)
        s.process.resultDisplayer.handlers.set_results(res, reverseIt=False)
        s.views.output.state.controller.display(s.process.resultDisplayer.views.container.outputs.layout, True, True)
    def onAdd(w):
        val = s.views.textWid.outputs.layout.value.strip()
        if val == "":
            return
            
        uuid = CryptsDB.generateUniqueId()
        sizeBefore = len(s.process.model)
        s.process.allValues.append({"name": val, "uuid": uuid})
        if sizeBefore == len(s.process.model):
            s.process.model.append({"name": val, "uuid": uuid})
        s.views.textWid.outputs.layout.value  = ""
        s.handlers.displayModelValue()
        s.handlers.modelChanged()
    def name_getter(x):
        if type(x) == str:
            return x
        return s.handlers.nameFunc(s.process.searcher.process.values[x])
    def set_file(file):
        s.process.filepath = file
        s.handlers.set_values(SerializationDB.readPickle(file))
        def sync():
            SerializationDB.pickleOut(s.handlers.values(), s.process.filepath) 
        s.handlers.modelChanged = sync
    def newValFunc(val, loc):
        dm = s.process.dm
        dm.s.process.model = val
        if dm.exists(loc):
            return dm.read(loc)
        return ""
    def onChange(w):
        val = s.views.filterWid.outputs.layout.value
        if val is None:
            return
        if val == s.process.noFilter:
            s.process.model = s.process.allValues
        else:
            s.process.dm.s.process.model = s.process.metaInfo
            searches = Array(s.process.dm.read(["filter", "options"])).filter(lambda x: x[0]==val).map(lambda x: x[1:]).array[0]
            s.process.dm.update(["filter", "selected"], val)
            s.process.searcher.process.values = s.process.allValues
            s.process.model = s.process.searcher.handlers.locSearch(searches)
        s.handlers.displayModelValue()
    def checkFilters():
        s.process.dm.s.process.model = s.process.metaInfo
        options = [s.process.noFilter]
        if s.process.dm.exists(["filter", "options"]):
            options += Array(s.process.dm.read(["filter", "options"])).map(lambda x: x[0]).array
        if len(options) > 1:
            s.views.filterWid.show()
            s.views.filterWid.outputs.layout.options = options
        else:
            s.views.filterWid.hide()
        selectedExists = s.process.dm.exists(["filter", "selected"])
        if selectedExists:
            s.views.filterWid.outputs.layout.value = s.process.dm.read(["filter", "selected"])
            s.handlers.onChange(1)
    resultDisplayer.handlers.name_getter = name_getter
    resultDisplayer.views.btns.handlers.handle = rbo.handlers.handle
    addConfirm.handlers.handle = onAdd
    opsWid.handlers.handle = od.handlers.handle
    filterWid.handlers.handle = onChange
    s = ObjMaker.uisOrganize(locals())
    rbo.process.p = s
    searcher.process.parent = s
    od.process.p = s
    od.handlers.handle(1)
    return s

class Main:
    def listCrud(filepath=None, content=None):
        lc = ListCRUDWithAttrsAndFilter()
        if filepath is not None:
            lc.handlers.set_file(filepath)
        if content is not None:
            lc.handlers.set_values(content)
        lc.handlers.checkFilters()
        return lc

