import os
class LatexFileExplorer:
    def __init__(self):
        pass
    
    def showTexFiles(self):
        pass
from enum import Enum
FileOpener = Enum("FileOpener","texWork Notepad")

class LatexDocument(LatexFileExplorer):
    def __init__(self, filename):
        from useful.TimeDB import TimeDB
        from useful.CryptsDB import CryptsDB
        
        self.content = {}
        self.header = ""
        self._path, self._backUpPath = self.getWorkingPath(filename)
        self.setHeader()
     
    def getWorkingPath(self, path):
        if(os.path.exists(path)):
            print(path +' already exist. Reading the exisiting file')
            self.content = SerializationDB.readPickle(path)
            return path, path.replace(".tex", ".pkl")
        
        setUpPath = path + ".tex"
        setUpPath = setUpPath.replace(".tex.tex", ".tex")
        basename = os.path.basename(setUpPath)
        baseDir = os.path.dirname(setUpPath)
        tempFolder =  CryptsDB.generateRandomName()
        tPath = Path.joinPath(baseDir, tempFolder).strip(os.sep)
        os.mkdir(tPath)
        
        newPath = Path.joinPath(tPath, basename)
        pklPath = newPath.replace(".tex",".pkl")
        
        return newPath, pklPath
        
    def setHeader(self, options = ["article"]):
        for opt in options:
            self.header += LatexOps.header(opt)
    
    def add2Content(self, text):
        if(text == ""):
            return
        self.content[TimeDB.today()] = text + "\n"
        self._backUp()
        
    def showChangesMade(self):
        pass
    
    def deleteChange(self, changeNr):
        pass
    
    def updateChange(self, changeNr):
        pass
    
    def getContent(self):
        txt = self.header + "\n"
        txt += "\\begin{document}\n"
        for c in self.content.values():
            txt += c + "\n"
        txt += "\\end{document}"
        return txt
    
    def addInclude(self, typ):
        pass
    
    def _backUp(self):
        SerializationDB.pickleOut(self.content, self._backUpPath)
        
    def openFile(self, typ = FileOpener.texWork):
        from useful.OpsDB import OpsDB
        prg = Path._programPaths()#['texWorks']
        tex = prg["texWorks"]
        pah = prg["notepad++"]
        notepad= f'"{pah}"'+' "{}" -n{}'
        st = notepad.format(self._path, "")
        if(typ == FileOpener.texWork):
            st = f'"{tex}"' +  " " + f'"{self._path}"'
        OpsDB.cmd().onthread([st])
    
    def _write(self):
        from useful.FileDatabase import File
        File.overWrite(self._path, self.getContent())
        


class TextOps:
    def bold(text):
        pass
    
    def table(arr):
        pass
    
    def emphasis(text):
        pass
    
    def italic(text):
        pass
    
    def underline(text):
        pass
    
    def color(text):
        pass

    def center(text):
        return f'\\begin{{center}}\n{text}\n\\end{{center}}'
class MathOps:
    def fraction( num= "", deno = ""):
        pass
    
    def limit(top = "", bottom = "", expression = ""):
        pass
    
    def sumSeries(top = "", bottom = "", expression = ""):
        pass