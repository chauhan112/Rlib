from useful.SerializationDB import SerializationDB 
from useful.LibsDB import LibsDB
from useful.Database import Database

class UrlDB:
    def learning(word = None):
        vals = UrlDB.getUrl('learning')
        db = Database.urlDB(vals)
        if(word is not None):
            db.search(word)
        return db
    def getUrl(key):
        return SerializationDB.readPickle(LibsDB.picklePath('urlDB.pkl'))[key]
    
    def db(word = None):
        from ancient.StaticDisplayerManager import StaticDisplayerManager
        k = SerializationDB.readPickle(LibsDB.picklePath('urlDB.pkl'))
        p = {}
        for key in k:
            p.update(k[key])
        db = Database.urlDB(p)
        StaticDisplayerManager.display('UrlDB container size Info', len(db.searchSys.container))
        return Database.dbSearch(db,word)
    
    def tree(word = None):
        vals = UrlDB.getUrl('tree')
        return Database.dbSearch(Database.urlDB(vals), word)
      
    def urlOps():
        from ancient.AIAlgoDB import AIAlgoDB
        from useful.ListDB import ListDB
        class TempUrl:
            content = SerializationDB.readPickle(LibsDB.picklePath('urlDB.pkl'))
            def getCategories(self):
                return list(self.content.keys())
            def add(self, key, val, cat = "ran", overWrite = False):
                sugg = AIAlgoDB.incrementalSearch(self.getCategories()).search(cat)[0]
                if(key in TempUrl.content[sugg]):
                    if(not overWrite):
                        raise IOError("key already exists")
                ListDB.dicOps().add(TempUrl.content,  [sugg, key], val)
                self._write()
            def delete(self, key, cat = "rand"):
                sugg = AIAlgoDB.incrementalSearch(self.getCategories()).search(cat)[0]
                del TempUrl.content[sugg][key]
                self._write()
            def keys(self, cat = "rand"):
                sugg = AIAlgoDB.incrementalSearch(self.getCategories()).search(cat)[0]
                return list(TempUrl.content[sugg].keys())
            def modify(self, key, val, cat):
                add(key, val, cat, True)
            def _write(self):
                SerializationDB.pickleOut(self.content, LibsDB.picklePath('urlDB.pkl'))
        return TempUrl()
            