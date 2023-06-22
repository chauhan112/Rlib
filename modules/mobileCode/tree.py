from OpsDB import IOps
from modules.mobileCode.CmdCommand import GCommand, IDisplayElements, ICommand, \
    ResultFilter, Search, DicList
from modules.Explorer.model import DictionaryExplorer
from treelib import Tree, Node
from ListDB import ListDB
class DisplayTree(IOps):
    def __init__(self, dic, parent='root'):
        self.data = dic
        self.tree = Tree()
        n = Node(parent)
        self.tree.add_node(n)
        self.makeTree(self.data, n.identifier)
    def makeTree(self, data, parent):
        if (type(data) == dict):
            for key in data:
                n = Node(key)
                self.tree.add_node(n, parent)
                self.makeTree(data[key], n.identifier)
        elif (type(data) == list):
            for val in data:
                self.makeTree(val, parent)
        else:
            dval = str(data)
            n = Node(dval)
            self.tree.add_node(n, parent)
    def execute(self):
        self.tree.show()
class MyOwnMadeTree(IOps):
    def __init__(self, dic, parent='root'):
        self.data = dic
        print(parent)
        self.arrowLine = "└──"
    def execute(self):
        self.displayData(self.data)
    def displayData(self, data, nSpaces = 0):
        if (type(data) == dict):
            for key in data:
                self.displayElement(self.arrowLine + " "+ key, nSpaces)
                self.displayData(data[key] , nSpaces+1)
        elif (type(data) == list):
            for val in data:
                self.displayData(val, nSpaces +1)
        else:
            self.displayElement(self.arrowLine + " "+data, nSpaces)
    def displayElement(self, val, fac, end ="\n"):
        nSpaces = fac * (len(self.arrowLine) + 1)
        print(" "*nSpaces+  val, end=end )
class ITreeable:
    def iterdir(self):
        pass
    def is_dir(self):
        pass
class DicTree(ITreeable):
    def __init__(self, dic, name ="root"):
        self.dic = dic
        self.name = str(name)
    def iterdir(self):
        ele = []
        if type(self.dic) == dict:
            for key in self.dic:
                if type(self.dic[key]) in [list, dict]:
                    ele.append(DicTree(self.dic[key], key))
                else:
                    ele.append(DicTree(key, key))
        elif type(self.dic) == list:
            for val in self.dic:
                ele.append(DicTree(val, val))
        return ele
    def is_dir(self):
        return type(self.dic) in [list, dict]
class TreeFromStackOverflow(IOps):
    def __init__(self, dic, parent="root"):
        self.parent = parent
        self.data = dic
        self.tree = self.getTree(DicTree(self.data))
    def execute(self):
        print(self.parent)
        for val in self.tree:
            print(val)
    def getTree(self, dic):
        space =  '    '
        branch = '│   '
        # pointers:
        tee =    '├── '
        last =   '└── '
        def tree(dir_path: ITreeable, prefix: str=''):
            """A recursive generator, given a directory Path object
            will yield a visual tree structure line by line
            with each line prefixed by the same characters
            """
            contents = list(dir_path.iterdir())
            # contents each get pointers that are ├── with a final └── :
            pointers = [tee] * (len(contents) - 1) + [last]
            for pointer, path in zip(pointers, contents):
                yield prefix + pointer + path.name
                if path.is_dir(): # extend the prefix and recurse:
                    extension = branch if pointer == tee else space
                    # i.e. space because last, └── , above so no more |
                    yield from tree(path, prefix=prefix+extension)
        return tree(dic)
class LayerDicList(DicList):
    def __init__(self, layer):
        self._layer_nr = layer
        self.dicExp = None
    def get(self):
        content = self.getCurrentValue()
        return self.getLayer(content, self._layer_nr)
    def getLayer(self, dic, layer=1):
        if type(dic) == dict:
            newDic = {}
            for key in dic:
                if layer > 0:
                    newDic[key] = self.getLayer(dic[key], layer - 1)
            return newDic
        return dic
class LayerDicListWithDepthInfo(LayerDicList):
    def getLayer(self, dic, layer=1):
        if type(dic) == dict:
            newDic = {}
            for key in dic:
                if layer > 0:
                    dpt = ListDB.dicOps().depth_calculator(dic[key])
                    newDic[(key, dpt)] = self.getLayer(dic[key], layer - 1)
            return newDic
        return dic
class LayeredDisplayElements(IDisplayElements, GCommand):
    def __init__(self,idd="l", resultMapper=lambda x: x,resultFilter =lambda x: True ):
        super().__init__(idd)
        self.resultMapper = resultMapper
        self._lastPos = []
        self._cmds = []
        self.filteredResult = None
        self.resultFilter = resultFilter
        self.mainResult = None
        self.setCommand(Search('s'))
    def callback(self):
        self.setFilteredResult()
        curVal = 'root'
        lastPos = self.parent.elementsDisplayer._lastPos
        if lastPos != []:
            curVal = lastPos[-1]
        print(f"t:{len(self.mainResult)} n:{len(self.filteredResult)}")
        TreeFromStackOverflow(self.filteredResult, curVal).execute()
    def setFilteredResult(self):
        elements = self.parent.lister.get()
        if self.filteredResult is None or self.mainResult != elements:
            fil = ResultFilter()
            fil.setData((elements, self.resultMapper, self.resultFilter))
            rs = fil.execute()
            self.filteredResult = {val:elements[val] for _,val in rs}
        self.mainResult = elements
    def getDisplayerCommands(self):
        return self._cmds
    def getHelp(self):
        return self.id, 'display tree view'
    def setCommand(self,cmd:ICommand):
        cmd.setParent(self)
        self._cmds.append(cmd)
class LayerDisplayerWithDepth(LayeredDisplayElements):
    def setFilteredResult(self):
        elements = self.parent.lister.get() # results from class LayerDicListWithDepthInfo
        if self.filteredResult is None or self.mainResult != elements:
            fil = ResultFilter()
            fil.setData((elements, self.resultMapper, self.resultFilter))
            rs = fil.execute()
            self.filteredResult = {f'{val[0]}:{val[1]}':elements[val[0]] for _,val in rs}
        self.mainResult = elements
class Goback(GCommand):
    def callback(self):
        self.parent.parent.lister.dicExp.goBack()
        lastPos = self.parent.parent.elementsDisplayer._lastPos
        if len(lastPos) != 0:
            lastPos.pop()
    def getHelp(self):
        return self.id, 'go back'