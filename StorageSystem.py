from PickleCRUDDB import PickleCRUD
from Path import Path
from SerializationDB import SerializationDB
class GPickleCRUD(PickleCRUD):
    def _load(self):
        self.content = SerializationDB.readPickle(self.pklName)
        return self.content

    def _write(self):
        SerializationDB.pickleOut(self.content, self.pklName)

class _StorageSytem:
    def __init__(self):
        self.path = self._storagePath()
        self.mainPkl = GPickleCRUD(Path.joinPath(self.path, "main.pkl"))
        self.storageIndex = GPickleCRUD(Path.joinPath(self.path, "storageIndex.pkl"))

    def createAnIndex(self, updateStorage = False):
        from CryptsDB import CryptsDB
        idx = CryptsDB.generateUniqueId()
        if(updateStorage):
            self.storageIndex.add(idx, self._getStorage())
        return idx

    def _getStorage(self, newStorage=False):
        n = self.mainPkl.read(['totalNrOfStorage'])
        if(newStorage):
            n += 1
            self.mainPkl.add(['totalNrOfStorage'], n, overwrite=True)
        return f"storage{n}.pkl"

    def getDataStructureForIndex(self, index):
        file = Path.joinPath(self.path, self.storageIndex.read(index))
        return GPickleCRUD(file, [index])

    def _storagePath(self):
        from LibPath import getPath
        storagepath = Path.joinPath(resourcePath(), "StorageSystem")
        return storagepath

    def folder(self):
        Path.openExplorerAt(self.path)

    def readStorageNr(self, nr):
        return SerializationDB.readPickle(Path.joinPath(self.path, f"storage{nr}.pkl"))

class Properties:
    def sizeMaintain(self,):
        pass

class StorageSystem:
    def createAnIndex(updateLookUpTable=False):
        s = StorageSystem.management()
        return s.createAnIndex(updateLookUpTable)

    def dataStructureForIndex(idx):
        s = StorageSystem.management()
        return s.getDataStructureForIndex(idx)

    def management():
        return _StorageSytem()