from timeline.t2023.sql_crud import SQLiteDictDB, SqlCRUD
class SQLCrudWrapper:
    def set_filename(self, filename, tablename):
        sqldb = SQLiteDictDB()
        sqldb.set_file(filename)
        scrud = SqlCRUD()
        scrud.set_db(sqldb)
        self.set_sqldb(scrud)
        sqldb.set_table_name(tablename)
    def set_sqldb(self, sqldb):
        self._sqldb = sqldb
    def add(self, key, value, override = False):
        if self._sqldb.alreadyExists(key) and not override:
            print("value aleady exists")
            return
        self._sqldb.add(key, value)
    def read(self, key):
        self._sqldb.goForward(key)
        val = self._sqldb.value()
        self._sqldb.goback()
        return val
    def readAll(self):
        return self._sqldb.value()
    def delete(self, key):
        self._sqldb.delete(key)