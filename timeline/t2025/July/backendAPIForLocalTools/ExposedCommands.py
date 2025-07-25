from basic import Main as ObjMaker
from modules.Explorer.model import OSFileExplorer
from ....t2024.tools import ConversionTool, FileTools
from useful.FileDatabase import File
from useful.Path import Path

def FolderCommand():
    exp = OSFileExplorer()
    def dirList(path):
        exp.set_path(path)
        folders, files = exp.dirList()

        return {
            "folders": folders,
            "files": files
            }
    def curDir():
        return exp.path
    s = ObjMaker.variablesAndFunction(locals())
    return s.handlers

def FilesInfo():
    def pyLibSize():
        return "2kb"
    def jsLibSize():
        return "500kb"
    def totalSize():
        return "2mb"
    s = ObjMaker.variablesAndFunction(locals())
    return s.handlers

def Controller():
    def commandPipeline(cmds: list):
        def run(cmd, params=None):
            if params is not None:
                return s.handlers.runCommand(cmd, params)
            elif isinstance(cmd, str):
                return s.handlers.runCommand(cmd,)
            return s.handlers.runCommand(cmd[0],  *cmd[1:])
        res = None
        for cmd in cmds:
            res = run(cmd, res)
        return res

    commands = {
        "folder": FolderCommand(),
        "filesInfo": FilesInfo(),
        "pipe": commandPipeline,
        "convert": ConversionTool(),
        "useful":{
            "file": File,
            "path": Path
        },
        "tools":{
            "fileTools": FileTools().handlers
        }
    }
    def get_command(cmd):
        cmdsp = cmd.strip().strip("/")
        if cmdsp == "":
            return None
        if cmdsp in commands:
            return commands[cmdsp]
        cmdsp = cmd.split("/")
        resCommand = s.process.commands
        for c in cmdsp:
            if isinstance(resCommand, dict) and c in resCommand:
                resCommand = resCommand[c]
            elif hasattr(resCommand, c):
                resCommand = getattr(resCommand, c)
            else:
                return None
        return resCommand
            
    def runCommand(cmd, *args):
        cmdF = s.handlers.get_command(cmd)
        return cmdF(*args)

    s = ObjMaker.variablesAndFunction(locals())
    return s
