import ipywidgets as widgets
from timeline.t2023.generic_logger.components import SingleButtonController
from modules.Explorer.personalizedWidgets import CustomOutput
from ComparerDB import ComparerDB
from timeline.t2023.searchSystem import Main as SWP
import os
from timeline.t2023.links_crud_ui import SearchEngine
from RegexDB import RegexDB
from ModuleDB import ModuleDB
from timeline.t2023.searchSystem import NotepadOpener
from jupyterDB import jupyterDB
from SearchSystem import MultilineStringSearch
from Path import Path
from LibPath import getPath
from FileDatabase import File
class SearchCopyReloadView:
    def __init__(self):
        self.operations = widgets.Dropdown(options = ["search","copy", "load"], layout=widgets.Layout(width='auto') )
        self.txt = widgets.Text(layout= {"width":"auto"},placeholder='word to search')
        self.reg = widgets.Checkbox(indent=False, layout={'width':"auto"}, description = "reg")
        self.concate = widgets.Checkbox(indent=False, layout={'width':"auto"}, description = "concate")
        self.search = SingleButtonController(description = "search", layout= {"width":"auto"})
        self.out1 = CustomOutput()
        self.out2 = CustomOutput()
        self.layout = widgets.VBox([widgets.HBox([self.operations, self.txt, self.reg,self.concate, self.search.layout]), self.out1.get_layout(), self.out2.get_layout()])
class FilesSearch:
    def search(self, word, reg=False, case=False):
        return self._search_in_files(self._files, word, case=case, reg =reg)
    def _search_in_files(self, files, word, reg, case):
        res = []
        for f in files:
            con = self._content[f]
            for i, line in enumerate(con):
                if ComparerDB.has(word, line, case=case, reg =reg):
                    res.append((f, i+1))
                    break
        return res
    def _search_in_files_line(self, filesWithLines,word, reg =False, case =False):
        res = []
        for f, lineNr in filesWithLines:
            line = self._content[f][lineNr-1]
            if ComparerDB.has(word, line, case=case, reg =reg):
                res.append((f, lineNr))
        return res
    def filter_search(self, words, reg =False, case =False):
        res = []
        files = self._files
        for w in words:
            res =  self._search_in_files(files, w, case=case, reg =reg)
            files = map(lambda x: x[0], res)
        return res
    def concated_search(self, words, reg =False, case=False):
        res = []
        for i, w in enumerate(words):
            if i == 0:
                res = self._search_in_files(self._files, w, case=case, reg =reg)
            else:
                res = self._search_in_files_line(res, w, case=case, reg=reg)
        return res
    def set_files(self, files):
        self._files = files
        self._content = {f: File.getFileContent(f).splitlines() for f in files}
class SearchCopyReloadController:
    def __init__(self):
        self._mss = MultilineStringSearch([])
    def set_display_engine(self, engine):
        self._engine = engine
    def set_up(self):
        self._view.search.set_clicked_func(self._ok_clicked)
    def set_view(self, view: SearchCopyReloadView):
        self._view = view
    def set_file_opener(self, fileopener):
        self._opener = fileopener
    def _result_btn_clicked(self, btn):
        self._clicked(btn , self)
    def _btn_maker(self, resElemInfo, onclick):
        path, lineNr = resElemInfo
        btn = widgets.Button(description=os.path.basename(path), tooltip=path, 
                             layout= {"width": "auto", "max_width": "150px"})
        if onclick is not None:
            btn.on_click(lambda x: onclick(resElemInfo))
        return btn
    def _search(self, resInfo, *param):
        f, n = resInfo
        self._opener.openIt(f, n)
    def _copy(self, resInfo, *param):
        p, n = resInfo
        line = self._engine._engine._content[p][n-1]
        key = self._view.txt.value.lower()
        if key[:2] == "ss" or key[:5] == "class":
            self._mss.set_container(p[:-3].split(os.sep))
            li = ".".join(self._mss.container[self._mss.search("Rlibs") + 1:])
            clssFound = RegexDB.regexSearch("ss [a-zA-Z]+", line)
            clsN = line
            if len(clssFound):
                clsN = clssFound[0].split()[-1]
            impLin = "from " + li + " import " + clsN
            impLin = impLin.replace(".__init__", "")
            self._view.out2.display(ModuleDB.colorPrint("python", impLin), ipy=False, clear=True)
            jupyterDB.clip().copy(impLin)
        elif key[:3] == "def":
            self._mss.set_container(p[:-3].split(os.sep))
            li = ".".join(self._mss.container[self._mss.search("Rlibs") + 1:])
            impLin = "from " + li + " import Main"
            impLin = impLin.replace(".__init__", "")
            self._view.out2.display(ModuleDB.colorPrint("python", impLin), ipy=False, clear=True)
            jupyterDB.clip().copy(impLin)
        else:
            self._view.out2.display(ModuleDB.colorPrint("python", line), ipy=False, clear=True)
            jupyterDB.clip().copy(line)
    def _reload(self, resInfo, *param):
        p, n = resInfo
        line = self._engine._engine._content[p][n-1]
        key = self._view.txt.value.lower()
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
            self._view.out2.display(ModuleDB.colorPrint("python", contet), ipy=False, clear=True)
            exec(contet)
        elif key[:3] == "def":
            self._mss.set_container(p[:-3].split(os.sep))
            li = ".".join(self._mss.container[self._mss.search("Rlibs") + 1:])
            impLin = "from " + li + " import Main"
            impLin = impLin.replace(".__init__", "")
            contet = impLin + "\n"
            contet += "from ModuleDB import ModuleDB\n"
            contet += f"ModuleDB.reloadClass(Main)"
            self._view.out2.display(ModuleDB.colorPrint("python", contet), ipy=False, clear=True)
            exec(contet)
        else:
            jupyterDB.clip().copy(line)
    def set_clicked(self,func):
        self._clicked = func
    def _ok_clicked(self, btn):
        conca = self._view.concate.value
        reg = self._view.reg.value
        word = self._view.txt.value
        typ = self._view.operations.value
        if conca:
            asdndn = {}
            exec(f"dfsdfda={word}",None,asdndn)
            words = asdndn['dfsdfda']
            res = self._engine._engine.concated_search(words, reg=reg)
            self._engine._result_handler.set_container(res)
            ly = self._engine._result_handler.get_layout()
        else:
            ly = self._engine.search(word, reg= reg)
        
        if typ == "search":
            self.set_clicked(self._search)
        elif typ == "copy":
            self.set_clicked(self._copy)
        elif typ == "load":
            self.set_clicked(self._reload)
        self._view.out2.clear()
        self._view.out1.display(ly, clear= True, ipy= True)
class Main:
    def copy_reload_search():
        scrv = SearchCopyReloadView()
        scrc = SearchCopyReloadController()
        fileSearch = FilesSearch()
        fileSearch.set_files(Path.filesWithExtension("py", getPath()))
        scrc.set_display_engine(SWP.searchWithPagination(fileSearch, scrc._btn_maker, scrc._result_btn_clicked))
        scrc.set_view(scrv)
        scrc.set_up()
        scrc.set_file_opener(NotepadOpener())
        return scrc