import os
from modules.Explorer.model import IExplorer
from modules.GUIs.model import KeyManager
from modules.FileAnalyser.FileAnalyser import Creator, Files2NodeGraph
from modules.mobileCode.GenericExplorer import ListRenderer
from modules.mobileCode.tree_ops import CmdExplorerDisplayer, ListElement, Alwaysrun, Goback, ElementSelected, GCommand
class IExplorerNode:
    def get_children(self):
        raise NotImplementedError("abstract method")
    def get_displayable_name(self) -> str:
        raise NotImplementedError("abstract method")
    def get_info(self) -> dict:
        raise NotImplementedError("abstract method")
    def is_folder(self) -> bool:
        raise NotImplementedError("abstract method")
class AdvanceNode(IExplorerNode):
    def __init__(self, *param):
        self._params = param
        self._info = {}
        self.children = []
    def get_children(self) -> list[IExplorerNode]:
        return list(self.children)
    def add_info(self, key, value):
        self._info[key] = value
    def get_info(self) -> dict:
        return self._info
    def set_name_func(self, func):
        self._func = func
    def get_displayable_name(self):
        return self._func(self)
    def is_folder(self):
        return len(self.children) != 0
class AdvanceCommandExplorer(IExplorer):
    def __init__(self):
        self._km = KeyManager()
        self.set_on_folder_selected(lambda pa, ele: None)
        self.set_on_file_selected(lambda pa, ele: None)
        self.set_sorting_func(lambda arr: arr)
        self._combined = None
    def cd(self, key: int):
        if key >= len(self._combined):
            print("[ERROR] :: out of index")
            return
        element = self._combined[key]
        if element.is_folder():
            self._cur_pos.append(element)
            self._on_folder_select(self, element)
            self._km.set_keys(element.get_children())
        else:
            self._on_file_select(self, element)
    def dirList(self):
        keys = self._km.getKeysForCurrentPageIndex()
        folders = []
        files = []
        for k in keys:
            if k.is_folder():
                folders.append(k)
            else:
                files.append(k)
        folders, files = self._sort_func(folders), self._sort_func(files)
        self._combined = [*folders, *files]
        folders = list(map(lambda x: x.get_displayable_name(), folders))
        files = list(map(lambda x: x.get_displayable_name(), files))
        return folders, files + [f"...{self._km.currentPageIndex}:t={self._km.totalNrOfPages()}"]

    def set_on_file_selected(self, func):
        self._on_file_select = func
    def set_on_folder_selected(self, func):
        self._on_folder_select = func
    def set_sorting_func(self, func):
        self._sort_func = func
    def next_section(self):
        if self._km.currentPageIndex < self._km.totalNrOfPages():
            self._km.currentPageIndex += 1
    def prev_section(self):
        if self._km.currentPageIndex > 0:
            self._km.currentPageIndex -= 1
    def set_root(self, root: IExplorerNode):
        self._cur_pos = [root]
        self._root = root
        self._km.set_keys(root.get_children())
    def goBack(self):
        if len(self._cur_pos)  > 1:
            self._cur_pos.pop()
            cur = self._cur_pos[-1]
            self._km.set_keys(cur.get_children())
class NextPage(GCommand):
    def callback(self, parent):
        exp: AdvanceCommandExplorer = parent.get_explorer()
        params = list(map(int, self.params[1:]))
        if len(params) == 0:
            exp.next_section()
        elif params[0] < 0:
            exp.prev_section()
        elif params[0] < exp._km.totalNrOfPages():
            exp._km.currentPageIndex = params[0]

    def get_help(self):
        return f"{self.idd} -> jump to page(nn val) or next page(nn) or prev page(nn -1)"
class Main:
    def os_explorer(path: str):
        from useful.FileDatabase import File
        fng = Files2NodeGraph()
        c = Creator()
        c.set_creator_class(AdvanceNode)
        c.set_setproperty_func(Main._prop_func)

        fng.set_path(path)
        fng.set_node_creator(c)
        graph = fng.execute()
       
        ace = AdvanceCommandExplorer()
        ace.set_sorting_func(lambda arr: sorted(arr, key=lambda x: x.get_displayable_name()))
        ace.set_root(graph[fng._root])
        ace.set_on_file_selected(lambda p, el: File.openFile(el.get_info()['path']))
        Main.explorer(ace)

    def _prop_func (cls: AdvanceNode):
        cls.add_info("path", cls._params[0])
        cls.set_name_func(lambda parent: os.path.basename(parent._info['path']))
        return cls
    def explorer(exp: AdvanceCommandExplorer):
        ced = CmdExplorerDisplayer()
        ced.set_command(Goback('b'))
        ced.set_command(NextPage('nn'))
        ele = ElementSelected()
        ced.set_command(ele)
        l = ListElement('l')
        l.set_renderer(ListRenderer())
        ar = Alwaysrun()
        ar.set_command(l)
        ced.set_explorer(exp)
        ced.set_command(ar)
        ced.display()
