from OpsDB import IOps
import os, random
from useful.CryptsDB import CryptsDB

class RandomPathGenerator(IOps):
    def __init__(self, length=5, folders=[], files=[] ):
        self.length = length
        self.folders = folders
        self.files = files
        ext = [".txt", '.py', '.java', '.cpp']
        from useful.CryptsDB import CryptsDB
        if len(folders) == 0:
            self.folders = [CryptsDB.generateRandomName(5) for _ in range(5)]
        if len(files) == 0:
            self.files = [CryptsDB.generateRandomName(5) + random.choice(ext) for _ in range(5)]
    def execute(self):    
        path= []
        ff = self.files + self.folders
        for i in range(self.length):
            selected = random.choice(ff)
            path.append(selected)
            if len(selected.split(".")) == 2:
                break
        return '/'.join(path)

class RandomFileFolderStructure(IOps):
    def __init__(self, number_of_iter = 5, initialState = None):
        self.iter_nr = number_of_iter
        self.dic = initialState
        if initialState is None:
            self.dic={'folders':{}, 'files':[]}
        
    def execute(self):
        val = self.dic
        for _ in range(self.iter_nr):
            val = Path2DictionaryStructure(RandomPathGenerator().execute(), val).execute()
        return val

class Path2DictionaryStructure(IOps):
    def __init__(self, path, dic = {}):
        self.path = path
        self._dic = dic 
   
    def execute(self):
        loc = self.path.replace("/", os.sep).split(os.sep)
        val = self._dic
        for fol in loc:
            if len(fol.split('.')) == 2:
                val['files'].append(fol)
                break
            else:
                if fol not in val['folders']:
                    val['folders'][fol] = {'folders':{}, 'files':[]}
                val = val['folders'][fol]
        return self._dic