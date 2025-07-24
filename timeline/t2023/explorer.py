import ipywidgets as widgets
import os
from useful.basic import NameSpace, BasicController
from timeline.t2023.generic_logger.components import SingleButtonController
from modules.Explorer.model import OSFileExplorer
from modules.GUIs.model import KeyManager
from modules.Explorer.displayer import ExplorerFileDisplayer
from modules.Explorer.personalizedWidgets import CustomOutput
from enum import Enum
from modules.SearchSystem.modular import HideableWidget

class OPS(Enum):
    FILE_CRUD = 0
    PATH_OPS = 1
    ANALYSIS = 2
    CREATE = 3
    DELETE = 4
    DISPLAY = 5
    OPEN = 6
    COPY = 7
    FILTER = 8
    REMOVE_EMPTY_SPACE = 9
    REMOVE_TRAIL_SPACE = 10
    DEPTH = 11
    COUNT = 12
    SIZE = 13
class Controller(Enum):
    Main = 0
    PaginaCont = 1
    ExplorerCont = 2
    OpsCont = 3
    PickleDisplayer = 4
class PaginationView:
    def __init__(self):
        box_layout = widgets.Layout(display='flex',flex_flow='row', align_items='stretch') 
        self.btns = [widgets.Button(description =str(i+1),layout={"width": "auto"}) for i in range(5)]
        self.btnsBox = widgets.HBox(self.btns)
        self.info = NameSpace()
        self.info.leftDots = widgets.Label("...")
        self.info.maxPageNr = widgets.Label("pMax")
        self.info.rightDots = widgets.Label("...")
        self.pageNrInput = widgets.BoundedIntText( min=0, max=2,layout ={"width":"auto"} )
        self.gotoBtn = widgets.Button(description="go", layout={"width":"auto"})
        self.layout = widgets.HBox([self.info.leftDots, self.btnsBox ,self.info.rightDots,self.info.maxPageNr, 
                                    self.pageNrInput, self.gotoBtn], layout=box_layout)
class ExplorerView:
    def __init__(self):
        self.headerWid = NameSpace()
        self.headerWid.title = widgets.HTML(value='title')
        self.headerWid.currentPath = widgets.Text(placeholder="current/path")
        self.headerWid.selectedFile = widgets.Text(placeholder='output filename', layout=widgets.Layout(width='auto', margin_right="0"))
        self.headerWid.row = widgets.HBox([self.headerWid.currentPath, self.headerWid.selectedFile], layout={"width":"484px", "padding":"0"})
        self.fileFoldersListWid = widgets.Select(rows=15, layout=widgets.Layout(width='484px'))
        self.outputDisplay = CustomOutput()
        self.opsSec = NameSpace()
        self.opsSec.opsDropSec = widgets.Dropdown(options=[OPS.FILE_CRUD.name, OPS.PATH_OPS.name, OPS.ANALYSIS.name], layout={"width":"auto"})
        self.opsSec.opsDrop = widgets.Dropdown(layout={"width":"auto"})
        self.opsSec.okBtn = SingleButtonController(description="ok",layout={"width":"auto"})
        self.opsSec.out1 = CustomOutput()
        self.opsSec.out2 = CustomOutput()
        self.opsRow = widgets.HBox([self.opsSec.opsDropSec, self.opsSec.opsDrop, self.opsSec.okBtn.layout, self.opsSec.out1.get_layout(), 
                               self.opsSec.out2.get_layout()])
        self.pagination = PaginationView()
        self.left_side = widgets.VBox([self.headerWid.title, self.headerWid.row, self.fileFoldersListWid, self.pagination.layout, self.opsRow], 
            layout={"min_width":"488px"})
        self.layout = widgets.HBox([self.left_side, self.outputDisplay.get_layout()])
class PaginationController:
    def __init__(self):
        self.set_options_setter(self._default_options_setter)
        self.set_key_manager(KeyManager())
        self._memoization = {}
        self._pag_size = 100
    def set_pagination_view(self, pagView):
        self._lview = pagView
    def set_basic_controller(self, cnt):
        self._cnt = cnt
    def set_results_container(self, res: list):
        self._results = res
        self._key_manager.set_keys(res)
        for ch in self._lview.btns:
            HideableWidget.showIt(ch)
        if len(res) <= self._key_manager.nrPerPage:
            HideableWidget.hideIt(self._lview.layout)
        else:
            HideableWidget.showIt(self._lview.layout)
            nr = self._key_manager.totalNrOfPages()
            for i in range(nr, 5):
                HideableWidget.hideIt(self._lview.btns[i])
            self._lview.info.maxPageNr.value = str(nr)
            self._lview.pageNrInput.min = 1
            self._lview.pageNrInput.max = nr
            self._update_pagination_btns()
        self._update_content()
    def set_options_setter(self, options_setter):
        self._setter = options_setter
    def _default_options_setter(self, options:list):
        self._cnt.views.ev.fileFoldersListWid.options = options
    def set_up(self):
        self._key_manager.set_limit_per_page(self._pag_size)
        for ch in self._lview.btns:
            ch.on_click(self._pagination_selected)
        self._lview.gotoBtn.on_click(self._goto)
    def set_key_manager(self, key_manager):
        self._key_manager = key_manager
    def _goto(self, btn):
        pageNr = self._lview.pageNrInput.value
        self._key_manager.setCurrentPageIndex(pageNr)
        self._update_pagination_btns()
        self._update_content()
    def _pagination_selected(self, btn):
        self._key_manager.setCurrentPageIndex(int(btn.description))
        self._update_pagination_btns()
        self._update_content()
    def _update_content(self):
        vals = self._key_manager.getKeysForCurrentPageIndex()
        self._setter(vals)
    def _update_pagination_btns(self):
        bts = self._key_manager.getButtonIndices()
        for i, vl in enumerate(bts):
            self._lview.btns[i].description = str(vl)
        if bts[0] != 1:
            HideableWidget.showIt(self._lview.info.leftDots)
        else:
            HideableWidget.hideIt(self._lview.info.leftDots)
        if bts[-1] != self._key_manager.totalNrOfPages():
            HideableWidget.showIt(self._lview.info.rightDots)
        else:
            HideableWidget.hideIt(self._lview.info.rightDots)
class ExplorerController:
    def __init__(self):
        self._dirIcon = "\U0001F4C1"
        self.set_file_selected_func(lambda x, *y: None)
    def set_basic_controller(self, cnt):
        self._cnt = cnt
    def set_up(self):
        self._cnt.views.ev.headerWid.title.value = "OS File Explorer"
        self._cnt.views.ev.headerWid.currentPath.disabled = True
        self._cnt.views.ev.headerWid.selectedFile.disabled = True
        self._update_files_folders()
        self._cnt.views.ev.fileFoldersListWid.observe(self._fileOrFolderSelected, names="value")
    def _update_files_folders(self):
        folders, files = self._cnt._model.dirList()
        folders = list(map(lambda x: self._dirIt(x), folders))
        self._pag_cnt.set_results_container(folders + files)
        self._cnt.views.ev.headerWid.currentPath.value = self._cnt._model.path
    def _fileOrFolderSelected(self, wid):
        curr = self._cnt.views.ev.fileFoldersListWid.label
        val = self._cnt.views.ev.fileFoldersListWid.value
        if curr is not None and curr.startswith(self._dirIcon):
            folder = self._undirIt(curr)
            if folder != ".":
                self._cnt._model.cd(folder)
                self._update_files_folders()
                self._cnt.views.ev.outputDisplay.clear()
        else:
            self._cnt.views.ev.headerWid.selectedFile.value = curr
            self._on_file_selected(wid, self)
    def _dirIt(self, txt):
        return f"{self._dirIcon} {txt}"
    def _undirIt(self, txt):
        return txt.replace(self._dirIcon +" ","" )
    def set_file_opener(self, opener):
        self._opener = opener
    def set_pagination_controller(self, cnt):
        self._pag_cnt = cnt
    def set_file_selected_func(self, func):
        self._on_file_selected = func
class OpsController:
    def __init__(self):
        self._opts = {
            OPS.FILE_CRUD.name: [ OPS.OPEN.name, OPS.DISPLAY.name, OPS.DELETE.name, OPS.CREATE.name, OPS.REMOVE_EMPTY_SPACE.name, OPS.REMOVE_TRAIL_SPACE.name ],
            OPS.PATH_OPS.name: [OPS.COPY.name,OPS.DISPLAY.name,OPS.FILTER.name], 
            OPS.ANALYSIS.name: [OPS.DEPTH.name, OPS.COUNT.name, OPS.SIZE.name ]
        }
        self.set_ok_func(self._default_ok_button)
    def _default_ok_button(self, btn, *param):
        sec = self._basic._view.opsSec.opsDropSec.value
        ops = self._basic._view.opsSec.opsDrop.value
        if sec == OPS.FILE_CRUD.name and ops == OPS.DISPLAY.name:
            path = self._basic._view.fileFoldersListWid.label
            ec = self._basic.get_controller(Controller.ExplorerCont.name)
            if path and not path.startswith(ec._dirIcon):
                self._basic._view.outputDisplay.clear()
                filepath = os.sep.join([self._basic._model.path, path])
                with self._basic._view.outputDisplay.get_out():
                    self._fdispalyer.displayPath(filepath)
    def set_ok_func(self, func):
        self._ok_func = func
    def set_file_displayer(self, file_displayer):
        self._fdispalyer = file_displayer
    def set_basic_controller(self, cont):
        self._basic = cont
    def set_up(self):
        self._basic._view.opsSec.opsDropSec.observe(self._opsChanged, names="value")
        self._opsChanged(self._basic._view.opsSec.opsDropSec)
        self._basic._view.opsSec.opsDrop.value = OPS.DISPLAY.name
        self._basic._view.opsSec.okBtn.set_clicked_func(self._ok_func)
    def _opsChanged(self, wid):
        val = self._basic._view.opsSec.opsDropSec.value
        self._basic._view.opsSec.opsDrop.options = self._opts[val]
class PickleDisplayer:
    def __init__(self):
        self._lay, self._cnt = None, None
    def display(self, file):
        from timeline.t2023.advance_pickle_crud import Main
        if self._lay is None:
            self._lay, self._cnt = Main.pickleCrud(file)
        else:
            self._cnt.set_file(file)
        return self._lay
class Main:
    def osExplorer(path):
        ev = ExplorerView()
        ec = ExplorerController()
        bc = BasicController()
        osExp = OSFileExplorer(os.path.abspath(path))
        bc.set_model(osExp)
        ec.set_basic_controller(bc)
        pc = PaginationController()
        ec.set_pagination_controller(pc)
        pc.set_basic_controller(bc)
        pc.set_pagination_view(ev.pagination)
        pc.set_up()
        ec.set_up()
        oc = OpsController()
        oc.set_basic_controller(bc)
        oc.set_up()
        efd = ExplorerFileDisplayer()
        oc.set_file_displayer(efd)
        pd = PickleDisplayer()
        efd.set_extension_displayer("pkl", pd.display)
        
        bc.controllers.ec = ec
        bc.controllers.pc = pc
        bc.controllers.oc = oc
        bc.controllers.pd = pd
        bc.views.ev = ev
        
        return ev.layout, bc
    def basic_explorer():
        ev = ExplorerView()
        ec = ExplorerController()
        bc = BasicController()
        #bc.set_view(ev)
        ec.set_basic_controller(bc)
        pc = PaginationController()
        ec.set_pagination_controller(pc)
        pc.set_basic_controller(bc)
        pc.set_pagination_view(ev.pagination)
        pc.set_up()
        
        bc.controllers.ec = ec
        bc.controllers.pc = pc
        bc.views.ev = ev
        return bc