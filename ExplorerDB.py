from modules.Explorer.displayer import IExt,NotebookGeneralDisplayer
class ExplorerDB:
    _exp = None
    def zipExplorer(path, exts = {}):
        from modules.Explorer.ZipFileExplorerDisplayer import ZipFileExplorerDisplayer
        from modules.Explorer.model import ZipExplorer
        return ExplorerDB._setExtraDisplayer(ZipFileExplorerDisplayer(path, ZipExplorer), exts)
    def _setExtraDisplayer(exp, exts):
        for key in exts:
            exp.displayer.set_extension_displayer(key,exts[key])
        ExplorerDB._exp = exp
        return exp
    def dicExplorer(dic, name = None):
        import json
        from LibsDB import LibsDB
        from SerializationDB import SerializationDB
        from IPython.display import HTML
        from CryptsDB import CryptsDB
        from FileDatabase import File
        from TimeDB import TimeDB
        from htmlDB import htmlDB
        content = htmlDB.urlDecode(SerializationDB.readPickle(LibsDB.picklePath("globals"))['codes']['dictionary explorer'])
        if(name is None):
            name = CryptsDB.generateRandomName()
        name += ".html"
        File.createFile(name,content.replace("#0>3847dicq398423<0#",str(json.dumps(dic))))
        File.openFile(name)
        TimeDB.setTimer().oneTimeTimer(10, File.deleteFiles, [[name]])
    def osFileExplorer(path=None, exts = {}):
        from modules.Explorer.displayer import OSFileExplorerDisplayer
        return ExplorerDB._setExtraDisplayer(OSFileExplorerDisplayer(path), exts)
    def _callback(ele):
        selected = ele.getCurrentValue()
        exp = ele.parent.parent.lister.dicExp
        if selected == '..':
            exp.goBack()
            return
        content = exp.getCurrentValue()
        if type(content) == dict:
            exp.cd(selected)
    def cmdDicExplorer(dic, lister =None, displayer=None):
        from modules.mobileCode.CmdCommand import GController, DicList, DisplayElements, CmdCommandHandler
        if lister is None:
            lister = DicList()
        if displayer is None:
            displayer = DisplayElements()
            displayer._runAfter = True
        handler = CmdCommandHandler(callback= ExplorerDB._callback)
        GController(dic,cmdRunner = handler, lister = lister, displayer = displayer).run()
    def dream3dFileExplorer(file):
        from modules.mobileCode.CmdCommand import GController
        from modules.rlib_notebook_tools.instructions_tool import ViewRunner, hdf5Explorer
        exp = hdf5Explorer()
        exp.setData(file)
        cnt = GController(lister=exp,  cmdRunner= ViewRunner(callback= exp.cd))
        cnt.run()
        return cnt
    def pickleExplorer(file):
        from modules.GUIs.PickleOps import PickleExpController
        return PickleExpController(file)