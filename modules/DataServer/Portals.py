from modules.DataServer.Interfaces import IPortal, IFilePortal, IMessage, GPortal, \
    IContact, IMessageReader, IMessageWriter
from modules.mobileCode.CmdCommand import GDataSetable
import os
from modules.DataServer.Tools import Tools

class TelegramPortal(IPortal):
    def __init__(self, account):
        self.account = account
    def sendMessage(self, data, to: IContact):
        pass
    def receiveMessage(self, fromC):
        pass

class GoogleDrivePortal(IPortal):
    def __init__(self, account):
        self.account = account
    def sendMessage(self, data, to: IContact):
        pass
    def receiveMessage(self, fromC):
        pass

class PathPortal(GPortal, IFilePortal):
    def __init__(self, repoPath):
        # for different user it must be same path
        self.path = repoPath
        if not os.path.exists(self.path):
            os.makedirs(self.path)
    def sendMessage(self, data, to: IContact):
        msg = NewMessage()
        msg.setData(data)
        writer = GMessageWriter(self)
        writer.setData(msg)
        writer.write(to)

    def receiveMessage(self, fromC: IContact, clean= True):
        reader = GMessageReader(self)
        return reader.read(fromC, clean)

class NewMessage(IMessage, GDataSetable):
    def get(self):
        dataWithInfo = {Tools.detailedTimeStamp(): self.data}
        return dataWithInfo

class GMessageReader(IMessageReader):
    def __init__(self, portal:IPortal):
        self.portal = portal

    def read(self, fromC: IContact, clean):
        froPath = self.portal.getPath(fromC)
        if not os.path.exists(froPath):
            return []
        from useful.SerializationDB import SerializationDB
        msgPath = self.portal.getPath(fromC, 'msg.pkl')
        msg = []
        if os.path.exists(msgPath):
            msg = SerializationDB.readPickle(msgPath)
        if clean:
            SerializationDB.pickleOut([], msgPath)
        return msg

class GMessageWriter(IMessageWriter, GDataSetable):
    def __init__(self, portal:IPortal):
        self.portal = portal

    def write(self, to:IContact):
        message = self.data.get()
        topath = self.portal.getPath(to)
        if not os.path.exists(topath):
            os.makedirs(topath)
        from useful.SerializationDB import SerializationDB
        msgPath = self.portal.getPath(to, 'msg.pkl')
        msg = []
        if os.path.exists(msgPath):
            msg = SerializationDB.readPickle(msgPath)
        msg.append(message)
        SerializationDB.pickleOut(msg, msgPath)