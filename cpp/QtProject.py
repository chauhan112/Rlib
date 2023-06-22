import os
from Path import Path
class Project:
    def __init__(self, path):
        self.path = path
        self.proFile = None
        
    def createFile(self, name, folder = ""):
        from cpp.Cpp import Cpp
        Path.joinPath(self._relPath(folder), name).strip("\\")
        Cpp.createCppClass(Path.joinPath(self.path, Path.joinPath(self._relPath(folder), name).strip("\\")))
        self.addTopPro(name, folder)
        
    def _relPath(self, key):
        if(key == ""):
            return key
        folders = ['controller', 'views', 'models']
        vals = []
        for f in folders:
            if(key in f):
                vals.append(f)
        if(len(vals) == 1):
            return vals[0]
        raise IOError("Not unique folder found")
        
    def addTopPro(self, name, folder):
        from RegexDB import RegexDB
        from WordDB import WordDB
        from FileDatabase import File

        name = self._relPath(folder) + "/" + name
        name = name.strip("/")
        proFile = self.proFile
        if(self.proFile is None):
            proFile = self.path + os.sep + os.path.basename(self.path) + ".pro"
        text = File.getFileContent(proFile)
        c = WordDB.searchWordWithRegex(RegexDB.lookBehind("HEADERS \+= ", "\n"), text)[0][0]
        h = WordDB.searchWordWithRegex(RegexDB.lookBehind("RESOURCES \+= ", "\n"), text)[0][0]
        newText = ""
        shift = 0
        newText += text[:c - shift] 
        newText += "    "+ name + ".cpp \\n"
        newText += text[c-shift:h-shift] 
        newText += "    "+ name + ".h \\n"
        newText += text[h-shift:]
        File.overWrite(proFile, newText)
    def folder(self):
        Path.openExplorerAt(self.path)

    def setProFileName(self, name):
        self.proFile = self.path + os.sep + name 
        if(not self.proFile.endswith(".pro")):
            self.proFile += ".pro"