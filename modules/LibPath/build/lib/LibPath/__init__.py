import re
import sys
import os

def insertPath():
    path = getPath()
    if path not in sys.path:
        sys.path.insert(0, path)

def base_path():
    path = r"C:\Users\rajab\Desktop\cloud\cloud\Global\code\libs\RLibs\modules\LibPath\LibPath"
    return path

def getPath():
    tillRlib = re.findall(".*RLibs", base_path())[0]
    return tillRlib

def resourcePath():
    tillCode = re.findall(".*code", base_path())[0]
    return os.sep.join([tillCode, "libs", "resource"])

def dumperPath():
    tillCode = re.findall(".*code", base_path())[0]
    return os.sep.join([tillCode, "daily code dumper"])

def computerName():
    return 'home'

def runBasic(*args):
    insertPath()
    from LibsDB import LibsDB
    return LibsDB.runBasic(*args)

