from timeline.t2024.ui_lib.IpyComponents import IpywidgetsComponentsEnum, Utils, BaseComponentV2
from timeline.t2023.console_opener import Main as COMain
from modules.Explorer.model import OSFileExplorer, ExplorerUtils
from ComparerDB import ComparerDB
from basic import ObjectOps

class OSFileExplorerLC(BaseComponentV2):
    def set_up(self):
        location = Utils.get_comp({"placeholder": "location", "disabled": True}, IpywidgetsComponentsEnum.Text, className= "w-90", bind=False)
        title = Utils.get_comp({"value": "OS Explorer"}, IpywidgetsComponentsEnum.HTML, bind =False)
        filterSearch = Utils.get_comp({"placeholder": "search or filter"}, IpywidgetsComponentsEnum.Text, className= "w-auto")
        lister = Utils.get_comp({"rows": 15}, IpywidgetsComponentsEnum.Select, className="w-100 p0")
        buttons = Utils.container([Utils.get_comp({"description": "open folder here"}, IpywidgetsComponentsEnum.Button, className ="w-auto")])
        outputDisplayer = Utils.get_comp({}, IpywidgetsComponentsEnum.Output, bind=False, className = "w-50")
        explorer = Utils.container([Utils.container([title, Utils.container([location, filterSearch], className="w-auto"), lister,buttons], 
                                   className= "flex flex-column w-50"), outputDisplayer], className="w-100")
        filterSearch.outputs.layout.continuous_update = False
        # ModelInitializer.initialize()
        
        cfff = COMain.console_and_folder_opener()
        folderOpener = cfff.app.controller.explorer.open
        exp = OSFileExplorer()

        ObjectOps.add_to_namespace(self, [
            [["views", "components", "titleLoc", "location"], location],
            [["views", "components", "titleLoc", "title"], title],
            [["views", "components", "filterSearch"], filterSearch],
            [["views", "components", "lister"], lister],
            [["views", "components", "buttons"], buttons],
            [["views", "components", "explorer"], explorer],
            [["views", "components", "outputDisplayer"], outputDisplayer],
            [["outputs", "layout"], explorer.outputs.layout],
            [["model", "explorer"], exp],
            [["controller", "callbacks", "folderOpener"], folderOpener],
            [["controller", "callbacks", "folderSelected"], self._folderSelected],
            [["controller", "callbacks", "render"], self.render],
            [["controller", "callbacks", "undir"], self._undir],
        ])
        
        lister.handlers.defs.filesSelected = self._optionSelected
        lister.handlers.handle = self._optionSelected
        filterSearch.handlers.defs.filterOut = self._filterOut
        filterSearch.handlers.handle = self._filterOut
        buttons.outputs.renderedStates[0].handlers.defs.openFolder = self._openFolder
        buttons.outputs.renderedStates[0].handlers.handle = self._openFolder
        
        self.controller.callbacks.render()
    def _openFolder(self, x=None):
        self.controller.callbacks.folderOpener(self.views.components.titleLoc.location.outputs.layout.value)
    def _folderSelected(self, value):
        if value == "..":
            self.model.explorer.goBack()
        elif value == ".":
            pass
        else:
            self.model.explorer.cd(value)
        self.controller.callbacks.render()
    def _filterOut(self,x=None):
        dirs, files = self.model.explorer.dirList()
        filteringValue = self.views.components.filterSearch.outputs.layout.value
        lister = self.views.components.lister
        if filteringValue != "":        
            lister.outputs.layout.options = ExplorerUtils.dirsWithIcon([".", ".."]) + list(filter(lambda x: ComparerDB.inCompare(filteringValue, x), 
                                                                                                  ExplorerUtils.dirsWithIcon(dirs[2:]) + files))
        else:
            lister.outputs.layout.options = ExplorerUtils.dirsWithIcon(dirs) + files
    def render(self):
        self.views.components.titleLoc.location.outputs.layout.value = self.model.explorer.path
        self.views.components.filterSearch.handlers.handle()
    def _optionSelected(self, val):
        selected =val["owner"].value
        if not selected:
            return 
        if selected.startswith(ExplorerUtils.dirIcon()):
            self.controller.callbacks.folderSelected(self.controller.callbacks.undir(selected))
    def _undir(self, dired):
        return dired[2:]
class Main:
    def osExplorer():
        osfe = OSFileExplorerLC()
        osfe.set_up()
        return osfe