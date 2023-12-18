from OpsDB import IOps
from modules.mobileCode.CmdCommand import GController, IReturnable, IDisplayElements, \
    GCommand, CmdCommandHandler, GParentable
import os
from SerializationDB import SerializationDB
class IFiller:
    def fill(self):
        pass
class IAnalyser:
    def analyse(self):
        pass
class IDataSetable:
    def setData(self, data):
        raise NotImplementedError("abstract method")
class IFileListGetter:
    def getFiles(self):
        pass
class IExplorer:
    def explore(self):
        pass
class GDataSetable(IDataSetable):
    def setData(self, data):
        self.data = data
class GFiller(IFiller, GDataSetable):
    def __init__(self, fileFunc, folderFunc):
        self.fileFunc = fileFunc
        self.folderFunc = folderFunc
        self._metaStr = 'metaData'
        self._dataStr = 'data'
    def fill(self):
        val = self._fill(self.data)
        self.data[self._metaStr] = val
        return self.data
    def _fill(self, dic, loc=[]):
        if dic[self._dataStr] == {}:
            return self.fileFunc(loc)
        vals = []
        for key in dic[self._dataStr]:
            try:
                val = self._fill(dic[self._dataStr][key], loc + [key])
            except Exception as e:
                val = -1
                print(e)
                print(key + " was not being able to read")
                continue
            dic[self._dataStr][key][self._metaStr] = val
            vals.append(val)
        re = self.folderFunc(vals, loc)
        dic[self._metaStr] = re
        return re
class SizeFiller(GFiller):
    def __init__(self):
        super().__init__(self.getSize, self.folderSize)
    def getSize(self, loc):
        path = os.sep.join(loc)
        return os.stat(path).st_size
    def folderSize(self, arr, loc):
        return sum(arr)
class NumberFiller(GFiller):
    def __init__(self):
        super().__init__(lambda x: 1, lambda arr, loc: sum(arr))
class SortDicWithMeta(IOps, GDataSetable):
    def __init__(self, reverse=False):
        self.reverse = reverse
        self._metaStr = 'metaData'
    def execute(self):
        #dic = self.data['data']
        arr = sorted(dic, key=lambda x: self.data[x][self._metaStr],
                     reverse=self.reverse)
        newDic = {'data': {}}
        newDic['metaData'] = self.data['metaData']
        for k in arr:
            newDic['data'][k] = dic[k].copy()
        return newDic
class MetaTheDictionary(IOps, GDataSetable):
    def execute(self):
        return self.metaDic(self.data)
    def metaDic(self, dic):
        if type(dic) != dict:
            return {'metaData': {}, 'data': dic}
        newDic = {}
        newDic['data'] = dic.copy()
        for key in dic:
            newDic['data'][key] = self.metaDic(dic[key])
        newDic['metaData'] = {}
        return newDic
class FileList2Dic(IOps, GDataSetable):
    def __init__(self, sep=None):
        self.sep = sep
        if sep is None:
            self.sep = os.sep
    def execute(self):
        from ListDB import ListDB
        dic = {}
        for f in self.data:
            ListDB.dicOps().addEvenKeyError(dic, f.split(self.sep), {})
        return dic
class AllFilesReader(IFileListGetter, GDataSetable):
    def __init__(self, path="."):
        self.setData(path)
    def getFiles(self):
        from Path import Path
        return Path.getFiles(self.data, True)
class GFileListGetter(IFileListGetter):
    def __init__(self, files):
        self.files = files
    def getFiles(self):
        return self.files
class FromPickle(IFileListGetter, GDataSetable):
    def getFiles(self):
        return SerializationDB.readPickle(self.data)
class ExecuteDatable(IOps):
    def __init__(self, OpClass, data):
        self.cls = OpClass
        self.data = data
    def execute(self):
        ins = self.cls()
        ins.setData(self.data)
        return ins.execute()
class MetaLister(IReturnable, GParentable,GDataSetable):
    def __init__(self):
        self.pos = []
        self._metaStr = 'metaData'
        self.reverse = False
    def get(self):
        content = self.currentValue()['data']
        arr = sorted(content, key=lambda x: content[x][self._metaStr], reverse = self.reverse)
        vals = [content[ke][self._metaStr] for ke in arr]
        return list(zip(arr, vals))
    def currentValue(self):
        from ListDB import ListDB
        loc = []
        for ke in self.pos:
            loc.append('data')
            loc.append(ke)
        content = ListDB.dicOps().get(self.data, loc)
        return content
class MetaDicValSelected:
    def __init__(self, metaLister):
        self.metaLister = metaLister
    def run(self, ele):
        val = ele.getCurrentValue() [0]
        self.metaLister.pos.append(val)
class DisplayFileAnalyser(IDisplayElements, GCommand):
    def __init__(self, idd="l", infoFunc = lambda x: str(x)):
        super().__init__(idd)
        self.infoFunc = infoFunc
    def callback(self):
        elements = self.parent.lister.get()
        content = self.parent.lister.currentValue()
        tsize = content['metaData']
        for i, (name, si) in enumerate(elements):
            if (os.path.isdir(os.sep.join(self.parent.lister.pos + [name]))):
                self.printFormatted('>', i, name, tsize, si)
            else:
                self.printFormatted('|', i, name, tsize, si)
    def printFormatted(self, pre, i, word, tsize, size):
        if tsize == 0:
            tsize = .0001
        from WordDB import WordDB
        forma = WordDB.formatting()
        print(pre + f'{forma.integer(i,3)}. {forma.word(word, 15)}-' + \
              forma.word("|" * int(20 * size / tsize), 20) + self.infoFunc(size))
    def getDisplayerCommands(self):
        a = [ Goback('b')]
        [i.setParent(self) for i in a]
        return a
    def getHelp(self):
        return self.id, 'display files distribution'
class Goback(GCommand):
    def callback(self):
        if len(self.parent.parent.lister.pos) > 0:
            self.parent.parent.lister.pos.pop()
    def getHelp(self):
        return self.id, 'go back'
class Save(GCommand):
    def callback(self):
        outfileName = input("output: ")
        SerializationDB.pickleOut(self.parent.parent.lister.data, outfileName)
    def getHelp(self):
        return self.id, 'save current content'
class MetaDicExplorer(IExplorer, GDataSetable):
    def __init__(self):
        lsiter = MetaLister()
        disp = DisplayFileAnalyser("l")
        disp._runAfter = True
        self.cnt =GController(cmdRunner = CmdCommandHandler(callback=MetaDicValSelected(lsiter).run,extraCommands  =[Save('s')]),lister=lsiter,
                         displayer= disp)
    def explore(self):
        self.cnt.lister.setData(self.data)
        self.cnt.run()
    def setFunc(self, func = lambda x: str(x)):
        self.cnt.elementsDisplayer.infoFunc = func
#####################################
class FileAnalyser(IAnalyser):
    def __init__(self):
        self.setFileReader(FromPickle())
        self.setFiller(SizeFiller())
        self.setExplorer(MetaDicExplorer())
    def analyse(self):
        files = self.reader.getFiles()
        dic = FileAnalyser.getMetaDicInfo(files, self.filler)
        self.explorer.setData(dic)
        self.explorer.explore()
    def setFileReader(self, reader: IFileListGetter):
        self.reader = reader
    def setFiller(self, filler:IFiller):
        self.filler = filler
    def setPostProcesser(self,pprocess: IOps):
        self.pprocess = pprocess
    def setExplorer(self, exp:IExplorer):
        self.explorer = exp
    def analyseFromFile(pklFile, reverse = True):
        data =SerializationDB.readPickle(pklFile)
        exp = MetaDicExplorer()
        exp.cnt.lister.reverse = reverse
        exp.setData(data)
        exp.explore()
    def sizeb(si):
        p = lambda x: str(round(x,2))
        if si > 1024*1024* 1024:
            return p(si / 1024**3) + " gb"
        elif si > 1024*1024:
            return p(si / (1024*1024)) + " mb"
        elif si > 1024:
            return p(si/ 1024) + " kb"
        else:
            return p(si) + " bytes"
    def getMetaDicInfo(files, filler: IFiller):
        dic = ExecuteDatable(FileList2Dic, files).execute()
        metaDic = ExecuteDatable(MetaTheDictionary, dic).execute()
        filler.setData(metaDic)
        newDic = filler.fill()
        return newDic
######
from modules.Explorer.DictionaryExplorer import Node, NodeTreeExplorer
class GNode(Node):
    def __init__(self, idd):
        super().__init__(idd)
        self.set_value_func(lambda x: os.path.basename(x.idd))
    @property
    def value(self):
        return self._func(self)
    def set_value_func(self, func):
        self._func = func
class IFillerStrategy:
    def fill(self, node):
        pass
class GFiller(IFiller):
    def set_filling_strategy(self, star: IFillerStrategy):
        self._strategy = star
    def fill(self):
        self._strategy.fill(self._root)
    def set_graph_root(self, root):
        self._root = root
class SizeFillerStrategy(IFillerStrategy):
    def fill(self, node: Node):
        from FileDatabase import File
        ch = node.children
        if len(ch) == 0:
            try:
                node.extra_info.size = File.size(node.idd)
            except: 
                node.extra_info.size = 0
            return node.extra_info.size
        node.extra_info.size = sum([self.fill(n) for n in ch])
        return node.extra_info.size
class NumberFillerStrategy(IFillerStrategy):
    def fill(self, node: Node):
        ch = node.children
        if len(ch) == 0:
            node.extra_info.number = 1
            return node.extra_info.number
        node.extra_info.number = sum([self.fill(n) for n in ch])
        return node.extra_info.number
class ICreator:
    def create(self):
        pass

class Creator(ICreator):
    def __init__(self):
        self.set_creator_class(GNode)
        self.set_setproperty_func(lambda x: x)
    def create(self, *val):
        return self._prop_func(self._className(*val))
    def set_creator_class(self, className):
        self._className = className
    def set_setproperty_func(self, func):
        self._prop_func = func
class Files2NodeGraph(IOps):
    def __init__(self):
        self._node_map = {}
        self.set_node_creator(Creator())
        self._root = None
    def set_files(self, files):
        from WordDB import WordDB
        self._files = files
        self._common_part = WordDB.commonPart(self._files).strip(os.sep)
    def execute(self):
        for ch in self._files:
            self._update_parent(ch)
        self._root = min(self._node_map, key=lambda x: len(x))
        return self._node_map
    def _update_parent(self, parent):
        child = parent
        while True:
            parent = os.path.dirname(child)
            if parent == "" or child.strip(os.sep) == self._common_part:
                break
            n = self._get_node(parent)
            n.children.add(self._get_node(child))
            child = parent
    def _get_node(self, val):
        if val not in self._node_map:
            node = self._node_creator.create(val)
            node.children = set()
            self._node_map[val] = node
        return self._node_map[val]
    def set_node_creator(self, creator):
        self._node_creator = creator
        
    def export(self, name):
        if not name.endswith(".pkl"):
            name += '.pkl'
        SerializationDB.pickleOut({'nodes': self._node_map, 'root': self._root}, name)
    def set_path(self, folder_path: str):
        from Path import Path
        self.set_files(Path.getFiles(folder_path, True))
class DynamicNodeExplorer(NodeTreeExplorer):
    def __init__(self, root=None):
        self._pos = []
        self.set_root(root)
        self.set_displayer_func(lambda x: x.value)
        self._current_map = {}
    def cd(self, key):
        cur = self._current_map[key]
        self._pos.append(cur)
    def dirList(self):
        self._current_map.clear()
        current = self._pos[-1]
        folders = []
        files = []
        for c in current.children:
            if len(c.children):
                folders.append(c)
            else:
                files.append(c)
        files = self._sort_func(files)
        folders = self._sort_func(folders)
        d_folders = self._make_displayable(folders)
        d_files =  self._make_displayable(files)
        return d_folders,d_files
    def _make_displayable(self, values):
        res = []
        for f in values:
            key = self._displayer_func(f)
            self._current_map[key] = f
            res.append(key)
        return res
    def set_sorted_func(self, func):
        self._sort_func = func
    def set_displayer_func(self, func):
        self._displayer_func = func
    def export(self, name):
        if not name.endswith(".pkl"):
            name += '.pkl'
        SerializationDB.pickleOut(self._root, name)
    def load(self, pkl):
        self.set_root(SerializationDB.readPickle(pkl))
    def set_root(self, root: GNode):
        self._root = root
        self._pos.clear()
        self._pos.append(self._root)
class FileAnalyse:
    def size():
        class Temp:
            def fromPath(path, save = None):
                fa = FileAnalyser()
                fa.explorer.setFunc(FileAnalyser.sizeb)
                afr = AllFilesReader(path)
                fa.setFileReader(afr)
                fa.analyse()
                return fa
            def fromPickle(pickle):
                mde  = MetaDicExplorer()
                mde.setFunc(FileAnalyser.sizeb)
                data = SerializationDB.readPickle(pickle)
                mde.setData(data)
                mde.explore()
        return Temp
    def new_design_file_explorer():
        class Temp:
            def from_path(path):
                from modules.mobileCode.GenericExplorer import Main
                nodes, root = Main.get_files_graph().from_path(path)
                Temp._run(root)
            def _run(root):
                from modules.mobileCode.GenericExplorer import Main, NumberView, DepthView, SizeView, \
                    SaveInfo, NoInfoView, LoadFromFile
                run_at_last_command, displayer = Main.os_explorer(root = root, display=False)
                displayer.set_command(NumberView('number'))
                displayer.set_command(DepthView("depth"))
                displayer.set_command(SizeView('size'))
                displayer.set_command(NoInfoView("no"))
                displayer.set_command(SaveInfo("save"))
                displayer.set_command(LoadFromFile("load"))
                displayer.set_command(run_at_last_command)
                displayer.display()
            def from_pickle(pkl):
                root = SerializationDB.readPickle(pkl)
                from modules.mobileCode.GenericExplorer import Main
                Temp._run(root)
        return Temp
    def zip_file(path): # from cmd, terminal
        from ZiptoolDB import ZiptoolDB
        from DataStructure import MaxDepthInverseCalculator
        from modules.mobileCode.GenericExplorer import NumberView, NoInfoView, DepthView, Main

        paths = ZiptoolDB.getZipContent(path)
        files = list(filter(lambda x: not x.endswith("/"), paths))

        gr , root = Main.get_files_graph().from_files(files)
        sf = GFiller()
        sf.set_graph_root(root)
        sf.set_filling_strategy(NumberFillerStrategy())
        sf.fill()
        MaxDepthInverseCalculator(root).execute()
        run_at_last_command, displayer = Main.explorer(root = root, display=False)
        displayer.set_command(NumberView('number'))
        displayer.set_command(DepthView("depth"))
        displayer.set_command(NoInfoView("no"))
        displayer.set_command(run_at_last_command)
        displayer.display()
            
class FileAnalyseGUI:
    def size():
        class Tem:
            def path(path):
                FileAnalyseGUI.explorer(path)
            def pickle(pkl):
                from modules.Explorer.DictionaryExplorer import Main
                from SerializationDB import SerializationDB
                gr = SerializationDB.readPickle(pkl)
                root = gr['data'][gr['root']]
                dne = DynamicNodeExplorer(root)
                dne.set_sorted_func(
                    lambda xList: sorted(xList, key=lambda x: x.extra_info.size, reverse=True))
                dne.set_displayer_func(
                    lambda x: os.path.basename(x.idd) + f" - {FileAnalyser.sizeb(x.extra_info.size)}")
                Main.explore(dne)
        return Tem
    def explorer(path, viewfunc=lambda x: FileAnalyser.sizeb(x.extra_info.size),
            sort_func = lambda x: x.extra_info.size, reverse = True):
        from modules.Explorer.DictionaryExplorer import Main
        from Path import Path
        from DataStructure import MaxDepthInverseCalculator
        cr = Creator()
        cr.set_creator_class(GNode)
        fng = Files2NodeGraph()
        fng.set_files(Path.getFiles(path, True))
        fng.set_node_creator(cr)
        gr = fng.execute()
        root = gr[fng._common_part]
        sf = GFiller()
        sf.set_graph_root(root)
        sf.set_filling_strategy(SizeFillerStrategy())
        sf.fill()
        sf.set_filling_strategy(NumberFillerStrategy())
        sf.fill()
        MaxDepthInverseCalculator(root).execute()
        dne = DynamicNodeExplorer(root)
        dne.set_sorted_func(
            lambda xList: sorted(xList, key=sort_func, reverse=reverse))
        dne.set_displayer_func(
            lambda x: os.path.basename(x.idd) + f" - {viewfunc(x)}")
        Main.explore(dne)
        return root