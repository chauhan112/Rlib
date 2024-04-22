from Path import Path
import os
from TimeDB import TimerDB
import fnmatch
class FilesGetter:
    def __init__(self):
        self._ignore_list = []
        self._files = []
    def set_location(self, loc):
        self._base_location = loc
    def set_git_ignore_file(self, ignoreFile):
        self._ignore_file = ignoreFile
        self._ignore_list = list(filter(lambda x: len(x.strip()) > 0 and x.strip()[0] != "#", File.getFileContent(ignoreFile).splitlines()))
    def get_ignored(self):
        if os.path.exists(os.path.join(self._base_location, ".git")):
            from git import Repo
            repo = Repo(self._base_location)
            return repo.git.ls_files().splitlines() + repo.git.execute(['git', 'ls-files', "--others","--exclude-standard"]).splitlines()
        if len(self._files) == 0:
            self._files = Path.getFiles(self._base_location, True)
        if len(self._ignore_list) == 0:
            return self.getRelativeFilesWithExt(self._files)
        filenames = [n for n in self._files
             if not any(fnmatch.fnmatch(n, ignore) for ignore in self._ignore_list)]
        return self.getRelativeFilesWithExt(filenames)
    def set_files(self, files):
        self._files = files
    def set_ignore_list(self, ignore_list):
        self._ignore_list = ignore_list
    def getRelativeFilesWithExt(self, files):
        files = list(map(lambda x: x[len(self._base_location):].strip(os.sep), files))
        return files
class FileSyncer:
    def __init__(self):
        self._running_instance = None
        self._time = 60 # 60 sec
    def set_files(self, files):
        self._files = files
    def sync(self, fromPath, toPath):
        self._params = [fromPath, toPath]
        self._running_instance = TimerDB(self._time, self._func)
    def stop(self):
        self._running_instance.cancel()
    def _func(self):
        self.fileSync(*self._params)
    def fileSync(self, fromPath, toPath):
        for file in self._files:
            fromFilePath = os.sep.join([fromPath, file])
            toFilePath = os.sep.join([toPath, file])
            if not os.path.exists(toFilePath):
                targetPath = os.path.dirname(toFilePath)
                if not os.path.exists(targetPath):
                    os.makedirs(targetPath)
                Path.copyFiles([fromFilePath], targetPath)
                continue
            fromStat = os.stat(fromFilePath)
            toStat = os.stat(toFilePath)
            if fromStat.st_size != toStat.st_size:
                Path.delete([toFilePath])
                Path.copyFiles([fromFilePath], os.path.dirname(toFilePath))


from timeline.t2024.experiments.models import LocalStorageTableOps, ModelInitializer

class FileSyncLC:
    def set_up(self):
        from timeline.t2024.ui_lib.IpyComponents import IpywidgetsComponentsEnum, Utils
        from timeline.t2023.console_opener import Main as COMain
        fromComp = Utils.get_comp({"description": "from location"}, IpywidgetsComponentsEnum.Text, bind =False)
        toComp = Utils.get_comp({"description": "to location"}, IpywidgetsComponentsEnum.Text, bind =False)
        updateBtn = Utils.get_comp({"description": "update"}, IpywidgetsComponentsEnum.Button)
        flipBtn = Utils.get_comp({"description": "flip"}, IpywidgetsComponentsEnum.Button)
        openFromBtn = Utils.get_comp({"description": "open from"}, IpywidgetsComponentsEnum.Button)
        openToBtn = Utils.get_comp({"description": "open to"}, IpywidgetsComponentsEnum.Button)
        container = Utils.container([fromComp, toComp, updateBtn, flipBtn, openFromBtn, openToBtn])
        cfff = COMain.console_and_folder_opener()
        ModelInitializer.initialize()
        openFromBtn.handlers.handle = self.openFrom
        openToBtn.handlers.handle = self.openTo
        updateBtn.handlers.handle = self.update_files
        flipBtn.handlers.handle = self.flip_func
        self.add_to_namespace([
            [["views", "components", "fromComp"], fromComp],
            [["views", "components", "toComp"], toComp],
            [["views", "components", "updateBtn"], updateBtn],
            [["views", "components", "flipBtn"], flipBtn],
            [["views", "components", "openFromBtn"], openFromBtn],
            [["views", "components", "openToBtn"], openToBtn],
            [["views", "output", "layout"], container.outputs.layout],
            [["controller", "syncState", "folderOpener"], cfff.app.controller.explorer.open],
            [["controller", "callbacks", "openFrom"], self.openFrom],
            [["controller", "callbacks", "openTo"], self.openTo],
            [["controller", "callbacks", "update_files"], self.update_files],
            [["controller", "callbacks", "flip_func"], self.flip_func],
        ])
        self.fillTheValues()
    def add_to_namespace(self, keyValsAsList):
        """keyValsAsList : [[["key", "key2"], val],[["key2", "key2"], val2]]"""
        for loc, val in keyValsAsList:
            ObjectOps.setEvenIfItdoesNotExist(self, loc, val)
            
    def fillTheValues(self):
        app_name, fromKey, toKey = FileSyncLC.get_infos()
        fromVal = LocalStorageTableOps.read(app_name, fromKey)["value"]
        toVal = LocalStorageTableOps.read(app_name, toKey)["value"]
        if fromVal:
            self.views.components.fromComp.outputs.layout.value = fromVal
        if toVal:
            self.views.components.toComp.outputs.layout.value = toVal
    def get_infos():
        from ModuleDB import ModuleDB
        app_name = "sync react files"
        laptopName = ModuleDB.laptopName()
        fromKey = laptopName + "-from"
        toKey = laptopName + "-to"
        return app_name, fromKey, toKey
    def update_files(self, btn):
        app_name, fromKey, toKey = FileSyncLC.get_infos()
        LocalStorageTableOps.update(app_name, fromKey, self.views.components.fromComp.outputs.layout.value)
        LocalStorageTableOps.update(app_name, toKey, self.views.components.toComp.outputs.layout.value)
        fg = FilesGetter()
        fg.set_location(self.views.components.fromComp.outputs.layout.value)
        fg._ignore_list.append('*manifest.json')
        fg._ignore_list.append('*src/react-app-env.d.ts')
        fs = FileSyncer()
        files = fg.get_ignored()
        # print(files)
        fs.set_files(files)
        fs.fileSync(self.views.components.fromComp.outputs.layout.value, self.views.components.toComp.outputs.layout.value)
    def flip_func(self, btn):
        fromVal = self.views.components.fromComp.outputs.layout.value
        self.views.components.fromComp.outputs.layout.value = self.views.components.toComp.outputs.layout.value
        self.views.components.toComp.outputs.layout.value = fromVal
    def openFrom(self,btn):
        self.controller.syncState.folderOpener(self.views.components.fromComp.outputs.layout.value)
    def openTo(self, btn):
        self.controller.syncState.folderOpener(self.views.components.toComp.outputs.layout.value)
        
class Main:
    def fslc():
        fs = FileSyncLC()
        fs.set_up()
        return fs