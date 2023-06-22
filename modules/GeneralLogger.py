import os, shutil
from ComparerDB import ComparerDB
from Path import Path

class PathWorkspace:
    def __init__(self, rootPath):
        self._rootPath = rootPath
        
    def doesFileExists(self, filePath):
        return os.path.exists(self._path(filePath))
    
    def download(self, filePath, to="."):
        toPath = os.path.abspath(to)
        Path.copyFiles([self._path(filePath)], toPath)
    
    def _path(self, relPath):
        return Path.joinPath(self._rootPath, relPath)
    
    def copyTo(self, file, toPath):
        toPath = self._path(toPath)
        shutil.copy2(file, toPath)
        
    def rootPath(self):
        return self._rootPath
    
    def deleteFile(self, filePath):
        Path.delete([self._path(filePath)])
    
    def showAsExplorer(self):
        from ExplorerDB import ExplorerDB
        return ExplorerDB.osFileExplorer(self._rootPath)

class CloudWorkspace(PathWorkspace):
    def __init__(self):
        super().__init__(self._cloudPath())

    def _cloudPath(self):
        from LibsDB import LibsDB
        return Path.joinPath(LibsDB.cloudPath(), 'Global', 'code', 'resources')
    
class LocalCloudEquivalentPath(PathWorkspace):
    def __init__(self):
        super().__init__(localCloudEqPath)

class ContentType:
    Text = 0
    File = 1
    
class LogItem:
    def __init__(self,_id=None, title=None, data=None, tags= []):
        # self.data is a list if item
        self.load(_id, title, data, tags)
    
    def load(self,_id=None, title=None, data=None, tags= []):
        self.eleKey = _id
        self.title = title
        self.data = data
        self.tags = tags
        
    def getData(self):
        return [c.getContent() for c in self.data]
    
class IItem:
    def getContent(self):
        raise IOError("Not implemented yet")
    
    def toString(self):
        raise IOError("Not implemented yet")
    
    def toHtml(self):
        raise IOError("Not implemented yet")
        
class Text(IItem):
    def __init__(self, data):
        self.data = data
    
    def getContent(self):
        return (ContentType.Text, self.data)
    
    def toString(self):
        return self.data
    
    def toHtml(self):
        return self.data
    
class NFile(IItem):
    def __init__(self, path, space: PathWorkspace= CloudWorkspace, pre=''):
        self.path = path
        self.workSpace = space
        self._storedPath = None
        self.prefix = pre
        self.store()
        
    def store(self):
        name = self.prefix+os.path.basename(self.path)
        storedPath = Path.joinPath(self._path2folder(self.path), name)
        self.workSpace().copyTo(self.path, storedPath)
        self._storedPath = storedPath
    
    def getContent(self):
        return (ContentType.File, self._storedPath)
    
    def _path2folder(self, filePath):
        p = {'mp3': 'audios', 'wav': 'audios', '3gp': 'audios', 'm4a': 'audios', 'mp4': 'videos', 'webm': 'videos', 
            'mkv': 'videos', 'flv': 'videos', 'avi': 'videos', 'txt': 'docs', 'pdf': 'docs', 'docs': 'docs', 
             'csv': 'docs', 'md': 'docs',"zip":"others", "jpg": "photos", "png":"photos", "gif":"photos", 
             "svg":"photos", "ipynb": "scripts", 'py':"scripts", "java": "scripts", "jpeg": "photos"}
        ext = os.path.basename(filePath).split(".")[-1].lower()
        if(ext in p):
            return p[ext]
        return 'others'
    
    def toString(self):
        return self._storedPath
    
    def toHtml(self):
        return self._storedPath
    
class LogFactory:
    def create(title, contentList, tag):
        from CryptsDB import CryptsDB
        uudi = CryptsDB.generateUniqueId()
        return LogItem(uudi, title, contentList, tag)

class GeneralLogger:
    def __init__(self):
        self.storageID = '6444900520fc49bcb425ee3a453da6e6'
        self._dataCrud = self._read()
        self._indexed = None
        
    def _read(self):
        from StorageSystem import StorageSystem
        return StorageSystem.dataStructureForIndex(self.storageID)
    
    def add(self,element: LogItem, overwrite = False):
        self._dataCrud.add(element.eleKey, {'title': element.title, 'content': element.getData(), 
                            'tags': element.tags}, overwrite)
        
    def db(self,tag=''):
        from SearchSystem import GeneralSearchEngine, GSearch
        
        content = self._dataCrud.getContent()
        tags = set(map(lambda x: x.strip(), tag.split(",")))
        tags.discard('')
        en = GeneralSearchEngine(content, searchFunc=lambda word, con, case, reg:GeneralSearchEngine.tools().iterate(
                    con, ifFunc=lambda i, key, con: ((len(tags.intersection(set(con[key]['tags']))) != 0  or 
                                                     len(tags) == 0)
                            and 
                        ComparerDB.has(word, con[key]['title'], case, reg)), 
                        resAppender= lambda i, key, con: key ),
                   callBackFunc=lambda key, con: print(con[key], key),
                   toolTipFunc= lambda key, con: con[key]['title'])
        return en
    
    def delete(self, elementKey):
        self._dataCrud.delete(elementKey)