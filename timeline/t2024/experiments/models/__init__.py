import timeline.t2024.experiments.models.tables as models
class ModelWrappper:
    def set_file(self, file_path):
        models.db_proxy.initialize(models.SqliteDatabase(file_path))
    def get_tables(self):
        return models.ns
    def readAll(table):
        return list(map(lambda x: x.__data__, getattr(table, "select")()))
class ModelInitializer:
    initialized = False
    instance = None
    def initialize():
        default_path = '../../2024/03_Mar/main.db'
        if not ModelInitializer.initialized:
            mw = ModelWrappper()
            mw.set_file(default_path)

class LocalStorageTableOps:
    def add(appName, key, value):
        models.ns.LocalStorage.create(app_name = appName, key=key, value = value)
    def clear(appName):
        models.ns.LocalStorage.delete().where(models.ns.LocalStorage.app_name == appName).execute()
    def delete(appName, key):
        models.ns.LocalStorage.delete().where(models.ns.LocalStorage.app_name == appName and models.ns.LocalStorage.key == key).execute()
    def readAll(appName):
        res = models.ns.LocalStorage.select().where(models.ns.LocalStorage.app_name == appName)
        return list(map(lambda x: x.__data__, res))
    def read(appName, key):
        res = models.ns.LocalStorage.select().where(models.ns.LocalStorage.app_name == appName and models.ns.LocalStorage.key == key)
        founds = list(map(lambda x: x.__data__, res))
        if len(founds) !=  0:
            return founds[0]
    def update(appName, key, value):
        val = LocalStorageTableOps.read(appName, key)
        if val:
            models.ns.LocalStorage.update(app_name = appName, key=key, value = value).where(models.ns.LocalStorage.id == val['id']).execute()
        else:
            LocalStorageTableOps.add(appName, key, value)