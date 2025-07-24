from timeline.t2024.tailwind.twcrudOps import DictionaryModel
from sqlitedict import SqliteDict
from useful.basic import Main as ObjMaker
def SqliteModelV3():
    dm = DictionaryModel()
    filePath = "test.sqlite"
    def readTableAsDic(table):
        with SqliteDict(s.process.filePath, tablename=table, autocommit=True) as db:
            return dict(db.iteritems())
    def read(loc):
        if len(loc)  == 0:
            tableNames = s.handlers.get_table_names()
            return tableNames
        if len(loc) == 1:
            return s.handlers.readTableAsDic(loc[0])
        else:
            with SqliteDict(s.process.filePath, tablename=loc[0], autocommit=True) as db:
                vals = db[loc[1]]
                s.process.dm.s.process.model = vals
                return dm.read(loc[2:])
    def delete(loc):
        if len(loc) == 1:
            with SqliteDict(s.process.filePath, autocommit=True) as db:
                db.conn.select_one(f'DROP TABLE "{loc[0]}"')
        elif len(loc) == 2:
            with SqliteDict(s.process.filePath, tablename=loc[0], autocommit=True) as db:
                del db[loc[1]]
        elif len(loc) > 2:
            tableName = loc[0]
            key = loc[1]
            with SqliteDict(s.process.filePath, tablename=tableName, autocommit=True) as db:
                vals = db[key]
                s.process.dm.s.process.model = vals
                s.process.dm.delete(loc[2:])
                db[key] = vals
    def add(loc, val):
        if len(loc) == 2:
            key = loc[1]
            with SqliteDict(s.process.filePath, tablename=loc[0], autocommit=True) as db:
                db[key] = val
        elif len(loc) > 2:
            tableName = loc[0]
            key = loc[1]
            with SqliteDict(s.process.filePath, tablename=tableName, autocommit=True) as db:
                vals = db.get(key)
                if vals is None:
                    vals = {}
                s.process.dm.s.process.model = vals
                s.process.dm.update(loc[2:], val)
                db[key] = vals
    def exists(loc):
        if len(loc) == 1:
            tables = s.handlers.get_table_names()
            return loc[0] in tables
        if len(loc) == 2:
            key = loc[1]
            with SqliteDict(s.process.filePath, tablename=loc[0], autocommit=True) as db:
                val = db.get(key)
                return val is not None
        elif len(loc) > 2:
            tableName = loc[0]
            key = loc[1]
            with SqliteDict(s.process.filePath, tablename=tableName, autocommit=True) as db:
                vals = db.get(key)
                if vals is None:
                    return False
                s.process.dm.s.process.model = vals
                return s.process.dm.exists(loc[2:])
    def readAll():
        tableNames = s.handlers.get_table_names()
        res = {}
        for t in tableNames:
            res[t] = s.handlers.readTableAsDic(t)
        return res
    def get_table_names():
        return SqliteDict.get_tablenames(s.process.filePath)
    s = ObjMaker.variablesAndFunction(locals())
    s.handlers.s = s
    return s.handlers