from timeline.t2022.TLCAP import Main,NameFinder, Tools, LocationData
from ComparerDB import ComparerDB
from RegexDB import RegexDB
class ILocCheck:
    def check(self, loc:list):
        pass
    def get_variables(self, content):
        pass
    def display(self, nameFinder: NameFinder):
        pass
class CommonLoc:
    def check(loc: list, nf: NameFinder):
        nf.set_location(LocationData(loc))
        path = nf.get_name()
        if "CitizenTool" in path:
            return False
        return True
class DuplicatePathCheck:
    def __init__(self):
        self._path_exists =set()
    def check(self, loc, nf):
        nf.set_location(LocationData(loc))
        path = nf.get_name()
        shorPaht = RemoveImportedTrail.remove(path)
        if tuple(shorPaht) in self._path_exists:
            return False
        self._path_exists.add(tuple(shorPaht))
        return True
class GlobalVariables:
    def set_value(self, vlaue:dict):
        self._data = vlaue
        variables = Tools.get(self._data, ['result', 'resources', 'components', 1,"variables"])
        globalVars = set()
        for i, key in enumerate(variables):
            globalVars.add(key)
        self.set_globals_vars(global_vars=globalVars)
    def set_globals_vars(self, global_vars: set):
        self._global_vars = global_vars
    def check(self, var):
        return  var in self._global_vars
class RemoveImportedTrail:
    def remove(res):
        newRes = []
        for p in res:
            if p =="importedModules":
                newRes = []
            else:
                newRes.append(p)
        return newRes
class LocIsGlobalBinding(ILocCheck):
    def set_location(self, loc: list):
        self._loc = loc
    def set_content(self, content: str):
        self._content = content
        self._var = self._content.split(".")[0]
    def check(self):
        isGlobal = ['variable', 'global'] == self._loc[-2:]
        isGlobal = isGlobal and self._glb_vars.check(self._var)
        return isGlobal
    def get_variables(self, ):
        return self._var
    def display(self, nf: NameFinder):
        nf.set_location(LocationData(self._loc))
        print(RemoveImportedTrail.remove(nf.get_name()), self._var)
    def set_global_var_checker(self, checker: GlobalVariables):
        self._glb_vars = checker
class LocIsInJavaScript(ILocCheck):
    def set_location(self, loc: list):
        self._loc = loc
    def set_content(self, content: str):
        self._content = content
        self._vars = set(map(lambda x: x.replace("VariableService.global.",""), set(RegexDB.regexSearch("VariableService\.global\.[a-zA-Z0-9]*.*?", content))))
    def check(self):
        if ['input', 'code'] == self._loc[-2:]:
            for v in self._vars:
                if self._glb_vars.check(v):
                    return True
        return False
    def get_variables(self):
        return self._vars
    def display(self, nf: NameFinder):
        nf.set_location(LocationData(self._loc))
        print(RemoveImportedTrail.remove(nf.get_name()))
        print("\n".join(self._vars))
    def set_global_var_checker(self, checker: GlobalVariables):
        self._glb_vars = checker
class Finder:
    def _default_compare(self, con):
        if type(con) == str:
            return ComparerDB.has("\\bglobal\\b", con, reg=True)
        return False
    def find(self, file):
        from timeline.t2022.TLCAP import Main
        val = Main._readJson(file)
        i = 1
        nf = NameFinder()
        dpc = DuplicatePathCheck()
        nf.set_data(val)
        res =Tools.pickle_search(val,self._default_compare,searchInKey=True)
        gbChecker = GlobalVariables()
        gbChecker.set_value(val)
        clss = [LocIsGlobalBinding, LocIsInJavaScript]
        for key, value in res:
            for clsN in clss:
                ins = clsN()
                ins.set_location(key)
                ins.set_content(value)
                ins.set_global_var_checker(gbChecker)
                if ins.check() and CommonLoc.check(key, nf) and dpc.check(key, nf):
                    print(i, key)
                    ins.display(nf)
                    print()
                    i = i+1
                    break

class Main:
    def find(file):
        fin = Finder()
        fin.find(file)
