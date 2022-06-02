from NotebookDB import NotebookDB
from ListDB import ListDB
from WordDB import WordDB
from RegexDB import RegexDB

class CodeDumperDB:
    def getSummaryDBofNDaysBefore(nDaysBefore = 0):
        from SerializationDB import SerializationDB
        from Database import Database
        path = CodeDumperDB.name(nDaysBefore)
        codes = CodeDumperDB.inputLinesFromDumper(SerializationDB.readPickle(path))
        return Database.allRunCellDB(_ih = codes)

    def parseLines(cells):
        import ast
        p = []
        for cell in cells:
            try:
                p += ast.parse(cell).body
            except:
                pass
        return p

    def inputLinesFromDumper(dic):
        k = dic
        vals = []
        for key in k:
            if(type(k[key]) == dict):
                return CodeDumperDB.inputLinesFromDumper(k[key])
            elif(type(k[key]) == list):
                vals += k[key]
        return vals
    
    def name(nDaysEarlier = 0):
        from TimeDB import TimeDB
        return NotebookDB.outFilename(TimeDB.nDaysBefore(nDaysEarlier))
    
    def firstDay():
        class Date:
            def __init__(self):
                self.date = (2020,7,29)
            def day(self):
                return TimeDB.weekday(self.date)
        return Date()
            
class Parser:
    def __init__(self, content):
        self.content = content
        self.functions = []
        self.classes = []

    def getAllFunctions(self):
        self.functions = RegexDB.regexSearch("def .*:",self.content)
        return self.functions

    def getOnlyFunctionsName(self):
        if(len(self.functions) ==0):
            self.getAllFunctions()
        func = lambda x: x.split("(")[0][4:]
        return ListDB.flatten(list(map(func, self.functions)))

    def getClasses(self):
        self.classes = RegexDB.regexSearch("class .*:",self.content)
        return self.classes
    
    def allFunctionWithClasses(self):
        from jupyterDB import jupyterDB
        name = "fromFileImportClass"
        k = jupyterDB.pickle().read(name)
        return list(filter(lambda x: x.split(".")[0] in set(k.keys()),  
            map(lambda x: x.strip("("), RegexDB.regexSearch("\w+\.\w+\((.*\)\..*\))*", self.content))))

class CodeDumperAnalyser:
    def __init__(self):
        self.libpath = jupyterDB.Libs().path
        self.dumperPath = jupyterDB.codeDumper().path
        self.content = self._read()
        self._wordFreq = {}
        
    def _read(self):
        files = Path.filesWithExtension("pkl", self.dumperPath)
        cont = {}
        for f in files:
            cont[os.path.basename(f)] = SerializationDB.readPickle(f)
        return cont
    
    def usedFunctionFrequency(self):
        funcs = self.allFuncInLib()
        freq = self.allWordsFrequency()
        dic= { }
        for f in funcs:
            try:
                dic[f] = freq[f]
            except:
                dic[f] = 0
        return ListDB.sortDicBasedOnValue(dic)
    
    def allFuncInLib(self):
        files = Path.filesWithExtension("py", self.libpath)
        funcs = set([])
        for f in files:
            names = Parser(File.getFileContent(f)).getOnlyFunctionsName()
            funcs = funcs.union(set(names))
        return funcs
    
    def allWordsFrequency(self):
        if(len(self._wordFreq) != 0): 
            return self._wordFreq
        content = ListDB.dicOps().flatten(self.content)
        words = {}
        for key in content:
            for word in WordDB.tokenize("\n".join(content[key])):
                if word in words:
                    words[word] += 1
                else:
                    words[word] = 1
        self._wordFreq = words
        return words