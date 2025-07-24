from modules.mobileCode.CmdCommand import GCommand, GController, CmdCommandHandler, \
    DisplayElements, GModalSetable,IReturnable, GDataSetable, GParentable, IRunnable
import os
from modules.Explorer.model import OSFileExplorer, DictionaryExplorer
from enum import Enum
SelectionType = Enum("SelectionType","File Folder Both")
class ISelector:
    def isCancelled(self):
        raise NotImplementedError("abstract method")
    def getSelected(self):
        raise NotImplementedError("abstract method")
class IPathSelector:
    def isCancelled(self):
        raise NotImplementedError("abstract method")
    def getPath(self):
        raise NotImplementedError("abstract method")
class IChangeableList(IReturnable):
    def cd(self, val):
        raise NotImplementedError("abstract method")
    def curPath(self):
        raise NotImplementedError("abstract method")
    def curVal(self, val):
        raise NotImplementedError("abstract method")
class IPathOps:
    def prefixDir(self, val):
        raise NotImplementedError("abstract method")
    def unprefixDir(self,val):
        raise NotImplementedError("abstract method")
    def isPathDir(self, path):
        raise NotImplementedError("abstract method")
    def dirname(self, path):
        raise NotImplementedError("abstract method")
    def join(self, *args):
        raise NotImplementedError("abstract method")
    def isdir(self, val):
        raise NotImplementedError("abstract method")
class GPathOps(IPathOps):
    def __init__(self):
        self.tee =  '├── '
    def prefixDir(self, val):
        return self.tee + val
    def unprefixDir(self, val):
        return val.replace(self.tee, "")
    def isdir(self, val):
        return self.tee in val
class DicPathOps(GPathOps):
    def join(self, *args):
        return "/".join(args)
    def dirname(self, path):
        patList = path.split("/")
        if len(patList) != 0:
            patList.pop()
        return self.join(*patList)
class OSPathOps(GPathOps):
    def isPathDir(self, path):
        return os.path.isdir(path)
    def dirname(self, path):
        return os.path.dirname(path)
    def join(self, *args):
        return os.sep.join(args)
class OSChangeableList(OSPathOps,GParentable, IChangeableList):
    def __init__(self, iniPath='.'):
        super().__init__()
        self.exp = None
        self.setData(iniPath)
    def setData(self, path):
        self.exp = OSFileExplorer(path)
    def cd(self, val):
        self.exp.cd(val)
    def curPath(self):
        return self.exp.path
    def get(self):
        if self.exp is None:
            self.setData(self.parent.container)
        folders, files= self.exp.dirList()
        return [self.prefixDir(ele) for ele in folders] + files
    def curVal(self, val):
        return val
class DicChangeableList(IChangeableList,GParentable,DicPathOps):
    def __init__(self):
        self.exp = None
        super().__init__()
    def setData(self, dic):
        self.exp = DictionaryExplorer(dic)
    def cd(self, val):
        self.exp.cd(val)
    def curPath(self):
        return self.join(*self.exp.currentPath)
    def get(self):
        if self.exp is None:
            self.setData(self.parent.container)
        folders, files= self.exp.keys()
        return [self.prefixDir(ele) for ele in ['..'] +folders] + files
    def isPathDir(self, path):
        from useful.ListDB import ListDB
        path = path.strip("/")
        pos = path.split("/")
        try:
            content = ListDB.dicOps().get(self.exp.content, pos)
            return type(content) == dict
        except:
            return False
    def curVal(self, val):
        from useful.ListDB import ListDB
        pos = self.exp.currentPath
        return ListDB.dicOps().get(self.exp.content, pos + [val])
class GSelector(ISelector, IRunnable):
    def __init__(self, lister: IChangeableList, selector: SelectionType= SelectionType.Both, container=None):
        self.lister = lister
        self.cnt = None
        self.currentPath = ''
        self.selector = selector
        self.container = container
    def run(self):
        self.setController()
        self.cnt.run()
    def getSelected(self):
        return self.currentPath
    def setController(self):
        if self.cnt is None:
            disp = DisplayElements()
            disp._runAfter = True
            self.cnt = GController(self.container,cmdRunner=CmdCommandHandler(callback=self._callback,
                extraCommands=self.extraFuncs()), lister = self.lister, displayer=disp )
    def isCancelled(self):
        lastCmd = self.cnt.cmdRunner._cmdHistory[-1]
        return lastCmd == "q"
    def _callback(self, ele):
        currentVal = ele.getCurrentValue()
        self.currentPath = self.cnt.lister.curPath()
        if self.cnt.lister.isdir(currentVal):
            self.cnt.lister.cd(self.cnt.lister.unprefixDir(currentVal))
            return
        self.setPath(self.cnt.lister.join(self.currentPath , currentVal))
    def setPath(self, path= None):
        if path is None:
            path = self.cnt.lister.curPath()
        self.currentPath = path
        self.cnt.cmdRunner._loopBreaker = True
    def extraFuncs(self):
        curPath = CurPath('curPath')
        func = [Select('p'), curPath]
        [f.setModel(self) for f in func]
        curPath._runAfter = True
        return func
class CurPath(GCommand, GModalSetable):
    def getHelp(self):
        return self.id, 'prints current path'
    def callback(self):
        print(self.model.cnt.lister.curPath())
class Select(GCommand, GModalSetable):
    def getHelp(self):
        return self.id, "select a path"
    def callback(self):
        ty = self.model.selector
        if ty == SelectionType.Both:
            self.model.setPath()
        elif ty == SelectionType.File:
            if not self.model.cnt.lister.isPathDir(self.model.currentPath):
                self.model.setPath()
                return
            print("can only select file")
            input('click to continue: ')
        else:
            if self.model.cnt.lister.isPathDir(self.model.currentPath):
                self.model.setPath()
                return
            self.model.setPath(self.model.dirname(self.model.currentPath))
class FileSelector(GSelector):
    def __init__(self, initialPath='.', filetype= "."):
        super().__init__(OSChangeableList(os.path.abspath(initialPath)), selector = SelectionType.File)
        self.filetype = filetype
    def run(self):
        self.setController()
        self.cnt.elementsDisplayer.resultFilter = self.filterFunction
        self.cnt.run()
    def filterFunction(self, path):
        path = self.lister.unprefixDir(path)
        if path in ['.', '..']:
            return True
        if self.filetype == '.':
            return True
        path = self.lister.join(self.lister.curPath(), path)
        isFolder = self.lister.isPathDir(path)
        return isFolder or path.endswith(self.filetype)