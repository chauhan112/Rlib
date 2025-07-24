from Database import Database
from WidgetsDB import WidgetsDB
import ipywidgets as widgets
from SerializationDB import SerializationDB
from IPython.display import display, HTML

class Separ:
    def getAlltext(file):
        breaker ="<53ea7c0>"
        c = breaker.join(File.getFileContent(file).splitlines())
        found = RegexDB.regexSearch(RegexDB.lookAheadAndBehind("<body>", "</body>", ".*"), c)
        if(len(found)> 0):
            c = found[0].replace(breaker, "\n")
        soup = TreeDB.decodeContent(c).soup()
        founds = [str(f) for f in soup.find_all(attrs={"class": "inner_cell"})]
        return founds

    def __init__(self, ques):
        self.report = {}
        self.ques = ques
        self.pos = 0
        self.genrtor = self.fileGenerator()
        self.out = WidgetsDB.outArea()
        self.nextFileInitialize()
        
    def fileGenerator(self):
        for f in self.ques:
            yield f

    def getWidgetsList(self):
        line = lambda intval, x: widgets.HBox([widgets.Label(f"{intval} -----"),widgets.HTML(x), 
                                               WidgetsDB.button(f"{intval}", self.add2Report)])
        return [line(i, val) for i, val in enumerate(self.ques[self.file])]
    
    def add2Report(self, wid):
        self.report[self.file].add(wid.description)
    
    def nextFileInitialize(self):
        self.pos = 0
        self.file = next(self.genrtor)
        self.report[self.file] = set([])
        self.widgetsVal = self.getWidgetsList()
    
    def doNext(self, x):
        if(self.pos + 5 < len(self.ques[self.file])):
            self.pos += 5
        else:
            self.nextFileInitialize()
        self.display()
    
    def archive(self, x):
        SerializationDB.pickleOut(self.report, "report.pkl")
    
    def reload(self, x):
        self.report = SerializationDB.readPickle("report.pkl")
    
    def skipFile(self, x):
        self.nextFileInitialize()
        self.display()
    
    def display(self):
        self.out.clear()
        self.out.add2Output(widgets.VBox(self.widgetsVal[self.pos:self.pos+5] + [widgets.HBox([WidgetsDB.button("next", 
                    self.doNext),WidgetsDB.button("archive", self.archive),
                        WidgetsDB.button("reload", self.reload),
                        WidgetsDB.button("skip", self.skipFile)])]))
                                             
class Receiver:
    def __init__(self, contentPath, path2ProcessPickle =None):
        # r = Receiver(r"questions\preprocessing\separated quesions\questions.pkl",
        #     r"questions\preprocessing\receiverBigQues.pkl")
        self.quesDic = {}
        self.content = SerializationDB.readPickle(contentPath)
        if(path2ProcessPickle is not None):
            self._load(path2ProcessPickle)
        self.pos = (0,0)
        self.keys = list(self.quesDic.keys())
        self.out = WidgetsDB.outArea()
        self._selectFileWi = WidgetsDB.dropdown(self.keys, self.selectFile, 15)
        self._txtWi = widgets.Text()
        self._searchRes = WidgetsDB.outArea(False)
        display(widgets.VBox([widgets.HBox([WidgetsDB.button("back", self.back), WidgetsDB.button("next", self.nextVal), 
            self._selectFileWi, self._txtWi, WidgetsDB.button("search", self._search)]), self._searchRes.out]))
        
    def preprocess(self, path2Pickle):
        # pickle to path is layer one path report.pkl
        a = SerializationDB.readPickle(path2Pickle)
        a = {key: sorted([int(val) for val in a[key]]) for key in a}
        for key in a:
            rep = a[key]
            self.quesDic[key] = []
            for i in range(1, len(rep)):
                self.quesDic[key].append((rep[i-1],rep[i]))
        self.keys = list(self.quesDic.keys())
        
    def totalNumberOfQuesions(self):
        return sum([len(self.quesDic[k]) for k in self.quesDic])
    
    def back(self, x):
        a, b = self.pos
        if(b-1 < 0):
            if(a-1 >= 0):
                a = a -1
                b = len(self.quesDic[self.keys[a]]) - 1
        else:
            b -= 1
        self._update(a,b)
        
    def _update(self, a, b):
        self.pos = (a, b)
        self.display()
        self._selectFileWi.value = self.keys[a]
        self._searchRes.clear()
    
    def _search(self, x):
        self._searchRes.clear()
        self._searchRes.add2Output(DataScience.docs().solutions().htmlForm().search(self._txtWi.value))
    
    def nextVal(self, x):
        a, b = self.pos
        if(b+1 >= len(self.quesDic[self.keys[a]])):
            if(a+1 < len(self.keys)):
                a = a + 1
                b = 0
        else:
            b += 1
        self._update(a,b)
        
    def selectFile(self, x):
        file = x['new']
        a = 0
        for i, key in enumerate(self.keys):
            if(key==file):
                a = i
        self.pos = (a,0)
        self.display()
        
    def archive(self, path=None):
        if(path is None):
            path = "receiverQues.pkl"
        SerializationDB.pickleOut(self.quesDic, path)
    
    def merge(self, q1, q2):
        pass

    def display(self):
        self.out.clear()
        i, j = self.pos
        key = self.keys[i]
        a, b = self.quesDic[key][j]
        self.out.add2Output(HTML("".join(self.content[key][a:b])))
    
    def _load(self, path2ProcessPickle):
        self.quesDic = SerializationDB.readPickle(path2ProcessPickle)

class CategorizerLayout:
    def __init__(self):
        self._quesOpt = dropdown(list(ques.keys()),self.assignMax,sizeInPercent = 15)
        self._maxLab = widgets.Label(str(len(ques[list(ques.keys())[0]])))
        self._indexNr = widgets.IntText( )
        
        self.out = WidgetsDB.outArea()
        self.mainLayout = self.makeLayout()
        display(self.mainLayout)
    
    def assignMax(self,x):
        self._maxLab.value = str(len(ques[x['new']]))
    
    def makeLayout(self):
        row1 = widgets.HBox([widgets.Label("Question::"), self._quesOpt, self._maxLab, 
                             self._indexNr, WidgetsDB.button("show", callbackFunc= self.displayQuesion)])
        row2 = widgets.HBox([widgets.Label("Libraries"), widgets.Text(), WidgetsDB.button("add")])
        row3 = widgets.HBox([widgets.Label("Functions"), widgets.Text(), WidgetsDB.button("add")])
        row4 = widgets.HBox([widgets.Label("Knowledge"), widgets.Text(), WidgetsDB.button("add")])
        row5 = widgets.HBox([widgets.Label("difficulty level"), widgets.IntText(), WidgetsDB.button("update")])
        row6 = widgets.HBox([widgets.Label("precision"), widgets.IntText(), WidgetsDB.button("update")])
        box1 =  widgets.VBox([row1, row2, row3, row4, row5, row6])
        return box1
    
    def displayQuesion(self, x):
        self.out.clear()
        file = self._quesOpt.value
        index = self._indexNr.value
        self.out.add2Output(HTML(ques[file][index]))

class DataScience:
    def _pathDB(filepaths):
        from SearchSystem import FilePathsSearchEngine
        return FilePathsSearchEngine(filepaths)
    def getPath():
        from Path import FrequentPaths
        return FrequentPaths.pathAsDic()['data science']
    def links():
        from ancient.DataStorageSystem import UrlsTable
        ut = UrlsTable("data science")
        return ut
    
    def docs():
        from Path import Path
        class Temp:
            def contentDB():
                return Database.pdfDB(Temp._files())
            def solutions():
                class Temp:
                    def _files(ext ="html"):
                        path = Path.joinPath(DataScience.getPath(), r"ops\exam_prep\solutions")
                        return Path.filesWithExtension(ext, path)
                    def htmlForm():
                        from FileDatabase import File
                        return Database.textFilesDB(Temp._files(), callbackFunc= lambda file, lineNr: File.openFile(file))
                    def pdfForm():
                        return Database.pdfDB(Temp._files("pdf"))
                return Temp
                
            def _files():
                p = Path.joinPath(DataScience.getPath(), "docs")
                return Path.filesWithExtension("pdf", p)
            
            def pathDB():
                return DataScience._pathDB(Temp._files()) 
        return Temp

    def exercises():
        from Path import Path
        from FileDatabase import File
        class Temp:
            def openExplorer(showContent = False):
                from ExplorerDB import ExplorerDB
                from jupyterDB import jupyterDB
                from TreeDB import TreeDB
                exp = ExplorerDB.osFileExplorer(Path.joinPath(DataScience.getPath(), "ops"))
                exp.setFileDisplayer("html", File.openFile)
                if(not showContent):
                    exp.setFileDisplayer("ipynb", lambda x: TreeDB.openWebLink(jupyterDB.localIpyLink(x, False)))
                return exp
            def contentDB():
                return Database.textFilesDB(Temp._files())
            def _files():
                return Path.filesWithExtension("ipynb",Path.joinPath(DataScience.getPath(), "ops"))
        return Temp