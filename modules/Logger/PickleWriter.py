from ListDB import ListDB
from SerializationDB import SerializationDB
from modules.Logger.Interfaces import IDumperWriter
import os

class PickleWriter(IDumperWriter):
    def __init__(self, path2Storage,overwrite =False):
        self.path = path2Storage
        if(not os.path.exists(self.path)):
            self.content = {}
            self._write()
        self.readAll()
        self.overwrite= overwrite
    def readAll(self):
        from SerializationDB import SerializationDB
        self.content= SerializationDB.readPickle(self.path)
        return self.content
    def _write(self):
        from SerializationDB import SerializationDB
        SerializationDB.pickleOut(self.content, self.path)
    def delete(self, loc):
        loc = self._makeLoc(loc)
        self.readAll()
        ListDB.dicOps().delete(self.content, loc)
        self._write()
    def add(self, loc, val):
        loc = self._makeLoc(loc)
        try:
            self.read(loc)
            if(not self.overwrite):
                print('value already exists')
                return
        except:
            pass
        ListDB.dicOps().addEvenKeyError(self.content, loc, val)
        self._write()
    def read(self, loc):
        loc = self._makeLoc(loc)
        self.readAll()
        val = ListDB.dicOps().get(self.content, loc)
        return val
    def _makeLoc(self,loc):
        if(type(loc)== str):
            return [loc]
        return loc
