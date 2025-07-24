class ProgramManager:
    def _read():
        from useful.LibsDB import LibsDB
        from useful.SerializationDB import SerializationDB
        return SerializationDB.readPickle(LibsDB.picklePath("paths"))
    def getApp(name):
        from useful.ModuleDB import ModuleDB
        content = ProgramManager._read()
        val = content['programs'][ModuleDB.laptopName()]
        if name in val:
            return val[name]
        raise IOError("Program not found")
