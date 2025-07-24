from InterfaceDB import ISearchSystem
from useful.ComparerDB import ComparerDB
from FileDatabase import File
import os


class SearchSystem:
    pass
       
class ISearch:
    def search(self, word, case = False, reg = False):
        raise NotImplementedError("abstract method")
    def set_container(self, container):
        raise NotImplementedError("abstract method")
class ContainerSetable:
    def set_container(self, container):
        self.container = container      
class DicSearch(ContainerSetable):
    def __init__(self, container):
        self.set_container(container)
        self.set_search_in_type("all")
    def search(self, word, case = False, reg = False):
        if self._type == "key":
            return self.key(word, case, reg)
        elif self._type == "value":
            return self.value(word, case, reg)
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
    def set_search_in_type(self, typ):
        self._type = typ
    
class SearchEngine:
    def __init__(self,content =None,  searchSys = None, nCols=6):
        if searchSys is not None:
            self.set_search_sys(searchSys)
        if content is not None:
            self.set_content(content)
        self._make_layout(nCols)
    def _make_layout(self, nCols):
        from modules.SearchSystem.modular import JupyterResultDisplayer, DisplayNElement
        self.nCols = nCols + 1
        self._displayer_engine = JupyterResultDisplayer()
        self._displayer_engine.set_displayer_way(DisplayNElement())
        self._displayer_engine.set_callback(self._callback)
        self.set_tooltip(self.buttonName)

    def displayer(self, result):
        from modules.SearchSystem.modular import GDisplayableResult
        res = [GDisplayableResult(self.buttonName(ele), self._tooltip_func(ele), ele) for ele in result]
        self._displayer_engine.set_result(res)
        return self._displayer_engine.display()
        
    def get_search_result_layout(self,word, case = False, reg = False):
        result = self.searchSys.search(word, case, reg)
        from modules.SearchSystem.modular import GDisplayableResult
        res = [GDisplayableResult(self.buttonName(ele), self._tooltip_func(ele), ele) for ele in result]
        self._displayer_engine.set_result(res)
        return self._displayer_engine.get_result_layout()
        
    def _callback(self, result):
        raise NotImplementedError("Overload this function")

    def search(self, word, case = False, reg = False):
        result = self.searchSys.search(word, case, reg)
        self.displayer(result)

    def buttonName(self, item):
        return item

    def set_tooltip(self, func):
        self._tooltip_func = func

    def displayItem(self,key, name, callbackFunc, tooltip=None):
        from WidgetsDB import WidgetsDB
        b = WidgetsDB.mButton(name, key, callbackFunc)
        b.tooltip = tooltip
        return b
    def set_content(self, content):
        self.searchSys = self._searchSys(content)
    def set_search_sys(self, searchSys):
        self._searchSys = searchSys

    
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
class NestedDicSearch(ISearch):
    def search(self, word, case=False, reg=False):
        self._word = word
        res = ComparerDB.pickle_search(self._dic, self._default_compare_func, searchInKey=True)
        return res
    def set_container(self, dic: dict):
        self._dic = dic
    def _default_compare_func(self, con):
        if type(con) == str and type(self._word) == str:
            return self._word in con
        return self._word == con

class NestedDicSearchEngine(SearchEngine):
    def __init__(self, dic=None):
        self._make_layout(6)
        self.set_search_sys(NestedDicSearch())
        self.set_container(dic)
        self.set_callback_func(self._print_content)
    def set_search_sys(self, searchSys: ISearch):
        self.searchSys = searchSys
    def _callback(self, result):
        self._func(result)
    def set_callback_func(self, fucn):
        self._func = fucn
    def set_container(self, container):
        self.searchSys.set_container(container)
    def buttonName(self, ele):
        key, val = ele
        return "/".join(key)
    def _print_content(self, ele):
        print(ele)
class MultilineStringSearch(ISearchSystem, ContainerSetable):
    def __init__(self, content, allRes = False):
        self.allRes = allRes
        if(type(content) == str):
            content = content.splitlines()
        self.set_container(content)
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

class FilesContentSearch(ISearchSystem, ContainerSetable):
    def __init__(self, filepaths):
        container = {path: MultilineStringSearch(self.getContent(path)) for path in filepaths}
        self.filepaths = filepaths
        self.set_container(container)
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
    def __init__(self, filepaths=None, engine = FilesContentSearch, nCols = 6, callBackFunc = None):
        super().__init__(nCols = nCols)
        self.set_search_sys(engine)
        if filepaths is not None:
            self.set_content(filepaths)
        self.set_callback(self._openApp)
        if callBackFunc is not None:
            self.set_callback(callBackFunc)

    def buttonName(self, item):
        return os.path.basename(item[0])

    def toolTip(self, item):
        return str(item[0])

    def displayItem(self,key, name, callbackFunc, tooltip=None):
        import ipywidgets as widgets
        from IPython.display import display
        s = super().displayItem(key, name, callbackFunc, tooltip)
        return widgets.HBox([s, widgets.Label(str(key[1]))])

    def _callback(self, resItem):
        self._runCallback(resItem[0], resItem[1])

    def _openApp(self, path, lineNr):
        from FileDatabase import NotepadAppTextOpener
        app = NotepadAppTextOpener()
        app.setData(lineNr)
        app.openIt(path)

    def set_callback(self, func):
        self._runCallback = func

    
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
        try:
            return PDF.readPdf(path)
        except Exception as e:
            print(e)
            return []
     
class PdfSearchEngine(FilesContentSearchEngine):
    def __init__(self, pdfs, cols = 6):
        super().__init__(pdfs, PdfSearch,cols)
    def _callback(self, resItem):
        from OpsDB import OpsDB
        from jupyterDB import jupyterDB
        from ModuleDB import ModuleDB
        file, pageNr = resItem
        k = jupyterDB.pickle().read("paths")
        urlPath = os.path.abspath(file).replace(os.sep, "/")
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
        from useful.ComparerDB import ComparerDB
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
        output = WidgetsDB.searchEngine().resultWidget()
        output.searchRes.clear_output()
        output.display()
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
        from useful.ComparerDB import ComparerDB
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
