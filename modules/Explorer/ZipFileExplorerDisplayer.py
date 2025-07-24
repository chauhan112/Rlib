import os
from modules.Explorer.displayer import FileExplorerDisplayer
from modules.Explorer.model import ZipFileExplorer, ExplorerUtils,IExplorer
from modules.Explorer.personalizedWidgets import WidgetsIpyExplorerDisplayer, IExplorerDisplayer
import ipywidgets as widgets

class ZipFileExplorerDisplayer(FileExplorerDisplayer):
    def __init__(self, zipPath, explorer = ZipFileExplorer):
        if(not zipPath.endswith(".zip")):
            raise IOError("Not valid zip file")
        super().__init__(zipPath, explorer, "Zip File Explorer")
    def set_explorer(self, exp):
        self._exp = exp

    def render(self):
        self.displayLog("")
        self._unobserveWidgets()
        folders, files = self.explorer.dirList()
        folders = list(folders)
        self.inputArea.dirList.options = ExplorerUtils.dirsWithIcon(folders) + files
        self.inputArea.pathsList.options = self._dropDownPaths()
        self._observeWidgets()

    def _dropDownPaths(self):
        vals = self.explorer._currentPath.split(self.explorer.sep)
        dropList = []
        vals.pop()
        for _ in range(len(vals)):
            dropList.append(self.explorer.sep.join(vals))
            vals.pop()
        return dropList

    def displayFileElement(self, change):
        self.extractFile()
        if(self.getSelectedFile() == ''):
            self.displayLog('No file selected')
        else:
            try:
                fpath = self.explorer.sep.join([self.explorer._extractingPath,
                    self.explorer._currentPath, self.getSelectedFile()])
                with self.outputArea:
                    self.displayer.displayPath(fpath)
            except Exception as e:
                self.displayLog(str(e))

    def copyPath(self, k):
        from ancient.ClipboardDB import ClipboardDB
        self.extractFile()
        fileName = self.getSelectedFile()
        p = self.explorer._extractingPath + self.explorer.sep + self.explorer._currentPath
        if(fileName != ''):
            p += self.explorer.sep + fileName
        ClipboardDB.copy2clipboard(os.path.abspath(p))
        self.displayLog(f"copied Path:{p}")

    def extractFile(self):
        file = self.getSelectedFile()
        if(file == ''):
            return
        p = self.explorer.sep.join([self.explorer._extractingPath, self.explorer.zipPath , file])
        if(not os.path.exists(os.path.abspath(p))):
            self.explorer.extract(file)


class IButtonOps:
    def get(self):
        pass
    def set_parent(self, parent):
        pass
class GButtonOps(IButtonOps):
    def set_parent(self, parent):
        self._parent = parent
        self._out = parent._wd._wid.components.outputDisplay
        self._selection = parent._wd._wid.components.selection
class CopyCurrentPathOps(GButtonOps):
    def __init__(self):
        self._btn = widgets.Button(description="copy path", layout={'width':'auto'})
        self._btn.on_click(self._callback)
    def get(self):
        return self._btn
    def _callback(self, btn):
        from ancient.ClipboardDB import ClipboardDB
        selected = self._selection.value
        path = selected
        if ExplorerUtils.dirIcon() in selected:
            path = path.replace(ExplorerUtils.dirIcon(), "").strip()
        openable_apth = self._parent.extracting_path(path)
        p = os.path.abspath(openable_apth)
        ClipboardDB.copy2clipboard(p)
        self._out.clear_output()
        with self._out:
            print(f"copied Path\n{p}")
            

class DisplayFileOps(GButtonOps):
    def __init__(self):
        from modules.Explorer.displayer import ExplorerFileDisplayer
        self._btn = widgets.Button(description="display", layout={'width':'auto'})
        self._btn.on_click(self._callback)
        self._displayer = ExplorerFileDisplayer()
    def get(self):
        return self._btn
    def _callback(self, btn):
        self._out.clear_output()
        selected = self._selection.value
        if ExplorerUtils.dirIcon() in selected:
            return
        openable_apth = self._parent.extracting_path(selected)
        with self._out:
            if not os.path.exists(openable_apth):
                self._parent._wd._exp.extract(selected)
            self._displayer.displayPath(openable_apth)
            
class ExtractThisPathOps(GButtonOps):
    def __init__(self):
        self._confirm_btn = widgets.Button(description="confirm")
        self._btn = widgets.Button(description="extract_this_path", layout={'width':'auto'})
        self._btn.on_click(self._callback)
        self._confirm_btn.on_click(self._on_confirm)
    def get(self):
        return self._btn
    def _callback(self, btn):
        self._out.clear_output()
        with self._out:
            files2extract = filter(lambda x: x.startswith(self._parent._wd._exp._currentPath + "/"), self._parent._wd._exp._files)
            self._not_extracted_files = list(filter(lambda x: not os.path.exists(self._parent._wd._exp._extractingPath +  os.sep + x), 
                files2extract))
            print(f"files to extracted: {len(self._not_extracted_files)}")
            display(self._confirm_btn)
    def _on_confirm(self, btn):
        self._parent._wd._exp.tool.extractWithPaths(self._parent._wd._exp.zipPath, 
            self._not_extracted_files, to = self._parent._wd._exp._extractingPath)
        self._out.clear_output()
            
class NewZipFileExplorer(IExplorerDisplayer):
    def __init__(self, zipPath):
        from modules.Explorer.model import ZipExplorer
        self._make_layout()
        self.set_explorer(ZipExplorer(zipPath))
        self._wd.set_location_func(lambda x: self._wd._exp._currentPath)
    def set_explorer(self, exp: IExplorer):
        self._wd.set_explorer(exp)
    def _make_layout(self):
        self._wd = WidgetsIpyExplorerDisplayer('exp')
        self._wd.get()
        self.add_ops(DisplayFileOps())
        self.add_ops(CopyCurrentPathOps())
        self.add_ops(ExtractThisPathOps())

    def display(self):
        return self._wd.display()
    
    def extracting_path(self, file):
        if self._wd._exp._currentPath == "":
            return self._wd._exp.sep.join([self._wd._exp._extractingPath, file])
        return self._wd._exp.sep.join([self._wd._exp._extractingPath,self._wd._exp._currentPath, file])

    def add_ops(self, ops: IButtonOps):
        self._wd._wid.components.footer.add_widget(ops.get())
        ops.set_parent(self)