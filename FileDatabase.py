import os
import webbrowser
from modules.mobileCode.CmdCommand import GDataSetable
class File:
    def createFile(filename, content = ""):
        if(os.path.exists(filename)):
            print(os.path.basename(filename) + " already exists.")
            return
        File.overWrite(filename, content)

    def getFileContent(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()

    def deleteFiles(files):
        for file in files:
            os.remove(file)

    def appendToFile(filename, content):
        if(not os.path.exists(filename)):
            print("File does not exists")
            return
        with open(filename, "a") as myfile:
            myfile.write(content)

    def openFile(file):
        AnyFileOpener().openIt(file)

    def overWrite(filename, content):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

    def createFileStructure(arr, path):
        # create a test case for this
        if(path is None):
            path = os.getcwd()
        if(type(arr) == str):
            File.createFile(os.sep.join([path, arr]))
        elif (type(arr) == dict):
            for key in arr:
                try:
                    os.mkdir(os.sep.join([path, key]))
                except:
                    pass
                File.createFileStructure(arr[key], os.sep.join([path, key]))
        elif(type(arr) == list):
            for f in arr:
                File.createFileStructure(f, path)

    def createFileInsideNonExistingFolder(path, content = '', openMode = "w"):
        import errno
        if not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        if openMode == "w":
            File.overWrite(path, content)
        else:
            with open(path, openMode) as f:
                f.write(content)

    def size(file): # returns size in bytes
        return os.stat(file).st_size

    def rename(oldName, newName):
        os.rename(oldName, newName)

    def program(name, directOpen = False):
        from LibsDB import LibsDB
        from SerializationDB import SerializationDB
        from Database import Database
        programs = SerializationDB.readPickle(LibsDB.picklePath("paths"))['programs']
        if(directOpen):
            File.openFile(programs[name])
            return
        return Database.dbSearch(Database.dicDB(programs, displayer= File.openFile), name)

    def textAround(path, lineNr, around):
        lineNr = lineNr -1
        content = File.getFileContent(path)
        lines = content.splitlines()
        a = lineNr-around
        if(a<0):
            a=0
        arondString = "\n".join(lines[a: lineNr+around+1])
        return arondString

class FileOpener:
    def _open(filePath, typ = None, lineNr = 0):
        from OpsDB import OpsDB
        if(typ is None):
            typ = FileOpener.getType(filePath)
        k = FileOpener.program()
        if(typ == "txt"):
            OpsDB.runOnThread(OpsDB.cmd, (f"\"{k.vscode}\" --goto {filePath}:{lineNr}:{0}",))
        else:
            FileOpener.normalOpen(filePath)

    def program():
        from Path import Path
        return Path._programPaths()

    def normalOpen(filePath):
        webbrowser.open(filePath)

    def getType(filepath):
        txtFile = ['py', 'md', 'cpp', 'h', 'js', 'txt']
        if(os.path.basename(filepath.lower()) in txtFile):
            return "txt"
        return 'unknown'

class IFileOpenerApp:
    def openIt(self, path):
        raise NotImplementedError("Not implemented yet")

class CmdPrinterApp(IFileOpenerApp):
    def __init__(self, around=10, lineNr =0):
        self.around = around
        self.lineNr = lineNr

    def openIt(self, path):
        aroundString = File.textAround(path, self.lineNr, self.around)
        print(aroundString)

class CmdFileOpen(IFileOpenerApp, GDataSetable):
    def openIt(self, path):
        lineNr = self.data
        import os
        os.system(f"view +{lineNr} {os.path.abspath(path)} --cmd \":set number\"")

class MarkDownFileOpenerApp(IFileOpenerApp):
    def __init__(self, around=10, lineNr=0):
        self.around = around
        self.lineNr = lineNr

    def openIt(self, path):
        content = File.textAround(path, self.lineNr,self.around)
        from ModuleDB import ModuleDB
        from IPython.display import display
        display(ModuleDB.colorPrint('python', content))

class NotepadAppTextOpener(IFileOpenerApp, GDataSetable):
    def __init__(self, notepadExePath=None):
        self.notepadExePathWithParams = f'"{notepadExePath}"'+' "{}" -n{}'
        if(notepadExePath is None):
            from SerializationDB import SerializationDB
            from ModuleDB import ModuleDB
            from LibsDB import LibsDB
            dic = SerializationDB.readPickle(LibsDB.picklePath("paths"))
            path = dic['programs'][ModuleDB.laptopName()]['notepad++']
            self.notepadExePathWithParams = f'"{path}"'+' "{}" -n{}'


    def openIt(self, path):
        lineNr= self.data
        from OpsDB import OpsDB
        cmd = self.notepadExePathWithParams.format(path, lineNr)
        OpsDB.cmd().onthread([cmd])

class ChromeAppPdfOpener(IFileOpenerApp):
    def __init__(self,pageNr=0,chromeExe =None):
        self.pageNr = pageNr
        if(chromeExe is None):
            chromeExe = self._get_chrome()
        self.set_chrome(chromeExe)

    def openIt(self, path):
        from OpsDB import OpsDB
        urlPath = path.replace(os.sep, "/")
        fpu = f"file:///{urlPath}#page={self.pageNr}"
        OpsDB.cmd().onthread(f'"{self.chromeExe}" "{fpu}"')
    def set_chrome(self, chrome):
        self.chromeExe = chrome
    def _get_chrome(self):
        from SerializationDB import SerializationDB
        from ModuleDB import ModuleDB
        from LibsDB import LibsDB
        dic = SerializationDB.readPickle(LibsDB.picklePath("paths"))
        return dic['programs'][ModuleDB.laptopName()]['chrome']

class ChromeHtmlFileOpenerWithHashTag(ChromeAppPdfOpener):
    def __init__(self):
        self.set_chrome(self._get_chrome())
    def openIt(self, html_path):
        import webbrowser
        webbrowser.get(f"{self.chromeExe.replace(os.sep, '/')} %s").open("file:///" + html_path)
        
class AnyFileOpener(IFileOpenerApp):
    def openIt(self, path):
        from SystemInfo import SystemInfo
        if(os.path.exists(path)):
            if(SystemInfo.isLinux()):
                os.system(f"xdg-open '{path}'")
            else:
                import webbrowser
                webbrowser.open(path)
        else:
            print(path + " does not exists")

class LinuxOpensuseVSCodeOpener(IFileOpenerApp):
    def __init__(self):
        self.set_linenr(0)
    def openIt(self, path):
        from OpsDB import OpsDB
        OpsDB.cmd().run(f'code --goto "{path}:{self._nr}"')
    def set_linenr(self, nr):
        self._nr = nr
