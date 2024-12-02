from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from basic import Main as ObjMaker
from timeline.t2024.tailwind.twcrudOps import DictionaryModel
from timeline.t2024.generic_logger.generic_loggerV3 import Pagination
from modules.SearchSystem.modular import HideableWidget as WidOps
import math
import ipyreact
class IpyReactLib:
    def htmlWid(typ, children, props=None):
        if props is not None:
            return ipyreact.Widget(_type=typ, children= children, props = {})
        return ipyreact.Widget(_type=typ, children= children)
def ResultDisplayerAsTable():
    tablesInfo = ObjMaker.namespace()
    dm = DictionaryModel()
    sizeCount = 20
    pageNr = 1
    page = Pagination()
    container = Utils.container([page.views.container], className ="flex flex-column")
    render_called = False
    actions = [dict(icon="ellipsis-v")]
    def set_results(results, newPageNr = 1, reverseIt = True):
        s.process.data = results
        if reverseIt:
            s.process.data = results[::-1]
        s.process.totalPagesNr = math.ceil(len(s.process.data)/s.process.sizeCount)
        if s.process.totalPagesNr < newPageNr:
            newPageNr = 1
        s.process.pageNr = newPageNr
        s.process.page.handlers.selectWithVal(str(newPageNr))
        s.handlers.render()
    def columnsNamesWithLoc(cols_loc_tuple):
        """  [('column name', locOrFunc, isFunc),('column name2', locOrFunc, isFunc) ] """
        s.process.columns = cols_loc_tuple
    def set_cols_as_list(cols, ignoreList= []):
        # setting the structure
        s.handlers.columnsNamesWithLoc([(k, [k], False) for k in cols if k not in ignoreList])
    def set_actions_params(params):
        """[{icon="ellipses-v"}, {"icon": "trash"}]"""
        s.process.actions = params
    def valueGetter(ele, loc, key):
        if loc is None: 
            return key
        s.process.dm.s.process.model = ele
        return s.process.dm.read(loc)
    def update_data():
        data = s.handlers.data_for_currentPage()
        for i in range(s.process.sizeCount):
            for col, locOrFnc, isFunc in s.process.columns:
                tr = s.process.tablesInfo.tbody.children[i]
                WidOps.showIt(tr)
                if i < len(data):
                    index, ele = data[i]
                    val = "Nan"
                    if isFunc:
                        val = locOrFnc(ele, index)
                    else:
                        val = s.handlers.valueGetter(ele, locOrFnc, ele)
                    s.process.tablesInfo.state[(i, col)].children = [val]
                else:
                    WidOps.hideIt(tr)
    
    def _btn_action(w):
        pass
    def render():
        if not s.process.render_called:
            s.handlers.initialize()
        if s.process.totalPagesNr == 1:
            s.process.page.views.container.hide()
        else:
            s.process.page.views.container.show()
        s.handlers.update_data()
        s.process.page.handlers.update_total_pages(s.process.totalPagesNr)
        s.process.render_called = True
    def initialize():
        s.process.tablesInfo.tds = []
        s.process.tablesInfo.ths = []
        s.process.tablesInfo.trs = []
        
        s.process.tablesInfo.state = {}
        s.process.tablesInfo.state["head"] = []
        
        for col, locOrFnc, isFunc in s.process.columns:
            s.process.tablesInfo.state["head"].append(IpyReactLib.htmlWid("th", [col]))
            for i in range(s.process.sizeCount):
                comp = IpyReactLib.htmlWid("td", ["some value"])
                comp._index = i
                s.process.tablesInfo.state[(i, col)] = comp

        s.process.tablesInfo.state["head"].append(IpyReactLib.htmlWid("th", ["actions"]))
        s.process.tablesInfo.thead = IpyReactLib.htmlWid("thead", [IpyReactLib.htmlWid("tr", s.process.tablesInfo.state["head"])])
        s.handlers.addingActionAlongRow()
        s.handlers.fillRowsInfo()
        res = []
        for row in s.process.tablesInfo.rowsInfo:
            res.append(IpyReactLib.htmlWid("tr", row))
        s.process.tablesInfo.tbody = IpyReactLib.htmlWid("tbody",res)
        s.process.tablesInfo.table = IpyReactLib.htmlWid("table",  [s.process.tablesInfo.thead, s.process.tablesInfo.tbody])
        s.views.container.append(Utils.wrapper(s.process.tablesInfo.table))
    def addingActionAlongRow():
        for i in range(s.process.sizeCount):
            actions = []
            for ac in s.process.actions:
                btn = Utils.get_comp(ac, IpywidgetsComponentsEnum.Button, className="w-auto")
                btn.handlers.handle = s.handlers._btn_action
                btn.state.index = i
                actions.append(btn.outputs.layout)
            s.process.tablesInfo.state[(i, "actions")] = IpyReactLib.htmlWid("div", actions)
    def fillRowsInfo():
        s.process.tablesInfo.rowsInfo = []
        for i in range(s.process.sizeCount):
            rows = []
            for col, locOrFnc, isFunc in s.process.columns + [("actions",1,1)]:
                rows.append(s.process.tablesInfo.state[(i, col)])
            s.process.tablesInfo.rowsInfo.append(rows)
        
    def data_for_currentPage():
        res = []
        fromStart = s.process.sizeCount * (s.process.pageNr-1)
        till = s.process.sizeCount * (s.process.pageNr)
        for i in range(fromStart, till):
            if i >= len(s.process.data):
                break
            res.append((i, s.process.data[i]))
        return res
    s = ObjMaker.uisOrganize(locals())
    return s
