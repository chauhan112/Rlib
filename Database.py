from ComparerDB import ComparerDB
from FileDatabase import File
from LibPath import *
import os
from SearchSystem import FilesContentSearchEngine, FilePathsSearchEngine, DicSearchEngine
from LibsDB import LibsDB
class DBResources:
    currentDB = None
    location = os.path.dirname(LibsDB.picklePath()) + os.sep + "dbs"
    closed = True
    name = ""
    def getDB():
        return DBResources.currentDB
class DB:
    def createNewDB(dbName):
        import sqlite3
        from Path import Path
        con = sqlite3.connect(Path.joinPath(DBResources.location, dbName))
        con.close()
    def connect2DB(dbName):
        import sqlite3
        from Path import Path
        from TimeDB import TimeDB
        DBResources.currentDB = sqlite3.connect(Path.joinPath(DBResources.location, dbName))
        DBResources.closed = False
        DBResources.name = dbName
        TimeDB.setTimer().oneTimeTimer(30*60, DB.closeConnection)
    def getCurrentDBName():
        return DBResources.name
    def tableNames(conn = None):
        conn = DB._getConn(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return cursor.fetchall()
    def deleteTable(tableName):
        DB.execute(f"DROP TABLE {tableName}")
    def _getConn(conn = None):
        if(conn is None):
            conn = DBResources.getDB()
        return conn
    def columnNames(table, conn = None):
        conn = DB._getConn(conn)
        cursor = conn.execute(f'select * from {table}')
        return [description[0] for description in cursor.description]
    def data(table, conn = None):
        return DB.execute(f"SELECT * FROM {table}")
    def showDBs():
        from Path import Path
        return [os.path.basename(f) for f in Path.filesWithExtension("db", DBResources.location)]
    def execute(statement, conn = None):
        conn = DB._getConn(conn)
        cur = conn.cursor()
        values = list(cur.execute(statement))
        conn.commit()
        return values
    def setLocation(loc):
        DBResources.location = loc
    def closeConnection():
        if(not DBResources.closed):
            DBResources.currentDB.close()
            DBResources.name = ""
        DBResources.closed = True
    def getResources():
        return DBResources
class Table:
    def __init__(self, db, name):
        self.db = db
        self.tableName = name
    def addVal(self, vals):
        cols = DB.columnNames(self.tableName, self.db)[1:1 + len(vals)]
        cmd = f"INSERT INTO {self.tableName}({','.join(cols)}) VALUES ("
        vals = [f"'{v}'" for v in vals]
        state = ",".join(vals)
        cmd += state + ")"
        DB.execute(cmd, self.db)
    def delete(self, condition = ""):
        rows = DB.execute(f"SELECT * from {self.tableName} {condition}", self.db)
        if(len(rows) == 0):
            raise IOError("no data exists for given condition")
        dels = f"DELETE FROM {self.tableName} {condition};"
        if(len(rows) == 1):
            DB.execute(dels, self.db)
        else:
            print("more entries with same key")
    def update(self, setStatement, condition):
        cmd = f"UPDATE {self.tableName} set {setStatement} {condition}"
        print(cmd)
        DB.execute(cmd, self.db)
    def read(self, col = "*", condition= ""):
        cmd = f'SELECT {col} from {self.tableName} {condition}'
        return DB.execute(cmd, self.db)
    def tutorial(self):
        class Temp:
            def conditions():
                print("WHERE colName='colVal'")
            def setValForUpdate():
                print(" SET colName = '{newVal}'")
        return Temp
    def columns(self):
        return DB.columnNames(self.tableName, self.db)
class DatabasePrototype:
    def __init__(self, content):
        self.content = content
    def search(self, word):
        raise IOError("It's a interface. Override this method")
class D2Database(DatabasePrototype):
    def search(self,word, case = False, reg = False):
        founds = []
        for i, val in enumerate(self.content):
            for j, page in enumerate(val):
                if(ComparerDB.has(word, page, case, reg)):
                    founds.append((i,j))
                    break
        return founds
class D1Database(DatabasePrototype):
    def search(self, word,case = False, reg = False):
        founds = []
        for j, val in enumerate(self.content):
            if(ComparerDB.has(word, val, case, reg)):
                founds.append(j)
        return founds
class DictionaryDatabase(DatabasePrototype):
    def search(self, word,case = False, reg = False):
        founds = []
        for val in self.content:
            if(ComparerDB.has(word, val, case, reg) or ComparerDB.has(word, self.content[val], case, reg)):
                founds.append(val)
        return founds
class DBServer:
    def __init__(self, content, db, keyFilter = lambda x: x, displayer = print):
        from WidgetsDB import WidgetsDB
        self.dbHandler = db(content)
        self.keysFilter = keyFilter
        self.displayer = displayer
        self.displayContainer = WidgetsDB.getGrid(5, displayIt= False)
    def search(self, word, case = False, reg = False):
        from WidgetsDB import WidgetsDB
        founds = self.dbHandler.search(word, case, reg)
        self.displayContainer.clearGrid()
        for i in founds:
            name = self.keysFilter(self.getName(i))
            self.displayContainer.append(WidgetsDB.mButton(name, i, self.resultDisplay))
        display(self.displayContainer.mainLayout)
    def getName(self, index):
        raise IOError("set button keys")
    def _setButtonNameFilter(self, keyFilter):
        self.keysFilter = keyFilter
    def _setKeys(self, keys):
        self.keys = keys
    def resultDisplay(self,x):
        self.displayContainer.output.clear_output()
        with self.displayContainer.output:
            self.displayer(self.dbHandler.content[x._key])
    def _setClickedFunction(self, func):
        self.displayer = func
class D1Server(DBServer):
    def __init__(self, keys, displayer = print, keysFilter = lambda x: x):
        super().__init__(keys, D1Database, keysFilter, displayer)
    def getName(self,index):
        return self.dbHandler.content[index]
class D2Server(DBServer):
    def __init__(self, keys, content = None, displayer = File.openFile, keysFilter = lambda x: x,
                    contentExFunc = File.getFileContent):
        if(content is None or content == ''):
            content = [contentExFunc(c) for c in keys]
        if(not(type(content) == list and len(content) == len(keys))):
            raise IOError("Inconsistent inputs")
        super().__init__(content,D2Database, keysFilter, displayer)
        self._setKeys(keys)
    def search(self, word, case = False, reg = False):
        from WidgetsDB import WidgetsDB
        import ipywidgets as widgets
        founds = self.dbHandler.search(word, case, reg)
        self.displayContainer = WidgetsDB.getGrid(4)
        for i,j in founds:
            p = self.keysFilter(self.keys[i])
            self.displayContainer.append(widgets.HBox([WidgetsDB.mButton(p,i, self.resultDisplay),
                widgets.Label(str(j+1))]))
        return self.displayContainer.mainLayout
    def resultDisplay(self,x):
        with self.displayContainer.output:
            self.displayContainer.output.clear_output()
            self.displayer(self.keys[x._key])
class DictionaryServer(DBServer):
    def __init__(self, dic):
        super().__init__(dic, DictionaryDatabase)
    def getName(self, x):
        return x
class Database:
    def getDB(keys, values = '', displayer = File.openFile, contentExtractionFunction = '', keysFilter = lambda x: x):
        if(values == '' and contentExtractionFunction == ''):
            return D1Server(keys, displayer, keysFilter)
        return D2Server(keys, values, displayer,  keysFilter, contentExtractionFunction)
    def pdfDB(files):
        from SearchSystem import PdfSearchEngine
        return PdfSearchEngine(files)
    def resourceDB():
        from Path import Path
        files = Path.getFiles(resourcePath(), walk = True)
        return Database.pathDB(files)
    def moduleDB(keyWord = None, engine = None):
        from LibPath import getPath
        from SearchSystem import FilesContentSearchEngine
        from StaticDisplayerManager import StaticDisplayerManager
        from Path import Path
        from IPython.display import display
        from FileDatabase import NotepadAppTextOpener
        pyfiles = Path.filesWithExtension("py", getPath())
        StaticDisplayerManager.display('total modules file number', len(pyfiles))
        if engine is None:
            engine = FilesContentSearchEngine(nCols=5)
            nato = NotepadAppTextOpener()
            def openIt (paht, lineNr):
                nato.setData(lineNr)
                nato.openIt(paht)
            engine.set_callback(openIt)
            engine.set_tooltip(lambda x: x[0])
        engine.set_content(pyfiles)
        return Database.dbSearch(engine, keyWord)
    def dicDB(dic, displayer = print):
        db = DicSearchEngine(dic)
        db.setCallback(lambda key, val: displayer(val))
        return db
    def urlDB(urlDic):
        from SearchSystem import UrlSearchEngine
        db = UrlSearchEngine(urlDic)
        return db
    def syntaxDB(sytaxDic, syn="python"):
        from ModuleDB import ModuleDB
        from IPython.display import display
        db = Database.dicDB(sytaxDic, displayer=lambda x : display(ModuleDB.colorPrint(syn, x)))
        return db
    def ipynbDB(files):
        from InterfaceDB import ISearchSystem
        from modules.SearchSystem.modular import JupyterResultDisplayer, IResultDisplayer, GDisplayableResult
        from SearchSystem import FilesContentSearch, MultilineStringSearch
        from NotebookDB import NotebookDB
        def display_content(re):
            from ModuleDB import ModuleDB
            filanem, pos = re
            content = "\n".join(NotebookDB.getCodeCellContent(filanem))
            display(ModuleDB.colorPrint("python",content))
        def open_as_file(re):
            from FileDatabase import File, NotepadAppTextOpener
            filanem, pos = re
            temp_file = "ksdfsia12342ajsnfs.py"
            content = "\n".join(NotebookDB.getCodeCellContent(filanem))
            File.overWrite(temp_file, content)
            nato = NotepadAppTextOpener()
            nato.setData(pos)
            nato.openIt(temp_file)
            File.deleteFiles([temp_file])
        class Searcher(FilesContentSearch):
            def __init__(self, files):
                self.container = {path: MultilineStringSearch(NotebookDB.getCodeCellContent(path)) for path in files}
        class Temp:
            def __init__(self,searchSys: ISearchSystem, engine: IResultDisplayer):
                self.searchSystem = searchSys
                self.engine = engine
            def search(self, word, case = False, reg =False):
                res = self.searchSystem.search(word, case, reg)
                res_f = [GDisplayableResult(name, '', (name, nr)) for name, nr in res]
                self.engine.set_result(res_f)
                return self.engine.display()
        jrd = JupyterResultDisplayer()
        jrd.set_callback(display_content)
        return Temp(Searcher(files), jrd)
    def pyRawCodeDB( files=None):
        from Path import Path
        from LibsDB import LibsDB
        if(files is None):
            rawFuncsPath = Path.joinPath(LibsDB.cloudPath(), "global", "code", "Code Godown", "funcs")
            files = Path.filesWithExtension("py", rawFuncsPath)
        return Database.textFilesDB(files)
    def textFilesDB(files, engine = FilesContentSearchEngine, callbackFunc = None):
        return engine(files, callBackFunc= callbackFunc)
    def videoDB(pathOrFiles, displayer = File.openFile):
        from Path import Path
        from ListDB import ListDB
        if(type(pathOrFiles) == str):
            ext = ["mp4", "mkv"]
            pathOrFiles =  ListDB.flatten([Path.filesWithExtension(i, pathOrFiles) for i in ext])
        db = Database.getDB(pathOrFiles, keysFilter=os.path.basename)
        return db
    def forestDB(word = None, engine = FilePathsSearchEngine):
        from Path import Path
        from TreeDB import ForestDB
        db = engine(Path.filesWithExtension("drawio", ForestDB.getForestPath()))
        return Database.dbSearch(db,word)
    def pathDB(filepaths):
        return FilePathsSearchEngine(filepaths)
    def allRunCellDB(_ih = None):
        from IPython.display import display
        from jupyterDB import jupyterDB
        from ListDB import ListDB
        from SerializationDB import SerializationDB
        if(_ih is None):
            _ih = list(set(ListDB.flatten(ListDB.dicOps().flatten(SerializationDB.readPickle(jupyterDB.codeDumper().fileName)).values())))
        from ModuleDB import ModuleDB
        lines = {f'line{i}': _ih[i] for i in range(len(_ih))}
        return Database.dicDB(lines, displayer=lambda x:display(ModuleDB.colorPrint("python",x)))
    def dbSearch(db, word):
        if(word is not None):
            db.search(word)
        return db
    def treeLinkDB(word):
        from UrlDB import UrlDB
        impLinks = UrlDB.getUrl('tree')
        db = Database.urlDB(impLinks)
        return Database.dbSearch(db, word)
