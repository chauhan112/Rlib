class DB_SWT:
    _dbs = {}
    def db():
        from Path import FrequentPaths, Path
        from Database import Database
        from SearchSystem import FilePathsSearchEngine
        class Temp:
            def docs():
                docsPath = Path.joinPath(Temp._path(), "data")
                files = Path.filesWithExtension("pdf", docsPath,False)
                p2 = Path.joinPath(Temp._path(), r"operations\Classwork\material")
                files += Path.filesWithExtension("pdf", p2)
                return DB_SWT._dbdb('db docs', files, Database.pdfDB)

            def exercise():
                class Tem:
                    def fhAachenFiles():
                        class Te:
                            def files():
                                p = Path.joinPath(Temp._path(), r"operations\Classwork")
                                files = Path.filesWithExtension("pdf", p, walk=False)
                                return files
                            def db(): 
                                return DB_SWT._dbdb('fh db exercises', Te.files(), FilePathsSearchEngine)
                        return Te
                    def tumFiles():
                        class Te:
                            def files():
                                p = Path.joinPath(Temp._path(), r"operations\Training Set\tum exercises")
                                files = Path.filesWithExtension("pdf", p, walk=False)
                                return files
                            def db():
                                return DB_SWT._dbdb('tum db exercises', Te.files(), FilePathsSearchEngine)
                        return Te
                    def contentSearch():
                        files = Tem.fhAachenFiles().files() +  Tem.tumFiles().files()
                        name ="db exercises"
                        return DB_SWT._dbdb(name, files, Database.pdfDB)              
                return Tem

            def _path():
                return FrequentPaths.pathAsDic()['database']
        return Temp

    def swt():
        from Path import FrequentPaths, Path
        from Database import Database
        class Temp:
            def docs():
                p = Path.joinPath(Temp._path(), r"data\matse scripts")
                files = Path.filesWithExtension("pdf", p)
                return DB_SWT._dbdb("swt", files, Database.pdfDB)
            
            def _path():
                return FrequentPaths.pathAsDic()['software engineering swt']
            
        return Temp
    
    def _dbdb(name, files, engine):
        if( name in DB_SWT._dbs):
            return DB_SWT._dbs[name]
        DB_SWT._dbs[name] = engine(files)
        return DB_SWT._dbs[name]