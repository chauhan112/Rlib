def insertPath():
    import sys
    sys.path.insert(0, getPath())

def getPath():
    return r"D:\cloud\Global\code\libs\RLibs"

def computerName():
    return 'office'

def runBasic(*args):
    insertPath()
    from LibsDB import LibsDB
    return LibsDB.runBasic(*args)