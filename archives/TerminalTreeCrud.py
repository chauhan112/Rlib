from modules.Logger.TextWriter import TextWriter
from modules.Logger.Interfaces import IDumperWriter
from modules.mobileCode.CmdCommand import GController, CmdCommandHandler, GCommand, \
    IRunnable, IListChangingOps, GModalSetable, GParentable, IParentable
import os
from modules.mobileCode.tree import LayerDicListWithDepthInfo, LayeredDisplayElements, Goback, \
    LayerDisplayerWithDepth, LayerDicList
from SerializationDB import SerializationDB
from ListDB import ListDB
from PickleCRUDDB import PickleCRUD
from modules.mobileCode.OpsListRunner import GRunnerWithModel,ReturnableOpsRunner,ReturnableOpsRunnerWithList
from modules.mobileCode.SelectPath import FileSelector
from Path import Path
class FilePathListCollection:
    clip_content = "data/trees/.clip.pkl"
class ITreeFile:
    def getPath(self):
        raise NotImplementedError('abstract method')
    def getContent(self):
        raise NotImplementedError('abstract method')
    def save(self):
        raise NotImplementedError('abstract method')
    def crud(self):
        raise NotImplementedError('abstract method')
class IModalSetable:
    def setModel(self, model):
        raise NotImplementedError('abstract method')
class IAdvanceOps:
    def getContentWithIndex(self, index):
        raise NotImplementedError('abstract method')
class DicListWithMoreOps(LayerDicList, IListChangingOps, IAdvanceOps):
    def delete(self, index):
        content = self.getCurrentValue()
        if index < len(content):
            val = list(content.keys())[index]
            ListDB.dicOps().delete(self.dicExp.content, self.getCurrentPath() + [val])
    def add(self, key, val, overwrite =False):
        content = self.getCurrentValue()
        if key not in content or overwrite:
            ListDB.dicOps().add(self.dicExp.content, self.getCurrentPath() + [key], val)
            return
        print("value already exists")
    def getContentWithIndex(self, index):
        content = self.getCurrentValue()
        if index < len(content):
            val = list(content.keys())[index]
            return val, ListDB.dicOps().get(self.dicExp.content, self.getCurrentPath() + [val])
class PklTreeFile(ITreeFile):
    def __init__(self, path):
        if os.path.exists(path) and os.path.isdir(path):
            raise IOError("given path is directorey")
        if not path.endswith(".pkl"):
            path += '.pkl'
        self.path = path
        self._crud = None
    def getPath(self):
        return self.path
    def crud(self):
        if not os.path.exists(self.path):
            SerializationDB.pickleOut({}, self.path)
        if self._crud is None:
            self._crud = PickleCRUD(self.path, loadFromMain = False)
        return self._crud
    def save(self):
        self.crud()._write()
    def getContent(self):
        return self.crud().getContent()
class TreeCrudModel(GParentable):
    def __init__(self, reader: IDumperWriter = None):
        self.reader = reader
        self.currentTree = None
        self._strLastRead = 'last read'
        self.metaInfo = {self._strLastRead:None}
        self._filesLoc = []
        self._currentContent= None
    def loadReader(self):
        content = self.reader.readAll()
        if self._strLastRead in content:
            self.load(content[self._strLastRead])
        for val in content:
            if self._strLastRead != val:
                self._filesLoc += Path.filesWithExtension('pkl', self.sanitize(val), False)
    def load(self, file):
        file = self.sanitize(file)
        if self.currentTree is not None:
            self.currentTree.save()
        self.currentTree = PklTreeFile(file)
        filepath = self.rel_path(self.currentTree.getPath())
        dirname = self.rel_path(os.path.dirname(os.path.abspath(filepath)))
        self.metaInfo[self._strLastRead] = filepath
        self.reader.add(self._strLastRead, filepath, overwrite = True)
        self.reader.add(dirname, filepath, overwrite = True)
        self._filesLoc += Path.filesWithExtension('pkl',dirname, False)
        self._filesLoc = list(set(self._filesLoc))
    def getAllTrees(self):
        return self._filesLoc
    def rel_path(self, path):
        path = self.sanitize(path)
        replacing_path = self.sanitize(os.getcwd())
        fi = path.replace(replacing_path, "").strip("/")
        if fi == "":
            fi = '.'
        return fi
    def sanitize(self, path):
        return path.replace("\\", "/")
    def getCurrentTree(self):
        if self.currentTree is None:
            from CryptsDB import CryptsDB
            name = CryptsDB.generateRandomName()
            path = os.path.dirname(self.reader.path) +os.sep + name
            self.load(path)
        return self.currentTree
class SaveAs(GCommand, GModalSetable):
    def getHelp(self):
        return self.id, 'save the content as new file'
    def callback(self):
        if 'o' in self.data:
            SerializationDB.pickleOut(self.parent.parent.lister.dicExp.content,
                self.model.getCurrentTree().getPath())
            return
        path = input("enter file path to save \n: ")
        if not path.endswith(".pkl"):
            path += '.pkl'
        dirpath = os.path.dirname(path)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        if not os.path.exists(path):
            if 'p' in self.data:
                SerializationDB.pickleOut(self.parent.parent.lister.getCurrentValue(), path)
            else:
                SerializationDB.pickleOut(self.parent.parent.lister.dicExp.content, path)
            self.model.load(path)
            return
        print(f"{path} already exists")
class DeleteNode(GCommand, GModalSetable):
    def getHelp(self):
        return self.id, 'delete a node; del id'
    def callback(self):
        try:
            valID = int(self.data[-1])
        except:
            print("give an index to delete the node")
            return
        self.parent.parent.lister.delete(valID)
        self.parent.runcmd("save o")
class Name(GCommand, GModalSetable):
    def callback(self):
        print(self.model.getCurrentTree().getPath())
    def getHelp(self):
        return self.id, 'get name of current file'
class Cut(GCommand, GModalSetable):
    def getHelp(self):
        return self.id, 'cut node; cut index'
    def callback(self):
        total_elements = len(self.parent.parent.lister.getCurrentValue())
        try:
            valIDs = []
            for val in self.data:
                val_int = int(val)
                if val_int < 0:
                    valIDs.append(val_int + total_elements)
                else:
                    valIDs.append(val_int)
        except Exception as e:
            print("give an index to delete the node")
            print(e)
            return
        data = [self.parent.parent.lister.getContentWithIndex(idd) for idd in valIDs]
        self.model.clip = data
        so = sorted(valIDs, reverse=True)
        [ self.parent.runcmd(f'del {i}') for i in so ]
        self.write_clip_data()
    def write_clip_data(self):
        assert type(self.model.clip) == list
        newDic = {}
        for key, val in self.model.clip:
            if type(val) == dict:
                val = val.copy()
            newDic[key] = val
        SerializationDB.pickleOut(newDic, FilePathListCollection.clip_content)
class Paste(GCommand, GModalSetable):
    def getHelp(self):
        return self.id, 'paste the cut node: paste'
    def callback(self):
        assert type(self.model.clip) == list
        for data in self.model.clip:
            key, val = data
            if type(val) == dict:
                val = val.copy()
            self.parent.parent.lister.add(key, val)
        self.parent.runcmd("save o")
class AddNewElement(GCommand):
    def callback(self):
        val = ' '.join(self.data).strip()
        if val == '':
            val = input('key: ')
        lister = self.parent.parent.lister
        content = lister.getCurrentValue()
        if val not in content:
            lister.add(val, {})
        self.parent.runcmd('save o')
    def getHelp(self):
        return self.id, 'add new node'
class LoadFromFile(GCommand, GModalSetable):
    def getHelp(self):
        return self.id, 'load tree'
    def navigatePath(self, model):
        initial_path = os.path.dirname(self.model.getCurrentTree().path)
        fs = FileSelector(initial_path, filetype='.pkl')
        fs.run()
        model.cnt.cmdRunner._loopBreaker = True
        if not fs.isCancelled():
            return fs.getSelected()
    def selectFile(self, model):
        def cll(ele):
            curval = ele.getCurrentValue()
            val = None
            if type(curval) == tuple:
                val = curval[1]
            else:
                val =ele.parent.parent.lister.exp.getVal(curval)
            ele.parent._loopBreaker = True
            return val
        rorwl = ReturnableOpsRunnerWithList(self.model.getAllTrees(),cll)
        rorwl.run()
        return rorwl.get()
    def _load_with_filename_hint(self, hint):
        initial_path = os.path.dirname(self.model.getCurrentTree().path)
        files_folders = os.listdir(initial_path)
        is_file = lambda f: os.path.isfile('/'.join([initial_path, f]))
        files = list(filter(is_file, files_folders))
        print(files)
        files_with_hint = list(filter(lambda x: x[:len(hint)].lower() == hint, files))
        count = len(files_with_hint)
        if count > 0:
            self._read(initial_path + "/" +files_with_hint[0])
        else:
            print("no match found")
    def callback(self):
        if len(self.data) != 0:
            self._load_with_filename_hint(self.data[0])
            return
        dic = {
            'select file': GRunnerWithModel(self.selectFile),
            'give path': GRunnerWithModel(self.givePath),
            'navigate': GRunnerWithModel(self.navigatePath)
        }
        ror = ReturnableOpsRunner(dic)
        ror.run()
        self._read(ror.get())
    def givePath(self, model):
        path = input("enter path: ")
        model.cnt.cmdRunner._loopBreaker = True
        if path == "q":
            return
        return os.path.abspath(path)
    def _read(self, path):
        if path is None:
            return
        self.model.load(path)
        self.model._currentContent.clear()
        self.model._currentContent.update(self.model.getCurrentTree().getContent())
        self.model.parent.cnt.lister.setData(self.model._currentContent)
class TreeCrud(IRunnable):
    def __init__(self, model: IParentable):
        self.model = model
        self.model.setParent(self)
        self.cnt = None
        self.layer = 3
    def run(self):
        if self.cnt is None:
            self.model.loadReader()
            disp = LayeredDisplayElements()
            disp._runAfter = True
            self.model._currentContent = self.model.getCurrentTree().getContent()
            self.cnt = GController(self.model._currentContent, cmdRunner = CmdCommandHandler(
                        callback = self._callback, extraCommands= self._getCommands()),
                    lister = DicListWithMoreOps(self.layer), displayer = disp)
        self.cnt.cmdRunner._loopBreaker = False
        self.cnt.run()
    def setLayer(self, layer):
        if self.cnt is None:
            self.layer = layer
        else:
            self.cnt.lister.layer = layer
    def _callback(self, ele):
        from ExplorerDB import ExplorerDB
        ele.parent.parent.elementsDisplayer._lastPos.append(ele.getCurrentValue())
        ExplorerDB._callback(ele)
    def _getCommands(self):
        cmds = [SaveAs('save'), DeleteNode("del"), Name('name'), Cut('cut'), Paste('paste'), LoadFromFile('ll')]
        for cmd in cmds:
            cmd.setModel(self.model)
        return cmds + [AddNewElement("add"), Goback('b')]
class TreeWithDepth(TreeCrud):
    pass
