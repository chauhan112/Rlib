from Path import Path
class _Opener:
    def pathDB(filesContainer):
        from SearchSystem import FilePathsSearchEngine
        fdb = FilePathsSearchEngine(filesContainer)
        return fdb
    
    def pathAsDic():
        from Path import FrequentPaths
        return FrequentPaths.pathAsDic()

class _DocInterface:
    def __init__(self):
        self._conDB = None
    def _getFiles(self):
        return self._files
    def pathDB(self):
        return _Opener.pathDB(self._getFiles())
    def contentDB(self):
        from Database import Database
        if(self._conDB is None):
            self._conDB = Database.pdfDB(self._getFiles())
        return self._conDB
    def set_files(self, files):
        self._files = files
class MathTheoryAndExercises:
    from Database import Database
    dbs = {}
    def lin_alg():
        class Teml:
            def one():
                class Temp:
                    def docs(refresh = False):
                        key = 'lin_alg one'
                        class T(_DocInterface):
                            def _getFiles(self):
                                return Path.filesWithExtension("pdf", Path.joinPath(
                                    _Opener.pathAsDic()['linear algebra LA 1'], "Books Scripts"), False)
                        if(refresh):
                            MathTheoryAndExercises.dbs[key] = T()
                        try:
                            MathTheoryAndExercises.dbs[key]
                        except: 
                            MathTheoryAndExercises.dbs[key] = T()
                        return MathTheoryAndExercises.dbs[key] 
                    def exercises():
                        class T:
                            def _getPath():
                                return Path.joinPath(_Opener.pathAsDic()['linear algebra LA 1'], 
                                                    r"Practice materials\HW n CW")
                            
                            def quesions():
                                class Q(_DocInterface):
                                    def _getFiles(self):
                                        return Path.filesWithExtension("pdf", Path.joinPath(T._getPath(), "Questions"))
                                return Q()
                            
                            def answers():
                                class M:
                                    def mine():
                                        return _Opener.pathDB(Path.filesWithExtension("pdf", 
                                            Path.joinPath(T._getPath(), "My Solutions")))
                                    def others():
                                        return _Opener.pathDB(Path.filesWithExtension("pdf", 
                                            Path.joinPath(T._getPath(), "Other Solutions")))
                                return M
                        return T
                return Temp
            
            def two():
                class Temp:
                    def docs(refresh = False):
                        return Teml.one().docs(refresh)
                    
                    def exercises():
                        class T:
                            def _getPath():
                                return Path.joinPath(_Opener.pathAsDic()['linear algebra LA 2'], "CW n HW")
                            def questions():
                                return _Opener.pathDB(Path.filesWithExtension("pdf", 
                                                Path.joinPath(T._getPath(), "Tasks")))
                            def answers():
                                return _Opener.pathDB(Path.filesWithExtension("pdf", 
                                                Path.joinPath(T._getPath(), r"Solutions\Ilias")))
                        return T
                return Temp
            

        return Teml
    
    def analysis():
        class Teml:
            def one():
                class Temp:
                    def _getPath():
                        return _Opener.pathAsDic()["Ana 1"]
                    
                    def docs(refresh = False):
                        key = 'ana one'
                        class T(_DocInterface):
                            def _getFiles(self):
                                return Path.filesWithExtension("pdf", Path.joinPath(Temp._getPath(), 
                                                                                    "Books Scripts\books"))
                        if(refresh):
                            MathTheoryAndExercises.dbs[key] = T()
                        try:
                            MathTheoryAndExercises.dbs[key]
                        except: 
                            MathTheoryAndExercises.dbs[key] = T()
                        return MathTheoryAndExercises.dbs[key] 
                    
                    def exercises():
                        class T:
                            def _openDB(paths):
                                files = []
                                for path in paths:
                                    files += Path.filesWithExtension("pdf", path)
                                return _Opener.pathDB(files)
                            def questions():
                                class Q:
                                    cw_path = Path.joinPath(Temp._getPath(), "Practice materials", "CW")
                                    hw_path = Path.joinPath(Temp._getPath(), "Practice materials", "HW")
                                    def cw():
                                        return T._openDB([Q.cw_path])
                                    def hw():
                                        return T._openDB([Q.hw_path])
                                    def both():
                                        return T._openDB([Q.hw_path, Q.cw_path])
                                return Q
                            
                            def answers():
                                class A:
                                    cw_path = Path.joinPath(Temp._getPath(), "Practice materials", "Losüngs CW")
                                    hw_path = Path.joinPath(Temp._getPath(), "Practice materials", "HW answers")
                                    def cw():
                                        return T._openDB([A.cw_path])
                                    def hw():
                                        return T._openDB([A.hw_path])
                                    def both():
                                        return T._openDB([A.hw_path, A.cw_path])
                                return A
                        return T
                return Temp
            
            def two():
                class Temp:
                    def _getPath():
                        return _Opener.pathAsDic()["Ana 2"]
                    
                    def docs(refresh = False):
                        key = "Ana 2"
                        class T(_DocInterface):
                            def _getFiles():
                                return Path.joinPath(Temp._getPath(), "Ana2_Skript.pdf")
                        if(refresh):
                            MathTheoryAndExercises.dbs[key] = T()
                        try:
                            MathTheoryAndExercises.dbs[key]
                        except: 
                            MathTheoryAndExercises.dbs[key] = T()
                        return MathTheoryAndExercises.dbs[key] 
                    
                    def exercises():
                        class AQ:
                            def _getType():
                                raise IOError("Not implemented yet")
                            def cw():
                                return Path.joinPath(Temp._getPath(), "CW", QA._getType())
                            def hw():
                                return Path.joinPath(Temp._getPath(), "HW", QA._getType())
                            
                        class T:
                            def _openDB(path):
                                files = Path.filesWithExtension("pdf", path)
                                return _Opener.pathDB(files)
                            
                            def questions():
                                class Q(QA):
                                    def _getType():
                                        return "Tasks"
                                return Q
                            
                            def answers():
                                class A(QA):
                                    def _getType():
                                        return "Solutions"
                                return A
                        return T
                return Temp
        return Teml
    
    def numericalAnalysis():
        class Temp:
            def _getPath():
                return _Opener.pathAsDic()["numerik"]

            def docs(refresh = False):
                key = 'Numerik'
                class T(_DocInterface):
                    def _getFiles(self):
                        path = Path.joinPath(Temp._getPath(), r"data\num-book chapterwise")
                        return Path.filesWithExtension("pdf", path)
                    def otherDocs(self):
                        class OD(_DocInterface):
                            def _getFiles(self):
                                path = Path.joinPath(Temp._getPath(), r"data\books")
                                return Path.filesWithExtension("pdf", path)
                        return OD()
                if(refresh):
                    MathTheoryAndExercises.dbs[key] = T()
                    
                try:
                    MathTheoryAndExercises.dbs[key]
                except: 
                    MathTheoryAndExercises.dbs[key] = T()
                return MathTheoryAndExercises.dbs[key] 
            
            def exercises():
                class T:
                    def questions():
                        class Q(_DocInterface):
                            def _getFiles(): 
                                path = Path.joinPath(Temp._getPath(), "operations", "Homework")
                                files = Path.filesWithExtension("pdf", path)
                                files = list(filter(lambda x: "NumI-"in x, files))
                                return files
                        return Q
                    
                    def answers():
                        from SearchSystem import FoldersExplorerDisplayer
                        path = Path.joinPath(Temp._getPath(), "operations", "Homework")
                        folders = Path.getDir(path)
                        fdb = FoldersExplorerDisplayer(folders)
                        return fdb
                return T
        return Temp
    
    def stochastik():
        class Temp:
            def _getPath():
                return _Opener.pathAsDic()["Stochastik"]
            
            def docs(refresh = False):
                key = 'Stochastik'
                class T(_DocInterface):
                    def _getFiles(self):
                        path = Path.joinPath(Temp._getPath(), r"data\literature\H schäfer")
                        return Path.filesWithExtension("pdf", path)
                    def otherFiles(self):
                        path = Path.joinPath(Temp._getPath(), r"data\literature\intro to probability", 
                                             "probability book en.pdf")
                        files = Path.filesWithExtension("pdf", path)
                        return _Opener.pathDB(files)
                if(refresh):
                    MathTheoryAndExercises.dbs[key] = T()
                    
                try:
                    MathTheoryAndExercises.dbs[key]
                except: 
                    MathTheoryAndExercises.dbs[key] = T()
                return MathTheoryAndExercises.dbs[key] 
            
            def exercises():
                class T:
                    def questions():
                        path = Path.joinPath(Temp._getPath(), r"operations\Test cases\class")
                        files = Path.filesWithExtension("pdf", path, False)
                        return _Opener.pathDB(files)
                    
                    def answers():
                        path = Path.joinPath(Temp._getPath(), r"operations\Test cases\class\soln")
                        files = Path.filesWithExtension("pdf", path)
                        return _Opener.pathDB(files)
                return T
        return Temp