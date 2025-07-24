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
                from useful.htmlDB import htmlDB
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
    def __init__(self):
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