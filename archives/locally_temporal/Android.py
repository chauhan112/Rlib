from Path import Path
from Database import Database

class Android:
    def _path():
        from Path import FrequentPaths
        path = FrequentPaths.pathAsDic()['sixth semester']
        return Path.joinPath(path, "Android")
    def fileNameSearch(word):
        androidPath = Path.joinPath(Android._path(), "ops")
        ktFiles = Path.filesWithExtension("kt", androidPath)
        return Database.pathDB(ktFiles).search(word)

    def pdfFiles(name =""):
        pdfFiles = Path.filesWithExtension("pdf", Android._path())
        Database.pdfDB(pdfFiles).search(name)

    def fileContentSearch():
        androidPath = Path.joinPath(Android._path(), "ops")
        files = Path.filesWithExtension("kt", androidPath)
        return Database.textFilesDB(files)

    def xmlFiles():
        androidPath = Path.joinPath(Android._path(), "ops")
        files = Path.filesWithExtension("xml", androidPath)
        return Database.textFilesDB(files)

    def allXmlFiles():
        androidPath = Path.joinPath(Android._path())
        files = Path.filesWithExtension("xml", androidPath)
        return Database.textFilesDB(files)
