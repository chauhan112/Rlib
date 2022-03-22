import lizard
from lib.Libs import Libs
from lib.DataModel import LocModel
from IPython.display import display, Markdown
import os

class ProjectAnalysis:
    def __init__(self, path, name="redesigned"):
        self.name = name
        self.path = path
        self.dataModel = LocModel()
        self.files = Libs.path().filesWithExtensions(['cpp','h','py'],self.path)
        self._analysed = list(lizard.analyze_files(self.files))
        self._tools().updateMethodInfo()
        self._tools().updateClassInfo()
        self._colorCode = {}
        self._tools().initializeColorCode()
                
    def complexityInfo(self, skipping = [], aboveCc = 0):
        table = []
        for cls in self.dataModel.classModel.content:
            if(cls in skipping ):
                continue
            classContent = self.dataModel.classModel.content[cls]['methods']
            for meth in classContent:
                if(classContent[meth]['ccn']> aboveCc):
                    table.append([cls, meth, classContent[meth]['ccn'], classContent[meth]['loc']])
        return table
    
    def summarize(self):
        filesNr = len(self.files)
        linesNr = self.dataModel.totalLoc()
        size = Libs.fileOps().getSize(self.files)
        libsNr = len(self.dataModel.classModel.read().allClasses())
        val = f'''
                #  <font face = "comic sans ms" color = "red">{self.name}</font>
                ---
                
                ### <font face = "comic sans ms" color = "orange">Total lines of code ::</font> {linesNr}
                ### <font face = "comic sans ms" color = "orange">Total project size ::</font> {size}
                ### <font face = "comic sans ms" color = "orange">No of files :</font> {filesNr}
                ### <font face = "comic sans ms" color = "orange">No of classes :</font> {libsNr}
            '''
        val = val.strip().split("\n")
        val = [line.strip() for line in val]
        return Markdown("\n".join(val))

    def _tools(self):
        class Temp:
            def updateMethodInfo():
                for f in self._analysed:
                    fname = f.filename
                    fileContent = Libs.fileOps().getFileContent(f.filename).splitlines()
                    for func in f.function_list:
                        complexity = func.cyclomatic_complexity
                        mLoc = func.nloc
                        name = func.name
                        a, b = func.start_line, func.end_line
                        clsName = ""
                        if( "::" in name): # for cpp files
                            clsName = name.split("::")[0]
                        ln = func.long_name
                        self.dataModel.methodModel.add(name, longName=ln,className=clsName, loc=mLoc, 
                                    complxity=complexity, misc= {'file': fname, 'content': "\n".join(fileContent[a:b])})

            def updateClassInfo():
                classes = {}
                for val in self.dataModel.methodModel.content:
                    cls = val[2]
                    methodName = val[1].replace(cls+"::", "")
                    if(cls not in classes):
                        classes[cls] = {}
                        classes[cls]['methods'] = {}
                    classes[cls]['methods'][methodName] = {}
                    classes[cls]['methods'][methodName]['loc'] = val[3]
                    classes[cls]['methods'][methodName]['ccn'] = val[4]
                    classes[cls]['methods'][methodName]['content'] = val[5]['content']
                    classes[cls]['file'] = val[5]['file']
                    classes[cls]['parent'] = ""
                self.dataModel.classModel.content = classes
            
            def initializeColorCode():
                i = 0
#                 colorsName = ['orange', 'limegreen', 'skyblue', 'red', 'yellow', 'brown', 'purple', 
#                               "grey", 'navi']
                c ={'Model': 'orange', 'View':'limegreen', 'Controller':'skyblue', '': 'red'}
                def colorMap(path):
                    for k in c:
                        if('module'+os.sep+k in path):
                            return k
                    return ''
                
                clsC = self.dataModel.classModel.content
                for cls in clsC:
                    dirName = os.path.dirname(clsC[cls]['file'])
                    self._colorCode[cls] = c[colorMap(dirName)]
        return Temp
    
    def classDependency(self):
        # see CodeDB analyseComplexityAndLOC for data model
        dependency = {}
        allClasses = set(self.dataModel.classModel.read().allClasses())
        for cls in self.dataModel.classModel.content:
            allClasses.remove(cls)
            for me in self.dataModel.classModel.read().allMethods(cls, False):
                if cls not in dependency:
                    dependency[cls] = []
                dependency[cls] += list(allClasses.intersection(
                    Libs.stringOps().tokenize(self.dataModel.classModel.content[cls]['methods'][me]['content'])))
            allClasses.add(cls)
        dependentClasses = {}
        for cls in dependency:
            if(len(dependency[cls]) !=0):
                dependentClasses[cls] = set(dependency[cls])
        return dependentClasses
    
    def total(self):
        class Temp:
            def numberOfComplexity():
                return sum([self.dataModel.classModel.read().noOfMethods(cls) * self.dataModel.classModel.read().avgComplexity(
                        cls) for cls in self.dataModel.classModel.read().allClasses()])
            def numberOfLoc():
                return self.dataModel.totalLoc()
            
            def numberOfMethods():
                return sum([self.dataModel.classModel.read().noOfMethods(cls) for cls in self.dataModel.classModel.read().allClasses()])
        return Temp
    
    def display(self):
        class Temp:
            def complexityTable(aboveCC= 0):
                tbale = self.complexityInfo(aboveCc=aboveCC)
                Temp.displayTable(tbale, ['class', 'method', "cyclomatic complexity", "LOC"], True, 3)
                
            def LOCPlot(aboveLoc = 0):
                nlocDic = {c:self.dataModel.classModel.read().loc(c) 
                           for c in self.dataModel.classModel.read().allClasses()}
                nlocDic = {c: nlocDic[c] for c in nlocDic if nlocDic[c] > aboveLoc}
                return Libs.barPlotDic(nlocDic, changeFigSize=True, rotate=90, sortDic=True, barLabel=True,
                  xLabel="Classes", yLabel="LOC", 
                )
            
            def dependencyGraphColored(skipClasses = [], copyIt = True):
                # moduleinfo = {'ClassName': 'Model', 'ClassName2': 'View'..}
                color = lambda x: f'{{bg:{x}}}'
                dependentClasses = self.classDependency()
                skipClasses = set(skipClasses)
                txt = ""
                for cls in dependentClasses:
                    c1 = color(self._colorCode[cls])
                    for de in dependentClasses[cls]:
                        if(len(set([cls, de]).intersection(skipClasses)) != 0):
                            continue
                        c2 = color(self._colorCode[cls])
                        txt += f"[{cls}{c1}] ->[{de}{c2}]\n"
                return Temp._deG(txt, copyIt)
            
            def _deG(txt, copyIt):
                if(copyIt):
                    Libs.clip().copy(txt)
                    print("Content copied. Paste on the webpage https://yuml.me/diagram/scruffy/class/draw")
                    return 
                return txt
            
            def dependencyGraph(skipClasses = [], copyIt =True):
                txt = ""
                dependentClasses = self.classDependency()
                for cls in dependentClasses:
                    for de in dependentClasses[cls]:
                        if(len(set([cls, de]).intersection(skipClasses)) != 0):
                            continue
                        txt += f"[{cls}] ->[{de}]\n"
                return Temp._deG(txt, copyIt)
                
            def displayTable(arr, titles, sortIt = False, sortingIndex = 0):
                if(sortIt):
                    arr = sorted(arr, key=lambda val: val[sortingIndex])
                Libs.displayTableFromArray([titles] + arr)
        return Temp