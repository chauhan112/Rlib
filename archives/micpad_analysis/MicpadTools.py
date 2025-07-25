import os
from useful.Path import Path
from useful.Database import Database
from useful.SerializationDB import SerializationDB
from ancient.ClipboardDB import ClipboardDB
from useful.LibsDB import LibsDB
class MicpadTools:
    def total_mic_files(micpath):
        total_files = []
        extensions = ["h", "cpp", "xml", "png", "ico", "pro", "qrc"]
        for e in extensions:
            total_files += Path.filesWithExtension(e, micpath, walk= False)
        return total_files
    def cppNheaderFiles(micPath):
        total_files = []
        extensions = ["h", "cpp"]
        for e in extensions:
            total_files += Path.filesWithExtension(e, micPath, walk= False)
        return total_files
    def sizeCompare(a,b):
        print(f"Size of a {len(a)}")
        print(f"Size of b {len(b)}")
        print("A - B")
        print(set(map(os.path.basename,a)).difference(set(map(os.path.basename,b))))
        print("B - A")
        print(set(map(os.path.basename,b)).difference(set(map(os.path.basename,a))))
class MicpadStuff:
    def pathRes():
        from archives.locally_temporal.Bachelorarbeit import Bachelorarbeit
        dic = SerializationDB.readPickle(LibsDB.picklePath("globals.pkl"))
        return Bachelorarbeit.reprocessCloudPath(dic['archive']['micpad_resource_aug_2020'])
    def linksDB(word = None):
        links = SerializationDB.readPickle(f"{MicpadStuff.pathRes()}{os.sep}links.pkl")
        db = Database.urlDB(links)
        return Database.dbSearch(db,word)
    def addToLinks(key, val):
        MicpadStuff.addToPaths(key,val, f"{MicpadStuff.pathRes()}{os.sep}links.pkl")
    def pathDB(word = None):
        from useful.Path import Path
        def dis(x):
            Path.openExplorerAt(x)
            print(x)
            ClipboardDB.copy2clipboard(x)
            print("copied path")
        db = Database.dicDB(MicpadStuff.getPaths(), displayer=dis)
        return Database.dbSearch(db,word)
    def getPaths():
        paths = SerializationDB.readPickle(f"{MicpadStuff.pathRes()}{os.sep}paths.pkl")
        return paths
    def addToPaths(val, path, pkl = None):
        if(pkl is None):
            pkl = f"{MicpadStuff.pathRes()}{os.sep}paths.pkl"
        paths = MicpadStuff.getPaths()
        paths[val] = path
        SerializationDB.pickleOut(paths, pkl)
    def projects(typ = "r"):
        from ancient.otherLangs.cpp.CppProject import CppProject
        if(typ.lower() in ['r', 'rebase', 'rebased', 'latest', 'late']):
            return CppProject(MicpadStuff.rebased)
        elif(typ.lower() in ['mine', 'backup', 'mi', 'b']):
            return CppProject(MicpadStuff.mine)
        else:
            return CppProject(MicpadStuff.master)
    def qtLibFiles():
        qtFilesPath = Path.joinPath(LibsDB.cloudPath(), "Global", "code", "Code Godown",
                                    "qt code", "comments removed code")
        qtFiles = Path.getFiles(qtFilesPath, walk = True)
        return qtFiles
    def qtLibNameDB(word = None):
        db = Database.getDB(MicpadStuff.qtLibFiles(), keysFilter=os.path.basename)
        return Database.dbSearch(db, word)
    def qtFileSearchDB(files, word = None):
        db = Database.textFilesDB(files)
        return Database.dbSearch(db, word)
    def displayTabFiles(content):
        import ipywidgets as widgets
        return widgets.HTML(
            value=f"""<textarea id="w3review" name="w3review" rows="10" style="font-family: 'Courier New'" cols="200">{content}</textarea>""",
            placeholder='Type something',
            disabled=False
        )