from useful.Path import Path
from useful.FileDatabase import File
from ancient.DataStorageSystem import LocalTree, FolderTable, UrlsTable,NotesTable
import os
from useful.LibsDB import LibsDB
from useful.RegexDB import RegexDB
from useful.htmlDB import htmlDB
from ancient.CodeDB import LocModel, CodeDB
from useful.SerializationDB import SerializationDB

class Bachelorarbeit:
    dbPath = None
    binPath = None
    def reprocessCloudPath(path):
        currentCloudPath = RegexDB.regexSearch(".*cloud", path)[0]
        return path.replace(currentCloudPath, LibsDB.cloudPath())
    def explorer():
        from useful.ExplorerDB import ExplorerDB 
        from useful.jupyterDB import jupyterDB
        from useful.TreeDB import TreeDB
        ba = Bachelorarbeit.reprocessCloudPath(Bachelorarbeit.path().getContentOfThisTable()['bachelorArbeit docs'])
        exp = ExplorerDB.osFileExplorer(ba)
        exp.setFileDisplayer("ipynb", lambda x: TreeDB.openWebLink(jupyterDB.localIpyLink(x, False)))
        return exp

    def path():
        ft = FolderTable("ba", Bachelorarbeit.dbPath)
        return ft

    def links():
        ut = UrlsTable("ba", Bachelorarbeit.dbPath)
        return ut

    def localTree():
        miniForest = Path.joinPath(Bachelorarbeit.binPath)
        return LocalTree(miniForest)

    def docs():
        class Temp:
            def seminarPaper():
                paths = Path.paths().getContent()
                seminarPath = paths['seminar arbeit rwth']
                File.openFile(Bachelorarbeit.reprocessCloudPath(Path.joinPath(seminarPath, 'operations', 'artifacts', 'seminar paper', 
                                            'V3_SeminarPaper14Dec.pdf')))
            
            def plan():
                Temp._openRelPath(Path.joinPath('ops', 'plan', 'plan_v5.pdf'))

            def _openRelPath(path):
                paths = Path.paths().getContent()
                bpath = paths['Bachelorarbeit']
                File.openFile(Bachelorarbeit.reprocessCloudPath(Path.joinPath(bpath, path)))
        return Temp

    def cmd():
        from useful.OpsDB import OpsDB
        from useful.SearchSystem import DicSearchEngine

        dic = {
            'otherApps': r"C:\Users\rajac\Desktop\gittest\project\otherBranch\Micapd",
            'newDesign': r"C:\Users\rajac\Desktop\gittest\bachelorArbeit\Redesign",
            "master": r"C:\Users\rajac\Desktop\gittest\project\MICpad",
            'mvc2' : r"C:\Users\rajac\Desktop\gittest\project\MICpadNew\micpadnew"
        }
        s = DicSearchEngine(dic)
        s._runCallback = lambda key, path: OpsDB.cmd().onthread(['C:', f"cd {path}", "start"])
        return s

    def notes():
        nt = NotesTable('redesign', Bachelorarbeit.dbPath)
        return nt
        
        
class Lexer:
    path = r"C:\Users\rajac\Desktop\gittest\bachelorArbeit\Redesign"
    def files():
        class Temp:
            def headers():
                return Path.filesWithExtension("h",Lexer.path)
            def cpp():
                return Path.filesWithExtension("cpp",Lexer.path)
            def both():
                return Temp.cpp() + Temp.headers()
        return Temp
    def classes():
        class Temp:
            def fromContent(content):
                clases = RegexDB.regexSearch("(class|struct) .*\n", content)
                classes = set(map(lambda x: RegexDB.replace(" +",x, lambda x: " "),clases))
                classes = set(map(lambda x: RegexDB.replace("(class|struct|public)|[{;]|( +)\|\n",x, lambda x: ""),
                                  classes))
                classes = set(map(lambda x: x.strip().replace(":",","),classes))
                classes = list(map(lambda x: x.split(","),classes))
                return classes
            def allClasses(files):
                cleas = []
                for f in files:
                    cleas += Temp.fromContent(File.getFileContent(f))
                classesTable = []
                i=1
                for cls in cleas:
                    if(cls[0] in ["QTextDocument"]):
                        continue
                    if(len(cls) == 1):
                        classesTable.append([i, cls[0],"--"])
                    else:
                        classesTable.append([i, cls[0],cls[1]])
                    i+=1
                return classesTable
            def displayTable():
                classes = [['sn', "class", "parent class"]] + Temp.allClasses(Lexer.files().both())
                return htmlDB.displayTableFromArray(classes)

        return Temp
    def parse(path =None, pklFile = None, classesWithPklFile = None):
        if(pklFile is not None):
            l = LocModel()
            l.load(pklFile)
            return l
        oldPath = Lexer.path
        Lexer.path = path
        dataModel = CodeDB.analyseComplexityAndLOC(Lexer.files().both())
        if(classesWithPklFile is not None):
            clsWithParents = SerializationDB.readPickle(classesWithPklFile)
            for cls in clsWithParents:
                dataModel.classModel.content[cls]['parent'] = clsWithParents[cls]
        Lexer.path = oldPath
        return dataModel
        
import ipywidgets as widgets
class ClassMapperWidget:
    def __init__(self, contentFile = None):
        self.content = {}
        if(contentFile is not None):
            self.content = SerializationDB.readPickle(contentFile)
        self.defineWidgets()
        self.mainDiagrm = self.getMainDiagram()
        self.connectCallback()
        display(self.mainDiagrm)
    
    def defineWidgets(self):
        self._old = widgets.Dropdown(description="old", options =old_dm.classModel.read().allClasses() )
        self._new = widgets.Dropdown(description="new", options =new_dm.classModel.read().allClasses() )
        self._mapBtn = widgets.Button(description="map")
    
    def getMainDiagram(self):
        return widgets.HBox([self._new, self._old, self._mapBtn])
    
    def connectCallback(self):
        self._mapBtn.on_click(self.mapAdd)
        self._new.observe(self.newSelected,names="value")

    def mapAdd(self, bth):
        self.content[self._new.value] = self._old.value
        
    def newSelected(self, change):
        newVal = change['new']
        if(newVal in self.content):
            self._old.value = self.content[newVal]
        else:
            self._old.value = self.getnearVal(newVal)
    
    def getnearVal(self,mainVal):
        d = ''
        dis = None
        for val in self._old.options:
            thisDis = distance(mainVal, val)
            if(dis is None):
                dis = thisDis
                continue
            if(thisDis < dis):
                dis = thisDis
                d = val
        return d
            