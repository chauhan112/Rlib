from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from useful.basic import Main as ObjMaker
from timeline.t2024.listCrudWithFilter import SearchComplex
import numpy as np
from LibPath import runBasic, getPath
from timeline.t2024.code_highlight import CodeHighlighter
from jupyterDB import jupyterDB

def CopyImportsFromRunBasic():
    textWid = Utils.get_comp({"placeholder":"search"}, IpywidgetsComponentsEnum.Text, className="w-auto", bind = False)
    searchBtn = Utils.get_comp({"description":"search"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    out = Utils.get_comp({},IpywidgetsComponentsEnum.Output)
    container = Utils.container([Utils.container([textWid, searchBtn]), out], className= "flex flex-column")
    sc = SearchComplex()
    sc.process.values = runBasic().splitlines()
    valuesAsNp =np.array(sc.process.values)
    parent = None
    chl = CodeHighlighter()
    def onSearch(w):
        val = textWid.outputs.layout.value.strip()
        res = sc.handlers.search("caseless",val)
        s.views.out.outputs.layout.clear_output()
        content = "\n".join(valuesAsNp[res].tolist())
        chl.handlers.set_content(content)
        jupyterDB.clip().copy(content)
        with s.views.out.outputs.layout:
            display(chl.views.container.outputs.layout)
    
    s = ObjMaker.uisOrganize(locals())
    searchBtn.handlers.handle = onSearch
    return s