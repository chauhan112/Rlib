from sqlitedict import SqliteDict
from useful.ListDB import ListDB
class SQLiteDictDB:
    def set_file(self, filename):
        self._filepath = filename
    def set_table_name(self, table):
        self._table_name = table
    def read(self, key):
        with SqliteDict(self._filepath, tablename=self._table_name, autocommit=True) as db:
            return db[key]
    def override(self, key, value):
        with SqliteDict(self._filepath, tablename=self._table_name, autocommit=True) as db:
            db[key] = value
    def has(self, key):
        with SqliteDict(self._filepath, tablename=self._table_name, autocommit=True) as db:
            val = db.get(key)
            return val is not None
    def get_table_names(self):
        return SqliteDict.get_tablenames(self._filepath)
    def get_keys(self):
        with SqliteDict(self._filepath, tablename=self._table_name, autocommit=True) as db:
            return list(db.iterkeys())
    def get_content_as_dict(self):
        with SqliteDict(self._filepath, tablename=self._table_name, autocommit=True) as db:
            return dict(db.iteritems())
    def delete(self, key):
        with SqliteDict(self._filepath, tablename=self._table_name, autocommit=True) as db:
            del db[key]
    def deleteTable(self, tableName):
        with SqliteDict(self._filepath, autocommit=True) as db:
            db.conn.select_one(f'DROP TABLE "{tableName}"')
class SqlCRUD:
    def __init__(self):
        self._loc = []
        self._sqlddb = SQLiteDictDB()
    def goback(self):
        if len(self._loc):
            self._loc.pop()
    def isDic(self):
        if len(self._loc) == 0:
            return True
        conte = self.value()
        return type(conte) == dict
    def value(self):
        if len(self._loc) == 0:
            return self._sqlddb.get_content_as_dict()
        conte = self._sqlddb.read(self._loc[0])
        return ListDB.dicOps().get(conte, self._loc[1:])
    def add(self, key, value):
        if len(self._loc) == 0:
            self._sqlddb.override(key, value)
            return
        content = self._sqlddb.read(self._loc[0])
        ListDB.dicOps().add(content, self._loc[1:] + [key], value)
        self._sqlddb.override(self._loc[0], content)
    def addEvenKeyError(self, key, value):
        if len(self._loc) == 0:
            self._sqlddb.override(key, value)
            return
        content = self._sqlddb.read(self._loc[0])
        ListDB.dicOps().addEvenKeyError(content, self._loc[1:] + [key], value)
        self._sqlddb.override(self._loc[0], content)
    def getKeys(self):
        val = self.value()
        if(type(val) == dict):
            return list(val.keys())
        raise IOError("value is not a dictionary")
    def alreadyExists(self, key):
        val = self.value()
        return key in val

    def delete(self, key):
        if len(self._loc) == 0:
            self._sqlddb.delete(key)
            return
        content = self._sqlddb.read(self._loc[0])
        ListDB.dicOps().delete(content, self._loc[1:] + [key])
        self._sqlddb.override(self._loc[0], content)
    def set_db(self, db):
        self._sqlddb = db
    def goForward(self, key):
        self._loc.append(key)
    def set_base_location(self, loc):
        self._loc = loc
        self._baseloc = loc
