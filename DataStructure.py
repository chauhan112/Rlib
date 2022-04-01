class DataStructure:
    def twoDarray2CSV(twoDimArray, name):
        import csv
        if( not name.endswith(".csv") ):
            name = name + ".csv"
        if(not DataStructure.not2dArray(twoDimArray)):
            raise IOError("not consistent 2d array")
        with open(name,"w+") as my_csv:
            csvWriter = csv.writer(my_csv,delimiter=',')
            csvWriter.writerows(twoDimArray)
    def nestedNamespace(dic):
        from types import SimpleNamespace
        class NestedNamespace(SimpleNamespace):
            def __init__(self, dictionary, **kwargs):
                super().__init__(**kwargs)
                for key, value in dictionary.items():
                    if isinstance(value, dict):
                        self.__setattr__(key, NestedNamespace(value))
                    else:
                        self.__setattr__(key, value)
        return NestedNamespace(dic)
    def namespace(dic):
        from types import SimpleNamespace
        return SimpleNamespace(**dic)
    def not2dArray(arr):
        dim = 0
        for i,val in enumerate(arr):
            if(i == 0):
                dim = len(val)
            if(dim != len(val)):
                return False
        return True
    def append2CSV(rows, name):
        import csv
        with open(name, 'a') as f:
            writer = csv.writer(f)
            for row in rows:
                writer.writerow(row)
    def readCSV(name):
        from IPython.display import display
        from htmlDB import htmlDB
        import csv
        class MyCSV:
            def __init__(self,path):
                self.content = self.read()
            def read(self):
                rows = []
                with open(name) as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        rows.append(row)
                return rows
            def head(self, n = 5):
                if(len(self.content) > n):
                    return htmlDB.displayTableFromArray(self.content[:n])
                return htmlDB.displayTableFromArray(self.content)
            def tail(self, n = 5):
                if(len(self.content) > n):
                    return htmlDB.displayTableFromArray(self.content[-n:])
                return htmlDB.displayTableFromArray(self.content)
        return MyCSV(name)
    def readCSVWithPanda(path):
        import pandas as pd
        return pd.read_csv(path)
    def deletePandasColumns(columns,pdData):
        if( type(columns ) == str):
            columns = [columns]
        return (pdData.drop(columns,axis = 1 ))
    def graph(connections, directed = False):
        """
        connections = [(1,2),(1,3), (2,4), (3,4)]
        """
        import pprint
        from collections import defaultdict
        class Graph:
            """ Graph data structure, undirected by default. """
            def __init__(self, connections, directed=False):
                self._graph = defaultdict(set)
                self._directed = directed
                self.add_connections(connections)
            def add_connections(self, connections):
                """ Add connections (list of tuple pairs) to graph """
                for node1, node2 in connections:
                    self.add(node1, node2)
            def add(self, node1, node2):
                """ Add connection between node1 and node2 """
                self._graph[node1].add(node2)
                if not self._directed:
                    self._graph[node2].add(node1)
            def remove(self, node):
                """ Remove all references to node """
                for n, cxns in self._graph.items():  # python3: items(); python2: iteritems()
                    try:
                        cxns.remove(node)
                    except KeyError:
                        pass
                try:
                    del self._graph[node]
                except KeyError:
                    pass
            def is_connected(self, node1, node2):
                """ Is node1 directly connected to node2 """
                return node1 in self._graph and node2 in self._graph[node1]
            def find_path(self, node1, node2, path=[]):
                """ Find any path between node1 and node2 (may not be shortest) """
                path = path + [node1]
                if node1 == node2:
                    return path
                if node1 not in self._graph:
                    return None
                for node in self._graph[node1]:
                    if node not in path:
                        new_path = self.find_path(node, node2, path)
                        if new_path:
                            return new_path
                return None
            def __str__(self):
                return '{}({})'.format(self.__class__.__name__, dict(self._graph))
        return Graph(connections, directed)
class DataStructure_test:
    def nestedNamespaceTest():
        nested_namespace = {
            'parent': {
                'child': {
                    'grandchild': 'value'
                }
            },
            'normal_key': 'normal value',
        }
        k = DataStructure.nestedNamespace(nested_namespace)
        assert(k.parent.child.grandchild == 'value')
    def namespaceTest():
        d = {'key1': 'value1', 'key2': 'value2'}
        k = DataStructure.namespace(d)
        assert(k.key1 == d['key1'])
class TreeNode:
    def __init__(self,value, left = None, right = None):
        self.left  = left
        self.right = right
        self.value = value
class BinTreeInterface:
    def __init__(self):
        self.root = None
        self.pointer = None
    def addNew(self, nodeVal):
        if(self.root is None):
            self.root = TreeNode(nodeVal)
        else:
            self._addNew(self.root, nodeVal)
    def _addNew(self, node, val):
        if(self.compare(node.value, val)):
            pass
        pass
    def compare(self, node1, node2):
        # return true or false (binary values)
        raise NotImplementedError("overload this method")
    def deleteNode(self, nodeVal):
        pass
    def updateNode(self, oldNodeValue, newNodeValue):
        self.deleteNode(oldNodeValue)
        self.addNew(newNodeValue)
class TreeIterator:
    def preOrderIterator(self):
        pass
    def inOrderIterator(self):
        pass
    def postOrderIterator(self):
        pass
from OpsDB import IOps
from modules.Explorer.DictionaryExplorer import Node
class MaxDepthInverseCalculator(IOps):
    def __init__(self, root: Node):
        self._root = root
    def execute(self):
        self._root.extra_info.depth = self._assign(self._root)
    def _assign(self, node):
        if len(node.children) == 0:
            node.extra_info.depth = 0
            return 0
        depths = []
        for child in node.children:
            child.extra_info.depth = self._assign(child)
            depths.append(child.extra_info.depth)
        return max(depths) + 1