def insertPath():
    import sys
    path = getPath()
    if path not in sys.path:
        sys.path.insert(0, path)

def getPath():
    return 'C:\\Users\\49162\\Desktop\\cloud\\Global\\code\\libs\\RLibs'

def resourcePath():
    return 'C:\\Users\\49162\\Desktop\\cloud\\Global\\code\\libs\\resource'

def dumperPath():
    return 'C:\\Users\\49162\\Desktop\\cloud\\Global\\code\\daily code dumper'

def computerName():
    return 'home'

def runBasic(*args):
    insertPath()
    from LibsDB import LibsDB
    return LibsDB.runBasic(*args)