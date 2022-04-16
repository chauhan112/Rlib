import os
from LibPath import *
from FileDatabase import File
from Path import Path
from IPython.display import Markdown
from SerializationDB import SerializationDB
from LibsDB import LibsDB

class ModuleDB:
    def colorPrint(filetyp, content):
        return Markdown(f"```{filetyp}\n{content}\n```")

    def createModule(name):
        if(not name.endswith(".py")):
            name = name + ".py"
        File.createFile(Path.joinPath(getPath(), name))

    def addTest(testName, testContent):
        from jupyterDB import jupyterDB
        from ListDB import ListDB
        def createFunction(name, content):
            content = shifLines(content.strip())
            return f"""def {name}:\n{content}"""

        def shifLines(lines):
            return "\n".join(ListDB.listMap(lambda x: "    " + x, lines.split("\n")))
        
        if(not testName.endswith(")")):
            testName += "()"
        filePath = Path.joinPath(getPath(), "TestDB.py")
        func = createFunction(testName, testContent)
        func = shifLines(func)
        File.appendToFile(filePath,"\n"+ func)
    
    def openModule(path,mode = "output_cell", filetype = "python"):
        """
        mode = ["output_cell", "input_cell", "editor"]
        """
        if(os.path.basename(path) == path):
            path = Path.joinPath(getPath(),path)
        if(mode == "output_cell"):
            content = File.getFileContent(path)
            from IPython.display import display
            display(ModuleDB.colorPrint(filetype, content ))
        elif(mode in ["inp", "in", "input_cell", "i"]):
            content = File.getFileContent(path)
            get_ipython().set_next_input(content)
        else:
            File.openFile(path)

    def laptopName():
        import socket
        try:
            if( os.environ['COMPUTERNAME'] == 'ACNBRC'):
                return 'office'
        except:
            return socket.gethostname()
        return 'home'

    def getImportAndCorrespondingFile(files = []):
        class Temp:
            def getAllClasses(files = []):
                if(files == []):
                    files = Path.filesWithExtension("py", getPath())
                p = []
                for k in files:
                    content = File.getFileContent(k)
                    p += ModuleDB.classDefinedInPyFile(content)
                return p 
        
        
        if(files == []):
            files = Path.filesWithExtension("py", getPath())
        imp = {}
        for f in files:
            cals = [i.split("(")[0] for i in Temp.getAllClasses([f])]
            for val in cals:
                imp[val] = f.replace(getPath(), "").strip(os.sep)[:-3].replace(os.sep, ".")
        SerializationDB.pickleOut(imp, LibsDB.picklePath("fromFileImportClass.pkl"))
        return imp

    def importingModules(*modules):
        myModules = SerializationDB.readPickle(LibsDB.picklePath("fromFileImportClass.pkl"))
        k = ""
        for mo in modules:
            k += f"from {myModules[mo]} import {mo}\n"
        return k
    
    def classDefinedInPyFile(pyFileContent):
        from RegexDB import RegexDB
        return RegexDB.regexSearch(RegexDB.lookAheadAndBehind("class ", ": *\n", "[a-zA-Z0-9_\(\), ]+"), pyFileContent)

    def copyMyLibsUsedInFiles(filePaths, to ="."):
        def allIncludedLibraries(files):
            from RegexDB import RegexDB
            all_libs = []
            for f in files:
                content = File.getFileContent(f)
                libs = RegexDB.regexSearch(RegexDB.lookAheadAndBehind("import ", "\n", "[a-zA-Z0-9_\(\)]+"), content)
                libs = [i.strip() for i in libs]
                all_libs += libs
            return list(set(all_libs))
        
        all_my_libs = ModuleDB.getImportAndCorrespondingFile(Path.filesWithExtension("py", getPath()))
        all_libs_used_in_project = ModuleDB.allIncludedLibraries(filePaths)
        myLibsUsed = list(set(all_my_libs).intersection(set(all_libs_used_in_project)))
        files2Copy = [Path.joinPath(getPath(), all_my_libs[val].replace(".",os.sep))+".py" for val in myLibsUsed]
        Path.copyFiles(files2Copy, to)
    
    def modulePath(modulename):
        import inspect
        return inspect.getfile(modulename)

    def run_once(f):
        def wrapper(*args, **kwargs):
            if not wrapper.has_run:
                wrapper.has_run = True
                return f(*args, **kwargs)
        wrapper.has_run = False
        return wrapper
        
    def reloadClass(clas, params):
        import inspect
        moduleName=inspect.getmodule(clas).__name__
        className = clas.__name__
        # params is globals()
        commands = [f'import {moduleName}', 'from importlib import reload', f'reload({moduleName})', 
                    f'{className} = {moduleName}.{className}', 'params.update(locals())']
        exec("\n".join(commands))