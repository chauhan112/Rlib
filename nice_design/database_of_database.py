from modules.SearchSystem.modular import JupyterResultDisplayer, DisplayNElement, GDisplayableResult
import ipywidgets as widgets
from nice_design.search import TelegramChannels
from modules.GUIs.search_guis import CodeDumperSearchGUI, FileSearchGUI, SyntaxSearchGUI, BachelorSubjectSearchGUI,\
    CodesGodownSearch
from modules.Explorer.personalizedWidgets import SearchWidget
from SearchSystem import DicSearch
from Database import Database
from nice_design.interfaces import IDatabaseGUI, IAbout
from TreeDB import ForestDB
from modules.Logger.ideas import IdeasSearchEngine
from PickleCRUDDB import PickleSearchEngine

class DefaultDatabaseGUI(IAbout, IDatabaseGUI):
    def __init__(self):
        self._sw = SearchWidget()
    def display(self):
        print(self.display_info())
        display(self._sw.get())
    def set_db(self, db):
        self._sw.set_database(db)
    def set_db_info(self, info):
        self._info = info
    def display_info(self):
        return self._info

class DatabaseOfDatabases:
    def __init__(self):
        from UrlDB import UrlDB
        self._default_db = DefaultDatabaseGUI()
        self._dbs = {
            'rlib module':( Database.moduleDB, 'search in Rlib codes'),
            'code dumper': (CodeDumperSearchGUI,'search in the autologged code'),
            'text files': (FileSearchGUI,'search in the text files'), # pdf, text, video, ipynb
            'urls': (UrlDB.db, 'search in the stored urls history'),
            'resources': (Database.resourceDB,'search in the resources files and open them'),
            'forest': (Database.forestDB, 'search in the forest files paths names'),
            'pickle db': (PickleSearchEngine,'search in all the resource pickle files'),
            'syntax': (SyntaxSearchGUI, 'search in the programming languages syntaxes'),
            'pycode': (CodesGodownSearch.py, 'search in code godown of python'),
            'tree content': (ForestDB, 'search in the content of drawio files'),
            'stuffs': 'search in stuffs logged',
            'telegram channels': (lambda : TelegramChannels(True),'search in the telegram exported channels'),
            'qt code library': (CodesGodownSearch.cpp,'search in cpp code library qt'),
            'bachelor': (BachelorSubjectSearchGUI, 'search in bachelor subjects content'),
            'js code godown': (CodesGodownSearch.js, "search in the all js files from code godown"),
            'ideas': (IdeasSearchEngine, "search in logged ideas")
        }
        self._info_index = 1
        self._db_index = 0
        self._search_sys = DicSearch({k: self._dbs[k][self._info_index] for k in self._dbs})
        self._jrs = JupyterResultDisplayer()
        self._jrs.set_callback(self._btn_click)
        self._jrs.set_displayer_way(DisplayNElement())
        self._db_map = {}
    def search(self, word, case=False, reg=False):
        res = self._search_sys.search(word, case, reg)
        self._jrs.set_result([GDisplayableResult(n, self._dbs[n][self._info_index], n) for n in res])
        self._jrs.display()
    def _btn_click(self, info):
        if type(self._dbs[info]) != tuple:
            print(info , "is not implemented yet")
            return
        db = self._get_instance(info)
        db.display()
    def _get_instance(self, key):
        if key not in  self._db_map:
            db = self._dbs[key][self._db_index]()
            if not isinstance(db, IDatabaseGUI):
                dbg = DefaultDatabaseGUI()
                dbg.set_db_info(self._dbs[key][self._info_index])
                dbg.set_db(db)
                db = dbg 
            self._db_map[key] = db
        return self._db_map[key]
    def get_search_result_layout(self,word, case = False, reg = False):
        res = self._search_sys.search(word, case, reg)
        self._jrs.set_result([GDisplayableResult(n, self._dbs[n][self._info_index], n) for n in res])
        return self._jrs.get_result_layout()