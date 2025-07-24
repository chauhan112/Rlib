import lizard
import os
from FileDatabase import File
from WordDB import WordDB
from SerializationDB import SerializationDB

class CodeDB:
    def parseFile(filePath):
        if(not os.path.exists(filePath)):
            raise IOError("FilePath does not exist.")
        return ParsedValue(filePath)

    def parseProject(listOfFilepaths):
        return Project(listOfFilepaths)

    def analyseComplexityAndLOC(files):
        dataModel = LocModel()
        analysed = list(lizard.analyze_files(files))
        class Temp:
            def updateMethodInfo(dataModel):
                for f in analysed:
                    fname = f.filename
                    fileContent = File.getFileContent(f.filename).splitlines()
                    for func in f.function_list:
                        complexity = func.cyclomatic_complexity
                        mLoc = func.nloc
                        name = func.name
                        a, b = func.start_line, func.end_line
                        clsName = ""
                        if( "::" in name): # for cpp files
                            clsName = name.split("::")[0]
                        ln = func.long_name
                        dataModel.methodModel.add(name, longName=ln,className=clsName, loc=mLoc,
                                    complxity=complexity, misc= {'file': fname, 'content': "\n".join(fileContent[a:b])})
            def updateClassInfo(dataModel):
                classes = {}
                for val in dataModel.methodModel.content:
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
                dataModel.classModel.content = classes

        Temp.updateMethodInfo(dataModel)
        Temp.updateClassInfo(dataModel)
        return dataModel

    def unCommentPython(regex, content):
        class Tmep:
            def remove_comments(content):
                from PyCodeUtils import PyCodeUtils
                return PyCodeUtils.pyCommentRemover(content)

            def extract_content(regex, content):
                founds = WordDB.searchWordWithRegex(regex, content)
                a = 0
                newContent = ""
                for i,j in founds:
                    newContent += content[a:i]
                    a = j
                return newContent
        return Tmep
        
class Project:
    def __init__(self, filesList):
        self.files = filesList
        self.scripts = [os.path.basename(f) for f in filesList]
        self.functionsList = self.listAllFunctions()
        self.History = {}

    def listAllFunctions(self):
        functions = []
        for file in self.files:
            analyze = lizard.analyze_file(file)
            functions += [f.long_name for f in analyze.function_list]
        return functions

    def searchInContent(self, keyword):
        if(keyword in self.History):
            return self.History[keyword]

        for file in self.files:
            content = File.getFileContent(file)

    def callsTracebackAnalyser(self, functionName):
        for f in self.files:
            pa = ParsedValue(f)
            print(f)
            print(pa.fuctionNamesWhereWordIs(functionName))
            print()

class ParsedValue:
    def __init__(self, path):
        self.fileContent = File.getFileContent(path).split("\n")
        self.i = lizard.analyze_file(path)

    def functions(self):
        return [f.long_name for f in self.i.function_list]

    def getFunctionContent(self, funcname):
        for f in self.i.function_list:
            if(f.long_name.strip() == funcname or f.name.strip() == funcname):
                functionData = self.fileContent[f.start_line:f.end_line +1]
                return "\n".join(functionData)
        return ''

    def getFunctionRange(self, funcname):
        for f in self.i.function_list:
            if(f.long_name.strip() == funcname or f.name.strip() == funcname):
                return f.start_line, f.end_line
        raise IOError( 'No such name' )

    def fuctionNamesWhereWordIs(self,word):
        funt = []
        for fun in self.functions():
            if(WordDB.regexMatchFound(word, self.getFunctionContent(fun))):
                funt.append(fun)
        return funt

class ClassModel:
    def __init__(self, filePath = None):
        # struc = {'name': {"file": "", methods: {name: loc, name:loc}, parent:""} }
        self.content = {}
        if(filePath is not None):
            self.content =SerializationDB.readPickle(filePath)

    def add(self, name, file ="", parent ="", methods= {}, override = False):
        if(name in self.content):
            if(not override):
                print("name already exits")
                return
        self.content[name] = {'file':file, 'methods': methods, 'parent': parent}

    def read(self):
        class Temp:
            def loc(name):
                return sum(Temp.locDist(name))
            def locDist(name):
                dic = self.content[name]['methods']
                return [dic[x]['loc'] for x in dic]
            def parent(name):
                return self.content[name]['parent']
            def file(name):
                return self.content[name]['file']
            def noOfMethods(name):
                return len(self.content[name]['methods'])
            def avgComplexity(name):
                dic = self.content[name]['methods']
                return sum([dic[x]['ccn'] for x in dic])/ Temp.noOfMethods(name)
            def allMethods(name, displayIt = True):
                from htmlDB import htmlDB
                methods =list(self.content[name]['methods'])
                if(not displayIt):
                    return methods
                htmlDB.displayTableFromArray([("","")]+ list(zip(range(len(methods)), methods)))
            def allClasses():
                return list(self.content.keys())
            def methodInfo(methodIndex, name):
                return self.content[name]['methods'][Temp.allMethods(name, False)[methodIndex]]

        return Temp

    def update(self, name, newName):
        if(name not in self.content):
            print("class does not exist")
            return
        val =self.content[name]
        if(newName not in self.content):
            self.delete(name)
            self.content[newName]=val

    def delete(self,name):
        if(name in self.content):
            del self.content[name]

class MethodModel:
    def __init__(self, filePath =None):
        # strct =  (methodName:str,longname:str, className:str, loc:int, ccn: int, misc: {})
        self.content = []
        if(filePath is not None):
            self.content =SerializationDB.readPickle(filePath)

    def read(self, name):
        class Temp:
            def className():
                return self.search(name, 2)
            def loc():
                return self.search(name, 3)
            def name():
                return self.search(name, 1)
            def complexity():
                return self.search(name, 4)
        return Temp
    def search(self, txt, idx= 0, compare= lambda x,y: x == y):
        filterFunc = lambda val: compare(txt, val[idx])
        return list(filter(filterFunc, self.content))

    def update(self,name, newName):
        pass

    def delete(self,name):
        a = -1
        for i, (mName,lName, cName, loc, com) in enumerate(self.content):
            if(name == mName):
                a = i
                break
        if(a != -1):
            del self.content[i]

    def add(self,name,longName ="", loc=0, complxity = 0, className = None, misc= {}):
        val = (name, longName, className, loc, complxity, misc)
        if( val not in self.content):
            self.content.append(val)
        else:
            print("value already exits")

class LocModel:
    def __init__(self,):
        self.methodModel = MethodModel()
        self.classModel = ClassModel()

    def totalLoc(self):
        n = 0
        for cls in self.classModel.read().allClasses():
            n += self.classModel.read().loc(cls)
        return n

    def archive(self, filePath):
        SerializationDB.pickleOut((self.classModel.content, self.methodModel.content), filePath)

    def load(self,filePath):
        self.classModel.content, self.methodModel.content = SerializationDB.readPickle(filePath)


class IAnalyser:
    def copy_source(self):
        pass
    def uncomment(self):
        pass

class PyAnalyseCode(IAnalyser):
    def __init__(self, path, target_path):
        self.path = path
        self.to_path = target_path
        self._pyfiles = Path.filesWithExtension("py", self.path)
    def copy_source(self):
        for f in self._pyfiles:
            File.createFileInsideNonExistingFolder(
                os.sep.join([self.to_path, "source", f'{f.replace(common_part, "")}']) , File.getFileContent(f))
    def uncomment(self):
        from PyCodeUtils import PyCodeUtils
        for f in self._pyfiles:
            content = PyCodeUtils.pyCommentRemover(File.getFileContent(f))
            File.createFileInsideNonExistingFolder(
                os.sep.join([self.to_path, "uncomment", f'{f.replace(common_part, "")}']), content)
    
    def get_size(self, path = None):
        from FileDatabase import File
        if path is None:
            path = self.to_path
        else:
            path = os.sep.join([self.to_path, path])
        pyfiles = Path.filesWithExtension("py", path)
        tot = sum([File.size(f) for f in pyfiles])
        print(f'{tot/1024} kb')