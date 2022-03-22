import time, os
from modules.mobileCode.CmdCommand import IReturnable,IRunnable, GDataSetable

class IObserver(IReturnable):
    def start(self):
        raise NotImplementedError("abstract method")
    def stop(self):
        raise NotImplementedError("abstract method")

class GObserver(IObserver):
    def start(self):
        pass
    def stop(self):
        pass

class IReturnableNRunnable(IRunnable, IReturnable):
    pass

class WatchDogFileObserve(IObserver, IReturnable):
    def __init__(self, path='.',interval=1, model: IReturnableNRunnable=None ):
        from watchdog.observers import Observer
        self.path = path
        self.interval = interval
        self.observer = Observer()
        self._looper = True
        self.model = model
        if self.model is None:
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
        from OpsDB import OpsDB
        OpsDB.runOnThread(runOnThread, [self])

    def get(self):
        return self.model.get()

class ObserverModel(IReturnable):
    def __init__(self):
        self._info = {}

    def run(self, event):
        from TimeDB import TimeDB
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

class IIgnorer:
    def check(self, path: str) -> bool:
        raise NotImplementedError("abstract method")

class IgnoreFiles(IIgnorer):
    def __init__(self):
        pass
    def add(self, checkerFunc):
        pass
    def addRegexIgnore(self, regex):
        pass
    def check(self, path):
        return True

class IFileStructureModel:
    def get_info(self, path):
        raise NotImplementedError("abstract method")
    def update(self, path, info):
        raise NotImplementedError("abstract method")
    def remove(self, path):
        raise NotImplementedError("abstract method")
    def add(self, path, info):
        raise NotImplementedError("abstract method")

class FileStructureModel:
    def __init__(self, initial_path ="."):
        self.parent = initial_path
        self._dic = {self.parent: {'folders': {}, 'files':{}, 
            'info':FileStructureModel.info_dir_func(self.parent)}}
    def _fill(self, name,dic, loc = []):
        path = '/'.join(loc +[name])
        if os.path.isdir(path):
            dirlist = os.path.listdir()
            for val in dirlist:
                element = '/'.join([path, val])
                if os.path.isdir(element):
                    dic['folders'][val]= {'folders': {}, 'files':{}, 
                        'info': FileStructureModel.info_dir_func(element)}
                    self._fill(val,dic['folders'][val], loc +[name, val])
                else:
                    dic['files'][val] ={'info': FileStructureModel.info_file_func(element)}
        else:
            pass
            
    def _fill2(self, name, dic, loc=[]):
        path = '/'.join(loc + [name])
        if os.path.isdir(path):
            pass
        else:
            pass
        
    @staticmethod
    def info_file_func(path):
        pass
    def info_dir_func(path):
        pass

class MyFileObserver(GObserver, IReturnable):
    def __init__(self, path = '.'):
        self.path = path
        self._last_modified = 0
        self._data = {}

    def get(self):
        pass
        
    
