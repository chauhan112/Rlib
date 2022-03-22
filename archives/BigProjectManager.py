class BigProjectManager:
    path = None
    def create(name, path = os.getcwd()):
        if(name == ""):
            print("give a correct name")
        pjPath = Path.joinPath(path, name)
        os.makedirs(pjPath)
        os.mkdir(Path.joinPath(pjPath, "input"))
        os.mkdir(Path.joinPath(pjPath, "process"))
        File.createFile(Path.joinPath(pjPath, "input", "IReader.py"), """class IReader:
        def read(self):
            raise IOError("Not implemented yet")""")
        File.createFile(Path.joinPath(pjPath, "process", "IProcess.py"), """class IProcess:
        def solve(self):
            raise IOError("Not implemented yet")""")
        File.createFile(Path.joinPath(pjPath, "main.py"))
        BigProjectManager.path = pjPath
    def explorer():
        from ExplorerDB import ExplorerDB
        return ExplorerDB.osFileExplorer(BigProjectManager.path)