from basic import NameSpace
from CryptsDB import CryptsDB
from timeline.t2023.dep_extractor.dependency_extractor import DicOps
class ControllerModel:
    def create_columns(tableName, struc):
        if not lapp.model.tables.logger.exists(tableName):
            lapp.model.tables.logger.create(tableName)
        lapp.model.tables.metaInfo.create(tableName, app.model.constants.strings.structure, struc)
        lapp.model.tables.metaInfo.create(tableName, app.model.constants.strings.key_index, 0)
class DictionaryCRUD:
    def __init__(self):
        self.set_dictionary({})
        self.set_baseloc([])
    def read(self, key):
        return DicOps.get(self._dic, self._baseloc +[key])
    def write(self, key, value, overwrite = False):
        if self.exists(key) and not overwrite:
            raise IOError("Value already exists")
        DicOps.addEventKeyError(self._dic, self._baseloc + [key], value)
    def set_baseloc(self, loc):
        self._baseloc = loc
    def exists(self, key):
        try:
            self.read(key)
            return True
        except:
            pass
        return False
    def set_dictionary(self, dic):
        self._dic = dic
    def delete(self, key):
        vals = DicOps.get(self._dic, self._baseloc)
        del vals[key]
    def readAll(self):
        return DicOps.get(self._dic, self._baseloc)
class ModelFuncs:
    def set_app(self, app):
        self.app = app
    def loggerData_create(self, tableName, key, value):
        uuid = lapp.model.tables.logger.get_uuid(tableName)
        lapp.model.global_meta.create(key, value, loc=lapp.model.constants.lists.loc_tables_data + [uuid])
    def loggerData_delete(self, tableName, key):
        uuid = lapp.model.tables.logger.get_uuid(tableName)
        lapp.model.global_meta.delete(key, loc=lapp.model.constants.lists.loc_tables_data + [uuid])
    def loggerData_update(self, tableName, key, old_val, new_val):
        uuid = lapp.model.tables.logger.get_uuid(tableName)
        lapp.model.global_meta.update(key, new_value, loc=lapp.model.constants.lists.loc_tables_data + [uuid])
    def loggerData_read(self, tableName, key):
        uuid = lapp.model.tables.logger.get_uuid(tableName)
        return lapp.model.global_meta.read(key, loc=lapp.model.constants.lists.loc_tables_data + [uuid])
    def loggerData_readAll(self, tableName):
        uuid = lapp.model.tables.logger.get_uuid(tableName)
        return lapp.model.global_meta.read(uuid, loc=lapp.model.constants.lists.loc_tables_data)
    def metaInfo_create(self, tableName, key, value):
        uuid = lapp.model.tables.logger.get_uuid(tableName)
        lapp.model.global_meta.create(key, value, loc=lapp.model.constants.lists.loc_tables + [uuid])
    def metaInfo_delete(self, tableName, key):
        uuid = lapp.model.tables.logger.get_uuid(tableName)
        lapp.model.global_meta.delete(key, loc=lapp.model.constants.lists.loc_tables + [uuid])
    def metaInfo_update(self, tableName, key, old_value, new_value):
        uuid = lapp.model.tables.logger.get_uuid(tableName)
        lapp.model.global_meta.update(key, new_value, loc=lapp.model.constants.lists.loc_tables + [uuid])
    def metaInfo_read(self, tableName, key):
        uuid = lapp.model.tables.logger.get_uuid(tableName)
        return lapp.model.global_meta.read(key, loc=lapp.model.constants.lists.loc_tables + [uuid])
    def metaInfo_readAll(self, tableName):
        uuid = lapp.model.tables.logger.get_uuid(tableName)
        return lapp.model.global_meta.read(name, uuid, loc=lapp.model.constants.lists.loc_tables + [uuid])
    def metaInfo_exists(self, key):
        uuid = lapp.model.tables.logger.get_uuid(tableName)
        return lapp.model.global_meta.exists(key, value, loc=lapp.model.constants.lists.loc_tables + [uuid])
    def logger_create(self, name):
        if not lapp.model.tables.logger.exists(name):
            uuid = CryptsDB.generateUniqueId()
            lapp.model.global_meta.create(name, uuid, loc=lapp.model.constants.lists.loc_tables2uuid)
            lapp.model.global_meta.create(uuid, {"name": name}, loc=lapp.model.constants.lists.loc_tables)
    def logger_delete(self, name):
        if lapp.model.tables.logger.exists(name):
            uuid = lapp.model.global_meta.read(name, loc=lapp.model.constants.lists.loc_tables2uuid)
            lapp.model.global_meta.delete(uuid, loc=lapp.model.constants.lists.loc_tables)
            lapp.model.global_meta.delete(name, loc=lapp.model.constants.lists.loc_tables2uuid)
    def logger_update(self, old_name, newname):
        oldExists = lapp.model.tables.logger.exists(old_name)
        newDoesNotExist = not lapp.model.tables.logger.exists(newname)
        if oldExists and newDoesNotExist:
            uuid = lapp.model.global_meta.read(old_name, loc=lapp.model.constants.lists.loc_tables2uuid)
            tableInfos = lapp.model.global_meta.read(uuid, loc=lapp.model.constants.lists.loc_tables)
            tableInfos["name"]= newname
            lapp.model.global_meta.delete(old_name, loc=lapp.model.constants.lists.loc_tables2uuid)
            lapp.model.global_meta.update(uuid, tableInfos, loc=lapp.model.constants.lists.loc_tables)
            lapp.model.global_meta.create(newname, uuid, loc=lapp.model.constants.lists.loc_tables2uuid)
    def logger_exists(self, name):
        return lapp.model.global_meta.exists(name, loc=lapp.model.constants.lists.loc_tables2uuid)
    def logger_get_uuid(self, name):
        return lapp.model.global_meta.read(name, loc=lapp.model.constants.lists.loc_tables2uuid)
    def logger_read(self, name):
        uuid = lapp.model.global_meta.read(name, loc=lapp.model.constants.lists.loc_tables2uuid)
        return lapp.model.global_meta.read(uuid, loc=lapp.model.constants.lists.loc_tables)
    def logger_readAll(self):
        return lapp.model.global_meta.readAll(loc=lapp.model.constants.lists.loc_tables)
    def global_meta_create(self, key, value,loc = None):
        if loc is None:
            loc = []
        lapp.controllers.instances.dicModel.set_baseloc(loc)
        lapp.controllers.instances.dicModel.write(key, value)
    def global_meta_delete(self, key, loc=None):
        if loc is None:
            loc = []
        lapp.controllers.instances.dicModel.set_baseloc(loc)
        lapp.controllers.instances.dicModel.delete(key)
    def global_meta_update(self, key, value, loc =None):
        if loc is None:
            loc = []
        lapp.controllers.instances.dicModel.set_baseloc(loc)
        lapp.controllers.instances.dicModel.write(key, value, True)
    def global_meta_read(self, key, loc = None):
        if loc is None:
            loc = []
        lapp.controllers.instances.dicModel.set_baseloc(loc)
        return lapp.controllers.instances.dicModel.read(key)
    def global_meta_exists(self, key, loc = None):
        if loc is None:
            loc = []
        lapp.controllers.instances.dicModel.set_baseloc(loc)
        return lapp.controllers.instances.dicModel.exists(key)
    def global_meta_readAll(self, loc = None):
        if loc is None:
            loc = []
        lapp.controllers.instances.dicModel.set_baseloc(loc)
        return lapp.controllers.instances.dicModel.readAll()