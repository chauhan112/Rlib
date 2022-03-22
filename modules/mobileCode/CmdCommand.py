from modules.Explorer.model import OSFileExplorer, DictionaryExplorer
from OpsDB import IOps
class IRunnable:
    def run(self):
        raise NotImplementedError("abstract method")
class IParentable:
    def setParent(self, parent):
        raise NotImplementedError("abstract method")
class IDataSetable:
    def setData(self, data):
        raise NotImplementedError("abstract method")
class ICommand:
    def check(self, cmd:str):
        raise NotImplementedError("abstract method")
    def callback(self):
        raise NotImplementedError("abstract method")
    def getHelp(self):
        raise NotImplementedError("abstract method")
    def runAfterCallback(self):
        raise NotImplementedError("abstract method")
class IListOps:
    def getCurrentPath(self):
        raise NotImplementedError("abstract method")
    def getCurrentValue(self):
        raise NotImplementedError("abstract method")
class IListChangingOps:
    def delete(self, val):
        raise NotImplementedError("abstract method")
    def add(self, key, val, overwrite =False):
        raise NotImplementedError("abstract method")
class IReturnable:
    def get(self):
        raise NotImplementedError("abstract method")
class IDisplayElements:
    def getDisplayerCommands(self):
        raise NotImplementedError("abstract method")
class IModalSetable:
    def setModel(self, model):
        raise NotImplementedError('abstract method')
class GParentable(IParentable):
    def setParent(self, parent):
        self.parent = parent
class GDataSetable(IDataSetable):
    def setData(self,data):
        self.data = data
class GCommand(ICommand, GParentable, GDataSetable):
    def __init__(self, idd):
        self.id = idd
        self._runAfter = False

    def check(self, cmd:str):
        return cmd.strip()==self.id

    def identifier(self):
        return self.id

    def runAfterCallback(self):
        return self._runAfter
class GModalSetable(IModalSetable):
    def setModel(self, model):
        self.model = model
class NormalList(IReturnable, GDataSetable, GParentable):
    def get(self):
        return self.parent.container
class OSExpList(IReturnable, GDataSetable, GParentable,IListOps):
    def __init__(self):
        self.exp = None
    def get(self):
        if self.exp is None:
            self.setData(self.parent.container)
        from ListDB import ListDB
        return ListDB.flatten(self.exp.dirList())
    def setData(self, path):
        self.exp = OSFileExplorer(path)
    def getCurrentPath(self):
        return self.exp.path
    def getCurrentValue(self):
        return self.exp.dirList()
class DicList(IReturnable, GDataSetable, GParentable, IListOps):
    def __init__(self):
        self.dicExp = None
    def get(self):
        self._setValue()
        from ListDB import ListDB
        return ['..'] + ListDB.flatten(self.dicExp.keys())
    def setData(self, dic):
        self.dicExp = DictionaryExplorer(dic)
    def getCurrentPath(self):
        self._setValue()
        return self.dicExp.currentPath
    def _setValue(self):
        if self.dicExp is None:
            self.setData(self.parent.container)
    def getCurrentValue(self):
        self._setValue()
        return self.dicExp.getCurrentValue()
class Exit(GCommand):
    def callback(self):
        self.parent._loopBreaker = True
    def getHelp(self):
        return self.id, 'quit'
class ClearScreen(GCommand):
    def callback(self):
        import os
        os.system('clear')
    def getHelp(self):
        return self.id, 'clear'
class Help(GCommand):
    def __init__(self):
        super().__init__('h')
    def callback(self):
        for cmd in self.parent.cmds:
            key, info = cmd.getHelp()
            if 'k' not in self.data:
                print(f"{key}. {info}")
            else:
                print(key, end=", ")
        print()
    def getHelp(self):
        return self.id, 'help > h k, h'
class ResultFilter(IOps, GDataSetable):
    def execute(self):
        lists, mapper, filterer = self.data
        res = []
        for i, val in enumerate(lists):
            disp = mapper(val)
            if filterer(disp):
                res.append((i, disp))
        return res
class DisplayElements(IDisplayElements, GCommand):
    def __init__(self, idd='l', resMapper = lambda x: x, resultFilter =lambda x: True ):
        super().__init__(idd)
        self.resultMapper = resMapper
        self.from1 = 0
        self.untill = 20
        self.resultFilter = resultFilter
        self.filteredResult = None
        self.mainResult = None

    def callback(self):
        elements = self.parent.lister.get()
        self.setFilteredElements(elements)
        if len(self.filteredResult) < self.from1:
            self.from1 = 0
            self.untill = 20
        print(f"t: {len(self.filteredResult)} n: {self.untill-self.from1} {self.from1}:{self.untill}")
        for i, shown in self.filteredResult[self.from1:self.untill]:
            print(f'{i}. {shown}')

    def getHelp(self):
        return self.id, 'list operations'

    def setFilteredElements(self, elements):
        fil = ResultFilter()
        fil.setData((elements, self.resultMapper, self.resultFilter))
        self.filteredResult = fil.execute()

    def getDisplayerCommands(self):
        cmds = [RangeSelected('r'),Search('s'), NextSection('n')]
        [r.setParent(self) for r in cmds]
        return cmds
class RangeSelected(GCommand):
    def callback(self):
        try:
            f1 = int(input('from: '))
            f2 = int(input('till: '))
            self.parent.from1 = f1
            self.parent.untill = f2
        except:
            pass
    def getHelp(self):
        return self.id, 'range select'
class ElementSelected(GCommand):
    def __init__(self,callback_):
        self.val = None
        self._callback= callback_
        super().__init__('')


    def check(self, cmd):
        try:
            self.val = int(cmd)
            return True
        except:
            return False
    def callback(self):
        self._callback(self)

    def getCurrentValue(self):
        content = self.parent.parent.lister.get()
        if type(content) == list:
            return content[self.val]
        elif type(content) == dict:
            return list(content.keys())[self.val]
        return None
    def getHelp(self):
        return 'intval', 'select element and run callback'
class Search(GCommand):
    def callback(self):
        filterWord = input("word: ")
        self.parent.resultFilter = lambda val: filterWord in val
        self.parent.filteredResult = None

    def getHelp(self):
        return self.id, 'filter result'
class NextSection(GCommand):
    def __init__(self, idd):
        self.delta = 20
        super().__init__(idd)
    def getHelp(self):
        return self.id, 'get next n list; n, n p, n d 10'

    def callback(self):
        if 'p' in self.data:
            self.parent.untill = self.parent.from1
            self.parent.from1 -= self.delta
        elif 'd' in self.data:
            self.delta = int(self.data[-1])
            self.parent.untill = self.parent.from1 + self.delta
        else:
            self.parent.from1 = self.parent.untill
            self.parent.untill += self.delta
        self.parent.parent.cmdRunner.runcmd("c")
        self.parent.callback()
class CmdCommandHandler(IRunnable, GParentable):
    def __init__(self, preCmds = None, extraCommands = None,promptText = 'enter cmd: ', callback = lambda x: x):
        if extraCommands is None:
            extraCommands = []
        if preCmds is None:
            preCmds = ['l']
        self._extraCommands = extraCommands
        self._preCmds = preCmds
        self._loopBreaker = False
        self.promptText = promptText
        self._cmdHistory = []
        self.elementSelected = ElementSelected(callback)
        self._prepareCommands()

    def _prepareCommands(self):
        self.cmds = [Exit('q'), ClearScreen('c'),Help(), self.elementSelected] + self._extraCommands
        for cmd in self.cmds:
            cmd.setParent(self)

    def run(self):
        if self.parent.elementsDisplayer not in self.cmds:
            self.cmds += self.parent.elementsDisplayer.getDisplayerCommands() + [self.parent.elementsDisplayer]
        for cmd in self._preCmds:
            self.runcmd(cmd)
        while True:
            inp = input(self.promptText)
            self.runcmd(inp)
            if self._loopBreaker:
                break
            self.runAfterCallback()

    def runAfterCallback(self):
        for cmd in self.cmds:
            if cmd.runAfterCallback():
                cmd.callback()

    def runcmd(self, inp):
        if(inp == ""):
            return
        self._cmdHistory.append(inp)
        inpList = inp.split()
        inp = inpList[0]
        params = inpList[1:]
        for cmd in self.cmds:
            if(cmd.check(inp)):
                cmd.setData(params)
                cmd.callback()
                break
class GController(IRunnable):
    def __init__(self,container = None, lister:IReturnable = None, displayer: IDisplayElements = None,
                 cmdRunner:IRunnable= None):
        if container is None:
            container = []
        if lister is None:
            lister = NormalList()
        if displayer is None:
            displayer = DisplayElements('l')
        if cmdRunner is None:
            cmdRunner = CmdCommandHandler()
        self.container = container
        self.setLister(lister)
        self.setDisplayer(displayer)
        self.cmdRunner = cmdRunner
        self.cmdRunner.setParent(self)

    def setDisplayer(self, displayElement:IDisplayElements):
        self.elementsDisplayer = displayElement
        self.elementsDisplayer.setParent(self)

    def setLister(self, lister: IReturnable):
        self.lister = lister
        self.lister.setParent(self)

    def setContainer(self, container):
        self.container = container

    def run(self):
        self.cmdRunner.run()
