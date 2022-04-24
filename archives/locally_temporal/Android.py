from Path import Path
from Database import Database

class Android:
    def _path():
        from Path import FrequentPaths
        path = FrequentPaths.pathAsDic()['sixth semester']
        return Path.joinPath(path, "Android")
    def fileNameSearch(word=None):
        androidPath = Path.joinPath(Android._path(), "ops")
        ktFiles = Path.filesWithExtension("kt", androidPath)
        return Database.dbSearch(Database.pathDB(ktFiles), word)

    def pdfFiles(name =None):
        pdfFiles = Path.filesWithExtension("pdf", Android._path())
        return Database.dbSearch(Database.pdfDB(pdfFiles), name)

    def fileContentSearch(word =None):
        androidPath = Path.joinPath(Android._path(), "ops")
        files = Path.filesWithExtension("kt", androidPath)
        return Database.dbSearch(Database.textFilesDB(files), word)

    def xmlFiles(word =None):
        androidPath = Path.joinPath(Android._path(), "ops")
        files = Path.filesWithExtension("xml", androidPath)
        return Database.dbSearch(Database.textFilesDB(files), word)

    def allXmlFiles(word =None):
        androidPath = Path.joinPath(Android._path())
        files = Path.filesWithExtension("xml", androidPath)
        return Database.dbSearch(Database.textFilesDB(files), word)
