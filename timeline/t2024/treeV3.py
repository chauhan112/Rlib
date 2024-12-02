from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from basic import Main as ObjMaker
from CryptsDB import CryptsDB
import datetime
from timeline.t2023.dep_extractor.dependency_extractor import DicOps
from timeline.t2024.ui_lib.refactored_key_value_adder import ListOps
from GraphDB import GraphDB
import copy as CopyLib
from SerializationDB import SerializationDB
from enum import Enum
import json

class CommandOps(Enum):
    ADD = 'add'
    DEL = 'del'
    EDIT = 'edit'
    COPY = 'copy'
    CUT = 'cut'
    PASTE = 'paste'
    DEPTH = 'dep'
    CHILDNR = 'cn'
    ENUM = 'enum'
    HELP = 'h'
    LS = 'ls'
    CD = 'cd'
    ADDD = "addd"
    HISTORY = "his"
    TOTAL_CHILD_NR = "tcn"
    MAX_DEPTH = "mdep"
    VALUE = "value"
    SHORT_CUTS = "sc"
def ParseLoc():
    def test():
        cases = [("1", [[1]]), ("1/1", [[1,1]]), ("1, 2-3", [[1], [2], [3]]), ("1-4, 7, 9, 6/6", [[1],[2],[3],[4],[7],[9],[6,6]])]
        for inp, out in cases:
            if parse(inp) != out:
                print(inp)
    def parse(inp):
        segs = list(map(lambda x: x.strip(), inp.split(",")))
        res = []
        for seg in segs:
            if "-" in seg:
                x, y = list(map(int, seg.split("-")))
                for i in range(x,y+1):
                    res.append([i])
            elif "/" in seg:
                res.append(list(map(int, seg.split("/"))))
            else:
                res.append([int(seg)])
        return res
    def parse_shortcuts(txt):
        from RegexDB import RegexDB,NameDicExp
        func = lambda string: RegexDB.group_name_search(NameDicExp(" *-", "op", "c|d|l|r|h", NameDicExp(" *", "name", r"\w*", 
                                    NameDicExp(" *", "params", ".*", ""))),string)
        return func(txt)
    s = ObjMaker.variablesAndFunction(locals())
    return s
def ProcessCommands():
    parent = None
    funcsAndValues = {}
    current_location = []
    editLoc = None
    parseLoc = ParseLoc()
    helpInfos = {}
    helpInfos[CommandOps.ADD.value] = "add a new node"
    helpInfos[CommandOps.ADDD.value] = "add a new node with loc. For example: addd 1/1/2 value"
    helpInfos[CommandOps.DEL.value] = "delete an existing node. del 1, del 1/1"
    helpInfos[CommandOps.EDIT.value] = "edit a node. Eg. edit 1, edit 1/1/2"
    helpInfos[CommandOps.LS.value] = "show tree"
    helpInfos[CommandOps.CD.value] = "go to the node. eg: cd 1/1, cd 1"
    helpInfos[CommandOps.COPY.value] = "copy a node selected. eg: copy 1/1, copy 1, copy 1-4, copy 1,2,6,7"
    helpInfos[CommandOps.CUT.value] = "cut a node selected. eg: cut 1/1, cut 1, cut 1-4, cut 1,2,6,7"
    helpInfos[CommandOps.PASTE.value] = "paste the selected nodes (copy or cut). eg: paste, paste 1"
    helpInfos[CommandOps.ENUM.value] = "toggle enumerate the listing"
    helpInfos[CommandOps.CHILDNR.value] = "number of childs in the name"
    helpInfos[CommandOps.DEPTH.value] = "set depth level. Eg: depth 3"
    helpInfos[CommandOps.HELP.value] = "show help"
    helpInfos[CommandOps.HISTORY.value] = "show command called history. Eg: his all, his 10"
    helpInfos[CommandOps.MAX_DEPTH.value] = "toggle max depth. Show the depth of the node"
    helpInfos[CommandOps.TOTAL_CHILD_NR.value] = "toggle all sum of nodes inside"
    helpInfos[CommandOps.SHORT_CUTS.value] = "short cuts cruds. Eg: sc -c name ls,cd 3, .., sc -d name, sc -r"
    copyCutValues = {}
    namesFunc = []
    def changed():
        pass
    def get_locationV2(param):
        locs = s.process.parseLoc.handlers.parse(param)
        res = []
        tv = s.process.parent.process.treeViewer
        for loc in locs:
            assert len(loc) != 0
            curLoc = tuple(s.process.current_location)
            for index in loc:
                children = tv.process.locToChildren[curLoc]
                curLoc = tuple(children[index-1])
            res.append(curLoc)
        return res
    def get_location(param):
        index = int(param.strip())
        tv = s.process.parent.process.treeViewer
        children = tv.process.locToChildren[tuple(s.process.current_location)]
        return children[index-1]
    def add(param):
        if param.strip() == "":
            return 
        s.process.parent.process.model.loc_ops(s.process.current_location, "add", param, {})
        s.handlers.changed()
    def addd(param):
        params = param.strip()
        if params == "":
            return 
        params = params.split(" ")
        if len(params) < 2:
            return
        loc = params[0]
        val = " ".join(params[1:])
        target_loc = list(s.handlers.get_locationV2(loc)[0])
        s.process.parent.process.model.loc_ops(target_loc, "add", val, {})
        s.handlers.changed()
    def delete(param):
        loc = s.handlers.get_location(param).copy()
        lastKey = loc.pop()
        s.process.parent.process.model.loc_ops(loc, "delete", lastKey)
        s.handlers.changed()
    def deleteAdvance(param):
        locs = s.handlers.get_locationV2(param)
        for loc in locs:
            locList = list(loc)
            lastKey = locList.pop()
            s.process.parent.process.model.loc_ops(locList, "delete", lastKey)
        s.handlers.changed()
    def update(param):
        loc = list(s.handlers.get_locationV2(param)[0])
        content = s.process.parent.process.model.loc_ops(loc, "read")["name"]
        parent = s.process.parent
        parent.views.commandInput.handlers.handle = parent.handlers.doNothing
        parent.views.commandInput.outputs.layout.value = content + " "
        parent.views.commandInput.handlers.handle = s.handlers.updateIt
        s.process.editLoc = loc.copy()
    def updateIt(w):
        val = w['owner'].value
        oldVals = s.process.parent.process.model.loc_ops(s.process.editLoc, "read")
        lastKey = s.process.editLoc.pop()
        oldVals["name"] = val
        s.process.parent.process.model.loc_ops(s.process.editLoc, "update", lastKey, oldVals)
        parent = s.process.parent
        parent.views.commandInput.handlers.handle = parent.handlers.doNothing
        parent.views.commandInput.outputs.layout.value = ""
        parent.views.commandInput.handlers.handle = parent.handlers.onEnteredCommand
        parent.process.ops[CommandOps.LS.value]("")
        s.handlers.changed()
    def listDir(param):
        name = ""
        if len(s.process.current_location) > 0:
            model_loc = s.process.parent.process.model.model_loc(s.process.current_location)
            name = s.process.parent.process.model.read(model_loc)["name"] + "\n"
        tv = s.process.parent.process.treeViewer
        txt = tv.handlers.get_text(s.process.current_location)
        s.process.parent.handlers.displayText ( name + txt + "\n"* 10)
        s.process.parent.process.afterRunFuncs.clear()
    def cd(param):
        if param.strip() == "..":
            if len(s.process.current_location) > 0:
                s.process.current_location.pop()
        else:
            s.process.current_location = list(s.handlers.get_locationV2(param)[0])
    def copy(param):
        locs = s.handlers.get_locationV2(param)
        for loc in locs:
            content = s.process.parent.process.model.loc_ops(list(loc), "read")
            s.process.copyCutValues[loc] = CopyLib.deepcopy(content)
    def cut(param):
        locs = s.handlers.get_locationV2(param)
        for loc in locs:
            content = s.process.parent.process.model.loc_ops(list(loc), "read")
            locList = list(loc)
            lastKey = locList.pop()
            s.process.copyCutValues[loc] = CopyLib.deepcopy(content)
            s.process.parent.process.model.loc_ops(locList, "delete", lastKey)
    def paste(param):
        if param.strip() == "":
            loc = s.process.current_location.copy()
        else:
            loc = list(s.handlers.get_locationV2(param)[0])
        for key in s.process.copyCutValues:
            s.process.parent.process.model.loc_ops(loc, "update", key[-1], s.process.copyCutValues[key])
        s.process.copyCutValues.clear()
        s.handlers.changed()
    def enumerateList(param):
        key = CommandOps.ENUM.value
        def nameGetter(name, loc):
            index = s.process.parent.process.treeViewer.process.locToIndex[tuple(loc)]
            return f"{index + 1}. {name}"
        s.handlers.toggleNameFunc(key, nameGetter)
    def childNr(param):
        key = CommandOps.CHILDNR.value
        def nameGetter(name, loc):
            vals = s.process.parent.process.treeViewer.handlers.cdToLocAndRead(loc)
            chNr = len(vals[CommandOps.VALUE.value])
            return f"{name} - {chNr}"
        s.handlers.toggleNameFunc(key, nameGetter)
    def totalChildNr(param):
        key = CommandOps.TOTAL_CHILD_NR.value
        def nameGetter(name, loc):
            vals = s.process.parent.process.treeViewer.handlers.cdToLocAndRead(loc)
            return f"{name} - {vals[key]}"
        s.handlers.totalChildCount(s.process.parent.process.model.s.process.model)
        s.handlers.toggleNameFunc(key, nameGetter)
    def maxDepth(param):
        key = CommandOps.MAX_DEPTH.value
        def nameGetter(name, loc):
            vals = s.process.parent.process.treeViewer.handlers.cdToLocAndRead(loc)
            return f"{name} - {vals[key]}"
        s.handlers.update_max_depth_count(s.process.parent.process.model.s.process.model)
        s.handlers.toggleNameFunc(key, nameGetter)
    def depthNr(param):
        ly = int(param)
        s.process.parent.process.treeViewer.process.dtr.process.depth_level= ly
    def totalChildCount(dic):
        ch = dic[CommandOps.VALUE.value]
        if len(ch) == 0:
            dic[CommandOps.TOTAL_CHILD_NR.value] = 1
            return dic[CommandOps.TOTAL_CHILD_NR.value]
        dic[CommandOps.TOTAL_CHILD_NR.value] = sum([s.handlers.totalChildCount(ch[n]) for n in ch])
        return dic[CommandOps.TOTAL_CHILD_NR.value]
    def update_max_depth_count(dic):
        ch = dic[CommandOps.VALUE.value]
        if len(ch) == 0:
            dic[CommandOps.MAX_DEPTH.value] = 0
            return 0
        depths = []
        for key in ch:
            child = ch[key]
            child[CommandOps.MAX_DEPTH.value] = s.handlers.update_max_depth_count(child)
            depths.append(child[CommandOps.MAX_DEPTH.value])
        dic[CommandOps.MAX_DEPTH.value] = max(depths) + 1
        return dic[CommandOps.MAX_DEPTH.value]
    def helpMe(param):
        arr = list(s.process.helpInfos.items())
        content = GraphDB.showTableEditor(arr, False)
        s.process.parent.handlers.displayText ( content )
        s.process.parent.process.afterRunFuncs.clear()
    def history(param):
        arr = s.process.parent.process.history
        content = "\n".join(list(map(lambda x: f"{x[0]+1}. {x[1]}",zip(range(len(arr)), arr)) ))
        s.process.parent.handlers.displayText ( content )
        s.process.parent.process.afterRunFuncs.clear()
    def nameModifier(loc):
        name = s.process.parent.process.treeViewer.handlers.nameGetter(loc)
        for key, func in s.process.namesFunc:
            name = func(name, loc)
        return name
    def toggleNameFunc(funKey, funToAdd):
        newRes = []
        exists = False
        for ke, fun in s.process.namesFunc:
            if ke == funKey:
                exists = True
            else:
                newRes.append((ke, fun))
        if not exists:
            newRes.append((funKey, funToAdd))
        s.process.namesFunc = newRes
    def short_cuts(param):
        info = s.process.parseLoc.handlers.parse_shortcuts(param.strip())
        if "op" in info:
            op = info["op"]
            params = info["params"]
            name = info["name"]
            if op == "c":
                if params != "" and name != "":
                    s.process.parent.process.metainfo[name] = list(map(lambda x: x.strip(), params.split(",")))
                    SerializationDB.pickleOut(s.process.parent.process.metainfo, s.process.parent.process.metafile)
            elif op == "d":
                if name in s.process.parent.process.metainfo:
                    del s.process.parent.process.metainfo[name]
                    SerializationDB.pickleOut(s.process.parent.process.metainfo, s.process.parent.process.metafile)
                else:
                    s.process.parent.handlers.displayText ( f"no name found to delete: {name}" )
            elif op == "r":
                if name in s.process.parent.process.metainfo:
                    vals = s.process.parent.process.metainfo[name]
                    for v in vals:
                        s.process.parent.views.commandInput.outputs.layout.value = v
            elif op == "l":
                txt = json.dumps(s.process.parent.process.metainfo, indent=4)
                s.process.parent.handlers.displayText ( txt )
                s.process.parent.process.afterRunFuncs.clear()
            elif op == "h":
                txt = "ops r -> run shortcut -r shortcut_name\n" 
                txt += "ops l -> list all shortcuts: -l\n" 
                txt += "ops c -> create new shortcut: -c name command1, command2, command3\n" 
                txt += "ops d -> delete shortcut: -d name\n"  
                txt += "ops h -> help with commands: -h\n"  
                s.process.parent.handlers.displayText ( txt )
                s.process.parent.process.afterRunFuncs.clear()
    s = ObjMaker.uisOrganize(locals())
    return s
def TreeComponent():
    treeViewer = TreeModelTreeRenderer()
    model = TreeModel()
    treeViewer.process.model = model
    # depthCounter = DepthChildCount() # needs fixing does not work yet
    
    outArea = Utils.get_comp({},ComponentsLib.CustomOutput, className = "w-auto")
    textArea = Utils.get_comp({"placeholder":"type h for help", "disabled":True}, IpywidgetsComponentsEnum.Textarea, 
                              className="w-auto txtArea-min-height", bind = False)
    commandInput = Utils.get_comp({"placeholder":"enter your command"}, IpywidgetsComponentsEnum.Text, className="w-auto")
    commandInput.outputs.layout.continuous_update = False
    customCss = Utils.get_comp({}, ComponentsLib.CSSAdder)
    classes = ['.txtArea-min-height textarea{', '    height: 400px', '}']
    classes = "\n".join(classes)
    customCss.outputs.layout.content = classes
    container = Utils.container([textArea, commandInput, outArea, customCss], className= "flex flex-column")
    history = []
    ops = {}
    afterRunFuncs = []
    commandHandler = ProcessCommands()
    def register():
        ops[CommandOps.ADD.value] = commandHandler.handlers.add
        ops[CommandOps.ADDD.value] = commandHandler.handlers.addd
        ops[CommandOps.DEL.value] = commandHandler.handlers.deleteAdvance
        ops[CommandOps.EDIT.value] = commandHandler.handlers.update
        ops[CommandOps.COPY.value] = commandHandler.handlers.copy
        ops[CommandOps.CUT.value] = commandHandler.handlers.cut
        ops[CommandOps.PASTE.value] = commandHandler.handlers.paste
        ops[CommandOps.DEPTH.value] = commandHandler.handlers.depthNr
        ops[CommandOps.CHILDNR.value] = commandHandler.handlers.childNr
        ops[CommandOps.ENUM.value] = commandHandler.handlers.enumerateList
        ops[CommandOps.HELP.value] = commandHandler.handlers.helpMe
        ops[CommandOps.LS.value] = commandHandler.handlers.listDir
        ops[CommandOps.CD.value] = commandHandler.handlers.cd
        ops[CommandOps.HISTORY.value] = commandHandler.handlers.history
        ops[CommandOps.MAX_DEPTH.value] = commandHandler.handlers.maxDepth
        ops[CommandOps.TOTAL_CHILD_NR.value] = commandHandler.handlers.totalChildNr
        ops[CommandOps.SHORT_CUTS.value] = commandHandler.handlers.short_cuts
        
        assert len(commandHandler.process.helpInfos) == len(ops)
    def onEnteredCommand(w):
        s.handlers.beforeCommand("")
        s.process.afterRunFuncs.append(s.process.ops[CommandOps.LS.value])   
        with s.views.outArea.state.controller._out:
            val = s.views.commandInput.outputs.layout.value.strip()
            s.views.commandInput.handlers.handle = s.handlers.doNothing
            s.views.commandInput.outputs.layout.value = ""
            s.views.commandInput.handlers.handle = s.handlers.onEnteredCommand
            if len(val) == 0:
                return
            s.process.history.append(val)
            x = val.split(" ")
            if x[0] in s.process.ops:
                s.process.ops[x[0]](" ".join(x[1:]))
            else:
                s.process.ops[CommandOps.ADD.value](val)
            s.handlers.afterCommand(val)
    def doNothing(w):
        pass
    def beforeCommand(param):
        s.views.outArea.state.controller._out.clear_output()
    def afterCommand(param):
        for func in s.process.afterRunFuncs:
            func(param)
    def displayText(txt):
        s.views.textArea.outputs.layout.value = txt
    def set_file(filePath): 
        s.process.filePath = filePath
        s.process.model.s.process.model = SerializationDB.readPickle(filePath)
        s.process.commandHandler.handlers.changed = s.handlers.sync
    def set_metafile_info(filename):
        s.process.metafile = filename
        s.process.metainfo = SerializationDB.readPickle(filename)
    def sync():
        SerializationDB.pickleOut(s.process.model.s.process.model, s.process.filePath)
    commandInput.handlers.handle = onEnteredCommand
    s = ObjMaker.uisOrganize(locals())
    register()
    treeViewer.process.dtr.handlers.name = commandHandler.handlers.nameModifier
    commandHandler.process.parent = s
    return s
def TreeModel():
    model = {"name": "root", "value": {}}
    main_loc = []
    version = 0
    def changed():
        s.process.version += 1
    def goback():
        if len(s.process.main_loc) > 0:
            s.process.main_loc.pop()
            s.process.main_loc.pop()
    def goForward(key):
        s.process.main_loc.append("value")
        s.process.main_loc.append(key)
    def generate_id():
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S') + CryptsDB.generateUniqueId()
    def add(key, val):
        if not s.handlers.nameExists(key):
            dateID = s.handlers.generate_id()
            s.handlers.update(dateID, {"value": val, "name": key})
            s.handlers.changed()
            return dateID
        return None
    def read(loc = None):
        newLoc = loc
        if newLoc is None:
            newLoc = s.process.main_loc
        elif type(newLoc) == str:
            newLoc = s.process.main_loc.copy() + [loc]
        return DicOps.get(s.process.model, newLoc)
    def update(key, newValue):
        loc = s.process.main_loc.copy() + ["value",key]
        DicOps.addEventKeyError(s.process.model, loc, newValue)
        s.handlers.changed()
    def delete(key):
        vals = s.handlers.read("value")
        del vals[key]
        s.handlers.changed()
    def exists(key):
        vals = s.handlers.read("value")
        return key in vals
    def nameExists(name):
        vals = s.handlers.read("value")
        for key in vals:
            if vals[key]["name"] == name:
                return True
        return False
    def readAll():
        return s.process.model
    def readableFormDic():
        return s.handlers._read(s.handlers.read("value"))
    def _read(dic):
        newDic = {}
        for key in dic:
            val = dic[key]
            if "value" in val:
                newDic[val["name"]] = s.handlers._read(val["value"])
        return newDic
    def set_dictionary(dic):
        if "value" in dic:
            s.process.model = dic
        else:
            s.process.model["value"]=dic
        s.process.main_loc = []
    def loc_ops(loc, opName, *param):
        return s.handlers.loc_ops_main_loc(s.handlers.model_loc(loc), opName, *param)
    def loc_ops_main_loc(loc, opName, *param):
        if opName not in ["add", "update", "delete", "exists", "read"]:
            return
        prev_loc = s.process.main_loc
        s.process.main_loc = loc
        try:
            res = getattr(s.handlers, opName)(*param)
        except:
            pass
        finally:
            s.process.main_loc = prev_loc
        return res
    def model_loc(loc):
        return ListOps.joinForList(loc, "value")

    s = ObjMaker.uisOrganize(locals())
    s.handlers.s = s
    return s.handlers
def DynamicTreeRenderer():
    location  = []
    depth_level = 3
    data = {"name":"root", "value": {}}
    space  = '    '
    branch = '│   '
    tee    = '├── '
    last   = '└── '
    def name(path):
        return str(path)
    def isDir(path):
        return False
    def get_children(path):
        return []
    def append_to_loc(key):
        s.process.location.append(key)
    def pop_from_loc():
        if len(s.process.location) > 0:
            s.process.location.pop()
    def set_data(data):
        s.process.data["value"] = data
    def _tree(dir_path, prefix= "", lyr = 0):
        contents = s.handlers.get_children(dir_path)
        pointers = [tee] * (len(contents) - 1) + [last]
        for pointer, path in zip(pointers, contents):
            yield prefix + pointer + s.handlers.name(path)
            if s.handlers.isDir(path) and lyr < s.process.depth_level:
                extension = branch if pointer == tee else space
                yield from s.handlers._tree(path, prefix=prefix+extension, lyr=lyr+1)
    def getAsText(loc):
        return "\n".join(s.handlers._tree(loc)) 
    s = ObjMaker.variablesAndFunction(locals())
    return s
def TreeModelTreeRenderer():
    model = TreeModel()
    dtr = DynamicTreeRenderer()
    dtr.handlers.append_to_loc = model.goForward
    dtr.handlers.pop_from_loc = model.goback
    locToIndex = {}
    locToChildren = {}
    def children(loc):
        vals = s.handlers.cdToLocAndRead(loc)
        res = []
        for i, val in enumerate(vals["value"]):
            arr = loc + [val]
            res.append(arr)
            s.process.locToIndex[tuple(arr)] = i
        s.process.locToChildren[tuple(loc)] = res
        return res
    def hasChildren(loc):
        vals = s.handlers.cdToLocAndRead(loc)
        return len(vals["value"]) != 0
    def nameGetter(loc):
        res = s.handlers.cdToLocAndRead(loc)
        name= res["name"]
        k = 65
        if len(name) > k:
            name = name[:k] + "..."
        return name
    def cdToLocAndRead(loc):
        arr = ListOps.joinForList(loc, "value")
        return s.process.model.read(arr)
    def get_text(loc):
        return dtr.handlers.getAsText(loc)
    dtr.handlers.get_children = children
    dtr.handlers.isDir = hasChildren
    dtr.handlers.name = nameGetter
    s = ObjMaker.variablesAndFunction(locals())
    return s