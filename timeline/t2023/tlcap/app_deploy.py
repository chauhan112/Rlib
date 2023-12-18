import json
from FileDatabase import File
from jupyterDB import jupyterDB
from RegexDB import RegexDB
class AppDeployment:
    def __init__(self):
        self._filepath = None
    def set_file(self, filename):
        self._filepath = filename
        content = File.getFileContent(filename)
        self._data = json.loads(content)
    def printAllDependencies(self):
        a = {}
        self._res = {}
        self._deps(self._data["result"], a)
        from timeline.t2023.treeOps import DynamicTreeRenderer
        from ListDB import ListDB
        dtr = DynamicTreeRenderer()
        dtr.set_dic(a[("", '')])
        dtr.set_depth_level(10)
        def nm(i, x):
            return '-'.join(x)
        def set_child_getter():
            return list(map(lambda x: "-".join(x), ListDB.dicOps().get(dtr._model, dtr._loc).keys()))
        dtr.set_name_getter(nm)
        print(dtr.getAsText())
    def _printAllDependencies_previous(self):
        for obj in self._data["result"]["resolvedIncludes"]:
            print(obj["pk"]["name"] + "-" + obj["pk"]["label"])
            self._print_dependent_list(obj["includes"])
            print()
    def _printConfig(self, dic):
        if "configValues" in dic["resources"]:
            for x in dic["resources"]["configValues"]:
                if "name" in dic:
                    anme = dic["name"]
                else:
                    anme = dic["pk"]["name"]
                val = f"{anme}, {x['name']}, {x['type']}"
                if "value" in x:
                    val += ", " + str(x["value"])
                else:
                    val += ", -"
                print(val)
            print()
    def printAllConfigs(self):
        print("app, var, type, value")
        self._printConfig(self._data["result"])
        for x in self._data["result"]["resolvedIncludes"]:
            self._printConfig(x)
    def printConfigsForConfigEditing(self):
        print("key, value")
        self._attrConfig(self._data["result"])
        for x in self._data["result"]["resolvedIncludes"]:
            self._attrConfig(x)
    def _attrConfig(self, dic):
        REG = "\d+\.\d+\.\d+\-[a-zA-Z0-9]+.*/"
        mmpo  = {"STRING": "string", "INT":"number", "LONG": "number"}
        if "configValues" in dic["resources"]:
            for x in dic["resources"]["configValues"]:
                if "name" in dic:
                    key = "cnf:"+x['name']
                    urlValreplacer = dic["label"]
                else:
                    key = "cnf:ECT."+dic["pk"]["name"]+":"+x['name']
                    urlValreplacer = dic["pk"]["label"]
                if "value" in x:
                    ttp = mmpo[x["type"]]
                    val = x["value"]
                    if type(val) == list:
                        ttp = f"[{ttp}]"
                    elif RegexDB.isThereRegexMatch(REG, str(val)):
                        val =RegexDB.replace(REG, str(val), lambda x: urlValreplacer+"/")
                    ffp = f'{key}, {{"type":"{ttp}", "value":"{val}"}}'
                    print(ffp)
            print()
    def _print_dependent_list(self, deps):
        for i, x in enumerate(deps):
            print(f"{i+1}. {x['includedName']}-{x['includedLabel']}")
    def replaceDefaultConfig(self, x, content=None):
        if content is None:
            content = jupyterDB.clip().text()
        x["data"]["default.conf"] = content
        res = json.dumps(x)
        jupyterDB.clip().copy(res)
        print(res)
    def get_included_modules(self):
        apps = []
        for x in self._data["result"]["includes"]:
            apps.append(x["includedName"])
        return apps
    def open_all_imported_modules(self):
        from timeline.t2023.tlcap.preview_log import PreviewAutomater, OpenModule, AppPlayGroundLogger
        pa = PreviewAutomater()
        pa.set_link("https://k8-lcap-255-105.ect-telecoms.de/#/welcome?returnUrl=%2Fapps")
        pa.add_step(AppPlayGroundLogger("chauh-ra", ".%:;u4?eCW5,?$-#", pa.get_driver()))
        paap = OpenModule(pa.get_driver())
        paap.set_names(self.get_included_modules())
        pa.add_step(paap)
        pa.automate()
        return pa
    def _deps(self, objx, res = {}, parentName="", parentLabel=""):
        for i, obj in enumerate(objx['resolvedIncludes']):
            appName = obj["pk"]["name"]
            label = obj["pk"]["label"]
            if (parentName, parentLabel) not in res:
                res[(parentName, parentLabel)] = {}

            res[(parentName, parentLabel)][(appName, label)] = {}
            if 'resolvedIncludes' in obj:
                self._deps(obj, res[(parentName, parentLabel)], appName, label)
    def _dic_iterator(self, dic, collectorFunc, loc = []):
        if type(dic) == dict:
            for ke in dic:
                val = dic[ke]
                collectorFunc(val, ke, loc)
                self._dic_iterator(val, collectorFunc, loc + [ke])
        elif type(dic) == list:
            for i, val in enumerate(dic):
                collectorFunc(val,i, loc)
                self._dic_iterator(val, collectorFunc, loc + [i])