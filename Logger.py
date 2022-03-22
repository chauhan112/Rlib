from datetime import timedelta, datetime
from PickleCRUDDB import PickleCRUD
from ListDB import ListDB
from SerializationDB import SerializationDB
from jupyterDB import jupyterDB

def downLoadFile(url, path):
    pass
    
class FoodLogger:
    def __init__(self):
        self.outPklFile = PickleCRUD('LifeLogs')
        self.category = 'eating'
        self.dumpingPath = jupyterDB.resource().getPath('recycleBin\\eatingDelete.pkl')
        self.recyleBin = {}
        raise IOError("needs testing")
    
    def logEating(self,name, time, content = "",date = 0):
        date = TimeDB.getTimeStamp(date)
        if(date not in self.outPklFile.data[self.category]):
            self.outPklFile.data[self.category][date] = {}
        self.outPklFile.data[self.category][date][time] = {'name':name, 'content': content}
        self.outPklFile._write(self.outPklFile.data)
    
    def showLog(self,date = 0):
        date = TimeDB.getTimeStamp(date)
        return self.outPklFile.data[self.category][date]

    def delete(self, pos = []):
        self.recyleBin = {'data':ListDB.dicOps().get(self.outPklFile.data, pos),
                          'pos': pos}
        ListDB.dicOps().delete(self.outPklFile.data, pos)
        SerializationDB.pickleOut(self.recyleBin, self.dumpingPath)
    
    def _restore(self):
        if(self.recyleBin is None):
            print("nothing to restore")
            return
        ListDB.dicOps().add(self.outPklFile.data, self.recyleBin['pos'], self.recyleBin['data'])
    
    def _restoreFromFile(self, path = None):
        if(path is None):
            path = self.dumpingPath
        self.recyleBin = SerializationDB.readPickle(path)
        self._restore()
        
class FoodBuyingSuggestion:
    def __init__(self, algorithm = ISuggestionAlgorithm()):
        self.algorithm = algorithm
        
    def suggest(self):
        pass
    
    def logBoughtStuff(self, namesWithPrice = {}):
        """namesWithPrice = {'potatoes' : {'total price': 2.15, 'quantity': 1 pkg},
        'brinjal': {'total price': ** , 'quantity' :3}}"""
        pass
      
class ISuggestionAlgorithm:
    def __init__(self, data = None):
        self.data = data
        self._result = []
        
    def setData(self, data):
        self.data = data
    
    def logics(self):
        raise IOError("overload this function")
    
    def getResults(self):
        self.logics()
        return self._result
        
class EatingExplorationSuggestion(ISuggestionAlgorithm):
    def logics(self):
        import random
        containerSet = set(container)
        alreadyPerformedSet = set(alreadyPerformed)
        left = containerSet.difference(alreadyPerformedSet)
        operateOn = list(left)
        if(len(left) == 0):
            operateOn = container
        return list(set([random.choice(operateOn) for i in range(suggestionSize)]))

class UsageEstimationSuggestion(ISuggestionAlgorithm):
    def __init__(self, data = None, extraData = None):
        super().__init__(data)
        self.extraInfo = extraData
        
    def logics(self):
        """codes which use last purchase date and use it predict the finish date"""
    

class NumberOfWidgetsLogger:
    storageID = "102fba78bb724d518a3ab79c7d854db7"
    def __init__(self, notebookId):
        import ipywidgets as widgets
        self.anInstance = widgets.Text()
        self.noteBookId = notebookId

    def log(self):
        from TimeDB import TimeDB
        (y,m,d), (hr, mi, ss) = TimeDB.today()
        pkl = NumberOfWidgetsLogger._read()
        pkl.add([self.noteBookId, f'{y}_{m}_{d} hour:{hr}'], len(self.anInstance.widgets))
        
    def _read():
        from StorageSystem import StorageSystem
        return StorageSystem.dataStructureForIndex(NumberOfWidgetsLogger.storageID)

class ForestTreeLogger:
    storageId= '9f90c36cb0774aa3953c2fa618f0b61b'
    def __init__(self):
        self.forestPath = self._path()

    def _path(self):
        from Path import FrequentPaths
        return FrequentPaths.pathAsDic()['forest']
        
    def fileNodes(self):
        from Path import Path
        files = Path.filesWithExtension("drawio", self.forestPath)
        relLoc = {tuple(x.replace(self.forestPath, "").strip(os.sep).split(os.sep)): x for x in files}
        return relLoc
    
    def _read():
        from StorageSystem import StorageSystem
        return StorageSystem.dataStructureForIndex(ForestTreeLogger.storageId)
    
    def log(self):
        from TimeDB import TimeDB
        from FileDatabase import File
        day,_ = TimeDB.today()
        pkl = ForestTreeLogger._read()
        filesLoc = self.fileNodes()
        for f in filesLoc:
            pkl.add([f, day], File.size(filesLoc[f]))

class Logger:
    def __init__(self):
        pass
        
    def log(self):
        pass