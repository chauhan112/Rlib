from IPython.display import display
from ComparerDB import ComparerDB
from useful.basic import Main as ObjMaker
from timeline.t2023.dep_extractor.dependency_extractor import DicOps
from timeline.t2024.ui_lib.refactored_key_value_adder import Main as KVMain
from timeline.t2024.ui_lib.IpyComponents import IpywidgetsComponentsEnum, Utils
import copy

def NewSearchComponent():
    inputText = Utils.get_comp({"placeholder": "search word or reg"}, IpywidgetsComponentsEnum.Text, bind=False)
    searchType = Utils.get_comp({"options":["--", "reg", "case", "word", "concatenated"]}, IpywidgetsComponentsEnum.Dropdown,
                                bind=False, className="w-auto")
    searchBtn = Utils.get_comp({"description": "search"}, IpywidgetsComponentsEnum.Button, className = "w-auto br-5px")
    selected = Utils.get_comp({"options":[]}, IpywidgetsComponentsEnum.Dropdown, className = "w-auto")
    container = Utils.container([inputText, searchType, searchBtn, selected], className="w-100")
    def update_selected():
        if len(s.views.selected.outputs.layout.options) == 0:
            s.views.selected.hide()
    s = ObjMaker.uisOrganize(locals())
    return s
def SearchFnc():
    values = []
    def sort(res, infos={"field":"key", "reverse": False}):
        """
            sortField: Key|Value
        """
        field = "key"
        reverse = False      
        if "field" in infos:
            field = infos["field"]
        if "reverse" in infos:
            reverse = infos["reverse"]
        if ComparerDB.inCompare(field, "key"):
            return s.handlers.sortThem(res, s.handlers.key_getter, reverse)
        elif ComparerDB.inCompare(field, "value"):
            return s.handlers.sortThem(res, s.handlers.value_getter, reverse)
        else:
            raise IOError("unknown sorting field")       
    def set_values(values):
        s.process.values = values
    def value_getter(ele):
        return str(ele[1][0]["value"])
    def key_getter(ele):
        return ele[0]
    def sortThem(results, func, reverse=False):
        return sorted(results, key=func, reverse=reverse)
    def grouper(groups):
        res = []
        for ele in s.process.values:
            if s.handlers.key_getter(ele) in groups:
                res.append(ele)
        return res
    def search(context):
        """
            context: {type: none|reg|case|word, value: str|list[str](for concatenate), field: key|value}
            context: text (mean {type: none, value: text, field: key})
        """
        field = "key"
        searchType = None
        value = context
        if type(context) == dict:
            value = context["value"]
            if "type" in context and context["type"] != "none":
                searchType = context["type"]
            if "field" in context:
                field = context["field"]
        
        func = None
        if ComparerDB.inCompare(field, "key"):
            func = s.handlers.key_getter
        elif ComparerDB.inCompare(field, "value"):
            func = s.handlers.value_getter
        else:
            raise IOError("unknown field type detected")
        newValFunc = lambda x: x
        reg = False
        case = False
        if searchType is None:
            pass
        elif ComparerDB.inCompare(searchType, "reg"):
            reg = True
        elif ComparerDB.inCompare(searchType, "case"):
            case =True
        elif ComparerDB.inCompare(searchType, "word"):
            reg = True
            newValFunc = lambda x: f"\\b{x}\\b"
        if type(value) == list:
            res2 = s.process.values
            for word in value:
                res2 = s.handlers.search2(newValFunc(word), case, reg, res2, func)
            return res2
        elif type(value) == str:
            return s.handlers.search2(newValFunc(value), case, reg, s.process.values, func)
        else:
            raise IOError("unknown context type detected")
    def search2(word, case, reg, vals, func):
        newRes = []
        for ele in vals:
            if ComparerDB.has(word, func(ele), case, reg):
                newRes.append(ele)
        return newRes
    def set_info(info):
        s.process.info = info
    s = ObjMaker.variablesAndFunction(locals())
    return s
def KeyValueWithSearchAndSort():
    #  search: {selected: "", options: {name: {type: search|group|sort, 
        # value:{type: reg|case|none, value: str|list[str]}(for search)|list[str] (for concate)| (ignore for sort)} | list[lastOption],field: key|value}}
    from timeline.t2024.listCrudWithFilter import SearchComplex
    searchComp = NewSearchComponent()
    container = KVMain.key_val_app_with_meta()
    kvapwm = container
    kvapwm.views.fileOpsRow.pop()
    kvapwm.views.fileOpsRow.pop()
    dropdownLabelForFilter = "--no-filter--"
    opsDropdownLabel = "--no-ops--"
    opsList = Utils.get_comp({"options":[opsDropdownLabel,"ops", "metaOps", "searchKeys"]}, IpywidgetsComponentsEnum.Dropdown, className = "w-auto")
    metaOpsList = Utils.get_comp({"options":[opsDropdownLabel,"ops", "refresh", "insertSearch"]}, IpywidgetsComponentsEnum.Dropdown, className = "w-auto")
    kvapwm.views.fileOpsRow.append(opsList)
    undoers = []
    undoersMeta = []
    kvapwm.process.metaKeyValue.process.kvsForMeta.views.fileOpsRow.pop()
    kvapwm.process.metaKeyValue.process.kvsForMeta.views.fileOpsRow.pop()
    kvapwm.process.metaKeyValue.process.kvsForMeta.views.fileOpsRow.append(metaOpsList)
    searchFunc = SearchFnc()
    searchFunc2 = SearchComplex()
    prev_funcs = ObjMaker.namespace()
    firstTimeSelected= False
    
    def dropDownSelected(w):
        for func in s.process.undoers:
            func()
        s.process.undoers.clear()
        val = opsList.outputs.layout.value
        if val == s.process.opsDropdownLabel:
            kvapwm.views.outputArea.outputs.layout.clear_output()
        elif val == "ops":
            kvapwm.views.opsCheckbox.outputs.layout.value = True
            s.process.undoers.append(lambda : set_val(kvapwm.views.opsCheckbox, False))
        elif val == "metaOps":
            kvapwm.views.metaOpsCheckbox.outputs.layout.value = True
            s.process.undoers.append(lambda : set_val(kvapwm.views.metaOpsCheckbox, False))
        elif val == "searchKeys":
            with kvapwm.views.outputArea.outputs.layout:
                display(s.process.searchComp.views.container.outputs.layout)
            s.process.undoers.append(kvapwm.views.outputArea.outputs.layout.clear_output)
    def set_val(comp,val):
        comp.outputs.layout.value = val
    def dropDownSelectedMeta(w):
        kvMeta = kvapwm.process.metaKeyValue.process.kvsForMeta
        for func in s.process.undoersMeta:
            func()
        s.process.undoersMeta.clear()
        val = s.views.metaOpsList.outputs.layout.value
        comp = kvapwm.process.metaKeyValue.process.kvsForMeta
        if val == s.process.opsDropdownLabel:
            comp.views.outputArea.outputs.layout.clear_output()
        elif val == "ops":
            comp.views.opsCheckbox.outputs.layout.value = True
            s.process.undoersMeta.append(lambda : set_val(comp.views.opsCheckbox, False))
        elif val == "refresh":
            comp.views.metaOpsCheckbox.outputs.layout.value = True
            s.process.undoersMeta.append(lambda : set_val(comp.views.metaOpsCheckbox, False))
        elif val == "insertSearch":
            key2Add = "--option--"
            if not kvMeta.process.model._model.exists(["searchAndSort", "options", key2Add]):
                value = {"type": "search|group|sort|loc", "value": "{type: reg|case|none, value: str|list[str], field: key|value}(for search) | \nlist[str] (for group)| \n{field: key|value, reverse=yes|no}(for sort)} | list[lastOption]"}
                examples = {"search keys": {"type":"search", "value": "xyz"}, "concate search": {"type":"search", 
                    "value": {"type": "reg", "value": ["xyz", "askds"], "field": "value"}}, "sort keys": {"type": "sort", "value": {"field":"key", "reverse":True}},
                    "search and sort": [{"type": "search", "value": {"type": "reg", "value": "lol", "field": "key"}}, {"type":"sort", "value": {"field": "key"}}]}
                s.handlers.save(["searchAndSort", "options", key2Add], value)
                s.handlers.save(["searchAndSort", "examples"], examples)
    def newDirList():
        res = s.process.prev_funcs.dirList()
        curMeta = kvapwm.process.model.read_meta()
        if "searchAndSort" in curMeta:
            options = [s.process.dropdownLabelForFilter] + list(curMeta["searchAndSort"]["options"].keys())
            if len(options) != 0:
                s.process.searchComp.views.selected.show()
                s.process.searchComp.views.selected.outputs.layout.options = options
            else:
                s.process.searchComp.views.selected.hide()
            if "selected" in curMeta["searchAndSort"]:
                name = curMeta["searchAndSort"]["selected"]
                if name == s.process.dropdownLabelForFilter:
                    return res
                s.process.firstTimeSelected = True
                s.process.searchComp.views.selected.outputs.layout.value = name
                s.process.firstTimeSelected = False
                res = s.handlers.getSelectedResults(res, curMeta["searchAndSort"]["options"][name])
        else:
            s.process.searchComp.views.selected.hide()
        return res
    def getSelectedResults(res, infos):
        if type(infos) == list:
            nress = res
            for ele in infos:
                nress = s.handlers.search_for_setting(ele, nress)
            return nress
        return s.handlers.search_for_setting(infos,res)
        s.process.firstTimeSelected = False
    def search_for_setting(infos, res):
        s.process.searchFunc.handlers.set_values(res)
        typ = infos["type"]
        value = infos["value"]
        if typ == "search":
            return s.process.searchFunc.handlers.search(value)
        elif typ == "sort":
            return s.process.searchFunc.handlers.sort(res, value)
        elif typ == "group":
            return s.process.searchFunc.handlers.grouper(value)
        elif typ == "loc":
            s.process.searchFunc2.process.values = res
            newVal = copy.deepcopy(value)
            for k in newVal:
                k[1][0] = [1, 0] + k[1][0]
            return s.process.searchFunc2.handlers.locSearch(newVal)
    def dropDownSelectedSearch(w):
        optValue = s.process.searchComp.views.selected.outputs.layout.value
        if optValue == s.process.dropdownLabelForFilter:
            res = s.process.prev_funcs.dirList()
            s.handlers.newRender(res)
        else:
            content = s.handlers.read_meta(["searchAndSort","options", optValue])
            res = s.process.prev_funcs.dirList()
            res = s.handlers.getSelectedResults(res, content)
            s.handlers.newRender(res)
        if not s.process.firstTimeSelected:
            kvapwm.process.model.write_meta(["searchAndSort", "selected"], optValue, True)
    def onSearched(w):
        txt = s.process.searchComp.views.inputText.outputs.layout.value.strip()
        typ = s.process.searchComp.views.searchType.outputs.layout.value
        if typ != "--":
            txt = {"value": txt, "type": typ}
        res = s.process.prev_funcs.dirList()
        res = s.handlers.getSelectedResults(res, {"type": "search", "value": txt})
        s.handlers.newRender(res)
    def save(loc, value):
        kvMeta = kvapwm.process.metaKeyValue.process.kvsForMeta
        kvMeta.process.model.write(loc, value)
        kvMeta.handlers.render_keys()
    def read_meta(loc=[]):
        curMeta = kvapwm.process.model.read_meta()
        return DicOps.get(curMeta,loc)
    def newRender(keys):
        keyValMap = {val[0]: val[1] for val in keys}
        s.process.container.process.keysDisplayer.handlers.set_results(keys, s.process.container.process.keysDisplayer.process.pageNr)
        s.process.container.process.keysDisplayer.keyValMap = keyValMap
    prev_funcs.dirList = kvapwm.process.model.dirList
    kvapwm.process.model.dirList = newDirList
    metaOpsList.handlers.handle = dropDownSelectedMeta
    opsList.handlers.handle = dropDownSelected
    searchComp.views.selected.handlers.handle = dropDownSelectedSearch
    searchComp.views.searchBtn.handlers.handle = onSearched
    s = ObjMaker.uisOrganize(locals())
    return s
