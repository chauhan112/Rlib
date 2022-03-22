import os

class Explorer:
    def __init__(self, content):
        self.content = content
        
    def cd(self, key):
        return NotImplementedError("Please implement getNext with key")
    
    def goBack(self):
        return NotImplementedError("Please implement goBack")

class ExplorerUtils:
    def dirsWithIcon(dirList):
        return ['\U0001F4C1 ' + dirname for dirname in dirList]

    def dirIcon():
        return "\U0001F4C1"
    
    def driveStartPath():
        return []
    
    def _driveStartPath():
        import sys
        import string
        from ListDB import ListDB
        from jupyterDB import jupyterDB
        
        class Cache:
            def readVal(indexName):
                vals = Cache._read()
                return ListDB.dicOps().get(vals, Cache._loc(indexName))
            
            def _read():
                return jupyterDB.pickle().read("temps")
            
            def writeVal(index, val):
                vals = Cache._read()
                ListDB.dicOps().add(vals, Cache._loc(index), val)
                
            def _loc(name):
                return ['rlibs','ExplorerUtils','driveStartPath', name]
        
        if(Cache.readVal("index") == Cache.readVal("lastIndex")):
            return Cache.readVal("value")
        
        a = []
        if sys.platform == 'win32':
            a = [
                '%s:\\' % d for d in string.ascii_uppercase
                if os.path.exists('%s:' % d)
            ]
        Cache.writeVal('lastIndex', Cache.readVal('index'))
        Cache.writeVal("value", a)
        return a

    def getDropdownPathSubList(path):
        if os.path.isfile(path):
            path = os.path.dirname(path)
        paths = [path]
        path, tail = os.path.split(path)
        while tail:
            paths.append(path)
            path, tail = os.path.split(path)
        try:
            drives = ExplorerUtils.driveStartPath()
            drives.remove(paths[-1])
            paths.extend(drives)
        except ValueError:
            pass
        return paths

class FileExplorerWithPaths:
    def __init__(self, paths, sep = "/"):
        self.paths = paths
        self._currentPath = ''
        self.sep = sep

    def dirList(self):
        return NotImplementedError("Function Not Implemnted")

    def goBack(self):
        self._currentPath = self.sep.join(self._currentPath.split(self.sep)[:-1])

    def cd(self,path):
        return NotImplementedError("Function Not Implemnted")

    @property
    def currentPath(self):
        return self._currentPath

class ZipFileExplorer(FileExplorerWithPaths):
    def __init__(self, zipPath):
        from ZiptoolDB import ZiptoolDB
        self.tool = ZiptoolDB
        if(type(zipPath) == list):
            raise IOError("Give zip path")
        paths  = ZiptoolDB.getZipContent(zipPath)
        self.zipPath = zipPath
        self._extractingPath = "." + os.path.basename(self.zipPath)[:-4]
        super().__init__(paths)
    
    def dirList(self):
        from ListDB import ListDB
        files = []
        folders = set([])
        paths = ListDB.listFilter(lambda x: x.startswith(self._currentPath), self.paths)
        paths = ListDB.listMap(lambda x: x[len(self._currentPath):], paths)
        for p in paths:
            k = self._getFileOrFolder(p)
            if(k is not None):
                name , isFolder = k
                if(isFolder):
                    if(name != ''):
                        folders.add(name)
                else:
                    files.append(name)
        folders = list(folders)
        if self.currentPath != '':
            folders.insert(0, '..')
        folders.insert(0, '.')
        return folders, files
    
    def _getFileOrFolder(self,path):
        isFolder = path.endswith(self.sep)
        k = path.strip(self.sep).split(self.sep)
        if(len(k) == 0 or k == ''):
            return None
        if(len(k) > 1):
            isFolder = True
        return k[0], isFolder
    
    def cd(self, fold = None):
        if(fold is None):
            return self._currentPath

        if(fold.strip() == '..'):
            self.goBack()
            return

        folders,_ = self.dirList()
        if(fold in folders):
            if(self._currentPath == ''):
                self._currentPath = fold
            else:
                self._currentPath += self.sep + fold
        else:
            print("No such folder")
    def extract(self, filename):
        path = self._currentPath + self.sep + filename
        if(self._currentPath == ''):
            path = filename
        self.tool.extractWithPaths(self.zipPath, [path], to= self._extractingPath)

class OSFileExplorer(Explorer):
    def __init__(self,initialPath = None):
        self.path = initialPath
        if(initialPath is None):
            self.path = os.path.abspath('.')
        self.sep = os.sep
    
    def cd(self, key):
        k = self.path + self.sep + key
        if(self.path == ''):
            k = key
        if(key == '..'):
            return self.goBack()
        if(key == '.'):
            return
        if(os.path.exists(k)):
            self.path = k
        else:
            print(f"{k} does not exists")
    
    def goBack(self):
        self.path = self.sep.join(self.path.split(self.sep)[:-1])
        
    def dirList(self):
        listDir = os.listdir(self.path + os.sep)
        if(self.path == ''):
            listDir = ExplorerUtils.driveStartPath()
        files = []
        folders = []
        for val in listDir:
            if(os.path.isdir(self.sep.join([self.path, val]))):
                folders.append(val)
            else:
                files.append(val)
        
        if os.path.basename(self.path) != '':
            folders.insert(0, '..')
        folders.insert(0, '.')   
        return folders, files

class DictionaryExplorer(Explorer):
    def __init__(self, dic):
        super().__init__(dic)
        self.currentPath = []
    
    def cd(self, key):
        if(key == '..'):
            return self.goBack()
        self.currentPath.append(key)
        try:
            return self.keys()
        except:
            self.currentPath.pop()
            print('Key error')

    def goBack(self):
        if(self.currentPath == []):
            return
        self.currentPath.pop()
    
    def keys(self):
        p = self.content
        for key in self.currentPath:
            p = p[key]
        folders = []
        vals = []
        if(type(p) == dict):
            for k in list(p.keys()):
                if(type(p[k]) in [dict, list]):
                    folders.append(k)
                else:
                    vals.append(k)
        elif(type(p) == list):
            for i,val in enumerate(p):
                if(type(val) == dict):
                    folders += str(i)
                else: 
                    vals.append(str(type(val)))
        return folders, vals

    def getCurrentValue(self):
        p = self.content
        for key in self.currentPath:
            p = p[key]
        return p
        
class IExplorer:
    def cd(self, key):
        raise NotImplementedError('abstract method')
    
    def dirList(self):
        raise NotImplementedError('abstract method')
        
    def goBack(self):
        raise NotImplementedError('abstract method')
    
    def getCurrentPath(self):
        raise NotImplementedError('abstract method')
    
    def setCurrentPath(self, path):
        raise NotImplementedError('abstract method')
    def displayContent(self, path):
        raise NotImplementedError('abstract method')
        
class ZipExplorerWithFilter(ZipFileExplorer):
    def __init__(self, zipPath):
        super().__init__(zipPath)
        self.paths = self.filterPaths()

    def filterPaths(self):
        raise IOError("implement this method")

class ZipExplorer:
    def __init__(self, zipPath):
        from ZiptoolDB import ZiptoolDB
        self.tool = ZiptoolDB
        from modules.FileAnalyser.FileAnalyser import FileList2Dic
        from modules.mobileCode.CmdCommand import DicList
        self.zipPath = zipPath
        
        files = ZiptoolDB.getZipContent(zipPath)
        fl = FileList2Dic("/")
        fl.setData(files)
        self._content = fl.execute()
        self._exp = DicList()
        self._exp.setData(self._content)
        self.deltaVal = 40
        self._from = 0
        self._currentList = self._exp.get()
        
        
        self._extractingPath = "." + os.path.basename(self.zipPath)[:-4]
        self.currentPath = "/".join(self._exp.dicExp.currentPath)
        self.sep = "/"
        
    def dirList(self):
        from ListDB import ListDB
        vals = self._currentList[self._from: self._from+self.deltaVal]
        folders = []
        files = []
        for val in vals:
            if val == '..':
                continue
            content =ListDB.dicOps().get(self._exp.dicExp.content, 
                                         self._exp.dicExp.currentPath+ [val])
            if type (content) == dict and content != {}:
                folders.append(val)
            else:
                files.append(val)
            params = ['..', f'... t:{len(self._currentList)} f:{self._from}']
            if self._from > 0:
                params = ['^^^'] + params
        return ['.',*params] + folders, files
    
    def cd(self, val):
        valList = val.split()
        if valList[0] == "...":
            val = valList[0]
        if val == '.':
            return
        if val == '..':
            self._from = 0
            self._exp.dicExp.goBack()
            self._currentList = self._exp.get()
            return
        if val == '...':
            if self._from + self.deltaVal < len(self._currentList):
                self._from += self.deltaVal
            return
        if val == '^^^':
            if self._from - self.deltaVal >= 0:
                self._from -= self.deltaVal
            return
        self._exp.dicExp.cd(val)
        self._currentList = self._exp.get()
        self.currentPath = "/".join(self._exp.dicExp.currentPath)
        
    def extract(self, filename):
        path = "/".join(self._exp.dicExp.currentPath + [filename])
        if(path == ''):
            path = filename
        self.tool.extractWithPaths(self.zipPath, [path], to= self._extractingPath)


class ExplorerTest:
    def test_getLevel1FileOrFolder():
        cases = ['drawio-master/drawio-master/src/main/webapp/connect/gdrive_common/editor.js',
                'drawio-master/drawio-master/src/main/webapp/connect/gdrive_common/',
                '/gdrive_common/editor.js',
                'editor.js',
                'drawio-master/', 
                '']
        outputs = [('drawio-master', True), ('drawio-master', True), ('gdrive_common', True),
            ('editor.js', False),('drawio-master', True), None ]
        a = ZipFileExplorer('')
        for inp, out in zip(cases, outputs):
            assert a._getFileOrFolder(inp) == out