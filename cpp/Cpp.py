import re
from IPython.display import display, Markdown
import os
from LibPath import getPath
from WordDB import WordDB
from GraphDB import GraphDB
from FileDatabase import File
from Path import Path

class Cpp:
    def uncomment(content):
        string = re.sub(r'/\*.*?\*/', " ",content.replace("\n"," skkssd ")).replace(" skkssd ","\n")
        string = re.sub(r'//.*', " ",string)
        string = re.sub(r'\n\s*\n', "\n",string)
        return string
    
    def libsUsed(content):
        content = Cpp.uncomment(content)
        libs = set([])
        for line in content.split("\n"):
            if("#include" in line):
                k = line.replace("#include","").strip().strip("<").strip(">").strip("\"").split("/")[-1]
                libs.add(k)
        return list(libs)
    
    def variablesUsed(content):
        content = content.split("\n")
        variables = {}
        def exceptionCheck(val):
            exceptions = ["()", "void", "#", "public"]
            for e in exceptions:
                if(e in val):
                    return False
            return True
        for line in content:
            lineTokens = re.sub(" +", " ", line).strip().split(" ")
            if(len(lineTokens) == 2 and exceptionCheck(" ".join(lineTokens))):
                variables[lineTokens[1]] = lineTokens[0]
        return variables
    
    def createCppClass(className):
        basename = os.path.basename(className)
        contentH = """
#pragma once


class {basename}{{
private:

public:
    {basename}();
    ~{basename}();
}};
        """.strip().format(basename = basename)

        contentCpp = """
#include "{basename}.h"


{basename}::{basename}(){{

}}
{basename}::~{basename}(){{
    
}}
        """.strip().format(basename = basename)
        if(not className.endswith(".cpp")):
            className = className + ".cpp"
        File.createFile(className, contentCpp)
        File.createFile(className[:-4] + ".h", contentH)
        
    def createFunction(func_name, file_path, returnTyp ="void" , className =None, typ = "public"):
        def addToHeader(filepath,func_name,typ = "public", returnTyp ="void"):
            header = getHeaderFile(filepath)
            content = File.getFileContent(header)
            nu = WordDB.searchWordWithRegex(typ + ":",content)
            newContent = ""
            if(len(nu) != 0):
                n = nu[-1][-1]
                newContent += content[:n] + "\n"  +"    " + returnTyp+ " " + func_name + ";" + content[n:]
            File.overWrite(header, newContent)

        def getHeaderFile(name):
            path = os.path.dirname(name)
            headers = Path.filesWithExtension("h", path)
            name = os.path.basename(name)[:-3] +  "h"
            h = list(filter(lambda x:  name  in x, headers))
            if(len(h) == 0):
                raise IOError("No Header file found")
            if(len(h) > 1):
                print(h)
                raise IOError("More header files found")
            return h[0]
        if(className is None):
            className = os.path.basename(file_path).split(".")[0]
        content = File.getFileContent(file_path)
        returnVar = ""
        if(returnTyp != "void"):
            returnVar = returnTyp + " r;\n\n    return r;"
        content += "\n" + returnTyp  + " " + className + "::" + func_name + "{\n    " +returnVar +"\n}"
        
        File.overWrite(file_path, content)
        addToHeader(file_path, func_name, typ=typ, returnTyp = returnTyp )

    def removeStringsCpp(text):
        text = Cpp.uncomment(text)
        text = text.replace('\\"', "[cm4723]").replace("\\'", "[cm4724]")
        return WordDB.getRemainingContent('".*?"', text)

    def visualizeTheClassConnectionFromSourceFiles(cppCodes):
        userbuildLibs = set([os.path.basename(k)[:-4] for k in cppCodes])
        def tokenizer(removedStringNComments):
            return [(removedStringNComments[i:j],[i,j]) for i, j in 
                    WordDB.searchWordWithRegex("[a-zA-Z_]+", removedStringNComments)]
        classConnection = {}
        for f in cppCodes:
            content = File.getFileContent(f)
            tokens = set([t[0] for t in tokenizer(content)])
            classConnection[os.path.basename(f)[:-4]] = tokens.intersection(userbuildLibs)
        conn = [[(d,k) for k in classConnection[d] if d != k] for d in classConnection]

        nconn = []
        for v in conn:
            nconn += v
        GraphDB.plotNodes(nconn)
    def getAllClassesName(pathToProject):
        files = Path.filesWithExtension("h", pathToProject) + Path.filesWithExtension("cpp", pathToProject)
        classes = []
        for h in files:
            content = File.getFileContent(h)
            for f in WordDB.searchWordWithRegex("(?<=class )[a-zA-Z_]+", content):
                classes.append(content[f[0]:f[1]])
        return classes

    def copyUtils(targetPath):
        Path.copyFiles(["utils.cpp", "utils.h"], targetPath, Path.joinPath(getPath(), "cpp"))

    def getVariableLinesFromFile(file):
        import re
        content = File.getFileContent(file)
        potentialVaribaleLines = list(filter(lambda x: x.strip().endswith(";"),Cpp.uncomment(content).splitlines()))
        variableLines = list(filter(lambda x: not x.strip().endswith(");"), potentialVaribaleLines))
        variableLines = list(map(lambda x: x.strip().strip(";"), variableLines))
        variableLines = list(filter(lambda x: len(x) > 3, variableLines))
        return variableLines
    
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
        
    def runCppCode(content = None):
        if(content is None):
            print("Give cell number to run or content")
        from CryptsDB import CryptsDB
        from OpsDB import OpsDB
        name = CryptsDB.generateRandomName(10) + ".cpp"
        File.createFile(name, content)
        OpsDB.cmd().run(["g++ "+ name])
        out = OpsDB.cmd().run(["a.exe"])
        File.deleteFiles([name, "a.exe"])
        return out