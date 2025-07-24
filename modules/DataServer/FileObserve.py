import time, os
from modules.mobileCode.CmdCommand import IReturnable,IRunnable, GDataSetable
class IObserver:
    def start(self):
        raise NotImplementedError("abstract method")
    def stop(self):
        raise NotImplementedError("abstract method")

class WatchDogFileObserve(IObserver, IReturnable):
    def __init__(self, path='.',interval=1 ):
        from watchdog.observers import Observer
        self.path = path
        self.interval = interval
        self.observer = Observer()
        self._looper = True
        self.model = ObserverModel()
    def start(self):
        from watchdog.events import FileSystemEventHandler
        func = self.model.run
        class _cal(FileSystemEventHandler):
            def dispatch(self,event):
                func(event)
        self.observer.schedule(_cal(), self.path, recursive=True)
        self.restart()
    def stop(self):
        self._looper = False
    def restart(self):
        self._looper = True
        self.observer.start()
        def runOnThread(inst):
            while inst._looper:
                time.sleep(inst.interval)
            inst.observer.stop()
            inst.observer.join()
        from useful.OpsDB import OpsDB
        OpsDB.runOnThread(runOnThread, [self])
    def get(self):
        return self.model.get()
class ObserverModel:
    def __init__(self):
        self._info = {}
    def run(self, event):
        from useful.TimeDB import TimeDB
        if event.event_type == "created":
            self._info['created'][event.src_path] = (TimeDB.modifiedTime(event.src_path), event.is_directory)
        elif event.event_type == "deleted":
            p = event.src_path
            if p in self._info['created']:
                del self._info['created'][p]
            else:
                self._info['deleted'][p] = TimeDB.today()
        elif event.event_type == "modified":
            self._info['modified'][event.src_path] = (TimeDB.modifiedTime(event.src_path), event.is_directory)
        else:
            print(event.event_type)
    def get(self):
        val = self._info.copy()
        self._info = {'created':{}, 'modified':{}, 'deleted': {}}
        return val
class MutuallyExclusiveEventModel(ObserverModel, GDataSetable):
    def run(self, event):
        self._info[self._sanitize_path(event.src_path)] = {'time': time.time(), 'type': event.event_type,
            'is_dir': event.is_directory}
        if event.event_type == "moved":
            self._info[self._sanitize_path(event.src_path)]['destination'] = self._sanitize_path(event.dest_path)
    def get(self):
        vla = self._info.copy()
        self._info.clear()
        return vla
    def _sanitize_path(self, path):
        replace_path = self.data
        return path.replace(replace_path, "").strip(os.sep)

class IFilesLister:
    def get_files(self):
        pass
class FilesLister(IFilesLister):
    def __init__(self):
        self.set_filter_func(lambda x: True)
    def set_filter_func(self, func):
        self._filter_func = func
    def get_files(self):
        from useful.Path import Path
        files = Path.getFiles(self._root_dir, True)
        return list(filter(self._filter_func, files))
    def set_directory(self, path:str):
        self._root_dir = path
class CalculateProperties:
    def __init__(self):
        self._funcs = {}
        self.add_property_func('size', lambda x: os.stat(x).st_size)
    def add_property_func(self, name:str, func):
        self._funcs[name] = func
    def calculate(self, files: list[str]):
        return {f:  self.calc_for_single_file(f) for f in files}
    def calc_for_single_file(self, file):
        return {n: self._funcs[n](file) for n in self._funcs}
from enum import Enum
class ChangeType(Enum):
    DELETED = 0
    CREATED = 1
    MODIFIED = 2
class ChangeModel:
    def __init__(self):
        self._files_info = {}
        self._cp = CalculateProperties()
        self.set_change_basis("size")
        self._updated = None
    def set_files_lister(self, lister: IFilesLister):
        self._files_lister = lister
    def get_changes(self):
        if self._updated is None:
            self.update()
            self._updated = True
        res = {ChangeType.DELETED.name: [], ChangeType.MODIFIED.name: []}
        for file in self._files_info:
            if os.path.exists(file):
                if self._files_info[file][self._basis] != self._cp.calc_for_single_file(file)[self._basis]:
                    res[ChangeType.MODIFIED.name].append(file)
            else:
                res[ChangeType.DELETED.name].append(file)
        new_files = set(self._files_lister.get_files())
        old_files = set(self._files_info.keys())
        res[ChangeType.CREATED.name] = list(new_files.difference(old_files))
        return res
    def set_change_basis(self, basis: str):
        if basis in self._cp._funcs:
            self._basis = basis
    def update(self):
        self._files = self._files_lister.get_files()
        self._files_info = self._cp.calculate(self._files)
    def remove_path_prefix(self, f):
        loc = f.replace("\\", "/").split("/")
        n = len(self._files_lister._root_dir.replace("\\", "/").split("/"))
        return "/".join(loc[n:])
    
class MyFileObserver(IObserver):
    def __init__(self):
        self.set_time_interval(2)
        self._fl = FilesLister()
        self._fl.set_filter_func(lambda x: True)
        self._cm = ChangeModel()
        self._cm.set_files_lister(self._fl)
        self._info = {}
    def set_time_interval(self, time_in_sec):
        self._time_interval = time_in_sec
    def start(self):
        pass
    def _run(self):
        self._info.clear()
        res = self._cm.get_changes()
        rl = len(self._path)
        rm = lambda x: x[rl:]
        for f in res[ChangeType.CREATED.name]:
            self._info[rm(f)] = {'time': time.time(), 'type': "created", 'is_dir': False}
        for f in res[ChangeType.MODIFIED.name]:
            self._info[rm(f)] = {'time': time.time(), 'type': "modified", 'is_dir': False}
        for f in res[ChangeType.DELETED.name]:
            self._info[rm(f)] = {'time': time.time(), 'type': "deleted", 'is_dir': False}
    def stop(self):
        pass
    def set_observable_path(self, path: str):
        self._path = path
        self._fl.set_directory(path)
    def get(self):
        self._run()
        self._cm.update()
        return self._info
class Main:
    pass

class Test:
    def change_model_test():
        fl = FilesLister()
        fl.set_directory(".")
        fl.set_filter_func(lambda x: x.endswith(".py"))
        cm = ChangeModel()
        cm.set_files_lister(fl)
        print(cm.get_changes())
        test_file ="asdjbasdb.py"
        print("-"*30)
        print("creating a temporary file")
        from useful.FileDatabase import File
        File.createFile(test_file)
        print(cm.get_changes())
        cm.update()
        print("-"*30)
        print("Modifying the temporary file")
        File.overWrite(test_file, "asdn")
        print(cm.get_changes())
        cm.update()
        print("-"*30)
        print("Deleting the temporary file")
        File.deleteFiles([test_file])
        print(cm.get_changes())
        cm.update()