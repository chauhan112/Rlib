from basic import Main as ObjMaker
import subprocess
from SystemInfo import SystemInfo
import platform
from enum import Enum
import threading
from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from modules.Explorer.model import OSFileExplorer, ExplorerUtils
from ComparerDB import ComparerDB
import os
from timeline.t2023.searchSystem import NotepadOpener
from FileDatabase import File
from Path import Path
def OSExpOps():
    createFileBtn = Utils.get_comp({"description": "create file"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    createFolderBtn = Utils.get_comp({"description": "create folder"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    renameBtn = Utils.get_comp({"description": "rename"}, IpywidgetsComponentsEnum.Button, className = "w-auto")
    deleteBtn = Utils.get_comp({"description": "delete"}, IpywidgetsComponentsEnum.Button, className = "w-auto")
    openFileBtn = Utils.get_comp({"description": "open"}, IpywidgetsComponentsEnum.Button, className = "w-auto")
    textWid = Utils.get_comp({"placeholder":"add word"}, IpywidgetsComponentsEnum.Text, className="w-auto", bind = False)
    displayContent = Utils.get_comp({"description": "display"}, IpywidgetsComponentsEnum.Button, className = "w-auto")
    cmdOpen = Utils.get_comp({"description": "open cmd"}, IpywidgetsComponentsEnum.Button, className = "w-auto")
    okBtn = Utils.get_comp({"description": "ok"}, IpywidgetsComponentsEnum.Button)
    outArea = Utils.get_comp({}, ComponentsLib.CustomOutput)
    
    from modules.Explorer.displayer import ExplorerFileDisplayer
    efd = ExplorerFileDisplayer()
    parent = None
    notepadOpener = NotepadOpener()
    def setUp():
        s.process.parent.views.buttons.append(s.views.createFileBtn)
        s.process.parent.views.buttons.append(s.views.createFolderBtn)
        s.process.parent.views.buttons.append(s.views.renameBtn)
        s.process.parent.views.buttons.append(s.views.openFileBtn)
        s.process.parent.views.buttons.append(s.views.deleteBtn)
        s.process.parent.views.buttons.append(s.views.displayContent)
        s.process.parent.views.buttons.append(s.views.cmdOpen)
        s.process.parent.views.mainSection.append(s.views.outArea)
        s.process.prev_func = s.process.parent.views.lister.handlers.handle
        s.process.parent.views.lister.handlers.handle = s.handlers.newOptionSelected
        s.views.deleteBtn.handlers.handle = s.handlers.onDelete
        s.views.createFileBtn.handlers.handle = s.handlers.onCreateFile
        s.views.createFolderBtn.handlers.handle = s.handlers.onCreateFolder
        s.views.openFileBtn.handlers.handle = s.handlers.onOpen
        s.views.displayContent.handlers.handle = s.handlers.onDisplay
        s.views.cmdOpen.handlers.handle = s.handlers.onCmdOpen
    def onCmdOpen(w):
        import platform
        import threading
        import subprocess
        uname = platform.uname()
        def console_opener_laptop2022(path):
            subprocess.run(['start', 'cmd', '/K', 'cd', path, '&&', "call", r"C:\Users\rajab\miniconda3\Scripts\activate.bat" , 
                            r"C:\Users\rajab\miniconda3"], shell=True)
        def open_in_thread(func, folder_path):
            folder_thread = threading.Thread(target=func, args=(folder_path,))
            folder_thread.start()
        if uname.system == "Windows" and uname.machine == "AMD64":
            open_in_thread(console_opener_laptop2022, s.process.parent.process.model.path)
        
    def onCreateFile(w):
        s.views.outArea.state.controller.clear()
        s.views.outArea.state.controller.display(s.views.textWid.outputs.layout, ipy=True)
        s.views.outArea.state.controller.display(s.views.okBtn.outputs.layout, ipy=True)
        s.views.okBtn.handlers.handle = createTheGivenFile
    def createTheGivenFile(w):
        filePath = s.views.textWid.outputs.layout.value.strip()
        if filePath:
            path = os.sep.join([s.process.parent.process.model.path, filePath])
            File.createFile(path)
            s.process.parent.handlers.render()
            s.views.outArea.state.controller.clear()
            s.views.textWid.outputs.layout.value = ""
        else:
            raise IOError("file name empty")
    def onCreateFolder(w):
        s.views.outArea.state.controller.clear()
        s.views.outArea.state.controller.display(s.views.textWid.outputs.layout, ipy=True)
        s.views.outArea.state.controller.display(s.views.okBtn.outputs.layout, ipy=True)
        s.views.okBtn.handlers.handle = createTheGivenFolder
    def createTheGivenFolder(w):
        filePath = s.views.textWid.outputs.layout.value.strip()
        if filePath:
            path = os.sep.join([s.process.parent.process.model.path, filePath])
            os.makedirs(path)
            s.process.parent.handlers.render()
            s.views.outArea.state.controller.clear()
            s.views.textWid.outputs.layout.value = ""
        else:
            raise IOError("folder name empty")
    def onDelete(w):
        s.views.outArea.state.controller.clear()
        s.views.textWid.outputs.layout.placeholder = "give folder name to delete folder else ignore"
        s.views.outArea.state.controller.display(s.views.textWid.outputs.layout, ipy=True)
        s.views.outArea.state.controller.display(s.views.okBtn.outputs.layout, ipy=True)
        s.views.okBtn.handlers.handle = deleteIt
    def deleteIt(w):
        filePath = s.views.textWid.outputs.layout.value.strip()
        if filePath:
            path = os.sep.join([s.process.parent.process.model.path, filePath])
            Path.deleteFolder(path)
        else:
            selected = s.process.parent.views.lister.outputs.layout.value
            if selected not in [".", ".."]:
                path = os.sep.join([s.process.parent.process.model.path, selected])
                File.deleteFiles([path])
        s.process.parent.handlers.render()
        s.views.outArea.state.controller.clear()
        s.views.textWid.outputs.layout.value = ""
    def onOpen(w):
        selected = s.process.parent.views.lister.outputs.layout.value
        if selected not in [".", ".."]:
            path = os.sep.join([s.process.parent.process.model.path, selected])
            opened = False
            for x in ["txt", "py", "js", "ts", "jsx", "tsx"]:
                if path.endswith("." + x ):
                    opened = True
                    s.process.notepadOpener.openIt(path, 0)
                    break
            if not opened:
                File.openFile(path)
            
    def onDisplay(w):
        s.process.parent.views.outputDisplayer.outputs.layout.clear_output()
        selected = s.process.parent.views.lister.outputs.layout.value
        if selected not in [".", ".."]:
            path = os.sep.join([s.process.parent.process.model.path, selected])
            with s.process.parent.views.outputDisplayer.outputs.layout:
                s.process.efd.displayPath(path)
    def newOptionSelected(w):
        s.process.parent.views.outputDisplayer.outputs.layout.clear_output()
        s.process.prev_func(w)
    def onRename(w):
        pass
    
    s = ObjMaker.uisOrganize(locals())
    return s
class Devices(Enum):
    GamingLaptop = 1
    OpenSuseOffice= 2
    Laptop2019 = 3
    Unknown = 4
def ConsoleAndFolderOpenerModel():
    selected_function = None
    def general_console_open(path):
        device = s.handlers.device_unique_identifier()
        if device == Devices.GamingLaptop:
            selected_function = s.process.console_funcs.handlers.gamingLaptop
        elif device == Devices.OpenSuseOffice:
            selected_function = s.process.console_funcs.handlers.opensuse
        elif device == Devices.Laptop2019:
            selected_function = s.process.console_funcs.handlers.window2019
        else:
            print("unknown device detected")
            return
        s.handlers.run_on_thread(selected_function, path)
    def general_folder_open(path):
        device = s.handlers.device_unique_identifier()
        if device == Devices.GamingLaptop:
            selected_function = s.process.folderOpenerFunc.handlers.gamingLaptop
        elif device == Devices.OpenSuseOffice:
            selected_function = s.process.folderOpenerFunc.handlers.opensuse
        elif device == Devices.Laptop2019:
            selected_function = s.process.folderOpenerFunc.handlers.window2019
        else:
            print("unknown device detected")
            return
        s.handlers.run_on_thread(selected_function, path)
    def run_on_thread(func, folder_path):
        folder_thread = threading.Thread(target=func, args=(folder_path,))
        folder_thread.start()
    def console_openers():
        def opensuse(path):
            subprocess.run(["konsole", "--workdir", path])
        def window(path):
            raise IOError("not defined")
        def window2019(path):
            raise IOError("not defined")
        def gamingLaptop(path):
            subprocess.run(['start', 'cmd', '/K', 'cd', path, '&&', "call", r"C:\Users\rajab\miniconda3\Scripts\activate.bat" ,
                         r"C:\Users\rajab\miniconda3"], shell=True)
        return ObjMaker.uisOrganize(locals())
    def folderOpeners():
        def opensuse(path):
            subprocess.run(["dolphin", path])
        def gamingLaptop(path):
            subprocess.run(["explorer", path.replace("/", os.sep)])
        def window2019(path):
            subprocess.run(["explorer", path.replace("/", os.sep)])
        return ObjMaker.uisOrganize(locals())
    def device_unique_identifier():
        uname = platform.uname()
        if SystemInfo.getName() == "linux-ier9":
            return Devices.OpenSuseOffice
        elif uname.system == "Windows" and uname.machine == "AMD64":
            return Devices.GamingLaptop
        return Devices.Unknown
    folderOpenerFunc = folderOpeners()
    console_funcs = console_openers()
    s = ObjMaker.uisOrganize(locals())
    return s
def OSExplorer():
    location = Utils.get_comp({"placeholder": "location", "disabled": True}, IpywidgetsComponentsEnum.Text, className= "w-90", bind=False)
    title = Utils.get_comp({"value": "OS Explorer"}, IpywidgetsComponentsEnum.HTML, bind =False)
    filterSearch = Utils.get_comp({"placeholder": "search or filter"}, IpywidgetsComponentsEnum.Text, className= "w-auto")
    lister = Utils.get_comp({"rows": 15}, IpywidgetsComponentsEnum.Select, className="w-100 p0")
    buttons = Utils.container([Utils.get_comp({"description": "open folder here"}, IpywidgetsComponentsEnum.Button, className ="w-auto")])
    outputDisplayer = Utils.get_comp({}, IpywidgetsComponentsEnum.Output, bind=False, className = "w-50 h-600px overflow-auto")
    mainSection = Utils.container([title, Utils.container([location, filterSearch], className="w-auto"), lister,buttons],
                               className= "flex flex-column w-50")
    container = Utils.container([mainSection, outputDisplayer], className="w-100")
    model = OSFileExplorer()
    pathManager = ConsoleAndFolderOpenerModel()
    def undir(dired):
        return dired[2:]
    def folderSelected(value):
        if value == "..":
            if ("\\" in s.process.model.path or "/" in s.process.model.path):
                s.process.model.goBack()
        elif value == ".":
            pass
        else:
            s.process.model.cd(value)
        s.handlers.render()
    def fileSelected(value):
        pass
    def openFolder(wid):
        path = s.process.model.path
        s.process.pathManager.handlers.general_folder_open(path)
    def optionSelected(val):
        selected = s.views.lister.outputs.layout.value
        if selected is None:
            return
        if type(selected)== str and selected.startswith(ExplorerUtils.dirIcon()):
            s.handlers.folderSelected(s.handlers.undir(selected))
        else:
            s.handlers.fileSelected(selected)
    def render():
        s.views.location.outputs.layout.value = s.process.model.path
        s.views.filterSearch.handlers.handle(1)
    def filterOut(wid):
        dirs, files = s.process.model.dirList()
        filteringValue = s.views.filterSearch.outputs.layout.value
        lister = s.views.lister
        if filteringValue != "":
            lister.outputs.layout.options = ExplorerUtils.dirsWithIcon([".", ".."]) + list(filter(lambda x: ComparerDB.inCompare(filteringValue, x), ExplorerUtils.dirsWithIcon(dirs[2:]) + files))
        else:
            lister.outputs.layout.options = ExplorerUtils.dirsWithIcon(dirs) + files
    def set_path(path):
        s.process.model.set_path(path)
        s.handlers.render()
    s = ObjMaker.uisOrganize(locals())
    filterSearch.outputs.layout.continuous_update = False
    lister.handlers.handle = optionSelected
    filterSearch.handlers.handle = filterOut
    buttons.outputs.renderedStates[0].handlers.handle = openFolder
    return s
def MoreFunctionalities():
    copyPathBtn = Utils.get_comp({"description": "copy path"}, IpywidgetsComponentsEnum.Button, className="w-auto")
    parent = None
    def copyPathCallback(w):
        from ClipboardDB import ClipboardDB
        selected = s.process.parent.views.lister.outputs.layout.value
        path2Copy = os.path.abspath(s.process.parent.process.model.path)
        if type(selected)== str:
            if not selected.startswith(ExplorerUtils.dirIcon()):
                path2Copy += os.sep + selected
        ClipboardDB.copy2clipboard(path2Copy.replace(os.sep, "/"))
    def set_up():
        s.process.parent.views.buttons.append(s.views.copyPathBtn)
        s.views.copyPathBtn.handlers.handle = copyPathCallback
    s = ObjMaker.uisOrganize(locals())
    return s
class Main:
    def osExplorer(path= None):
        exp = OSExplorer()
        if path is not None:
            exp.handlers.set_path(path)
        moreFunctions = MoreFunctionalities()
        moreFunctions.process.parent = exp
        moreFunctions.handlers.set_up()
        exp.process.moreFunctions = moreFunctions
        osExpOps = OSExpOps()
        osExpOps.process.parent = exp
        osExpOps.handlers.setUp()
        exp.process.osExpOps = osExpOps
        exp.handlers.render()
        return exp
    def osExpWithPagination(path= None):
        from timeline.t2024.ListResultDisplayer import ListResultDisplayer
        lrd = ListResultDisplayer()
        lrd.handlers.set_up()
        if path is not None:
            lrd.process.exp.handlers.set_path(path)
        return lrd
