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
