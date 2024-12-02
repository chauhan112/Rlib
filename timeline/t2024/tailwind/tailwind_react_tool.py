import os
from basic import Main as ObjMaker
from FileDatabase import File
from timeline.t2024.osExplorer import Main as OSExpMain
from timeline.t2024.ui_lib.IpyComponents import IpywidgetsComponentsEnum, Utils,ComponentsLib
from SerializationDB import SerializationDB
from timeline.t2024.tailwind.tailwind_config_modify import LanguageParser
from timeline.t2024.Array import Array

def twFileCreator():
    fileAddInput = Utils.get_comp({"placeholder": "add a file to look for className"}, IpywidgetsComponentsEnum.Text, 
                                  className= "flex-1", bind =True)
    filesAddedList = Utils.get_comp({}, IpywidgetsComponentsEnum.HTML, bind =False)
    popup = Utils.get_comp({}, IpywidgetsComponentsEnum.Output, bind =False)
    outputFileLocationAndName = Utils.get_comp({"placeholder": "output file path"}, IpywidgetsComponentsEnum.Text, bind =False, className= "flex-1")
    generateBtn = Utils.get_comp({"description": "generate"}, IpywidgetsComponentsEnum.Button)
    undoBtn = Utils.get_comp({"icon": "undo"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
    openExplorer = Utils.get_comp({"description": "explore"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
    openExplorerForOutput = Utils.get_comp({"description": "explore"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
    addButton = Utils.get_comp({"icon": "plus"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
    
    selectBtnForExp = Utils.get_comp({"description": "select"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
    cancelBtnForExp = Utils.get_comp({"description": "cancel"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
    explorer = OSExpMain.osExplorer()
    explorer.views.buttons.pop()
    explorer.views.buttons.append(selectBtnForExp)
    explorer.views.buttons.append(cancelBtnForExp)
    container = Utils.container([Utils.container([fileAddInput, undoBtn, addButton,openExplorer], className="w-100"),
            explorer.views.container, filesAddedList, Utils.container([outputFileLocationAndName, openExplorerForOutput], className="w-100"), 
            generateBtn], className= "flex flex-column w-100")
    fileAddInput.outputs.layout.continuous_update = False
    explorer.views.container.hide()
    explorer.views.lister.outputs.layout.rows = 10
    filesToExtractFrom = []
    expOpened = False
    uiToPutValue = None
    langParser = LanguageParser()
    langParser.handlers.set_lang_components({'"':'"'})
    def renderLists(): 
        res = ""
        for ele in s.process.filesToExtractFrom:
            res += f"<li>{ele}</li>"
        s.views.filesAddedList.outputs.layout.value = f"<ol>{res}</ol>"
    def add_to_the_files_list(x=None):
        val = s.views.fileAddInput.outputs.layout.value.strip()
        if val and val not in s.process.filesToExtractFrom:
            s.process.filesToExtractFrom.append(val)
            s.views.fileAddInput.outputs.layout.value = ""
            s.handlers.renderLists()
    def displayExplorer(x=None):
        if not s.process.expOpened:
            s.process.expOpened = True
            s.process.explorer.views.container.show()
        else:
            s.process.expOpened = False
            s.process.explorer.views.container.hide()
    def browseFileForList(x):
        s.handlers.displayExplorer()
        s.views.selectBtnForExp.handlers.handle = s.handlers.selectFile
    def selectFile(x=None):
        s.views.fileAddInput.outputs.layout.value = s.process.explorer.views.location.outputs.layout.value + os.sep +  \
            s.process.explorer.views.lister.outputs.layout.value
        s.process.explorer.views.container.hide()
        s.process.expOpened = False
    def selectFolder(x):
        foldLoc = s.process.explorer.views.location.outputs.layout.value.strip()
        if os.path.isdir(foldLoc):
            s.views.outputFileLocationAndName.outputs.layout.value = os.path.dirname(foldLoc)
        else:
            s.views.outputFileLocationAndName.outputs.layout.value = foldLoc
        s.process.explorer.views.container.hide()
        s.process.expOpened = False
    def explorerOpenerForOutput(x=None):
        s.handlers.displayExplorer()
        s.views.selectBtnForExp.handlers.handle = s.handlers.selectFolder
    def undo_func(x=None):
        if len(s.process.filesToExtractFrom) > 0:
            s.process.filesToExtractFrom.pop()
            s.handlers.renderLists()
    def inputAdded(x=None):
        val = s.views.fileAddInput.outputs.layout.value
        abc = "src" + os.sep
        if abc in val:
            l = "".join(val.split(abc)[:-1])
            s.views.outputFileLocationAndName.outputs.layout.value = l + os.sep + abc + "abc213.tsx"
    def createTsxFile(inpFiles, creatablePath = None):
        if len(inpFiles) == 0:
            return 
        
        res = []
        for file in inpFiles:
            content = File.getFileContent(file)
            s.process.langParser.process.content = content
            root = s.process.langParser.handlers.parse_with_parent_child()
            arr = s.process.langParser.handlers.bfs(root, s.handlers.classNameChecker, True)
            res += Array(arr).map(lambda x: s.process.langParser.process.content[x.start + 1: x.end]).array
        classNames = " ".join(set(res))
        fileToCreatePath = "abc.tsx"
        content = "\n".join(['type Props = {};', 'const Component = (props: Props) => {', 
            f'  return <div className = "{classNames}">Component</div>;', '};'])
        if creatablePath is None:
            creatablePath = os.path.dirname(file) + os.sep +fileToCreatePath 

        File.overWrite(creatablePath, content)
    def classNameChecker(node):
        val = s.process.langParser.process.content[node.start-14: node.start]
        if len(val) == 14:
            return "className" in val
        return False
    def generate_file_handler (x=0):
        s.handlers.createTsxFile(s.process.filesToExtractFrom, s.views.outputFileLocationAndName.outputs.layout.value.strip())
    generateBtn.handlers.handle = generate_file_handler
    selectBtnForExp.handlers.handle = selectFile
    cancelBtnForExp.handlers.handle = lambda x: s.process.explorer.views.container.hide()
    addButton.handlers.handle = add_to_the_files_list
    openExplorer.handlers.handle = browseFileForList
    openExplorerForOutput.handlers.handle = explorerOpenerForOutput
    undoBtn.handlers.handle = undo_func
    fileAddInput.handlers.handle = inputAdded
    s = ObjMaker.uisOrganize(locals())
    return s
def FilePathGetter():
    filePathInp = Utils.get_comp({"placeholder": "file path"}, IpywidgetsComponentsEnum.Text, className= "w-auto", bind =False)
    container = filePathInp
    def get_value():
        val = s.views.filePathInp.outputs.layout.value.strip()
        return val
    def isFile():
        val = s.handlers.get_value()
        return os.path.isfile(val)
    def exists():
        val = s.handlers.get_value()
        return os.path.exists(val)
    def isFolder():
        val = s.handlers.get_value()
        return os.path.isdir(val)
    s = ObjMaker.uisOrganize(locals())
    return s
def ExportAndImportState():
    exportBtn = Utils.get_comp({"description": "export"}, IpywidgetsComponentsEnum.Button, className= "w-auto")
    importBtn = Utils.get_comp({"description": "import"}, IpywidgetsComponentsEnum.Button, className= "w-auto")
    impExpInp = FilePathGetter()
    impExpInp.views.container.outputs.layout.placeholder = "export/import file path"
    impExpInp.views.container.outputs.layout.value = "abc.pkl"
    outArea = Utils.get_comp({}, ComponentsLib.CustomOutput)
    okBtn = Utils.get_comp({"description": "ok"}, IpywidgetsComponentsEnum.Button, className= "w-auto")
    container = Utils.container([exportBtn, importBtn, impExpInp.views.container, okBtn, outArea])
    func = None
    def exporting():
        filepath = s.process.impExpInp.handlers.get_value()
        if s.process.impExpInp.handlers.isFolder():
            s.views.outArea.state.controller.display("given path is a folder", True)
            return 
        if filepath == "":
            s.views.outArea.state.controller.display("please give  a file name", True)
            return 
        obj =  {
            "output-loc": s.process.parent.views.outputFileLocationAndName.outputs.layout.value.strip(),
            "selected-files": s.process.parent.process.filesToExtractFrom
        }
        SerializationDB.pickleOut(obj, filepath)
    def importing():
        filepath = s.process.impExpInp.handlers.get_value()
        if not s.process.impExpInp.handlers.isFile():
            s.views.outArea.state.controller.display("file does not exist", True)
            return 
        obj = SerializationDB.readPickle(filepath)
        s.process.parent.views.outputFileLocationAndName.outputs.layout.value  = obj["output-loc"]
        s.process.parent.process.filesToExtractFrom  = obj["selected-files"]
        s.process.parent.handlers.renderLists()
    def exportBtnClicked(x):
        s.process.impExpInp.views.container.show()
        s.process.func = exporting
        s.views.okBtn.show()
        s.process.impExpInp.views.container.outputs.layout.value = "abc.pkl"
        s.process.impExpInp.views.container.outputs.layout.placeholder = "export file path"
    def importBtnClicked(x):
        s.process.impExpInp.views.container.show()
        s.process.func = importing
        s.views.okBtn.show()
        s.process.impExpInp.views.container.outputs.layout.value = "abc.pkl"
        s.process.impExpInp.views.container.outputs.layout.placeholder = "import file path"
    def okBtnClicked(x):
        
        s.process.func()
        s.process.impExpInp.views.container.hide()
        s.views.okBtn.hide()
        s.process.impExpInp.views.filePathInp.outputs.layout.value = ""
    s = ObjMaker.uisOrganize(locals())
    impExpInp.views.container.hide()
    okBtn.hide()
    exportBtn.handlers.handle = exportBtnClicked
    importBtn.handlers.handle = importBtnClicked
    okBtn.handlers.handle = okBtnClicked
    return s
class Main:
    def twClassGenerator():
        twf = twFileCreator()
        explortImportFunc = ExportAndImportState()
        explortImportFunc.process.parent = twf
        twf.process.explortImportFunc = explortImportFunc
        twf.views.container.append(explortImportFunc.views.container)
        return twf
    
def loader(filepath):
    obj = SerializationDB.readPickle(filepath)
    x.views.outputFileLocationAndName.outputs.layout.value  = obj["output-loc"]
    x.process.filesToExtractFrom  = obj["selected-files"]
    x.handlers.renderLists()
def export(filename):
    obj =  {
        "output-loc": x.views.outputFileLocationAndName.outputs.layout.value.strip(),
        "selected-files": x.process.filesToExtractFrom
    }
    SerializationDB.pickleOut(obj, filename)