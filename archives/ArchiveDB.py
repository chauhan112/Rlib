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
    def _driveStartPath():
        import sys
        import string
        from ListDB import ListDB
        from jupyterDB import jupyterDB
        
        class Cache:
            def readVal(indexName):
                vals = Cache._read()
                return ListDB.dicOps().get(vals, Cache._loc(indexName))
            
            def _read():
                return jupyterDB.pickle().read("temps")
            
            def writeVal(index, val):
                vals = Cache._read()
                ListDB.dicOps().add(vals, Cache._loc(index), val)
                
            def _loc(name):
                return ['rlibs','ExplorerUtils','driveStartPath', name]
        
        if(Cache.readVal("index") == Cache.readVal("lastIndex")):
            return Cache.readVal("value")
        
        a = []
        if sys.platform == 'win32':
            a = [
                '%s:\\' % d for d in string.ascii_uppercase
                if os.path.exists('%s:' % d)
            ]
        Cache.writeVal('lastIndex', Cache.readVal('index'))
        Cache.writeVal("value", a)
        return a
    def syntax(word = None):
        from LibsDB import LibsDB
        from IPython.display import display
        from ModuleDB import ModuleDB
        from SerializationDB import SerializationDB
        from Database import Database
        from SearchSystem import DicSearchEngine
        class CppCodeDisplayerSearcher(DicSearchEngine):
            def _callback(self, item):
                display(ModuleDB.colorPrint("cpp", self.searchSys.container[item]))
        class CppSyntax:
            def __init__(self):
                self.mainContent = self._read()
            def search(self, word = None):
                return Database.dbSearch(CppCodeDisplayerSearcher(self.mainContent['cpp']), word)
            def addCode(self,key, val, overwrite= False):
                if(not overwrite):
                    if(key in self.mainContent['cpp']):
                        print("key already exists")
                        return 
                self.mainContent['cpp'][key] = val
                self._write()
            def _read(self):
                return SerializationDB.readPickle(LibsDB.picklePath("cpp"))
            def _write(self):
                SerializationDB.pickleOut(self.mainContent, LibsDB.picklePath("cpp"))
            def delete(self, key):
                del self.mainContent['cpp'][key]
                self._write()
        db = CppSyntax()
        return db
        
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
class PdfSearchGUI(IDatabaseGUI, IAbout):
    def __init__(self):
        self._make_layout()
    def _make_layout(self):
        self._gnrb = GenerateNRowsBox(2)
        self._gnrb.get_child(0).add_widget(widgets.Text(placeholder="path or variable name"))
        self._is_path_wid = RCheckbox(description="is path", indent = False, layout={'width': 'auto'})
        self._gnrb.get_child(0).add_widget(self._is_path_wid.get())
        self._gnrb.get_child(0).add_widget(widgets.Checkbox(
            description="walk", indent = False,  layout={'width': 'auto'}))
        self._gnrb.get_child(0).add_widget(widgets.Button(description="execute"))
        self._gnrb.get_child(1).add_widget(widgets.Output())
        self._hw = HideableWidget()
        self._hw.set_widget(self._gnrb.get_child(0).get_child(2))
        self._hw.hide()
        self._is_path_wid.on_changed(self._show_on_path_selected)
        self._sw = SearchWidget()
        self._gnrb.get_child(0).get_child(-1).on_click(self._pdf_search)
    def display(self):
        display(self._gnrb.get())
        return self._gnrb.get()
    def display_info(self):
        return "search in pdf files and or variables in the notebook"
    def _show_on_path_selected(self, btn):
        if self._is_path_wid.get().value:
            self._hw.show()
        else:
            self._hw.hide()
    def _pdf_search(self, btn):
        path = self._gnrb.get_child(0).get_child(1)
        val = self._gnrb.get_child(0).get_child(0).value.strip()
        if not path.value:
            files = jupyterDB._params[val]
        else:
            files = Path.filesWithExtension('pdf', val, walk=self._gnrb.get_child(0).get_child(2).value)
        out = self._gnrb.get_child(1).get_child(0)
        out.clear_output()
        with out:
            self._sw.set_database(Database.pdfDB(files))
            display(self._sw.get())

class DrawIOGeometry:
    def __init__(self, x= 0, y= 0, h= 20, w =20):
        self.x= x
        self.y = y
        self.h =h
        self.w = w

    def string(self):
        return f'<mxGeometry as="geometry" height="{self.h}" width="{self.w}" x="{self.x}" y="{self.y}"/>'

def lineOne(left='..', middle= "..", right= "..", y = 0):
    words = [DrawIOWord(left, geometry=DrawIOGeometry(x = 0, y=y), align="right"),
     DrawIOWord(middle, geometry=DrawIOGeometry(x = 80, y=y)),
     DrawIOWord(right, geometry=DrawIOGeometry(x = 230, y=y))]
    return DrawIO(words)

def container(iid = 2, parent = 1):
    drawIO = DrawIO([])
    inc = 0
    for i in range(10):
        drawIO.merge(lineOne(y = inc))
        inc += 22
    contain = f"""<mxCell connectable="0" id="{iid}" parent="{parent}" style="group;strokeColor=#000000;"""\
                f"""opacity=30;" value="" vertex="1"><mxGeometry as="geometry" height="{drawIO.maxX+2}" """ \
                f"""width="{drawIO.maxY+2}" x="0" y="0"/></mxCell>"""
    s = iid +1
    for w in drawIO.words:
        w.parentId = iid
        w._id = s
        s += 1
    jupyterDB.clip().copy(urllib.parse.quote(drawIO._string(contain)))
    
class FoodLogger:
    def __init__(self):
        self.outPklFile = PickleCRUD('LifeLogs')
        self.category = 'eating'
        self.dumpingPath = Path.joinPath(resourcePath(), 'recycleBin\\eatingDelete.pkl')
        self.recyleBin = {}
        raise IOError("needs testing")

    def logEating(self,name, time, content = "",date = 0):
        date = TimeDB.getTimeStamp(date)
        if(date not in self.outPklFile.data[self.category]):
            self.outPklFile.data[self.category][date] = {}
        self.outPklFile.data[self.category][date][time] = {'name':name, 'content': content}
        self.outPklFile._write(self.outPklFile.data)

    def showLog(self,date = 0):
        date = TimeDB.getTimeStamp(date)
        return self.outPklFile.data[self.category][date]

    def delete(self, pos = []):
        self.recyleBin = {'data':ListDB.dicOps().get(self.outPklFile.data, pos),
                          'pos': pos}
        ListDB.dicOps().delete(self.outPklFile.data, pos)
        SerializationDB.pickleOut(self.recyleBin, self.dumpingPath)

    def _restore(self):
        if(self.recyleBin is None):
            print("nothing to restore")
            return
        ListDB.dicOps().add(self.outPklFile.data, self.recyleBin['pos'], self.recyleBin['data'])

    def _restoreFromFile(self, path = None):
        if(path is None):
            path = self.dumpingPath
        self.recyleBin = SerializationDB.readPickle(path)
        self._restore()
class TreeRenderer:
    def __init__(self):
        self.set_node_creator(self._default_node_creator)
    def _name_func(self, dicIns):
        return dicIns.name
    def _default_node_creator(self, val, index):
        dt = DicTree(val, index)
        dt.set_name_func()
        return dt
    def set_dictionary(self, dic):
        self.data = dic
        self.dicExpl = DicTree(dic)
    def getAsText(self):
        return self._rendered(self.dicExpl)
    def _rendered(self, root):
        space =  '    '
        branch = '│   '
        tee =    '├── '
        last =   '└── '
        def tree(dir_path , prefix: str=''):
            contents = list(dir_path.iterdir())
            pointers = [tee] * (len(contents) - 1) + [last]
            for pointer, path in zip(pointers, contents):
                yield prefix + pointer + path.get_name()
                if path.is_dir():
                    extension = branch if pointer == tee else space
                    yield from tree(path, prefix=prefix+extension)
        return "\n".join(tree(root))
    def set_node_creator(self, node_creator):
        self._node_creator = node_creator
    def set_tree_root(self, root):
        self.dicExpl = root
class Dic2GraphImproved:
    def __init__(self):
        self._node_map = {}
        self.ROOT_LABEL = "root"
        self._path = [self.ROOT_LABEL]
        self.set_node_creator_func(self._default_node_creator)
    def _default_node_creator(self, val):
        ns = NameSpace()
        ns.value = val
        ns.children = []
        return ns
    def set_dic(self, dic):
        self._dic = dic
    def convert(self):
        self._path.clear()
        self._node_map.clear()
        self._path.append(self.ROOT_LABEL)
        self._get_node(self._path)
        self._execute(self._dic)
        return self._node_map[tuple([self.ROOT_LABEL, ])]
    def _execute(self, val):
        for key in val:
            value = val[key]
            node = self._get_node(self._path)
            node.children.append(self._get_node(self._path + [key]))
            self._path.append(key)
            if type(value) == dict:
                self._execute(value)
            self._path.pop()
    def _get_node(self, loc: list[str]):
        val = tuple(loc)
        if val not in self._node_map:
            node = self._creator(val)
            self._node_map[val] = node
        return self._node_map[val]
    def set_node_creator_func(self, node_creator):
        self._creator = node_creator
class LoggerRenderer:
    def __init__(self):
        self._key_view_map = {}
        self.set_adder_func(self._default_log_func)
        self._rendered = None
    def _default_log_func(self, btn, *param):
        vals = {}
        for ke in self._key_view_map:
            wid = self._key_view_map[ke]
            if type(wid) != tuple:
                vals[ke] = wid.value
            elif self._structure[ke][StringEnums.TYPE]== SupportedTypes.MultipleSelect.name:
                vals[ke] = wid[1]._model
            elif self._structure[ke][StringEnums.TYPE]== SupportedTypes.KeyValuesPair.name:
                vals[ke] = wid[1]._basic._model.content
            else:
                raise IOError("Unknown parameter detected")
        cotnent = self._model.read(self._name)
        cotnent["data"].append(vals)
        self._model.add(self._name, cotnent, True)
    def set_adder_func(self, func):
        self._on_log_func = func
    def set_model(self, name, model):
        self._name = name
        self._model = model
        self._structure = model.read(name)['structure']
    def render(self):
        if self._rendered:
            return self._rendered
        res = []
        for key in self._structure:
            typ = self._structure[key][StringEnums.TYPE]
            if typ == SupportedTypes.Text.name:
                wid = widgets.Text(description=key)
                res.append(wid)
                self._key_view_map[key] = wid
            elif typ == SupportedTypes.LargeText.name:
                wid = widgets.Textarea(description=key, layout={"width":"auto", "max_width":"800px"})
                res.append(wid)
                self._key_view_map[key] = wid
            elif typ in [SupportedTypes.Checkbox.name, SupportedTypes.Boolean.name]:
                wid = widgets.Checkbox(description=key, layout={"width":"auto"})
                res.append(wid)
                self._key_view_map[key] = wid
            elif typ == SupportedTypes.Options.name:
                options = []
                if StringEnums.OPTIONS in self._structure[key][StringEnums.INFO]:
                    options = self._structure[key][StringEnums.INFO][StringEnums.OPTIONS]
                wid = widgets.Dropdown(options=options,description=key)
                res.append(wid)
                self._key_view_map[key] = wid
            elif typ == SupportedTypes.MultipleSelect.name:
                ly, cont = ViewsCollection.get_list_maker()
                obj = widgets.HBox([widgets.Label(key, layout={"width":"80px", "justify_content":"flex-end", "margin":"0px 8px 0px 0px"}), ly])
                res.append(obj)
                self._key_view_map[key] = (obj, cont)
            elif typ in [SupportedTypes.DateTime.name, SupportedTypes.Date.name]:
                infos = self._structure[key][StringEnums.INFO]
                ui = self._get_date_time_wid(typ, autoFill = StringEnums.AUTO in infos)
                ui.description = key
                if StringEnums.DISABLED in infos:
                    ui.disabled = infos[StringEnums.DISABLED]
                res.append(ui)
                self._key_view_map[key] = ui
            elif typ == SupportedTypes.Time.name:
                now = datetime.datetime.now()
                infos = self._structure[key][StringEnums.INFO]
                ui = widgets.TimePicker(description= key)
                if StringEnums.AUTO in infos:
                    ui.value = datetime.time(now.hour, now.minute)
                if StringEnums.DISABLED in infos:
                    ui.disabled = infos[StringEnums.DISABLED]
                res.append(ui)
                self._key_view_map[key] = ui
            elif typ == SupportedTypes.KeyValuesPair.name:
                ly, cnt = KeyValueAdderView.keyValueCrud({})
                obj = widgets.HBox([widgets.Label(key, layout={"width":"80px", "justify_content":"flex-end", "margin":"0px 8px 0px 0px"}), ly])
                res.append(obj)
                self._key_view_map[key] = (obj, cnt)
            else:
                print(self._structure[key][StringEnums.TYPE])
        btn = widgets.Button(description="log")
        btn.on_click(self._on_log_func)
        res.append(btn)
        self._rendered = widgets.VBox(res)
        return self._rendered
    def _get_date_time_wid(self, typ, autoFill = False):
        now = datetime.datetime.now()
        if typ == SupportedTypes.DateTime.name:
            x = widgets.NaiveDatetimePicker()
        else:
            x = widgets.DatePicker()
        if autoFill:
            x.value = now
        return x
    def creator():
        return LoggerRenderer()
class DisplayAndEditor:
    def __init__(self):
        self._ops_map =  {}
        self._renderer = None
        self._out = CustomOutput()
    def _set_description(self, wid, des, typ):
        if typ in [SupportedTypes.KeyValuesPair.name, SupportedTypes.MultipleSelect.name]:
            wid._description.value = des
        else:
            wid.description = des
    def _update_values(self):
        for key in self._renderer._structure:
            typ = self._renderer._structure[key][StringEnums.TYPE]
            infos = self._renderer._structure[key][StringEnums.INFO]
            wid = self._ops_map[(key, typ)]["wid"]
            sbc, extra_lay = self._ops_map[(key, typ)]["data"]
            wid.set_info(infos)
            wid.process_info()
            wid.set_value(self._data[key])
            sbc.layout._key = key
            if extra_lay:
                new_val = self._get_readable_lay(key)
                extra_lay.value = new_val.value
    def get_visualizer(self):
        if self._renderer is None:
            self._renderer = NewRenderer.creator()
            self._renderer.set_scope(self._bsc._scope)
            self._renderer._structure = self._bsc._model.read(self._bsc.controllers.ldcc._cur_btn.description)["structure"]
        res = []
        for key in self._renderer._structure:
            typ = self._renderer._structure[key][StringEnums.TYPE]
            infos = self._renderer._structure[key][StringEnums.INFO]
            wid = self._renderer._creator_map[typ](description=key)
            wid.set_info(infos)
            wid.process_info()
            wid.set_value(self._data[key])
            lay = wid.layout()
            lay.disabled = True
            lay.layout.width ="auto"
            extra_lay = self._get_readable_lay(key)
            sbc = SingleButtonController(icon="edit", layout={"width":"auto"}, button_style="success")
            sbc.layout._key = key
            sbc.set_clicked_func(self._btn_clicked)
            self._set_editable_status(infos, sbc.layout)
            if extra_lay:
                HideableWidget.hideIt(lay)
                row_lay = widgets.HBox([sbc.layout, lay, extra_lay])
            else:
                row_lay = widgets.HBox([sbc.layout, lay])
            res.append(row_lay)
            self._renderer._key_view_map[key] = wid
            self._ops_map[(key, typ)] = {'layout': row_lay, 'editable_view': lay, 'data': [sbc, extra_lay], "wid": wid}
        res.append(self._out.get_layout())
        return widgets.VBox(res)
    def _btn_clicked(self, btm):
        if btm.button_style != "danger":
            btm.button_style = "danger"
        else:
            btm.button_style = "success"
        typ = self._renderer._structure[btm._key][StringEnums.TYPE]
        ly_info = self._ops_map[(btm._key, typ)]
        if typ in [SupportedTypes.KeyValuesPair.name, SupportedTypes.MultipleSelect.name]:
            if btm.button_style == "success":
                HideableWidget.hideIt(ly_info["editable_view"])
                _, extra_lay = ly_info["data"]
                HideableWidget.showIt(extra_lay)
            else:
                HideableWidget.showIt(ly_info["editable_view"])
                _, extra_lay = ly_info["data"]
                HideableWidget.hideIt(extra_lay)
        else:
            if btm.button_style == "success":
                lay = ly_info['editable_view']
                lay.disabled = True
            else:
                lay = ly_info['editable_view']
                lay.disabled = False
    def _set_editable_status(self, infos, wid):
        k = "disabled"
        if k in infos:
            wid.disabled = infos[k]
    def _get_readable_lay(self, key):
        forma = lambda x: f"""<font face='comic sans ms' color ='darkcyan'>{x}</font>"""
        extra_lay = None
        typ = self._renderer._structure[key][StringEnums.TYPE]
        if typ in [SupportedTypes.KeyValuesPair.name, SupportedTypes.MultipleSelect.name]:
            content = str(self._data[key])
            if type(self._data[key]) == str:
                content = "<br>".join(self._data[key].splitlines())
            return widgets.HTML(forma(key) + ": " + content + "<br>")
        return extra_lay
    def set_basic_controller(self, bsc):
        self._bsc = bsc
    def set_data(self, data):
        self._data = data