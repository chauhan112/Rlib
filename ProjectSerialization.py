from FileDatabase import File
from SerializationDB import SerializationDB
import os
from LibPath import getPath
from Path import Path

class ProjectSerialization:
    def archive(files, name):
        s = _Serialize(files, name)
        s.archive()
    
    def unarchive(name):
        pklFile = os.sep.join([resourcePath(), "project", name])
        k = SerializationDB.readPickle(pklFile)
        k.restore()
    
class _Serialize:
    def __init__(self, files, name ):
        self.content = {}
        self.dirStrucuture = set([])
        self.name = name
        self.descriptions = ""
        self._preprocess(files)
        
    def _preprocess(self, files):
        commonDir = _Serialize._commonDir(files)
        for f in files:
            base = os.path.dirname(f).replace(commonDir, "").strip(os.sep)
            self.content[Path.joinPath(base,os.path.basename(f))] = File.getFileContent(f)
            self.dirStrucuture.add(base)
    
    def _commonDir(files):
        dirExp = None
        while True:
            every = True
            for file in files:
                if(dirExp is None):
                    dirExp = os.path.dirname(file)
                if(dirExp !=  file[:len(dirExp)] ):
                    every = False
                    break
            if(every):
                return dirExp
            else: 
                every = True
                dirExp = os.path.dirname(dirExp)
        return dirExp
    
    def restore(self, name = ""):
        if(name == ""):
            name = self.name
        try:
            os.mkdir(name)
        except:
            pass
        
        for d in self.dirStrucuture:
            try:
                os.makedirs(Path.joinPath(self.name, d))
            except:
                pass
            
        for f in self.content:
            File.createFile(Path.joinPath(name, f), self.content[f])
    
    def archive(self):
        outFile = os.sep.join([resourcePath(), "project", self.name + ".pkl"])
        if(os.path.exists(outFile)):
            print("project name already exists")
            return
        SerializationDB.pickleOut(self, outFile)

    def readPklFile(pklFile):
        pklFile = os.sep.join([resourcePath(), "project", pklFile])
        k = SerializationDB.readPickle(pklFile)
        k.restore()
