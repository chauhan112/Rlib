from SerializationDB import SerializationDB
from LibsDB import LibsDB
from Path import Path
from ListDB import ListDB
from SearchSystem import SearchEngine, SearchSystem
import os
from InterfaceDB import ISearchSystem
from ComparerDB import ComparerDB
from jupyterDB import jupyterDB

class PickleCRUD:
    def __init__(self, name, loc = [], loadFromMain= True):
        self._loadFromMainFolder = loadFromMain
        self.pklName = name
        self.loc = loc
        self.content = self._load()
        
    def read(self, key):
        self._load()
        loc = self._LocFromkey(key)
        val = ListDB.dicOps().get(self.content, loc)
        return val

    def add(self, key, val, overwrite = False):
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
        
    def _LocFromkey(self, key):
        if(type(key) == list):
            return self.loc + key
        return self.loc + [key]
    
    def _load(self):
        if self._loadFromMainFolder:
            self.content = jupyterDB.pickle().read(self.pklName)
        else:
            self.content = SerializationDB.readPickle(self.pklName)
        return self.content
    
    def _write(self):
        if self._loadFromMainFolder:
            jupyterDB.pickle().write(self.content, self.pklName)
        else:
            SerializationDB.pickleOut(self.content, self.pklName)
        
    def delete(self, key):
        self._load()
        loc = self._LocFromkey(key)
        ListDB.dicOps().delete(self.content, loc)
        self._write()
    
    def getStructure(self, key = []):
        content = self.read(key)
        return ListDB.branchPath(content)
    
    def _append2Loc(self, addr):
        if(type(addr)  == list):
            self.loc += addr
        else:
            self.loc.append(addr)
    def getContent(self):
        return self.read([])
    
    def searchInDB(word= None):
        from Database import Database
        db = PickleSearchEngine()
        return Database.dbSearch(db, word)

class DictypePickle(PickleCRUD):
    def getKeys(self):
        return self.content.keys()
    
    def addContent(self, itemsAsDic):
        self.content.update(itemsAsDic)
    
    def getContent(self, key):
        return self.content

class PickleSearch(ISearchSystem):
    def __init__(self, pklPath =None):
        binFiles = ['abstraction.pkl']
        if(pklPath is None): 
            pklPath = LibsDB.picklePath()
        files = list(filter(lambda x: os.path.basename(x) not in binFiles,
                              Path.filesWithExtension("pkl", pklPath)))
        super().__init__(files)
        
    def search(self, word, case = False, reg = False):
        founds = []
        for path in self.container:
            val = self._search(path, word, case, reg)
            if val:
                founds.append((path, val))
        return founds
    
    def _search(self, path, word, case, reg):
        pkl = SerializationDB.readPickle(path)
        branchedPath = ListDB.branchPath(pkl)
        for l1 in branchedPath:
            for val in l1:
                if( ComparerDB.has(word, val, case, reg )):
                    return l1

class AdvancePickleSearch(PickleSearch):
    def __init__(self, pkl=None,compareFunc=None):
        self._compareFunc = compareFunc
        super().__init__(pkl)
    def comp(self, val, x, case, reg):
        if type(x) == str:
            return ComparerDB.has(val, x, case, reg)
        return val == x
    def search(self, word, case = False, reg = False):
        founds = []
        for path in self.container:
            val = SearchSystem.pickle_search(SerializationDB.readPickle(path), 
                lambda x: self.comp(word, x, case, reg), searchInKey=True)
            if len(val) > 0:
                founds.append((path, val))
        return founds
        
        
class PickleSearchEngine(SearchEngine):
    def __init__(self):
        super().__init__(None, PickleSearch)
        
    def buttonName(self, item):
        return os.path.basename(item[0])
    
    def toolTip(self, item):
        return os.path.basename(",".join(item[1]))
    
    def _callback(self, item):
        path, keys = item
        from SerializationDB import SerializationDB
        from ExplorerDB import ExplorerDB
        k = SerializationDB.readPickle(path)
        ExplorerDB.dicExplorer(k)
        
class RunBasicOps:
    name = "runBasic"
    def add(key, value = None, overwrite = False):
        if(value is None):
            value = jupyterDB.clip().text()
        k = RunBasicOps._read()
        if(key in k):
            if(not overwrite):
                print("key already exists")
                return 
        k[key] = value
        RunBasicOps._write(k)
        
    def delete(key):
        k = RunBasicOps._read()
        del k[key]
        RunBasicOps._write(k)
        
    def showAll():
        import LibPath as lp
        return jupyterDB.displayer(lp.runBasic())
    
    def _read():
        return jupyterDB.pickle().read(RunBasicOps.name)
    
    def _write(k):
        jupyterDB.pickle().write(k, RunBasicOps.name)
    
    def get(key):
        return jupyterDB.displayer(RunBasicOps._read()[key])