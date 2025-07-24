from LibPath import resourcePath
import os
from useful.LibsDB import LibsDB
from useful.SerializationDB import SerializationDB
from useful.Database import Database

class QtDB:        
    def _dbSearcher(word, dic):
        from IPython.display import display
        from useful.ModuleDB import ModuleDB
        db = Database.dicDB(dic, lambda x: display(ModuleDB.colorPrint("cpp", x)))
        return Database.dbSearch(db, word)

    def add2Functions(function):
        from useful.DataStructure import DataStructure
        from useful.Path import Path
        functionTableHead = ['name',"content", "parameters", "returns", "keywords", "description"]
        tablePath = Path.joinPath(resourcePath(), "cpp", "functions.csv")
        if(not os.path.exists(tablePath)):
            DataStructure.append2CSV([functionTableHead], tablePath)
        val = [function[i] for i in functionTableHead]
        DataStructure.append2CSV([val], tablePath)

    def createEmptyProject(name):
        from useful.FileDatabase import File
        from useful.Path import Path
        path = Path.joinPath(resourcePath(), "cpp")
        files = ["main.cpp", "mainwindow.cpp", "mainwindow.h", "mainwindow.ui"]
        projectFileContent = File.getFileContent(Path.joinPath(path,"projectName.pro"))
        os.mkdir(name)
        File.createFile(Path.joinPath(name, name+".pro"), projectFileContent)
        Path.copyFiles([Path.joinPath(path, f) for f in files], name)