def dependencyFromHeaderFiles(allClasses, headerFiles):
    allClasses = set(allClasses)
    dep = {}
    for file in headerFiles:
        content = File.getFileContent(file)
        classesContent = headerClassContent(content)
        for cls in classesContent:
            if(cls not in dep):
                dep[cls] = []
            dep[cls] += list(allClasses.intersection(WordDB.tokenize(classesContent[cls])))
    return {key:set(dep[key]) for key in dep}
    
def headerClassContent(content):
    pos = WordDB.searchWordWithRegex("class|struct|enum",content)
    classInitialPoses = [a for a,b in pos] + [len(content)]
    classContentPoss = [(classInitialPoses[i-1], classInitialPoses[i]) for i in range(1, len(classInitialPoses))]
    
    clsGroup = {}
    for a,b in classContentPoss:
        classesFound = Lexer.classes().fromContent(content[a:b])
        if(len(classesFound) == 0):
            continue
        cls = classesFound[0][0]
            
        g = OpsDB.grouperValues(Tracker().mapFunc, content[a:b].splitlines())
        if(1 in g):
            val = "\n".join(g[1])
            clsGroup[cls.strip()] = val
    return clsGroup
    
    
class Tracker:
    def __init__(self):
        self.curlyCounter = 0
        self.groupingTracker = 0
        
    def mapFunc(self, content):
        for c in content:
            if(c == "{"):
                self.curlyCounter += 1
                if(self.curlyCounter == 1):            
                    self.groupingTracker += 1
            if(c == "}"):
                self.curlyCounter -= 1
        return self.groupingTracker
        


def calculateTheImproveMent(new, old, optimalComplexity = 3.5):
    cn = total(new).complexity()
    co = total(old).complexity()
    mn = total(new).methods()
    mo = total(old).methods()
    predCom = mn * optimalComplexity
    tot= co - predCom

    improved = co - cn
    return improved *100/ tot
    
def total(path):
    class Temp:
        def complexity():
            ar = Lexer.parse(path)
            return sum([ar.classModel.read().noOfMethods(cls) * ar.classModel.read().avgComplexity(
                        cls) for cls in ar.classModel.read().allClasses()])
        def methods():
            ar = Lexer.parse(path)
            return sum([ar.classModel.read().noOfMethods(cls) for cls in ar.classModel.read().allClasses()])
    return Temp