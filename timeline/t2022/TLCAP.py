import json
import re
from FileDatabase import File
import csv

class SearchInDictionary:
    def __init__(self,):
        self.set_search_func(self._default_search)
        self.set_search_in_key_also(False)
    def set_search_in_key_also(self, ke):
        self._in_key_only = ke
    def set_dic(self, dic):
        self._data = dic
    def set_search_func(self, func):
        self._func = func
    def _default_search(self, word, container):
        if type(container) == str and type(word) == str:
            return self._has(word, container,self._case, self._reg)
        return word == container
    def search(self, word, case=False, reg= False):
        self._reg = reg
        self._case = case
        return Tools.pickle_search(self._data, lambda x: self._func(word, x),searchInKey=self._in_key_only,)
    def _inCompare(self, leftIn, right, case = False):
        if(not case):
            leftIn = leftIn.lower()
            right = right.lower()
        return leftIn in right

    def _has(self, word, content, case = False, reg = False):
        if(reg):
            return re.search(word,content) != None
        return self._inCompare(word, content, case)

class Tools:
    def regexSearch(regex,content):
        return [content[i:j] for i, j in Tools._searchWordWithRegex(regex,content)]
    def _searchWordWithRegex(regex,content):
        matches = re.finditer(regex, content)
        found = []
        for i,match in enumerate(matches):
            found.append([match.start(),  match.end()])
        return found
    def getFileContent(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    def get(dic, loc):
        val = dic
        for x in loc:
            val = val[x]
        return val

    def twoDarray2CSV(twoDimArray, name):
        if( not name.endswith(".csv") ):
            name = name + ".csv"
        if(not DataStructure.not2dArray(twoDimArray)):
            raise IOError("not consistent 2d array")
        with open(name,"w+") as my_csv:
            csvWriter = csv.writer(my_csv,delimiter=',')
            csvWriter.writerows(twoDimArray)
    def displayTableFromArray(arr, displayIt = True):
        from IPython.display import HTML, display
        arrHtmlTxt = "".join([f"<th>{head}</th>\n  " for head in arr[0]])
        arrHtmlTxt = f"<tr>{arrHtmlTxt}</tr>\n"
        for row in arr[1:]:
            vals = ""
            for val in row:
                vals += f"<td>{val}</td>\n  "
            arrHtmlTxt += f"<tr>{vals}</tr>\n"
        if(displayIt):
            display(HTML(f"<table>{arrHtmlTxt}</table>"))
            return
        return f"<table>{arrHtmlTxt}</table>"
    def pickle_search(data, compareFunc, loc=[], searchInKey=False, founds =None):
        if founds is None:
            founds = []
        if type(data) == dict:
            for key in data:
                if searchInKey and compareFunc(key):
                    founds.append((loc + [key], data[key]))
                Tools.pickle_search(data[key], compareFunc, loc + [key], searchInKey, founds)
        elif type(data) in [list, set]:
            for i, val in enumerate(data):
                Tools.pickle_search(val, compareFunc, loc + [i], searchInKey, founds)
        else:
            if compareFunc(data) and (loc, data) not in founds :
                founds.append((loc, data))
        return founds
class IComponent:
    def isUsed(self, name):
        pass
    def get_all(self):
        pass
    def get_counts(self):
        pass

class GComponent:
    def set_data(self, data):
        self._data = data
    def set_string(self, content):
        self._content = content

class UIComponent(IComponent, GComponent):
    def isUsed(self, name):
        return Tools.regexSearch(f"\\b{name}\\b", self._content)
    def get_all(self):
        loc = ['result','resolvedIncludes']
        resolvedComponentLoc = ['resources', 'components']
        resolved_vals = Tools.get(self._data,loc)
        components = {}
        for comp in resolved_vals:
            name = comp['pk']['name']
            self._add(name, Tools.get(comp,resolvedComponentLoc), components)
        self._add('main', Tools.get(self._data,['result']+resolvedComponentLoc), components)
        return components

    def _add(self, name, vals, allComponents):
        allComponents[name] = []
        for ui_comp in vals:
            if 'icon' in ui_comp:
                allComponents[name].append(ui_comp['name'])

    def get_counts(self):
        cmp ={}
        vals = self.get_all()
        for mod in vals:
            cmp[mod] = {}
            for com in vals[mod]:
                cmp[mod][com] = len(self.isUsed(com)) - 1
        return cmp

class IGVFinderMethod:
    def uses(self, name: str):
        pass
    def set_parent(self):
        pass

class RegexMethod(IGVFinderMethod):
    def uses(self, name):
        res= Tools.regexSearch(f" *\"(global|flow)\": *\"{name}\.*(\w|\.)*\"", self._parent._content)
        if len(res) == 0:
            res = Tools.regexSearch(f"VariableService\.global\.{name}", self._parent._content)
        return res
    def set_parent(self, parent):
        self._parent = parent

class OutputBindingChecker(IGVFinderMethod):
    def uses(self, name: str):
        sid = SearchInDictionary()
        sid.set_dic(self._parent._data)
        sid.set_search_in_key_also(True)
        up_res = sid.search(name)
        up_res_filtered_for_exact = list(filter(lambda x: x[0][-1] == name, up_res))
        return list(filter(lambda x: "output" in x[0], up_res_filtered_for_exact))
    def set_parent(self, parent):
        self._parent = parent

class GlobalVariable(IComponent, GComponent):
    def isUsed(self, name):
        rm = RegexMethod()
        rm.set_parent(self)
        rm_res = rm.uses(name)
        if len(rm_res) != 0:
            return rm_res
        obc = OutputBindingChecker()
        obc.set_parent(self)
        obc_res = obc.uses(name)
        if len(obc_res) != 0:
            return obc_res

        return []

    def get_all(self):
        for val in self._data['result']['resources']['components']:
            if val['name'] == "MyApp":
                break
        key = 'Main'
        res = {key: []}
        for name in val['variables']:
            res[key].append(name)
        return res
    def get_counts(self):
        cmp ={}
        vals = self.get_all()
        for mod in vals:
            cmp[mod] = {}
            for com in vals[mod]:
                cmp[mod][com] = len(self.isUsed(com))
        return cmp

class LocationData:
    def __init__(self, data = None):
        self.set_data(data)
    def set_data(self, data):
        self._content = data
        self._total_numebr_elements = len(data)
        self.reset_index()
    def reset_index(self):
        self._index = 0
        self._is_finished = False
    def get_current_index(self):
        return self._index
    def get_next_n_elements(self, n:int):
        return self._content[self._index: self._index + n]
    def get_nr_of_remaining_elements(self):
        return self._total_numebr_elements - self._index
    def set_index(self, i: int):
        self._index = i
    def get_element(self, i: int):
        return self._content[i]
    def get_current_location(self):
        return self._content[:self._index+1]
    def is_over(self):
        return self._index >= self._total_numebr_elements

class NameFinder:
    def set_data(self, data):
        self._data = data
    def set_location(self, loc: LocationData):
        self._location_data = loc
    def get_name(self):
        self._location_data.reset_index()
        res = []
        while not self._location_data.is_over():
            i = self._location_data.get_current_index()
            val = self._location_data.get_element(i)
            if val == "resolvedIncludes":
                elem = self._location_data.get_element(i+1)
                naem = self._get_data([elem, "pk","name"])
                res.append("importedModules")
                res.append(naem)
                self._location_data.set_index(i+2)
            elif val == "flows":
                elem = self._location_data.get_element(i+1)
                lastElement = self._location_data.get_element(i-1)
                if lastElement == "resources":
                    res.pop()
                    res.append("BusinessLogic")
                aa = self._get_data([elem, 'variant'])
                if aa == "FRONTEND":
                    res.append("clientFlows")
                else:
                    res.append("serverFlows")
                res.append(self._get_data([elem, "name"]))
                self._location_data.set_index(i+2)
            elif val in ["components"]:
                elem = self._location_data.get_element(i+1)
                nmaeOFfCompo = self._get_data([elem, "name"])
                res.pop()
                if nmaeOFfCompo == "MyApp":
                    res.append("CitizenTool")
                    res.append("ui" )
                else:
                    res.append("ProTool")
                    res.append("ui" )
                    res.append(nmaeOFfCompo)

                self._location_data.set_index(i+2)
            elif val == "states":
                last2elements = self._location_data._content[i-2: i]
                if last2elements == ['views', 0]:
                    res.pop()
                    res.pop()
                    res.append("Layout")
                else:
                    res.append(val)
                self._location_data.set_index(i + 1)
            elif val == "exits":
                elem = self._location_data.get_element(i+1)
                try:
                    nmaeOFfCompo = self._get_data([elem,"name"])
                    if nmaeOFfCompo == "Default":
                        self._location_data.set_index(i + 2)
                    else:
                        self._else_case(i, val, res)
                except:
                    self._else_case(i, val, res)
                    
            elif val == "views":
                elem = self._location_data.get_element(i+1)
                elemId = self._get_data([elem, "id"])
                res.append(elemId)
                self._location_data.set_index(i + 2)
            elif val == "projection":
                elem = self._location_data.get_element(i+1)
                if elem == "content":
                    lco = self._location_data.get_element(i+2)
                    nid = self._get_data([elem, lco, "id"])
                    res.append(nid)
                    self._location_data.set_index(i + 3)
                else:
                    self._else_case(i, val, res)
            elif val == "children":
                self._location_data.set_index(i + 1)
            else:
                self._else_case(i, val, res)
        return res
    def _else_case(self, i, val, res):
        try:
            naem = self._get_data(["name"])
            assert type(naem) == str
            res.append(naem)
        except:
            res.append(val)
        self._location_data.set_index(i + 1)
    def _get_data(self, loc):
        actLoc = self._location_data.get_current_location() + loc
        return Tools.get(self._data, actLoc)

class TLCAPApp:
    def __init__(self):
        self._ui = None
        self._gv = None

    def set_data(self, data):
        self._data = data
        self._content = json.dumps(self._data)

    def set_file(self, filename):
        self._file = filename
        self._content = Tools.getFileContent(self._file)
        self.set_data(json.loads(self._content))
    def get_included_modules(self):
        return [ele['includedName'] for ele in self._data['result']['includes']]
    def get_ui(self) -> IComponent:
        if self._ui is not None:
            return self._ui
        ui = UIComponent()
        ui.set_data(self._data)
        ui.set_string(self._content)
        self._ui = ui
        return ui
    def get_variables(self) -> IComponent:
        if self._gv is not None:
            return self._gv

        gv  = GlobalVariable()
        gv.set_data(self._data)
        gv.set_string(self._content)
        self._gv = gv
        return self._gv

    def save_as_csv(self, name, compo: IComponent):
        Tools.twoDarray2CSV(self._array_form(compo), f"all_{name}.csv")
        Tools.twoDarray2CSV(self._array_form(compo,lambda x: x == 0), f"unused_{name}.csv")
    def _array_form(self,elem: IComponent,  condition= lambda count: True):
        arr = [['name', 'package', 'count']]
        used_res = elem.get_counts()
        for mdo in used_res:
            for ele in used_res[mdo]:
                v = used_res[mdo][ele]
                if condition(v):
                    arr.append([ele, mdo, v])
        return arr
    def display(self, mod: IComponent, cond = lambda x: True):
        Tools.displayTableFromArray(self._array_form(mod, cond))

class Main:
    def _readJson(file):
        import json
        return json.loads(Tools.getFileContent(file))
        
    def getAllHardCodedValues(filename, searchFor, reg=False, searchInKey=False):
        # from TLCAP import TLCAPApp, SearchInDictionary, NameFinder, LocationData
        app = TLCAPApp()
        app.set_file(filename)
        sid = SearchInDictionary()
        sid.set_search_in_key_also(searchInKey)
        sid.set_dic(app._data)
        res = sid.search(searchFor, reg=reg)
        # print("total results:", len(res))
        nf = NameFinder()
        founds = set()
        nf.set_data(app._data)
        i = 0
        for (loc, va) in (res):
            nf.set_location(LocationData(loc))
            # print( nf._location_data._content)
            path = Main._remove_dependencies_path(nf.get_name())
            if str(path) not in founds:
                print(i+1 , end=" ")
                print(loc)
                print(path)
                founds.add(str(path))
                print()
                i += 1
        return app
    def _remove_dependencies_path(res):
        newRes = []
        for p in res:
            if p =="importedModules":
                newRes = []
            else:
                newRes.append(p)
        return newRes
    def getRedundantVariables(filename):
        pass
    def getRedundantUI(filename, outfile= None):
        uis = Main.getUIComponents(filename)
        sid = SearchInDictionary()
        sid.set_dic(Main._readJson(filename))
        red = []
        for e in uis:
            founds = sid.search(f"\\b{e}\\b", reg = 1)
            if len(founds) == 4:
                red.append(e)
        return red
    def getGlobalVariables(filepath):
        val = Main._readJson(filepath)
        variables = Tools.get(val, ['result', 'resources', 'components', 1,"variables"])
        globalVars = set()
        for i, key in enumerate(variables):
            globalVars.add(key)
        return globalVars
    def showValuesUsed(filename, searchFor, reg=False):
        # from TLCAP import TLCAPApp, SearchInDictionary, NameFinder, LocationData
        app = TLCAPApp()
        app.set_file(filename)
        sid = SearchInDictionary()
        sid.set_dic(app._data)
        res = sid.search(searchFor, reg=reg)
        # print("total results:", len(res))
        nf = NameFinder()
        founds = set()
        nf.set_data(app._data)
        text = ""
        i = 0
        for (loc, va) in (res):
            nf.set_location(LocationData(loc))
            # print( nf._location_data._content)
            path = Main._remove_dependencies_path(nf.get_name())
            if str(path) not in founds:
                text += f"{i+1} {str(loc)}\n{path}\n\n"
                founds.add(str(path))
                i += 1
        File.overWrite("temp.txt", text)
        File.openFile("temp.txt")
        return app

    def interpretPath(filename: str, loc: list):
        nf = NameFinder()
        nf.set_data(Main._readJson(filename))
        nf.set_location(LocationData(loc))
        return (nf.get_name())
    def getUIComponents(filename):
        components = Tools.get(Main._readJson(filename), ['result', 'resources', 'components'])
        res = []
        for comp in components:
            ui = comp['name']
            if ui in ["MainTemplate", "MyApp"]:
                continue
            res.append(ui)
        return res
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="enter the file name containing the json data for application")
    parser.add_argument("word", help="the word you are searching for")
    parser.add_argument("-r", "--regex", help="search with regex",
                    action="store_true")
    args = parser.parse_args()

    Main.getAllHardCodedValues(args.file, args.word, args.regex)

