from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
import ast
import os
from useful.CryptsDB import CryptsDB
from FileDatabase import File
from ListDB import ListDB
from ancient.ClipboardDB import ClipboardDB
from useful.basic import Main as ObjMaker
from timeline.t2023.dep_extractor.dependency_extractor import AstTools, DicOps
class GlobalData:
    all_imports = {}
    all_calls = {}
class ExtractorTool:
    typ = set()
    def iterate(astObj, extractFunc=None, parent=None):
        if extractFunc is None:
            extractFunc = lambda x: x
        skipper = extractFunc(astObj)
        if type(skipper) == bool and skipper:
            return
        if type(astObj) in [set, list]:
            for val in astObj:
                ExtractorTool.iterate(val, extractFunc, parent)
        elif isinstance(astObj, ast.AST):
            astObj._parent = parent
            if type(astObj) not in ExtractorTool.typ:
                ExtractorTool.typ.add(type(astObj))
            for _, val in ast.iter_fields(astObj):
                ExtractorTool.iterate(val, extractFunc, astObj)
        else:
            if type(astObj) in [str, int, bool, float]:
                pass
            elif astObj:
                print(type(astObj), astObj)
    def separate(nodeWithBody):
        defs = []
        nondefs = []
        imps = []
        ExtractorTool.iterate(nodeWithBody)
        for el in nodeWithBody.body:
            if isinstance(el, ast.ClassDef) or isinstance(el, ast.FunctionDef):
                defs.append(el)
            elif isinstance(el, ast.Import) or isinstance(el, ast.ImportFrom):
                imps.append(el)
            else:
                nondefs.append(el)
        return imps, defs, nondefs
    def splitCallAttr(node):
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
    def text_from_nodes(nodes):
        mod = ast.parse("")
        mod.body = nodes
        return ast.unparse(mod)
def DepScope():
    resolver = NewResolver()
    it = ImportsTracker()
    ind = Indexing()
    prefix = None
    filepath = None
    root = None
    def add_to_call(res, loc, node):
        try:
            vals = ListDB.dicOps().get(res, loc)
        except:
            vals = []
            s.handlers.addEventKeyError(res, loc, vals)
        vals.append(node)
    def addEventKeyError(dic, loc, val):
        valT = dic
        lastKey = loc.pop()
        for x in loc:
            n = x
            a = {}
            if type(x) == tuple:
                n,a = x
            if type(valT) == dict and n not in valT:
                valT[n] = {}
            for k in a:
                if "<meta>" not in valT[n]:
                    valT[n]["<meta>"] = {}
                valT[n]["<meta>"][k] = a[k]
            valT = valT[n]
        valT[lastKey] = val
    def set_file(filepath):
        s.process.filepath = filepath
        s.handlers.set_content( File.getFileContent(filepath))
    def set_content(content):
        s.process.content = content
        s.process.lines  = content.splitlines()
        s.process.root = ast.parse(content)
    s = ObjMaker.variablesAndFunction(locals())
    resolver.process.bsc = s
    resolver.process.ce.process.bsc = s
    resolver.handlers.add_to_call = add_to_call
    it.process.bsc = s
    ind.process.bsc = s
    return s
def CallsExtractor():
    resolver_map_tester = {}
    resolver_tracker = set()
    bsc = None
    def call_getter(node):
        if isinstance(node, ast.Call):
            pnode = s.handlers.get_parent_call(node)
            s.process.resolver_map_tester[id(pnode)] = pnode
    def get_parent_call(node):
        s.process.resolver_tracker.add(id(node))
        higest_call = node
        while node._parent:
            if isinstance(node._parent, ast.Call):
                s.process.resolver_tracker.add(id(node._parent))
                higest_call= node._parent
            node = node._parent
            if not isinstance(node, ast.Attribute):
                break
        return higest_call 
    def get_all_calls( node):
        s.process.resolver_map_tester.clear()
        s.process.resolver_tracker.clear()
        AstTools.assign_parent(node)
        ExtractorTool.iterate(node, extractFunc=s.handlers.call_getter)
        return list(s.process.resolver_map_tester.values()) 
    s = ObjMaker.variablesAndFunction(locals())
    return s
def ImportsTracker():
    bsc = None
    temp_result = []
    def get_imports(scope=None):
        if scope is None:
            scope = s.process.bsc.process.root
        s.process.temp_result.clear()
        ExtractorTool.iterate(scope, s.handlers.importFunc)
        return s.process.temp_result.copy()
    def importFunc(astObj):
        if isinstance(astObj, ast.Import) or isinstance(astObj, ast.ImportFrom):
            s.process.temp_result.append(astObj)
    def get_used_imports_in_map(imps):
        used_imports = []
        for im in imps:
            newNames = []
            for name in im.names:
                used_name = name.name
                if name.asname:
                    used_name = name.asname
                if used_name in s.process.bsc.process.resolver.process.all_calls:
                    newNames.append(name)
            if len(newNames):
                newIm = AstTools.copyFuncOrClassDef(im)
                newIm.lineno = im.lineno
                newIm.names = newNames
                newIm._parent = im._parent
                used_imports.append(newIm)
                s.handlers.index_import(newIm, newNames)
        return used_imports
    def index_import(im, usedNames):
        bsc = s.process.bsc
        for nn in usedNames:
            filepath = bsc.process.it.handlers.get_file_path_from_import(im)
            try:
                locs = ListDB.dicOps().get(GlobalData.all_imports, [filepath, nn.name])
            except:
                locs = {}
                DicOps.addEventKeyError(GlobalData.all_imports, [filepath, nn.name], locs)
            if (bsc.process.filepath, im.lineno) not in locs:
                locs[(bsc.process.filepath, im.lineno)] = im
    def get_file_path_from_import(im):
        if isinstance(im, ast.Import):
            return None
        file = s.process.bsc.process.prefix.replace(os.sep,"/") + "/" + im.module.replace(".", "/") + ".py"
        initPath = s.process.bsc.process.prefix.replace(os.sep,"/") + "/" + im.module.replace(".", "/") + "/__init__.py" 
        if os.path.exists(file):
            return file
        elif os.path.exists(initPath):
            return initPath
        if s.process.bsc.process.filepath and im.level > 0:
            fileFolder = os.path.dirname(s.process.bsc.process.filepath)
            lvl = im.level -1
            while lvl > 0:
                fileFolder = os.path.dirname(fileFolder)
                lvl -= 1    
            file = fileFolder + "/" + im.module.replace(".", "/") + ".py"
            if os.path.exists(file):
                return file
        return None
    def paths_with_classes(imports):
        fileWithClasses = {}
        for im in imports:
            path = s.handlers.get_file_path_from_import(im)
            s.handlers.add_to_path(path, fileWithClasses, im)
        return fileWithClasses
    def add_to_path(path, dic, im):
        if path not in dic:
            dic[path] = []
        for n in im.names:
            dic[path].append((n.name, n.asname, im))
    s = ObjMaker.variablesAndFunction(locals())
    return s
def ScopeStorer():
    defs = []
    imports = []
    used_imports = []
    all_calls = []
    exps = []
    def save_scope(resolver):
        s.process.defs.append(resolver.process.defs)
        s.process.imports.append(resolver.process.imports)
        s.process.used_imports.append(resolver.process.used_imports)
        s.process.all_calls.append(resolver.process.all_calls)
        s.process.exps.append(resolver.process.exps)
    def pop_scope(resolver):
        if len(s.process.defs) > 0:
            resolver.process.defs = s.process.defs.pop()
            resolver.process.imports = s.process.imports.pop()
            resolver.process.used_imports = s.process.used_imports.pop()
            resolver.process.all_calls = s.process.all_calls.pop()
            resolver.process.exps = s.process.exps.pop()
    s = ObjMaker.variablesAndFunction(locals())
    return s
def ResolveImportsAndCalls():
    resolved_tracker = {}
    instance_tracker = {}
    resolved = []
    scope_storer = ScopeStorer()
    def add_functions(child, funcs, clsName):
        rt = s.process.resolved_tracker
        
        path = child.process.filepath 
        indices = child.process.ind.handlers.index()
        clssFuncs = indices[path][clsName].keys()
        non_deprecated_funcs = []
        for f in funcs:
            if f in clssFuncs:
                non_deprecated_funcs.append(f)
            else:
                print(f"class {clsName} does not have {f} anymore")

        previousFuncs = ListDB.dicOps().get(rt, [path, clsName,'<method>'])
        clsNode  = ListDB.dicOps().get(rt, [path, clsName,'<value>'])
        for f in non_deprecated_funcs:
            clsNode.body.append(indices[path][clsName][f]['<value>'])
            previousFuncs.append(f)
        
        node = AstTools.copyFuncOrClassDef(clsNode)
        nb = [indices[path][clsName][k]['<value>'] for k in non_deprecated_funcs]
        node.body = nb
        return node
    def get_current_call(bsca, clsName, asName):
        if asName:
            val = bsca.process.resolver.process.all_calls[asName]
        else:
            val = bsca.process.resolver.process.all_calls[clsName]
        return val
    def get_functions(bsca, clsName, asName):
        val = s.handlers.get_current_call(bsca, clsName=clsName, asName=asName)
        funcs = []
        keyToIgnore = set(["<meta>", "<value>"])
        if isinstance(val, dict):
            funcs = [k for k in val if k not in keyToIgnore]
        return funcs
    def add_new_node(child, toRe, clsName):
        rt = s.process.resolved_tracker
        
        if isinstance(toRe, ast.ClassDef):
            toRe2 = AstTools.copyFuncOrClassDef(toRe)
            toRe2.body = [ep for ep in toRe.body if not isinstance(ep, ast.FunctionDef)]
            toRe2.lineno = toRe.lineno
        else:
            toRe2 = toRe
        DicOps.addEventKeyError(rt, [child.process.filepath, clsName,'<value>'], toRe2)
        DicOps.addEventKeyError(rt, [child.process.filepath, clsName,'<method>'], [])
        if (child.process.filepath, clsName) not in s.process.resolved:
            s.process.added = True
            s.process.resolved.append((child.process.filepath, clsName))
    def filter_out_imported_funcs(bsca, clsName, funcs):
        previ = ListDB.dicOps().get(s.process.resolved_tracker, [bsca.process.filepath, clsName,'<method>'])
        newfuncs = []
        for f in funcs:
            if f not in previ:
                newfuncs.append(f)
        return newfuncs
    def exists(bsca, clsName):
        try:
            ListDB.dicOps().get(s.process.resolved_tracker, [bsca.process.filepath, clsName,'<value>'])
            return True
        except:
            pass
        return False
    def update_for_instance(node, path, clsName):
        rt = s.process.resolved_tracker
        previousFuncs = ListDB.dicOps().get(rt, [path, clsName,'<method>'])
        clsNode  = ListDB.dicOps().get(rt, [path, clsName,'<value>'])
        for f in node.body:
            if isinstance(f, ast.FunctionDef):
                has_self_parameter = any(param.arg == 'self' for param in f.args.args)
                if has_self_parameter and f.name not in previousFuncs:
                    clsNode.body.append(f)
                    previousFuncs.append(f.name)
    def extractFuncs(parent, clsName, asName, child):
        indices = child.process.ind.handlers.index()
        toReClsass = indices[child.process.filepath][clsName]['<value>']
        s.process.added = False
        if not s.handlers.exists(child, clsName):
            s.handlers.add_new_node(child, toReClsass, clsName)
        funcs = s.handlers.get_functions(parent, clsName, asName)
        val = s.handlers.get_current_call(parent, clsName=clsName, asName=asName)
        if  val["<meta>"]["is_call"]:
            s.handlers.update_for_instance(toReClsass, child.process.filepath, clsName)
        newfuns = s.handlers.filter_out_imported_funcs(child, clsName, funcs)
        if len(newfuns) == 0:
            if s.process.added:
                return s.process.added, toReClsass
            return False, None
        node = s.handlers.add_functions(child, newfuns, clsName)
        return True, node
    def _resolve(bsca, scope=None):
        if scope is None:
            bsca.process.resolver.handlers.parse()
        pathsWith = bsca.process.it.handlers.paths_with_classes(bsca.process.resolver.process.used_imports)
        for path in pathsWith:
            if path is None: continue
            lowInstance = s.handlers.get_instance(path)
            for clsName, asName, im in pathsWith[path]:
                s.handlers.log_calls(lowInstance, bsca, clsName, asName)
                added, scope = s.handlers.extractFuncs(bsca, clsName, asName, lowInstance)
                if added:
                    s.handlers.save_scope_resolve(lowInstance, scope)
    def log_calls(_from, to, clsName, asName):
        from_path = _from.process.filepath
        to_path = to.process.filepath
        if from_path not in GlobalData.all_calls:
            GlobalData.all_calls[from_path] = {}
        if clsName not in GlobalData.all_calls[from_path]:
            GlobalData.all_calls[from_path][clsName] = {}
        val = s.handlers.get_current_call(to, clsName=clsName, asName=asName)
        dic = GlobalData.all_calls[from_path][clsName]
        if to_path not in dic:
            dic[to_path] = {}
        s.handlers.update_dic(dic[to_path], val)
    def update_dic(dicA, dicB):
        for k in dicB:
            if k not in dicA: 
                dicA[k] = dicB[k]
                continue
            val = dicB[k]
            if isinstance(val, dict):
                update_dic(dicA[k], dicB[k])
            elif isinstance(val, list):
                for el in val:
                    if el not in dicA[k]:
                        dicA[k].append(el)
            else:
                if type(val) not in [bool]:
                    print("different", val)
    def save_scope_resolve(child, scope):
        ss = s.process.scope_storer
        scouped = False
        if hasattr(child.process.resolver.process, "defs"):
            scouped = True
            ss.handlers.save_scope(child.process.resolver)
        child.process.resolver.handlers.parse_body(scope)
        s.handlers._resolve(child, scope)
        s.handlers.resolve_scope(child)
        if scouped:
            ss.handlers.pop_scope(child.process.resolver)
    def resolve_scope(child):
        indices = child.process.ind.handlers.index()
        if child.process.filepath in indices: 
            indices = indices[child.process.filepath]
        for usedName in indices:
            if usedName in child.process.resolver.process.all_calls:
                s.handlers.log_calls(child, child, usedName, usedName)
                added, scope = s.handlers.extractFuncs(child, usedName, None, child)
                if added:
                    s.handlers.save_scope_resolve(child, scope)
    def resolve():
        GlobalData.all_imports.clear()
        GlobalData.all_calls.clear()
        s.process.resolved.clear()
        s.process.resolved_tracker.clear()
        s.handlers._resolve(s.process.bsc)
    def get_instance(path):
        if path not in s.process.instance_tracker: 
            ins = DepScope()
            ins.process.prefix = s.process.bsc.process.prefix
            ins.handlers.set_file(path.replace(os.sep, "/"))
            s.process.instance_tracker[path] = ins
        return s.process.instance_tracker[path]
    def copy_to_clipboard():
        ClipboardDB.copy2clipboard(s.handlers.get_resolved_text())
    def get_resolved_text():
        body = []
        done= set()
        for ke in s.process.resolved[::-1]:	
            if ke not in done:
                body.append(ListDB.dicOps().get(s.process.resolved_tracker, list(ke) + ["<value>"]))
                done.add(ke)
        return ast.unparse(body + s.process.bsc.process.resolver.handlers.get_first_layer())
    s = ObjMaker.variablesAndFunction(locals())
    return s
def NewResolver():
    ce = CallsExtractor()
    bsc = None
    exps = None
    def get_all_calls(nodeL, res = None):
        ce = s.process.ce
        calls = ce.handlers.get_all_calls(nodeL)
        if res is None:
            res = {}
        for node in calls:
            txloc = ExtractorTool.splitCallAttr(node)
            txloc.append('<value>')
            s.handlers.add_to_call(res, txloc, node)
        return res
    def add_to_call(res, loc, node):
        try:
            vals = ListDB.dicOps().get(res, loc)
        except:
            vals = []
            DicOps.addEventKeyError(res, loc, vals)
        vals.append(node)
    def get_all_uses(node, res = None):
        if res is None:
            res = {}
        s.handlers.get_all_calls(node, res)
        def coll(dic, node):
            for n in node.bases:
                if isinstance(n, ast.Name):
                    txloc = [(n.id, {"is_call": True}),'<value>']
                    s.handlers.add_to_call(res, txloc, n)
                else:
                    print(ast.unparse(n))
        s.handlers.get_any(node, res, conditions= [lambda node, res: isinstance(node, ast.ClassDef) and node.bases],
                      collector=coll)
        return res
    def all_names(nodeL,  res = None):
        if res is None:
            res = {}
        for node in ast.walk(nodeL):
            if isinstance(node, ast.Name):
                if node.id not in res:
                    res[node.id] = node
        return res
    def get_any(nodeL, res=None, conditions = None, collector = None):
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
    def bases_and_anno(nodeL, res = None):
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
    def parse_body(objWithBody):
        s.handlers.parse()
        _, _ , s.process.exps = ExtractorTool.separate(objWithBody)
        s.process.all_calls = s.handlers.get_all_uses(objWithBody)
        s.process.used_imports = s.process.bsc.process.it.handlers.get_used_imports_in_map(s.process.imports)
    def parse():
        s.process.imports = s.process.bsc.process.it.handlers.get_imports()
        _, s.process.defs, s.process.exps = ExtractorTool.separate(s.process.bsc.process.root)
        s.process.all_calls = s.handlers.get_all_uses(s.process.bsc.process.root)
        s.process.used_imports = s.process.bsc.process.it.handlers.get_used_imports_in_map(s.process.imports)
    def get_first_layer():
        if s.process.exps is None:
            s.handlers.parse()
        return s.process.exps
    s = ObjMaker.variablesAndFunction(locals())
    return s
def Indexing():
    indices = {}
    import_dic = {}
    def make_parent_tuple(node, loc=None):
        bsc = s.process.bsc
        if loc is None:
            loc =  []
        if node:
            if hasattr(node, "name"):
                name = node.name
            elif hasattr(bsc.process, "filepath") and bsc.process.filepath: 
                name = bsc.process.filepath
            else:
                name = None
            loc.append(name)
            make_parent_tuple(node._parent, loc)
        return loc[::-1]
    def create_node(node):
        loc = s.handlers.make_parent_tuple(node)
        DicOps.addEventKeyError(s.process.indices, loc + ["<value>"], node)
    def collector(x):
        if isinstance(x, ast.ClassDef) or isinstance(x, ast.FunctionDef):
            s.handlers.create_node(x)
        elif isinstance(x,ast.Import) or isinstance(x, ast.ImportFrom):
            lien = ast.unparse(x)
            if lien not in s.process.import_dic:
                s.process.import_dic[lien] = x
    def index():
        ind = s.process.indices
        if len(ind):
            return ind
        ind.clear()
        s.process.import_dic.clear()
        ExtractorTool.iterate(s.process.bsc.process.root)
        ExtractorTool.iterate(s.process.bsc.process.root, s.handlers.collector)
        return ind
    s = ObjMaker.variablesAndFunction(locals())
    return s
def ClassOrderMaker():
    clssesOrder = None
    clsses = None
    show_annotation = True
    def uniqueCheck():
        allCls = set()
        for c in s.process.defs:
            if c.name not in allCls:
                allCls.add(c.name)
            else:
                print(c.name)
    def map_classes(defs):
        clsIndex = {}
        for csls in defs:
            clsIndex[csls.name] = csls
        return clsIndex 
    def get_all_bases(defs):
        clsIndex = set()
        for csls in defs:
            if isinstance(csls, ast.ClassDef):
                for nna in csls.bases:
                    if isinstance(nna, ast.Name):
                        clsIndex.add(nna.id)
        return clsIndex 
    def ordering(x):
        if x in s.process.clsses:
            return len(s.process.clsses[x].bases)
        return 0
    def ordering2(x):
        if x in s.process.clssesOrder:
            return s.handlers.ordering(x)
        return 100
    def get_text():
        s.process.clssesOrder = sorted(s.handlers.get_all_bases(s.process.defs), key= s.handlers.ordering )
        orderedClsses = sorted(s.process.clsses, key = s.handlers.ordering2)
        vals = [s.process.clsses[k] for k in orderedClsses]
        res = s.process.imps + vals + s.process.non_defs
        s.process.vals = vals
        mod = ast.parse("")
        mod.body = res
        AstTools.assign_parent(mod)
        if s.process.show_annotation:
            AstTools.remove_annotations(mod)
        return ast.unparse(mod)
    def copy():
        ClipboardDB.copy2clipboard(s.handlers.get_text())
    def set_text(txt): # containing only classes
        s.process.text = txt
        s.process.tree = ast.parse(txt)
        resolr = s.process.bsc.process.resolver
        s.process.imps, s.process.defs, s.process.non_defs = ExtractorTool.separate(s.process.tree)
        s.process.clsses = s.handlers.map_classes(s.process.defs)
    s = ObjMaker.variablesAndFunction(locals())
    return s
def RenameSameNameClasses():
    new_name = None
    allNonResolvedImports =set()
    riac = None
    def callRename(node, loc):
        if isinstance(node, ast.Attribute):
            callRename(node.value, s.process.new_name)
        elif isinstance(node, ast.Call):
            callRename(node.func, s.process.new_name)
        elif isinstance(node, ast.Name):
            node.id = s.process.new_name
        else:
            print("error a different type of node was detected", node)
    def rename():
        from OpsDB import OpsDB
        clsToFiles = OpsDB.group(s.process.riac.process.resolved, lambda x: x[1])
        toRename = list(filter(lambda x: len(clsToFiles[x]) > 1, clsToFiles))
        for clsName in toRename:
            files = clsToFiles[clsName]
            for f, clsNa in files:
                s.process.new_name = AstTools.get_new_name(f, s.process.bsc.process.prefix, clsNa)
                s.process.riac.process.resolved_tracker[f][clsNa]['<value>'].name = s.process.new_name
                DicOps.dicIterIter(GlobalData.all_calls[f][clsNa], apply_value_func=s.handlers.callRename)
        if None in GlobalData.all_imports:
            DicOps.dicIterIter(GlobalData.all_imports[None], apply_value_func=s.handlers.extact_all_non_resolved_imports)
    def exits(imp):
        try:
            exec(imp)
            return True
        except:
            pass
        return False
    def get_content():
        content = "\n".join(filter(s.handlers.exits, s.process.allNonResolvedImports))
        txt = s.process.riac.handlers.get_resolved_text()
        withoutImports = ast.unparse(AstTools.remove_imports(ast.parse(txt)))
        res = content + "\n\n" + withoutImports
        return res
    def extact_all_non_resolved_imports(val, loc):
        s.process.allNonResolvedImports.add(ast.unparse(val))
    def copy():
        ClipboardDB.copy2clipboard(s.handlers.get_content())
    s = ObjMaker.variablesAndFunction(locals())
    return s
def DepExtractor():
    def resolve(text=None, path =None, prefix = None):
        co = s.handlers._resolve(text,path,prefix)
        toResolveText = co.handlers.get_text()
        tsi = len(toResolveText)
        # while True:
        #     toResolveText = s.handlers._resolve(toResolveText, None, prefix).handlers.get_text()
        #     if len(toResolveText) >= tsi:
        #         break
        #     tsi = len(toResolveText)
        toResolveText = s.handlers._resolve(toResolveText, None, prefix).handlers.get_text()
        ClipboardDB.copy2clipboard(toResolveText)
        print("copied to clipboard")
    def _resolve(text=None, path =None, prefix = None):
        riac = ResolveImportsAndCalls()
        rsnc = RenameSameNameClasses()
        co = ClassOrderMaker()
        bsc = DepScope()
        rsnc.process.riac = riac
        riac.process.bsc = bsc
        rsnc.process.bsc = bsc
        co.process.bsc = bsc 
        
        bsc.process.prefix = prefix
        if path is not None:
            bsc.handlers.set_file(path.replace(os.sep, "/"))
        elif text is not None:
            bsc.handlers.set_content(text)
        riac.handlers.resolve()
        riac.handlers.resolve_scope(bsc)
        rsnc.handlers.rename()
        co.handlers.set_text(rsnc.handlers.get_content())
        co.handlers.uniqueCheck()
        return co
    def tempFile(content):
        name = f"py{CryptsDB.generateUniqueId()}.py"
        File.createFile(name, content)
        return name
    s = ObjMaker.variablesAndFunction(locals())
    return s