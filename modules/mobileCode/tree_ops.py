import os
from SerializationDB import SerializationDB
from modules.Explorer.personalizedWidgets import IExplorerDisplayer
from modules.Explorer.model import IExplorer
class ICommand:
    def check(self, parent, val):
        pass
    def callback(self, parent):
        pass
    def get_help(self):
        pass
class GCommand(ICommand):
    def __init__(self, idd="q"):
        self.idd = idd
    def check(self, parent, val):
        self.params = val.strip().split()
        if len(self.params) > 0:
            return self.params[0] == self.idd
        return False
class Exit(GCommand):
    def callback(self, parent):
        parent.set_breaker()
    def get_help(self):
        return f"{self.idd} -> exit the explorer"
class Clear(GCommand):
    def callback(self, parent):
        import os
        os.system("clear")
    def get_help(self):
        return f"{self.idd} -> clear the current screen"
class Help(GCommand):
    def callback(self, parent):
        for i, cmd in enumerate(parent.get_commands()):
            print(i,cmd.get_help())
    def get_help(self):
        return f"{self.idd} -> help about commands"
class Goback(GCommand):
    def callback(self, parent):
        exp = parent.get_explorer()
        exp.goBack()
    def get_help(self):
        return f"{self.idd} -> goback one step in explorer"
class IRenderer:
    def render(self):
        pass
    def set_explorer(self, exp: IExplorer):
        pass
class ListElement(GCommand):
    def callback(self, parent):
        exp = parent.get_explorer()
        if not self._explorer_set:
            self._renderer.set_explorer(exp)
            self._explorer_set = True
        self._renderer.render()
    def set_renderer(self, renderer: IRenderer):
        self._renderer = renderer
        self._explorer_set = False
    def get_help(self):
        return f"{self.idd} -> list the elements"
class LayeredTreeRenderer(IRenderer):
    def set_explorer(self, exp:IExplorer):
        self._exp = exp
    def render(self):
        folders, _ = self._exp.dirList()
        if len(folders):
            root = folders.pop()
            mt = ModifyTreeForNode(self._exp._pos[-1].value)
            mt.set_root(root)
            mt.execute()
class ElementSelected(ICommand):
    def __init__(self, idd='i'):
        self._renderer = None
        self.idd = ''
        self._selected = None
    def check(self, parent, val):
        try:
            self._selected = int(val)
            return True
        except:
            return False
    def get_help(self):
        return "n -> integer value to select from the list"
    def callback(self, parent):
        exp = parent.get_explorer()
        if self._selected is not None:
            exp.cd(self._selected)
        self._selected = None
class Alwaysrun(ICommand):
    def __init__(self):
        self._commands_ids = []
        self._commands = []
        self.idd = ""
    def check(self, parent, val):
        return True
    def callback(self, parent):
        cmds = parent.get_commands()
        for c in cmds:
            if c.idd in self._commands_ids:
                c.callback(parent)
        for c in self._commands:
            c.callback(parent)
    def set_cmd_idd(self, idd):
        self._commands_ids.append(idd)
    def set_command(self,cmd: ICommand):
        self._commands.append(cmd)
    def get_help(self):
        return "  -> dummy command which runs every entry"
class CmdExplorerDisplayer(IExplorerDisplayer):
    def __init__(self):
        self._commands = []
        self._paths = []
        self._clear = Clear("c")
        [self.set_command(cmd) for cmd in [Exit('q'), Help('h'), self._clear]]
        self._breaker = False
    def set_explorer(self, explorer: IExplorer):
        self._exp = explorer
    def set_command(self, cmd: ICommand):
        self._commands.append(cmd)
    def display(self):
        self._run_cmd("c")
        while True:
            inp = input("enter cmd: ")
            self._run_cmd(inp)
            if self._breaker:
                break
    def _run_cmd(self, c_str):
        for cmd in self._commands:
            if cmd.check(self, c_str):
                cmd.callback(self)
            if self._breaker:
                break
    def set_breaker(self):
        self._breaker = True
    def get_explorer(self):
        return self._exp
    def get_commands(self):
        return self._commands
from OpsDB import IOps
from modules.FileAnalyser.FileAnalyser import GNode
class Dic2Graph(IOps):
    def __init__(self):
        self._path = []
        self._node_map = {}
    def set_dic(self, dic):
        self._dic = dic
    def execute(self):
        self._path.clear()
        self._node_map.clear()
        self._path.append('root')
        self._get_node(self._path)
        self._execute(self._dic)
        return self._node_map
    def _execute(self, val):
        for key in val:
            value = val[key]
            node = self._get_node(self._path)
            node.children.append(self._get_node(self._path + [key]))
            self._path.append(key)
            if type(value) == dict:
                self._execute(value)
            self._path.pop()
    def _get_node(self, loc: list[str]):
        val = "/".join(loc)
        if val not in self._node_map:
            node = self._node_creator.create(val)
            node.extra_info.value = loc[-1]
            self._node_map[val] = node
        return self._node_map[val]
    def set_node_creator(self, creator):
        self._node_creator = creator
    def export(self, name):
        if not name.endswith(".pkl"):
            name += '.pkl'
        SerializationDB.pickleOut(self._node_map, name)
from modules.mobileCode.tree import TreeFromStackOverflow, ITreeable
class MTreeable(GNode):
    def iterdir(self):
        return self.children
    def is_dir(self):
        return True
    @property
    def name(self):
        return self.value
    @property
    def value(self):
        m = NameDisplayModel.get_instance()
        return m.display_node_info(self)
class ModifyTreeForNode(TreeFromStackOverflow):
    def __init__(self, parent = "root"):
        self.parent = parent
    def set_root(self, root: MTreeable):
        self.tree = self.getTree(root)
class LayerNode(IOps):
    def set_root(self, root):
        self._root = root
    def execute(self):
        return self._get_node(self._root, self._layer)
    def _get_node(self, node, l):
        n = self._func(node, MTreeable(node.idd))
        if l == 0:
            return n
        for ch in node.children:
            n.children.append(self._get_node(ch, l-1))
        return n
    def set_layer(self, nr:int):
        self._layer = nr
    def set_modify_func(self, func):
        self._func = func
class TreeNodeExplorer(IExplorer):
    def __init__(self):
        self._pos = []
        self._layer_model = None
        self._map_keys = {}
    def set_root(self, root):
        self._root = root
        self._pos.append(self._root)
    def cd(self, val):
        if val >= len(self._map_keys):
            print("index out error")
            return
        key = list(self._map_keys.keys())[val]
        self._pos.append(self._map_keys[key])
    def goBack(self):
        if len(self._pos) > 1:
            self._pos.pop()
    def dirList(self):
        if self._layer_model is None:
            self._layer_model = LayerNode()
            self._layer_model.set_layer(3)
            self._layer_model.set_modify_func(self._modify_func)
        ndoe = self._pos[-1]
        self._layer_model.set_root(ndoe)
        node = self._layer_model.execute()
        self._map_keys.clear()
        for c in ndoe.children:
            self._map_keys[c.value] = c
        return [node], []
    def _modify_func(self, old: MTreeable, new: MTreeable):
        new.extra_info.__dict__ = old.extra_info.__dict__
        return new
class ChangeLayerNr(GCommand):
    def callback(self, parent):
        if len(self.params) > 1:
            val = int(self.params[-1])
            exp = parent.get_explorer()
            exp._layer_model.set_layer(val)
    def get_help(self):
        return f"{self.idd} -> change the size of the depth layers"
class Node2Dic(IOps):
    def set_root(self, root):
         self._root = root
    def execute(self):
        return self._node_2_dic(self._root)
    def _node_2_dic(self, node):
        dic = {}
        for ch in node.children:
            dic[ch.extra_info.value] = self._node_2_dic(ch)
        return dic
class SyncNodeWithFile(IOps):
    def __init__(self, root, file):
        self._root = root
        self._file = file
    def execute(self):
        from SerializationDB import SerializationDB
        nd = Node2Dic()
        nd.set_root(self._root)
        SerializationDB.pickleOut(nd.execute(), self._file)
from modules.Logger.Interfaces import IDumperWriter
class FileModel:
    def __init__(self):
        self._working_dir = None
        self._current_tree = None
        self._reader = None
        self._last_read_str = "last read"
        self._recycle_file = None
    def get_current_file(self):
        val = self._reader.read(self._last_read_str)
        if val is None:
            from CryptsDB import CryptsDB
            name = CryptsDB.generateRandomName()
            path = os.sep.join([self._working_dir, name]) +  ".pkl"
            SerializationDB.pickleOut({}, path)
            self._reader.add(self._last_read_str, path, True)
            self.add_new_file(path)
        return self._reader.read(self._last_read_str)
    def set_working_dir(self, path):
        if os.path.exists(path):
            self._initialize(path)
    def set_reader(self, reader: IDumperWriter):
        self._reader = reader
    def add_new_file(self, filepath):
        filepath = os.path.abspath(filepath)
        self._reader.add(os.path.basename(filepath), filepath, True)
    def get_all_files(self):
        allfiles = self._reader.readAll()
        if self._last_read_str in allfiles:
            del allfiles[self._last_read_str]
        return list(allfiles.values())
    def get_recycle_path(self):
        return self._recycle_file
    def _initialize(self, path):
        from modules.Logger.TextWriter import TextWriter, TextParser
        self._working_dir = path
        info_file = self._working_dir + os.sep + "trees.txt"
        self._recycle_file = self._working_dir + os.sep + ".storage.pkl"
        if not os.path.exists(info_file):
            File.createFile(info_file )
        self._reader = TextWriter()
        self._reader.set_parser(TextParser(info_file))
        if not os.path.exists(self._recycle_file):
            SerializationDB.pickleOut({}, self._recycle_file)
        if not os.path.exists(self.get_current_file()):
            self._reader.delete(self._last_read_str)
            self._reader.delete(os.path.basename(self.get_current_file()))
    def set_current_tree(self, filepath):
        if not os.path.exists(filepath):
            SerializationDB.pickleOut({}, filepath)
        self._reader.add(self._last_read_str, filepath, True)
class ModelNeedable:
    def set_file_model(self, model: FileModel):
        self._model = model
class NodeOnChangeApply:
    def __init__(self, **infos):
        self._infos = infos
    def apply(self):
        from DataStructure import MaxDepthInverseCalculator
        MaxDepthInverseCalculator(self._infos['root']).execute()
        FillNumber(self._infos['root']).execute()
        if 'model' in self._infos:
            SyncNodeWithFile(self._infos['root'], self._infos['model'].get_current_file()).execute()
        self._infos['root'].extra_info.index = 0
        EnumerateNodes().fill(self._infos['root'])
class AddNew(GCommand, ModelNeedable):
    def callback(self, parent):
        exp = parent.get_explorer()
        node = exp._pos[-1]
        if len(self.params) > 1:
            val = " ".join(self.params[1:])
            new_node = MTreeable("/".join([node.idd, val]))
            new_node.extra_info.value = val
            found = False
            for ch in node.children:
                if ch.idd.replace(node.idd, "").strip("/") == val:
                    print('value already exists')
                    found = True
            if not found:
                node.children.append(new_node)
        NodeOnChangeApply(root = exp._root, model=self._model).apply()
    def get_help(self):
        return f"{self.idd} -> add new node: add valname"
class DeleteNode(GCommand, ModelNeedable):
    def callback(self, parent):
        exp = parent.get_explorer()
        if len(self.params) > 0:
            indices = [int(v) for v in self.params[1:]]
            keys = exp._map_keys.keys()
            indices = list(map(lambda x: x % len(keys), indices))
            new_children = []
            temp = []
            for i, k in enumerate(keys):
                if i not in indices:
                    new_children.append(exp._map_keys[k])
                else:
                    temp.append(exp._map_keys[k])
            current_node = exp._pos[-1]
            current_node.children.clear()
            current_node.children += new_children
            ch = MTreeable("root")
            ch.children += temp
            SyncNodeWithFile(ch, self._model.get_recycle_path()).execute()
        NodeOnChangeApply(root = exp._root, model=self._model).apply()
    def get_help(self):
        return f"{self.idd} -> delete a node: del 0 1 2"
class Cut(DeleteNode):
    def get_help(self):
        return f"{self.idd} -> cut nodes for pasting: cut 0 1 2"
class Paste(GCommand, ModelNeedable):
    def callback(self, parent):
        exp = parent.get_explorer()
        content = SerializationDB.readPickle(self._model.get_recycle_path())
        self._creator.set_dic(content)
        root = self._creator.execute()['root']
        current = exp._pos[-1]
        ids = set([x.extra_info.value for x in current.children])
        for ch in root.children:
            val = ch.idd[len("root/"):]
            if val not in ids:
                current.children.append(ch)
            else:
                print(val + " already exists")
        NodeOnChangeApply(root = exp._root, model=self._model).apply()
    def set_graph_creator(self, creator: Dic2Graph):
        self._creator = creator
    def get_help(self):
        return f"{self.idd} -> paste node from cut or deleted items"
class NameDisplayModel:  # singleton
    instance = None
    def __init__(self):
        self.set_display_info_func(lambda x: x.extra_info.value)
    def get_instance():
        if NameDisplayModel.instance is None:
            NameDisplayModel.instance = NameDisplayModel()
        return NameDisplayModel.instance
    def display_node_info(self, node: MTreeable):
        return self._func(node)
    def set_display_info_func(self, func):
        self._func = func
class DepthInfo(GCommand):
    def callback(self, parent):
        model = NameDisplayModel.get_instance()
        model.set_display_info_func(lambda x: f"{x.extra_info.depth}-{x.extra_info.value}")
    def get_help(self):
        return f"{self.idd} -> show depth information"
class NoInfo(GCommand):
    def callback(self, parent):
        model = NameDisplayModel.get_instance()
        model.set_display_info_func(lambda x: x.extra_info.value)
    def get_help(self):
        return f"{self.idd} -> set default information"
class NumberOfChildrenInfo(GCommand):
    def callback(self, parent):
        model = NameDisplayModel.get_instance()
        model.set_display_info_func(lambda x: f"{x.extra_info.number}-{x.extra_info.value}")
    def get_help(self):
        return f"{self.idd} -> set total number of children info"
class FillNumber(IOps):
    def __init__(self, root):
        self._root = root
    def execute(self):
        from modules.FileAnalyser.FileAnalyser import GFiller, NumberFillerStrategy
        filler = GFiller()
        filler.set_graph_root(self._root)
        filler.set_filling_strategy(NumberFillerStrategy())
        filler.fill()
from modules.FileAnalyser.FileAnalyser import IFillerStrategy
class EnumerateNodes(IFillerStrategy):
    def fill(self, node: MTreeable):
        children = node.children
        for i, ch in enumerate(children):
            ch.extra_info.index = i
            self.fill(ch)
class ListFiles(GCommand, ModelNeedable):
    def callback(self, parent):
        dirname = os.path.dirname(self._model.get_current_file())
        if len(self.params) < 2:
            return
        try:
            val = os.sep.join([dirname, self.params[-1]])
            if val == "":
                val = "."
            files = os.listdir(val)
            print(list(filter(lambda x: x.endswith(".pkl"), files)))
        except Exception as e:
            print(e)
    def get_help(self):
        return f"{self.idd} -> list files of given dir: ll .."
class LoadFile(GCommand, ModelNeedable):
    def callback(self, parent):
        file = self._get_file()
        if file is None:
            return
        exp = parent.get_explorer()
        exp._pos.clear()
        self._creator.set_dic(SerializationDB.readPickle(file))
        root = self._creator.execute()['root']
        exp.set_root(root)
        NodeOnChangeApply(root = exp._root).apply()
        self._model.set_current_tree(file)
        self._model.add_new_file(file)
    def _get_file(self):
        val = self.params[-1]
        dirname = os.path.dirname(self._model.get_current_file())
        dir_of_param = os.path.dirname(val)
        path = os.sep.join([dirname, dir_of_param])
        if path == "":
            path = "."
        files = os.listdir(path)
        pkls = list(filter(lambda x: x.endswith(".pkl"), files))
        filename = os.path.basename(val)
        file_starts_with = list(filter(lambda x: x[:len(filename)] == filename, pkls))
        if len(file_starts_with) == 1:
            return os.path.abspath(path + os.sep + file_starts_with[0])
        print(pkls)
    def get_help(self):
        return f"{self.idd} -> load file from current index: load filename or filestarts_with"
    def set_graph_creator(self, creator: Dic2Graph):
        self._creator = creator
class NameCommand(GCommand, ModelNeedable):
    def callback(self, parent):
        print(self._model.get_current_file())
    def get_help(self):
        return f"{self.idd} -> prints the name of the current file"
class DirCommand(GCommand, ModelNeedable):
    def callback(self, parent):
        dirpath = os.path.dirname(self._model.get_current_file())
        if dirpath == "":
            dirpath = "."
        dirlist = os.listdir(dirpath)
        print(list(filter(lambda x: os.path.isdir(os.sep.join([dirpath,x])), dirlist)))
    def get_help(self):
        return f"{self.idd} -> lists the directories of the current file folder"
class OpenFolderCommand(GCommand, ModelNeedable):
    def callback(self, parent):
        dirpath = os.path.dirname(self._model.get_current_file())
        if dirpath == "":
            dirpath = "."
        from Path import Path
        Path.openExplorerAt(dirpath)
    def get_help(self):
        return f"{self.idd} -> open explorer at current file path"
class CmdFeature(GCommand):
    def callback(self, parent):
        os.system(" ".join(self.params[1:]))
    def get_help(self):
        return f"{self.idd} -> run cmd commands"
class SaveAsCommand(GCommand, ModelNeedable):
    def callback(self, parent):
        dirpath = os.path.dirname(self._model.get_current_file())
        if dirpath == "":
            dirpath = "."
        name = self.params[-1]
        if not name.endswith(".pkl"):
            name += ".pkl"
        exp = parent.get_explorer()
        target_file = os.sep.join([dirpath, name])
        if not os.path.exists(target_file):
            SyncNodeWithFile(exp._root, target_file).execute()
        else:
            print("file already exists")
    def get_help(self):
        return f"{self.idd} -> save file as new: save filename.pkl"
class EnumerateElements(GCommand):
    def callback(self, parent):
        model = NameDisplayModel.get_instance()
        model.set_display_info_func(lambda x: f"{x.extra_info.index}-{x.extra_info.value}")
    def get_help(self):
        return f"{self.idd} -> show depth information"
class Main:
    def run_tree_ops_at(path):
        from modules.FileAnalyser.FileAnalyser import Creator
        fm = FileModel()
        fm.set_working_dir(path)
        content = SerializationDB.readPickle(fm.get_current_file())
        dg = Dic2Graph()
        dg.set_dic(content)
        cr = Creator()
        cr.set_creator_class(MTreeable)
        dg.set_node_creator(cr)
        gr = dg.execute()
        root = gr['root']
        NodeOnChangeApply(root = root).apply()
        ced = CmdExplorerDisplayer()
        ele = ElementSelected()
        l = LayeredTreeRenderer()
        ced.set_command(ele)
        gb = Goback("b")
        ced.set_command(gb)
        exp = TreeNodeExplorer()
        exp.set_root(root)
        ced.set_explorer(exp)
        ced.set_command(ChangeLayerNr("cl"))
        an = AddNew("add")
        an.set_file_model(fm)
        ced.set_command(an)
        delcmd = DeleteNode('del')
        delcmd.set_file_model(fm)
        ced.set_command(delcmd)
        cut_cmd = Cut('cut')
        cut_cmd.set_file_model(fm)
        ced.set_command(cut_cmd)
        paste_cmd = Paste('paste')
        paste_cmd.set_file_model(fm)
        paste_cmd.set_graph_creator(dg)
        ced.set_command(paste_cmd)
        ced.set_command(NoInfo("no"))
        ced.set_command(DepthInfo("depth"))
        ced.set_command(EnumerateElements("enum"))
        ced.set_command(NumberOfChildrenInfo("number"))
        name_cmd = NameCommand("name")
        name_cmd.set_file_model(fm)
        ced.set_command(name_cmd)
        dirlist_cmd = DirCommand("dirlist")
        dirlist_cmd.set_file_model(fm)
        ced.set_command(dirlist_cmd)
        ofc = OpenFolderCommand("here")
        ofc.set_file_model(fm)
        ced.set_command(ofc)
        sac = SaveAsCommand("save")
        sac.set_file_model(fm)
        ced.set_command(sac)
        ced.set_command(CmdFeature("cmd"))
        ll = ListFiles("ll")
        ll.set_file_model(fm)
        load_file = LoadFile('load')
        load_file.set_file_model(fm)
        load_file.set_graph_creator(dg)
        ced.set_command(ll)
        ced.set_command(load_file)
        ar = Alwaysrun()
        li = ListElement('l')
        li.set_renderer(l)
        ar.set_command(li)
        ced.set_command(ar)
        ced.display()