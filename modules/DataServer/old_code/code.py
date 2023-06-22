from modules.DataServer.Interfaces import INode, IGitManager, GNode
from GitDB import IGitCommand, CommandLinePush, GitPull, GitPush
from modules.DataServer.Server import CommandManager
from modules.DataServer.Commands import ICommand

class GitManager(IGitManager):
    def __init__(self, username, password, path2repo, pushCommand:IGitCommand=None, pullCommand:IGitCommand=None):
        self.path = path2repo
        self.username = username
        self.password = password
        self.pushCommand = pushCommand
        self.pullCommand = pullCommand
        if(self.pushCommand is None):
            self.pushCommand = GitPush(CommandLinePush(self.username, self.password, self.path))
        if(self.pullCommand is None):
            self.pullCommand = GitPull(self.path, self.username)
    def push(self):
        self.pushCommand.act()
    def pull(self):
        self.pullCommand.act()
    def getPath(self):
        return self.path
        
class GitServer(GNode):
    def __init__(self, localPath,portal:GitPortal, serverInfo:GitContact= GitContact('server'), updateTime=1):
        super().__init__(updateTime)
        self.path = localPath
        self.contactID = serverInfo 
        self.portal = portal
        self.commandManager = CommandManager()
        print(f"thread started. Updating every {updateTime} second")
    def run(self):
        print("running")
        msg = self.portal.receiveMessage(self.contactID)
        print(msg)
        if(msg == {}):
            return
        
        dataWithInfo = msg['dataWithClientInfo']
        fromContact = dataWithInfo['from']
        data = dataWithInfo['data']
        commands = self.commandManager.getCommand(data)
        res = ""
        for cmd in commands:
            try:
                res += cmd.run() + "\n" + "-"*20 + "\n"
            except:
                return res
        self.portal.sendMessage({'from': self.contactID.getId(), 'result': res, 'time': Tools.detailedTimeStamp()}, fromContact)
        print(res)

class GitClient(INode):
    def __init__(self, portal:IPortal, contactInfo: GitContact=GitContact("testSub")):
        self.contactId = contactInfo
        self.portal = portal

    def run(self, command:ICommand):
        res =command.run()
        return res

    def sendCommand(self, command: ICommand):
        server = GitContact("server")
        data = command.serialize()
        self.portal.sendMessage({'from': self.contactId.getId(),'data': data}, server)
        
class TreeStructure(IDetectorStructure):
    def __init__(self, parent_folder, uuid):
        self.dic = {parent_folder:{'is_dir': True, 'changed_id': uuid, 'content': {}}}
        self._parent = parent_folder

    def add(self, path, uuid, is_dir = False):
        rel_location = os.path.dirname(path).split(os.sep)
        basename = os.path.basename(path)
        val = self.dic
        for folder in rel_location:
            val[folder]['changed_id'] = uuid
            val = val[folder]['content']
        val.update({basename: {'is_dir': is_dir, 'changed_id': uuid, 'content': {}}})

    def get_changes(self, last_uuid):
        return self._get_changed(self.dic, last_uuid)

    def _get_changed(self, content, uuid,loc=[], res= []):
        for val in content:
            if val['changed_id'] != uuid:
                if not val['is_dir']:
                    res.append('/'.join(loc+[val]))
                else:
                    res = self._get_changed(content[val], uuid, loc+ [val], res)
        return res

    def is_changed(self, uuid, loc=[]):
        if len(loc) == 0:
            loc = [self._parent]
        data = self.dic
        for folder in loc:
            data = data[folder]['content']
        return data['changed_id'] != uuid

    def get_deleted(self, uuid, parent):
        pass

class TreeStructureTest:
    def update_test():
        stru = TreeStructure('alla', 'sdjfjhisdhc')

class DeletionMananger(IDeleteManager):
    def __init__(self):
        self.mail_box = {}
    def addNode(self, node_id):
        self.mail_box[node_id] = []
    def deleteNode(self, node_id):
        del self.mail_box[node_id]
    def notifyNodes(self, info):
        for no in self.mail_box:
            self.mail_box[no].append(info)
    def getAllNotificationForNode(self, node_id):
        return self.mail_box[node_id]
    def deleteAllMailsForNode(self, node_id):
        self.mail_box[node_id].clear()


class IDetectorStructure:
    def add(self, path, uuid, is_dir = False):
        raise NotImplementedError("abstract method")
    def get_changes(self, last_uuid):
        raise NotImplementedError("abstract method")

class IDeleteManager:
    def addNode(self, node_id):
        raise NotImplementedError("abstract method")
    def deleteNode(self, node_id):
        raise NotImplementedError("abstract method")
    def notifyNodes(self, info):
        raise NotImplementedError("abstract method")
    def getAllNotificationForNode(self, node_id):
        raise NotImplementedError("abstract method")

class IFileFolderOps(IOps):
    pass

class RenameOps(IFileFolderOps, GDataSetable):
    def execute(self):
        from FileDatabase import File
        old, new = self.data
        File.rename(old, new)

class DeleteOps(IFileFolderOps,GDataSetable):
    def execute(self):
        path = self.data
        os.system(f'rm -rf {path}')

class ReplaceOps(IFileFolderOps, GDataSetable):
    def execute(self):
        oldpath, form_path = self.data
        os.system(f'mv -f "{form_path}" "{oldpath}"')
