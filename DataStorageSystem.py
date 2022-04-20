
from ListDB import ListDB
from SerializationDB import SerializationDB
from FileDatabase import File
from Database import Database
from Path import Path, PathServer
import os
from SearchSystem import DicSearchEngine
from RegexDB import RegexDB

tablesName = ["filePaths","folders","instructions","urls","notes"]

class UpdatableEngine(DicSearchEngine):
    def __init__(self, content, params):
        super().__init__(content)
        self.params = params
    def _callback(self, item):
        content = self.searchSys.container[item]
        exec(content)
        self.params.update(locals())
        
class _Tools:
    def advanceDBNameGenerator():
        class Temp:
            def getDBName():
                path = Temp.getPath()
                targetFolder = Path.joinPath(path, "_rajaDB")
                name = Path.joinPath(targetFolder,"pickleDB.name")
                try:
                    dbName = Path.joinPath(targetFolder, File.getFileContent(name))
                except: 
                    from CryptsDB import CryptsDB
                    dbName = CryptsDB.generateRandomName() + ".pkl"
                    File.createFileInsideNonExistingFolder(name, dbName)
                    dbName = Path.joinPath(targetFolder, dbName)
                return dbName
            
            def isItInMonth():
                from RegexDB import RegexDB
                cwd = Temp._cwd()
                sep = "\\\\" if os.sep =="\\" else "/"
                match = RegexDB.isThereRegexMatch(sep.join(["cloud", "timeline", "20\d\d", "\d{1,2}\. "]),cwd)
                return match
            
            def _cwd():
                import os
                return os.getcwd()
            
            def monthPath():
                cwd = Temp._cwd()
                sep = "\\\\" if os.sep =="\\" else "/"
                val = RegexDB.regexSearch( ".*"+ sep.join(["cloud", "timeline", "20\d\d", "\d{1,2}\. "]) +  "[a-zA-Z]+", 
                                    cwd)
                if(len(val) != 0):
                    return val[0]
                raise IOError("Could not find the month path")
            def _create(name, dbName):
                File.createFileInsideNonExistingFolder(name, dbName)
                
            def getPath():
                if (Temp.isItInMonth()):
                    return Temp.monthPath()
                return Temp._cwd()
        
        class advanceDBNameGeneratorTest:
            def __init__(self):
                self.case1()
                self.case2()
                
            def case1(self):
                inp1 = r"C:\Users\49162\Desktop\cloud\timeline\2021\4. apr\home\prj1"
                out = r"C:\Users\49162\Desktop\cloud\timeline\2021\4. apr"
                Temp._cwd = lambda : inp1
                assert(Temp.getPath() == out)
                
            def case2(self):
                inp1 = r"C:\Users\49162\Desktop\cloud\timeline"
                out = r"C:\Users\49162\Desktop\cloud\timeline"
                Temp._cwd = lambda : inp1
                assert(Temp.getPath() == out)
                
        #advanceDBNameGeneratorTest()
        
        return Temp.getDBName()

class PickleDB:
    def __init__(self, pklFile = None):
        self.content = {}
        self.dbName = _Tools.advanceDBNameGenerator()
        if(pklFile is not None):
            self.dbName = pklFile
        self._load()
               
    def _load(self):
        if(not os.path.exists(self.dbName)):
            self._write()
        self.content = SerializationDB.readPickle(self.dbName)
    
    def _write(self):
        SerializationDB.pickleOut(self.content, self.dbName)

class CRUD(PickleDB):
    def __init__(self, tableName, pklFile = None):
        super().__init__(pklFile)
        self.loc = []
        self.tableName = tableName
        self.createTable(tableName)
        
    def add(self, key, val, overwrite = False):
        self._load()
        try:
            self.read(key)
            if(not overwrite):
                print('value already exists')
                return 
        except:
            pass
        loc = self._LocFromkey(key)
        ListDB.dicOps().addEvenKeyError(self.content, loc, val)
        self._write()
    
    def delete(self, key):
        self._load()
        loc = self._LocFromkey(key)
        ListDB.dicOps().delete(self.content, loc)
        self._write()
    
    def read(self, key):
        self._load()
        loc = self._LocFromkey(key)
        val = ListDB.dicOps().get(self.content, loc)
        return val
    
    def update(self, key , newVal):
        self.add(key, newVal, True)
    
    def getStructure(self, key = []):
        content = self.read(key)
        return ListDB.branchPath(content)
    
    def _append2Loc(self, addr):
        if(type(addr)  == list):
            self.loc += addr
        else:
            self.loc.append(addr)
    
    def _LocFromkey(self, key):
        if(type(key) == list):
            return self.loc + key
        return self.loc + [key]
    
    def createTable(self, name):
        global tablesName
        self._load()
        val = ListDB.dicOps().get(self.content, self.loc)
        if(val is not None and name in val):
            if(name not in tablesName):
                print(name + " name already exists.")
            self.loc = [name]
            return
        self.add(name, {})
        self.loc = [name]
        self._write()

    def getContentOfThisTable(self):
        return self.read([])

class AdvanceOps:
    def search(self, word, case = False, reg = False):
        db = self._getDB()
        db.search(word, case, reg)
    
    def _getDB(self): 
        raise IOError("not implemented yet")

class FilePathTable(CRUD, AdvanceOps):
    def __init__(self, childOption = [], dbPklFile = None):
        super().__init__("filePaths", dbPklFile)
        self._append2Loc(childOption)

    def _getDB(self):
        from AIAlgoDB import AIAlgoDB
        class DicTempSearchEngine(DicSearchEngine):
            def _callback(self, item):
                File.openFile(self.searchSys.container[item])
                
        res = ListDB.flatten(self.getStructure())
        files = {}
        for key in res:
            val = self.read(key) 
            if(type(val) == str):
                files[key] = val
        return DicTempSearchEngine(files)

class FolderTable(CRUD, AdvanceOps):
    def __init__(self, childOption = [], dbPklFile = None):
        super().__init__("folders", dbPklFile)
        self._append2Loc(childOption)
        
    def _getDB(self):
        dics = ListDB.dicOps().flatten(self.read([]))
        dics = {key: Path.convert2CloudPath(dics[key]) for key in dics}
        return PathServer(dics, False)

class InstructionTable(CRUD, AdvanceOps):
    def __init__(self, childOption = [], params={}, dbPklFile = None):
        self.params = params
        super().__init__("instructions", dbPklFile)
        self._append2Loc(childOption)
        self.lastVal = None

    def _getDB(self):
        return UpdatableEngine(ListDB.dicOps().flatten(self.getContentOfThisTable()), self.params)
    
    def printContent(self, key, nextCell= False):
        from jupyterDB import jupyterDB
        if(key == ""):
            return self._printSearch(self.read([])).search("")
        content = self.read([])[key]
        if(nextCell):
            get_ipython().set_next_input(content)
            return
        return jupyterDB.displayer(content)
        
    def _printSearch(self,content):
        from jupyterDB import jupyterDB
        class TempDic(DicSearchEngine):
            def _callback(self, item):
                from IPython.display import display
                val = self.searchSys.container[item]
                display(jupyterDB.displayer(val))
        return TempDic(content)
        
    def getLastOverwrittenVal(self):
        print(self.lastVal)
        
    def add(self, key, val =None):
        from jupyterDB import jupyterDB
        if(val is None):
            val = jupyterDB.clip().text()
        content = self.read([])
        if(key in content):
            self.lastVal = content[key]
        super().add(key, val, True)
    
    def archive(self, key = None):
        pass
    
class UrlsTable(CRUD, AdvanceOps):
    def __init__(self, childOption = [],dbPklFile = None):
        super().__init__("urls", dbPklFile)
        self._append2Loc(childOption)
    
    def _getDB(self):
        dic = ListDB.dicOps().flatten(self.read([]))
        return Database.urlDB(dic)

    def cat():
        ut = UrlsTable()
        return ut.getContentOfThisTable().keys()
        
class NotesTable(CRUD,AdvanceOps):
    def __init__(self, childOption = [], dbPklFile = None):
        super().__init__("notes", dbPklFile)
        self._append2Loc(childOption)
    
    def _getDB(self):
        return DicSearchEngine(ListDB.dicOps().flatten(self.read([])))
        
class LocalTree:
    def __init__(self, miniForestPath = None):
        self.pklPath = miniForestPath
        
    def add(self, name,overwrite = False):
        from ClipboardDB import ClipboardDB
        k = self._reader()
        if(name in k and not overwrite):
            raise IOError("Name already exits")
        content = ClipboardDB.getText()
        k[name] = content
        self._writer(k)
        print("Total number of trees in the forest : " + str(len(k)))
        print("Content size : " + str(len(content)))

    def search(self, word, reg = False):
        from Database import D1Database
        from WidgetsDB import WidgetsDB
        from ClipboardDB import ClipboardDB
        trees = self._reader()
        vals = list(trees.keys())
        db = D1Database(vals)
        k = [vals[x] for x in db.search(word, reg = reg)]
        def copy(x):
            ClipboardDB.copy2clipboard(trees[x.description])
        return WidgetsDB.getGrid(7, [WidgetsDB.button(name=x, callbackFunc=copy, tooltip=x) for x in k])
    
    def updateKey(self, oldname, newName):
        con = self._reader()
        con[newName] = con.pop(oldname)
        self._writer(con)
        
    def _writer(self, k):
        SerializationDB.pickleOut(k, self._fileName())
        
    def _reader(self):
        return SerializationDB.readPickle(self._fileName())
    
    def _fileName(self):
        if(self.pklPath is not None):
            return self.pklPath
        from Path import Path
        path = Path.joinPath(os.path.dirname(_Tools.advanceDBNameGenerator()), "miniForest.pkl")
        if(not os.path.exists(path)):
            SerializationDB.pickleOut({}, path)
        return path
        
    def keys(self):
        return self._reader().keys()
        
class TestSite:
    def FilePathTableTest():
        try:
            Path.deleteFolder("_rajaDB")
        except:
            pass
        tab = FilePathTable()
        getContent = lambda : SerializationDB.readPickle(tab.dbName)
        assert ( getContent() == {'filePaths': {}})
        class FilePathTableTest:
            def addtest(tab):
                # overwrite false
                tab.add("ausbildungsnachwies 122020", r"D:\cloud\timeline\2021\1. jan\12.2020.pdf" )
                output = {'filePaths': {'ausbildungsnachwies 122020': r"D:\cloud\timeline\2021\1. jan\12.2020.pdf"}}
                assert (getContent() == output) , "add withot overwrite failed"
                # overwrite true
                tab.add("ausbildungsnachwies 122020", "new something" ,1 )
                output = {'filePaths': {'ausbildungsnachwies 122020': "new something"}}
                k = getContent()
                assert(k == output) , "add with overwrite failed"
                
            def deleteTest(tab):
                tab.delete("ausbildungsnachwies 122020")
                output = {'filePaths': {}}
                assert (getContent() == output), "delete failed"
                
            def modifytest(tab):
                tab.add("ausbildungsnachwies 122020", r"D:\cloud\timeline\2021\1. jan\12.2020.pdf" )
                output = {'filePaths': {'ausbildungsnachwies 122020': "modifyTest"}}
                tab.update("ausbildungsnachwies 122020","modifyTest" )
                assert (getContent() == output)
                
            def readTest(tab):
                tab.add("ausbildungsnachwies 122020", r"D:\cloud\timeline\2021\1. jan\12.2020.pdf", 1 )
                output = r"D:\cloud\timeline\2021\1. jan\12.2020.pdf"
                assert tab.read("ausbildungsnachwies 122020") == output
        FilePathTableTest.addtest(tab)
        FilePathTableTest.deleteTest(tab)
        FilePathTableTest.modifytest(tab)
        FilePathTableTest.readTest(tab)
        
    def synctest():
        try:
            Path.deleteFolder("_rajaDB")
        except:
            pass
            
        f = FolderTable("aaa")
        ett = UrlsTable("aaa")
        f.add("dummy path", "")
        ett.add("dummy url", "")
        ett._load()
        f._load()
        assert(f.content == ett.content)