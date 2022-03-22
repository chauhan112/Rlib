class StaggingAreaDB:
    def translate(path):
        from SerializationDB import SerializationDB
        from ListDB import ListDB
        def _translate(path):
            pkl = SerializationDB.readPickle(path)
            newPkl = {}
            for key in pkl:
                for key2 in pkl[key]:
                    newPkl[key2] = pkl[key][key2]
            return newPkl
            
        import numpy as np
        dic = SerializationDB.readPickle(path)
        branchPath = ListDB.branchPath(dic)
        shape = np.array(branchPath).shape
        if(shape[1] == 3):
            print(f"translating {path}")
            dic = _translate(path)
        SerializationDB.pickleOut(dic, path)
        
    def miniCondaPath():
        paths = {'office': r"C:\Users\rajac\Miniconda3"}
        from ModuleDB import ModuleDB
        return paths[ModuleDB.laptopName()]
        
    def get_default_windows_app(suffix):
        import shlex
        import winreg

        class_root = winreg.QueryValue(winreg.HKEY_CLASSES_ROOT, suffix)
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r'{}\shell\open\command'.format(class_root)) as key:
            command = winreg.QueryValueEx(key, '')[0]
            return shlex.split(command)[0]

    def getAllPythonKeyWords():
        import keyword
        return keyword.kwlist

    def getAllImportedClasses():
        import sys, inspect
        arr = []
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if(not name.startswith("_")):
                arr.append(name)
        return arr
    
    def getAllLinesContainingFromImport(contentList):
        from RegexDB import RegexDB
        lines = []
        for line in contentList:
            if(RegexDB.isThereRegexMatch(RegexDB.lookAheadAndBehind("from ", " import", ".*" ),line)):
                lines.append(line)
        return lines

    def getImportedClassFromLines(importLines):
        clas = []
        for line in importLines:
            c = line.split("import")[1]
            cls = [i.strip() for i in c.split(",")]
            clas += cls
        return clas

    def logger():
        import inspect
        class Foo:
            def foo(self):
                pass

            def bar(self,a, b):
                pass

            def foobar(self, x, y, z):
                pass

            def __getattribute__(self, name):
                returned = object.__getattribute__(self, name)
                if inspect.isfunction(returned) or inspect.ismethod(returned):
                    print ('called ', returned.__name__)
                return returned

        a = Foo()
        a.foo()
        a.bar(1, 2)
        a.foobar(1, 2, 3)
    
    def getPdfPageAsImage(pdfPath, pageNr):
        from CryptsDB import CryptsDB
        from pdf2image import convert_from_path
        from Pdf_Database import PDF
        from Path import Path
        
        tempPdf = CryptsDB.generateRandomName(20) + ".pdf"
        print(tempPdf)
        PDF.extractPdf(pdfPath, tempPdf, (pageNr-1,pageNr))
        image = convert_from_path(tempPdf)[0]
        Path.delete([tempPdf])
        return image

    def simpleCommentRemoverPython(content):
        from  ListDB import ListDB
        from RegexDB import RegexDB
        lines = content.split("\n")
        filer = [RegexDB.isThereRegexMatch("[ \n]#", i) for i in lines]
        filer = [not i for i in filer]
        py = [line for i, line in enumerate(lines) if(filer[i])]
        return "\n".join(ListDB.listFilter(lambda x: len(x.strip())>0, py))

    def describeProject(path = "."):
        from Path import Path
        files = Path.filesWithExtension("py", path)
        print(Path.getSize(files))

    def commaSeperate(val):
        new_val = ""
        for i,j in enumerate(val[::-1]):
            new_val = j + new_val
            if((i+1) % 3 == 0):
                new_val = ',' + new_val
        return new_val

    def fillClassList(text):
        import ast
        classList = []
        className = None
        methodName = None
        p = ast.parse(text)
        node = ast.NodeVisitor()
        for node in ast.walk(p):
            if isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
                if isinstance(node, ast.ClassDef):
                    className = node.name
                else:
                    methodName = node.name
                if className != None and methodName != None:
                    subList = (methodName , className)
                    classList.append(subList)
                    print("class: " + className + ", method: " + methodName)

    def zipPathGrouper(paths, sep ="/"):
        from collections import defaultdict
        from OpsDB import OpsDB
        tree = lambda : defaultdict(tree)
        def add(t, path):
            for node in path:
                t = t[node]
        k = OpsDB.grouperValues(lambda x: x.endswith("/"), paths)
        folders, files = k[True], k[False]
        tr = tree()
        for fp in files:
            add(tr, fp.split("/"))
        return tr

    def getVariableTypeDB(varname, files):
        from Database import Database, D2Server
        import os
        from cpp.Cpp import Cpp
        vartypes = {}
        for file in files:
            bas = os.path.basename(file)
            vartypes[bas] = getVariableLinesFromFile(file)

        db = Database.getDB(list(vartypes.keys()), list(vartypes.values()), displayer = lambda x: print(vartypes[x]))
        db.search(varname)
        return db

    def taskManager():
        import os
        os.system("start /b cmd /c taskmgr")
        
    def getCloudPathTo(word = None, path =None):
        if( path is None):
            path = getPath()
        pathWords = path.split("\\")
        if(word is None):
            word = 'cloud'
        path = pathWords[0]
        for i in pathWords[1:]:
            path += os.sep + i
            if(word.lower() in i.lower()):
                return path
        return path

    def performanceChecker(functionCallAsString):
        import cProfile
        return cProfile.run(functionCallAsString)

    def startDrawio():
        from OpsDB import OpsDB
        from NetworkingDB import NetworkingDB
        from LibsDB import LibsDB
        import webbrowser
        OpsDB.runOnThread(NetworkingDB.startAPythonServer, [LibsDB.cloudPath() + r"\Global\code\Code Godown\drawio-master\drawio-master\drawio-master\src\main\webapp", 
                    8001])
        webbrowser.open("http://127.0.0.1:8001/")

    def combiner():
        class LinearCombinerExample:
            def combiner2(self, l1, l2):
                # see testDB for example and what it does
                def firstIntersectedIndex(l1, val, _from):
                    interse = []
                    for i in range(_from, len(l1)):
                        if(val.intersects(l1[i])):
                            interse.append(i)
                    return interse

                newArr = []
                ini = 0
                for val in l2:
                    inter = firstIntersectedIndex(l1, val, ini)
                    if(len(inter) > 0):
                        b = inter[0]
                        newArr += l1[ini: b]
                        newArr.append(val)
                        ini = inter[-1] + 1
                newArr += l1[ini:]
                return newArr

            def combiner(self, l1, l2):
                l2Pointer = 0
                newContainer = []
                flag = False
                first = False
                for i in range(len(l1)):
                    if(l2Pointer >= len(l2)):
                        newContainer.append(l1[i])
                        continue

                    if(l1[i].intersects(l2[l2Pointer])):
                        flag = True
                        if(not first):
                            newContainer.append(l2[l2Pointer])
                        first = True
                    else:
                        first = False
                        if(flag):
                            flag = False
                            l2Pointer += 1
                        newContainer.append(l1[i])
                return newContainer
        return LinearCombinerExample()

    def isThereInternetConnection():
        import requests
        url = "http://www.kite.com"
        timeout = 5
        try:
            request = requests.get(url, timeout=timeout)
            return True
        except (requests.ConnectionError, requests.Timeout) as exception:
            return False

    def retryUntillThereIsInternet():
        import time
        print("retrying")
        if(not isThereInternetConnection()):
            time.sleep(5)
            retryUntillThereIsInternet()
            
    def runOnceInAMonth(lastRunMonth, func, parameters = []):
        (_, month ,_), _ = TimeDB.today()
        if(lastRunMonth == month ):
            return
        if(type(parameters) != list):
            parameters = [parameters]
        func(*parameters)
        
    def PickleOps(path):
        import ipywidgets as widgets
        from WidgetsDB import WidgetsDB
        class Temp:
            pass

        res = widgets.HBox([])
        return widgets.VBox([
            widgets.HBox([widgets.Label(f'Pickle path: '),
                          widgets.Text(path, disabled = True)]),
            widgets.HBox([widgets.Label("Location:"), widgets.Text("", disabled = True)]),
            widgets.HBox([widgets.Label("Keys::"),res ]),
            widgets.HBox([widgets.Label("value::"),widgets.Text("") ]),
            widgets.HBox([widgets.Button(description="add"), 
                          widgets.Button(description="get"),
                          WidgetsDB.mButton("view", path, lambda x: ExplorerDB.dicExplorer(
                              SerializationDB.readPickle(x._key)))])
         ])
            
    def helpArea(mod):
        import ipywidgets as widgets
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            print(help(mod))
        out = f.getvalue()
        wid = widgets.Textarea(
                value=out,
                disabled=True,
                layout=widgets.Layout(width='90%')
            )
        return wid

    def getNebors(pos, maxes):
        i, j, k = pos
        
        def ne(arr):
            for i, val in enumerate(arr):
                if(val < 0 or val >= maxes[i]):
                    return False
            return True
        
        nebors = [(i,j, k-1), (i,j, k+1), (i,j-1, k), (i,j+1, k), (i-1,j, k), (i+1,j, k)]
        nebors = list(filter(ne,nebors ))
        return nebors
       
    def classDependency(dataModel):
        # see CodeDB analyseComplexityAndLOC for data model
        dependency = {}
        allClasses = set(dataModel.classModel.read().allClasses())
        for cls in dataModel.classModel.content:
            for me in dataModel.classModel.read().allMethods(cls, False):
                if cls not in dependency:
                    dependency[cls] = []
                dependency[cls] += list(allClasses.intersection(
                    WordDB.tokenize(dataModel.classModel.content[cls]['methods'][me]['content'])))
                
        dependentClasses = {}
        for cls in dependency:
            if(len(dependency[cls]) !=0):
                dependentClasses[cls] = set(dependency[cls])
        return dependentClasses

    def weather_data(city):
        import requests
        query='q='+city
        url = 'http://api.openweathermap.org/data/2.5/weather?'+query+'&APPID=b35975e18dc93725acb092f7272cc6b8&units=metric'
        res=requests.get(url)
        return res.json()
    
    def uninstallPackages(packages = [], env='base', showOut= True):
        from OpsDB import OpsDB
        cmds = [f'conda activate {env}']
        for pa in packages:
            cmds.append(f'pip uninstall {pa} -y')
        out, err = OpsDB.cmd().run(cmds, True)
        if(showOut):
            print(out + "\n" + err)
        
    def installPackages(setupFiles = [], env='base', showOut= True):
        from OpsDB import OpsDB
        cmds = [f'conda activate {env}',]
        for f in setupFiles:
            absF = os.path.abspath(f)
            cmds.append(absF[:2])
            cmds.append(f'cd "{os.path.dirname(absF)}"')
            cmds.append("python setup.py install")
        out, err = OpsDB.cmd().run(cmds, True)
        if(showOut):
            print(out + "\n" + err)

    def displayLineWise(container):
        for ele in container:
            print(ele)
            inp = input("next")
            if(inp == 'q'):
                break
class TempUrlFileManager:
    def __init__(self, filename):
        from SerializationDB import SerializationDB
        from Database import Database
        self.filename = filename
    def addUrl(self, title, value):
        val = self.read()
        val[title] = value
        self.write(val)
    def search(self, word):
        return Database.dbSearch(Database.urlDB(self.read()), word)
    def delete(self, title):
        val = self.read()
        del val[title]
        self.write(val)
    def write(self, val):
        SerializationDB.pickleOut(val, self.filename)
    def read(self):
         return SerializationDB.readPickle(self.filename)
         
class TimeAdder:
    def __init__(self, time = "00:00"):
        self.time = time

    def addString(self, string):
        a1, b1 = self._parse(self.time)
        a2, b2 = self._parse(string)
        m = (b1+b2) % 60
        h_delta = (b1 + b2) // 60
        h = (a1 +a2 + h_delta) % 24
        return self._rep(h,m)

    def _parse(self, txt):
        a , b  = txt.split(":")
        return int(a), int(b)

    def _rep(self, hr, m):
        hs = str(hr)
        ms = str(m)
        if (hr < 10 ):
            hs = "0" + str(hr)
        if (m < 10 ):
            ms = "0" + str(m)
        return hs + ":"+ms

    def addMin(self, vla):
        a, b = self._parse(self.time)
        m = b % 60
        h = b//60
        return self._rep((a +d_delta)%24, m)