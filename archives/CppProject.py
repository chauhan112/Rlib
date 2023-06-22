import os
import re
from IPython.display import display, Markdown
import webbrowser
from Path import Path
from FileDatabase import File

class CppCodeRefactoring:
    def uncomment(self, scriptName):
        content = File.getFileContent(self.path + os.sep + scriptName)
        string = re.sub(r'/\*.*?\*/', " ",content.replace("\n"," skkssd ")).replace(" skkssd ","\n")
        string = re.sub(r'//.*', " ",string)
        string = re.sub(r'\n\s*\n', "\n",string)
        return string
    def searching(self,string, case = False, filt = []):
        filt = self.getCompleteFileNamesFromHints(filt)
        for file in self.headerFiles + self.scriptFiles:
            k = File.getFileContent(self.path + os.sep + file)
            if( not case):
                k = k.lower()
                string = string.lower()
            pos = k.find(string)
            if(pos is not -1):
                foundAtLineNumber = str(k[:pos].count("\n") + 1)
                self.addHistory(string, file ,foundAtLineNumber)
                if(not file in filt):
                    self.report(file, foundAtLineNumber)
    def getCompleteFileNamesFromHints(self,hints):
        k = []
        for f in hints:
            for file in self.headerFiles + self.scriptFiles:
                if(f.lower() in file.lower()):
                    k.append(file)
        return k
                
    def report(self, file ,foundAtLineNumber):
        print(file)
        print("line : " +foundAtLineNumber )
        print()              
    def getClassDiagram(self):
        print(self.structure)  
    def addHistory(self, keyword, file, lineNumber):
        try:
            self.searchHistory[keyword].add(file + ":" + lineNumber)
        except:
            self.searchHistory[keyword] = set([ file + ":" + lineNumber])
    def _removeLineWithHash(self, string):
        withoutHash = []
        for line in string.split("\n"):
            try:
                if (line.strip()[0] != '#' ):
                    withoutHash.append(line)
            except:
                pass
        return "\n".join(withoutHash)              
    def _projectSize(self):
        totalSize = 0
        for file in (self.headerFiles + self.scriptFiles):
            totalSize += os.path.getsize(self.path + os.sep + file)
        return str(int(totalSize/1024)) + " kb"     
    def generalize(self):
        totalLinesOfCode = 0
        for script in self.scriptFiles:
            totalLinesOfCode += len(self.uncomment(script).split("\n"))
        return totalLinesOfCode
    def getContent(self,scriptName):
        content = File.getFileContent(self.path + os.sep + scriptName)
        return Markdown("```c++\n" + f.read() + "\n```")   
    def colorPrint(self, string):
        return Markdown("```c++\n" + string + "\n```")
    def difference(self):
        return (self._diff(self.scriptFiles, self.headerFiles),
             self._diff(self.headerFiles, self.scriptFiles))
    def getSearchHistory(self):
        
        lis = ""
        for key in self.searchHistory:
            lis += "<li>{}</li>\n".format(key)
        ol = "<ol>{}</ol>".format(lis) 
        return Markdown(ol)
    def _diff(self, set1, set2):
        setX = [x.split(".")[0] for x in set2]
        dif = ""
        for fname in set1:
            if(fname.split(".")[0] not in setX):
                dif += "<li>{}</li>".format(fname)
        return dif
    def openFile(self,name, path = None): 
        if( path is None):
            path = self.path
        if ( os.path.isfile(path + os.sep +name) ):
            webbrowser.open(path + os.sep +name)
        else:
            print("file does not exits.")
class CppLexer:
    def dataStructuresFromClassPrototype(string,structure):
        
        # class
        structure['class'] += CppLexer.dataTypeParse(r"class .*\n*{(\n.*)*?\n};", string)
        #struct
        structure['struct'] += CppLexer.dataTypeParse(r"struct .*\n*{(\n.*)*?\n};", string)
        #enum
        structure['enum'] += CppLexer.dataTypeParse(r"enum .*\n*{(\n.*)*?\n};", string)
        #typedef 
        if("typedef" in string):
            structure['typedef'] += CppLexer.dataTypeParse(r"typedef struct\n*{(\n.*)*?\n} [A-Za-z]+;",string)
        return structure
    def dataTypeParse(regex,string):
        dataList = []
        matches = re.finditer(regex, string, re.MULTILINE)
        for match in matches:
            dataList.append(match.group())
        return dataList
class CppProject(CppCodeRefactoring):
    def __init__(self, path, name = None):
        if(name is None):
            name = os.path.split( path )[-1]
        self.path = path
        self.name = name
        self.scriptFiles = [os.path.basename(x) for x in Path.filesWithExtension("cpp", self.path, False)]
        self.headerFiles = [os.path.basename(x) for x in Path.filesWithExtension("h", self.path, False)]
        self.searchHistory = {}
        self.structure = {"class":[], "struct":[], "enum":[],"typedef":[]}
        self._dataStructures()        
    def libsUsed(self):
        libs = set([])
        for file in self.headerFiles + self.scriptFiles:
            content = self.uncomment(file)
            for line in content.split("\n"):
                if("#include" in line):
                    k = line.replace("#include","").strip().strip("<").strip(">").strip("\"").split("/")[-1]
                    libs.add(k)

        return list(libs)
    def getFilePath(self, fileName):
        return self.path + os.sep + fileName
    def _dataStructures(self):
        for file in self.headerFiles:
            content = self._removeLineWithHash(self.uncomment(file) )
            self.structure = CppLexer.dataStructuresFromClassPrototype(content, self.structure)
    def summarize(self):
        a, b = self.difference()
        val = '''
                #  <font face = "comic sans ms" color = "red">{}</font>
                ---
                ## <font face = "comic sans ms" color = "orange">cppfiles - headerfiles</font>
                <ol>{}</ol>

                ## <font face = "comic sans ms" color = "orange">headerfiles - cppfiles</font>
                <ol>{}</ol>
                <hr>

                ### <font face = "comic sans ms" color = "orange">Total lines of code ::</font> {}
                ### <font face = "comic sans ms" color = "orange">Total project size ::</font> {}
                ### <font face = "comic sans ms" color = "orange">No of classes :</font> {}
                ### <font face = "comic sans ms" color = "orange">No of libs class :</font> {}
            '''.format(self.name, a,b, self.generalize(), self._projectSize(), 
                       len(self.structure['class']), len(self.libsUsed()))
        val = val.strip().split("\n")
        val = [line.strip() for line in val]
        return Markdown("\n".join(val))