from zipfile import ZipFile 

class ZiptoolDB:
    def getZipContent(zipfile):
        with ZipFile(zipfile, 'r') as zip:
            files = zip.namelist()
        return files
    def zipExtractAll(zipFile, targetPath = None):
        with ZipFile(zipFile, 'r') as zip:
            zip.extractall(path = targetPath)
    
    def extractWithPaths(zipFilePath, filesPath, to = None):
        with ZipFile(zipFilePath, 'r') as zip:
            for f in filesPath:
                zip.extract(f, to)
    def filterFiles(contentList):
        return list(filter(lambda x: x[-1] != '/', contentList))

    def paths2DicLevelOne(paths):
        from OpsDB import OpsDB
        dics = OpsDB.grouper(lambda x: x.split("/")[0], paths, 
                            lambda x: x.replace(x.split("/")[0], "").strip("/"))
        return dics
        
    def zipFiles(files, outName):
        # use zipExplorer from ExplorerDB to see the content of the file
        import zipfile
        if(not outName.endswith(".zip")):
            outName += ".zip"
        zf = zipfile.ZipFile(outName, "w")
        for f in files:
            zf.write(f)
        zf.close()