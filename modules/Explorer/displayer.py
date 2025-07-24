import os

from modules.Explorer.model import ExplorerUtils, ZipFileExplorer,OSFileExplorer

class IExt:
    def setPath(self, path):
        self.path = os.path.abspath(path)
    def display(self):
        raise NotImplementedError("abstract method")
def NewCodeDisplayer():
    from timeline.t2024.code_highlight import CodeHighlighter
    from basic import Main as ObjMaker
    from useful.FileDatabase import File
    chl = CodeHighlighter()
    lang = "py"
    def set_language(lang):
        s.process.lang = lang
    def display(filepath):
        content = File.getFileContent(filepath)
        chl.handlers.set_content(content, s.process.lang)
        return chl.views.container.outputs.layout
    s = ObjMaker.variablesAndFunction(locals())
    return s
class NotebookGeneralDisplayer(IExt):
    def __init__(self, func ):
        self.func = func
    def display(self):
        from IPython.display import display
        display(self.func(self.path))

class DisplayInMd(IExt):
    def __init__(self,ext, keyword = None):
        self.ext = ext
        self.keyword = keyword
        if keyword is None:
            self.keyword = ext
    def display(self):
        from useful.ModuleDB import ModuleDB
        from useful.FileDatabase import File
        dp = NotebookGeneralDisplayer(lambda path: ModuleDB.colorPrint(self.keyword, 
                                File.getFileContent(path)))
        dp.setPath(self.path)
        dp.display()
        
class DefaultOpener(IExt):
    def display(self):
        from useful.FileDatabase import File
        File.openFile(self.path)
    
class ExplorerFileDisplayer:
    def __init__(self, extDic = {}):
        # extDic = {'py': something} , something is of type IExt
        self.extDic = self._defaultDisplayer()
        for key in extDic:
            self.set_extension_displayer(key, extDic[key])
        self.ncd = NewCodeDisplayer()
    def _defaultDisplayer(self):
        extDic= {}
        from useful.FileDatabase import File
        from useful.ModuleDB import ModuleDB
        from archives.NotebookDB import NotebookDB
        from ancient.ImageProcessing import ImageProcessing, ShowImage
        from useful.ExplorerDB import ExplorerDB
        from useful.LibsDB import LibsDB
        from useful.SerializationDB import SerializationDB
        data = SerializationDB.readPickle(LibsDB.picklePath("GeneralDB"))
        standardContentFiles = data['files_to_read']
        for ext in standardContentFiles:
            extDic[ext] = DisplayInMd(ext)
        for ext in data["hasLexers"]:
            extDic[ext] = NotebookGeneralDisplayer(lambda x: self.hasLexers(ext, x))
        
        extDic['png'] = NotebookGeneralDisplayer(ImageProcessing.showImgFromFile)
        extDic['jpg'] = NotebookGeneralDisplayer(ImageProcessing.showImgFromFile)
        extDic['ipynb'] = NotebookGeneralDisplayer(lambda path: ModuleDB.colorPrint('python',
                                                "\n".join(NotebookDB.getCodeCellContent(path))))
        extDic['gif'] = NotebookGeneralDisplayer(lambda path: ShowImage.gif(path).animate())
        extDic['dcm'] = NotebookGeneralDisplayer(ShowImage.displayDCMImage)
        extDic['zip'] = NotebookGeneralDisplayer(ExplorerDB.zipExplorer)
        extDic['pkl'] = NotebookGeneralDisplayer(ExplorerDB.pickleExplorer)
        extDic['webp'] = NotebookGeneralDisplayer(self.webp)
        return extDic
    def hasLexers(self,lang, path):
        self.ncd.handlers.set_language(lang)
        return self.ncd.handlers.display(path)
    def webp(self, filepath):
        from PIL import Image
        im = Image.open(filepath)
        return im

    def displayPath(self, path):
        ext = path.split(".")[-1].lower()
        if(ext in self.extDic):
            self.extDic[ext].setPath(path)
            self.extDic[ext].display()
        else:
            do =DefaultOpener()
            do.setPath(path)
            do.display()
    def set_extension_displayer(self, ext, funcOrDisplayer: IExt):
        if not isinstance(funcOrDisplayer, IExt):
            self.extDic[ext] = NotebookGeneralDisplayer(funcOrDisplayer)
        else:
            print("unknown extension function instance")
            
class IpywidgetsDisplayer:
    def __init__(self, explorer, exts = {}):
        from useful.WidgetsDB import WidgetsDB
        self.explorer = explorer
        self.inputArea, self.outputArea = WidgetsDB.ioArea()
        self.displayer = ExplorerFileDisplayer(exts)
        
    def setFileDisplayer(self, ext, func):
        self.displayers[ext.lower()] = func
    
    def getSelectedFile(self):
        raise IOError("Search function Not implemented yets")
        
    def displayLog(self, msg):
        raise IOError("Search function Not implemented yets")
        
class FileExplorerDisplayer(IpywidgetsDisplayer):
    def __init__(self, path = None, explorer = OSFileExplorer, title = ''):       
        import ipywidgets as widgets
        super().__init__(explorer(path))
        self.inputArea.log = widgets.HTML(value='')
        self.inputArea.fileOps.children += (self.inputArea.log,)
        self.addEventsNCallbacks()
        self.setInitialValues(title)
        
    def setInitialValues(self, title):
        self.inputArea.title.value = title
        self.displayLog('')
        self.inputArea.b1.description = 'copy filepath'
        self.inputArea.b2.description = 'display'
        self.render()
        
    def addEventsNCallbacks(self):
        self._oneTimeEvent()
        self._observeWidgets()
    
    def _oneTimeEvent(self):
        self.inputArea.b1.on_click(self.copyPath)
        self.inputArea.b2.on_click(self.displayFileElement)
    
    def _unobserveWidgets(self):
        self.inputArea.pathsList.unobserve(self._on_pathList_select, names = 'value')
        self.inputArea.dirList.unobserve(self._on_dirlist_select, names = 'value')
    
    def _observeWidgets(self):
        self.inputArea.pathsList.observe(self._on_pathList_select, names = 'value')
        self.inputArea.dirList.observe(self._on_dirlist_select, names = 'value')
        
    def _on_pathList_select(self, change):
        self.explorer.path = change['new']
        self.render()
    
    def _on_dirlist_select(self,change):
        if(change['new'][0] == ExplorerUtils.dirIcon()):
            self.explorer.cd(change['new'].replace(ExplorerUtils.dirIcon(), '').strip())
            self.inputArea.filename.value = ''
            self.inputArea.b1.visibility  = 'hidden'
            self.inputArea.b2.visibility  = 'hidden'
            self.render()
        else:
            self.inputArea.b1.visibility  = 'visible'
            self.inputArea.b2.visibility  = 'visible'
            self.inputArea.filename.value = change['new']
        self.outputArea.clear_output()
        self.displayLog('')
        
    def render(self):
        self.displayLog("")
        self._unobserveWidgets()
        folders, files = self.explorer.dirList()
        self.inputArea.dirList.options = ExplorerUtils.dirsWithIcon(folders) + files
        self.inputArea.pathsList.options = ExplorerUtils.getDropdownPathSubList(self.explorer.path)
        self._observeWidgets()

    def getSelectedFileExtension(self):
        return self.inputArea.filename.value.split(".")[-1].lower()
    
    def getSelectedFile(self):
        return self.inputArea.filename.value
    
    def displayLog(self, msg):
        self.inputArea.log.value = msg

    def displayFileElement(self, change):
        raise IOError("Not Implemented Error")

    def copyPath(self, k):
        raise IOError("Not Implemented Error")

class OSFileExplorerDisplayer(FileExplorerDisplayer):
    def __init__(self, path = None):
        from useful.WidgetsDB import WidgetsDB
        super().__init__(path, OSFileExplorer, 'OS File Explorer')
        ch = list(self.inputArea.fileOps.children)
        self._openExplorerBtn = WidgetsDB.button('Open in explorer', self.openExpl)
        self.inputArea.fileOps.children = tuple(ch[:2] + [self._openExplorerBtn] + [ch[-1]])
        
    def openExpl(self, btn):
        from useful.Path import Path
        Path.openExplorerAt(self.explorer.path)

    def displayFileElement(self, change):
        if(self.getSelectedFile() == ''):
            self.displayLog('No file selected')
        else: 
            try:
                fpath = self.explorer.path + self.explorer.sep + self.getSelectedFile()
                with self.outputArea:
                    self.displayer.displayPath(fpath)
            except Exception as e:
                self.displayLog(str(e))

    def copyPath(self, k):
        from ancient.ClipboardDB import ClipboardDB
        fileName = self.getSelectedFile()
        p = self.explorer.path
        if(fileName != ''):
            p += self.explorer.sep + fileName
        ClipboardDB.copy2clipboard(p)
        self.displayLog(f"copied Path:{p}")



