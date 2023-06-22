class ProgramManager:
    def _read():
        from LibsDB import LibsDB
        from SerializationDB import SerializationDB
        return SerializationDB.readPickle(LibsDB.picklePath("paths"))
    def getApp(name):
        from ModuleDB import ModuleDB
        content = ProgramManager._read()
        val = content['programs'][ModuleDB.laptopName()]
        if name in val:
            return val[name]
        raise IOError("Program not found")
