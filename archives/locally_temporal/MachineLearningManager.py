from useful.Path import FrequentPaths, Path
from useful.SearchSystem import DicSearchEngine
from useful.FileDatabase import File
from useful.Database import Database
class Sth(DicSearchEngine):
    def _callback(self, item):
        import webbrowser
        webbrowser.open(self.searchSys.container[item])
mlPath = Path.joinPath(FrequentPaths.pathAsDic()["ml"], "operations\\class works\\better solutions\\tasks")
class MachineLearningManager:
    def exercises():
        class Tmep:
            def htmlForm(nr):
                file = Tmep._filePath(nr)
                File.openFile(file)
            def defaultForm():
                files = {f"task {n}": Tmep._filePath(n) for n in range(1, 14)}
                s = Sth(files)
                return s
            def inIpynbForm(nr):
                fle = Tmep._filePath(nr, "ipynb")
                content = File.getFileContent(fle)
                File.overWrite("temp.ipynb", content)
                print(f"http://localhost:8888/notebooks/2021/3.%20mar/{os.path.basename(os.getcwd())}/temp.ipynb")

            def _filePath(n, ext = "html"):
                global mlPath
                if(ext == "html"):
                    return Path.joinPath(mlPath,"htmlForm", f"Uebung-{n}.{ext}")
                return Path.joinPath(mlPath, f"Uebung-{n}.{ext}")
        return Tmep   

    def docs():
        class Temp:
            path = Path.joinPath(FrequentPaths.pathAsDic()['ml'], "data", "ML-FZJ-CGN-Kurs-Foliensatz_2020.pdf")
            def load():
                print(Temp.path)
                File.openFile(Temp.path)
            def search(word):
                files = Path.filesWithExtension("pdf", Path.joinPath(FrequentPaths.pathAsDic()['ml'], 
                                                                     "data", "folien"))
                db = Database.pdfDB(files)
                db.search(word)

        return Temp
    def openSolutions():
        class Temp:
            def ipynbForm(n):
                files = Path.filesWithExtension("ipynb", Path.joinPath(FrequentPaths.pathAsDic()["ml"],
                                             "operations\\class works\\better solutions\\solutions"), walk=False)
                if(n is None):
                    return files
                print(MachineLearningManager.getLinkForFile(files[n]))

            def htmlForm(n = None):
                hPath = Path.joinPath(FrequentPaths.pathAsDic()["ml"], "operations","class works",
                            "better solutions", "solutions", "htmlForm", "Task {:0>2d}.html")
                if(n is not None ):
                    File.openFile(hPath.format(n))
                    return
                files = {f"Task {i}":hPath.format(i) for i in range(1, 14)}
                s = Sth(files)
                return s
            def db():
                from useful.FileDatabase import File
                from useful.SearchSystem import FilesContentSearchEngine
                class HtmlContentSearch(FilesContentSearchEngine):
                    def _callback(self, item):
                        File.openFile(item[0])
                hPath = Path.joinPath(FrequentPaths.pathAsDic()["ml"], "operations","class works",
                            "better solutions", "solutions", "htmlForm", "Task {:0>2d}.html")
                files = [hPath.format(i) for i in range(1, 14)]
                return HtmlContentSearch(files)
                
        return Temp
    def getLinkForFile(f):
        from useful.RegexDB import RegexDB
        return RegexDB.replace(".*timeline",f, 
                               lambda x: "http://localhost:8888/notebooks").replace(os.sep, "/").replace(" ","%20")
    def folder():
        Path.openExplorerAt(Path.joinPath(FrequentPaths.pathAsDic()["ml"]))

    def codes():
        from useful.SearchSystem import FilesContentSearchEngine
        p = Path.joinPath(FrequentPaths.pathAsDic()["ml"], r"operations\class works\exam prep")
        files = Path.filesWithExtension("py", p)
        return FilesContentSearchEngine(files)