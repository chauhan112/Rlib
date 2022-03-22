from InterfaceDB import ISearchSystem
from ComparerDB import ComparerDB
from FileDatabase import File
import os

class SearchSystem:
    pass
       
class ISearch:
    def search(self, word, case = False, reg = False):
        raise NotImplementedError("abstract method")

class DicSearch:
    def __init__(self, container):
        self.container = container
        
    def search(self, word, case = False, reg = False):
        return self._gSearch(lambda key: ComparerDB.has(word, key, case, reg) or ComparerDB.has(word, self.container[key], case, reg))
    
    def key(self, word, case = False, reg = False):
        return self._gSearch(lambda key: ComparerDB.has(word, key, case, reg))
    
    def value(self, word, case = False, reg = False):
        return self._gSearch(lambda key: ComparerDB.has(word, self.container[key], case, reg))
    
    def _gSearch(self, func):
        res = []
        for key in self.container:
            if(func(key)):
                res.append(key)
        return res

class SearchEngine:
    def __init__(self,content,  searchSys, nCols = 6):
        self.searchSys = searchSys(content)
        self.nCols = nCols + 1 

    def displayer(self, result):
        from WidgetsDB import WidgetsDB
        import ipywidgets as widgets
        output = WidgetsDB.searchEngine().resultWidget()
        output.searchRes.clear_output()
        display(widgets.VBox([output.searchRes,output.buttonRes]))
        with output.searchRes:
            display(WidgetsDB.getGrid(self.nCols, [self.displayItem(key= x, name=self.buttonName(x), 
                callbackFunc=lambda x: self.callback(x, output.buttonRes), tooltip=self.toolTip(x)) for x in result]))
        return output
    
    def callback(self, button, resSect):
        resSect.clear_output()
        with resSect:
            self._callback(button._key)
    
    def _callback(self, result):
        raise NotImplementedError("Overload this function")

    def search(self, word, case = False, reg = False):
        result = self.searchSys.search(word, case, reg)
        self.displayer(result)
    
    def buttonName(self, item):
        return item
    
    def toolTip(self, item):
        return self.buttonName(item)
       
    def displayItem(self,key, name, callbackFunc, tooltip=None):
        from WidgetsDB import WidgetsDB
        b = WidgetsDB.mButton(name, key, callbackFunc)
        b.tooltip = tooltip
        return b

class DicSearchEngine(SearchEngine):
    def __init__(self, content, nCols = 6, engine= DicSearch):
        super().__init__(content, engine, nCols)
        self._runCallback = None
    
    def _callback(self, item):
        if(self._runCallback is None):
            print(self.searchSys.container[item])
        else: 
            return self._runCallback(item, self.searchSys.container[item])
        
    def setCallback(self, funcWith2Params):
        self._runCallback = funcWith2Params

class MultilineStringSearch(ISearchSystem):
    def __init__(self, content, allRes = False):
        self.allRes = allRes
        if(type(content) == str):
            content = content.splitlines()
        super().__init__(content)
    def wordSearch(self, word, case = False):
        return self._iterator(lambda val: ComparerDB.inCompare(leftIn=word, right=val, case=case))
    def pattern(self, patt):
        return self._iterator(lambda val: ComparerDB.regexSearch(regex=patt, word=val))
    def function(self, func):
        return self._iterator(func)
    def _iterator(self, condition):
        founds = []
        for i,val in enumerate(self.container):
            if(condition(val)):
                if(self.allRes):
                    founds.append(i)
                else:
                    return i
                    
        if(self.allRes):
            return founds

class FilesContentSearch(ISearchSystem):
    def __init__(self, filepaths):
        container = {path: MultilineStringSearch(self.getContent(path)) for path in filepaths}
        super().__init__(container)
    def wordSearch(self, word, case = False):
        return self._iterator(lambda key: self.container[key].wordSearch(word, case))
    def pattern(self, patt):
        return self._iterator(lambda key: self.container[key].pattern(patt))
    def function(self, func):
        return self._iterator(lambda key: self.container[key].function(func))
    def _iterator(self, condition):
        founds = []
        for key in self.container:
            found = condition(key)
            if(found is not None):
                founds.append((key, found + 1))
        return founds
    def getContent(self,path):
        return File.getFileContent(path).splitlines()
    
class FilesContentSearchEngine(SearchEngine):
    def __init__(self, filepaths, engine = FilesContentSearch, nCols = 6, callBackFunc = None):
        super().__init__(filepaths, engine, nCols)
        self._runCallback = callBackFunc
        def openApp(path, lineNr):
            app = NotepadAppTextOpener()
            app.setData(lineNr)
            app.openIt(path)
        if(callBackFunc is None):
            from FileDatabase import NotepadAppTextOpener
            self._runCallback = openApp

    def buttonName(self, item):
        return os.path.basename(item[0])
    
    def toolTip(self, item):
        return str(item[1])
    
    def displayItem(self,key, name, callbackFunc, tooltip=None):
        import ipywidgets as widgets
        from IPython.display import display
        s = super().displayItem(key, name, callbackFunc, tooltip)
        return widgets.HBox([s, widgets.Label(str(key[1]))])
    
    def _callback(self, resItem):
        self._runCallback(resItem[0], resItem[1])

class StringListSearchEngine(SearchEngine):
    def __init__(self, stringLisrt):
        class Temp(MultilineStringSearch):
            def __init__(self, contents):
                super().__init__(contents, True)
        super().__init__(stringLisrt, Temp)
    def buttonName(self, item):
        return "line " + str(item)
    def _callback(self, item):
        val = self.searchSys.container[item-3: item+3]
        print("\n".join(val))
        
class FilePathsSearchEngine(StringListSearchEngine):
    def _callback(self, item):
        File.openFile(self.searchSys.container[item])
    
    def buttonName(self, index):
        return os.path.basename(self.searchSys.container[index])
        
class UrlSearchEngine(DicSearchEngine):
    def __init__(self, urlDic, nCols = 5):
        super().__init__(urlDic, nCols)
    
    def toolTip(self, item):
        return self.searchSys.container[item]
    
    def _callback(self, key):
        from TreeDB import TreeDB
        TreeDB.openWebLink(self.searchSys.container[key])

class CodeDumperSearch:
    def __init__(self, container):
        self.container = container
    def search(self, word, case = False, reg = False):
        res = []
        for key in self.container:
            for i, line in enumerate(self.container[key]):
                if(ComparerDB.has(word, line, case, reg)):
                    res.append((key, i))
        return res
    
class CodeDumperEngine(SearchEngine):
    def __init__(self, content, nCols = 6):
        super().__init__(content, CodeDumperSearch, nCols)
        
    def buttonName(self, item):
        return item[0]
    
    def toolTip(self, item):
        return str(item[1] )
    
    def _callback(self, item):
        from ModuleDB import ModuleDB
        from IPython.display import display
        content = self.searchSys.container[item[0]][item[1]]
        display(ModuleDB.colorPrint('python', content))
        
class PdfSearch(FilesContentSearch):
    def getContent(self, path):
        from Pdf_Database import PDF
        return PDF.readPdf(path)
     
class PdfSearchEngine(FilesContentSearchEngine):
    def __init__(self, pdfs, cols = 6):
        super().__init__(pdfs, PdfSearch,cols)
    def _callback(self, resItem):
        from OpsDB import OpsDB
        from jupyterDB import jupyterDB
        from ModuleDB import ModuleDB
        file, pageNr = resItem
        k = jupyterDB.pickle().read("paths")
        urlPath = file.replace(os.sep, "/")
        fpu = f"file:///{urlPath}#page={pageNr}"
        browser = k['programs'][ModuleDB.laptopName()]['chrome']
        pa = f'"{browser}" "{fpu}"'
        OpsDB.cmd().onthread(pa)
        
class FoldersExplorerDisplayer(DicSearchEngine):
    def __init__(self, folders):
        super().__init__({os.path.basename(f):f for f in folders})
    def _callback(self, item):
        from ExplorerDB import ExplorerDB
        display(ExplorerDB.osFileExplorer(self.searchSys.container[item]))        

class GSearch:
    def __init__(self, container, searchFunc = None):
        self.container = container
        self.setSearchFunc(searchFunc)
        
    def search(self, word, case = False, reg = False):
        return self._search(word, self.container, case, reg) 
    
    def setSearchFunc(self, searchFunc):
        self._search = searchFunc
        if(self._search is None):
            self._search = GSearch._default
    
    def _default(word, container, case = False, reg = False):
        from ComparerDB import ComparerDB
        return GeneralSearchEngine.tools().iterate(container, 
                            ifFunc = lambda i, val, con: ComparerDB.has(word, val, case, reg))
    
class GeneralSearchEngine(SearchEngine):
    def __init__(self, container, searchFunc = None, callBackFunc = None, buttonNameFunc = None, 
                 toolTipFunc = None, nCols = 6 ):
        self._buttonFunc = buttonNameFunc
        self._callbackFunc = callBackFunc
        self._tooltipFunc = toolTipFunc
        super().__init__(container, GSearch,nCols)
        self.searchSys.setSearchFunc(searchFunc)
        
    def _callback(self, item):
        if(self._callbackFunc is None):
            print("No callback func is set")
        else:
            self._callbackFunc(item, self.searchSys.container)
        
    def buttonName(self, item):
        if(self._buttonFunc is None):
            return item
        return self._buttonFunc(item, self.searchSys.container)
    
    def toolTip(self, item):
        if(self._tooltipFunc is None):
            return item
        return self._tooltipFunc(item, self.searchSys.container)
    
    def tools():
        class Temp:
            def iterate(container, ifFunc, resAppender = lambda i, val, container: val):
                res = []
                for i,val in enumerate(container):
                    if(ifFunc(i, val, container)):
                        res.append(resAppender(i, val, container))
                return res
        return Temp
        


class ISearchEngine:
    def display(self, result, container):
        raise NotImplementedError("abstract method")
    
    def callback(self, key):
        raise NotImplementedError("abstract method")

class GSearchEngine:
    def __init__(self,searchSys:ISearch, engine:ISearchEngine):
        self.searchSystem = searchSys
        self.engine = engine
    
    def search(self, word, case = False, reg =False):
        res = self.searchSystem.search(word, case, reg)
        return self.engine.display(res)
        
class JupyterNotebookSE(ISearchEngine):
    def __init__(self,container =None,  callbackFunc = print, nCols= 6):
        self.container = container
        self._callbackFunc = callbackFunc
        self._nCols = nCols 
        
    def display(self, result):
        from WidgetsDB import WidgetsDB
        import ipywidgets as widgets
        disp = WidgetsDB.getGrid(self._nCols)
        for res in result:
            b = WidgetsDB.button(res, lambda x: self._callback(x, disp.output))
            disp.append(b)
    
    def _callback(self, itemBtn, resSect):
        with resSect:
            self.callback(itemBtn.description)
    
    def callback(self, key):
        self._callbackFunc(key)
        
class JupyterNotebookResultReplaceableSE(ISearchEngine):
    def __init__(self,container=None,callbackFunc = print, nCols= 6):
        self._callbackFunc = callbackFunc
        self._nCols = nCols 
        self.container =container
        
    def display(self, result):
        from WidgetsDB import WidgetsDB
        import ipywidgets as widgets
        output = WidgetsDB.searchEngine().resultWidget()
        output.searchRes.clear_output()
        display(widgets.VBox([output.searchRes,output.buttonRes]))
        with output.searchRes:
            display(WidgetsDB.getGrid(self._nCols, [self.displayItem(key= x, name=self.buttonName(x), 
                callbackFunc=lambda x: self._callback(x, output.buttonRes), tooltip=self.toolTip(x)) for x in result]))
        return output
    
    def _callback(self, itemBtn, resSect):
        resSect.clear_output()
        with resSect:
            self.callback(itemBtn._key)
    
    def callback(self, key):
        self._callbackFunc(key)
    def buttonName(self, item):
        return item
    
    def toolTip(self, item):
        return self.buttonName(item)
    
    def displayItem(self,key, name, callbackFunc, tooltip=None):
        from WidgetsDB import WidgetsDB
        b = WidgetsDB.mButton(name, key, callbackFunc)
        b.tooltip = tooltip
        return b
    
class JupyNbManyResults(ISearchEngine):
    def display(self, result):
        pass
    
class CmdSearchEngine(ISearchEngine):
    def __init__(self,container=None, callbackFunc = print, resultBeautifier = lambda x: x):
        self.parser = self.setupArgParser()
        self._callbackFunc = callbackFunc
        self.container = container
        self.resultBeautifier = resultBeautifier
        
    def setupArgParser(self):
        import argparse
        class ArgPar(argparse.ArgumentParser):
            def error(self,msg):
                print(msg)
        parser = ArgPar(description='command line search system')
        parser.add_argument('-f','--filter', help='filter result')
        parser.add_argument('-r','--range', nargs = 2,type=int, help='set result list ranges')
        parser.add_argument('-c','--callback',type =int, help='run callback func for index')
        parser.add_argument('-l','--list',action='store_true', help='command list')
        return parser

    def display(self, result):
        import re
        print(f"total number of results: {len(result)}")
        print(f"First 10 results are shown below: {len(result)}\n")
        ini, fi= 0, 9
        self.showResults(result, ini, fi)
        while True:
            inp = input()
            if(inp.strip() == ""):
                continue
            if(inp in [':q', 'exit']):
                break
            ar = self.parser.parse_args(re.split(" +", inp))
            if(ar.range):
                ini, fi = ar.range
                self.showResults(result, ini, fi)
            if(ar.list):
                self.showResults(result, ini, fi)
            if(ar.filter is not None):
                self.filterRes(result, ar.filter)
            if(ar.callback is not None):
                self.callback(result[ar.callback])
            
    def callback(self, key):
        self._callbackFunc(key)
        
    def filterRes(self,result, filtStr):
        from ComparerDB import ComparerDB
        res = []
        for i,val in enumerate(result):
            if(ComparerDB.has(filtStr, self.resultBeautifier(val), reg=True)):
                res.append((i, val))
        self._showRes(res)
        
    def showResults(self,result,fro, to):
        for i, res in enumerate(result[fro:to]):
            print(f"{fro+i}. {self.resultBeautifier(res)}")
            
    def _showRes(self,resultsWithIndex):
        for i, res in resultsWithIndex:
            print(f"{i}. {self.resultBeautifier(res)}")