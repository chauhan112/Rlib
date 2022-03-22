import os
class IFileManager:
    def getPathTo(self, *folder):
        raise NotImplementedError("abstract method")
    def basePath(self):
        raise NotImplementedError("abstract method")
    def pathExists(self, *folders):
        raise NotImplementedError("abstract method")
    def createPathIfDoesNotExists(self, *folders):
        raise NotImplementedError("abstract method")
        
class FileManager(IFileManager):
    def __init__(self,basePath):
        self.path = basePath
    def getPathTo(self, *folders):
        return os.path.sep.join([self.path] + list(folders))
    def basePath(self):
        return self.path
    def pathExists(self, *folders):
        path = self.getPathTo(*folders)
        return os.path.exists(path)
    def createPathIfDoesNotExists(self, *folders):
        path =[]
        for f in folders:
            path.append(f)
            if(not self.pathExists(*path)):
                os.mkdir(self.getPathTo(*path))