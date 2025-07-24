import ast
from modules.mobileCode.CmdCommand import GDataSetable, IReturnable
class IElement:
    pass

class Log:
    show_info = True

class CommonNamedBody(IElement, GDataSetable):
    def __init__(self):
        self._funcs = None
        self._classes = None
        self._attr = None
        self._imports = None

    def _parse(self):
        self._funcs = []
        self._classes = []
        self._attr = []
        self._imports = {}
        for ele in self.data.body:
            if isinstance(ele, ast.FunctionDef):
                fa = FunctionAst()
                fa.setData(ele)
                self._funcs.append(fa)
            elif isinstance(ele, ast.ClassDef):
                ca = ClassAst()
                ca.setData(ele)
                self._classes.append(ca)
            elif isinstance(ele, ast.Assign) or isinstance(ele, ast.AugAssign):
                aa = AttributeAst()
                aa.setData(ele)
                self._attr.append(aa)
            elif isinstance(ele, ast.Import) or isinstance(ele, ast.ImportFrom):
                self._imports.update(ImportParser(ele).get())
            else:
                if Log.show_info:
                    print(type(ele), end=",")

    def get_funcs(self):
        if self._funcs is None:
            self._parse()
        return self._funcs

    def get_name(self):
        return self.data.name

    def get_classes(self):
        if self._classes is None:
            self._parse()
        return self._classes

    def get_attributes(self):
        if self._attr is None:
            self._parse()
        return self._attr

    def get_dependency(self):
        from useful.ListDB import ListDB
        res = []
        for ele in self.data.body:
            if isinstance(ele, ast.ClassDef):
                ca = ClassAst()
                ca.setData(ele)
                res += ca.get_dependency()
            elif isinstance(ele, ast.FunctionDef) or isinstance(ele, ast.AsyncFunctionDef):
                fa = FunctionAst()
                fa.setData(ele)
                res += fa.get_dependency()
            else:
                uf = Uses()
                uf.setData(ele)
                res += uf.get()
        return ListDB.keepUnique(res, True)

    def get_imports(self):
        if self._imports is None:
            self._parse()
        return self._imports

class ClassAst(CommonNamedBody):
    def get_bases(self):
        return self.data.bases

class FunctionAst(CommonNamedBody):
    pass

class ModuleAst(CommonNamedBody):
    def get_name(self):
        return ''

class AttributeAst(IElement, GDataSetable):
    def get_name(self):
        attrs = []
        if 'targets' in self.data.__dict__:
            for tar in self.data.targets:
                attrs += self._resolve(tar)
        else:
            attrs += self._resolve(self.data.target)
        return attrs

    def _resolve(self, target):
        if isinstance(target, ast.Tuple):
            return TupleSolve(target).get()
        elif isinstance(target, ast.Name):
            return [target.id]
        elif isinstance(target, ast.Starred):
            if isinstance(target.value, ast.Name):
                return self._resolve(target.value)
        elif isinstance(target, ast.Attribute):
            return [Attrparse(target).get()]
        else:
            raise IOError("unknown found")

class TupleSolve(IElement, IReturnable):
    def __init__(self, data):
        self.data = data

    def get(self):
        res = []
        for ele in self.data.elts:
            if isinstance(ele, ast.Tuple):
                res += TupleSolve(ele).get()
            elif isinstance(ele, ast.Name):
                res.append(ele.id)
        return res

class UsesMoreSpecific(IElement, IReturnable, GDataSetable):
    def get(self):
        res = []
        if isinstance(self.data, ast.Module):
            us = Uses()
            for ele in self.data.body:
                us.setData(ele)
                res += us.get()
        elif isinstance(self.data, ast.Call):
            res += UsesFromCall(self.data).get()
        elif isinstance(self.data, ast.Assign) or isinstance(self.data, ast.AugAssign):
            res += UsesFromAssign(self.data).get()
        elif isinstance(self.data, ast.Expr):
            res += UsesFromExpr(self.data).get()
        elif isinstance(self.data, ast.ClassDef):
            ca = ClassAst()
            ca.setData(self.data)
            res += ca.get_dependency()
        elif isinstance(self.data, ast.FunctionDef) or isinstance(self.data, ast.AsyncFunctionDef):
            fd = FunctionAst()
            fd.setData(self.data)
            res += fd.get_dependency()
        elif isinstance(self.data, ast.Return):
            res += ReturnAst(self.data).get()
        else:
            i = 0
            for ele in ast.walk(self.data):
                if i == 0:
                    i = 1
                    continue
                usy = Uses()
                usy.setData(ele)
                res += usy.get()
        return list(set(res))

class UsesALittleSpecific(IElement, IReturnable, GDataSetable):
    def get(self):
        res = []
        if isinstance(self.data, ast.Call):
            res += UsesFromCall(self.data).get()
        elif isinstance(self.data, ast.ClassDef):
            ca = ClassAst()
            ca.setData(self.data)
            res += ca.get_dependency()
        elif isinstance(self.data, ast.FunctionDef) or isinstance(self.data, ast.AsyncFunctionDef):
            fd = FunctionAst()
            fd.setData(self.data)
            res += fd.get_dependency()
        else:
            for ele in ast.walk(self.data):
                if isinstance(ele, ast.Call):
                    usy = Uses()
                    usy.setData(ele)
                    res += usy.get()
        return list(set(res))

class Uses(IElement, IReturnable, GDataSetable):
    def get(self):
        res = []
        for ele in ast.walk(self.data):
            if isinstance(ele, ast.Call):
                res += UsesFromCall(ele).get()
        return list(set(res))

class GUsesElement(IElement):
    def __init__(self, data):
        self.data = data

class ImportParser(GUsesElement, IReturnable):
    def get(self):
        res = {}
        if isinstance(self.data, ast.ImportFrom):
            for nma in self.data.names:
                vval  = self.data.module
                if vval is None:
                   vval = ""
                vval += "/" + nma.name
                self._add(nma, vval, res)
        elif isinstance(self.data, ast.Import):
            for nma in self.data.names:
                self._add(nma, nma.name, res)
        return res

    def _add(self, alia, mod, dic):
        if alia.asname is not None:
            dic[alia.asname] = mod
        else:
            dic[alia.name] = mod

class UsesFromAssign(GUsesElement, IReturnable):
    def get(self):
        if isinstance(self.data.value, ast.Call):
            return UsesFromCall(self.data.value).get()
        return []

class UsesFromCall(GUsesElement, IReturnable):
    def get(self):
        uses = []
        uses += self._func_solve()
        for arg in self.data.args:
            if isinstance(arg, ast.Starred):
                uses += self._check(arg.value)
            else:
                uses += self._check(arg)

        for keyw in self.data.keywords:
            uses += self._check(keyw.value)
        return uses

    def _check(self, node):
        if isinstance(node, ast.Call):
            return UsesFromCall(node).get()
        return []

    def _func_solve(self):
        func = self.data.func
        if isinstance(func, ast.Attribute):
            return [tuple(Attrparse(func).get())]
        elif isinstance(func, ast.Name):
            return [(func.id, )]
        elif isinstance(func, ast.Call):
            return UsesFromCall(func).get()
        return []

class UsesFromExpr(GUsesElement, IReturnable):
    def get(self):
        if isinstance(self.data.value, ast.Call):
            return UsesFromCall(self.data.value).get()
        return []

class Attrparse(GUsesElement, IReturnable):
    def _get(self):
        res = []
        if isinstance(self.data.value, ast.Attribute):
            res = Attrparse(self.data.value).get() + res
        elif isinstance(self.data.value, ast.Name):
            res = [self.data.value.id] + res
        return res

    def get(self):
        return  self._get() + [self.data.attr]

class ReturnAst(GUsesElement, IReturnable):
    def get(self):
        usy = Uses()
        usy.setData(self.data.value)
        return usy.get()

class Main:
    def parse(content: str =None, file_path: str=None):
        from useful.FileDatabase import File
        if content is None:
            content = File.getFileContent(file_path)
        p = ast.parse(content)
        cnb = CommonNamedBody()
        cnb.setData(p)
        return cnb
    