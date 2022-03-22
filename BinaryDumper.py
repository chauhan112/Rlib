import sqlite3
from Database import DB, DBResources
from SerializationDB import SerializationDB
import time, os
from CryptsDB import CryptsDB

class _BinaryDumper:
    def __init__(self):
        from jupyterDB import jupyterDB
        from Path import Path
        self.dbPath = Path.joinPath(DBResources.location, "BinaryDumper.db")
        self.db = sqlite3.connect(self.dbPath)
        self.dumperFolder = Path.joinPath(jupyterDB.resource().dirPath, "binaryDumper")
        self.alreadyRead = {}

    def add(self,key, overwrite = True, content = None):
        from jupyterDB import jupyterDB
        file = self._getFile()
        exists = self.read().exists(key)
        if(exists):
            if(not overwrite):
                raise IOError("key already exists")
            file = self.read().fileNr(key)

        if(content is None):
            content = jupyterDB.clip().text()
        c = self._readBinary(file)

        c[key] = content
        SerializationDB.pickleOut(c, file)

        if(not exists):
            DB.execute(f"INSERT INTO KeyFileNr VALUES ('{key}', '{os.path.basename(file)}')", self.db)

    def read(self):
        class Temp:
            def getValue(key):
                content = self._readBinary(Temp.fileNr(key))
                return content[key]

            def exists(key):
                return Temp.count(key) != 0

            def count(key):
                val = Temp._content(key)
                return len(val)

            def fileNr(key):
                from Path import Path
                val = Temp._content(key)
                if(len(val) == 0):
                    raise IOError("Key does not exists") 
                fileNrCol = 1
                return Path.joinPath(self.dumperFolder,val[0][fileNrCol])

            def keys():
                from ListDB import ListDB
                content = DB.execute('SELECT key from KeyFileNr', self.db)
                return ListDB.flatten(content)

            def _content(key):
                return DB.execute(f'SELECT * from KeyFileNr where key="{key}"', self.db)
        return Temp

    def _readBinary(self, file):        
        from ModuleDB import ModuleDB
        from FileDatabase import File

        start = time.time()
        content = SerializationDB.readPickle(file)
        end = time.time()

        name = os.path.basename(file)
        laptop = ModuleDB.laptopName()
        sizeInKb = File.size(file)/1024
        if(name not in self.alreadyRead):
            DB.execute(f"INSERT INTO TimeSize VALUES ('{laptop}', '{end - start}', '{name}', '{sizeInKb}')", self.db)
        self.alreadyRead[os.path.basename(file)] = True
        return content

    def _getFile(self):
        from jupyterDB import jupyterDB
        from Path import Path
        from FileDatabase import File
        class Temp:
            def getThreshold():
                name = "globals"
                k = jupyterDB.pickle().read(name)
                return k['libs']['BinaryDumper']['threshold']
            def allFiles():
                return Path.filesWithExtension("pkl", self.dumperFolder)
            def createAFile():
                file = Path.joinPath(self.dumperFolder, CryptsDB.generateUniqueId()+".pkl")
                SerializationDB.pickleOut({}, file)
                return file
            def fileBasedOnThreshHold():
                files = Temp.allFiles()
                t = Temp.getThreshold()
                if(t == -1):
                    return files[0]

                for f in files:
                    if((File.size(f)/1024) < t):
                        return f
                return Temp.createAFile()

        files = Temp.allFiles()
        if(len(files) ==0):
            return Temp.createAFile()
        return Temp.fileBasedOnThreshHold()

    def search(self,word = "", applyOnValue = None):
        from SearchSystem import DicSearchEngine
        from Path import Path
        if(applyOnValue is None):
            applyOnValue = jupyterDB.clip().copy
        values = DB.execute('SELECT * from KeyFileNr', self.db)
        dic = {key: Path.joinPath(self.dumperFolder, val) for key, val in values}
        s = DicSearchEngine(dic)
        s._runCallback = lambda key, val: applyOnValue(val)
        return s.search(word)

    def delete(self,key):
        from Path import Path
        fileKeyList = DB.execute(f"SELECT * from KeyFileNr WHERE key='{key}'", self.db)
        if(len(fileKeyList) == 0):
            raise IOError("no such key exists")

        delStatement = f"DELETE FROM KeyFileNr WHERE key='{key}';"
        outFile = Path.joinPath(self.dumperFolder, fileKeyList[0][1])
        c = self._readBinary(outFile)
        del c[key]
        SerializationDB.pickleOut(c, outFile)
        if(len(fileKeyList) == 1):
            DB.execute(delStatement, self.db)
        else:
            print("more entries with same key")

    def changeKey(self,oldKeyName, newKey):
        from Path import Path
        if(not self.read().exists(oldKeyName)):
            raise IOError("key does not exists")
        if(self.read().count(oldKeyName) != 1):
            raise IOError("many keys with same name")
        update = f"UPDATE KeyFileNr" \
            f" SET key = '{newKey}'" \
            f" WHERE key = '{oldKeyName}';"
        file = self.read().fileNr(oldKeyName)
        file = Path.joinPath(self.dumperFolder, file)
        content = self._readBinary(file)
        val = content[oldKeyName]
        del content[oldKeyName]
        content[newKey] = val
        SerializationDB.pickleOut(content, file)
        DB.execute(update, self.db)
        
class BinaryDumper:
    def add(key, content = None, overwrite = False):
        b = _BinaryDumper()
        if(content is not None):
            b.add(key, overwrite, content)
    
    def read(key):
        b = _BinaryDumper()
        return b.read().getValue(key)
    
    def delete(key):
        b = _BinaryDumper()
        b.delete(key)
    
    def updateKey(old, new):
        b = _BinaryDumper()
        b.changeKey(old, new)

    def getAllKeys():
        b = _BinaryDumper()
        return b.read().keys()