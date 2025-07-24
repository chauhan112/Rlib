from useful.jupyterDB import jupyterDB
from useful.ExplorerDB import ExplorerDB
from useful.SerializationDB import SerializationDB
import os
from useful.Path import Path
from useful.FileDatabase import File

class ICloudCommand:
    def act(self):
        raise NotImplementedError('abstract method')

class ConflictedFileList(ICloudCommand):
    def __init__(self, conflictedDir):
        self.path = conflictedDir
    
    def act(self):
        from useful.Path import Path
        files = Path.getFiles(self.path, False)
        files = list(filter(lambda x: "conflicted copy" in x, files))
        return files

class ConflictedBaseFile(ICloudCommand):
    def __init__(self, filePath):
        self.path = os.path.abspath(filePath)
    def act(self):
        from useful.RegexDB import RegexDB
        return RegexDB.regexSearch(RegexDB.lookBehind(" \(conflicted copy", ".*"),
                                   self.path)[0] + ".pkl"

class ISolveConflictedFile:
    def setPath(self, filePath):
        self.file = os.path.abspath(filePath)
    def solve(self):
        raise NotImplementedError('abstract method')
    
class CodeDumperConflictSolver(ISolveConflictedFile):
    def solve(self):
        from useful.SerializationDB import SerializationDB
        baseFile = ConflictedBaseFile(self.file).act()
        mainVal = SerializationDB.readPickle(baseFile)
        conVal = SerializationDB.readPickle(self.file)
        
        mergedVal = self.fixContent(conVal, mainVal)
        condition = self.verify(mergedVal, conVal) and self.verify(mergedVal, mainVal)
        if(not condition):
            print('Needs to be resolved manually')
        else:    
            SerializationDB.pickleOut(mergedVal, baseFile)
            File.deleteFiles([conflictedFile])
    
    def fixContent(self):
        for laptopName in conVal:
            if(laptopName not in mainVal):
                mainVal[laptopName] = conVal[laptopName]
                continue

            tempVal = conVal[laptopName]
            for sessionid in tempVal:
                if(sessionid not in mainVal[laptopName]):
                    mainVal[laptopName][sessionid] = conVal[laptopName][sessionid]
                    continue
                conList = tempVal[sessionid]
                mainList = mainVal[laptopName][sessionid]
                mainVal[laptopName][sessionid] = self.update(conList, mainList)
        return mainVal
    
    def update(self,list1, list2):
        if(len(list1) >= len(list2)):
            return list1
        else:
            return list2
    
    def verify(self, mergedVal, againstVal):
        for com in againstVal:
            for ssid in againstVal[com]:
                for i, line in enumerate(againstVal[com][ssid]):
                    if(line != mergedVal[com][ssid][i]):
                        return False
        return True
    
class LibSizeConflictSolver(ISolveConflictedFile):
    def solve(self):
        from useful.SerializationDB import SerializationDB
        baseFile = ConflictedBaseFile(self.file).act()
        base = SerializationDB.readPickle(baseFile)
        val = set(SerializationDB.readPickle(self.file)['libSize']).union(
            set(base['libSize']))
        base['libSize'] = sorted(val, key=lambda x: self.keyForSorting(x[0]))
        Path.delete([self.file])
        SerializationDB.pickleOut(base, baseFile)
    def keyForSorting(self, val):
        a, b, c = val.split(" ")
        date = list(map(lambda x: int(x), b.split(".")))
        time = list(map(lambda x: int(x), c.split(":")))
        days = date[2]*365 + date[1]*30 + date[0]
        secs = time[0]* 3600 + time[1]*60 + time[0]
        return days*3600*24 + secs
        
class ScieboDB:
    def solveConflicts():
        solvers = {
            jupyterDB.pickle().path() : LibSizeConflictSolver(),
            jupyterDB.codeDumper().path : CodeDumperConflictSolver()
        }
        for path in solvers:
            for conflictedF in ConflictedFileList(path).act():
                solvers[path].setPath(conflictedF)
                solvers[path].solve()