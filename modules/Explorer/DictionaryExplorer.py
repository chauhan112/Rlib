from InterfaceDB import EmptyClass
from modules.Explorer.personalizedWidgets import WidgetsIpyExplorerDisplayer
from modules.Explorer.model import IExplorer
from OpsDB import IOps
class Node:
    def __init__(self, idd):
        self.idd = idd
        self.children = []
        self.parent = None
        self.extra_info = EmptyClass()
    @property
    def value(self):
        return f"node:{self.idd}, d: {self.extra_info.depth}"
class NodeTreeExplorer(IExplorer):
    def __init__(self, root = None):
        self._pos = [root]
    def cd(self, key):
        current = self._pos[-1]
        for c in current.children:
            if str(c.value) == key:
                self._pos.append(c)
                break
    def goBack(self):
        if len(self._pos) > 1:
            self._pos.pop()
    def dirList(self):
        current = self._pos[-1]
        folders = []
        files = []
        for c in current.children:
            if len(c.children):
                folders.append(c.value)
            else:
                files.append(c.value)
        return sorted(folders), sorted(files)
class Graph2TreeNodeMaker(IOps):
    def __init__(self, graph, first_key):
        self._graph = graph
        self._node_map = {}
        self._root = first_key
    def execute(self):
        n = self._get_node(self._root)
        visited = set([self._root])
        unvisited = set(self._graph[self._root]).difference(visited)
        self._add_children(unvisited, visited, n)
        return n
    def _get_node(self, key):
        if key not in self._node_map:
            n = Node(key)
            self._node_map[key] = n
            n.extra_info.depth = 0
        return self._node_map[key]
    def _add_children(self, nebors, visited, parent):
        for neb in nebors:
            n = self._get_node(neb)
            n.parent = parent
            parent.children.append(n)
            visited.add(neb)
            self._update_depth(n)
        for neb in nebors:
            neb_nebors = set(self._graph[neb])
            self._add_children(neb_nebors.difference(visited), visited, self._get_node(neb))
    def _update_depth(self, node):
        depth = 0
        while True:
            if node.extra_info.depth < depth:
                node.extra_info.depth = depth
                break
            parent = node.parent
            if parent is None:
                break
            node = parent
            depth += 1
class Graph2NodeTreeMakerBreadthFirstSearch(IOps):
    def __init__(self, graph, first):
        self._graph = graph
        self._root = first
        self._node_map = {}
        self._parent_map = {}
    def execute(self):
        visited = set([])
        stack = [self._root]
        self._parent_map[self._root] = None
        while len(stack) > 0:
            key = stack.pop()
            visited.add(key)
            n = self.get_node(key)
            nebors = self._graph[key]
            for neb in nebors:
                if neb not in self._parent_map:
                    self._parent_map[neb] = n
                if neb not in visited:
                    stack.insert(0, neb)
        self._update_parent()
        self._update_depth_of_all_nodes()
        return self._node_map[self._root]
    def _update_parent(self):
        for key in self._parent_map:
            parent = self._parent_map[key]
            child = self._node_map[key]
            if parent is not None:
                parent.children.append(child)
            child.parent = parent
    def _update_depth_of_all_nodes(self):
        for key in self._parent_map:
            node = self._node_map[key]
            self._update_parent_depth(node, node.extra_info.depth + 1)
    def _update_parent_depth(self, node, val):
        parent = node.parent
        if parent is not None:
            if val >= parent.extra_info.depth:
                parent.extra_info.depth = val
                self._update_parent_depth(parent, val+1)
    def get_node(self, key):
        if key not in self._node_map:
            n = Node(key)
            self._node_map[key] = n
            n.extra_info.depth = 0
        return self._node_map[key]
class Main:
    def explore(exp: IExplorer, title = "title", displayit=True):
        wied = WidgetsIpyExplorerDisplayer(title)
        wied.set_explorer(exp)
        if displayit:
            wied.display()
        return wied