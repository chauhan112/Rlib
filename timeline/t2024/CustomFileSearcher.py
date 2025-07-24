from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from basic import Main as ObjMaker
from useful.SearchSystem import FilesContentSearch
from timeline.t2023.searchSystem import NotepadOpener
from timeline.t2024.generic_logger.generic_loggerV3 import ResultDisplayers
from timeline.t2024.experiments.keyValueWithSearchAndFilter import NewSearchComponent
from useful.Path import Path
import os

def FileContentSearcher():
    pathInp = Utils.get_comp({"placeholder":"give folder path val: ."}, IpywidgetsComponentsEnum.Text, className="w-auto", bind = False)
    fileType = Utils.get_comp({"placeholder":"Eg:py, txt, .. default: py"}, IpywidgetsComponentsEnum.Text, className="w-auto", bind = False)
    loadBtn = Utils.get_comp({"description":"load"}, IpywidgetsComponentsEnum.Button, className = "w-auto")
    goBackBtn = Utils.get_comp({"icon":"arrow-left"}, IpywidgetsComponentsEnum.Button, className = "w-fit")
    allFileWid = Utils.get_comp({"indent":False, "description": "walk"}, IpywidgetsComponentsEnum.Checkbox,className="w-auto", bind=False)
    searchComponent = NewSearchComponent()
    searchComponent.handlers.update_selected()
    resultDis = ResultDisplayers()
    opener = NotepadOpener()
    loaderUi = Utils.container([pathInp, fileType, allFileWid, loadBtn])
    container = Utils.container([loaderUi, goBackBtn, searchComponent.views.container, resultDis.views.container], className="flex-column")
    searcher = None
    prev_path = None
    resultDis.views.container.hide()
    searchComponent.views.container.hide()
    goBackBtn.hide()
    def onLoad(w):
        path = s.views.pathInp.outputs.layout.value.strip()
        if path == "":
            path = "."
        ext = s.views.fileType.outputs.layout.value.strip().lower()
        if ext == "":
            ext = "py"
        walk = s.views.allFileWid.outputs.layout.value
        files = Path.filesWithExtension(ext, path, walk)
        s.process.searcher = FilesContentSearch(files)
        s.views.loaderUi.hide()
        s.process.searchComponent.views.container.show()
        s.views.goBackBtn.show()
    def onGoBack(w):
        s.views.loaderUi.show()
        s.process.searchComponent.views.container.hide()
        s.views.goBackBtn.hide()
    def onSearch(w):
        txt = s.process.searchComponent.views.inputText.outputs.layout.value.strip()
        typ = s.process.searchComponent.views.searchType.outputs.layout.value
        case = False
        reg = False
        if typ == "reg":
            reg = True
        elif typ == "case":
            case = True
        elif typ == "word":
            reg = True
            txt = r"\b" + txt + r"\b"
        founds = s.process.searcher.search(txt, case, reg)
        s.process.resultDis.views.container.show()
        s.process.resultDis.handlers.set_results(founds)
    def nameGetter(x):
        if type(x) == str:
            return x
        return os.path.basename(x[0])
    def get_placeholder(x):
        if type(x) == str:
            return x
        return x[0]
    def new_button_state_update(btn, info):
        index, ele = info
        btn.outputs.layout.description = s.process.resultDis.handlers.name_getter(ele)
        btn.outputs.layout.tooltip = s.handlers.get_placeholder(ele)
        btn.state.index = index
    def onOpenFile(w):
        index = w._parent.state.index
        val = s.process.resultDis.process.data[index]
        file, nr = val
        s.process.opener.openIt(file, nr)
    loadBtn.handlers.handle = onLoad
    goBackBtn.handlers.handle = onGoBack
    searchComponent.views.searchBtn.handlers.handle = onSearch
    resultDis.handlers.name_getter = nameGetter
    resultDis.views.btns.handlers.handle = onOpenFile
    resultDis.handlers.button_state_update = new_button_state_update
    s = ObjMaker.uisOrganize(locals())
    return s
class Main:
    def customFileSearcher():
        fcs = FileContentSearcher()
        return fcs