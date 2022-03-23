from FileDatabase import File
from LibPath import *
import os
from Path import Path
from Database import Database
from SerializationDB import SerializationDB
from LibsDB import LibsDB

class jupyterDB:
    def header(topic = 'headerName', fontFace = "comic sans ms"):
        import random, yaml
        colors = yaml.safe_load(File.getFileContent(Path.joinPath(getPath(),'..', 'resource', "colorNames.yaml")))
        val = "# <font face='{}' color ='{}'>{}</font>".format(fontFace, random.choice(colors),topic)
        print(val)
        from ClipboardDB import ClipboardDB
        ClipboardDB.copy2clipboard(val)
        return val
    
    def syntax():
        class SyntaxDatabase:
            def _path():
                name = "syntax"
                pkl_path = LibsDB.picklePath(name)
                return pkl_path
            def db_ops():
                from types import SimpleNamespace
                pkl_path = SyntaxDatabase._path()
                content = SerializationDB.readPickle(pkl_path)
                res = {}
                for key in content:
                    res[key] = SyntaxDatabase.ops(pkl_path, key)
                return SimpleNamespace(**res)
                
            def ops(pkl, key):
                class Temp:
                    def _set_path(self, pkl_path: str):
                        self._path = pkl_path
                    def _set_root_loc(self, key: str):
                        self._key = key
                    def add(self, key: str, value, overwrite = False):
                        val = self._read(self._key)
                        val[key] = value
                        self._write(val)
                    def delete(self, key: str):
                        val = self._read(self._key)
                        del val[key]
                        self._write(val)
                    def read_keys(self):
                        return list(self._read(self._key).keys())
                    @property
                    def db(self):
                        return Database.syntaxDB(self._read(self._key), self._key)
                    def _read(self, key =  None):
                        content = SerializationDB.readPickle(self._path)
                        if key is None:
                            return content
                        return content[self._key]
                    def _write(self, val):
                        content = self._read()
                        content[self._key] = val
                        SerializationDB.pickleOut(content, self._path)
                t = Temp()
                t._set_path(pkl)
                t._set_root_loc(key)
                return t
        return SyntaxDatabase
        
    def desktop(openFolder = True):
        from menuinst.knownfolders import FOLDERID, get_folder_path
        desk = get_folder_path(FOLDERID.Desktop)[0]
        if(openFolder):
            Path.openExplorerAt(desk)
        return desk

    def createJupyterNotebook(name):
        from NotebookDB import NotebookDB
        cells = SerializationDB.readPickle(LibsDB.picklePath("jupyterDB.pkl"))['createNotebook']
        NotebookDB.createNotebookWithCells(name, cells)
        jupyterDB.localIpyLink(name)

    def libSize():
        pyFiles = Path.filesWithExtension("py", getPath())
        si = Path.getSize(pyFiles)
        from TimeDB import TimeDB
        timeStamp = TimeDB.getTimeStamp() + " " +  ":".join([str(i) for i in TimeDB.today()[1]])
        k = jupyterDB.pickle().read("logs")
        k['libSize'] += [(timeStamp, si)]
        jupyterDB.pickle().write(k, 'logs')
        print(si)

    def codeDumper():
        from NotebookDB import NotebookDB
        class Dumper:
            def __init__(self):
                self.fileName = NotebookDB.outFilename()
                self.path_year = os.path.dirname(self.fileName)
                self._dumper_path = os.path.dirname(self.path_year)
            def folder(self):
                Path.openExplorerAt(self.path_year)
            def summarize(self, _ih = None):
                if(_ih is None and nbName is None):
                    return "NotebookDB.summarizeTheCoding(_ih, theNotebook)"
                NotebookDB.summarizeTheCoding(_ih)
            def name(self, ndaysBefore = 0):
                from TimeDB import TimeDB
                return NotebookDB.outFilename(TimeDB.nDaysBefore(ndaysBefore))
            def db(self,nday = 0, filterFunc = None):
                if(filterFunc is None):
                    basename = os.path.basename(self.name(nday * -1))
                    filterFunc = lambda x: os.path.basename(x) == basename
                from ListDB import ListDB
                files = list(filter(filterFunc, Path.filesWithExtension('pkl', self._dumper_path)))
                vals = {}
                print("files::")
                for f in files:
                    fileBaseName = os.path.basename(f)
                    print(fileBaseName, end=",")
                    vals [fileBaseName] = self.read(f)
                class Temp:
                    def __init__(self, container):
                        self.container = container
                        self.sizeInfo = {key: len(self.container[key]) for key in self.container}
                        lsiting = []
                        for key in self.container:
                            lsiting += self.container[key]
                        self._db = Database.allRunCellDB(_ih = lsiting)

                    def search(self, word, case = False, reg = False):
                        self._db.search(word, case, reg)
                        return self._db

                    def getFileInfo(self, lineNr):
                        i = 0
                        lastkey = None
                        for key in self.sizeInfo:
                            if(i > lineNr):
                                return lastkey
                            i += self.sizeInfo[key]
                            lastkey = key
                return Temp (vals)
            def read(self, filename , where = 'all'):
                if(where == 'all'):
                    checkPlaces = lambda x: True
                else:
                    checkPlaces = lambda x: x in [where]
                k = SerializationDB.readPickle(filename)
                vals = []
                for place in k:
                    if(checkPlaces(place)):
                        for id_ in k[place]:
                            vals += k[place][id_]
                return vals
            def tools(self):
                class Te:
                    def nameStamp2Date(x):
                        basename = os.path.basename(x)
                        dateStamp = basename[:10]
                        return tuple(list(map(int, dateStamp.split("_")))[::-1])
                    def dateCheckCondition(x):
                        from TimeDB import TimeDB
                        return TimeDB.dateCheckCondition(Te.nameStamp2Date(x))
                return Te
        return Dumper()

    def Libs():
        class Lib:
            def __init__(self):
                self.path = getPath()
            def folder(self):
                Path.openExplorerAt(self.path)
            def getLibPath(self, libName):
                return LibsDB.getLibPath(libName)
            def openLib(self,className, equalityTest = False):
                checker = lambda x,y: x in y
                if(equalityTest):
                    checker = lambda x,y: x == y
                if(className.endswith('.py')):
                    File.openFile(self.getLibPath(className))
                File.openFile(LibsDB.libPathOfClass(className, checker=checker))
            def libPath4Class(self,className):
                return LibsDB.libPathOfClass(className)
            def content(self, wordHint, raw = False, checker = lambda x,y: x in y):
                from ModuleDB import ModuleDB
                content = File.getFileContent(LibsDB.libPathOfClass(wordHint, checker))
                if(raw):
                    return content
                return ModuleDB.colorPrint("py", content)
            def size(self):
                jupyterDB.libSize()
            def addPathToFront(self, filename):
                return self.path + os.sep + filename
            def totalNrOfLines(self):
                files = Path.filesWithExtension("py", self.path)
                su = 0
                for f in files:
                    try:
                        su+=lines(f)
                    except:
                        print(f)
                return su
            def plotLibSize(self):
                from GraphDB import GraphDB
                from RegexDB import RegexDB
                from OpsDB import OpsDB

                class LibSizePlot:
                    def __init__(self):
                        name = "logs"
                        self.k = SerializationDB.readPickle(LibsDB.picklePath(name))['libSize']

                    def days(self):
                        p = OpsDB.grouperValues(lambda x: RegexDB.regexSearch("\d{2}\.\d{2}\.\d{4}", x[0])[0], self.k,
                                lambda x: float(x[-1].split(" ")[0]))
                        p = dict({x:p[x][-1] for x in p})
                        return GraphDB.plotX({'size': list(p.values())}, "libSize with days")

                    def changes(self):
                        from ListDB import ListDB
                        p = ListDB.keepUnique(list(map(lambda x: float(x[-1].split(" ")[0]), self.k)), True)
                        return GraphDB.plotX({'size': p}, "libSize with changes")

                    def fitWithDays():
                        import matplotlib.pyplot as plt
                        import numpy as np
                        p = OpsDB.grouperValues(lambda x: RegexDB.regexSearch("\d{2}\.\d{2}\.\d{4}", x[0])[0], k['libSize'],
                                                        lambda x: float(x[-1].split(" ")[0]))
                        p = dict({x:p[x][-1] for x in p})
                        vals = np.array(list(p.values()))
                        x = np.array(list(range(len(vals))))
                        m,b = np.polyfit(x, vals,1)
                        plt.plot(x, vals)
                        plt.plot(x, m*x + b)

                return LibSizePlot()
        return Lib()

    def resource():
        class Res:
            def __init__(self):
                self.dirPath = Path.joinPath(getPath(), "resource")
            def folder(self):
                Path.openExplorerAt(self.dirPath)
            def getPath(self, path):
                if(type(path) == list):
                    path = Path.joinPath(*path)
                Path.joinPath(self.dirPath, path)
        return Res()

    def pickle():
        class Pkl:
            def __init__(self):
                self.dirPath = LibsDB.picklePath()
            def folder(self):
                Path.openExplorerAt(self.dirPath)
            def path(self, name = None):
                return LibsDB.picklePath(name)
            def read(self, name):
                return SerializationDB.readPickle(self.path(name))
            def write(self,data, name):
                SerializationDB.pickleOut(data, LibsDB.picklePath(name))
                return data
            def listDir(self):
                return os.listdir(self.dirPath)
            def search(self,word):
                from PickleCRUDDB import PickleCRUD
                return PickleCRUD.searchInDB(word)
        return Pkl()

    def treeTool():
        from TreeDB import ForestDB, TreeCRUD, TreeDB, TreeSearchEngine
        from TimeDB import TimeDB
        class Tree:
            def __init__(self):
                self.dirPath = ForestDB.getForestPath()
                self.pklPath = TreeCRUD.getPicklePath()
            def waterFall(self, small = True):
                return TreeCRUD.waterFall(small)
            def timeStamp(self):
                return TreeCRUD.textWithBlueBackground(TimeDB.getTimeStamp())
            def copyDB(self, word = None):
                name = "TreeCRUD"
                k = jupyterDB.pickle().read(name)
                return Database.dbSearch(TreeSearchEngine(k), word)

            def folder(self):
                from TreeDB import ForestDB
                Path.openExplorerAt(ForestDB.getForestPath())
            def changeTimeStamp(self, dDay = 0):
                val = jupyterDB.clip().text()
                jupyterDB.clip().copy(TreeCRUD._replaceTimeStamp(val, dDay))

            def search(word, reg=False):
                return TreeDB.forest().search(word, reg = reg)

        return Tree()

    def clip():
        from ClipboardDB import ClipboardDB
        class Clip:
            def __init__(self):
                pass
            def text(self):
                return ClipboardDB.getText()
            def img(self):
                return ClipboardDB.getImage()
            def copy(self, text):
                ClipboardDB.copy2clipboard(text)
            def applyOnCopied(self,func):
                self.copy(func(self.text()))
            def image2Text(self,img = None):
                from CryptsDB import CryptsDB
                from ImageProcessing import ImageProcessing as im
                if (img is None):
                    img = self.img()
                name = CryptsDB.generateUniqueId() + ".png"
                img.save(name)
                txt = im.image2text(name)
                File.deleteFiles([name])
                return txt
        return Clip()

    def displayer(content, typ = "python"):
        from ModuleDB import ModuleDB
        return ModuleDB.colorPrint(typ, content)

    def startUp():
        from TreeDB import TreeDB
        from FileDatabase import File
        from TreeDB import ForestDB
        from TimeDB import TimeDB

        class SetUp:
            def home():
                content = SetUp._text(jupyterDB.startUp().Ops().home().getContent())
                SetUp._both()
                exec(content)

            def _text(arr):
                return "\n".join(arr)

            def office():
                content = SetUp._text(jupyterDB.startUp().Ops().office().getContent())
                SetUp._both()
                exec(content)

            def _both():
                content = SetUp._text(jupyterDB.startUp().Ops().both().getContent())
                exec(content)

            def Ops():
                from PickleCRUDDB import PickleCRUD
                class IOps(PickleCRUD):
                    def __init__(self, loc = []):
                        if(type(loc) == str):
                            loc = [loc]
                        super().__init__("globals", ['codes','start up'] + loc )
                    def add(self, lineOrContent):
                        val = self.read()
                        val += lineOrContent.splitlines()
                        super().add([], val, True)

                    def delete(self, lineNrRange):
                        a, b = IOps._parse(lineNrRange)
                        self._extractNAddNUpdate([],a-1, b)

                    def _parse(lineRange):
                        if(type(lineRange) ==  int):
                            return lineRange, lineRange
                        a,b = lineRange.split("-")
                        return int(a), int(b)

                    def _extractNAddNUpdate(self, lines, a, b):
                        val = self.read()
                        newVal  = val[:a]
                        newVal += lines
                        newVal += val[b:]
                        super().add([], newVal, True)

                    def replace(self, line, lineNr):
                        self._extractNAddNUpdate(line.splitlines(),lineNr-1, lineNr)

                    def insert(self, line, at):
                        self._extractNAddNUpdate(line.splitlines(),at-1, at-1)

                    def display(self):
                        content = "\n".join(self.read())
                        from GraphDB import GraphDB
                        return GraphDB.displayCode().smallNrOfLines(content, "py")

                    def read(self):
                        return super().read([])

                    def getContent(self):
                        return self.read()

                    def getStructure(self):
                        return self.read()
                class Temp:
                    def office():
                        class OOps(IOps):
                            def __init__(self):
                                super().__init__("office")
                        return OOps()
                    def home():
                        class HOps(IOps):
                            def __init__(self):
                                super().__init__("home")
                        return HOps()

                    def both():
                        class BOps(IOps):
                            def __init__(self):
                                super().__init__("both")
                        return BOps()

                return Temp
        return SetUp

    def plan():
        from PlanningDB import PlanningDB
        return PlanningDB

    def localIpyLink(path, printIt = True):
        if(not path.endswith(".ipynb")):
            path += ".ipynb"

        path = os.path.abspath(path)
        from RegexDB import RegexDB
        res = RegexDB.replace(".*timeline",path,
                               lambda x: "http://localhost:8888/notebooks").replace(os.sep, "/").replace(" ","%20")
        if(printIt):
            print(res)
        else:
            return res

    def myDetails():
        class Attr:
            def __init__(self, val):
                self.value = val
            def get(self):
                return self.value
            def copy(self):
                from jupyterDB import jupyterDB
                jupyterDB.clip().copy(self.value)
        class Tempo:
            def email():
                class Email:
                    def rwth():
                        return Attr("Raja.Chauhan@rwth-aachen.de")
                    def fh():
                        return Attr("raja-babu.chauhan@alumni.fh-aachen.de")
                    def access():
                        return Attr("r.chauhan@access-technology.de")
                return Email

            def phoneNr():
                return Attr("01627078024")

            def matriculationNr():
                return Attr("3194210")

            def bankInfo():
                class Temp:
                    def iban():
                        return Attr("DE06 6607 0024 0113 5011 00")

                    def bic():
                        return Attr("DEUTDEDB660")

                    def kundeNummer():
                        return Attr("1921135011")

                    def allInOne():
                        return Attr(" ".join(["IBAN:" , Temp.iban().get(), "bic:", Temp.bic().get(), "kundeNummer: ",
                                              Temp.kundeNummer().get()]))

                return Temp

            def address():
                class Temp:
                    def street():
                        return Attr("Kullenhofstraße")

                    def houseNr():
                        return Attr("66")

                    def roomNr():
                        return Attr("1014")

                    def pobNr():
                        return Attr("52074")

                    def allInOne():
                        return Attr(" ".join([Temp.street().get(), Temp.houseNr().get(), " room Nr.",
                                              Temp.roomNr().get(), "Plz.",Temp.pobNr().get()]))
                return Temp

        return Tempo

    def notifyWindow(title, msg, timeInsec = 2, icon=None):
        from plyer import notification
        if(icon is None):
            icon = Path.joinPath(jupyterDB.resource().dirPath,r"assests\python_18894.ico")
        notification.notify(
            title = title,
            message = msg,
            timeout = timeInsec,
            app_icon = icon
        )