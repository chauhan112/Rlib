from LibsDB import LibsDB
from timeline.t2024.generic_logger.generic_loggerV3 import ResultDisplayers
from SerializationDB import SerializationDB
from timeline.t2023.dep_extractor.dependency_extractor import DicOps
from timeline.t2023.copy_search_reload import FilesSearch
from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from basic import Main as ObjMaker
from timeline.t2024.generic_logger.generic_loggerV3 import SearchComponent
import os
from timeline.t2023.searchSystem import NotepadOpener

def SearchInRlibAndSync():
    sc = SearchComponent()
    sc.views.container.outputs.layout.remove_class("w-100")
    sc.views.searchType.outputs.layout.options = ('any', 'reg', 'case', 'word', 'concatenated')
    syncBtn = Utils.get_comp({"icon":"sync"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    
    filepath = os.sep.join([LibsDB.cloudPath(), "timeline", "2024", "12_Dec", "fileSearchOptimize.pkl"])
    fileContent = SerializationDB.readPickle(filepath)
    resultDisp = ResultDisplayers()
    fs = FilesSearch()
    fileOpener = NotepadOpener()
    container = Utils.container([Utils.container([syncBtn, sc.views.container]), resultDisp.views.container], className="flex flex-column")
    def onSearchResultClicked(w):
        file, nr = s.process.resultDisp.process.data[w._parent.state.index]
        s.process.fileOpener.openIt(file, nr)
        
    def nameGetter(key):
        if type(key) == str:
            return key
        file, nr = key
        return os.path.basename(file)[:-3]
    def onLoad(w):
        s.process.fileContent = SerializationDB.readPickle(s.process.filepath)
        s.process.fs._files = list(s.process.fileContent.keys())
        s.process.fs._content = s.process.fileContent
    def onSearch(w):
        val = s.process.sc.views.searchType.outputs.layout.value
        reg, case = False, False
        word = s.process.sc.views.inputText.outputs.layout.value
        if val == "case":
            case = True
        elif val == "reg":
            reg = True
        elif val == "word":
            word = r"\b" + word + r"\b"
            reg = True
        elif val == "concatenated":
            words = eval(word)
            res = s.process.fs.concated_search(words, reg, case)
            s.process.resultDisp.handlers.set_results(res, reverseIt = False)
            return
        res = s.process.fs.search(word, reg, case)
        s.process.resultDisp.handlers.set_results(res, reverseIt = False)
        s.process.resultDisp.views.container.show()
    def onSync(q):
        from LibPath import getPath
        from Path import Path
        from FileDatabase import File
        allPyFiles = Path.filesWithExtension("py", getPath(), True)
        res = {}
        for f in allPyFiles:
            res[f] = File.getFileContent(f).splitlines()
        SerializationDB.pickleOut(res, s.process.filepath)
        s.handlers.onLoad(1)
    resultDisp.views.btns.handlers.handle = onSearchResultClicked
    sc.views.searchBtn.handlers.handle = onSearch
    syncBtn.handlers.handle = onSync
    s = ObjMaker.uisOrganize(locals())
    onLoad(1)
    resultDisp.views.container.hide()
    resultDisp.handlers.name_getter = nameGetter
    return s