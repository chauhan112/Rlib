from modules.mobileCode.terminal_explorer import AdvanceCommandExplorer, AdvanceNode, Main as TExpMain
from modules.FileAnalyser.FileAnalyser import Creator, ICreator
from ancient.InterfaceDB import EmptyClass
from useful.OpsDB import IOps

class ICommand:
    def callback(self):
        pass
class TerminalCommand(ICommand):
    def set_func(self, func, params=()):
        self._func = func
        self._params = params
    def callback(self):
        self._func(*self._params)
class NodeMap:
    def __init__(self):
        self._node_map = {}
    def create(self, *p):
        idx = tuple(p[0])
        if idx not in self._node_map:
            a = AdvanceNode()
            a.add_info('pos', idx)
            if len(p) > 1:
                variables = p[1]
                val = variables['value']
                if type(val) != dict:
                    a.add_info('callable', val)
            self._node_map[idx] = a
        return self._node_map[idx]

class GenericDic2Graph(IOps):
    def set_dic(self, dic):
        self._dic = dic
        self._path = []
        self._node_map = {}
    def execute(self):
        self._path.clear()
        self._path.append('root')
        root = self._node_creator.create(self._path)
        self._execute(self._dic)
        return root
    def _execute(self, val):
        for key in val:
            value = val[key]
            node = self._node_creator.create(self._path, locals())
            node.children.append(self._node_creator.create(self._path + [key], locals()))
            self._path.append(key)
            if type(value) == dict:
                self._execute(value)
            self._path.pop()
    def set_node_creator(self, creator: ICreator):
        self._node_creator = creator
    def export(self, name):
        if not name.endswith(".pkl"):
            name += '.pkl'
        SerializationDB.pickleOut(self._node_map, name)

class Main:
    def cmd_explorer(dic):
        nm = NodeMap()
        c = Creator()
        c.set_creator_class(nm.create)
        c.set_setproperty_func(ExampleCommand._prpt)
        dg = GenericDic2Graph()
        dg.set_dic(dic)
        dg.set_node_creator(c)
        root = dg.execute()
        ace = AdvanceCommandExplorer()
        ace.set_root(root)
        ace.set_on_file_selected(ExampleCommand._file_selected_func)
        TExpMain.explorer(ace)
class ExampleCommand:
    def _make_command(func, params=()):
        g = TerminalCommand()
        g.set_func(func, params)
        return g
    def _prpt(cls: AdvanceNode):
        cls.set_name_func(lambda x: x.get_info()['pos'][-1])
        return cls
    def _file_selected_func(parent, a: AdvanceNode):
        cmd: ICommand = a.get_info()['callable']
        cmd.callback()
    def example1():
        from useful.jupyterDB import jupyterDB
        dic = {
            'basics': {
                'start-up': {
                    'home': ExampleCommand._make_command(jupyterDB.startUp().home),
                    'office': ExampleCommand._make_command(jupyterDB.startUp().office)
                }
            }
        }
        Main.cmd_explorer(dic)