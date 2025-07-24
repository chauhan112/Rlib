import os
from useful.Path import Path
class VersionSystem:
    _timer = None
    def update():
        for f in VersionSystem.Ops().getFiles():
            VersionSystem._oneFile(f)
    
    def _oneFile(file):
        from useful.OpsDB import OpsDB
        class Temp:
            out = ""
            def fixDeletedFile(file):
                if(os.path.exists(file)):
                    return
                print(file + " is deleted")
                VersionSystem.Ops().delete(file)
            
            def setup(file):
                Temp.fixDeletedFile(file)
                os.chdir(os.path.dirname(file))
                out, err = OpsDB.cmd().run("git status", getErr=True)
                if(err != ""):
                    OpsDB.cmd().run("git init")
                Temp.out = out
                
            def addAndCommit(file):
                fileBase = os.path.basename(file)
                if(fileBase in Temp.out):
                    print(f"{fileBase} added and commited")
                    OpsDB.cmd().run("git add "+  os.path.basename(file))
                    OpsDB.cmd().run(f'git commit -m"{fileBase}"')

        file = os.path.abspath(file)
        cwd = os.getcwd()
        try: 
            Temp.setup(file)
            Temp.addAndCommit(file)
        except:
            os.chdir(cwd)        
        os.chdir(cwd)
        
    def rollBack(file):
        pass
    
    def Ops():
        from useful.PickleCRUDDB import PickleCRUD
        class GitPklCRUD(PickleCRUD):
            def __init__(self):
                super().__init__("globals", ['infos','git version system'])
        class Temp:
            git = GitPklCRUD()
            def add(val, overwrite = False):
                Temp.git.add(val, val, overwrite)
            def getFiles():
                vals = list(map(lambda x: Path.convert2CloudPath(x),Temp.git.getContent().values()))
                return vals
            def delete(val):
                Temp.git.delete(val)
        return Temp
    
    def automate():
        from useful.TimeDB import TimeDB
        VersionSystem._timer = TimeDB.setTimer().regularlyUpdateTime(10, VersionSystem.update)
    
    def test():
        from useful.PickleCRUDDB import PickleCRUD
        class TestPklCRUD(PickleCRUD):
            def __init__(self):
                super().__init__("test", [])
        return TestPklCRUD()
    def stopTimer():
        if(VersionSystem._timer):
            VersionSystem._timer.cancel()