def insertPath():
    import sys
    sys.path.insert(0, getPath())

def getPath():
    return r"C:\Users\49162\Desktop\cloud\Global\code\libs\RLibs"

def computerName():
    return 'home'

def runBasic(*args):
    insertPath()
    from LibsDB import LibsDB
    return LibsDB.runBasic(*args)