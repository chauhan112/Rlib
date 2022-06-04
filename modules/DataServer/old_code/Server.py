from modules.DataServer.Commands import CopyContentToServerClipboard
class ICommandManager:
    def getCommand(self, msg):
        raise NotImplementedError('abstract method')
    def parseCommand(self, comd):
        raise NotImplementedError('abstract method')

from enum import Enum
commands = Enum('CommandName', "Copy2Clipboard")
class CommandManager(ICommandManager):
    def getCommand(self,msgSerializedCommand):
        res = []
        for comd in msgSerializedCommand:
            res.append(self.parseCommand(comd))
        return res
    def parseCommand(self, comd):
        name = msgSerializedCommand[0]
        if(name == CommandName.Copy2Clipboard.name):
            cmd = CopyContentToServerClipboard(comd[1])
            return cmd