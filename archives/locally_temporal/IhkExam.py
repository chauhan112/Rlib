from Path import FrequentPaths, Path
class IhkExam:
    from Path import FrequentPaths
    ihkPath = FrequentPaths.pathAsDic()["ihk exam"]
    dbs = {}
    def qa():
        qaPath = Path.joinPath(IhkExam.ihkPath, "ops", "sets with solutions")
        class Temp:
            def _getPath(self):
                raise IOError("Not implemented yet")

            def questions(self):
                files = Path.filesWithExtension("pdf", Path.joinPath(self._getPath(), "questions"))
                IhkExam.fileSearch(files)

            def solutions(self):
                files = Path.filesWithExtension("pdf", Path.joinPath(self._getPath(), "solutions"))
                IhkExam.fileSearch(files)

            def both(self):
                print("Questions")
                self.questions()
                print("Solutions")
                self.solutions()
        class Tme:
            def maths():
                class TempMath(Temp):
                    def _getPath(self):
                        return Path.joinPath(qaPath, "mathematik")
                return TempMath()

            def informatik():
                class TempInfo(Temp):
                    def _getPath(self):
                        return Path.joinPath(qaPath, "informatik")
                return TempInfo()
            
            def wiso():
                class WisoT(Temp):
                    def _getPath(self):
                        return Path.joinPath(qaPath, "wiso")

                    def solutions(self):                        
                        from ExplorerDB import ExplorerDB
                        return ExplorerDB.zipExplorer(Path.joinPath(qaPath, "wiso","WiSo IHK.zip"))
                return WisoT()
        return Tme
    def fileSearch(files,word = ""):
        from SearchSystem import FilePathsSearchEngine
        f = FilePathsSearchEngine(files)
        f.search(word)
        return f

    def modelSets():
        class Temp:
            def search(word = ""):
                files = Temp._files()
                return IhkExam.fileSearch(files, word)
            
            def _files():
                path = Path.joinPath(IhkExam.ihkPath, "ops", "sets without solutions")
                files = Path.filesWithExtension("pdf", path, False)
                return files
                      
            def taskManager():
                from jupyterDB import jupyterDB
                from ListDB import ListDB
                from Path import Path
                class Ops:
                    name = None
                    def add(year):
                        vals = Ops._load()
                        loc = Ops._loc() + [Ops.name, year]
                        ListDB.dicOps().addEvenKeyError(vals, loc,  "")
                        Ops._write(vals)
                    def get():
                        vals = Ops._load()
                        return ListDB.dicOps().get(vals, Ops._loc())
                    def delete(year):
                        vals = Ops._load()
                        loc = Ops._loc() + [Ops.name, year]
                        ListDB.dicOps().delete(vals, loc)
                        Ops._write(vals)
                    def _load():
                        name = "temps"
                        vals = jupyterDB.pickle().read(name)
                        return vals
                    def _loc():
                        return ['archives','locally_temporal','IhkExam','modelSets', 'task manager']
                    def _write(vals):
                        name = "temps"
                        jupyterDB.pickle().write(vals, name)
                class Show:
                    name = None
                    def done():
                        pass
                    def undone():
                        pass
                    def both():
                        pass
                    def _getFullPath(names):
                        import os
                        files = Temp._files()
                        base = os.path.basename(files[0])
                        return [Path.joinPath(base, n) for n in names]
                            
                    def _getFiles():
                        import os
                        allFiles = set([os.path.basename(f) for f in Temp._files()])
                        vals = Ops.get()
                        done = set(vals[Show.name].keys() )
                        notdone = allFiles.difference(done)
                        return list(done), list(notdone)
                    
                class TeInterface:
                    def getIndex(self):
                        raise IOError("Implemnt this")
                    def ops(self):
                        Ops.name = self.getIndex()
                        return Ops
                    def show():
                        Show.name = self.getIndex()
                        return Show
                class Tem:
                    def informatik():
                        class Te(TemInterface):
                            def getIndex(self):
                                return 'informatik'
                        return Te()
                    def maths():
                        class Te(TemInterface):
                            def getIndex(self):
                                return 'maths'
                        return Te()
                    def wiso():
                        class Te(TemInterface):
                            def getIndex(self):
                                return 'wiso'
                        return Te()
                    def wiso():
                        class Te(TemInterface):
                            def getIndex(self):
                                return 'groß_prog'
                        return Te()
                return Temp
            def toPageNr():
                class TeInterface:
                    def search(self,word = ""):
                        from SearchSystem import GeneralSearchEngine
                        from FileDatabase import ChromeAppPdfOpener
                        class Te:
                            def makeDic(pages):
                                import os
                                dci = {}
                                for f in Temp._files():
                                    try:
                                        dci[f] = pages[os.path.basename(f)]
                                    except: 
                                        dci[f] =0
                                return dci
                        return GeneralSearchEngine(Te.makeDic(TeInterface._ops(self.getIndex()).pageNrs()), lambda w,co, ca,re: GeneralSearchEngine.tools().iterate(
                            co, lambda i, val, con: w in val, resAppender= lambda i,val, con: (i, val) ), 
                                    lambda x,y: ChromeAppPdfOpener(x[1]).openIt(y[x[1]]), 
                            lambda x, y: os.path.basename(x[1]), lambda x,y : str(y[x[1]])).search(word)
                    def ops(self):
                        return TeInterface._ops(self.getIndex())
                    def _ops(sub):
                        from jupyterDB import jupyterDB
                        from ListDB import ListDB
                        class TeTe:
                            sub = None
                            def add(index, value):
                                lc = TeTe._loc()
                                lc.append(index)
                                vals = TeTe._read()
                                ListDB.dicOps().addEvenKeyError(vals, lc, value)
                                TeTe._write(vals)
                            
                            def pageNrs():
                                try:
                                    return ListDB.dicOps().get(TeTe._read(), TeTe._loc())
                                except:
                                    return {}
                            def _read():
                                name = "temps"
                                return jupyterDB.pickle().read(name)
                                
                            def _loc():
                                return ['rlibs', "archives", "locally_temporal", "IhkExam", "modelSets", TeTe.sub]
                            
                            def _write(vals):
                                jupyterDB.pickle().write(vals, "temps") 
                        TeTe.sub = sub
                        return TeTe
                    def getIndex(self):
                        raise IOError("Implement this")
                class Tem:
                    def informatik():
                        class Te(TeInterface):
                            def getIndex(self):
                                return "informatik"
                        return Te()
                    def maths():
                        class Te(TeInterface):
                            def getIndex(self):
                                return "maths"
                        return Te()
                    def wiso():
                        class Te(TeInterface):
                            def getIndex(self):
                                return "wiso"
                        return Te()
                    def grosProg():
                        class Te(TeInterface):
                            def getIndex(self):
                                return "gross_prog"
                        return Te()
                    
                return Tem
            
        return Temp
    
    def docs(word = ""):
        class Temp:
            def content(word = ""):
                files = Path.getFiles(Path.joinPath(IhkExam.ihkPath, "docs", "content"), walk=True)
                return IhkExam.fileSearch(files, word)
            def summary(word = ""):
                return IhkExam.fileSearch(Path.getFiles(Path.joinPath(IhkExam.ihkPath, "docs", "zusaamenfassuung"), walk=True), word)
            def explorer():
                from ExplorerDB import ExplorerDB
                return ExplorerDB.osFileExplorer(Path.joinPath(IhkExam.ihkPath, "docs"))
            
            def booksDB(refresh = False):
                if(not ('books' in IhkExam.dbs and not refresh)):
                    print("inde")
                    files = Path.filesWithExtension("pdf", Path.joinPath(IhkExam.ihkPath, "docs", "books"))
                    IhkExam.dbs['books'] = Database.pdfDB(files)
                return IhkExam.dbs['books']
        return Temp
    
    def faysal_docs():
        from ExplorerDB import ExplorerDB
        return ExplorerDB.zipExplorer(IhkExam.ihkPath + os.sep + "IHK_Komplett.zip")
        
        
class GP:
    def getpath():
        from Path import FrequentPaths
        ihkPath = FrequentPaths.pathAsDic()["ihk exam"]
        return Path.joinPath(ihkPath, r"ops\gros_prog")

    def explorer(showContent = False):
        from ExplorerDB import ExplorerDB
        from jupyterDB import jupyterDB
        from TreeDB import TreeDB
        exp = ExplorerDB.osFileExplorer(GP.getpath())
        if(not showContent):
            exp.setFileDisplayer("ipynb", lambda x: TreeDB.openWebLink(jupyterDB.localIpyLink(x, False)))
        return exp

    def structure():
        from FileDatabase import File
        from Path import Path
        File.openFile(Path.joinPath(GP.getpath(), r"Hinweise_GroProg.pdf"))