from Path import Path
from SearchSystem import DicSearch
class IdeasSearchEngine:
    def __init__(self):
        from LibsDB import LibsDB
        from modules.SearchSystem.modular import JupyterResultDisplayer, DisplayNElement
        self.set_folder(Path.joinPath(LibsDB.cloudPath(), "Global", "logger", "ideas"))
        self._jrd = JupyterResultDisplayer()
        self._jrd.set_displayer_way(DisplayNElement())
        self._jrd.set_callback(self._print_content)
    def set_folder(self, path:str):
        self._path = path
        self._files = Path.filesWithExtension("txt", self._path)
        self._content = {}
        for p in self._files:
            self._content[p] = DicSearch(self._read(p))
        
    def search(self, word, case=False, reg=False):
        from modules.SearchSystem.modular import GDisplayableResult 
        founds = []
        for f in self._content:
            found = self._content[f].search(word, case, reg)
            if len(found) != 0:
                [founds.append(GDisplayableResult(k, f, (k, self._content[f]))) for k in found]
        self._jrd.set_result(founds)
        self._jrd.display()
    def _read(self, path):
        from modules.Logger.TextWriter import TextWriter, DuplicatableSameKeyContentParser, TextParser
        tw = TextWriter()
        tp =TextParser(path)
        tp.set_content_parser(DuplicatableSameKeyContentParser())
        tw.set_parser(tp)
        return tw.readAll()
    def set_callback(self, func):
        self._jrd.set_callback(func)
    def _print_content(self, info):
        ek, en = info
        txt = en.container[ek]
        print(" ".join(txt.splitlines()))