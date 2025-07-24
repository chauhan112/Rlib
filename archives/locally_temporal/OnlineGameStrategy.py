class Graph:
    def __init__(self, arr,  vertices= set([]), edges= {}):
        """
        vertices =  list of position e.g [(1,2), (1,2)]
        edges = dict e.g {(3,2):{(2,2): 3,(3,1): 1 }} # (3,2) => Vertex key (3,2) ---3---> (2,2)
        """
        self._vertices = vertices
        self._edges = edges
        self.arr = arr
    def addVertex(self, vertex):
        self._vertices.add(vertex)
    
    def addEdge(self, start, end, directed = False):
        self._addEdge(start, end)
        if( not directed):
            self._addEdge(end, start)
        
    def _addEdge(self, start, end):
        if(start not in self._edges):
            self._edges[start] = {}
        a, b = end
        self._edges[start][end] = self.arr[a][b]
        
    def getVertices(self):
        return self._vertices
    
    def getEdges(self):
        return self._edges
        
class GInput:
    def __init__(self):
        self.comment = ""
        self.size = ()
        self.start = None
        self.end = None
        self.arr = None
    
    def getGraph(self) -> Graph:
        g = Graph(self.arr)
        for i, row in enumerate(self.arr):
            for j,val in enumerate(row):
                g.addVertex((i,j))
                if(i-1 >= 0):
                    g.addEdge((i,j), (i-1, j))
                if(j-1 >= 0):
                    g.addEdge((i,j), (i, j-1))
        return g

class IReader:
    def read(self,content) -> GInput:
        raise IOError("Not implemented yet")
        
class ContentParser(IReader):
    def __init__(self, content):
        self._content = content
    
    def parse(self) -> GInput:
        gameParams = GInput()
        lines = self._content.splitlines()
        lines = list(filter(lambda x: len(x) != 0, lines))
        comments, vals = Tools.separeteCommentAndVals(lines)
        gameParams.start, gameParams.end, gameParams.arr = Tools.integerfy(vals)
        gameParams.size = (len(vals), len(vals[0]))
        gameParams.comment = comments[0]
        return gameParams
    
class FileReader(IReader):
    def __init__(self, filePath):
        self._path = filePath
        
    def parse(self) -> None:
        content = Tools.fileContent(self._path)
        c = ContentParser(content)
        return c.parse()

class Tools:
    def isComment(line) -> bool:
        line = line.strip() 
        if(len(line) == 0):
            return True
        return line[0] =="%"
    
    def separeteCommentAndVals(arr)-> tuple:
        
        comm = []
        vals = []
        for line in arr:
            if(Tools.isComment(line)):
                comm.append(line)
            else:
                vals.append(line.split(","))
        return comm, vals
    
    
    def integerfy(arr:list):
        res = []
        start = ()
        end = ()
        for i, row in enumerate(arr):
            newRow = []
            for j,v in enumerate(row):
                k = v.strip()
                if(k == 'S'):
                    start = (i, j)
                    k = 0
                if(k == 'Z'):
                    end = (i, j)
                    k = 0
                newRow.append(int(k))
            res.append(newRow)
        return start, end, res
    
    def fileContent(path: str) -> str:
        from FileDatabase import File
        return File.getFileContentt(path)
    
    def generate_path(parents, start, end):
        path = [end]
        while True:
            key = parents[path[0]]
            path.insert(0, key)
            if key == start:
                break
        return path
    
    def add(p1 , p2):
        a, b = p1
        c, d = p2
        return (a+c, b+d)
    
    def shift(paths):
        return list(map(lambda x: Tools.add(x, (1,1)), paths))
    
    def generatePathNShift(parents, start, end):
        a = Tools.generate_path(parents, start, end)
        return Tools.shift(a)
    
    def changeOrder(paths):
        a = lambda x: (x[1], x[0])
        return [a(x) for x in paths]

from ancient.AIAlgoDB import Dijkstra
    
def main(inp):
    gParams = ContentParser(inp).parse()
    g = gParams.getGraph()
    d = Dijkstra(g.getVertices(), g.getEdges())
    p, vi = d.find_route(gParams.start, gParams.end)
    p =Tools.generatePathNShift(p, gParams.start, gParams.end)
    return Tools.changeOrder(p)


inp = """
    %Waldgebiet mit 7 x 7 Elementen
    10, 10, 10, 10, 10, 10, 10
    10, S, 10, 10, 10, 10, 10
    10, 2, 1, 10, 10, 10, 10
    10, 10, 1, 10, 10, 10, 10
    10, 2, 1, 2, 1, Z, 10
    10, 10, 10, 10, 10, 10, 10
    10, 10, 10, 10, 10, 10, 10
"""
inp2 = """
    %Sumpfgebiet mit 7 x 7 Elementen
    10, 10, 10, 10, 10, 10, 10
    10, S, 2, 2, 10, 10, 10
    10, 1, 10, 2, 2, 2, 10
    10, 1, 1, 10, 10, 1, 10
    10, 2, 1, 2, 9, Z, 10
    10, 10, 10, 10, 10, 10, 10
    10, 10, 10, 10, 10, 10, 10
"""

inp3 = """
    %Flussgebiet mit 20 x 3 Elementen
    S, 1, 1, 10, 10, 10, 1, 1, 1, 10, 10, 1, 1, 1, 10, 10, 1, 1, 1, 10
    10, 10, 1, 10, 10, 10, 1, 10, 1, 10, 1, 1, 10, 1, 1, 10, 1, 10, 1, 1
    10, 10, 1, 1, 1, 1, 1, 10, 1, 1, 1, 10, 10, 10, 1, 1, 1, 10, 10, Z
"""


out1 = [(2, 2), (2, 3), (3, 3), (3, 4), (3, 5), (4, 5), (5, 5), (6, 5)]
out2 = [(2, 2), (3, 2), (4, 2), (4, 3), (5, 3), (6, 3), (6, 4), (6, 5)]
out3 = [(1, 1), (2, 1), (3, 1), (3, 2), (3, 3), (4, 3), (5, 3), (6, 3), 
        (7, 3), (7, 2), (7, 1), (8, 1), (9, 1), (9, 2), (9, 3), (10, 3), 
        (11, 3), (11, 2), (12, 2), (12, 1), (13, 1), (14, 1), (14, 2), (15, 2), 
        (15, 3), (16, 3), (17, 3), (17, 2), (17, 1), (18, 1), (19, 1), (19, 2), (20, 2), (20, 3)]