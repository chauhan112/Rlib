import os
import yaml
from Path import Path
from FileDatabase import File
import copy
from zipfile import ZipFile 
from Path import Path
import shutil

class ZipTools:
    def getMyStudentFilePaths(zipFile):
        files = ZipTools.getZipContent(zipFile)
        namesYaml = os.sep.join([os.path.dirname(zipFile), "..", "names.yaml"])
        student_ids = list(yaml.safe_load(File.getFileContent(namesYaml)).values())
        myRelevantContent = []
        for idVal in student_ids:
            for file in files:
                if(idVal in file.lower()):
                    myRelevantContent.append(file)
                    break
        return myRelevantContent
    
    def unzipFilesFromZipWithPaths(zipFilePath, filesToExtract, to = None):
        with ZipFile(zipFilePath, 'r') as zip:
            files = zip.namelist()
            for f in filesToExtract:
                for file in files:
                    zip.extract(file, to)
    
    def getZipContent(zipfile):
        with ZipFile(zipfile, 'r') as zip:
            files = zip.namelist()
        return files
    
    def zipExtractAll(zipFile, targetPath = None):
        with ZipFile(zipFile, 'r') as zip:
            zip.extractall(path = targetPath)
    
    def extractAllZipsToPath(zipList, targetPath=None):
        for f in zipList:
            ZipTools.zipExtractAll(f, targetPath+ os.sep+ os.path.basename(f)[:-4])

class HomeWorkCorrectionTool:
    def __init__(self, homeworkNr):
        self.homeworkPath = HomeWorkCorrectionTool.getHomeWorkPath(homeworkNr)
        self.student = HomeWorkCorrectionTool.studentDetails()
        HomeWorkCorrectionTool.createFolderStructure(homeworkNr)
        
    def initialize(self, question_format = None):
        question_format = yaml.safe_load(question_format)
        self.homeworkFolders = list(map(os.path.basename, os.listdir(os.sep.join([self.homeworkPath, "to check"]))))
        if(len(self.homeworkFolders) != 8):
            print("[-] unzip the folders first")
        self.remarks = self.getRemark(question_format)
        self.question_format = question_format

    def getRemark(self, question_format):
        file = os.sep.join([self.homeworkPath, "remarks.yaml"])
        if(not os.path.exists(file)):
            remark = {}
            for f in self.homeworkFolders:
                remark[f] = copy.deepcopy(question_format)
            File.createFile(file, yaml.dump(remark))
            return remark
        return yaml.safe_load(File.getFileContent(file))          
    
    def getHomePath():
        path = ['cloud','timeline', 'fourth semester', 'Algorithm']
        p2 = ['C:', 'Users', '49162', 'Desktop']
        
        if(os.environ['COMPUTERNAME'] == 'RAJA'):
            return os.sep.join(p2 + path)
        return os.sep.join(['D:'] +path)
    
    def getHomeWorkPath(nr):
        homeworkPath = os.sep.join([HomeWorkCorrectionTool.getHomePath(),"h"+ str(nr)])
        if( nr < 10):
            homeworkPath = os.sep.join([HomeWorkCorrectionTool.getHomePath(), "h0"+str(nr)])
        return homeworkPath
    
    def studentDetails():
        names = yaml.safe_load(File.getFileContent(os.sep.join([HomeWorkCorrectionTool.getHomePath(), "names.yaml"])))
        return names
    
    def correctParticularStudent(self, name):
        self.ask(self.remarks[name])
    
    def startCorrecting(self):
        if(self.remarks is None):
            self.initialize()
        eclipseTestingArea = r"C:\Users\49162\Desktop\Code\jaba\Homework\src"
        tocheck = self.homeworkPath + os.sep + "to check"
        for folder in self.homeworkFolders:
            javaFiles = Path.filesWithExtension("java",os.sep.join([tocheck, folder]), walk=False)
            files = [os.path.basename(x) for x in javaFiles]
            if(self.checkCorrected(self.remarks)):
                print("X :" + folder)
                continue
            print(folder)
            print("Do you want to copy all files to eclipse src?   :", end=" ")

            ques = input()
            if( "y" in ques.lower()):
                filesOfTestingSite = Path.getFiles(eclipseTestingArea)
                File.deleteFiles(filesOfTestingSite)
                Path.copyFiles(files, eclipseTestingArea,os.sep.join([tocheck, folder]))
            elif( "b" in ques.lower()):
                break
            elif ("n" in ques.lower()):
                continue
            elif("o" in ques.lower()):
                filetype = input("file type :")
                for f in Path.filesWithExtension(filetype,os.sep.join([tocheck, folder])):
                    File.openFile(f)
            self.ask(self.remarks[folder])
    
    def writeComment(self, name, comment= ""):
        if(comment == ""):
            comment = input("Give him comment: ")
        if(name not in self.homeworkFolders):
            raise IOError("Wrong Filename")
        try:
            self.remarks[name]["comment"].append(comment)
        except:
            self.remarks[name]["comment"] = comment

    def correctQuestionWise(self):
        print("Options \n"
                  "j: copy java files to ecplise   :\n"
                  "b: to break loop \n"
                  "o: open certain filestype\n"
                  "n: skip correction\n\n")
        eclipseTestingArea = r"C:\Users\49162\Desktop\Code\jaba\Homework\src"
        tocheck = self.homeworkPath + os.sep + "to check"
        allLoopBreak = False
        filetype = None
        for question in self.question_format:
            print("correcting question "+ question)
            
            for folder in self.homeworkFolders:
                if(self.remarks[folder][question] is not None):
                    print("X :" + folder)
                    continue
                print("  *" + folder)
                print("Select your options:",end=" ")

                ques = input()
                if( "j" in ques.lower()):
                    javaFiles = Path.filesWithExtension("java",os.sep.join([tocheck, folder]), walk=False)
                    files = [os.path.basename(x) for x in javaFiles]
                    filesOfTestingSite = Path.getFiles(eclipseTestingArea)
                    File.deleteFiles(filesOfTestingSite)
                    Path.copyFiles(files, eclipseTestingArea,os.sep.join([tocheck, folder]))
                elif( "b" in ques.lower()):
                    allLoopBreak = True
                    break
                elif("n" in ques.lower()):
                    continue
                elif("o" in ques.lower()):
                    if(filetype is None):
                        filetype = input("file type :")
                    for f in Path.filesWithExtension(filetype,os.sep.join([tocheck, folder])):
                        File.openFile(f)
                self.remarks[folder][question] = self.trueValue(question)
            if(allLoopBreak):
                break
 
    def ask(self,dic):
        for key in dic:
            if(type(dic[key]) == dict):
                print(key + ":")
                dic[key] = self.ask(dic[key])
            else:
                if(dic[key] is None):
                    dic[key] = self.trueValue(key)
                        
        return dic

    def trueValue(self,key):
        print(key + ":")
        print("Give the truth value of this question: ")
        k = input()
        if("t" in k.lower()):
            return True
        elif("s" in k.lower()):
            return None
        elif("h" in k.lower()):
            return input("Give Point For Half Correct: ")
        return False
    
    def createFolderStructure(nr):
        homework_path = HomeWorkCorrectionTool.getHomeWorkPath(nr)
        if(not os.path.exists(homework_path)):
            os.mkdir(homework_path)
        subFolders = ['standard solution', 'to check']
        for folder in subFolders:
            path = os.sep.join([homework_path, folder])
            if(not os.path.exists(path)):
                os.mkdir(path)

    def checkCorrected(self,dic):
        truth = True
        for key in dic:
            if(type(dic[key]) == dict):
                truth = truth and self.checkCorrected(dic[key])
            if(dic[key] is None):
                return False
        return True and truth
        
    def writeRemark(self):
        f = self.homeworkPath + os.sep + "remarks.yaml"
        File.deleteFiles([f])
        File.createFile(f, yaml.dump(self.remarks))

    def openPath(self,name):
        pathsList = {
            'homework': r"C:\Users\49162\Desktop\Code\jaba\Homework\src",
            'solution': r"C:\Users\49162\Desktop\Code\jaba",
            'desktop' : r"C:\Users\49162\Desktop"
        }
        for key in pathsList:
            if(name.lower() in key):
                Path.openExplorerAt(pathsList[key])
                break

    def summarize(self):
        def getVal(dic):
            for key in dic:
                typ = type(dic[key])
                if( typ == bool):
                    if(dic[key]):
                        print("3", end="")
                    else:
                        print("0", end="")
                elif(typ == str):
                    if(key == "comment"):
                        print("\ncomment: " )
                    print(dic[key], end="")
                    
                else: 
                    getVal(dic[key])

        for name in self.remarks:
            print(name + ":")
            getVal(self.remarks[name])
            print("\n")
    
    def prepQuestionFormat(dic):
        qu = ""
        for qNr in dic:
            nr = dic
            qu += "A"+ str(qNr) + ":\n"
            for i in range(dic[qNr]):
                qu += "    " + chr(ord('a') + i) + ":\n"
        return qu

class extractHomework:
    def __init__(self, homeworkNr):
        self.path = HomeWorkCorrectionTool.getHomeWorkPath(homeworkNr)
        self.mainZipFile = self.getMainZipFile()
        self.extractFromZipFileToToCheck()
        self.moveNdeleteFiles()
        self.extractAllZipFiles()
        self.moveAllFilesInTheFolder2SameLevel()
        
    def extractFromZipFileToToCheck(self):
        myStudentFiles = ZipTools.getMyStudentFilePaths(self.mainZipFile)
        print("No of files found in Main Zip :" + str(len(myStudentFiles)))
        if(len(myStudentFiles) != 8):
            self.informMissingStudent(myStudentFiles)
            print("Do you want to continue? ")
            conti = input()
            if("y" not in conti.lower()):
                raise IOError()
        ZipTools.unzipFilesFromZipWithPaths(self.mainZipFile, myStudentFiles, self.path + os.sep + "to check")
    
    def extractAllZipFiles(self):
        zips = Path.filesWithExtension("zip", self.path + os.sep + "to check")
        print("No of zips found in to check after move and deletion:" + str(len(zips)))
        ZipTools.extractAllZipsToPath(zips, self.path + os.sep + "to check")
        Path.delete(zips)
    
    def moveNdeleteFiles(self):
        def condition(path):
            path = path.split(os.sep)[-1]
            infos = HomeWorkCorrectionTool.studentDetails()
            for student in infos:
                if(infos[student].lower() in path.lower()):
                    return True
            return False
        
        paths = list(filter(condition, Path.getAllFolders( self.path)))
        print("No of folder found during moving and deleting :" + str(len(paths)))
        newPaths =[]
        for p in paths:
            zips = Path.filesWithExtension("zip", p)
            if(len(zips) == 1):
                newPaths.append(zips[0])
            elif(len(zips) == 0):
                newPaths.append(p)
            else:
                print("more than one zip file found in path " + p)
                newPaths.append(zips[0])
        
        for p in newPaths:
            if(p.endswith(".zip")):
                Path.move().files([p], self.path + os.sep + "to check")
            else:
                shutil.move(p, self.path + os.sep + "to check")
        shutil.rmtree(Path.joinPath(self.path, "to check", "Hausaufgabe " +os.path.basename(self.path)[1:]))
    
    def getMainZipFile(self):
        paths = Path.filesWithExtension("zip", self.path)
        if(len(paths) == 0):
            print("No ZipPath found")
            raise IOError()
        return paths[0]

    def informMissingStudent(self, arr):
        infos = HomeWorkCorrectionTool.studentDetails()
        for key in infos:
            if(infos[key].lower() not in "".join(arr).lower()):
                print(key)
        print()
        print()
        for val in arr:
            print(val)
    
    def moveAllFilesInTheFolder2SameLevel(self):
        path = self.path + os.sep + 'to check'
        folders = os.listdir(path)
        folders = list(map(lambda x: path +os.sep +x, folders))
        for p in folders:
            files = Path.getFiles(p, walk=True)
            for f in files:
                try:
                    Path.move().files([f], p)
                except:
                    pass
            
            foldersInside = Path.getAllFolders(p)
            for f in foldersInside[1:]:
                try:
                    Path.deleteFolder(f)
                except:
                    pass
                    
class LA_2_HW_Correct:
    def _getStudentFilePaths(zipPath):
        from ZiptoolDB import ZiptoolDB
        paths  = ZiptoolDB.getZipContent(zipPath)
        def check(val):
            names = LA_2_HW_Correct.getStudentIdentifier()
            for name in names:
                if(name.lower() in val.lower()):
                    return True
            return False
        return sorted(list(filter(check, paths)))
    
    def getStudentIdentifier():
        from jupyterDB import jupyterDB
        name = "globals"
        k = jupyterDB.pickle().read(name)
        return k['infos']['la hw correction student names']
    
    def extractFiles(hwNr):
        folderName = "hw{:0>2d}".format(hwNr)
        ZiptoolDB.extractWithPaths(la_h1, LA_2_HW_Correct.extractStudents(la_h1))
        
    def showFiles(zipPath):
        from modules.Explorer.model import ZipExplorerWithFilter
        from modules.Explorer.displayer import ZipFileExplorerDisplayer
        class LA_HW(ZipExplorerWithFilter):
            def filterPaths(self):
                return LA_2_HW_Correct._getStudentFilePaths(self.zipPath)
        return ZipFileExplorerDisplayer(zipPath, explorer= LA_HW)