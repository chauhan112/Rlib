from useful.SearchSystem import FilesContentSearch, MultilineStringSearch
from useful.RegexDB import RegexDB
from useful.ModuleDB import ModuleDB
from timeline.t2023.searchSystem import CodeSearchEngine
from timeline.t2023.searchSystem import Main as SWP
from timeline.t2023.advance_searcher import Main as SWAO
import os
class ModuleReloader:
    def btn_click(self,detail):
        contet = f"from {self.dic[detail.description]} import {detail.description}\n"
        contet += "from ModuleDB import ModuleDB\n"
        contet += f"ModuleDB.reloadClass({detail.description})"
        exec(contet)
        self._swwov._click_display_region.display(ModuleDB.colorPrint("python", contet), ipy=False, clear=True)
    def old_main(self):
        from useful.SearchSystem import DicSearch
        from useful.SerializationDB import SerializationDB
        from useful.LibsDB import LibsDB
        from timeline.t2023.DBSearchGUIWithOutput import SearchWidgetWithOutputVisible
        from timeline.t2023.links_crud_ui import SearchEngine, ButtonViewWithPagination
        self.dic = SerializationDB.readPickle(LibsDB.picklePath("fromFileImportClass"))
        ds = DicSearch(self.dic)
        se = SearchEngine()
        se.default_display(False)
        bvwp =ButtonViewWithPagination()
        bvwp.set_btn_click_func(self.btn_click)
        se.set_engine(ds)
        se.set_result_maker(bvwp)
        self._swwov = SearchWidgetWithOutputVisible()
        self._swwov.set_database(se)
        lay =self._swwov._make_layout()
        self._swwov.set_up()
        return lay
    def load_lib_files(self):
        from useful.Path import Path
        from LibPath import getPath
        self._fcs = FilesContentSearch(Path.filesWithExtension("py", getPath()))
        self._mss = MultilineStringSearch([])
    def clicked(self, res):
        p, n = res
        line = self._fcs.container[p].container[n-1]
        key = self._searcher._key.lower()
        if key[:2] == "ss" or key[:5] == "class":
            self._mss.set_container(p[:-3].split(os.sep))
            li = ".".join(self._mss.container[self._mss.search("Rlibs") + 1:])
            clssFound = RegexDB.regexSearch("ss [a-zA-Z]+", line)
            clsN = line
            if len(clssFound):
                clsN = clssFound[0].split()[-1]
            impLin = "from " + li + " import " + clsN
            impLin = impLin.replace(".__init__", "")
            contet = impLin + "\n"
            contet += "from ModuleDB import ModuleDB\n"
            contet += f"ModuleDB.reloadClass({clsN})"
            exec(contet)
            self._cnt._view.btnOutput.display(ModuleDB.colorPrint("python", contet), ipy=False, clear=True)
        elif key[:3] == "def":
            self._mss.set_container(p[:-3].split(os.sep))
            li = ".".join(self._mss.container[self._mss.search("Rlibs") + 1:])
            impLin = "from " + li + " import Main"
            impLin = impLin.replace(".__init__", "")
            contet = impLin + "\n"
            contet += "from ModuleDB import ModuleDB\n"
            contet += f"ModuleDB.reloadClass(Main)"
            exec(contet)
            self._cnt._view.btnOutput.display(ModuleDB.colorPrint("python", contet), ipy=False, clear=True)
        else:
            from useful.jupyterDB import jupyterDB
            jupyterDB.clip().copy(line)
    def set_searcher(self, cnt):
        self._searcher = cnt
    def main(self):
        see = SWP.searchWithPagination(self._fcs, CodeSearchEngine()._button_maker, self.clicked )
        self.set_searcher(see)
        self._cnt = SWAO.search_with_advance_options(see)
        return self._cnt._view.layout