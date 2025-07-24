import os
from LibPath import dumperPath

class CodeLogger:
    def __init__(self):
        self.content = {}
        self._loaded = False
        self._prev_path = None
    def load(self):
        ouputFile = self.getFilePath()
        if(os.path.exists(ouputFile)):
            self.content = SerializationDB.readPickle(ouputFile)
        self._loaded = True
    def getFilePath(self):
        from TimeDB import TimeDB
        import datetime
    
        fileName = ".".join(TimeDB.getTimeStamp(date).split(", ")[::-1]).replace(".", "_") + '.pkl'
        yearPath = os.sep.join([dumperPath(), f'{datetime.datetime.now().year}'])
        filePath = os.sep.join([yearPath, fileName])
        return filePath
    def dump(self, _ih):
        device_id, nb_id = self.get_id()
        if not self._loaded:
            self.load()
        if(device not in self.content):
            self.content[device]= {}
        self.content[device][nb_id] = _ih
        ouputFile = self.getFilePath()
        SerializationDB.pickleOut(self.content, ouputFile)
        if ouputFile != self._prev_path:
            if self._prev_path is not None:
                _ih.clear()
            self._prev_path = ouputFile
    def get_id(self):
        from ModuleDB import ModuleDB
        from useful.CryptsDB import CryptsDB
        device = ModuleDB.laptopName()
        if(NotebookDB.id_ is None):
            NotebookDB.id_ = CryptsDB.generateUniqueId()
        id_ = NotebookDB.id_
        return device, id_