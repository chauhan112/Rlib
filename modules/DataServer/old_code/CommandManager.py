from modules.DataServer.Interfaces import GNode

class IManager:
    def manage(self):
        pass

class GServer(GNode):
    def __init__(self, info:IContact, cmdManher: IManager, portal:IPortal, updateTimeInterval =1 ):
        super().__init__(updateTimeInterval)
        self.commandManager = cmdManher
        self.contactID = info
        self.portal = portal
    
    def run(self):
        pass
        
class ICommand:
    def setData(self, data):
        self.data = data
    def execute(self):
        raise NotImplementedError("abstract method")

class Copy2ClipBoard(ICommand):
    def execute(self):
        assert type(self.data[0]) == str
        from ClipboardDB import ClipboardDB
        ClipboardDB.copy2clipboard(self.data[0])

commandList = [Copy2ClipBoard()]

class CommandManager:
    def register(self, command: ICommand):
        commandList.append(command)
    def parseMsg(self, msg):
        msgLines = msg.strip().splitlines()
        res = []
        for line in msgLines:
            cmdAndParams = line.split(",")
            cmd = commandList[int(cmdAndParams[0])]
            cmd.setData(cmdAndParams[1:])
            res.append(cmd)
        return res
    def funcExplorer(self):
        for i, cmd in enumerate(commandList):
            print(f"{i}. {cmd.__class__}")
