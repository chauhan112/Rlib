import os
from modules.Explorer.displayer import FileExplorerDisplayer
from modules.Explorer.model import ZipFileExplorer, ExplorerUtils

class OldZipFileExplorerDisplayer(FileExplorerDisplayer):
    def __init__(self, zipPath, explorer = ZipFileExplorer):
        if(not zipPath.endswith(".zip")):
            raise IOError("Not valid zip file")
        super().__init__(zipPath, explorer, "Zip File Explorer")
    def render(self):
        self.displayLog("")
        self._unobserveWidgets()
        folders, files = self.explorer.dirList()
        folders = list(folders)
        self.inputArea.dirList.options = ExplorerUtils.dirsWithIcon(folders) + files
        self.inputArea.pathsList.options = self.dropDownPaths()
        self._observeWidgets()
    
    def dropDownPaths(self):
        vals = self.explorer.currentPath.split(self.explorer.sep)
        dropList = []
        vals.pop()
        for _ in range(len(vals)):
            dropList.append(self.explorer.sep.join(vals))
            vals.pop()
        return dropList

    def displayFileElement(self, change):
        self.extractFile()
        if(self.getSelectedFile() == ''):
            self.displayLog('No file selected')
        else: 
            try:
                fpath = self.explorer.sep.join([self.explorer._extractingPath, 
                    self.explorer.currentPath, self.getSelectedFile()])
                with self.outputArea:
                    self.displayer.displayPath(fpath)
            except Exception as e:
                self.displayLog(str(e))

    def copyPath(self, k):
        from ClipboardDB import ClipboardDB
        self.extractFile()
        fileName = self.getSelectedFile()
        p = self.explorer._extractingPath + self.explorer.sep + self.explorer.currentPath
        if(fileName != ''):
            p += self.explorer.sep + fileName
        ClipboardDB.copy2clipboard(os.path.abspath(p))
        self.displayLog(f"copied Path:{p}")
    
    def extractFile(self):
        file = self.getSelectedFile()
        if(file == ''):
            return
        self._extractFileIfNotExtractedYet(file)

    def _extractFileIfNotExtractedYet(self, file):
        p = self._getExtractedFilePath(file)
        if(not os.path.exists(os.path.abspath(p))):
            self.explorer.extract(file)

    def _getExtractedFilePath(self, filename):
        return self.explorer.sep.join([self.explorer._extractingPath, self.explorer.zipPath , filename])

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

class ZipFileExplorerDisplayer(OldZipFileExplorerDisplayer):
    def __init__(self, zipPath):
        super().__init__(zipPath, ZipExplorerWithLargeNumberOfContent)
    
    def setSectionSize(self, size):
        self.explorer.sectionSize = size