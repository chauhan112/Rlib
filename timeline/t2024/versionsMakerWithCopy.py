from useful.ListDB import ListDB
from basic import Main as ObjMaker
from useful.TimeDB import TimeDB
import os
from useful.Path import Path
from useful.FileDatabase import File
def VersionSystem():
    filesAndLocation = {}
    duration = 30*60 # 30 min
    numberOfCopies = 20
    timer = None
    prev_size = None
    def add_file_and_location(file, location):
        absPath = os.path.abspath(file)
        if absPath in s.process.filesAndLocation:
            raise IOError("file already exists")
        s.process.filesAndLocation[absPath] = location
    def update_file_location(file, location):
        absPath = os.path.abspath(file)
        if absPath not in s.process.filesAndLocation:
            raise IOError("file does not exist")
        s.process.filesAndLocation[absPath] = location
    def delete_file(file):
        absPath = os.path.abspath(file)
        del s.process.filesAndLocation[absPath]
    def read(file):
        absPath = os.path.abspath(file)
        return s.process.filesAndLocation[absPath]
    def copy_to_target():
        for file in s.process.filesAndLocation:
            location = s.process.filesAndLocation[file]
            cur_size = File.size(file)
            if s.process.prev_size != cur_size:
                s.handlers.copyAndRename(file, location, s.handlers.add_name_stamp(os.path.basename(file)))
                s.process.prev_size = cur_size
    def add_name_stamp(name):
        splitted = name.split(".")
        newBaseName =  ".".join([".".join(splitted[:-1]) + s.handlers.current_time_stamp() ,splitted[-1]])
        return newBaseName
    def remove_name_stamp(name):
        splitted = name.split(".")
        x = ".".join(splitted[:-1])
        y = x[:-14]
        newBaseName =  ".".join([y ,splitted[-1]])
        return newBaseName
    def current_time_stamp():
        yr, tim = TimeDB.today()
        return "".join(list(map(s.handlers.twoDigitShift,ListDB.flatten(TimeDB.today()))))
    def twoDigitShift(nr):
        if nr < 10:
            return "0" + str(nr)
        return str(nr)
    def prepare_target_dirs():
        for file in s.process.filesAndLocation:
            location = s.process.filesAndLocation[file]
            if not os.path.exists(location):
                os.makedirs(location)
    def copyAndRename(file, toLocation, newName):
        Path.copyFiles([file], toLocation)
        filePath = os.sep.join([toLocation, os.path.basename(file)])
        newFilePathName = os.sep.join([toLocation, newName])
        if os.path.exists(filePath):
            File.rename(filePath, newFilePathName)
    def run_on_thread():
        if s.process.timer is None:
            s.process.timer = TimeDB.setTimer().regularlyUpdateTime( s.process.duration, windowMover)
    def windowMover():
        s.handlers.copy_to_target()
        s.handlers.delete_files_more_than_window_size()
    def delete_files_more_than_window_size():
        for file in s.process.filesAndLocation:
            location = s.process.filesAndLocation[file]
            allFiles = s.handlers.filesFor(file, location)
            if len(allFiles) > s.process.numberOfCopies:
                x = sorted(allFiles, reverse=True)
                y = x[s.process.numberOfCopies:]
                Path.delete(y)
    def filesFor(file, location):
        allFiles = Path.getFiles(location, False)
        return list(filter(lambda x: s.handlers.remove_name_stamp(os.path.basename(x)) == os.path.basename(file),
            allFiles))
    s = ObjMaker.variablesAndFunction(locals())
    return s
