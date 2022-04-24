class ArchiveDB:
    def resizeAllFiles(files, numberOFLines = 30):
        from FileDatabase import File
        for f in files:
            content = File.getFileContent(f).split("\n")[:numberOFLines]
            content = "\n".join(content)
            File.overWrite(f, content)
    def renameAllFiles(files, newNameFunc):
        import os
        for f in files:
            newName = newNameFunc(f)
            os.rename(f, newName)
    def filesWithNames(names, path = None, walk = False):
        import os
        from Path import Path
        if(path is None):
            path = os.getcwd()
        files = Path.getFiles(path, walk)
        filteredFiles = []
        for n in names:
            filteredFiles += list(filter(lambda x: n in x, files))
        return filteredFiles
    def getKeys():
        content = ArchiveDB.getFileContentAsDictionary()
        return list(content.keys())
    def getFileContentAsDictionary():
        from Path import Path
        from FileDatabase import File
        path = Path.joinPath(resourcePath(),"treeDB.yaml")
        content = yaml.safe_load(File.getFileContent(path))
        return content
    def overwritePrototype(content):
        from Path import Path
        from FileDatabase import File
        file = Path.joinPath(resourcePath(), "Prototype.ipynb")
        File.overWrite(file, content)
    def toQtPath(path):
        return path.replace("\\", "/")
    def toWinPathFromQt(path):
        return path.replace("/", "\\")
    def ipAddress2Binary(nets):
        def getSize(byte):
            s =""
            for i in range(8-len(byte)):
                s += '0'
            return s + byte
        i = 0
        for ip in nets:
            bi = ""
            for no in ip.split("."):
                bi += getSize(str(bin(int(no)))[2:]) + " "
            i+=1
            print("R" + str(i) +"  =>  " + bi)
    def getQuestionAnswer(question = "", answer =""):
        return "\n".join([f"## <font face='comic sans ms' color ='BlueViolet'>{question}</font>",
                f"=> <font face='comic sans ms' color ='DarkCyan'>{answer}</font>"])
    def qa(qestion):
        return f"<font face='comic sans ms' color ='MidnightBlue'>{qestion}</font>"
    def ans(answer):
        return f"<font face='comic sans ms' color ='MediumTurquoise'>{answer}</font>"
    def searchWordInList(word, container, regex = False):
        indices = []
        condition = lambda word, line: word.lower() in line.lower()
        if (regex ):
            condition = lambda word, line: len(WordDB.searchWordWithRegex(regex , line.lower())) != 0
        for i,line in enumerate(container):
            if(condition(word, line)):
                indices.append(i)
        return indices
    def engineModifier(engine, buttonNameFunc= None, toolTipFunc=None, callbackXSelf=None):
        prefix = "SearchEngine"
        en = ["Dic", "FilesContent", "StringList", "FilePaths", "Url"]
        class Temp:
            def __init__(self):
                self.engine = None
        t = Temp()
        if(type(engine) == str):
            res = ArchiveDB.searchWordInList(engine, en)
            val = en[res[0]] + prefix
            exec("from SearchSystem import "+ val)
            exec("t.engine = "+ val)
            engine = t.engine
        if(callbackXSelf is not None):
            engine._callback = lambda x,y : callbackXSelf(y)
        if(buttonNameFunc is not None):
            engine.buttonName = lambda x,y : buttonNameFunc(y)
        if(toolTipFunc is not None):
            engine.toolTip = lambda x,y : toolTipFunc(y)
        return engine
    def invertList(listLength,initialValue = 0, step = 1):
        newArr = []
        while (initialValue < listLength):
            newArr.append(initialValue)
            initialValue += step
        return newArr
    def getArrayValuesWithIndicesList(listOfIndex, arr):
        values = []
        for i in listOfIndex:
            values.append(arr[i])
        return values
    def runBasic():
        from Path import Path
        from jupyterDB import jupyterDB
        from Database import Database
        from UrlDB import UrlDB
        from FileDatabase import File
        from TreeDB import TreeDB
        from SerializationDB import SerializationDB
        from DataStorageSystem import InstructionTable
        from TimeDB import TimeDB
        # data storage system
        it = InstructionTable(params=globals())
        modb = Database.moduleDB()
        jupyterDB.libSize()
        from IPython.display import HTML, display
        from NotebookDB import NotebookDB
        # code logging
        display(NotebookDB.currentRunningNotebookName())
        loggingTimeLogs = []
        def logger():
            global _ih, loggingTimeLogs
            loggingTimeLogs.append(TimeDB.today())
            jupyterDB.codeDumper().summarize(_ih, theNotebook)
        import atexit
        atexit.register(logger)
        try:
            loggerTimer
        except:
            loggerTimer = TimeDB.setTimer().regularlyUpdateTime(10*60, logger)
    def getLinks(content = None):
        from htmlDB import htmlDB
        from Crypts import DecryptDB
        from ClipboardDB import ClipboardDB
        from OpsDB import OpsDB
        from ComparerDB import ComparerDB
        from WordDB import WordDB
        from RegexDB import RegexDB
        from TreeDB import TreeDB
        def filterCells(soup):
            noOfParents = RegexDB.regexSearch(RegexDB.lookAheadAndBehind("parent=\"",'" style=', "\d+" ), str(soup))
            nr = set(noOfParents)
            sth = []
            for val in nr:
                sth += htmlDB.searchOnSoup({"tagName": "mxcell", "attr":{'parent':val}}, soup)
            return sth
        def mapperKey(dic, val):
            for key in dic:
                if(condition(val[1], key)):
                    return key
        def getContent(value):
            regex = r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
            if(ComparerDB.regexSearch(regex, value)):
                i,j = WordDB.searchWordWithRegex(regex, value)[0]
                filteredValue = value[i:j]
                return filteredValue.split('"')[0]
            else:
                try:
                    return RegexDB.regexSearch(RegexDB.lookAheadAndBehind(">","</",".*"),value)[0]
                except:
                    return value
        def getYs(val):
            try:
                y = val.mxgeometry['y']
            except:
                y = '0'
            return y
        if(content is None):
            soup = htmlDB.getParsedData(TreeDB.decodeContent(display=0))
            content = str(soup)
        soup = htmlDB.getParsedData(htmlDB.htmlDecode(urllib.parse.unquote(content)))
        linsk = filterCells(soup)
        tol = 10
        condition = lambda x, y: (float(y) >= float(x)-tol) and (float(y) <= float(x) + tol)
        val = [(i, getYs(l)) for i,l in enumerate(linsk)]
        print(len(val))
        grouped = OpsDB.grouperBasedOnKeys(mapperKey, val, lambda x: x[1])
        pairs = list(filter(lambda x: len(x) ==2, list(grouped.values())))
        for i, j in pairs:
            print(f"'{getContent( linsk[j]['value']).strip().strip(':').strip()}':",f"'{getContent(linsk[i]['value'])}',")
    def linear_alg2_correct():
        from DataStorageSystem import NotesTable
        from archives.HomeWorkCheckTools import LA_2_HW_Correct
        from ExplorerDB import ExplorerDB
        nt  = NotesTable()
        print(nt.read(['LA2', 'log']))
        exp = ExplorerDB.osFileExplorer(Path.convert2CloudPath(nt.read(['LA2', "hw", "path"])))
        exp.setFileDisplayer("zip", lambda x: LA_2_HW_Correct.showFiles(x))
        return exp
    def getSpaces(container):
        # for TreeDB.decodeContent
        # input  = [" hi", "   raja"]
        # out = [1, 3]
        res = []
        for val in container:
            n = 0
            for el in val:
                if(el == " "):
                    n += 1
                else:
                    break
            res.append(n)
        return res
    def addSpaces(spaces, toVal):
        # for TreeDB.decodeContent
        # inp spaces= [1,3], toVal = ["hi","raja"]
        # out = [" hi", "   raja"]
        newVal = []
        for i,val in enumerate(toVal):
            newVal.append(" "*spaces[i] + val)
        return newVal
    def reminder_timer():
        def reminder():
            from TimeDB import TimeDB
            from ImageProcessing import ICOPath
            hour = TimeDB.nowTime()[0]
            hour = hour - 9
            if(hour % 3 == 0):
                jupyterDB.notifyWindow("balance", "balance the big tasks", 10,ICOPath.getPathForFile("balance"))
            else:
                jupyterDB.notifyWindow("review steps for implementation", "go through final pos, and steps ", 10,
                                       ICOPath.getPathForFile("review"))
        try:
            reminderTimer
        except:
            reminderTimer = TimeDB.setTimer().regularlyUpdateTime(30*60, reminder)
import ipywidgets as widgets
class StartUpOpsEditor:
    def __init__(self):
        self.out = None
        self.history = None
    def _createGUI(self):
        class callbacks:
            def add():
                pass
            def delete():
                pass
            def replace():
                pass
            def archive():
                pass
            def undo():
                pass
        add    = Temp.functionWidget(buttonName= "add", textPlaceholder="codeLine, lineNr")
        delete = Temp.functionWidget(buttonName= "delete", textPlaceholder="number or range eg: 1-5")
        replace = Temp.functionWidget(buttonName= "replace", textPlaceholder="line, lineNr")
        archive = Temp.functionWidget(buttonName= "archive", textPlaceholder="number or range eg: 1-5")
        undo = WidgetsDB.button("undo")
        self.out = widgets.Output()
        self._displayOutput()
        self.ops    = widgets.VBox([add, delete,replace, archive, undo])
        self.res    = widgets.VBox([self.out, self.ops])
        return self.res
    def functionWidget(buttonName = "button", textPlaceholder = "", horizontal = True,
                       callbackFunc = lambda x: print(x)):
        button = WidgetsDB.mButton(buttonName, buttonName + "I",callbackFunc=callbackFunc )
        params = widgets.Text(placeholder =textPlaceholder)
        wList  = [params, button]
        if(horizontal):
            return widgets.HBox(wList)
        return widgets.VBox(wList)
    def _displayOutput(self):
        from jupyterDB import jupyterDB
        from IPython.display import display
        with self.out:
            display(jupyterDB.startUp().Ops().both().display())
class SetParam(GCommand):
    def callback(self):
        key = input("enter key: ")
        value = input('enter val : ')
        keyList = key.split(",")
        pa = parameters
        for val in keyList:
            vla = val.strip()
            if vla not in pa:
                pa[vla] = {}
            pa = pa[vla]
        pa.update({value: {}})
    def getHelp(self):
        return self.id, 'set parameters; eg: .. key,innerkey2,.. valinstr'
class ListParameters(GCommand):
    def callback(self):
        self.print(parameters, 1)
        print()
    def print(self, dic, space = 1):
        sp = ' ' * space*2
        if type(dic) == dict:
            for i, val in enumerate(dic):
                print()
                print(f'{sp}{i}. {val}', end=" ")
                self.print(dic[val], space +1)
        elif type(dic) == list:
            for i, val in enumerate(dic):
                print()
                print(f'{sp}{i}. {val}', end=" ")
        else:
            print(dic, end=" ")
    def getHelp(self):
        return self.id, 'list the parameters'
class ImportLib(GCommand):
    def __init__(self, idd, params):
        super().__init__(idd)
        self.params = params
    def callback(self):
        statement = input(":")
        exec(statement)
        self.params.update(locals())
    def getHelp(self):
        return self.id, 'execute importing statement'
class Redesign:
    index = 0
    files = Path._filesWithExtensions(['h', 'cpp'], r"C:\Users\rajac\Desktop\gittest\bachelorArbeit\MICpad")
    def openScript():
        File.openFile(Redesign.currentFile())
    def reset(index = 0):
        Redesign.index = index
    def currentFile():
        return Redesign.files[Redesign.index]
    def paths():
        class Temp:
            def newPrj():
                return 'C:\\Users\\rajac\\Desktop\\gittest\\bachelorArbeit\\Redesign'
        return Temp
    def nextt():
        if(Redesign.index >= len(Redesign.files)):
            print("All files opened")
            return
        Redesign.index += 1
def redesignOps():
    from IPython.display import display
    from WidgetsDB import WidgetsDB
    import ipywidgets as widgets
    class Temp:
        def add(x):
            name = x.description
            currentFileName = os.path.basename(Redesign.currentFile())
            copy2File = Path.joinPath(Redesign.paths().newPrj(), "module", name, currentFileName)
            clipContent = jupyterDB.clip().text()
            clipContent = "\n\n"+"\n".join(clipContent.splitlines())
            File.appendToFile(copy2File, clipContent)
        def clear(x):
            pass
        def openContent(x):
            name = x.description
            currentFileName = os.path.basename(Redesign.currentFile())
            copy2File = Path.joinPath(Redesign.paths().newPrj(), "module", name, currentFileName)
            File.openFile(copy2File)
    print("add")
    display(widgets.HBox([WidgetsDB.button("Model", Temp.add),
                  WidgetsDB.button("View", Temp.add),
                  WidgetsDB.button("Controller", Temp.add)]))
    print("open")
    display(widgets.HBox([WidgetsDB.button("Model", Temp.openContent),
                  WidgetsDB.button("View", Temp.openContent),
                  WidgetsDB.button("Controller", Temp.openContent)]))
class OldScieboDB:
    def __init__(self):
        self.pickleRegion = jupyterDB.pickle().path()
        self.codeDumper = jupyterDB.codeDumper().path
    def solveConflicts():
        s = ScieboDB()
        ScieboDB._solveConflicts(ScieboDB._getAllConflictedFiles(s.pickleRegion),
                                   ScieboDB._solvePickleConflict)
        ScieboDB._solveConflicts(ScieboDB._getAllConflictedFiles(s.codeDumper),
                                   ScieboDB._solveCodeDumperConflict)
    def _solveCodeDumperConflict(conflictedFile, baseFile):
        def update(list1, list2):
            if(len(list1) >= len(list2)):
                return list1
            else:
                return list2
        def mergeVerifier(mergedVal, againstVal):
            for com in againstVal:
                for ssid in againstVal[com]:
                    for i, line in enumerate(againstVal[com][ssid]):
                        if(line != mergedVal[com][ssid][i]):
                            return False
            return True
        def merge(mainVal, conVal):
            for laptopName in conVal:
                if(laptopName not in mainVal):
                    mainVal[laptopName] = conVal[laptopName]
                    continue
                tempVal = conVal[laptopName]
                for sessionid in tempVal:
                    if(sessionid not in mainVal[laptopName]):
                        mainVal[laptopName][sessionid] = conVal[laptopName][sessionid]
                        continue
                    conList = tempVal[sessionid]
                    mainList = mainVal[laptopName][sessionid]
                    mainVal[laptopName][sessionid] = update(conList, mainList)
            return mainVal
        conVal = SerializationDB.readPickle(conflictedFile)
        mainVal = SerializationDB.readPickle(baseFile)
        mergedVal = merge(conVal, mainVal)
        condition = mergeVerifier(mergedVal, conVal) and mergeVerifier(mergedVal, mainVal)
        if(not condition):
            print('Needs to be resolved manually')
            ScieboDB._manualCodeDumperResolver(conflictedFile, baseFile)
        else:
            SerializationDB.pickleOut(mergedVal, baseFile)
            File.deleteFiles([conflictedFile])
    def _manualCodeDumperResolver(conflictedFile, baseFile):
        ExplorerDB.dicExplorer(SerializationDB.readPickle(conflictedFile), os.path.basename(conflictedFile))
        ExplorerDB.dicExplorer(SerializationDB.readPickle(baseFile),os.path.basename(baseFile) )
    def _solveConflicts(files, resolver):
        for file in files:
            dirPath = os.path.dirname(file)
            f = os.path.basename(file)
            print(f"solving {f}")
            bas = Path.joinPath(dirPath, ScieboDB._conflictedNameToBasename(f))
            if(os.path.exists(bas)):
                resolver(file, bas)
    def _getAllConflictedFiles(path):
        files = os.listdir(path)
        f = []
        for file in files:
            if('(conflicted copy' in file):
                f.append(Path.joinPath(path, file))
        return f
    def _conflictedNameToBasename( filename):
        from RegexDB import RegexDB
        return RegexDB.regexSearch(RegexDB.lookBehind(" \(conflicted copy", ".*"),
                                   filename)[0] + ".pkl"
    def _solvePickleConflict(conflictedFile, baseFile):
        base = SerializationDB.readPickle(baseFile)
        val = set(SerializationDB.readPickle(conflictedFile)['libSize']).union(
            set(base['libSize']))
        base['libSize'] = sorted(val, key=lambda x: ScieboDB._keyForSorting(x[0]))
        Path.delete([conflictedFile])
        SerializationDB.pickleOut(base, baseFile)
    def _keyForSorting( val):
        # 'Monday, 09.11.2020 22:17:48'
        a, b, c = val.split(" ")
        date = list(map(lambda x: int(x), b.split(".")))
        time = list(map(lambda x: int(x), c.split(":")))
        days = date[2]*365 + date[1]*30 + date[0]
        secs = time[0]* 3600 + time[1]*60 + time[0]
        return days*3600*24 + secs
def oldPathSelector():
    from modules.mobileCode.CmdCommand import GController, OSExpList, GCommand, IRunnable, CmdCommandHandler
    from modules.mobileCode.tree import Goback
    import os
    class PickPath(GCommand):
        def callback(self):
            ele = self.parent.elementSelected
            exp = self.parent.parent.lister
            val = ele.getCurrentValue()
            path = exp.exp.path
            self.parent._pselected = path
            self.parent._loopBreaker = True
        def getHelp(self):
            return self.id, 'select path'
    class GobackForController(Goback):
        def callback(self):
            self.parent.parent.lister.exp.goBack()
    class ReturnableController(IRunnable):
        def __init__(self, controller : GController, confirm = True):
            self.cntrl = controller
            self.cntrl.cmdRunner._pselected = None
            self.confirm = confirm
        def run(self):
            while True:
                self.cntrl.run()
                lastCmd = self.cntrl.cmdRunner._cmdHistory.pop()
                if lastCmd == "q":
                    raise IOError("selection stopped")
                if self.confirm:
                    inp = input('confirm: ').strip()
                    if inp in ['yes','y']:
                        break
                else:
                    break
                if inp == 'q':
                   raise IOError("selection stopped")
                self.cntrl.cmdRunner._loopBreaker = False
            return self.cntrl.cmdRunner._pselected
    def onElementSelect(ele):
        exp = ele.parent.parent.lister
        val = ele.getCurrentValue()
        path = exp.exp.path +os.sep+val
        if not os.path.isfile(path):
            exp.exp.cd(val)
        else:
            ele.parent._pselected = path
            ele.parent._loopBreaker = True
        print()
    def terminalFileSelector(confirm = True):
        cnt = GController(os.path.abspath('.'), lister=OSExpList(),cmdRunner=CmdCommandHandler(callback=onElementSelect,
            promptText = "select a path: ", extraCommands=[PickPath('p'), GobackForController('b')]) )
        cnt.elementsDisplayer._runAfter = True
        return ReturnableController(cnt, confirm).run()
class Container:
    def __init__(self, contents, sectionSize = 100):
        self.contents = contents
        self.index = 0
        self.sectionSize = sectionSize
        self.temp = None
    def nextSection(self):
        if(self.index != -1):
            self.temp = self.contents[self.index* self.sectionSize: (self.index + 1)* self.sectionSize]
            self.index += 1
            if(len(self.temp) == 0):
                self.index = -1
        else:
            self.temp = []
    def prevSection(self):
        if(self.index < 1):
            self.temp = self.contents[(self.index - 1)* self.sectionSize: self.index * self.sectionSize]
            self.index -= 1
        else:
            self.temp = []
    def get(self):
        return self.temp
class ZipExplorerWithLargeNumberOfContent(ZipFileExplorer):
    def __init__(self, path, sectionSize = 200):
        self.sectionSize = sectionSize
        self._reset()
        super().__init__(path)
    def _reset(self):
        from DataStructure import DataStructure
        self.section = DataStructure.nestedNamespace({
            'status': False,
            'size': self.sectionSize,
            'totalNr': 0,
            'currentIndex': 0,
            'folders': None,
            'files': None})
    def dirList(self):
        if(self.section.status):
            return self.nextSectionListDir()
        temp = super().dirList()
        totalNr = len(temp[0]) + len(temp[1])
        if(totalNr > 300):
            self.section.status = True
            self.section.totalNr = totalNr
            self.section.folders ,self.section.files = temp[0][2:], temp[1]
            return self.nextSectionListDir()
        else:
            self._reset()
        return temp
    def cd(self, fold = None):
        if(fold == '...'):
            return self.nextSectionListDir()
        if(fold == '^^^'):
            return self.prevSectionListDir()
        super().cd(fold)
        self._reset()
    def nextSectionListDir(self):
        a = self.section.currentIndex
        halfSize = int(self.section.size / 2)
        folders = self.section.folders[a * halfSize: (a + 1) *halfSize]
        files = self.section.files[a: a + self.section.size - len(folders)]
        self.section.folders.currentIndex += len(folders)
        self.section.files.currentIndex += len(files)
        if(self.section.folders.currentIndex + self.section.files.currentIndex >= self.section.totalNr):
            self._reset()
        prefolders = ['.','..']
        if(a + b != 0):
            prefolders = ['.','..','^^^']
        return  prefolders + folders, files + ['\U0001F4C1 ...']
    def prevSectionListDir(self):
        pass
class ZipFileExplorerDisplayer(ZipFileExplorerDisplayer):
    def __init__(self, zipPath):
        super().__init__(zipPath, ZipExplorerWithLargeNumberOfContent)
    def setSectionSize(self, size):
        self.explorer.sectionSize = size