from SerializationDB import SerializationDB
from ListDB import ListDB
import os
class DictionaryCRUD:
    def __init__(self, filePaht=None):
        self._file_path =filePaht
        self.set_location([])
    def set_file(self, filepath: str):
        self._file_path = filepath
        if not os.path.exists(self._file_path):
            print("file does not exists")
    def add(self, key, value=None, overwrite = False):
        if value is None:
            from ClipboardDB import ClipboardDB
            value = ClipboardDB.getText()
        try:
            self.read(key)
            if(not overwrite):
                print('value already exists')
                return
        except:
            pass
        loc = self._LocFromkey(key)
        ListDB.dicOps().addEvenKeyError(self._content, loc, value)
        self.write(self._content)
    def set_location(self, location: list):
        if type(location) != list:
            location = [location]
        self._location = location
    def read(self, key= []):
        self.getContent()
        loc = self._LocFromkey(key)
        val = ListDB.dicOps().get(self._content, loc)
        return val
    def getContent(self):
        self._content = SerializationDB.readPickle(self._file_path)
        return self._content
    def _LocFromkey(self, key):
        if(type(key) == list):
            return self._location + key
        return self._location + [key]
    def write(self, content):
        SerializationDB.pickleOut(content, self._file_path)
    def delete(self, key):
        self.getContent()
        loc = self._LocFromkey(key)
        ListDB.dicOps().delete(self._content, loc)
        self.write(self._content)
