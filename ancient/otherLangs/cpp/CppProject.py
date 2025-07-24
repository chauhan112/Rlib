from ancient.otherLangs.cpp.Cpp import Cpp
from useful.Path import Path
from useful.FileDatabase import File
from IPython.display import Markdown
from useful.SearchSystem import FilesContentSearchEngine
import os
from ancient.CodeDB import CodeDB

class CppProject:
    def __init__(self, path, name = None):
        self.headers = Path.filesWithExtension("h", path)
        self.cpps = Path.filesWithExtension("cpp", path)
        self.name = name
        self.path = path
        if(name is None):
            self.name = os.path.basename(path)
        self.searchHistory = {}
        self.db = FilesContentSearchEngine(self.headers + self.cpps, nCols=5)
        self.codeModel = CodeDB.analyseComplexityAndLOC(self.headers + self.cpps)
        
    def search(self, word,case = True, reg = False):
        self.db.search(word, case, reg)
        
    def libsUsed(self):
        libs = []
        for file in self.headers + self.cpps:
            libs += Cpp.libsUsed(File.getFileContent(file))
        return set(libs)
    
    def summarize(self):
        filesNr = len(self.headers + self.cpps)
        linesNr = self.codeModel.totalLoc()
        size = Path.getSize(self.headers + self.cpps)
        libsNr = len(self.codeModel.classModel.read().allClasses())
        val = f'''
                #  <font face = "comic sans ms" color = "red">{self.name}</font>
                ---
                
                ### <font face = "comic sans ms" color = "orange">Total lines of code ::</font> {linesNr}
                ### <font face = "comic sans ms" color = "orange">Total project size ::</font> {size}
                ### <font face = "comic sans ms" color = "orange">No of files :</font> {filesNr}
                ### <font face = "comic sans ms" color = "orange">No of classes :</font> {libsNr}
            '''
        val = val.strip().split("\n")
        val = [line.strip() for line in val]
        return Markdown("\n".join(val))
    
    def folder(self):
        Path.openExplorerAt(self.path)
        
    def cmd(self, moreCommands=[]):
        from useful.OpsDB import OpsDB
        OpsDB.cmd().onthread(["c:", f'cd "{self.path}"', "start"])