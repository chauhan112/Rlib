import dill as pickle
import os
from LibPath import getPath

class SerializationDB:
    def pickleOut(dataStructure, outFileName):
        from CompressDB import CompressDB
        data = pickle.dumps(dataStructure)
        dataCompressed = CompressDB.content().compressToBinVal(data)
        with open(outFileName, "wb") as f:
            f.write(dataCompressed)

    def readPickle(filePath):
        from CompressDB import CompressDB
        with open(filePath, "rb") as f:
            binValCompressed = f.read()
        try:
            binVal = CompressDB.content().decompressFromBinVal(binValCompressed)
        except:
            binVal = binValCompressed
        return pickle.loads(binVal)

    def serializeProject(files, projectName):
        from ProjectSerialization import ProjectSerialization
        k = ProjectSerialization(files, projectName)
        k.archive()

    def deserializeProject(pklFile):
        pklFile = os.sep.join([resourcePath(), "project", pklFile])
        k = SerializationDB.readPickle(pklFile)
        k.restore()

class PickleDB:
    def __init__(self, name, addFunc):
        self.name = name
        self.addFunc = addFunc

    def read(self):
        return SerializationDB.readPickle(self.name)

    def overWrite(self,newData):
        SerializationDB.pickleOut(newData, self.name)

    def addValue(self, val):
        newVal = self.addFunc(self.read(), val)
        self.overWrite(newVal)
