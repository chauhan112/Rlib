from modules.FileAnalyser.FileAnalyser import DynamicNodeExplorer
from modules.Explorer.personalizedWidgets import IExplorerDisplayer
from modules.Explorer.model import IExplorer
from modules.mobileCode.tree_ops import IRenderer
import os
from modules.FileAnalyser.FileAnalyser import GNode
from modules.mobileCode.tree_ops import GCommand

class DNEWithCdAtIndex(IExplorer):
    def __init__(self, root: GNode):
        self._root = root
        self.dynamic_exp = DynamicNodeExplorer(root)

    def cd(self, key):
        if type(key) == int:
            self.cd_at_index(key)
        else:
            self.dynamic_exp.cd(key)
    def cd_at_index(self, index):
        if index >= len(self.dynamic_exp._current_map):
            print("index out error")
            return
        key = list(self.dynamic_exp._current_map.keys())[index]
        self.cd(key)

    def dirList(self):
        return self.dynamic_exp.dirList()
    def goBack(self):
        self.dynamic_exp.goBack()

class ListRenderer(IRenderer):
    def render(self):
        folders, files = self._exp.dirList()
        j = -1
        for j, fold in enumerate(folders):
            self._printFormatted('>', j, fold)
        for i, file in enumerate(files):
            self._printFormatted('|', j+i+1, file)

    def _printFormatted(self, pre, i, word):
        from WordDB import WordDB
        forma = WordDB.formatting()
        print(pre + f'{forma.integer(i,3)}. {forma.word(word, 15)}')

    def set_explorer(self, exp):
        self._exp = exp
class NumberView(GCommand):
    def callback(self, parent):
        exp = parent.get_explorer()
        exp.dynamic_exp.set_sorted_func(
            lambda xList: sorted(xList, key=lambda x: x.extra_info.number, reverse=True))
        exp.dynamic_exp.set_displayer_func(
            lambda x: os.path.basename(x.idd) + f" - {x.extra_info.number}")
    def get_help(self):
        return f"{self.idd} -> view number info"

class DepthView(GCommand):
    def callback(self, parent):
        exp = parent.get_explorer()
        exp.dynamic_exp.set_sorted_func(
            lambda xList: sorted(xList, key=lambda x: x.extra_info.depth, reverse=True))
        exp.dynamic_exp.set_displayer_func(
            lambda x: os.path.basename(x.idd) + f" - {x.extra_info.depth}")
    def get_help(self):
        return f"{self.idd} -> view depth info"

class SizeView(GCommand):
    def callback(self, parent):
        from modules.FileAnalyser.FileAnalyser import FileAnalyser
        exp = parent.get_explorer()
        exp.dynamic_exp.set_sorted_func(
            lambda xList: sorted(xList, key=lambda x: x.extra_info.size, reverse=True))
        viewfunc = lambda x: FileAnalyser.sizeb(x.extra_info.size)
        exp.dynamic_exp.set_displayer_func(
            lambda x: os.path.basename(x.idd) + f" - {viewfunc(x)}")
    def get_help(self):
        return f"{self.idd} -> view size info"

class NoInfoView(GCommand):
    def callback(self, parent):
        exp = parent.get_explorer()
        exp.dynamic_exp.set_sorted_func(lambda xList: sorted(xList, 
            key=lambda x: os.path.basename(x.idd)))
        exp.dynamic_exp.set_displayer_func(lambda x: os.path.basename(x.idd))
    def get_help(self):
        return f"{self.idd} -> view no info"

class SaveInfo(GCommand):
    def callback(self, parent):
        if len(self.params) > 1:
            name = self.params[-1]
            exp = parent.get_explorer()
            exp.dynamic_exp.export(name)
    def get_help(self):
        return f"{self.idd} -> export root graph nodes as tree: save filename"

class LoadFromFile(GCommand):
    def callback(self, parent):
        if len(self.params) < 2:
            return
        path = self.params[-1]
        if os.path.exists(path):
            exp = parent.get_explorer()
            exp.dynamic_exp.load(path)
        else:
            print("path does not exists")
            
    def get_help(self):
        return f"{self.idd} -> load from file: load f"

class Main:
    def explorer(path = None, root = None, display = True) -> IExplorerDisplayer:
        from modules.mobileCode.tree_ops import CmdExplorerDisplayer, ListElement,  \
            Alwaysrun, Goback, ElementSelected
        from modules.FileAnalyser.FileAnalyser import FileAnalyser
        ced = CmdExplorerDisplayer()
        if path is not None:
            _, root = Main.get_files_graph().from_path(path)
        sort_func = lambda x: x.extra_info.size
        dne = DNEWithCdAtIndex(root)
        dne.dynamic_exp.set_sorted_func(lambda xList: sorted(xList, 
            key=lambda x: os.path.basename(x.idd)))
        dne.dynamic_exp.set_displayer_func(
            lambda x: os.path.basename(x.idd))
        ced.set_command(Goback('b'))
        ele = ElementSelected()
        ced.set_command(ele)
        l = ListElement('l')
        l.set_renderer(ListRenderer())
        ar = Alwaysrun()
        ar.set_command(l)
        ced.set_explorer(dne)
        if not display:
            return ar, ced
        ced.set_command(ar)
        ced.display()

    def get_files_graph():
        class Temp:
            def from_path(path):
                from modules.FileAnalyser.FileAnalyser import GFiller, SizeFillerStrategy, NumberFillerStrategy
                from DataStructure import MaxDepthInverseCalculator
                from Path import Path
                gr, root = Temp.from_files(Path.getFiles(path, True))
                sf = GFiller()
                sf.set_graph_root(root)
                sf.set_filling_strategy(SizeFillerStrategy())
                sf.fill()
                sf.set_filling_strategy(NumberFillerStrategy())
                sf.fill()
                MaxDepthInverseCalculator(root).execute()
                return gr, root

            def from_file_nodes_pickle(pkl):
                from SerializationDB import SerializationDB
                val = SerializationDB.readPickle(pkl)
                nodes = val['nodes']
                root = nodes[val['root']]
                return nodes, root
            def from_dynamic_explorer_pickle(pkl):
                from SerializationDB import SerializationDB
                Main.explorer(root=SerializationDB.readPickle(pkl))
            def from_files(files):
                from modules.FileAnalyser.FileAnalyser import Creator, GNode, Files2NodeGraph
                cr = Creator()
                cr.set_creator_class(GNode)
                fng = Files2NodeGraph()
                fng.set_files(files)
                fng.set_node_creator(cr)
                gr = fng.execute()
                root = gr[fng._root]
                return gr, root
        return Temp