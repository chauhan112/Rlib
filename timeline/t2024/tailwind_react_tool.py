from timeline.t2024.ui_lib.IpyComponents import BaseComponentV2
import os
from basic import ObjectOps, addToNameSpace

def twFileCreator(state):
    from timeline.t2024.osExplorer import Main as OSExpMain
    from timeline.t2024.ui_lib.IpyComponents import IpywidgetsComponentsEnum, Utils
    fileAddInput = Utils.get_comp({"placeholder": "add a file to look for className"}, IpywidgetsComponentsEnum.Text, 
                                  className= "flex-1", bind =True)
    filesAddedList = Utils.get_comp({}, IpywidgetsComponentsEnum.HTML, bind =False)
    popup = Utils.get_comp({}, IpywidgetsComponentsEnum.Output, bind =False)
    outputFileLocationAndName = Utils.get_comp({"placeholder": "outputFile location"}, IpywidgetsComponentsEnum.Text, bind =False, className= "flex-1")
    generateBtn = Utils.get_comp({"description": "generate"}, IpywidgetsComponentsEnum.Button)
    undoBtn = Utils.get_comp({"icon": "undo"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
    openExplorer = Utils.get_comp({"description": "explore"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
    openExplorerForOutput = Utils.get_comp({"description": "explore"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
    addButton = Utils.get_comp({"icon": "plus"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
    
    selectBtnForExp = Utils.get_comp({"description": "select"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
    cancelBtnForExp = Utils.get_comp({"description": "cancel"}, IpywidgetsComponentsEnum.Button, className ="w-auto")
    explorer = OSExpMain.osExplorer()
    explorer.views.components.buttons.append(selectBtnForExp)
    explorer.views.components.buttons.append(cancelBtnForExp)
    container = Utils.container([Utils.container([fileAddInput, undoBtn, addButton,openExplorer], className="w-100"),
                                 explorer,
                                 filesAddedList, 
                                 Utils.container([outputFileLocationAndName, openExplorerForOutput], className="w-100"), 
                                 generateBtn], 
                                className= "flex flex-column w-100")
    fileAddInput.outputs.layout.continuous_update = False
    app_name = "tw generate"
    explorer.hide()
    explorer.views.components.lister.outputs.layout.rows = 10
    state.model = ObjectOps.make_obj()
    state.model.filesToExtractFrom = []
    
    def renderLists(): 
        res = ""
        for ele in state.model.filesToExtractFrom:
            res += f"<li>{ele}</li>"
        filesAddedList.outputs.layout.value = f"<ol>{res}</ol>"
    def add_to_the_files_list(x=None):
        val = fileAddInput.outputs.layout.value.strip()
        if val and val not in state.model.filesToExtractFrom:
            state.model.filesToExtractFrom.append(val)
            fileAddInput.outputs.layout.placeholder = val
            fileAddInput.outputs.layout.value = ""
            state.handlers.renderLists()
    def explorerOpen(x=None):
        if not state.state.expOpened:
            state.state.expOpened = True
            explorer.show()
        else:
            state.state.expOpened = False
            explorer.hide()
    def selectFile(x=None):
        # check for folder
        fileAddInput.outputs.layout.value = explorer.views.components.titleLoc.location.outputs.layout.value + os.sep+  \
            explorer.views.components.lister.outputs.layout.value
        explorer.hide()
        state.state.expOpened = False
    def explorerOpenerForOutput(x=None):
        state.state.views.openExplorer.handlers.handle()
        def selectFile(x=None):
            # check for folder
            explorer = state.state.views.explorer
            state.state.views.outputFileLocationAndName.outputs.layout.value = explorer.views.components.titleLoc.location.outputs.layout.value + os.sep+  \
                explorer.views.components.lister.outputs.layout.value
            state.state.views.explorer.hide()
            state.state.expOpened = False
            state.state.views.selectBtnForExp.handlers.handle = state.handlers.selectFile
        state.state.views.selectBtnForExp.handlers.handle = selectFile
    def undo_func(x=None):
        if len(state.model.filesToExtractFrom) > 0:
            state.model.filesToExtractFrom.pop()
            state.handlers.renderLists()
    def inputAdded(x=None):
        val = fileAddInput.outputs.layout.value
        abc = "src" + os.sep
        if abc in val:
            l = "".join(val.split(abc)[:-1])
            outputFileLocationAndName.outputs.layout.value = l + os.sep + abc + "abc213.tsx"
    def createTsxFile(inpFiles, creatablePath = None):
        if len(inpFiles) == 0:
            return 
        from FileDatabase import File
        res = []
        for file in inpFiles:
            lines = File.getFileContent(file).splitlines()
            res += list(map(lambda x: x.strip().strip("className").strip(",").strip(":").strip().strip('"').split(","), filter(lambda x: "className" in x, lines)))
        from ListDB import ListDB
        classNames = " ".join(set(ListDB.flatten(res)))
        fileToCreatePath = "abc.tsx"
        content = """
        type Props = {{}};
        const Component = (props: Props) => {{
          return <div className = "{}">Component</div>;
        }};
        """.format(classNames)
        if creatablePath is None:
            creatablePath = os.path.dirname(filePath) + os.sep +fileToCreatePath 

        File.overWrite(creatablePath, content)
    def generate_file_handler (x=0):
        createTsxFile(state.model.filesToExtractFrom, outputFileLocationAndName.outputs.layout.value.strip())
    generateBtn.handlers.handle = generate_file_handler
    selectBtnForExp.handlers.handle = selectFile
    cancelBtnForExp.handlers.handle = lambda x: explorer.hide()
    addButton.handlers.handle = add_to_the_files_list
    openExplorer.handlers.handle = explorerOpen
    openExplorerForOutput.handlers.handle = explorerOpenerForOutput
    undoBtn.handlers.handle = undo_func
    fileAddInput.handlers.handle = inputAdded
    addToNameSpace(state, locals(), ["state"])
    state.state.expOpened = False

class Main:
    def twClassGenerator():
        state = BaseComponentV2()
        state.inputs.bind = False
        
        twFileCreator(state)
        state.outputs.layout = state.state.views.container.outputs.layout
        return state