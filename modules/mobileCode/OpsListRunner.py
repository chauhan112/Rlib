from modules.mobileCode.CmdCommand import IRunnable, IReturnable, GDataSetable, GModalSetable
from modules.mobileCode.CmdCommand import GController, DicList, DisplayElements,CmdCommandHandler
from modules.mobileCode.SelectPath import GSelector, DicChangeableList
class IExplorer:
    def cd(self, val):
        raise NotImplementedError('abstract method')
    def dirList(self):
        raise NotImplementedError('abstract method')
    def curPath(self):
        raise NotImplementedError('abstract method')
    def getVal(self, key):
        raise NotImplementedError('abstract method')
    def goback(self):
        raise NotImplementedError('abstract method')
    def getCurrentValue(self):
        raise NotImplementedError('abstract method')
class DicListExplorer(IExplorer):
    def __init__(self, dic):
        self.content = dic
        self._curpath = []
        self._tillNowVal = self.content
    def cd(self, key):
        if type(key) == str and key.strip() == "..":
            return self.goback()
        if type(self._tillNowVal) in [dict, list]:
            self._tillNowVal = self._tillNowVal[key]
            self._curpath.append(key)
        else:
            raise IOError(f"Cannot change to {key}")
    def dirList(self):
        folders = []
        files   = []
        if type(self._tillNowVal) == dict:
            for key in self._tillNowVal:
                if type(self._tillNowVal[key]) in [dict, list]:
                    folders.append(key)
                else:
                    files.append(key)
        elif type(self._tillNowVal) == list:
            for i, val in enumerate(self._tillNowVal):
                files.append((i, val))
        return folders, files
    def curPath (self):
        return self._curpath
    def getVal(self, key):
        return self._tillNowVal[key]
    def getCurrentValue(self):
        temp = self.content
        for val in self._curpath:
            temp = self.content[val]
        return temp
    def goback(self):
        if len(self._curpath) > 0:
            self._curpath.pop()
        self._tillNowVal = self.getCurrentValue()
class GRunable(IRunnable, GDataSetable):
    def __init__(self, func, data = None):
        self.func = func
        self.setData(data)
    def run(self):
        if(self.data is None):
          self.func()
        else:
          self.func(self.data)
class GRunnerWithParent(GRunable):
    def run(self):
        if(self.data is None):
          self.func(self)
        else:
          self.func(self,self.data)
class GRunnerWithModel(IRunnable, GDataSetable, GModalSetable, IReturnable):
    def __init__(self, func, data = None):
        self.func = func
        self.setData(data)
        self._res = None
    def get(self):
        return self._res
    def run(self):
        if self.data is None:
            self._res = self.func(self.model)
        else:
            self._res = self.func(self.model, self.data)
class GitPushSync(IRunnable):
    def __init__(self, path):
        self.path = path
    def run(self):
        from ancient.GitDB import CommandLinePush
        from SerializationDB import SerializationDB
        from LibsDB import LibsDB
        content= SerializationDB.readPickle(LibsDB.picklePath("crypts"))
        usr, pss = content['git user'], content['git token']
        CommandLinePush(usr,pss,self.path).push()
class GitPullSync(IRunnable):
    def __init__(self, path):
        self.path = path
    def run(self):
        from ancient.GitDB import GitPull
        GitPull(self.path, 'chauhan112').act()
class OpsListRunner(IRunnable):
    def __init__(self, opsDic, controller: IRunnable = None):
        if controller is None:
            controller = GController()
        controller.cmdRunner.elementSelected._callback = self.callbackFunc
        controller.elementsDisplayer._runAfter = True
        controller.setContainer(opsDic)
        controller.setLister(DicList())
        self.controller = controller
    def callbackFunc(self, elementSelected):
        cdVal = elementSelected.getCurrentValue()
        exp = elementSelected.parent.parent.lister
        if (cdVal == ".."):
            exp.dicExp.cd("..")
            return
        from ListDB import ListDB
        content = ListDB.dicOps().get(exp.dicExp._content, exp.dicExp.currentPath + [cdVal])
        if (type(content) == dict):
            exp.dicExp.cd(cdVal)
        else:
            content.parent = elementSelected.parent
            content.run()
    def run(self):
        self.controller.run()
class ReturnableOpsRunner(IRunnable, IReturnable):
    def __init__(self, opsDic):
        self.cnt = None
        self.container = opsDic
        self._res = None
    def run(self):
        if self.cnt is None:
            disp = DisplayElements()
            disp._runAfter = True
            self.cnt = GController(self.container,lister=DicChangeableList(), displayer=disp,
                cmdRunner=CmdCommandHandler(callback=self._callback))
        self.cnt.run()
    def _callback(self, ele):
        currentVal = ele.getCurrentValue()
        if self.cnt.lister.isdir(currentVal):
            self.cnt.lister.cd(self.cnt.lister.unprefixDir(currentVal))
            return
        content = self.cnt.lister.curVal(currentVal)
        content.setModel(self)
        content.run()
        self._res = content.get()
    def get(self):
        return self._res
class DicListExplorerAdapter(DicListExplorer):
    def keys(self):
        return self.dirList()
    @property
    def currentPath(self):
        return self.curPath()
class DicListLister(DicChangeableList):
    def setData(self, dic):
        self.exp = DicListExplorerAdapter(dic)
    def mapper(ele):
        if type(ele) == str:
            return ele
        elif type(ele) == tuple:
            return ele[1]
        return ele
    def _callback(ele, func):
        currentVal = ele.getCurrentValue()
        cnt = ele.parent.parent
        if cnt.lister.isdir(currentVal):
            cnt.lister.cd(cnt.lister.unprefixDir(currentVal))
            return
        func(ele)
class ReturnableOpsRunnerWithList(ReturnableOpsRunner):
    def __init__(self, opsDic, callOnLeaveVal):
        self._callOnLeaveVal = callOnLeaveVal
        super().__init__(opsDic)
    def run(self):
        if self.cnt is None:
            disp = DisplayElements(resMapper=DicListLister.mapper)
            disp._runAfter = True
            self.cnt = GController(self.container, lister=DicListLister(), displayer = disp,
                cmdRunner=CmdCommandHandler(callback=self._callback))
        self.cnt.run()
    def _callback(self, ele):
        currentVal = ele.getCurrentValue()
        if self.cnt.lister.isdir(currentVal):
            self.cnt.lister.cd(self.cnt.lister.unprefixDir(currentVal))
            return
        self._res = self._callOnLeaveVal(ele)