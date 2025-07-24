from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from useful.basic import Main as ObjMaker
from timeline.t2024.listCrudWithFilter import Main as LMain
from Path import Path
from SerializationDB import SerializationDB
import copy
import os
from FileDatabase import File
def SearcherUi():
    from timeline.t2024.CustomFileSearcher import FileContentSearcher
    from timeline.t2023.copy_search_reload import FilesSearch
    fcs = FileContentSearcher()
    fcs.views.loaderUi.hide()
    fcs.views.goBackBtn.hide()
    forceLoadBtn = Utils.get_comp({"description":"force load"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    fcs.process.searchComponent.views.container.show()
    container = Utils.container([forceLoadBtn, fcs.views.container], className="flex flex-column")
    searcher = FilesSearch()
    def set_files(files):
        searcher._content = {}
        for file_path in files:
            try:
                searcher._content[os.path.normpath(file_path)] = File.getFileContent(file_path).splitlines()
            except UnicodeDecodeError:
                pass
        searcher._files = list(searcher._content.keys())
    def onForceLoad(w):
        if not hasattr(s.process.searcher, "_files"):
            print("cant force load. set files first")
            return
        s.process.searcher.set_files(s.process.searcher._files)
    def get_content():
        if not hasattr(s.process.searcher, "_content"):
            return None
        return s.process.searcher._content
    def set_content(content):
        if content is not None:
            s.process.searcher._content = content
     
    forceLoadBtn.handlers.handle = onForceLoad
    searcher.set_files = set_files
    fcs.process.searcher = searcher
    s = ObjMaker.uisOrganize(locals())
    return s
class ProjectAnalyserData:
    def __init__(self):
        self.lastN = 50
        self.path2Save = r"C:\Users\rajab\Desktop\cloud\cloud\timeline\2024\10_Oct\projectAnalyser.pkl"
        self.data = {}
    def add_path(self, path):
        history = [p for p in self.data["history"] if p != path]
        history.append(path)
        history = history[-self.lastN:]
        self.data["history"] = history
        self.data["last path"] = path
    @property
    def history(self):
        history = self.data["history"]
        hsi = history[-self.lastN:]
        return hsi[::-1]
    def read_path(self, path=None):
        self.data = SerializationDB.readPickle(self.path2Save)
        if path is None:
            path = self.data["last path"]
        if "data" in self.data and path in self.data["data"]:
            vals = self.data["data"][path]
            allFiles = vals["filteredFiles"]
            if "allFiles" in vals:
                allFiles = vals["allFiles"]
            filesContent = None
            if "filesContent" in vals:
                filesContent= vals["filesContent"]
            return [path, vals["excluded paths"], vals["extensions"], vals["filteredFiles"] , allFiles, filesContent]
        return path, {"values": [],"meta": {}}, {"values": [],"meta": {}}, [], [], None
    def save(self, rootPath, excludedPaths, extensions, filteredFiles, allFiles, filesContent):
        self.add_path(rootPath)
        self.data["history"] = self.history
        self.data["last path"] = rootPath
        if "data" not in self.data:
            self.data["data"] = {}

        self.data["data"][rootPath] = {
            "excluded paths": copy.deepcopy(excludedPaths),
            "extensions": copy.deepcopy(extensions),
            "filteredFiles": filteredFiles.copy(),
            "allFiles": allFiles.copy(),
            "filesContent": copy.deepcopy(filesContent)
        }
        self.sync()
    def sync(self):
        SerializationDB.pickleOut(self.data, self.path2Save)
def OSExplorerCustomized():
    from timeline.t2024.osExplorer import Main as OSMain
    from WordDB import WordDB
    oe = OSMain.osExplorer()
    oe.views.mainSection.outputs.layout.remove_class("w-50")
    oe.views.mainSection.outputs.layout.add_class("w-100")
    oe.views.outputDisplayer.hide()
    oe.views.buttons.outputs.renderedStates[0].outputs.layout.description = "open folder"
    oe.views.buttons.outputs.layout.add_class("flex-wrap")
    oe.views.filterSearch.handlers.handle = lambda x: x
    parent = None
    def render():
        oe.views.lister.outputs.layout.options = oe.process.data
    def hideNotNeededBtns():
        for btn in oe.views.buttons.outputs.renderedStates:
            for btnDes in ["create", "rename", "delete", "open cmd", "display"]:
                if btnDes in btn.outputs.layout.description:
                    btn.hide()
                    break
    def onFolderOpen(w):
        selected = oe.views.lister.outputs.layout.value
        folderName = os.path.dirname(selected)
        oe.process.pathManager.handlers.general_folder_open(s.process.root_path +os.sep+ folderName.strip(os.sep))
    def onFileOpen(w):
        selected = oe.views.lister.outputs.layout.value
        oe.process.osExpOps.process.notepadOpener.openIt(s.process.root_path +os.sep + selected, 0)
    def onCopyPath(w):
        from ancient.ClipboardDB import ClipboardDB
        selected = oe.views.lister.outputs.layout.value
        ClipboardDB.copy2clipboard(s.process.root_path +os.sep+ selected)    
    def set_files(files):
        root_path = s.process.parent.views.rootPath.outputs.layout.value
        s.process.oe.process.data = list(map(lambda x: x[len(root_path):], files))
        s.process.oe.views.location.outputs.layout.value = root_path
        s.process.root_path = root_path
        s.handlers.render()
    hideNotNeededBtns()
    oe.views.buttons.outputs.renderedStates[0].handlers.handle = onFolderOpen
    oe.process.osExpOps.views.openFileBtn.handlers.handle = onFileOpen
    oe.process.moreFunctions.views.copyPathBtn.handlers.handle = onCopyPath
    oe.process.osExpOps.views.openFileBtn.outputs.layout.description = "open file"
    container = oe.views.container
    s = ObjMaker.uisOrganize(locals())
    return s
def OpenSubFunc():
    extension = Utils.get_comp({"placeholder":"extension"}, IpywidgetsComponentsEnum.Text, className="w-auto", bind = False)
    loadBtn = Utils.get_comp({"description":"show"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    searchBtn = Utils.get_comp({"description":"search"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    parent = None
    container = Utils.container([extension, loadBtn, searchBtn])
    def onLoad(w):
        ext = s.views.extension.outputs.layout.value.strip()
        if ext not in s.process.parent.process.separateFiles:
            return
        s.process.parent.process.oec.handlers.set_files(s.process.parent.process.separateFiles[ext])
        s.process.parent.views.outArea.outputs.layout.clear_output()
        with s.process.parent.views.outArea.outputs.layout:
            display(s.process.parent.process.oec.views.container.outputs.layout)
    def onSearch(w):
        p = s.process.parent
        ext = s.views.extension.outputs.layout.value.strip()
        if ext not in p.process.separateFiles:
            return
        p.handlers.searchFileDomains(p.process.separateFiles[ext])

    searchBtn.handlers.handle = onSearch
    loadBtn.handlers.handle = onLoad
    s = ObjMaker.uisOrganize(locals())
    return s
def ProjectFilesAnalyser():
    cssDefined = """
        .container {
            display: grid;
            grid-template-columns: 2fr 4fr;
            min-height: 50vh;
        }
        .left {
            padding: 20px;
        }
        .right {
            padding: 20px;
            width: 100%;
        }
        """
    rootPath = Utils.get_comp({"placeholder":"project path"}, IpywidgetsComponentsEnum.Text, className="w-auto", bind = False)
    extensionBtn = Utils.get_comp({"description":"show extensions"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    plotBtn = Utils.get_comp({"description":"plot freq"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    filterBtn = Utils.get_comp({"description":"filter out excluded folders"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    loadFilesBtn = Utils.get_comp({"description":"load files"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    saveBtn = Utils.get_comp({"description":"saveState"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    searchInAllBtn = Utils.get_comp({"description":"searchAllTextFiles"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    showHistory = Utils.get_comp({"description":"history"},IpywidgetsComponentsEnum.Button, className = "w-auto", bind = False)
    excludedLocations = LMain.listCrud()
    extensions = LMain.listCrud()
    outArea = Utils.get_comp({}, IpywidgetsComponentsEnum.Output, className="w-auto", bind = False)
    css = Utils.get_comp({}, ComponentsLib.CSSAdder, customCss = cssDefined)
    container = Utils.container([css, Utils.container([Utils.container([
            Utils.container([rootPath,loadFilesBtn]), excludedLocations.views.container, 
        Utils.container([filterBtn, plotBtn, extensionBtn, saveBtn, showHistory, searchInAllBtn], className = "flex flex-wrap"),
                            ], className="left flex flex-column"), 
                                 Utils.container([outArea], className="right")], className="container w-100")])
    loadHistoryBtn = Utils.get_comp({"description":"load"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    historyList = Utils.get_comp({"options":[]},IpywidgetsComponentsEnum.Dropdown, className = "w-auto", bind=False)
    historyContent = Utils.container([historyList, loadHistoryBtn], className ="flex flex-column")
    allFiles = []
    excludedLocations.views.textWid.outputs.layout.placeholder = "exclude path"
    pad = ProjectAnalyserData()
    oec = OSExplorerCustomized()
    osf = OpenSubFunc()
    searcherUi = SearcherUi()
    
    def onFilesLoad(w):
        path = s.views.rootPath.outputs.layout.value.strip()
        if path != "" and os.path.exists(path):
            s.process.allFiles = Path.getFiles(path, True)
        # s.handlers.load_path(path)
        s.process.pad.add_path(path)
        s.process.pad.sync()
    def onFilter(w):
        filteredFiles = []
        excludedPaths = list(map(lambda x: x["name"], s.process.excludedLocations.handlers.values()["values"]))
        for f in s.process.allFiles:
            found = False
            for p in excludedPaths:
                if f.startswith(p):
                    found = True
                    break
            if not found:
                filteredFiles.append(f)
        s.process.filteredFiles = filteredFiles
    def onExtension(w):
        s.process.separateFiles = s.handlers.separateFilesIntoExt(s.process.filteredFiles)
        values = {"values": [{"name": k} for k in s.process.separateFiles.keys()], 
            "meta": s.process.extensions.process.metaInfo}
        s.process.extensions.handlers.set_values(values)
        s.views.outArea.outputs.layout.clear_output()
        tempContainer = Utils.container([s.process.extensions.views.container, 
            s.process.osf.views.container], className = "flex flex-column")
        with s.views.outArea.outputs.layout:
            display(tempContainer.outputs.layout)
    def add_values(key, value, bag):
        if key not in bag:
            bag[key] = []
        bag[key].append(value)
    
    def separateFilesIntoExt(files):
        separateFiles = {}
        for file in files:
            baseName = os.path.basename(file)
            ext = baseName.split(".")[-1]
            if len(ext) > 10:
                add_values("others", file, separateFiles)
            else:
                add_values(ext, file, separateFiles)
        return separateFiles
    
    def onPlotFreq(w):
        import matplotlib.pyplot as plt
        if not hasattr(s.process, "separateFiles"):
            s.process.separateFiles = s.handlers.separateFilesIntoExt(s.process.filteredFiles)
        
        data = {k: len(s.process.separateFiles[k]) for k in s.process.separateFiles}
        sorted_data = {k["name"]: data[k["name"]] for k in s.process.extensions.process.model}
        keys = list(sorted_data.keys())
        values = list(sorted_data.values())
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(keys, values)
        
        ax.set_title('Frequency of Items')
        ax.set_xlabel('Frequency')
        ax.set_ylabel('Items')
        
        for i, v in enumerate(values):
            ax.text(v, i, str(v), va='center')
        
        plt.tight_layout()
        s.views.outArea.outputs.layout.clear_output()
        with s.views.outArea.outputs.layout:
            display(plt.show())
            print("extensions are filtered from the extensions section")
    def onSave(w):
        rootPath = os.path.abspath(s.views.rootPath.outputs.layout.value.strip())
        s.process.pad.save(
            rootPath, 
            s.process.excludedLocations.handlers.values(), 
            s.process.extensions.handlers.values(), 
            s.process.filteredFiles,
            s.process.allFiles,
            s.process.searcherUi.handlers.get_content()
        )
    def onLoad(w):
        s.handlers.load_path(None)
    def load_path(path):
        root, exc, ext, fi, allfiles, filesContent = s.process.pad.read_path(path)
        s.process.excludedLocations.handlers.set_values(exc)
        s.process.extensions.handlers.set_values(ext)
        s.views.rootPath.outputs.layout.value = root
        s.process.filteredFiles = fi
        s.process.allFiles = allfiles
        s.process.searcherUi.handlers.set_content(filesContent)
    def onHistoryLoad(w):
        path = s.views.historyList.outputs.layout.value 
        s.handlers.load_path(path)
        s.process.pad.add_path(path)
        s.process.pad.sync()
        s.views.extensionBtn.outputs.layout.click()
    def onHistory(w):
        s.views.historyList.outputs.layout.options = s.process.pad.data["history"]
        s.views.outArea.outputs.layout.clear_output()
        with s.views.outArea.outputs.layout:
            display(s.views.historyContent.outputs.layout)
    def onSearch(w):
        s.handlers.searchFileDomains(list(filter(lambda x: x in s.process.allFiles, s.process.filteredFiles)))
    def searchFileDomains(files):
        s.process.searcherUi.process.searcher._files = files
        s.views.outArea.outputs.layout.clear_output()
        with s.views.outArea.outputs.layout:
            display(s.process.searcherUi.views.container.outputs.layout)
     
    searchInAllBtn.handlers.handle = onSearch
    saveBtn.handlers.handle = onSave
    loadFilesBtn.handlers.handle = onFilesLoad
    filterBtn.handlers.handle = onFilter
    extensionBtn.handlers.handle = onExtension
    plotBtn.handlers.handle = onPlotFreq
    showHistory.handlers.handle = onHistory
    loadHistoryBtn.handlers.handle = onHistoryLoad
    s = ObjMaker.uisOrganize(locals())
    oec.process.parent = s
    osf.process.parent = s
    extensions.process.parent = s
    excludedLocations.process.parent = s
    onLoad(1)
    return s