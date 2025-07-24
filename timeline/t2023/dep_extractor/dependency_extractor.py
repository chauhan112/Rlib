import os
from useful.FileDatabase import File
import ast
from useful.ListDB import ListDB
from useful.jupyterDB import jupyterDB

class NameSpace:
    pass
class CentralLocationImports:
    all_imports = {}
    all_calls = {}
class ImportsTracker:
    def _get_used_imports_in_map(self, imps):
        used_imports = []
        for im in imps:
            newNames = []
            for name in im.names:
                used_name = name.name
                if name.asname:
                    used_name = name.asname
                if used_name in self._bsc.clss.resolver._all_calls:
                    newNames.append(name)
            if len(newNames):
                newIm = AstTools.copyFuncOrClassDef(im)
                newIm.lineno = im.lineno
                newIm.names = newNames
                newIm._parent = im._parent
                used_imports.append(newIm)
                self._index_import(newIm, newNames)
        return used_imports
    def _index_import(self, im, usedNames):
        for nn in usedNames:
            filepath = self._bsc.clss.dep.get_file_path_from_import(im)
            try:
                locs = ListDB.dicOps().get(CentralLocationImports.all_imports, [filepath, nn.name])
            except:
                locs = {}
                DicOps.addEventKeyError(CentralLocationImports.all_imports, [filepath, nn.name], locs)
            if (self._bsc._filepath, im.lineno) not in locs:
                locs[(self._bsc._filepath, im.lineno)] = im
    def set_basic(self, basic):
        self._bsc = basic
class BasicSetters:
    def __init__(self):
        self._filepath = None
    def set_content(self, content):
        self._content = content
        self._lines  = content.splitlines()
        self._root = ast.parse(self._content)
    def set_file(self, fiel):
        self._filepath = fiel
        self.set_content( File.getFileContent(fiel))
    def set_prefix(self, prefix):
        self._prefix = prefix
class DependencyExtractor:
    def __init__(self):
        self._temp_result = []
        self._typ = set()
        self._all_imports = {}
    def set_type_checker(self, ech):
        self._checker = ech
    def set_basic(self, basic):
        self._basic = basic
    def get_imports(self, scope=None):
        if scope is None:
            scope = self._basic._root
        self._temp_result.clear()
        self.iteriter(scope, self._imports)
        return self._temp_result.copy()
    def _imports(self, astObj):
        if isinstance(astObj, ast.Import) or isinstance(astObj, ast.ImportFrom):
            self._temp_result.append(astObj)
    def iteriter(self, astObj, extractFunc=None, parent=None):
        if extractFunc is None:
            extractFunc = lambda x: x
        skipper = extractFunc(astObj)
        if type(skipper) == bool and skipper:
            return
        if type(astObj) in [set, list]:
            for val in astObj:
                self.iteriter(val, extractFunc, parent)
        elif isinstance(astObj, ast.AST):
            astObj._parent = parent
            if type(astObj) not in self._typ:
                self._typ.add(type(astObj))
            for _, val in ast.iter_fields(astObj):
                self.iteriter(val, extractFunc, astObj)
        else:
            if type(astObj) in [str, int, bool, float]:
                pass
            elif astObj:
                print(type(astObj), astObj)
    def _add_to_path(self, path, dic, im):
        if path not in dic:
            dic[path] = []
        for n in im.names:
            dic[path].append((n.name, n.asname, im))
    def get_file_path_from_import(self, im):
        if isinstance(im, ast.Import):
            return None
        file= self._basic._prefix.replace(os.sep,"/") + "/" + im.module.replace(".", "/") + ".py"
        initPath = self._basic._prefix.replace(os.sep,"/") + "/" + im.module.replace(".", "/") + "/__init__.py"
        if os.path.exists(file):
            return file
        elif os.path.exists(initPath):
            return initPath
        return None
    def _paths_with_classes(self, imports = None):
        if imports is None:
            imports = self.get_imports()
        fileWithClasses = {}
        for im in imports:
            path = self.get_file_path_from_import(im)
            self._add_to_path(path, fileWithClasses, im)
        return fileWithClasses
    def _typeExtractor(self, astObj):
        if self._checker(astObj):
            self._temp_result.append(astObj)
    def get_all_classes(self):
        self._temp_result.clear()
        self.set_type_checker(lambda x: isinstance(x, ast.ClassDef))
        self.iteriter(self._basic._root, self._typeExtractor)
        return self._temp_result.copy()
    def get_content(self, obj):
        return "\n".join(self._basic._lines[obj.lineno-1: obj.end_lineno])
    def get_all_functions(self):
        self._temp_result.clear()
        self.set_type_checker(lambda x: isinstance(x, ast.FunctionDef))
        self.iteriter(self._basic._root, self._typeExtractor)
        return self._temp_result.copy()
    def get_obj(self, name):
        funcs = self.get_all_functions()
        res = []
        for func in funcs:
            if func.name == name:
                res.append(func)
        lcss = self.get_all_classes()
        for clss in lcss:
            if clss.name == name:
                res.append(clss)
        return res
    def get_calls(self, scope = None):
        if scope is None:
            scope = self._basic._root
        self._temp_result.clear()
        self.set_type_checker(lambda x: isinstance(x, ast.Call))
        self.iteriter(scope, self._typeExtractor)
        return self._temp_result.copy()
    def get_used_imports(self, scope = None, imports=None):
        if scope is None:
            scope = self._basic._root
        
        imports = self._paths_with_classes(imports)
        usedImports = {}
        for k in imports:
            imps = imports[k]
            for name, asname, imported in imps:
                s = asname
                if asname is None:
                    s = name
                if(self._basic.clss.ef.isUsed(s, scope)):
                    if k not in usedImports:
                        usedImports[k] = []
                    ins = None
                    if k:
                        ins = Main.get_instance(path=k, prefix= self._basic._prefix)
                    usedImports[k].append((name, asname, imported, ins))
        return usedImports
class ExtraFunctionality:
    def __init__(self):
        self._abc = NameSpace()
    def set_basic(self, basic):
        self._basic = basic
    def _removed_resolved_imported_lines_and_print(self,obj):
        if isinstance(obj, ast.Import) or isinstance(obj, ast.ImportFrom):
            if obj.lineno in self._abc.linesToNotIgnore:
                self._abc.res += self._abc.used_importsLins[obj.lineno] + "\n"
                self._abc.visited_lines.add(obj.lineno)
        elif hasattr(obj, "lineno") and obj.lineno not in self._abc.visited_lines:
            self._abc.res += self._basic.clss.dep._basic._lines[obj.lineno-1] + "\n"
            self._abc.visited_lines.add(obj.lineno)
    def display_first_level_imports(self, scope=None):
        if scope is None:
            scope = self._basic._root
        imps = self._basic.clss.dep.get_used_imports(scope)
        linesToNotIgnore =  set()
        resolved = ""
        for pat in imps:
            vals = imps[pat]
            if pat:
                for val in vals:
                    name, asanme, im, ins = val
                    objs = ins.get_obj(name)
                    for obj in objs:
                        resolved += ins.get_content(obj) + "\n\n"
            else:
                for name, asanme, im, ins in vals:
                    linesToNotIgnore.add(im.lineno)
        
        self.remove_unnecessary_imports(scope)
        self._abc.res = ""
        self._abc.visited_lines = set()
        self._abc.linesToNotIgnore = linesToNotIgnore
        self._basic.clss.dep.iteriter(self._basic._root, self._removed_resolved_imported_lines_and_print)
        resolved += self._abc.res + "\n\n"
        display(ModuleDB.colorPrint("python", resolved))
    def isUsed(self, name: str, scope: ast.AST = None):
        uses = self.get_uses(name, scope)
        return len(uses)
    def get_uses(self, name: str, scope = None):
        if scope is None:
            scope = self._basic._root
        def attrChecker(ob, cc):
            if isinstance(ob.value, ast.Name) and ob.value.id== name:
                self._basic.clss.dep._temp_result.append(cc)
        def importExtrac(ob):
            self._basic.clss.dep._debug = ob
            if isinstance(ob, ast.Call):
                if isinstance(ob.func, ast.Name) and ob.func.id == name:
                    self._basic.clss.dep._temp_result.append(ob)
                elif isinstance(ob.func, ast.Attribute):
                    attrChecker(ob.func, ob)
            elif isinstance(ob, ast.Attribute):
                attrChecker(ob, ob)
            elif isinstance(ob, ast.Name) and ob.id== name:
                self._basic.clss.dep._temp_result.append(ob)
        self._basic.clss.dep._temp_result.clear()
        self._basic.clss.dep.iteriter(scope, importExtrac)
        return self._basic.clss.dep._temp_result.copy()
    def remove_unnecessary_imports(self, scope=None):
        if scope is None:
            scope = self._basic._root
        self._abc.res = ""
        self._abc.visited_lines = set()
        self._abc.used_imports = self._basic.clss.dep.get_used_imports(scope)
        used_importsLins = {}
        for path in self._abc.used_imports:
            imports = self._abc.used_imports[path]
            for name, asname, im, ll in imports:
                if im.lineno not in used_importsLins:
                    if path or isinstance(im, ast.ImportFrom):
                        used_importsLins[im.lineno] = " "* im.col_offset + "from " + im.module + " import " + name 
                    else:
                        used_importsLins[im.lineno] = " "* im.col_offset +"import " + name
                    if asname:
                        used_importsLins[im.lineno] += " as " + asname
                    continue
                used_importsLins[im.lineno] += ", "+ name
                if asname:
                    used_importsLins[im.lineno] += " as " + asname
        self._abc.used_importsLins = used_importsLins
        self._basic.clss.dep.iteriter(self._basic._root, self._printer)
        return self._abc.res 
    def _printer(self,obj):
        if isinstance(obj, ast.Import) or isinstance(obj, ast.ImportFrom):
            if obj.lineno in self._abc.used_importsLins:
                self._abc.res += self._abc.used_importsLins[obj.lineno] + "\n"
                self._abc.visited_lines.add(obj.lineno)
        elif hasattr(obj, "lineno") and obj.lineno not in self._abc.visited_lines:
            self._abc.res += self._basic.clss.dep._basic._lines[obj.lineno-1] + "\n"
            self._abc.visited_lines.add(obj.lineno)
class Resolver:
    def __init__(self):
        self._abc = NameSpace()
    def set_basic(self, basic):
        # print(type(basic))
        self._basic = basic
    def resolve_classes(self, scope, fileiNs):
        return self._resolve_classes(scope, fileiNs)
    def _resolve_classes(self, scope, fileiNs):
        self._abc.imported_tracker.add((fileiNs._filepath, scope.name))
        resolved = ""
        clsses = list(filter(lambda x: x.name != scope.name, fileiNs.clss.dep.get_all_classes()))
        for cls in clsses:
            if (fileiNs.clss.ef.isUsed(cls.name, scope)) and (fileiNs._filepath, cls.name) not in self._abc.imported_tracker:
                self._abc.imported_tracker.add((fileiNs._filepath, cls.name))
                res = self._resolve_classes(cls, fileiNs)
                resolved += "\n\n" + res
                resolved = resolved.strip()
        res = self._resolve_imports(fileiNs, scope)
        resolved += "\n\n" + res
        resolved = resolved.strip()
        return resolved
    def _resolve_imports(self,insM,sp=None):
        imps = insM.clss.dep.get_used_imports(sp)
        resolved = ""
        for pat in imps:
            vals = imps[pat]
            if pat:
                for val in vals:
                    name, asanme, im, ins = val
                    objs = ins.get_obj(name)
                    for obj in objs:
                        if (ins._basic._filepath, obj.name) not in self._abc.imported_tracker:
                            resolved += "\n\n" + self._resolve_classes(obj, ins._basic)
                            resolved = resolved.strip()
                            self._abc.imported_tracker.add((ins._basic._filepath, obj.name))
        if sp:
            resolved += "\n\n" + ast.unparse(sp)
        else:
            resolved += "\n\n" + ast.unparse(insM._root)

        return resolved
    def resolve_imports(self, ins=None):
        if ins is None:
            ins = self._basic
        self._abc.imported_tracker = set()
        return self._resolve_imports(ins)
class CallsExtractor:
    def __init__(self):
        self._call_resolver_map_tester = {}
        self._calls_resolver_tracker = set()
    def _call_getter(self, node):
        if isinstance(node, ast.Call):
            pnode = self._get_parent_call(node)
            self._call_resolver_map_tester[id(pnode)] = pnode
    def _get_parent_call(self, node):
        self._calls_resolver_tracker.add(id(node))
        higest_call = node
        while node._parent:
            if isinstance(node._parent, ast.Call):
                self._calls_resolver_tracker.add(id(node._parent))
                higest_call= node._parent
            node = node._parent
            if not isinstance(node, ast.Attribute):
                break
        return higest_call
    
    def get_all_calls(self, node):
        self._call_resolver_map_tester.clear()
        self._calls_resolver_tracker.clear()
        AstTools.assign_parent(node)
        self._bsc.clss.dep.iteriter(node, extractFunc=self._call_getter)
        return list(self._call_resolver_map_tester.values())
    def set_basic(self, basic):
        self._bsc = basic
class NewResolver:
    def __init__(self):
        self._ce = None
    def _get_call_extractor(self):
        if self._ce is None:
            self._ce = CallsExtractor()
            self._ce.set_basic(self._basic)
        return self._ce
    def _separate(self, nodeWithBody):
        defs = []
        nondefs = []
        imps = []
        self._basic.clss.dep.iteriter(nodeWithBody)
        for el in nodeWithBody.body:
            if isinstance(el, ast.ClassDef) or isinstance(el, ast.FunctionDef):
                defs.append(el)
            elif isinstance(el, ast.Import) or isinstance(el, ast.ImportFrom):
                imps.append(el)
            else:
                nondefs.append(el)
        return imps, defs, nondefs
    def _has_parent(self, k, typ):
        while k:
            if isinstance(k, typ):
                return True
            k = k._parent
        return False
    def _splitCallAttr(self, node):
        def splitter(callNode, res = None):
            if res is None:
                res = []
            if isinstance(callNode, ast.Call):
                return splitter(callNode.func, res)
            elif isinstance(callNode, ast.Name):
                res.append(callNode.id)
                return res
            elif isinstance(callNode, ast.Attribute):
                res.append(callNode.attr)
                return splitter(callNode.value, res)
            return res
        attrs = splitter(node)
        return attrs[::-1]
    def _get_all_calls(self, nodeL, res = None):
        ce = self._get_call_extractor()
        calls = ce.get_all_calls(nodeL)
        if res is None:
            res = {}
        for node in calls:
            txloc = self._splitCallAttr(node.func)
            txloc.append('<value>')
            self._add_to_call(res, txloc, node)
        return res
    
    def _add_to_call(self, res, loc, node):
        try:
            vals = ListDB.dicOps().get(res, loc)
        except:
            vals = []
            DicOps.addEventKeyError(res, loc, vals)
        vals.append(node)
    def _get_all_uses(self, node, res = None):
        if res is None:
            res = {}
        self._get_all_calls(node, res)
        def coll(dic, node):
            for n in node.bases:
                if isinstance(n, ast.Name):
                    txloc = [n.id,'<value>']
                    self._add_to_call(res, txloc, n)
                else:
                    print(ast.unparse(n))
        self._get_any(node, res, conditions= [lambda node, res: isinstance(node, ast.ClassDef) and node.bases],
                      collector=coll)
        return res
    def _all_names(self, nodeL,  res = None):
        if res is None:
            res = {}
        for node in ast.walk(nodeL):
            if isinstance(node, ast.Name):
                if node.id not in res:
                    res[node.id] = node
        return res
    def _get_any(self, nodeL, res=None, conditions = None, collector = None):
        def def_colec(dic, node):
            dic[node.id] = node
        if res is None:
            res = {}
        if conditions is None:
            print("pass a condition")
            return 
        if collector is None:
            collector = def_colec
        for node in ast.walk(nodeL):
            for i, cond in enumerate(conditions):
                if cond(node, res):
                    collector(res, node)
                    break
        return res
    def _bases_and_anno(self, nodeL, res = None):
        if res is None:
            res = {}
        for node in ast.walk(nodeL):
            if isinstance(node, ast.AnnAssign) or isinstance(node, ast.arg):
                if node.annotation:
                    res[node.annotation.id] = node
            elif isinstance(node, ast.ClassDef) and node.bases:
                for n in node.bases:
                    res[n.id] = node
        return res
    def _parse_body(self, objWithBody):
        self._parse()
        _, _ , self._exps = self._separate(objWithBody)
        self._all_calls = self._get_all_uses(objWithBody)
        self._used_imports = self._basic.clss.it._get_used_imports_in_map(self._imports)
    def _parse(self):
        self._imports = self._basic.clss.dep.get_imports()
        _, self._defs, self._exps = self._separate(self._basic._root)
        self._all_calls = self._get_all_uses(self._basic._root)
        self._used_imports = self._basic.clss.it._get_used_imports_in_map(self._imports)
    def get_first_layer(self):
        if not hasattr(self, "_parsed") or not self._parsed:
            self._parse()
        return self._exps
    def set_basic(self, basic):
        self._basic = basic
class Indexing:
    def __init__(self):
        self._indices = {}
        self._import_dic = {}    
    def _make_parent_tuple(self, node, loc=None):
        if loc is None:
            loc =  []
        if node:
            if hasattr(node, "name"):
                name = node.name
            elif hasattr(self._basic, "_filepath") and self._basic._filepath: 
                name = self._basic._filepath
            else:
                name = None
            loc.append(name)
            self._make_parent_tuple(node._parent, loc)
        return loc[::-1]
    def _create_node(self, node):
        loc = self._make_parent_tuple(node)
        DicOps.addEventKeyError(self._indices, loc + ["<value>"], node)
    def _collector(self, x):
        if isinstance(x, ast.ClassDef) or isinstance(x, ast.FunctionDef):
            self._create_node(x)
        elif isinstance(x,ast.Import) or isinstance(x, ast.ImportFrom):
            lien = ast.unparse(x)
            if lien not in self._import_dic:
                self._import_dic[lien] = x
    def index(self):
        if len(self._indices):
            return self._indices
        self._indices.clear()
        self._import_dic.clear()
        self._basic.clss.dep.iteriter(self._basic._root)
        self._basic.clss.dep.iteriter(self._basic._root, self._collector)
        return self._indices
    def set_basic(self, basic):
        self._basic = basic
class RemoveAnnotation:
    def __init__(self):
        self._decorators_to_ignore = set(["dataclass"])
    def remove(self, node):
        dep = DependencyExtractor()
        dep.iteriter(node, extractFunc=self._remove)
        self._remove_ann_assign(node)
    def _remove(self, node):
        if isinstance(node, ast.AnnAssign):
            pass
        elif isinstance(node, ast.arg) and node.annotation:
            if not self._has_decorator_of_data_class(node):
                node.annotation = None
    def _has_decorator_of_data_class(self, node):
        while node:
            if isinstance(node, ast.ClassDef):
                for n in node.decorator_list:
                    if n.id in self._decorators_to_ignore:
                        return True
            node = node._parent
        return False
    def _replace_ann_assign(self, node):
        newNode = ast.Assign(targets=[node.target])
        for key, val in ast.iter_fields(node):
            if key not in ["annotation","simple"]:
                setattr(newNode, key, val)
        newNode.lineno = node.lineno
        return newNode
    def _remove_ann_assign(self, node):
        if isinstance(node, (ast.AnnAssign)):
            if not self._has_decorator_of_data_class(node):
                return self._replace_ann_assign(node)
        elif hasattr(node, "body"):
            new_body = [self._remove_ann_assign(n) for n in node.body]
            if len(new_body) == 0:
                return None
            node.body = new_body
        return node
class AstTools:
    def copyFuncOrClassDef(node):
        newnode = node
        if isinstance(node, ast.FunctionDef):
            newnode = ast.FunctionDef()
        elif isinstance(node, ast.ClassDef):
            newnode = ast.ClassDef()
        elif isinstance(node, ast.Import):
            newnode = ast.Import()
        elif isinstance(node, ast.ImportFrom):
            newnode = ast.ImportFrom()
        else: 
            print("not copying" + str(node))
            return node
        for key, val in ast.iter_fields(node):
            setattr(newnode, key, val)
        return newnode
    def remove_imports(node):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            return None
        elif hasattr(node, "body"):
            new_body = [AstTools.remove_imports(n) for n in node.body if AstTools.remove_imports(n) is not None]
            if len(new_body) == 0:
                return None
            node.body = new_body
        return node
    def remove_annotations(node):
        ra = RemoveAnnotation()
        ra.remove(node)
    def assign_parent(astObj, parent=None):
        if type(astObj) in [set, list]:
            np = NameSpace()
            np.value = astObj
            np._parent = parent
            for val in astObj:
                AstTools.assign_parent(val, np)
        elif isinstance(astObj, ast.AST):
            astObj._parent = parent
            for _, val in ast.iter_fields(astObj):
                AstTools.assign_parent(val, astObj)
        else:
            if type(astObj) in [str, int, bool, float]:
                pass
            elif astObj:
                print(type(astObj), astObj)
    def get_new_name(path, prefix, class_name):
        prefic = prefix.replace(os.sep, "/")
        path = path.replace(os.sep, "/")
        fil = path.replace(prefic, "")
        file = fil.replace("__init__.py","").strip("/").replace("/", "_")
        file = file.replace(".py", "")
        return file + class_name
class DicOps:
    def addEventKeyError(dic, loc, val):
        valT = dic
        lastKey = loc.pop()
        for x in loc:
            if type(valT) == dict and x not in valT:
                valT[x] = {}
            valT = valT[x]
        valT[lastKey] = val
    def get(dic, loc):
        val = dic
        for x in loc:
            val = val[x]
        return val
    def dicIterIter(cont, loc = None, extract_func=None, apply_value_func=None):
        if extract_func is None:
            extract_func = lambda dic, loc: None
        if apply_value_func is None:
            apply_value_func = lambda dic, loc: None
        if loc is None:
            loc = []
        dic = ListDB.dicOps().get(cont, loc)
        if isinstance(dic, dict):
            for key in dic:
                loc.append(key)
                extract_func(dic, loc)
                DicOps.dicIterIter(cont, loc = loc, extract_func=extract_func, apply_value_func=apply_value_func)
                loc.pop()
        elif isinstance(dic, list):
            for i, item in enumerate(dic):
                loc.append(i)
                extract_func(dic, loc)
                DicOps.dicIterIter(cont, loc = loc, extract_func=extract_func,apply_value_func=apply_value_func)
                loc.pop()
        else:
            apply_value_func(dic, loc)
class ScopeStorer:
    def __init__(self) -> None:
        self._defs = []
        self._imports = []
        self._used_imports = []
        self._all_calls = []
        self._exps = []
    def save_scope(self, resolver):
        self._defs.append(resolver._defs)
        self._imports.append(resolver._imports)
        self._used_imports.append(resolver._used_imports)
        self._all_calls.append(resolver._all_calls)
        self._exps.append(resolver._exps)
    def pop_scope(self, resolver):
        if len(self._defs) > 0:
            resolver._defs = self._defs.pop()
            resolver._imports = self._imports.pop()
            resolver._used_imports = self._used_imports.pop()
            resolver._all_calls = self._all_calls.pop()
            resolver._exps = self._exps.pop()
class ResolveImportsAndCalls:
    def __init__(self) -> None:
        self._resolved_tracker = {}
        self._resolved = []
        self._instance_tracker = {}
        self._scope_storer = ScopeStorer()
    def add_functions(self,child, funcs, clsName):
        path = child._filepath 
        indices = child.clss.ind.index()
        clssFuncs = indices[path][clsName].keys()
        non_deprecated_funcs = []
        for f in funcs:
            if f in clssFuncs:
                non_deprecated_funcs.append(f)
            else:
                print(f"class {clsName} does not have {f} anymore")

        previousFuncs = ListDB.dicOps().get(self._resolved_tracker, [path, clsName,'<method>'])
        clsNode  = ListDB.dicOps().get(self._resolved_tracker, [path, clsName,'<value>'])
        for f in non_deprecated_funcs:
            clsNode.body.append(indices[path][clsName][f]['<value>'])
            previousFuncs.append(f)
        
        node = AstTools.copyFuncOrClassDef(clsNode)
        nb = [indices[path][clsName][k]['<value>'] for k in non_deprecated_funcs]
        node.body = nb
        return node
    def _get_current_call(self, bsca, clsName, asName):
        if asName:
            val = bsca.clss.resolver._all_calls[asName]
        else:
            val = bsca.clss.resolver._all_calls[clsName]
        return val
    def get_functions(self, bsca, clsName, asName):
        val = self._get_current_call(bsca, clsName=clsName, asName=asName)
        funcs = []
        if isinstance(val, dict):
            funcs = [k for k in val if k != "<value>"]
        return funcs
    def add_new_node(self, child, toRe, clsName):
        if isinstance(toRe, ast.ClassDef):
            toRe2 = AstTools.copyFuncOrClassDef(toRe)
            toRe2.body = [ep for ep in toRe.body if not isinstance(ep, ast.FunctionDef)]
            toRe2.lineno = toRe.lineno
        else:
            toRe2 = toRe
        DicOps.addEventKeyError(self._resolved_tracker, [child._filepath, clsName,'<value>'], toRe2)
        DicOps.addEventKeyError(self._resolved_tracker, [child._filepath, clsName,'<method>'], [])
        if (child._filepath, clsName) not in self._resolved:
            self._added = True
            self._resolved.append((child._filepath, clsName))
    def filter_out_imported_funcs(self, bsca, clsName, funcs):
        previ = ListDB.dicOps().get(self._resolved_tracker, [bsca._filepath, clsName,'<method>'])
        newfuncs = []
        for f in funcs:
            if f not in previ:
                newfuncs.append(f)
        return newfuncs
    def exists(self, bsca, clsName):
        try:
            ListDB.dicOps().get(self._resolved_tracker, [bsca._filepath, clsName,'<value>'])
            return True
        except:
            pass
        return False
    def _update_for_instance(self, node, path, clsName):
        previousFuncs = ListDB.dicOps().get(self._resolved_tracker, [path, clsName,'<method>'])
        clsNode  = ListDB.dicOps().get(self._resolved_tracker, [path, clsName,'<value>'])
        for f in node.body:
            if isinstance(f, ast.FunctionDef):
                has_self_parameter = any(param.arg == 'self' for param in f.args.args)
                if has_self_parameter and f.name not in previousFuncs:
                    clsNode.body.append(f)
                    previousFuncs.append(f.name)
    def extractFuncs(self, parent, clsName, asName, child):
        indices = child.clss.ind.index()
        toReClsass = indices[child._filepath][clsName]['<value>']
        self._added = False
        if not self.exists(child, clsName):
            self.add_new_node(child, toReClsass, clsName)
        funcs = self.get_functions(parent, clsName, asName)
        if len(funcs) == 0:
            self._update_for_instance(toReClsass, child._filepath, clsName)
        newfuns = self.filter_out_imported_funcs(child, clsName, funcs)
        if len(newfuns) == 0:
            if self._added:
                return self._added, toReClsass
            return False, None
        node = self.add_functions(child, newfuns, clsName)
        return True, node
    def _resolve(self, bsca, scope=None):
        if scope is None:
            bsca.clss.resolver._parse()
        pathsWith = bsca.clss.dep._paths_with_classes(bsca.clss.resolver._used_imports)
        for path in pathsWith:
            if path is None: continue
            lowInstance = self._get_instance(path)
            for clsName, asName, im in pathsWith[path]:
                self._log_calls(lowInstance, bsca, clsName, asName)
                added, scope = self.extractFuncs(bsca, clsName, asName, lowInstance)
                if added:
                    self._save_scope_resolve(lowInstance, scope)
    def _log_calls(self, _from, to, clsName, asName):
        from_path = _from._filepath
        to_path = to._filepath
        if from_path not in CentralLocationImports.all_calls:
            CentralLocationImports.all_calls[from_path] = {}
        if clsName not in CentralLocationImports.all_calls[from_path]:
            CentralLocationImports.all_calls[from_path][clsName] = {}
        val = self._get_current_call(to, clsName=clsName, asName=asName)
        dic = CentralLocationImports.all_calls[from_path][clsName]
        if to_path not in dic:
            dic[to_path] = {}
        self._update_dic(dic[to_path], val)
    def _update_dic(self, dicA, dicB):
        for k in dicB:
            if k not in dicA: 
                dicA[k] = dicB[k]
                continue
            val = dicB[k]
            if isinstance(val, dict):
                self._update_dic(dicA[k], dicB[k])
            elif isinstance(val, list):
                for el in val:
                    if el not in dicA[k]:
                        dicA[k].append(el)
            else:
                print("different")
    def _save_scope_resolve(self, child, scope):
        scouped = False
        if hasattr(child.clss.resolver, "_defs"):
            scouped = True
            self._scope_storer.save_scope(child.clss.resolver)
        child.clss.resolver._parse_body(scope)
        self._resolve(child, scope)
        self._resolve_scope(child)
        if scouped:
            self._scope_storer.pop_scope(child.clss.resolver)
    def _resolve_scope(self, child):
        indices = child.clss.ind.index()
        if child._filepath in indices: 
            indices = indices[child._filepath]
        for usedName in indices:
            if usedName in child.clss.resolver._all_calls:
                self._log_calls(child, child, usedName, usedName)
                added, scope = self.extractFuncs(child, usedName, None, child)
                if added:
                    self._save_scope_resolve(child, scope)
    def resolve(self):
        CentralLocationImports.all_imports.clear()
        CentralLocationImports.all_calls.clear()
        self._resolved.clear()
        self._resolved_tracker.clear()
        self._bsca.clss.resolver._parse()
        self._resolve(self._bsca)
    def set_parent(self, parent):
        self._bsca = parent
    def _get_instance(self, path):
        if path not in self._instance_tracker: 
            self._instance_tracker[path] = Main.get_instance(path=path, prefix=self._bsca._prefix)
        return self._instance_tracker[path]
    def copy_to_clipboard(self):
        jupyterDB.clip().copy(self.get_resolved_text())
    def get_resolved_text(self):
        body = []
        done= set()
        for ke in self._resolved[::-1]:	
            if ke not in done:
                body.append(ListDB.dicOps().get(self._resolved_tracker, list(ke) + ["<value>"]))
                done.add(ke)
        return ast.unparse(body + self._bsca.clss.resolver.get_first_layer())
class ImportsRenamer:
    def __init__(self) -> None:
        self._varAlloc = NameSpace()
    def _applying(self, val, loc):
        self._change_class_name(val, self._varAlloc.name)
    def _change_class_name(self, node, new_name):
        if isinstance(node, ast.Attribute):
            self._change_class_name(node.value, new_name)
        elif isinstance(node, ast.Call):
            self._change_class_name(node.func, new_name)
        elif isinstance(node, ast.Name):
            node.id = new_name
        elif isinstance(node, ast.ClassDef):
            for n in node.bases:
                if self._varAlloc.nameUsedScope == n.id or self._varAlloc.clsName == n.id:
                    self._change_class_name(n, new_name)
        else:
            print("error a different type of node was detected", node)
    def _resolve_imports(self):
        for _from in CentralLocationImports.all_imports:
            for clsName in CentralLocationImports.all_imports[_from]:
                usedIn = CentralLocationImports.all_imports[_from][clsName]
                for to, lineNr in usedIn:
                    imp = usedIn[(to,lineNr)]
                    if isinstance(imp, ast.Import):
                        continue
                    resolved = self._rename_imports_calls(imp,clsName)
                    for na in resolved:
                        self._add_rename_resolved_imports(_from, na)
    def _rename_imports_calls(self, imp, clsName):
        res = []
        for n in imp.names:
            clsName = n.name
            path = self._bsc.clss.dep.get_file_path_from_import(imp)
            uses = self._bsc.clss.resolver._get_all_uses(imp._parent)
            nameUsed = clsName
            if n.asname:
                nameUsed = n.asname
            if path not in self._ri._resolved_tracker:
                continue
            if clsName not in self._ri._resolved_tracker[path]:
                continue
            newName = imp.module.replace(".", "_") + clsName
            self._ri._resolved_tracker[path][clsName]['<value>'].name = newName
            self._varAlloc.name = newName
            if nameUsed in uses:
                nameUsedScope = uses[nameUsed]
            elif newName in uses:
                nameUsedScope = uses[newName]
            else:
                continue
            res.append(clsName)
            self._varAlloc.nameUsedScope = nameUsedScope
            self._varAlloc.clsName = clsName
            DicOps.dicIterIter(nameUsedScope, apply_value_func = self._applying)
        return res
    def _add_rename_resolved_imports(self, _from, name):
        if _from not in self._varAlloc.imports_resolved:
            self._varAlloc.imports_resolved[_from] = set()
        self._varAlloc.imports_resolved[_from].add(name)
    def _extact_all_non_resolved_imports(self, val, loc):
        filePath = loc[0]
        if filePath in self._varAlloc.imports_resolved and loc[1] in self._varAlloc.imports_resolved[filePath]:
            return
        path = self._bsc.clss.dep.get_file_path_from_import(val)
        if path is None:
            self._varAlloc.allNonResolvedImports.add(ast.unparse(val))
    def rename(self):
        self._varAlloc.imports_resolved = {}
        self._varAlloc.allNonResolvedImports = set()
        self._resolve_imports()
        DicOps.dicIterIter(CentralLocationImports.all_imports, apply_value_func=self._extact_all_non_resolved_imports)
    def set_basic(self, val):
        self._bsc = val
    def set_resolve_imports(self, val):
        self._ri = val
    def _exits(self, imp):
        try:
            exec(imp)
            return True
        except:
            pass
        return False
    def get_content(self):
        content = "\n".join(filter(self._exits, self._varAlloc.allNonResolvedImports))
        txt = self._ri.get_resolved_text()
        withoutImports = ast.unparse(AstTools.remove_imports(ast.parse(txt)))
        res = content + "\n\n" + withoutImports
        return res
    def copy(self):
        jupyterDB.clip().copy(self.get_content())
class ClassOrderMaker:
    def __init__(self):
        self._clssesOrder = None
        self._clsses = None
        self.set_show_annotations()
    def uniqueCheck(self):
        allCls = set()
        for c in self._defs:
            if c.name not in allCls:
                allCls.add(c.name)
            else:
                print(c.name)
    def _map_classes(self, defs):
        clsIndex = {}
        for csls in defs:
            clsIndex[csls.name] = csls
        return clsIndex 
    def _get_all_bases(self, defs):
        clsIndex = set()
        for csls in defs:
            if isinstance(csls, ast.ClassDef):
                for nna in csls.bases:
                    if isinstance(nna, ast.Name):
                        clsIndex.add(nna.id)
        return clsIndex 
    def _ordering(self, x):
        if x in self._clsses:
            return len(self._clsses[x].bases)
        return 0
    def _ordering2(self, x):
        if x in self._clssesOrder:
            return self._ordering(x)
        return 100
    def copy(self):
        self._clssesOrder = sorted(self._get_all_bases(self._defs), key= self._ordering )
        orderedClsses = sorted(self._clsses, key = self._ordering2)
        vals = [self._clsses[k] for k in orderedClsses]
        res = self._imps + vals + self._non_defs
        mod = ast.parse("")
        mod.body = res
        AstTools.assign_parent(mod)
        if self._show_annotation:
            AstTools.remove_annotations(mod)
        jupyterDB.clip().copy(ast.unparse(mod))
    def set_text(self, txt): # containing only classes
        self._text = txt
        self._tree = ast.parse(self._text)
        self._imps, self._defs, self._non_defs = self._bsc.clss.resolver._separate(self._tree)
        self._clsses = self._map_classes(self._defs)
    def set_basic(self, basic):
        self._bsc = basic
    def set_show_annotations(self, show: bool = True):
        self._show_annotation = show
class RenameSameNameClasses:
    def __init__(self) -> None:
        self._new_name = None
        self._allNonResolvedImports =set()
    def _callRename(self, node, loc):
        if isinstance(node, ast.Attribute):
            self._callRename(node.value, self._new_name)
        elif isinstance(node, ast.Call):
            self._callRename(node.func, self._new_name)
        elif isinstance(node, ast.Name):
            node.id = self._new_name
        else:
            print("error a different type of node was detected", node)
    def rename(self):
        from useful.OpsDB import OpsDB
        clsToFiles = OpsDB.group(self._riac._resolved, lambda x: x[1])
        toRename = list(filter(lambda x: len(clsToFiles[x]) > 1, clsToFiles))
        for clsName in toRename:
            files = clsToFiles[clsName]
            for f, clsNa in files:
                self._new_name = AstTools.get_new_name(f, self._bsc._prefix, clsNa)
                self._riac._resolved_tracker[f][clsNa]['<value>'].name = self._new_name
                DicOps.dicIterIter(CentralLocationImports.all_calls[f][clsNa], apply_value_func=self._callRename)
        if None in CentralLocationImports.all_imports:
            DicOps.dicIterIter(CentralLocationImports.all_imports[None], apply_value_func=self._extact_all_non_resolved_imports)
    def set_basic(self, bsc):
        self._bsc = bsc
    def set_resolver(self, riac):
        self._riac = riac
    def _exits(self, imp):
            try:
                exec(imp)
                return True
            except:
                pass
            return False
    def get_content(self):
        content = "\n".join(filter(self._exits, self._allNonResolvedImports))
        txt = self._riac.get_resolved_text()
        withoutImports = ast.unparse(AstTools.remove_imports(ast.parse(txt)))
        res = content + "\n\n" + withoutImports
        return res
    def _extact_all_non_resolved_imports(self, val, loc):
        self._allNonResolvedImports.add(ast.unparse(val))
    def copy(self):
        jupyterDB.clip().copy(self.get_content())
class Main:
    def get_instance(txt = None, prefix = None, path = None):
        if prefix is None:
            from LibPath import getPath
            prefix = getPath()
        bsc = BasicSetters()
        if path:
            bsc.set_file(path.replace(os.sep, "/"))
        if txt:
            bsc.set_content(txt)
        bsc.clss = NameSpace()
        bsc.set_prefix(prefix)
        
        imp_dep = DependencyExtractor()
        bsc.clss.dep = imp_dep
        imp_dep.set_basic(bsc)
        
        # ef = ExtraFunctionality()
        # ef.set_basic(bsc)
        # bsc.clss.ef = ef
        
        resolver = NewResolver()
        resolver.set_basic(bsc)
        bsc.clss.resolver = resolver
        
        ind = Indexing()
        ind.set_basic(bsc)
        bsc.clss.ind = ind
        
        it = ImportsTracker()
        it.set_basic(bsc)
        bsc.clss.it = it
        
        
        return bsc
    def get_explorer(node):
        from modules.code_parser.explorer import Main as MainExp
        exp = MainExp.ast_explorer("")
        exp._exp.set_model(node)
        exp._fill_values()
        return exp
    def resolve(txt = None, prefix = None, path = None):
        bsc = Main.get_instance(txt, prefix = prefix, path = path)
        riac = ResolveImportsAndCalls()
        riac.set_parent(bsc)

        riac.resolve()
        riac._resolve_scope(bsc)
        rsnc = RenameSameNameClasses()
        rsnc.set_basic(bsc)
        rsnc.set_resolver(riac)
        rsnc.rename()
        rsnc.copy()

        co = ClassOrderMaker()
        co.set_basic(bsc)
        co.set_text(rsnc.get_content())
        co.uniqueCheck()
        co.copy()
        print("copied to clipboard")