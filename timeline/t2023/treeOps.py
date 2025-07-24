from modules.GUIs.PickleOps import PickleOpsModel
from ListDB import ListDB
import ipywidgets as widgets
from useful.basic import NameSpace

class StringInfoEnums:
    LAST_DIR_LIST = "treeList"
    EXTRA_INFO = "extraInfoInName"
    LOCATION = "location"
    LAST_COMMAND = "last command"
    OPS_LOC = "opsLoc"
    DEPTH = "depth"
    ADD = "add"
class NodeExplorer:
    def __init__(self):
        self._loc = []
        self._root = self._make_node("root")
        self._loc_node = [self._root]
        self._version = 0
    def goback(self):
        if len(self._loc_node) > 1:
            self._loc.pop()
            self._loc_node.pop()
    def goForward(self, key):
        self._loc.append(key)
        cur = self._loc_node[-1]
        child = cur.children[key]
        self._loc_node.append(child)
    def delete(self, key):
        cur = self._loc_node[-1]
        del cur.children[key]
        self._version += 1
    def getKeys(self):
        cur = self._loc_node[-1]
        return list(cur.children.keys())
    def value(self):
        if len(self._loc_node) == 0:
            node = self._root
        else:
            node = self._loc_node[-1]
        return self._ge_val(node)
    def _ge_val(self, node):
        res = {}
        for key in node.children:
            res[key] = self._ge_val(node.children[key])
        return res
    def alreadyExists(self, key):
        cur = self._loc_node[-1]
        return key in cur.children
    def add(self, key, val):
        cur = self._loc_node[-1]
        node = self._make_node(key)
        node.value = val
        node.parent = cur
        cur.children[key] = node
        self._version += 1
    def _make_node(self, key):
        node = NameSpace()
        node.key = key 
        node.children = {}
        return node
    def loadFile(self, file):
        pass
class PickleModelWrapper:
    def __init__(self):
        self._pcrud = PickleOpsModel()
        self.set_base_location([])
    def set_base_location(self, base_loc: list):
        self._basepath = base_loc 
        self._pcrud._loc = base_loc
    def reset_to_baseloc(self):
        self.set_base_location(self._basepath)
    def dirList(self):
        pass
class DynamicTreeRenderer:
    def __init__(self):
        self._loc = []
        self._temp = None
    def set_loc_appender(self, func):
        self._location_appender = func
    def set_dic(self, dic):
        self._model = {"root": dic}
        self.set_dir_checker(lambda x: type(ListDB.dicOps().get(self._model, self._loc + [x])) in [dict, list])
        self.set_name_getter(lambda i, x: x)
        self.set_children_getter(self._dic_child_getter_default)
        self.set_loc_appender(lambda ctx, x: ctx._loc.append(x))
        self._temp = "root"
    def _dic_child_getter_default(self, x):
        val = ListDB.dicOps().get(self._model, self._loc)
        if type(val) in [list, set]:
            return val
        elif type(val) == dict:
            return list(val.keys())
        return []
    def set_dir_checker(self, func):
        self._dir_checker = func
    def set_name_getter(self, func):
        self._name_getter = func
    def set_children_getter(self, func):
        self._child_getter = func
    def getAsText(self):
        return "\n".join(self._tree(self._temp)) 
    def _tree(self,dir_path , prefix: str='', lyr = 0):
        self._location_appender(self, dir_path)
        space =  '    '
        branch = '│   '
        tee =    '├── '
        last =   '└── '
        contents = self._child_getter(dir_path)
        pointers = [tee] * (len(contents) - 1) + [last]
        for i, (pointer, path) in enumerate(zip(pointers, contents)):
            yield prefix + pointer + self._name_getter(i, path)
            if lyr < self._depth and self._dir_checker(path):
                extension = branch if pointer == tee else space
                yield from self._tree(path, prefix=prefix+extension, lyr=lyr+1)
        if len(self._loc) > 0:
            self._loc.pop()
    def set_root_node_of_a_tree(self, root):
        self._model = root
        self.set_dir_checker(lambda x: x.children != 0)
        self.set_name_getter(lambda i, x: x)
        self.set_children_getter(lambda x: list(x.children.keys()))
        self.set_loc_appender(lambda ctx, x: ctx._loc.append(x))
        self._temp = self._model
    def set_list(self, data):
        self._model = data
        self.set_dir_checker(lambda x: False)
        self.set_name_getter(lambda i, x: str(x))
        self.set_children_getter(lambda x: self._model)
        self.set_loc_appender(lambda ctx, x: ctx._loc.append(x))
        self.set_depth_level(1)
        self._temp = self._model
    def set_depth_level(self, lvl):
        self._depth = lvl
class TreeViewIpyWidget:
    def __init__(self):
        self.txtArea = widgets.Textarea(layout={"width":"auto", "height":"300px"}, disabled=True)
        self.inpSection = widgets.Text(placeholder="enter your command (type h for help) enter to run")
        self.out = widgets.Output()
        self.layout = widgets.VBox([self.txtArea, self.inpSection,self.out])
class BasicController:
    def set_model(self, model):
        self._model = model
    def set_displayer(self, displayer):
        self._displayer = displayer
    def set_view(self, view):
        self._view = view
    def set_tree_renderer(self, ren):
        self._renderer = ren
class TreeOpsController:
    def __init__(self):
        self._ops = {}
        self._infos = {}
        self._ops_desc ={}
        self.set_user_input_func(self._default_user_input)
        self._history = []
        self.set_call(self._def_call)
    def set_call(self, func):
        self._call = func
    def _default_user_input(self, param):
        res = self._bsc._view.inpSection.value.split(" ")
        return " ".join(res[1:])
    def set_basic_controller(self, cont):
        self._bsc = cont
    def add_ops(self, opKey, opsFunc, description=""):
        self._ops[opKey] = opsFunc
        self._ops_desc[opKey] = description
    def call(self, opsKey):
        self._call(opsKey, self)
    def _def_call(self, opsKe, cnt):
        func = self._ops[opsKe]
        self._bsc._view.out.clear_output()
        with self._bsc._view.out:
            func(self)
        self.set_info(StringInfoEnums.LAST_COMMAND, opsKe)
    def set_up(self):
        self._bsc._view.inpSection.observe(self._bsc.controllers.views.input.wrapper_func, "value")
        self._bsc._view.inpSection.continuous_update = False
    def def_entered(self, wid):
        content = self._bsc._view.inpSection.value.strip()
        if len(content) == 0:
            return
        self._history.append(content)
        x = content.split(" ")
        if x[0] in self._ops:
            self.call(x[0])
        elif len(x) != 0:
            self.call(StringInfoEnums.ADD)
        self._bsc._view.inpSection.value = ""
    def get_user_input(self):
        return self._ufunc(self)
    def set_user_input_func(self, func):
        self._ufunc = func
    def set_info(self, key, value):
        self._infos[key] = value
class ExtraInfoOps:
    def helpUs(cnt):
        infos = {}
        txt = ""
        for i, op in enumerate(cnt._ops_desc):
            infos[i+1] = op
            txt += f"{i+1}. {op} -> {cnt._ops_desc[op]}\n"
        cnt._bsc._view.txtArea.value = txt
        cnt.set_info(StringInfoEnums.OPS_LOC, infos)
    def depth(cnt):
        val = int(cnt.get_user_input())
        cnt._bsc._renderer.set_depth_level(val)
        cnt.set_info(StringInfoEnums.DEPTH, val)
        SingleTreeOps.readAll(cnt)
    def enumeratee(cnt):
        cnt.set_info(StringInfoEnums.EXTRA_INFO, lambda i, x: f"{i+1}. {x}")
        SingleTreeOps.readAll(cnt)
    def childNrs(cnt):
        dcc = cnt._bsc.controllers.dcc
        dcc.set_update_function(dcc.update_children_count)
        dcc._data_nr = None
        cnt._bsc.controllers.toc.set_info(StringInfoEnums.EXTRA_INFO, dcc._child_nr_name_getter)
    def depthCountInfo(cnt):
        dcc = cnt._bsc.controllers.dcc
        dcc.set_update_function(dcc.update_max_depth_count)
        dcc._data_nr = None
        cnt._bsc.controllers.toc.set_info(StringInfoEnums.EXTRA_INFO, dcc._max_name_getter)
    def noInfo(cnt):
        cnt.set_info(StringInfoEnums.EXTRA_INFO, lambda i, x: x)
        SingleTreeOps.readAll(cnt)
    def lastNCommands(cnt):
        cnt._bsc._view.txtArea.value = "\n".join(cnt._history[-10:])
    def operatorSelector(cnt):
        if StringInfoEnums.OPS_LOC not in cnt._infos:
            ExtraInfoOps.helpUs(cnt)
        ops = cnt._infos[StringInfoEnums.OPS_LOC]
        if ops != ExtraInfoOps.operatorSelector:
            val = cnt.get_user_input().split(" ")
            x = " ".join(val[1:])
            cnt.set_user_input_func(lambda y: x)
            try:
                cnt.call(ops[int(val[0])])
            finally:
                cnt.set_user_input_func(cnt._default_user_input)
    def open_folder_here(cnt):
        pass
class SingleTreeOps:
    def treeReadAll(cnt):
        cnt._bsc._model._loc.clear()
        tr = cnt._bsc._renderer
        teree = cnt._bsc._model.getKeys()
        cnt.set_info(StringInfoEnums.LAST_DIR_LIST, teree)
        tr.set_list(teree)
        if StringInfoEnums.EXTRA_INFO in cnt._infos:
            tr.set_name_getter(cnt._infos[StringInfoEnums.EXTRA_INFO])
        cnt._bsc._view.txtArea.value = tr.getAsText()
        if StringInfoEnums.DEPTH in cnt._infos:
            tr.set_depth_level(cnt._infos[StringInfoEnums.DEPTH])
    def addNode(cnt):
        inp = cnt._bsc._view.inpSection.value.strip()
        words = inp.split()
        if words[0] == "add":
            inp = cnt.get_user_input()
        name = inp.strip()
        if not cnt._bsc._model.alreadyExists( name ):
            cnt._bsc._model.add(name, {})
        SingleTreeOps.readAll(cnt)      
    def readAll(cnt):
        if StringInfoEnums.LOCATION not in cnt._infos:
            cnt._infos[StringInfoEnums.LOCATION] = []
        if len(cnt._infos[StringInfoEnums.LOCATION]) == 0:
            SingleTreeOps.treeReadAll(cnt)
            return
        tn = cnt._infos[StringInfoEnums.LOCATION][-1]
        tr = cnt._bsc._renderer
        vals = cnt._bsc._model.value()
        cnt.set_info(StringInfoEnums.LAST_DIR_LIST, list(vals.keys()))
        tr.set_dic(vals)
        if StringInfoEnums.EXTRA_INFO in cnt._infos:
            tr.set_name_getter(cnt._infos[StringInfoEnums.EXTRA_INFO])
        if StringInfoEnums.DEPTH in cnt._infos:
            tr.set_depth_level(cnt._infos[StringInfoEnums.DEPTH])
        cnt._bsc._view.txtArea.value = tn + "\n" + tr.getAsText()
    def cdToNode(cnt):
        key = cnt.get_user_input()
        if key.strip() == "..":
            cnt._bsc._model.goback()
            if len(cnt._infos[StringInfoEnums.LOCATION]):
                cnt._infos[StringInfoEnums.LOCATION].pop()
            SingleTreeOps.readAll(cnt)
            return
        index = int(key)-1
        nnae = cnt._infos[StringInfoEnums.LAST_DIR_LIST][index]
        cnt._bsc._model.goForward(nnae)
        cnt._infos[StringInfoEnums.LOCATION].append(nnae)
        SingleTreeOps.readAll(cnt)
    def delNode(cnt):
        key = cnt.get_user_input()
        index = int(key)-1
        vla = cnt._infos[StringInfoEnums.LAST_DIR_LIST][index]
        cnt._bsc._model.delete(vla)
        SingleTreeOps.readAll(cnt)
class DeepCopier:
    def for_dict(dic):
        newDic = {}
        for ke in dic:
            val = dic[ke]
            if type(val) == list:
                newDic[ke] = DeepCopier.for_list(val)
            elif type(val) == dict:
                newDic[ke] = DeepCopier.for_dict(val)
            else:
                newDic[ke] = val
        return newDic
    def for_list(arr):
        newArr = []
        for ele in arr:
            if type(ele) == list:
                newArr.append(DeepCopier.for_list(ele))
            elif type(ele) == dict:
                newArr.append(DeepCopier.for_dict(ele))
            else:
                newArr.append(ele)
        return newArr
class CutPasteOps:
    def _mmgr(inp):
        vals = list(map(int, inp.strip().split("-")))
        if len(vals) == 2:
            vals = list(range(vals[0], vals[1]+1))
        return vals
    def _get_input(cnt):
        inp = cnt.get_user_input().strip().strip(",").strip()
        res = []
        imm = inp.split(",")
        for e in imm:
            res += CutPasteOps._mmgr(e)
        return res
    def _goAhead(cnt):
        if "Cut" in cnt._infos:
            values = cnt._infos["Cut"]
            for loc in values:
                val = values[loc]
                if len(val) != 0:
                    print("You have some keys in the clipboard. You need to paste them somewhere")
                    return False
        return True
    def cut(cnt):
        if not CutPasteOps._goAhead(cnt):
            return 
        lco = tuple(cnt._bsc._model._loc)
        temp = {lco:{}}
        inx = CutPasteOps._get_input(cnt)
        allCn = cnt._bsc._model.value()
        for i in inx:
            key = cnt._infos[StringInfoEnums.LAST_DIR_LIST][i-1]
            value = DeepCopier.for_dict(allCn[key])
            temp[lco][key] = value
            cnt._bsc._model.delete(key)
        cnt.set_info("Cut", temp)
        SingleTreeOps.readAll(cnt)
    def paste(cnt):
        values = cnt._infos["Cut"]
        added = []
        for loc in values:
            vls = values[loc]
            for ke in vls:
                val = vls[ke]
                if not cnt._bsc._model.alreadyExists(ke):
                    cnt._bsc._model.add(ke, val)
                    added.append((loc, ke))
                else:
                    print(ke, "key already exists")
        for loc, k in added:
            del values[loc][k]
        cnt.set_info("Cut", values)
        SingleTreeOps.readAll(cnt)
class DepthChildCount:
    def __init__(self):
        self._data_nr = None
        self.set_update_function(self.update_children_count)
    def before_call(self, opsKey, cnt):
        if self._data_nr != cnt._bsc._model._version:
            self._update_func(cnt._bsc._model._root)
            self._data_nr = cnt._bsc._model._version
    def after_call(self, opsKey, cnt):
        pass
    def new_call(self, opsKey, cnt):
        self.before_call(opsKey, cnt)
        cnt._def_call(opsKey, cnt)
        self.after_call(opsKey, cnt)
    def update_children_count(self, node):
        ch = node.children
        if len(ch) == 0:
            node.children_number = 1
            return node.children_number
        node.children_number = sum([self.update_children_count(ch[n]) for n in ch])
        return node.children_number
    def update_max_depth_count(self, node):
        if len(node.children) == 0:
            node.max_depth = 0
            return 0
        depths = []
        for key in node.children:
            child = node.children[key]
            child.max_depth = self.update_max_depth_count(child)
            depths.append(child.max_depth)
        return max(depths) + 1
    def set_update_function(self, func):
        self._update_func = func
    def _max_name_getter(self, index, key):
        node = self._get_cur_node()
        node = node.children[key]
        if hasattr(node, "max_depth"):
            return f"{index+1}. {key} - {node.max_depth}"
        return f"{index+1}. {key} - 0"
    def _child_nr_name_getter(self, index, key):
        node = self._get_cur_node()
        node = node.children[key]
        if hasattr(node, "children_number"):
            return f"{index+1}. {key} - {node.children_number}"
        return f"{index+1}. {key} - 0"
    def set_basic_controller(self, bsc):
        self._bsc = bsc
    def _get_cur_node(self):
        node = self._bsc._model._root
        for ke in self._bsc._model._loc + self._bsc._renderer._loc[1:]:
            node = node.children[ke]
        return node
class Main:
    def runWithDic(dic):
        toc = TreeOpsController()
        bsc = BasicController()
        bsc.set_tree_renderer(DynamicTreeRenderer())
        view = TreeViewIpyWidget()
        bsc.set_view(view)
        toc.set_basic_controller(bsc)
        tm = PickleOpsModel()
        tm.set_dictionary(dic)
        bsc.set_model(tm)
        
        bsc.controllers = NameSpace()
        bsc.controllers.toc = toc
        
        Main.add_namespace(bsc)
        
        toc.set_up()
        toc.add_ops(StringInfoEnums.ADD, SingleTreeOps.addNode, "add a new node")
        toc.add_ops("del", SingleTreeOps.delNode, "delete an existing node")
        toc.add_ops("ls", SingleTreeOps.readAll, "show tree")
        toc.add_ops("cd", SingleTreeOps.cdToNode, "go to the node")
        toc.add_ops("so", ExtraInfoOps.operatorSelector, "run the operator by using a number")
        toc.add_ops("enum", ExtraInfoOps.enumeratee, "enumerate the listing")
        toc.add_ops("depth", ExtraInfoOps.depth, "set depth level")
        toc.add_ops("no", ExtraInfoOps.noInfo, "hide info from listing")
        toc.add_ops("h", ExtraInfoOps.helpUs, "show the list of all the operations and their keys")
        toc.add_ops("here", ExtraInfoOps.open_folder_here, "open folder at current location of the tree")
        toc.add_ops("cut", CutPasteOps.cut, "cut nodes like 1,2-4,6,7-10")
        toc.add_ops("paste", CutPasteOps.paste, "paste the nodes in the clipboard")
        toc.add_ops("his", ExtraInfoOps.lastNCommands, "show last 10 history")
        toc.add_ops("md", ExtraInfoOps.depthCountInfo, "max depth")
        toc.add_ops("chno", ExtraInfoOps.childNrs, "number of childs")
        
        ExtraInfoOps.enumeratee(toc)
        
        return bsc
    def add_namespace(bsc):
        bsc.controllers.views = NameSpace()
        bsc.controllers.views.input = NameSpace()
        bsc.controllers.views.input.wrapper_func = lambda wid: bsc.controllers.views.input.entered_func(wid)
        bsc.controllers.views.input.default_entered_func = bsc.controllers.toc.def_entered
        bsc.controllers.views.input.entered_func = bsc.controllers.views.input.default_entered_func
    def runWithFile(filepath):
        bsc = Main.runWithDic({})
        bsc._model.loadFile(filepath)
        return bsc
    def runWithNode(dic=None, filepath=None):
        if dic is None:
            bsc = Main.runWithDic({})
        else:
            bsc = Main.runWithDic(dic)
        dcc = DepthChildCount()
        bsc.controllers.toc.set_call(dcc.new_call)
        bsc.set_model(NodeExplorer())
        if filepath is not None:
            bsc._model.loadFile(filepath)
        bsc.controllers.dcc = dcc
        dcc.set_basic_controller(bsc)
        return bsc