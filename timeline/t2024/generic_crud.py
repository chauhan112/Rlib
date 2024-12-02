from timeline.t2024.Array import Array
from timeline.t2024.generic_logger.generic_loggerV3 import ResultDisplayers
from timeline.t2024.generic_logger.generic_loggerV4 import SearchAndCrudView, FormGeneratorV2
from timeline.t2024.tailwind.twcrudOps import DictionaryModel
from timeline.t2024.listCrudWithFilter import SearchComplex
from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from timeline.t2024.ui_lib.refactored_key_value_adder import Main as KVMain
from basic import Main as ObjMaker
import copy
from ComparerDB import ComparerDB
import json
from timeline.t2024.antif import ExecFilterers
from timeline.t2023.generic_logger.components import GComponent


def BreadCrumb():
    css = """
        .bcrumb:before {
            display: inline-block;
            padding-right: .5rem;
            padding-left: .5rem;
            color: #6c757d;
            content: "/";
        }
        
        .bcrumb{
            all:revert;
            padding: 0px;
            margin: 0;
            background: unset;
            color: #0056b3;
            text-decoration-line: underline;
            border: 0;
            padding-right: .25rem;
            cursor: pointer;
            font-size: var(--jp-widgets-font-size);
            line-height: var(--jp-widgets-inline-height);
            display: inline;
            min-width: 50px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, 
                "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
            text-overflow: ellipsis;
        }
        .bcrumb:active{
            box-shadow: unset;
            color: var(--jp-ui-font-color1);
            background-color: unset;
        }
        
        .bcrumb:hover:enabled{
            box-shadow: unset;
        }
        
        .bcrumb:focus:enabled{
            outline: 0px solid var(--jp-widgets-input-focus-border-color);
        }
        .bcrumb:focus-visible {
            outline: 0px solid var(--jp-accept-color-active, var(--jp-brand-color1));
            outline-offset: unset;
        }
        
        
        """
    wcss = Utils.get_comp({},ComponentsLib.CSSAdder, className = "w-auto bcrumb", customCss= css)
    label = Utils.get_comp({"value": "location : "}, IpywidgetsComponentsEnum.Label, className = "w-auto")
    dotDotBtn = Utils.get_comp({"icon": "arrow-circle-left"}, IpywidgetsComponentsEnum.Button, className="w-auto")
    btns = [Utils.get_comp({"description":"add"},IpywidgetsComponentsEnum.Button, className = "w-auto bcrumb", index=i) for i in range(10)]
    btnWid = Utils.container(btns)
    container = Utils.container([label, dotDotBtn, btnWid, wcss])
    debug = None
    def goBack(w):
        pass
    def onClick(w):
        s.process.debug = w
    def set_location(loc):
        for i, btn in enumerate(s.process.btns):
            if i < len(loc):
                btn.show()
                btn.outputs.layout.description = loc[i]
            else:
                btn.hide()
    btnWid.handlers.handle = onClick
    dotDotBtn.handlers.handle = goBack
    s = ObjMaker.uisOrganize(locals())
    return s
def BasicForm():
    opsWid = Utils.get_comp({"options": ["text",'textarea',"dict", "eval", "json"]},IpywidgetsComponentsEnum.Dropdown, className = "w-auto")
    textWid = Utils.get_comp({"placeholder":"add word"}, IpywidgetsComponentsEnum.Text, className="w-auto", bind = False)
    textArea = Utils.get_comp({"placeholder":"add word"}, IpywidgetsComponentsEnum.Textarea, className="hmin-200px w-auto", bind = False)
    keyVal = KVMain.key_val_normal()
    outArea = Utils.get_comp({}, IpywidgetsComponentsEnum.Output, className="w-auto", bind = False)
    container = Utils.container([opsWid, outArea], className="flex flex-column")
    def onChange(w):
        val = s.views.opsWid.outputs.layout.value
        toDisplay = None
        if val == "text":
            toDisplay = s.views.textWid.outputs.layout
        elif val in ["textarea", "eval","json"]:
            toDisplay = s.views.textArea.outputs.layout
        elif val == "dict":
            toDisplay = s.process.keyVal.process.container.views.container.outputs.layout
        s.views.outArea.outputs.layout.clear_output()
        with s.views.outArea.outputs.layout:
            display(toDisplay)
    def value():
        typ = s.views.opsWid.outputs.layout.value
        if typ == "text":
            return typ, s.views.textWid.outputs.layout.value
        elif typ == "textarea":
            return typ, s.views.textArea.outputs.layout.value
        elif typ == "dict":
            return typ, copy.deepcopy(s.process.keyVal.handlers.readAll())
        elif typ == "eval":
            vl = s.views.textArea.outputs.layout.value
            return typ, eval(vl)
        elif typ == "json":
            vl = s.views.textArea.outputs.layout.value
            return typ, json.loads(vl)
    def set_value(typ, val):
        if typ == "text":
            s.views.textWid.outputs.layout.value = val
        elif typ == "textarea":
            s.views.textArea.outputs.layout.value = val
        elif typ == "dict":
            s.process.keyVal.handlers.set_dictionary(val)
        elif typ == "eval":
            s.views.textArea.outputs.layout.value = str(val)
        elif typ == "json":
            s.views.textArea.outputs.layout.value = json.dumps(val)
    def reset(typ):
        if typ == "text":
            s.views.textWid.outputs.layout.value = ""
        elif typ in ["textarea", "eval","json"]:
            s.views.textArea.outputs.layout.value = ""
        elif typ == "dict":
            s.process.keyVal.handlers.set_dictionary({})
    def resetAll():
        s.views.textWid.outputs.layout.value = ""
        s.views.textArea.outputs.layout.value = ""
        s.process.keyVal.handlers.set_dictionary({})
    opsWid.handlers.handle = onChange
        
    s = ObjMaker.uisOrganize(locals())
    onChange(1)
    return s
def Model():
    dicModel = DictionaryModel()
    def add_data(val):
        index = s.process.dicModel.read(["meta", "current-key"])
        s.process.dicModel.add(["data", index], val)
        s.process.dicModel.update(["meta", "current-key"], index + 1)
    def update_data(key, value):
        s.process.dicModel.update(["data", key], value)
    def read_data(key):
        return s.process.dicModel.read(["data", key])
    def delete_data(key):
        s.process.dicModel.delete(["data", key])
    def set_data(data):
        dm = s.process.dicModel
        s.process.data = data
        dm.s.process.model = data
        if not dm.exists(["data"]):
            dm.add(["data"], {})
            dm.add(["meta", "current-key"], 0)
        if not dm.exists(["meta"]):
            dm.add(["meta", "current-key"], 0)
    def readAll():
        return s.process.dicModel.read(["data"]) 
    s = ObjMaker.variablesAndFunction(locals())
    set_data({})
    return s
def SearchWithCases():
    locSearcher = SearchComplex()
    prevCompare = locSearcher.handlers.compare
    values = []
    def forAnyCompare(typ, word, key, targetWord):
        return word.lower() in str(targetWord).lower()
    def forCaseCompare(typ, word, key, targetWord):
        return word in str(targetWord)
    def forRegCompare(typ, word, key, targetWord):
        return ComparerDB.has(word, str(targetWord), reg=True)
    def search(typ, word):
        s.process.locSearcher.process.values = s.process.values
        s.process.locSearcher.handlers.valFunc = s.process.locSearcher.handlers.default_val_func
        if typ == "reg":
            s.process.locSearcher.handlers.compare = s.handlers.forRegCompare
        elif typ == "any":
            s.process.locSearcher.handlers.compare = s.handlers.forAnyCompare
        elif typ == "case":
            s.process.locSearcher.handlers.compare = s.handlers.forCaseCompare
        elif typ == "word":
            s.process.locSearcher.handlers.compare = s.handlers.forRegCompare
            return s.process.locSearcher.handlers.search(typ, f"\\b{word}\\b")
        elif typ == "concatenated": # any search multiple times
            s.process.locSearcher.handlers.compare = s.handlers.forAnyCompare
            res = s.process.values
            for wo in word:
                res = s.process.locSearcher.handlers.search("any", wo, res)
            return res
        elif typ == "loc":
            s.process.locSearcher.handlers.compare = s.handlers.prevCompare
            res = s.process.locSearcher.handlers.locSearch(word, False)
            return res
        return s.process.locSearcher.handlers.search(typ, word)
    s = ObjMaker.variablesAndFunction(locals())
    return s
def CRUDFilter():
    scv = SearchAndCrudView()
    scv.process.searchComponent.views.searchType.outputs.layout.options = ["any", "reg", "case", "word", "concatenated", "loc"]
    container = scv.views.container
    logger_name = "default"
    form = formMaker()
    model = Model()
    basicForm = BasicForm()
    searcher = SearchWithCases()
    btn = Utils.get_comp({"description":"add"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    current_form = None
    resultDisplayer = ResultDisplayers()
    undoers = ObjMaker.namespace()
    undoers.radio = []
    undoers.results = []
    def btnMaker(ele):
        return Utils.get_comp({"description": s.process.resultDisplayer.handlers.name_getter(ele)}, 
                              IpywidgetsComponentsEnum.Button, className="mw-100px w-auto")
    def get_form():
        if s.process.model.process.dicModel.exists(["meta", "structure"]):
            pstr = s.process.model.process.dicModel.read(["meta", "structure"])
            pstr = {k: pstr[k] for k in sorted(pstr, key =lambda x: pstr[x]["order"])}
            s.process.form.handlers.set_structure(pstr)
            s.process.current_form = ("fgv2", s.process.form)
        else:
            s.process.current_form = ("basic", s.process.basicForm)
        return s.process.current_form
    def goToRead():
        s.process.scv.process.crudView.views.crudView.outputs.layout.value = "r"
    def onCreateForStructuredForm(w):
        if not s.process.form.handlers.is_empty():
            val = s.process.form.handlers.value()
            s.process.model.handlers.add_data(val)
            s.process.form.handlers.reset()
            s.handlers.goToRead()
    def onSearch(w):
        typ = s.process.scv.process.searchComponent.views.searchType.outputs.layout.value
        word = s.process.scv.process.searchComponent.views.inputText.outputs.layout.value
        s.process.searcher.process.values = s.process.model.handlers.readAll()
        if typ in ["loc", "concatenated"]:
            word = eval(word)
        res = s.process.searcher.handlers.search(typ, word)
        s.process.resultDisplayer.handlers.set_results(res)
        s.process.scv.views.keysOut.state.controller.display(s.process.resultDisplayer.views.container.outputs.layout, True, True)
    def undo(fs):
        for f in fs:
            f()
        fs.clear()
    def onChange(w):
        s.handlers.undo(s.process.undoers.radio)
        ops = s.process.scv.process.crudView.views.crudView.outputs.layout.value
        if ops == "c":
            typ, frm = s.handlers.get_form()
            s.process.scv.process.searchComponent.views.container.hide()
            s.process.scv.views.resultsOut.state.controller.clear()
            if typ == "basic":
                s.process.scv.views.keysOut.state.controller.display(s.process.basicForm.views.container.outputs.layout, True, True)
                s.process.scv.views.keysOut.state.controller.display(s.views.btn.outputs.layout, False, True)
                s.views.btn.handlers.handle = s.handlers.onCreateForBasic
                s.process.basicForm.handlers.onChange(1)
            else:
                frm.handlers.get_layout()
                s.process.form.handlers.reset()
                s.process.scv.views.keysOut.state.controller.display(frm.handlers.get_layout(), True, True)
                frm.handlers.add_clicked = s.handlers.onCreateForStructuredForm
            s.process.undoers.radio.append(s.process.scv.views.keysOut.state.controller.clear)
        else:
            s.process.scv.process.searchComponent.views.container.show()
            s.process.undoers.radio.append(s.process.scv.views.resultsOut.state.controller.clear)
    def onCreateForBasic(w):
        typ, val = s.process.basicForm.handlers.value()
        s.process.model.handlers.add_data((typ, val))
        s.process.basicForm.handlers.reset(typ)
        s.handlers.goToRead()
    def get_name(key):
        if key == "":
            return key
        data = s.process.model.handlers.readAll()
        dp = data[key] # the next three lines would need to be deleted (incase of structured only)
        val = dp 
        if type (dp) == tuple and len(dp) == 2:
            val = dp[1]
        if type(val) == str:
            return val[:20]
        elif type(val) == dict:
            for key in val:
                v = val[key]
                if type(v) == str:
                    return v[:20]
            return str(val)[:20]
        else:
            return str(val)[:20]
    def onBtnClickOfResultDisplayers(w):
        s.handlers.result_btn_prefunc(w)
        op = s.process.scv.process.crudView.views.crudView.outputs.layout.value
        if op == "r":
            s.handlers.read_data(w)
        elif op == "u":
            s.handlers.update_data(w)
        elif op == "d":
            s.handlers.delete_data(w)
    def result_btn_prefunc(w):
        s.handlers.undo(s.process.undoers.results)
        s.process.current_button = w
        s.process.current_button.add_class("selected")
        s.process.undoers.results.append(s.handlers.remove_btn_css)
        s.process.undoers.results.append(s.process.scv.views.resultsOut.state.controller.clear)
    def remove_btn_css():
        if s.process.current_button is not None:
            s.process.current_button.remove_class("selected")
    def update_data(w):
        vals = s.handlers.get_info_current_selected_btn(w)
        data = s.handlers.get_info_current_selected_btn(s.process.current_button)
        rctrl = s.process.scv.views.resultsOut.state.controller
        if type(vals) == tuple and len(vals) == 2:
            s.views.btn.outputs.layout.description = "update"
            s.process.basicForm.handlers.resetAll()
            s.process.basicForm.handlers.set_value(*data)
            s.process.basicForm.views.opsWid.outputs.layout.value = data[0]
            rctrl.display(s.process.basicForm.views.container.outputs.layout, True, True)
            rctrl.display(s.views.btn.outputs.layout, False, True)
            s.views.btn.handlers.handle = s.handlers.onUpdateBasic
            s.process.basicForm.handlers.onChange(1)
            return 
        
        typ, frm = s.handlers.get_form()
        if typ == "fgv2":
            rctrl.display(frm.handlers.get_layout(), True, True)
            frm.handlers.set_values(data)
            frm.handlers.add_clicked = s.handlers.onUpdateStructure
    def delete_data(w):
        s.views.btn.outputs.layout.description = "confirm"
        s.views.btn.handlers.handle = s.handlers.delete_confirm
        s.process.scv.views.resultsOut.state.controller.display(s.views.btn.outputs.layout, True, True)
    def delete_confirm(w):
        btnIndex = s.process.current_button._parent.state.index
        key = s.process.resultDisplayer.process.data[btnIndex]
        s.process.model.handlers.delete_data(key)
        s.process.current_button._parent.hide()
        s.process.scv.views.resultsOut.state.controller.clear()
    def onUpdateBasic(w):
        s.handlers.updateBoth(s.process.basicForm.handlers.value)
    def updateBoth(valFunc):
        btnIndex = s.process.current_button._parent.state.index
        key = s.process.resultDisplayer.process.data[btnIndex]
        vals = valFunc()
        s.process.model.handlers.update_data(key, vals )
        s.process.current_button.description = s.handlers.get_name(key)
        s.process.scv.views.resultsOut.state.controller.clear()
    def onUpdateStructure(w):
        s.handlers.updateBoth(s.process.form.handlers.value)
    def get_info_current_selected_btn(w):
        btnIndex = w._parent.state.index
        index = s.process.resultDisplayer.process.data[btnIndex]
        vals = s.process.searcher.process.values[index]
        return vals
    def read_data(w):
        vals = s.handlers.get_info_current_selected_btn(w)
        if type(vals) == dict:
            res = ""
            for ke in vals:
                res +=  ke + ": " +  str(vals[ke]) + "\n"
                res += ("-"*40) + "\n"
            s.process.scv.views.resultsOut.state.controller.display(res, True, printIt=True)
        else:
            s.process.scv.views.resultsOut.state.controller.display(vals, True, printIt=True)
    scv.process.crudView.views.crudView.handlers.handle = onChange
    scv.process.searchComponent.views.searchBtn.handlers.handle = onSearch
    resultDisplayer.views.btns.handlers.handle = onBtnClickOfResultDisplayers
    resultDisplayer.handlers.btnMaker = btnMaker
    resultDisplayer.handlers.name_getter = get_name
    s = ObjMaker.uisOrganize(locals())
    return s
def ToolFeatures():
    deleteBtn = Utils.get_comp({"description":"delete"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    filterCrudBtn = Utils.get_comp({"description":"filters crud"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    parent = None
    btns = Utils.container([deleteBtn, filterCrudBtn])
    filtersCrud = CRUDFilter()
    filterDropdown = Utils.get_comp({"options": []},IpywidgetsComponentsEnum.Dropdown, className = "w-auto")
    btn = Utils.get_comp({"description":"save and goback"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    filtersComp = Utils.container([btn, filtersCrud.views.container], className="flex flex-column")
    def onChange(w):
        p = s.process.parent
        ops = p.process.scv.process.crudView.views.crudView.outputs.layout.value
        if ops == "t":
            p.process.scv.process.searchComponent.views.container.hide()
            p.process.scv.views.keysOut.state.controller.display(s.views.btns.outputs.layout, True, True)
            p.process.undoers.radio.append(p.process.scv.views.keysOut.state.controller.clear)
        else:
            s.process.prev_onChange(w)
        if ops == "r":
            s.process.resultFunc = p.handlers.read_data
        elif ops == "u":
            s.process.resultFunc = p.handlers.update_data
    def onSaveAndApply(w):
        v = s.process.filtersCrud.process.model.handlers.readAll()
        p = s.process.parent
        p.process.model.process.dicModel.update(["meta", "filters", "data"], v)
        s.handlers.onChange(1)
        s.handlers.setup_filters()
    def onFilter(w):
        p = s.process.parent
        s.process.filtersCrud.process.model.handlers.set_data({})
        s.process.filtersCrud.process.model.process.dicModel.add(["meta", "structure"], {'created on': {'type': 'DateTime',
           'info': {'auto': True, 'disabled': True},
           'order': 1},
          'modified-on': {'type': 'DateTime',
           'info': {'auto': True, 'auto-edit': True},
           'order': 2},
          'name': {'type': 'Text', 'info': {}, 'order': 2},                                                             
          'typ': {'type': 'Options',
              'info': {'options': p.process.scv.process.searchComponent.views.searchType.outputs.layout.options, 'value': 'any'},
              'order': 3},
          'word': {'type': 'LargeText', 'info': {}, 'order': 4}})
        s.views.btn.handlers.handle = s.handlers.onSaveAndApply
        if p.process.model.process.dicModel.exists(["meta", "filters", "data"]):
            fil = p.process.model.process.dicModel.read(["meta", "filters", "data"])
            for k in fil:
                vv = fil[k]
                s.process.filtersCrud.process.model.handlers.add_data(vv)
        p.process.scv.views.keysOut.state.controller.display(s.views.filtersComp.outputs.layout, True, True)
    def onDelete(w):
        p = s.process.parent
        p.process.scv.process.searchComponent.views.container.show()
        p.process.scv.views.keysOut.state.controller.clear()
        p.process.scv.views.resultsOut.state.controller.clear()
        p.process.undoers.radio.append(p.process.scv.views.resultsOut.state.controller.clear)
        s.process.resultFunc = p.handlers.delete_data
    def set_up():
        p = s.process.parent
        p.process.scv.process.crudView.views.crudView.outputs.layout.options = ('r', 'c', 'u', 't')
        s.process.prev_onChange = p.process.scv.process.crudView.views.crudView.handlers.handle
        p.process.scv.process.crudView.views.crudView.handlers.handle = s.handlers.onChange
        s.process.prevResultBtnClick = p.process.resultDisplayer.views.btns.handlers.handle
        p.process.resultDisplayer.views.btns.handlers.handle = s.handlers.onResultBtnClicked
        s.process.resultFunc = p.handlers.read_data
        p.process.scv.process.searchComponent.views.container.append(s.views.filterDropdown)
        s.views.filterDropdown.handlers.handle = s.handlers.onFilterChange
        s.handlers.setup_filters()
    def onResultBtnClicked(w):
        p = s.process.parent
        p.handlers.undo(p.process.undoers.results)
        p.process.current_button = w
        p.process.current_button.add_class("selected")
        p.process.undoers.results.append(p.handlers.remove_btn_css)
        s.process.resultFunc(w)
        p.process.undoers.results.append(p.process.scv.views.resultsOut.state.controller.clear)
    def setup_filters():
        p = s.process.parent
        if p.process.model.process.dicModel.exists(["meta", "filters", "data"]):
            lf = p.process.model.process.dicModel.read(["meta", "filters", "data"])
            s.views.filterDropdown.show()
            s.views.filterDropdown.outputs.layout.options = [("--", -1)] + Array(lf).map(lambda x: (lf[x]["name"], x)).array
            if p.process.model.process.dicModel.exists(["meta", "filters", "selected"]):
                s.views.filterDropdown.outputs.layout.value = p.process.model.process.dicModel.read(["meta", "filters", "selected"])
        else:
            s.views.filterDropdown.hide()
    def onFilterChange(w):
        p = s.process.parent
        val = s.views.filterDropdown.outputs.layout.value
        model = p.process.model.process.dicModel
        scv = p.process.scv.process.searchComponent.views
        if not model.exists(["meta", "filters", "selected"]):
            model.add(["meta", "filters", "selected"], val)
        else:
            model.update(["meta", "filters", "selected"], val)
        if val < 0:
            scv.inputText.outputs.layout.value = ""
            scv.searchType.outputs.layout.value = "any"
            return 
        data = model.read(["meta", "filters", "data", val])
        scv.inputText.outputs.layout.value = data["word"]
        scv.searchType.outputs.layout.value = data["typ"]
        
    deleteBtn.handlers.handle = onDelete
    filterCrudBtn.handlers.handle = onFilter
    s = ObjMaker.uisOrganize(locals())
    return s
def CustomRenderer():
    toggler = Utils.get_comp({"options": ["default",'custom']}, IpywidgetsComponentsEnum.ToggleButtons, className = "w-auto")
    customRenderBtn = Utils.get_comp({"description":"custom renderer crud"}, IpywidgetsComponentsEnum.Button, className = "w-auto")
    saveAndApply = Utils.get_comp({"description":"save and apply"}, IpywidgetsComponentsEnum.Button, className = "w-auto")
    cusCrd = CRUDFilter()
    execCode = ExecFilterers()
    parent = None
    container = Utils.container([saveAndApply, cusCrd.views.container], className = "flex flex-column")
    struc = {'created on': {'type': 'DateTime',
           'info': {'auto': True, 'disabled': True},
           'order': 1},
          'modified-on': {'type': 'DateTime',
           'info': {'auto': True, 'auto-edit': True},
           'order': 2},
            'typ': {'type': 'Options',
              'info': {'options': ["read", "create", "update", "delete"], 'value': 'any'},
              'order': 3},
            'value': {'type': 'LargeText', 'info': {}, 'order': 3}}
    opsMapp = {
            "r": "read",
            "c": "create",
            "u": "update",
            "d": "delete",
            "t": "tools"
        }
    locInMeta = ["meta", "custom-renderer", "data"]
    def set_up():
        p = s.process.parent
        s.process.cusCrd.process.model.process.dicModel.add(["meta", "structure"], s.process.struc)
        s.process.parent.process.tools.views.btns.append(s.views.customRenderBtn)
        s.views.customRenderBtn.handlers.handle = s.handlers.onCustomRenderBtnClick
        p.process.scv.views.customToggler = s.views.toggler
        resultOut = p.process.scv.views.container.pop()
        p.process.scv.views.container.append(p.process.scv.views.customToggler)
        p.process.scv.views.container.append(resultOut)
        p.process.resultDisplayer.views.btns.handlers.handle = s.handlers.onResultsBtnClick
        s.views.toggler.handlers.handle = s.handlers.onToggled
        s.views.toggler.hide()
        s.process.prev_onChange = p.process.scv.process.crudView.views.crudView.handlers.handle
        p.process.scv.process.crudView.views.crudView.handlers.handle = s.handlers.newOnChange
    def newOnChange(w):
        p = s.process.parent
        s.views.toggler.hide()
        p.process.scv.views.resultsOut.state.controller.clear()
        s.process.prev_onChange(w)
    def newExecute(key, content):
        ec = s.process.execCode
        if key not in ec.process.instances:
            ec.process.instances[key] = ec.handlers.load(content)()
        ins = ec.process.instances[key]
        return ins
    def onToggled(w):
        p = s.process.parent
        crd = p.process.scv.process.crudView.views.crudView.outputs.layout.value
        if s.views.toggler.outputs.layout.value == "default":
            p.process.tools.process.resultFunc(p.process.current_button)
        else:
            customRendering = s.handlers.newExecute(crd, s.handlers.read(crd))
            vals = p.handlers.get_info_current_selected_btn(p.process.current_button)
            customRendering.handlers.set_data(vals, p)
            p.process.scv.views.resultsOut.state.controller.display(customRendering.views.container.outputs.layout, True, True)
    def onCustomRenderBtnClick(w):
        p = s.process.parent
        s.process.cusCrd.process.model.handlers.set_data({})
        s.process.cusCrd.process.model.process.dicModel.add(["meta", "structure"], s.process.struc)
        s.views.saveAndApply.handlers.handle = s.handlers.onSaveAndApply
        if p.process.model.process.dicModel.exists(s.process.locInMeta.copy()):
            fil = p.process.model.process.dicModel.read(s.process.locInMeta.copy())
            for k in fil:
                vv = fil[k]
                s.process.cusCrd.process.model.handlers.add_data(vv)
        p.process.scv.views.keysOut.state.controller.display(s.views.container.outputs.layout, True, True)
    def onSaveAndApply(w):
        v = s.process.cusCrd.process.model.handlers.readAll()
        p = s.process.parent
        p.process.model.process.dicModel.update(s.process.locInMeta.copy(), v)
        p.process.scv.process.crudView.views.crudView.handlers.handle(1)
        s.process.execCode.process.instances.clear()
    def onResultsBtnClick(w):
        p = s.process.parent
        p.handlers.result_btn_prefunc(w)
        crd = p.process.scv.process.crudView.views.crudView.outputs.layout.value
        s.views.toggler.hide()
        if s.handlers.exists(crd):
            s.views.toggler.show()
            s.handlers.onToggled(1)
        else:
            p.process.tools.process.resultFunc(w)
    def exists(crd):
        p = s.process.parent
        if p.process.model.process.dicModel.exists(s.process.locInMeta.copy()):
            data = p.process.model.process.dicModel.read(s.process.locInMeta.copy())
            for k in data:
                val = data[k]
                if val["typ"] == s.process.opsMapp[crd]:
                    return True
        return False
    def read(crd):
        p = s.process.parent
        data = p.process.model.process.dicModel.read(s.process.locInMeta.copy())
        for k in data:
            val = data[k]
            if val["typ"] == s.process.opsMapp[crd]:
                return val["value"]
    
    s = ObjMaker.uisOrganize(locals())
    return s
def ViewRenderer():
    cr = CustomRenderer()
    container = cr.views.container
    parent = None
    cr.views.customRenderBtn.outputs.layout.description = "view renderer crud"
    cr.process.locInMeta = ["meta", "view-renderer", "data"]
    def set_up():
        cr = s.process.cr
        p = s.process.parent
        cr.process.parent = p
        cr.process.cusCrd.process.model.process.dicModel.add(["meta", "structure"], cr.process.struc)
        p.process.tools.views.btns.append(cr.views.customRenderBtn)
        cr.views.customRenderBtn.handlers.handle = cr.handlers.onCustomRenderBtnClick
        x = p.process.scv.views.searchWithResults.pop()
        y = p.process.scv.views.searchWithResults.pop()
        p.process.scv.views.searchWithResults.append(s.process.cr.views.toggler)
        p.process.scv.views.searchWithResults.append(y)
        p.process.scv.views.searchWithResults.append(x)
        cr.views.toggler.handlers.handle = s.handlers.onToggled
        cr.views.toggler.hide()
        s.process.prev_onChange = p.process.scv.process.crudView.views.crudView.handlers.handle
        p.process.scv.process.crudView.views.crudView.handlers.handle = s.handlers.newOnChange
    def newOnChange(w):
        p = s.process.parent
        p.handlers.undo(p.process.undoers.radio)
        cr = s.process.cr
        crd = p.process.scv.process.crudView.views.crudView.outputs.layout.value
        cr.views.toggler.hide()
        if cr.handlers.exists(crd):
            cr.views.toggler.show()
            s.handlers.onToggled(1)
        else:
            s.process.prev_onChange(w)
        
    def onToggled(w):
        p = s.process.parent
        cr = s.process.cr
        crd = p.process.scv.process.crudView.views.crudView.outputs.layout.value
        p.process.scv.views.keysOut.state.controller.clear()
        p.process.scv.views.resultsOut.state.controller.clear()
        if cr.views.toggler.outputs.layout.value == "default":
            s.process.prev_onChange(w)
            p.process.scv.process.searchComponent.views.container.show()
        else:
            customRendering = cr.handlers.newExecute(crd, cr.handlers.read(crd))
            allData = p.process.model.handlers.readAll()
            p.process.scv.process.searchComponent.views.container.hide()
            customRendering.handlers.set_data(allData, p)
            p.process.scv.views.keysOut.state.controller.display(customRendering.views.container.outputs.layout, True, True)
        
    s = ObjMaker.uisOrganize(locals())
    return s
def StructureCrud():
    strucBtn = Utils.get_comp({"description":"structure crud"},IpywidgetsComponentsEnum.Button, className = "w-auto")    
    parent = None
    filtersCrud = CRUDFilter()
    saveAndApply = Utils.get_comp({"description":"save and apply"}, IpywidgetsComponentsEnum.Button, className = "w-auto")
    container = Utils.container([saveAndApply, filtersCrud.views.container], className="flex flex-column")
    locInMeta = ["meta", "structure"]
    struc = {'name': {'type': 'Text', 'info': {}, 'order': 2},
     'type': {'type': 'Options',
      'info': {'options': ['Text',
        'LargeText',
        'Checkbox',
        'Options',
        'Date',
        'Time',
        'DateTime',
        'KeyValuesPair',
        'MultipleSelect',
        'Boolean',
        'Crud']},
      'order': 3},
     'order': {'type': 'Text', 'info': {}, 'order': 4},
     'auto-edit': {'type': 'Checkbox', 'info': {'value': True}, 'order': 5},
     'auto': {'type': 'Checkbox', 'info': {}, 'order': 6},
     'disabled': {'type': 'Checkbox', 'info': {}, 'order': 7},
     'info': {'type': 'KeyValuesPair', 'info': {}, 'order': 8}}
    def set_up():
        p = s.process.parent
        p.process.tools.views.btns.append(s.views.strucBtn)
        s.views.strucBtn.handlers.handle = s.handlers.onCrudStrucClicked
    def onCrudStrucClicked(w):
        p = s.process.parent
        s.process.filtersCrud.process.model.handlers.set_data({})
        s.process.filtersCrud.process.model.process.dicModel.add(["meta", "structure"], s.process.struc)
        s.views.saveAndApply.handlers.handle = s.handlers.onSaveAndApply
        if p.process.model.process.dicModel.exists(s.process.locInMeta.copy()):
            fil = p.process.model.process.dicModel.read(s.process.locInMeta.copy())
            fil = s.handlers.translateBackToData(fil)
            for k in fil:
                vv = fil[k]
                s.process.filtersCrud.process.model.handlers.add_data(vv)
        p.process.scv.views.keysOut.state.controller.display(s.views.container.outputs.layout, True, True)
    def onSaveAndApply(w):
        p = s.process.parent
        dat = s.process.filtersCrud.process.model.handlers.readAll()
        stsr = s.handlers.translateToDicForm(dat)
        p.process.model.process.dicModel.update(s.process.locInMeta.copy(), stsr)
        p.process.scv.process.crudView.views.crudView.handlers.handle(1)
        p.process.form.process.viewGenerator._rendered = None
    def translateToDicForm(data):
        ldata = { k:data[k] for k in sorted(data, key= lambda x: eval(data[x]["order"]) if data[x]["order"] != "" else 0)}
        fo ={}
        for i, k in enumerate(ldata):
            val = ldata[k]
            info = val["info"]
            for v in ["auto", "auto-edit", "disabled" ]:
                if val[v]:
                    info[v]= True
            fo[val["name"]] = {"type": val["type"],"info": info, "order": i }
        return fo
    def translateBackToData(strc):
        res = {}
        for i, k in enumerate(strc):
            allinfos = strc[k]["info"]
            isAuto = "auto" in allinfos
            isAEdit = "auto-edit" in allinfos
            isDisabled = "disabled" in allinfos
            info = {l: allinfos[l] for l in allinfos if l not in ["auto", "auto-edit", "disabled"]}
            res[i] = {"name": k, "type": strc[k]["type"], "order": str(strc[k]["order"]),
                       "auto-edit": isAEdit, "auto": isAuto, "disabled": isDisabled, "info": info}
        return res
    s = ObjMaker.uisOrganize(locals())
    return s
def AdvanceCRUDFilterer():
    cf = CRUDFilter()
    tf = ToolFeatures()
    tf.process.parent = cf
    
    tf.handlers.set_up()
    cf.process.tools = tf
    cr = CustomRenderer()
    cr.process.parent = cf
    cr.handlers.set_up()
    vr = ViewRenderer()
    vr.process.parent = cf
    vr.handlers.set_up()
    stc = StructureCrud()
    stc.process.parent = cf
    stc.handlers.set_up()
    cf.views.container.outputs.layout
    container = cf.views.container
    def set_file(file):
        s.process.cf.process.model.process.dicModel.set_file(file)
    s = ObjMaker.uisOrganize(locals())
    # set_file("test.pkl")
    return s
def formMaker():
    from timeline.t2024.generic_logger.generic_loggerV4 import FormGeneratorV2, SupportedTypes
    fg2 = FormGeneratorV2()
    fg2.process.viewGenerator._creator_map[SupportedTypes.Crud.name] = lambda **x: CRUDAdvance(**x)
    return fg2
class CRUDSimple(GComponent):
    def __init__(self, **kwargs):
        lcrud = Main.crud_filter()
        model = lcrud.process.model
        lcrud.views.container.outputs.layout.add_class("w-fit")
        descriptionLabel = Utils.get_comp(dict(value = kwargs["description"], 
                                               layout= dict(width="80px", justify_content= "flex-end", margin="0px 8px 0px 0px")), 
                                         IpywidgetsComponentsEnum.Label, bind=False)
        container = Utils.container([descriptionLabel,lcrud.views.container])
        self.set_widget(container.outputs.layout)
        self.state = ObjMaker.uisOrganize(locals())
    def clear(self):
        self.set_value({})
    def value(self):
        return self.state.process.model.process.dicModel.s.process.model
    def process_info(self):
        pass
    def set_value(self, val):
        self.state.process.model.handlers.set_data(val)
    def is_empty(self):
        return len(self.state.process.model.handlers.readAll()) == 0
    def set_structure(self, struc):
        self.state.process.model.process.dicModel.add(["meta", "structure"], struc)
class CRUDAdvance(GComponent):
    def __init__(self, **kwargs):
        lcrud = Main.crud_with_renderer()
        lcrud.views.container.outputs.layout.add_class("w-fit")
        model = lcrud.process.cf.process.model
        descriptionLabel = Utils.get_comp(dict(value = kwargs["description"], 
                                               layout= dict(width="80px", justify_content= "flex-end", margin="0px 8px 0px 0px")), 
                                         IpywidgetsComponentsEnum.Label, bind=False)
        container = Utils.container([descriptionLabel,lcrud.views.container])
        self.set_widget(container.outputs.layout)
        self.state = ObjMaker.uisOrganize(locals())
    def clear(self):
        self.set_value({})
    def value(self):
        return self.state.process.model.process.dicModel.s.process.model
    def process_info(self):
        pass
    def set_value(self, val):
        self.state.process.model.handlers.set_data(val)
    def is_empty(self):
        return len(self.state.process.model.handlers.readAll()) == 0
class Main:
    def crud_filter():
        cf = CRUDFilter()
        return cf
    def with_tools():
        cf = Main.crud_filter()
        tf = ToolFeatures()
        tf.process.parent = cf
        tf.handlers.set_up()
        cf.process.tools = tf
        return cf
    def crud_with_renderer():
        return AdvanceCRUDFilterer()