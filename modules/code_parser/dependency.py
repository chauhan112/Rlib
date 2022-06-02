from OpsDB import IOps
from FileDatabase import File
import ast

class IDependent:
    def get_dependents(self):
        pass
    def get_name(self):
        pass

class IDependency:
    def get_dependencies(self) ->list[IDependent]:
        pass

class IDepView:
    def view(self):
        pass
class IViewClass:
    def get_dependent_classes(self) -> list[str]:
        pass
    def get_name(self):
        pass

class DependencyGraph(IOps):
    def __init__(self, classes: list[IDependent],skipClasses = []):
        self.classes = classes
        self.skipClasses = set(skipClasses)

    def execute(self):
        txt = ""
        for cls_ins in self.classes:
            dep_classes = cls_ins.get_dependent_classes()
            cls = cls_ins.get_name()
            for de in dep_classes:
                if(len(set([cls, de]).intersection(self.skipClasses)) != 0):
                    continue
                txt += f"[{cls}] ->[{de}]\n"
        return txt

class DepClassAsDic(IOps):
    def __init__(self, files, show_log = True):
        self._dependencies = {f: self._mod_ast(f) for f in files}
        from modules.code_parser.ast_parser import Log
        Log.show_info = show_log

    def execute(self):
        dep = self._dependencies
        classes_dep = {}
        for file in dep:
            clas = dep[file].get_classes()
            classes_dep[file] = {'imports': dep[file].get_imports(),
                                 'classes': {},
                                 'funcs'  : {}}
            for cls in clas:
                classes_dep[file]['classes'][cls.get_name()] = {'imports': cls.get_imports(), "funcs":{} }
                for fun in cls.get_funcs():
                    classes_dep[file]['classes'][cls.get_name()]['funcs'][fun.get_name()] = {'dep':fun.get_dependency(),
                                                                                   'imports': fun.get_imports()}
            for func in dep[file].get_funcs():
                classes_dep[file]['funcs'][func.get_name()] = { 'dep':func.get_dependency(),
                                                                'imports': func.get_imports()}
        return classes_dep
    def _mod_ast(self, file):
        from modules.code_parser.ast_parser import ModuleAst
        from FileDatabase import File
        content = File.getFileContent(file)
        ma = ModuleAst()
        ma.setData(ast.parse(content))
        return ma

class AstParseView(IViewClass):
    def __init__(self,name, cls_content):
        self._class_content = cls_content
        self._name = name
        self._reg = None
    def get_dependent_classes(self):
        from ListDB import ListDB
        res = []
        for func in self._class_content:
            for de in self._class_content[func]:
                res.append(de[0])

        res = ListDB.keepUnique(res, True)
        if self._reg is not None:
            return list(filter(lambda x: WordDB.regexMatchFound(self._reg, x), res))
        return res
    def get_name(self):
        return self._name
    def set_reg(self, reg):
        self._reg = reg
class MakeGraph(IOps):
    def __init__(self):
        self._primitive = ['self', 'len', 'list', 'zip', 'range', 'int', 'float', 'format', 'join', "type"]
    def setFile(self, file):
        self.file = file
    def execute(self):
        from jupyterDB import jupyterDB
        pypa_cls_dic = DepClassAsDic([self.file]).execute()[self.file]
        tzes= []
        for cls in pypa_cls_dic:
            apv = AstParseView(cls, pypa_cls_dic[cls])
#             apv.set_reg("^[A-Z]")
            tzes.append(apv)
        jupyterDB.clip().copy(DependencyGraph(tzes, skipClasses=self._primitive).execute())
    def open_site(self):
        import webbrowser
        webbrowser.open("https://yuml.me/diagram/scruffy/class/draw")

class MakeGraphManyFiles(MakeGraph):
    def setFiles(self, files):
        self.files = files
    def execute(self):
        from jupyterDB import jupyterDB
        dcad = DepClassAsDic(self.files)
        pypa_cls_dics = dcad.execute()
        tzes= []
        for fil in pypa_cls_dics:
            pypa_cls_dic = pypa_cls_dics[fil]
            for cls in pypa_cls_dic:
                apv = AstParseView(cls, pypa_cls_dic[cls])
                tzes.append(apv)
        jupyterDB.clip().copy(DependencyGraph(tzes, skipClasses=self._primitive).execute())

class IMakeGraph:
    def open_server(self):
        pass
    def graph(self):
        pass

class YumlGraphMaker(IMakeGraph):
    def setDependencyCreator(self, dep: IDependency):
        self.dep = dep
    def open_server(self):
        import webbrowser
        webbrowser.open("https://yuml.me/diagram/scruffy/class/draw")
    def graph(self):
        deps = self.dep.get_dependencies()
        txt = DependencyGraph(deps).execute()
        jupyterDB.clip().copy(txt)

class GDependency(IDependency):
    def __init__(self, files):
        self.files = files
        self._parsed = DepClassAsDic(self.files, False).execute()

class FilesDependency(GDependency):
    def get_dependencies(self):
        from WordDB import WordDB
        deps = self._imports_only()
        filter_deps = self._filter_imports_with_file(deps)
        common_part = WordDB.commonPart(list(filter_deps.keys()))
        dependents = []
        for f in filter_deps:
            vals = [v.replace(common_part,"") for v in filter_deps[f].values()]
            dependents.append(GDependent(f.replace(common_part,""), vals))
        return dependents

    def _filter_imports_with_file(self, dic):
        newdic = {}
        keys = dic.keys()
        yes_or_no = {}
        for file in dic:
            newdic[file] = {}
            for imp in dic[file]:
                val = dic[file][imp]
                if val not in yes_or_no:
                    yes_or_no[val] = self.check(val, keys)
                if yes_or_no[val][0]:
                    newdic[file][imp] = yes_or_no[val][1]
        return newdic

    def check(self, val, container):
        for v in container:
            if self._check(val, v):
                return True, v
        return False, None

    def _check(self, val, name):
        truth = val +"/" in name or val+".py" in name
        if truth:
            return True
        val = "/".join(val.split("/")[:-1])
        return val + "/" in name or val + ".py" in name

    def _imports_only(self):
        sanitize = lambda dic: {x:dic[x].replace(".", "/").strip("/") for x in dic}
        res = self._parsed
        imports_only = {}
        res = {f.replace("\\","/"): res[f] for f in res}
        for f in res:
            imports_only[f] = sanitize(res[f]['imports'])
            for cls in res[f]['classes']:
                imports_only[f].update(sanitize(res[f]['classes'][cls]['imports']))
                for func in res[f]['classes'][cls]['funcs']:
                    imports_only[f].update(sanitize(res[f]['classes'][cls]['funcs'][func]['imports']))
            for func in res[f]['funcs']:
                imports_only[f].update(sanitize(res[f]['funcs'][func]['imports']))
        return imports_only

class Main:
    pass