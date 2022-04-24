import os
from modules.Explorer.displayer import FileExplorerDisplayer
from modules.Explorer.model import ZipFileExplorer, ExplorerUtils
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
        from ClipboardDB import ClipboardDB
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


class NewZipFileExplorer(IExplorerDisplayer):
    def __init__(self, zipPath):
        from modules.Explorer.model import ZipExplorer
        self._make_layout()
        self.set_explorer(ZipExplorer(zip_path))
        self._wd.set_location_func(lambda x: self._wd._exp._currentPath)
    def set_explorer(self, exp: IExplorer):
        self._wd.set_explorer(exp)
    def _make_layout(self):
        
        from modules.Explorer.displayer import ExplorerFileDisplayer
        self._wd = WidgetsIpyExplorerDisplayer('exp')
        self._wd.set_file_displayers(ExplorerFileDisplayer())
        self._wd._wid.components.footer.add_widget(widgets.Button(description="display", layout={'width':'auto'}))
        self._wd._wid.components.footer.add_widget(widgets.Button(description="copy path", layout={'width':'auto'}))
        self._wd._wid.components.footer.add_widget(widgets.Button(description="extract_this_path", layout={'width':'auto'}))
        self._wd._wid.components.footer.get_child(0).on_click(self._extract_n_open)
        self._wd._wid.components.footer.get_child(1).on_click(self._copy_path)
        self._wd._wid.components.footer.get_child(2).on_click(self._extract_path)
    def display(self):
        return self._wd
    def _copy_path(self, btn):
        from ClipboardDB import ClipboardDB
        selected = self._wd._wid.components.selection.value
        path = selected
        if ExplorerUtils.dirIcon() in selected:
            path = path.replace(ExplorerUtils.dirIcon(), "").strip()
        openable_apth = extracting_path(path)
        p = os.path.abspath(openable_apth)
        ClipboardDB.copy2clipboard(p)
        out = self._wd._wid.components.outputDisplay
        out.clear_output()
        with out:
            print(f"copied Path\n{p}")
    def _extracting_path(self, file):
        if self._wd._exp._currentPath == "":
            return self._wd._exp.sep.join([self._wd._exp._extractingPath, file])
        return self._wd._exp.sep.join([self._wd._exp._extractingPath,self._wd._exp._currentPath, file])

    def _extract_path(self, btn):
        out = self._wd._wid.components.outputDisplay
        out.clear_output()
        with out:
            files2extract = filter(lambda x: x.startswith(self._wd._exp._currentPath), self._wd._exp._files)
            not_extracted_files = filter(lambda x: not os.path.exists(self._wd._exp._extractingPath +  os.sep + x), files2extract)
            print(f"files to extracted: {len(list(not_extracted_files))}")
            self._wd._exp.tool.extractWithPaths(self._wd._exp.zipPath,not_extracted_files, to = self._wd._exp._extractingPath)
    def _extract_n_open(self, btn):
        out = self._wd._wid.components.outputDisplay
        out.clear_output()
        selected = self._wd._wid.components.selection.value
        if ExplorerUtils.dirIcon() in selected:
            return
        openable_apth = extracting_path(selected)
        with out:
            if not os.path.exists(openable_apth):
                self._wd._exp.extract(selected)
            self._wd._displayer.displayPath(openable_apth)
