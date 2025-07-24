from modules.SearchSystem.modular import JupyterResultDisplayer, DisplayNElement, GDisplayableResult
from useful.FileDatabase import NotepadAppTextOpener, File
import os
from useful.SerializationDB import SerializationDB
class PickleManyFilesSearch:
    def __init__(self):
        self._jrd = JupyterResultDisplayer()
        self._jrd.set_displayer_way(DisplayNElement())
        self._opener = NotepadAppTextOpener()
        self.set_callback(self._create_and_open)
    def search(self, word, case=False, reg=False):
        founds = []
        for f in self._line_map:
            found = self._line_map[f].search(word, case, reg)
            if found is not None:
                founds.append(GDisplayableResult(os.path.basename(f),f, (f, found)))
        self._jrd.set_result(founds)
        self._jrd.display()
        
    def set_pickle(self, pickle): # eg: D:\TimeLine\global\codes\py_files.pkl
        from useful.SearchSystem import MultilineStringSearch
        self._pickle = pickle
        self._content = SerializationDB.readPickle(self._pickle)
        self._line_map = {}
        a = True
        for f in self._content:
            if a and isinstance(self._content[f], MultilineStringSearch):
                self._line_map = self._content
                break
            else:
                a = False
                self._line_map[f] = MultilineStringSearch(self._content[f])
    def set_callback(self, func):
        self._jrd.set_callback(func)
    def _create_and_open(self, info):
        file, linenr = info
        self._opener.setData(linenr + 1)
        content = '\n'.join(self._line_map[file].container)
        if not os.path.exists(".pkl"):
            os.makedirs('.pkl')
        basename = os.path.basename(file)
        name = os.sep.join(['.pkl', basename])
        File.overWrite(name, content)
        self._opener.openIt(name)
        
    