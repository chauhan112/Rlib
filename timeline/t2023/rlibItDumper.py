
# searching in the code. for example: if i want to search in the rlib some function, i could use this function
def codeSearch():
    key = "codeSearch"
    from modules.rlib_notebook_tools.instructions_tool import GElement, GNotebookLayoutController
    from IPython.display import display
    if key in GNotebookLayoutController.instances:
        display(GNotebookLayoutController.instances[key])
        return
    from modules.Explorer.personalizedWidgets import Main as GUIMaker
    from useful.Database import Database
    GNotebookLayoutController.instances[key] = GUIMaker.gui_for_db(Database.moduleDB())
    display(GNotebookLayoutController.instances[key])

# used for copying the application names: For example: this contains all the names of apps i created in the TLCAp and i want to search them, here i can find them all and onclicking
# it copies the name of the application
def apps():
    from IPython.display import display
    from LibPath import getPath
    from modules.rlib_notebook_tools.instructions_tool import GElement, GNotebookLayoutController
    from useful.jupyterDB import  jupyterDB
    import os
    names = jupyterDB.pickle().read("temps")['2023']['app names']
    dic = {v: v for v in names}
    eles = []
    for na in dic:
        ele=GElement(na, jupyterDB.clip().copy)
        ele.setData(dic[na])
        eles.append(ele)
    display(GNotebookLayoutController().get(eles))

# pickle crud operations
def picGui():
    key = "pickleCRUD"
    from timeline.t2023.pickleCrudUI import Main as Mnn
    from modules.rlib_notebook_tools.instructions_tool import GElement, GNotebookLayoutController
    if key in GNotebookLayoutController.instances:
        display(GNotebookLayoutController.instances[key])
        return
    cont = Mnn.pickleCrudGui(False)
    cont.set_scope(globals())
    GNotebookLayoutController.instances[key] = cont._view.layout
    display(GNotebookLayoutController.instances[key])

# overides the value of rlib it
def overrideKey():
    key = "overrideKey"
    from modules.rlib_notebook_tools.instructions_tool import GElement, GNotebookLayoutController
    from useful.jupyterDB import jupyterDB
    from IPython.display import display
    if key in GNotebookLayoutController.instances:
        display(GNotebookLayoutController.instances[key])
        return
    from timeline.t2023.tools import Confirmer
    cc = Confirmer()
    from timeline.t2023.searchSystem import Main as SWP
    from useful.SearchSystem import DicSearch
    from timeline.t2023.generic_logger.components import SingleButtonController
    from timeline.t2023.advance_searcher import Main as SWAO
    class Abc:
        def _btn_maker(self, des, onclick):
            btn = SingleButtonController(description=des, layout= {"width": "auto", "max_width": "150px"})
            btn.set_clicked_func(onclick)
            return btn.layout
        def _cliek(self, wid):
            item = wid.description
            cc.set_callback_function(jupyterDB._params["rlib"].it.add)
            cc.set_params(item)
            self._s_cnt._view.btnOutput.display(cc.get_layout(), True, True)
        def set_searcher(self, cnt):
            self._s_cnt = cnt
    abc = Abc()
    see = SWP.searchWithPagination(DicSearch({k:"" for k in jupyterDB._params["rlib"].it._content.keys()}), abc._btn_maker, abc._cliek)
    cnt = SWAO.search_with_advance_options(see)
    abc.set_searcher(cnt)
    GNotebookLayoutController.instances[key] = cnt._view.layout
    display(GNotebookLayoutController.instances[key])

# helps to reload a key
def refreshKey():
    key = "refreshKey"
    from modules.rlib_notebook_tools.instructions_tool import GElement, GNotebookLayoutController
    from useful.jupyterDB import jupyterDB
    from IPython.display import display
    if key in GNotebookLayoutController.instances:
        display(GNotebookLayoutController.instances[key])
        return
    from timeline.t2023.searchSystem import Main as SWP
    from useful.SearchSystem import DicSearch
    from timeline.t2023.generic_logger.components import SingleButtonController
    from timeline.t2023.advance_searcher import Main as SWAO
    class Abc:
        def _btn_maker(self, des, onclick):
            btn = SingleButtonController(description=des, layout= {"width": "auto", "max_width": "150px"})
            btn.set_clicked_func(onclick)
            return btn.layout
        def _cliek(self, wid):
            ley = wid.description
            from useful.PickleCRUDDB import PickleCRUDOps
            pops = PickleCRUDOps()
            pops.set_pickle_file(Path.filesWithExtension("pkl","_rajaDB")[-1])
            pops.set_always_sync(True)
            pops.set_base_location(['instruction-key-map'])
            maps = pops.readAll()
            key = maps[ley]
            if key is None:
                self._s_cnt._view.btnOutput.display("refresh for "+ ley +" is not defined", True)
                return
            try:
                del GNotebookLayoutController.instances[key]
            except:
                pass
        def set_searcher(self, cnt):
            self._s_cnt = cnt
    abc = Abc()
    see = SWP.searchWithPagination(DicSearch({k:"" for k in jupyterDB._params["rlib"].it._content.keys()}), abc._btn_maker, abc._cliek)
    cnt = SWAO.search_with_advance_options(see)
    abc.set_searcher(cnt)
    
    GNotebookLayoutController.instances[key] = cnt._view.layout
    display(GNotebookLayoutController.instances[key])

# urls manager
def urlsOps():
    from modules.rlib_notebook_tools.instructions_tool import GElement, GNotebookLayoutController
    from IPython.display import display
    import ipywidgets as widgets
    from ancient.UrlDB import UrlDB
    from useful.LibsDB import LibsDB
    from modules.GUIs.urlCRUD import Main
    key = "urls"
    if key in GNotebookLayoutController.instances:
        display(GNotebookLayoutController.instances[key])
        return
    
    db = UrlDB.db()
    def searchResult(btn):
        out.clear_output()
        with out:
            display(db.search(textWdi.value))
    
    tab_contents = ['Search', 'Crud Operation']
    srchBtn = widgets.Button(description="search",layout={'width':"auto"})
    textWdi = widgets.Text(placeholder="word to search")
    srchBtn.on_click(searchResult)
    out = widgets.Output()

    tabs = {     
        'search': widgets.VBox([widgets.HBox([textWdi, srchBtn]), out ]),
        'crud': Main.url_crud_gui(LibsDB.picklePath("urlDB"), displayIt =False).display() }
    tabWid = widgets.Tab()
    tabWid.children = tuple(tabs.values())
    tabWid.titles = [t for t in tab_contents]
    GNotebookLayoutController.instances[key] = tabWid
    display(GNotebookLayoutController.instances[key])

# generic logger v1
def ggn():
    key = "generic-logger"
    from IPython.display import display
    from modules.rlib_notebook_tools.instructions_tool import GElement, GNotebookLayoutController
    if key in GNotebookLayoutController.instances:
        display(GNotebookLayoutController.instances[key].views.glv.views.container.outputs.layout)
        return

    from timeline.t2023.generic_logger import Main
    from timeline.t2023.security import Main as Sec
    cbnt = Main.generic_logger("../../2023/10. oct/logger.pkl", globals())
    cbnt.set_model(Sec.model_with_security("../../2023/10. oct/logger.pkl"))
    GNotebookLayoutController.instances[key] = cbnt
    display(GNotebookLayoutController.instances[key].views.glv.views.container.outputs.layout)

# generic logger v4 (advance search and sort filters ) 
def ggn():
    key = "test-generic-logger"
    from IPython.display import display
    from modules.rlib_notebook_tools.instructions_tool import GNotebookLayoutController
    if key in GNotebookLayoutController.instances:
        display(GNotebookLayoutController.instances[key].process.container.views.container.outputs.layout)
        return
    import os
    from timeline.t2024.generic_logger.generic_loggerV4 import Main
    from useful.LibsDB import LibsDB
    filename = os.sep.join([LibsDB.cloudPath(), 'timeline', '2024', '05_May', "logger_transformed.sqlite"])
    cnt = Main.generic_logger(filename)
    cnt.process.container.views.container.outputs.layout
    GNotebookLayoutController.instances[key] = cnt
    display(cnt.process.container.views.container.outputs.layout)