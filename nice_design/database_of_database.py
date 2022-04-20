from modules.SearchSystem.modular import JupyterResultDisplayer, DisplayNElement, GDisplayableResult
from modules.Explorer.personalizedWidgets import GenerateNRowsBox, SearchWidget, Main
import ipywidgets as widgets
from nice_design.search import TelegramChannels
from SearchSystem import DicSearch
from Database import Database

class IDatabaseGUI:
    def display(self):
        raise NotImplementedError("abstract method")

class IAbout:
    def display_info(self):
        raise NotImplementedError("abstract method")

class DefaultDatabaseGUI(IAbout):
    def __init__(self):
        from modules.Explorer.personalizedWidgets import SearchWidget
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
            'rlib module':( Database.moduleDB(), 'search in Rlib codes'),
            'code dumper': 'search in the autologged code',
            'pdf files': 'search in the given list of pdf files',
            'notebook ipynb': 'search in given notebook files',
            'text files': 'search in given text files and open at found line number',
            'urls': (UrlDB.db(), 'search in the stored urls history'),
            'resources': 'search in the resources files and open them',
            'forest': 'search in the forest files paths names',
            'video': 'search in the given names of given video paths',
            'pickle db': 'search in all the resource pickle files',
            'syntax': 'search in the programming languages syntaxes', # cpp, py, ubuntu, string formats, git, regexs, sympy
            'dictionary': 'search in the given dictionary and print the content',
            'pycode': 'search in code godown of python',
            'paths': 'search in the stored path',
            'tree content': 'search in the content of drawio files',
            'projects': 'search in archived projects',
            'stuffs': 'search in stuffs logged',
            'telegram channels': (TelegramChannels(True),'search in the telegram exported channels'),
            'qt code library': 'search in qt code library cpp',
            'bachelor': 'search in bachelor subjects content', #android, SWT, machine learning, ihk, data science, maths
        }
        self._info_index = 1
        self._db_index = 0
        self._search_sys = DicSearch({k: self._dbs[k][self._info_index] for k in self._dbs})
        self._jrs = JupyterResultDisplayer()
        self._jrs.set_callback(self._btn_click)
        self._jrs.set_displayer_way(DisplayNElement())
    def search(self, word, case=False, reg=False):
        res = self._search_sys.search(word, case, reg)
        self._jrs.set_result([GDisplayableResult(n, self._dbs[n][self._info_index], n) for n in res])
        self._jrs.display()
    def _btn_click(self, info):
        if type(self._dbs[info]) != tuple:
            print(info , "is not implemented yet")
            return
        db = self._dbs[info][self._db_index]
        if not isinstance(self._dbs[info], IDatabaseGUI):
            db = self._default_db
            db.set_db_info(self._dbs[info][self._info_index])
            db.set_db(self._dbs[info][self._db_index])
        db.display()
