from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from basic import Main as ObjMaker
from timeline.t2024.generic_logger.generic_loggerV3 import ResultDisplayers, SearchComponent
from timeline.t2024.listCrudWithFilter import SearchComplex
def SearchWithResultKeys():
    scv = SearchComponent()
    outArea = Utils.get_comp({}, IpywidgetsComponentsEnum.Output, bind=False)
    container = Utils.container([scv.views.container, outArea], className="flex flex-column")
    resultDisp = ResultDisplayers()
    def _on_res_click(w):
        data = s.process.resultDisp.process.data[w._parent.state.index]
        s.handlers.btnClicked(data)
    def btnClicked(data):
        print(data)
    def search(word, typ, ctx = None):
        return ["a", "c"]
    def btnNameMaker(key):
        return key
    def onSearch(w):
        word = s.process.scv.views.inputText.outputs.layout.value
        typ = s.process.scv.views.searchType.outputs.layout.value
        res = s.handlers.search(word, typ, s)
        s.process.resultDisp.handlers.set_results(res, reverseIt = False)
        s.process.resultDisp.views.container.show()
        s.views.outArea.outputs.layout.clear_output()
        with s.views.outArea.outputs.layout:
            display(s.process.resultDisp.views.container.outputs.layout)
    resultDisp.views.container.hide()
    resultDisp.views.btns.handlers.handle = _on_res_click 
    resultDisp.handlers.name_getter = btnNameMaker
    scv.views.searchBtn.handlers.handle = onSearch
    s = ObjMaker.uisOrganize(locals())
    return s
def InstanceGetter():
    from timeline.t2024.ui_lib.refactored_key_value_adder import EventBasic
    from useful.jupyterDB import jupyterDB
    
    srk = SearchWithResultKeys()
    container = srk.views.container
    nri = jupyterDB._params["rlib"].kvs
    sc = SearchComplex()
    sc.handlers.valFunc = lambda x,y: y[0]
    def search(word, typ, ctx=None):
        s.process.data = nri.process.realtime.process.callers
        s.process.sc.process.values = list(s.process.data.keys())
        newTyp = "caseless"
        if typ in ["case", "word", "reg"]:
            newTyp = typ
        res = s.process.sc.handlers.search(newTyp, word)
        res = list(map(lambda x: s.process.sc.process.values[x], res))
        return res
    def btnClicked(key):
        
        jupyterDB._params["cnt"] = s.process.data[key]
        with s.process.srk.views.outArea.outputs.layout:
            display("assigned to variable cnt")
    def nameGetter(info):
        if type(info) == str:
            return info
        return info[0]
    srk.process.scv.views.searchType.outputs.layout.options = ['any', 'reg', 'case', 'word']
    srk.handlers.search = search
    srk.process.resultDisp.handlers.name_getter = nameGetter
    srk.handlers.btnClicked = btnClicked
    s = ObjMaker.uisOrganize(locals())
    return s