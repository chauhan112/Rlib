class IContact:
    def getId(self):
        raise NotImplementedError("abstract method")

class NameContact(IContact):
    def __init__(self, name):
        self._name = name
    def getId(self):
        return self._name

class INode:
    def run(self): # run at specific interval continuously
        raise NotImplementedError("abstract method")
    def start(self):
        raise NotImplementedError("abstract method")
    def stop(self):
        raise NotImplementedError("abstract method")

class GNode(INode):
    def __init__(self, updateInterval):
        from TimeDB import TimeDB
        self.timer = TimeDB.setTimer().regularlyUpdateTime(updateInterval, self.run)

class IMessage:
    def get(self):
        raise NotImplementedError("abstract method")

class IMessageWriter:
    def write(self, to:IContact):
        raise NotImplementedError("abstract method")

class IMessageReader:
    def read(self, fromC: IContact,clean = True):
        raise NotImplementedError("abstract method")

class IPortal:
    def sendMessage(self, data, to: IContact):
        raise NotImplementedError("abstract method")
    def receiveMessage(self, fromC: IContact, clean = True):
        raise NotImplementedError("abstract method")
    def getPath(self):
        raise NotImplementedError("abstract method")

class IFilePortal:
    def sendFile(self, filepath, to:IContact, loc = ".", target_name = ""):
        raise NotImplementedError("abstract method")
    def receiveFile(self, fromC: IContact):
        raise NotImplementedError("abstract method")
    def download(self, files, local_toP_path):
        raise NotImplementedError("abstract method")
    def deleteFiles(self, files):
        raise NotImplementedError("abstract method")

class GPortal(IPortal):
    def getPath(self, *toArr):
        import os
        path = self.path
        for to in toArr:
            if type(to) == str:
                path += os.sep + to
            elif isinstance(to, IContact):
                path += os.sep + to.getId()
        return path

class IGitManager:
    def push(self):
        raise NotImplementedError("abstract method")
    def pull(self):
        raise NotImplementedError("abstract method")
    def getPath(self):
        raise NotImplementedError("abstract method")