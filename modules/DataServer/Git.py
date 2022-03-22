from modules.DataServer.Interfaces import IContact, GPortal, IGitManager
from modules.DataServer.Tools import Tools
import os
from modules.DataServer.FileManager import FileManager

class GitContact(IContact):
    def __init__(self, name:str = None):
        self._name = name
        if(name is None):
            from uuid import getnode as get_mac
            self._name = str(get_mac())
    def getId(self):
        return self._name

class GitPortal(GPortal):
    def __init__(self, path2repo):
        self.pathManger = FileManager(path2repo)
        self.gitManager = GitSSHManager(path2repo)

    def sendMessage(self, data, to:IContact):
        self.gitManager.pull()
        from SerializationDB import SerializationDB
        self.pathManger.createPathIfDoesNotExists(to.getId())
        dataWithInfo = {Tools.detailedTimeStamp(): data}
        path = self.pathManger.getPathTo(to.getId(), 'msg.pkl')
        oldContent = {}
        if(os.path.exists(path)):
            oldContent = SerializationDB.readPickle(path)
        oldContent.update(dataWithInfo)
        SerializationDB.pickleOut(oldContent, self.pathManger.getPathTo(to.getId(), 'msg.pkl'))
        self.gitManager.push()

    def receiveMessage(self, fromC:IContact):
        self.gitManager.pull()
        from SerializationDB import SerializationDB
        path = self.pathManger.getPathTo(fromC.getId(), 'msg.pkl')
        if(os.path.exists(path)):
            content = SerializationDB.readPickle(path)
            if len(content) != 0:
                SerializationDB.pickleOut({}, path)
                self.gitManager.push()
            return content
        return {}

class GitSSHManager(IGitManager):
    def __init__(self, path2repo):
        self.path = path2repo
    def push(self):
        from GitDB import GitSSHPush
        return GitSSHPush(self.path).push()
    def pull(self):
        from GitDB import GitSSHPull
        return GitSSHPull(self.path).pull()
    def getPath(self):
        return self.path