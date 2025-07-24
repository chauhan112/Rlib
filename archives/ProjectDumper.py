from enum import Enum
from BinaryDumper import BinaryDumper
import sqlite3
from useful.Path import Path
from useful.Database import DBResources,DB
from useful.CryptsDB import CryptsDB
from useful.RegexDB import RegexDB
from useful.Database import Table

class DType(Enum):
    text = 1
    drawio = 2
    binary = 3

class ProjectDumperCRUD:
    def __init__(self):
        self.dbPath = Path.joinPath(DBResources.location, "General.db")
        self.db = sqlite3.connect(self.dbPath)
        self.currentProject = None

    def project(self):
        class Temp:
            def table():
                return Table(self.db, "projects")
        return Temp

    def keys(self):
        class Temp:
            def keyCol():
                return "name"
            def table():
                return Table(self.db, "keys")
            def doesKeyExist(name, projectID):
                values = Temp.table().read("name, project_id", f"where name='{name}' and project_id={projectID}")
                return len(values) != 0
            def getHashID(key,projectID):
                vals = Temp.table().read("hashID", f"where name='{key}' and project_id={projectID}")
                return vals[0][0]
            def isActive(name, projectID):
                vals = Temp.table().read("active", f"where name='{key}' and project_id={projectID}")
                return int(vals[0][0]) != 0
            def setActive(name, projectID,activate = 1):
                Temp.table().update(f"active={activate}", f"where {Temp.keyCol()}='{name}' and project_id={projectID}")
        return Temp


class ProjectDumper:
    db = ProjectDumperCRUD()
    projectID = None
    name = None
    def showAllProjects():
        return ProjectDumper.db.project().table().read("name")

    def createNewProject(name):
        from useful.TimeDB import TimeDB
        ProjectDumper.db.project().table().addVal([name, TimeDB.getTimeStamp()])
        
    def select(name):
        ProjectDumper.name = name
        ProjectDumper.projectID = ProjectDumper._findProjectId(name)

    def _findProjectId(name):
        return ProjectDumper.db.project().table().read("id", f"where name='{name}'")[0][0]
    
    def icrud():
        class Tools:
            def headerExtraction(txt):
                founds = RegexDB.regexSearch(RegexDB.lookAheadAndBehind("<h1>", "</h1>", ".*"), txt)
                if(len(founds) > 0):
                    return founds[0]
                return ""

            def getContents(content = ""):
                if(content == ""):
                    content = jupyterDB.clip().text()
                sou = TreeDB.decodeContent(content).soup()
                vals = sou.mxGraphModel.root.findAll("mxCell")[2:]
                cont = []
                for val in vals:
                    cont.append(val['value'])
                return cont
            
            def add(key,val, projectID, typ=DType.text.value, overwrite = False):
                if(projectID is None):
                    raise IOError("project id is None")    
                    
                if(ProjectDumper.db.keys().doesKeyExist(key, projectID)):
                    if(overwrite or not ProjectDumper.db.keys().isActive()):
                        uuid = ProjectDumper.db.keys().getHashID(key, projectID)
                        BinaryDumper.add(uuid, val, overwrite)
                        ProjectDumper.db.keys().setActive(key, projectID,1)
                    else:
                        print("id already exists")
                    return

                uuid = CryptsDB.generateUniqueId()
                active = 1
                ProjectDumper.db.keys().table().addVal([key,uuid, projectID, active, typ])
                BinaryDumper.add(uuid, val)
                print(f"value add to project {ProjectDumper.name}")

            def keyCol():
                return ProjectDumper.db.keys().keyCol()

            def deactivate(name, projectID):
                ProjectDumper.db.keys().setActive(name, projectID,0)

            def update(newkeyName, oldkeyName, projectID ):
                ProjectDumper.db.keys().table().update(f"{Tools.keyCol()}='{newkeyName}'", 
                                               f"where {Tools.keyCol()}='{oldkeyName}' and project_id={projectID}")
            
            def copy(hashID):
                from useful.jupyterDB import jupyterDB
                jupyterDB.clip().copy(BinaryDumper.read(hashID))
            
            def makeDic(twoDArray):
                return {a:b for a,b in twoDArray}
            
            def search(typ, projectID):
                from useful.SearchSystem import DicSearchEngine
                tw = ProjectDumper.db.keys().table().read("name, hashID", 
                                        f"where active=1 and type={typ} and project_id={projectID}")
                dic = Tools.makeDic(tw)
                engin = DicSearchEngine(dic)
                engin.setCallback(lambda key, hashID: Tools.copy(hashID))
                return engin
            
        class Temp:
            def text():
                from useful.jupyterDB import jupyterDB
                class Tem:
                    def add( title = None, val = "", overwrite = False):
                        if(title is not None):
                            Tools.add(title, val, ProjectDumper.projectID, DType.text.value, overwrite)
                        else:
                            contentList = Tools.getContents(val)
                            for con in contentList:
                                header = Tools.headerExtraction(con)
                                if(header == ""):
                                    raise IOError("give header")
                                Tools.add(title, val, ProjectDumper.projectID, DType.text.value, overwrite)
                        
                    def delete(keyTitle):
                        Tools.deactivate(keyTitle, ProjectDumper.projectID)

                    def update( oldkeyName, newkeyName):
                        Tools.update(newkeyName, oldkeyName, ProjectDumper.projectID)
                    
                    def searchEngine():
                        return Tools.search(DType.text.value, ProjectDumper.projectID)
                    
                return Tem

            def designs():
                class Tem:
                    def add(title, content = None, overwrite = False):
                        if(content is None):
                            content = jupyterDB.clip().text()
                        Tools.add(title, content, ProjectDumper.projectID, DType.drawio.value, overwrite)

                    def delete(keyTitle):
                        Tools.deactivate(keyTitle, ProjectDumper.projectID)

                    def update(oldkeyName,newkeyName):
                        Tools.update(newkeyName, oldkeyName,ProjectDumper.projectID)

                    def searchEngine():
                        return Tools.search(DType.drawio.value,ProjectDumper.projectID)
                return Tem
        return Temp