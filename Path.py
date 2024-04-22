import os
import shutil
import webbrowser
from ListDB import ListDB
from ComparerDB import ComparerDB
from LibPath import *
from SerializationDB import SerializationDB
from SearchSystem import GSearchEngine, JupyterNotebookSE, DicSearch

class PathServer(GSearchEngine):
    def __init__(self,pathDic, copy=False):
        self.paths = pathDic
        super().__init__(DicSearch(self.paths), JupyterNotebookSE(callbackFunc=self.display))
        self.copy = copy
    
    def display(self, key):
        from ClipboardDB import ClipboardDB
        path = self.paths[key]
        if(type(path) == type(lambda x: x)):
            path = path()
        if(self.copy):
            ClipboardDB.copy2clipboard(x)
        else:
            Path.openExplorerAt(path)

class Path:
    def searchFile(directory, name, case = True, walk = False):
        file_contents = Path.getFiles(directory, walk)
        for file in file_contents:
            if(ComparerDB.inCompare(name , file, case)):
                print(file)
                break
    def home():
        from pathlib import Path as p
        return str(p.home())
        
    def openFile(file):
        if(os.path.exists(file)):
            webbrowser.open(file)
            return
        print(file + " does not exists")

    def openExplorerAt(path = None):
        from SystemInfo import SystemInfo
        if(path is None):
            path = os.getcwd()
        command = 'explorer "{}"'
        if SystemInfo.getName() == "linux-ier9":
            command = 'dolphin "{}"'
        elif(SystemInfo.isLinux()):
            command = "xdg-open '{}'"
        os.system(command.format(path))

    def _getAllFilesInFolder(directory):
        file_paths = []
        for root, directories, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)
        return file_paths
    
    def filesWithExtension( extension,directory = None, walk = True):
        return Path._filesWithExtensions([extension], directory, walk)        

    def _filesWithExtensions( extensions ,directory = None, walk = True):
        results = []
        if(directory is None):
            directory = os.getcwd()

        files = Path.getFiles(directory, walk)
        for file in files:
            if(ComparerDB.hasExtension(file, extensions)):
                results.append(file)
        return results
        
    def getFiles(directory, walk = False):
        if(walk):
            return Path._getAllFilesInFolder(directory)
        cand = os.listdir(directory)
        files = []
        for file in cand:
            if(os.path.isfile(directory + os.sep + file)):
                files.append(directory + os.sep + file)
        return files
    
    def move():
        class Temp:
            def files(self, fileList, destination = ""):
                if(type(fileList) == str):
                    fileList = [fileList]
                if(destination == ""):
                    destination = os.getcwd()
                if not os.path.exists(destination):
                    os.makedirs(destination)
                for f in fileList:
                    shutil.move(f,destination)
            def folder(self, srcFolder, desFolder):
                shutil.move(srcFolder, desFolder)
            def downloadedFile(self, fileNameHint, targetFolderNameHint, downloadedFolder = ""):
                if(downloadedFolder == ""):
                    downLoadedFolder = desktopPath()
                f = AIAlgoDB.incrementalSearch(os.listdir(downLoadedFolder)).search(fileNameHint)[0]
                k = FrequentPaths.pathAsDic()
                targetFolderKey = AIAlgoDB.incrementalSearch(k.keys()).search(targetFolderNameHint)[0]
                targetFolder = k[targetFolderKey]
                self.files([Path.joinPath(downLoadedFolder, f)], targetFolder)
        return Temp()
    
    def copyFiles(files, target_path = "", source_path=None):
        if(target_path == ""):
            target_path == os.getcwd();
        if(source_path is not None):
            for x in files:
                shutil.copy2(source_path + os.sep + x, target_path + os.sep + x)
        else:
            for x in files:
                shutil.copy2( x, target_path + os.sep + os.path.basename(x))

    def delete(files):
        for di in files:
            os.remove(di)

    def joinPath(*arr):
        return Path.changeSeparator(os.sep.join(arr))
    
    def getAllFolders(startingPath= ".", walk = True):
        if(not walk):
            return Path.getDir(startingPath)
        return [x[0] for x in os.walk(startingPath)]
        
    def getDir(path="."):
        content = os.listdir(path)
        folders = []
        for v in content:
            if(os.path.isdir(os.sep.join([path, v]))):
                folders.append(os.sep.join([path, v]))
        return folders
    
    def moveFolder( sourceDir, destDir):
        shutil.move(sourceDir, destDir)

    def deleteFolder(directory):
        shutil.rmtree(directory)

    def createFolderStructure(arr, path = None):
        if(path is None):
            path = os.getcwd()
        if(type(arr) == str):
            os.mkdir(os.sep.join([path, arr]))
        elif (type(arr) == dict):
            for key in arr:
                os.mkdir(os.sep.join([path, key]))
                Path.createFolderStructure(arr[key], os.sep.join([path, key]))
        elif(type(arr) == list):
            for f in arr:
                Path.createFolderStructure(f, path)

    def getSize(files):
        si = 0
        for f in files:
            si += os.stat(f).st_size
        return str(si / 1024) + " kb"
        
    def copyFolderAndItsContent(folder2copy, destinationFolder):
        from distutils.dir_util import copy_tree
        if(type(folder2copy) == str):
            copy_tree(folder2copy, destinationFolder)
        elif(type(folder2copy) == list):
            for f in folder2copy:
                copy_tree(f, destinationFolder)

    def paths(word = '', copy = False):
        from PickleCRUDDB import PickleCRUD
        class PathOps(PickleCRUD):
            def __init__(self):
                name = 'paths'
                super().__init__(name, ['directory'])
            
            def searchInDB(self, word= "",copy = False):
                db = PathServer(FrequentPaths.pathAsDic(), copy)
                db.search(word)
                return db
        return PathOps()
    
    def changeSeparator(path):
        from WordDB import WordDB
        return WordDB.replaceWithRegex(r"\\+", "<sjdfsdj>", WordDB.replaceWithRegex("/+","<sjdfsdj>",  
            path)).replace("<sjdfsdj>", os.sep)
    
    def arrange():
        class Temp:
            def combineAll(path, name = None):
                files = Path.getFiles(path, True)
                Temp._common(path, files, name)
                
            def nowTime(path, name = None):
                files = Path.getFiles(path)
                Temp._common(path, files, name)
                
            def _common(path, files, name):
                from TimeDB import TimeDB
                if(name is None):
                    name = TimeDB.getTimeStamp().replace(",", "")
                    
                foldersTemplate = Temp._createNgetFolder(path, name)
                Temp._moveFiles(files, path, name)
                Temp._deleteEmptyFoldersOfPath(Path.joinPath(path, name))
            def _moveFiles(files, path, name):
                p, folders = Temp._createNgetFolder(path, name)
                for f in files:
                    _, ext = os.path.splitext(f.lower())
                    try:
                        Path.move().files([f], folders[p[ext.replace(".", "")]])
                    except:
                        print(ext)
                        try:
                            Path.move().files([f], folders['others'])
                        except:
                            print(f + " did not move")
                

            def _createNgetFolder(path, name =None):
                p = {'mp3': 'audios', 'wav': 'audios', '3gp': 'audios', 'm4a': 'audios', 'mp4': 'videos', 'webm': 'videos', 
                    'mkv': 'videos', 'flv': 'videos', 'avi': 'videos', 'txt': 'docs', 'pdf': 'docs', 'docs': 'docs', 'csv': 'docs', 
                    'md': 'docs',"zip":"others", "jpg": "photos", "png":"photos", "gif":"photos", "svg":"photos", "ipynb": "scripts",
                    'py':"scripts", "java": "scripts", "jpeg": "photos"}
                folders = [name, f"{name}\\audios",f"{name}\\videos", f"{name}\\docs", f"{name}\\others", f"{name}\\photos",
                        f"{name}\\scripts"]
                folders = [Path.changeSeparator(path + os.sep + f) for f in folders]

                for folder in folders:
                    if(not os.path.exists(folder)):
                        os.mkdir(folder)

                folders = {os.path.basename(f): f for f in folders[1:]}
                return p, folders

            def _deleteEmptyFoldersOfPath(path):
                folders = os.listdir(path)
                for f in folders:
                    newPath = Path.joinPath(path, f)
                    files = os.listdir(newPath)
                    if(len(files) == 0):
                        os.system(f"rmdir '{newPath}'")
                        
        return Temp
    def _programPaths():
        from jupyterDB import jupyterDB
        from ModuleDB import ModuleDB
        return FrequentPaths.readPicklePath()['programs'][ModuleDB.laptopName()]
    
    

class FrequentPaths:
    def addPath(key, value, cloudPath = True):
        paths = FrequentPaths.readPicklePath()
        paths.append((key, cloudPath, value))
        SerializationDB.pickleOut(paths, file)
        
    def readPicklePath():
        from LibPath import resourcePath
        val = 'paths.pkl'
        file = Path.joinPath(resourcePath(), 'pickle', val)
        paths = SerializationDB.readPickle(file)
        return paths
        
    def pathAsDic():
        paths = {}
        from LibsDB import LibsDB
        from WordDB import WordDB

        content = FrequentPaths.getContent()
        for key in content:
            val = content[key]
            if(type(val) == str):
                paths[key] = Path.joinPath(WordDB.replaceWithRegex("^.*?cloud", LibsDB.cloudPath().replace("\\",r"\\"), val))
            elif(type(val) == type(lambda x: x)):
                paths[key] = val()
            else:
                paths[key] = val
        paths.update(FrequentPaths._otherPaths())
        return paths
    
    def getContent():
        paths = FrequentPaths.readPicklePath()['directory']
        return paths
    
    def desktopPath():
        from pathlib import Path as p
        return Path.joinPath(str(p.home()), "Desktop")

    def _otherPaths():
        from TreeDB import ForestDB
        paths = {}
        paths['here'] = os.getcwd()
        paths['forest'] = ForestDB.getForestPath()
        paths['telegram project'] = os.path.abspath(Path.joinPath(getPath(), '../../projects/telapp/old'))
        return paths