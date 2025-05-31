from basic import Main as ObjMaker
def ConversionTool():
    def sizeReduce(size_bytes):
        import math
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"
    s = ObjMaker.variablesAndFunction(locals())
    return s
def FileTools():
    def size(filepaths):
        from FileDatabase import File
        conversionTool = ConversionTool()
        return conversionTool.handlers.sizeReduce(sum(map(File.size, filepaths)))
    s = ObjMaker.variablesAndFunction(locals())
    return s
def YearManagerTools():
    import os
    import calendar
    import datetime
    from SerializationDB import SerializationDB
    from LibsDB import LibsDB
    from timeline.t2023.tools import TimelineDB

    def createIpynbFiles(year):
        months = list(calendar.month_name)[1:]
        short_months_with_indices = [ '{:0>2d}'.format(i+1) + "_" + val[:3] for i, val in enumerate(months)]
        year_loc = TimelineDB.getYearPath(year)
        month_fullpaths = [year_loc + os.sep + mth for mth in short_months_with_indices]
        for dirpath in month_fullpaths:
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            spaceIpynb = dirpath + os.sep + "space.ipynb" 
            content = SerializationDB.readPickle(LibsDB.picklePath("temps"))["timeline"]["2024"]["12_Dec"]["nb-data"]
            File.overWrite(spaceIpynb, content)
    s = ObjMaker.variablesAndFunction(locals())
    return s
