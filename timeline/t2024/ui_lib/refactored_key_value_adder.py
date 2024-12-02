from timeline.t2024.ui_lib.IpyComponents import IpywidgetsComponentsEnum, Utils, ComponentsLib
from basic import NameSpace
from timeline.t2024.experiments.namespace_generic_logger import DictionaryCRUD
from basic import Main as ObMakr
from timeline.t2023.dep_extractor.dependency_extractor import DicOps
from timeline.t2024.generic_logger.generic_loggerV3 import AddCancelBtns
import copy
from CryptsDB import CryptsDB
from enum import Enum
from SerializationDB import SerializationDB
import json

def BijectiveFunction():
    indices2Vals = {}
    vals2indices = {}
    def get_val(index):
        return s.process.indices2Vals[index]
    def get_index(val, addEntry = False):
        idd = s.handlers.val_to_index_func(val)
        if idd in s.process.vals2indices:
            pass
        elif addEntry:
            s.process.vals2indices[idd] = CryptsDB.generateUniqueId()
            s.process.indices2Vals[s.process.vals2indices[idd]] = s.handlers.valueWrapper(val)
        else:
            raise IOError("not found")
        return s.process.vals2indices[idd]
    def val_to_index_func(val):
        return id(val)
    def valueWrapper(val): # to copy it
        return val
    s = ObMakr.variablesAndFunction(locals())
    return s
class EventBasic(Enum):
    onRender = "onRender"
    onFirstTimeRender = "onFirstTimeRender"
    onClicked = "onClicked"
def DicCRUDV2():
    vals = {}
    loc = []
    def model_changed():
        pass
    def delete(key,transform = True):
        cur_loc = key
        if transform:
            cur_loc = s.handlers._loc(key)
        lastKey = cur_loc.pop() 
        vals = DicOps.get(s.process.vals, cur_loc)
        del vals[lastKey]
        s.handlers.model_changed()
    def get_state():
        return s
    def _loc(key):
        if type(key) == list:
            return s.process.loc + key
        return s.process.loc + [key]
    def set_baseloc(loc):
        s.process.loc = loc
    def exists(key):
        try:
            s.handlers.read(key)
            return True
        except:
            pass
        return False
    def write(key, value, overwrite=False, transform = True):
        if s.handlers.exists(key) and not overwrite:
            raise IOError("Value already exists")
        cur_loc = key
        if transform:
            cur_loc = s.handlers._loc(key)
        DicOps.addEventKeyError(s.process.vals, cur_loc, value)
        s.handlers.model_changed()
    def read(key, transform = True):
        cur_loc = key
        if transform:
            cur_loc = s.handlers._loc(key)
        return DicOps.get(s.process.vals, cur_loc)
    def readAll():
        return DicOps.get(s.process.vals, s.process.loc) 
    def set_dictionary(dic):
        s.process.vals = dic
        s.process.loc = []
    s = ObMakr.variablesAndFunction(locals())
    return s
def DicListCRUDV2():
    model_inst = DicCRUDV2()
    model = model_inst.handlers
    prev_funcs = ObMakr.namespace()
    changedDeclared = False
    def model_changed():
        pass
    def append_in_list(key, value):
        vals = s.process.model.read(key)
        vals.append(value)
        newKey = len(vals) - 1
        s.handlers.model_changed()
        return newKey
    def set_file(file):
        s.process.filename = file
        content = SerializationDB.readPickle(file)
        s.process.model.set_dictionary(content)
        s.process.model.model_changed = sync
    def sync():
        SerializationDB.pickleOut(s.process.model_inst.process.vals, s.process.filename)
    def set_dictionary(dic):
        s.process.model.set_dictionary(dic)
        s.process.model.model_changed = model_changed
    localState = ObMakr.variablesAndFunction(locals())
    s = ObMakr.variablesAndFunction(locals())
    ObMakr.dicToNamespace(model.__dict__, s.handlers)
    return s
def KeyValueModelWithMetaV3Tool():
    parent = None
    def transform_loc(loc):
        newLoc = ListOps.joinForList(loc, "value", True)
        return newLoc
    def read_meta(absLoc):
        loc = s.handlers.transform_loc(absLoc) + ["meta"]
        return s.process.parent.process.model.read(loc, False)
    def read(absLoc):
        loc = s.handlers.transform_loc(absLoc)
        return s.process.parent.process.model.read(loc, False)
    def write_meta(absLoc, vals, overwrite=True):
        loc = s.handlers.transform_loc(absLoc) + ["meta"]
        return s.process.parent.process.model.write(loc, vals, overwrite, False)
    def write(absLoc, vals, overwrite):
        loc = s.handlers.transform_loc(absLoc)
        return s.process.parent.process.model.write(loc,vals, overwrite, False)
    s = ObMakr.variablesAndFunction(locals())
    return s
def KeyValueModelWithMetaV3():
    loc = []
    model_inst = DicListCRUDV2()
    model = model_inst.handlers
    tools = KeyValueModelWithMetaV3Tool()

    locIndexfunc = BijectiveFunction()
    locIndexfunc.handlers.val_to_index_func = lambda x: tuple(x)
    locIndexfunc.handlers.valueWrapper = lambda x: x.copy()
    def model_changed():
        pass
    def set_dictionary(dic):
        s.process.loc = []
        s.process.model.set_dictionary(dic)
    def transform_to_absLoc(loc):
        return ListOps.joinForList(loc, "value", True)
    def set_baseloc(loc):
        s.process.loc = loc
        if len(loc) == 0:
            s.process.model.set_baseloc([])
        else:
            s.process.model.set_baseloc(s.handlers.transform_to_absLoc(loc))
    def exists(key):
        return s.process.model.exists(["value", key])
    def delete(key):
        s.process.model.delete(["value", key])
        s.handlers.model_changed()
    def readAll():
        return s.process.model.read(["value"])
    def read_meta(key = None):
        if key is None:
            return s.process.model.read(["meta"])
        if s.process.model.exists(["value", key, "meta"]):
            return s.process.model.read(["value", key, "meta"])
        return {}
    def write_meta(loc, value, overwrite=False):
        newLoc = ["meta"] + loc
        s.process.model.write(newLoc,value, overwrite)
    def read_value(key = None):
        if key is None:
            return s.process.model.read(["value"])
        return s.process.model.read(["value", key, "value"])
    def read(key):
        return [s.handlers.read_value(key), s.handlers.read_meta(key)]
    def write( key, value, overwrite=False ):
        if not overwrite:
            if s.process.model.read(["meta", "type"]) == list:
                newKey = s.process.model.append_in_list(["value"], {"value": value})
                s.process.model.write(["value", newKey, "meta", "type"], type(value), True)
                s.handlers.model_changed()
                return
        s.process.model.write(["value", key, "value"], value, overwrite)
        s.process.model.write(["value", key, "meta", "type"],type(value), True)
        s.handlers.model_changed()
    def cd(key):
        s.process.loc.append(key)
        s.handlers.set_baseloc(s.process.loc)
    def get_abs_loc(key=None):
        if key is None:
            return s.handlers.transform_to_absLoc(s.process.loc)
        return s.handlers.transform_to_absLoc(s.process.loc + [key])
    def get_current_location():
        return s.process.loc
    def get_current_type():
        return s.process.model.read(["meta", "type"])
    def dirList():
        res = []
        vals = s.handlers.readAll()
        typ = s.handlers.get_current_type()
        if typ == list:
            for index, value in enumerate(vals):
                res.append((str(index), (value, s.process.locIndexfunc.handlers.get_index(s.process.loc, True), index, typ), 
                    value["meta"]["type"] in [dict, list]))
        elif typ == dict:
            for key in vals:
                data = vals[key]
                res.append((str(key),( data, s.process.locIndexfunc.handlers.get_index(s.process.loc, True), key, typ), 
                    s.handlers.read_meta(key)["type"] in [dict, list]))
        return res
    def get_location(key):
        return s.process.model._loc(["value", key])
    def goBack():
        if len(s.process.loc) == 0:
            return 
        s.process.loc.pop()
        s.handlers.set_baseloc(s.process.loc)
    def set_file(file):
        s.process.file = file
        s.process.model.set_file(file)
    def get_content():
        return s.process.model_inst.process.model_inst.process.vals
    def write_to_a_file(file):
        SerializationDB.pickleOut(s.handlers.get_content(), file)
    s = ObMakr.variablesAndFunction(locals())
    tools.process.parent = s
    set_dictionary({"value": {}, "meta":{"type": dict}})
    return s
class ListOps:
    def joinForList(loc, inserter="", first=True, last=False):
        newLoc = []
        size = len(loc)
        for i, val in enumerate(loc):
            if i == 0:
                if first:
                    newLoc.append(inserter)
            else:
                newLoc.append(inserter)
            newLoc.append(val)
        if last:
            newLoc.append(inserter)
        return newLoc
class KeyValueModel:
    def __init__(self):
        self._model_changed = lambda : ""
        self._model = DicListCRUD()
        locIndexfunc = BijectiveFunction()
        locIndexfunc.handlers.val_to_index_func = lambda x: tuple(x)
        locIndexfunc.handlers.valueWrapper = lambda x: x.copy()
        self.locIndexfunc = locIndexfunc
    def get_current_location(self):
        return self._model._baseloc
    def get_current_type(self):
        vals = self._model.readAll()
        return type(vals)
    def write(self, key, value, overwrite=False):
        self._model.write(key, value, overwrite)
        self._model_changed()
    def dirList(self):
        res = []
        vals = self._model.readAll()
        typ = type(vals)
        if typ == list:
            for index, value in enumerate(vals):
                res.append((str(index), (value, self.locIndexfunc.handlers.get_index(self.get_current_location(), True), index, typ), 
                            type(value) in [dict, list]))
        elif typ == dict:
            for key in vals:
                data = vals[key]
                res.append((key, (data, self.locIndexfunc.handlers.get_index(self.get_current_location(), True), key, typ),
                            type(data) in [dict, list]))
        return res
    def cd(self, key):
        current_loc = self.get_current_location()
        current_loc.append(key)
        self.set_baseloc(current_loc)
        self._current_key = key
    def set_baseloc(self, loc):
        self._model.set_baseloc(loc)
    def goBack(self):
        current_loc = self.get_current_location()
        if len(current_loc) != 0:
            current_loc.pop()
        self.set_baseloc(current_loc)
    def delete(self, key):
        self._model.delete(key)
        self._model_changed()
    def readAll(self):
        return self._model.readAll()
    def set_dictionary(self, dic):
        self._model.set_dictionary(dic)
class KeyValueModelWithMeta:
    def __init__(self):
        self._model = DictionaryCRUD()
        self.set_dictionary({})
        self.set_baseloc([])
        self._define_defaults()
    def _define_defaults(self):
        metaInfo = "meta"
        value = "val"
        typeOfValue = "type"
        self.constants = ObMakr.dicToNamespace(locals())
    def set_dictionary(self, dic):
        self._data = dic
        self._model.set_dictionary(dic)
    def dirList(self):
        vals = self.get_current_vals()
        typ = self.get_current_type()
        res = []
        if typ == list:
            for index, value in enumerate(vals):
                res.append((index, value[self.constants.value], value[self.constants.metaInfo][self.constants.typeOfValue] in [dict, list]))
        elif typ == dict:
            for key in vals:
                data = vals[key]
                metaInfo = data[self.constants.metaInfo]
                res.append((key, data[self.constants.value], metaInfo[self.constants.typeOfValue] in [dict, list]))
        return res
    def isContainer(self, key =None):
        if key is None:
            typ = self.get_current_type()
        else:
            typ = self.get_meta(key)[self.constants.metaInfo]
        return typ in [list, dict]
    def get_meta(self, key):
        self._model.set_baseloc(self._to_valLoc)
        val = self._model.read(key)
        self._model.set_baseloc(self._modified_base_loc)
        return val[self.constants.metaInfo]
    def get_value(self, key):
        self._model.set_baseloc(self._to_valLoc)
        val = self._model.read(key)
        self._model.set_baseloc(self._modified_base_loc)
        return val[self.constants.value]
    def get_current_meta(self):
        vals = self._model.readAll()
        if len(self._base_loc) == 0:
            return {self.constants.typeOfValue: dict}
        return vals[self.constants.metaInfo]
    def get_current_vals(self):
        vals = self._model.readAll()
        if len(self._base_loc) == 0:
            return vals
        return vals[self.constants.value]
    def read(self, key):
        return self._model.read(key)
    def delete(self, key):
        self._model.set_baseloc(self._to_valLoc)
        self._model.delete(key)
        self._model.set_baseloc(self._modified_base_loc)
    def exists(self, key):
        self._model.set_baseloc(self._to_valLoc)
        res = self._model.exists(key)
        self._model.set_baseloc(self._modified_base_loc)
        return res
    def add_meta_info(self, key, metaKey, metaValue):
        self._model.set_baseloc(self._to_valLoc + [key, self.constants.metaInfo])
        self._model.write(metaKey, metaValue, True)
        self._model.set_baseloc(self._modified_base_loc)
    def write(self, key, value, overwrite = False):
        typ = self.get_current_type()
        self._model.set_baseloc(self._to_valLoc)
        if typ == list:
            curVal = self._model.readAll()
            valWrapper = {self.constants.value: value}
            if overwrite and type(key) == int:
                self._model.write(key, valWrapper, overwrite)
            else:
                curVal.append(valWrapper)
                key = len(curVal) - 1
        else:
            self._model.write(key, {"val": value}, overwrite)
        self.add_meta_info(key, self.constants.typeOfValue, type(value))
        self._model.set_baseloc(self._modified_base_loc)
    def set_baseloc(self, loc):
        self._base_loc = loc
        self._to_valLoc = self._modify_location(loc)
        self._modified_base_loc = self._to_valLoc
        if len(self._to_valLoc) != 0:
            self._modified_base_loc = self._to_valLoc[:-1]
        self._model.set_baseloc(self._modified_base_loc)
    def _modify_location(self, loc):
        newLoc = []
        for i, val in enumerate(loc):
            newLoc.append(val)
            newLoc.append(self.constants.value)
        return newLoc
    def get_current_location(self):
        return self._base_loc
    def goBack(self):
        current_loc = self.get_current_location()
        if len(current_loc) != 0:
            current_loc.pop()
        self.set_baseloc(current_loc)
    def cd(self, key):
        current_loc = self.get_current_location()
        current_loc.append(key)
        self.set_baseloc(current_loc)
    def get_current_type(self):
        return self.get_current_meta()[self.constants.typeOfValue]
class DicListCRUD(DictionaryCRUD):
    def _get_loc(self, key):
        loc = self._baseloc.copy()
        if type(key) == list:
            loc += key
        else:
            loc.append(key)
        return loc
    def write(self, key, value, overwrite = False):
        loc = self._get_loc(key)
        vals = self.readAll()
        if type(vals) == list:
            if overwrite:
                DicOps.addEventKeyError(self._dic, loc, value)
            else:
                vals.append(value)
                newKey = len(vals) - 1
                return newKey
        else:
            if self.exists(key):
                if overwrite:
                    DicOps.addEventKeyError(self._dic, loc, value)
                else:
                    raise IOError("Value already exists")
            else:
                DicOps.addEventKeyError(self._dic, loc, value)
        return key
    def read(self, key):
        loc = self._get_loc(key)
        return DicOps.get(self._dic, loc)
    def delete(self, key):
        loc = self._get_loc(key)
        lastKey = loc.pop()
        vals = DicOps.get(self._dic, loc)
        del vals[lastKey]
    def set_dictionary(self, dic):
        self.set_baseloc([])
        super().set_dictionary(dic)
class KeyValueModelWithMetaV2:
    def __init__(self):
        self.set_dictionary({},{})
        self._initialize()
    def set_dictionary(self, dic, metaDic = None):
        if dic is not None:
            self._main_dic = dic
        if metaDic is not None:
            self._meta_dic = metaDic
    def _initialize(self):
        self.main_model = DicListCRUD()
        self.main_model.set_dictionary(self._main_dic)
        self.meta_model = DicListCRUD()
        self.meta_model.set_dictionary(self._meta_dic)
    def set_baseloc(self, loc):
        self.main_model.set_baseloc(loc)
        self.meta_model.set_baseloc(ListOps.joinForList(loc, "keys"))
    def exists(self, key):
        return self.main_model.exists(key)
    def delete(self, key):
        self.main_model.delete(key)
        self.meta_model.delete(key)
    def readAll(self):
        vals = self.main_model.readAll()
        return list(vals.keys())
    def read_meta(self, key):
        return self.meta_model.read(["keys", key, "meta"])
    def read_value(self, key):
        return self.main_model.read(key)
    def read(self, key):
        return [self.read_value(key), self.read_meta(key)]
    def write(self, key, value, overwrite=False):
        newKey = self.main_model.write(key, value, overwrite)
        self.meta_model.write(["keys", newKey, "meta", "type"], type(value))
    def cd(self, key):
        self.main_model._baseloc.append(key)
        self.set_baseloc(self.main_model._baseloc)
    def get_current_location(self):
        return self.main_model._baseloc
    def get_current_type(self):
        vals = self.meta_model.readAll()
        loc = self.get_current_location()
        if len(loc) == 0:
            return dict
        return vals["meta"]["type"]
    def dirList(self):
        res = []
        vals = self.main_model.readAll()
        typ = self.get_current_type()
        if typ == list:
            for index, value in enumerate(vals):
                res.append((index, value, self.read_meta(index)["type"] in [dict, list]))
        elif typ == dict:
            for key in vals:
                data = vals[key]
                res.append((key, data, self.read_meta(key)["type"] in [dict, list]))
        return res
    def goBack(self):
        current_loc = self.get_current_location()
        if len(current_loc) != 0:
            current_loc.pop()
        self.set_baseloc(current_loc)
def OpsComponent():
    opsType = Utils.get_comp({"options": ["add", "delete"]}, IpywidgetsComponentsEnum.Dropdown, className="fit")
    multiLineValues = Utils.get_comp({"placeholder": "content"}, IpywidgetsComponentsEnum.Textarea, bind=False, className="w-100 textarea-h-150px p0")
    keyInp = Utils.get_comp({"placeholder": "key"},IpywidgetsComponentsEnum.Text, bind=False, className="w-120px")
    textInp = Utils.get_comp({"placeholder": "value"},IpywidgetsComponentsEnum.Text, bind=False, className="w-250px")
    inpType = Utils.get_comp({"options": ["text", "var", "textarea","eval", "list", "dict", "bool", "json"]}, IpywidgetsComponentsEnum.Dropdown, className="fit")
    boolVal = Utils.get_comp({"description":"boolValue","indent": False}, IpywidgetsComponentsEnum.Checkbox, bind=False, className="w-auto")
    overwriteBox = Utils.get_comp({"description":"overwrite","indent": False}, IpywidgetsComponentsEnum.Checkbox, className="w-auto")
    okBtn = Utils.get_comp({"description": "ok"}, IpywidgetsComponentsEnum.Button, className="w-auto")
    container = Utils.container([Utils.container([opsType, keyInp, inpType, textInp,boolVal, overwriteBox, okBtn]), multiLineValues],
                                className="flex flex-column w-100")
    multiLineValues.hide()
    boolVal.hide()
    global_state = {}
    def ops_changed(wid):
        opsTypeValue = opsType.outputs.layout.value
        s.process.opsStateUpdator[opsTypeValue]()
    def inpType_changed(wid):
        inpTypeValue = inpType.outputs.layout.value
        if inpTypeValue in ["text", "var"]:
            textInp.show()
            boolVal.hide()
            multiLineValues.hide()
        elif inpTypeValue in ["textarea", "json", "eval"]:
            multiLineValues.show()
            textInp.hide()
            boolVal.hide()
        elif inpTypeValue in ["list", "dict"]:
            multiLineValues.hide()
            textInp.hide()
            boolVal.hide()
        else:
            textInp.hide()
            boolVal.show()
            multiLineValues.hide()
    def valueHide():
        inpType.hide()
        textInp.hide()
        boolVal.hide()
        multiLineValues.hide()
    def valueShow():
        inpType.show()
        textInp.show()
        boolVal.show()
        multiLineValues.show()
        inpType_changed(1)
    def get_key_value():
        valType = inpType.outputs.layout.value
        key = keyInp.outputs.layout.value
        value = None
        if valType == "text":
            value = textInp.outputs.layout.value
        elif valType == "var":
            value = s.process.global_state[textInp.outputs.layout.value]
        elif valType == "textarea":
            value = multiLineValues.outputs.layout.value
        elif valType == "list":
            value = []
        elif valType == "dict":
            value = {}
        elif valType == "json":
            value = json.loads(multiLineValues.outputs.layout.value)
        elif valType == "eval":
            value = eval(multiLineValues.outputs.layout.value)
        else:
            value = boolVal.outputs.layout.value
        return key, value
    def set_value(val):
        valType = inpType.outputs.layout.value
        if type(val) == str:
            if  "\n" in val:
                inpType.outputs.layout.value = "textarea"
                multiLineValues.outputs.layout.value= val
            else:
                inpType.outputs.layout.value = "text"
                textInp.outputs.layout.value= val
    def clearFields():
        keyInp.outputs.layout.value =""
        inpTyp = inpType.outputs.layout.value
        if inpTyp in ["text", "var"]:
            textInp.outputs.layout.value = ""
        elif inpTyp =="textarea":
            multiLineValues.outputs.layout.value = ""
    def stateForDelete():
        s.views.keyInp.show()
        s.views.okBtn.show()
        s.views.overwriteBox.hide()
        s.handlers.valueHide()
    def stateForAdd():
        s.views.keyInp.show()
        s.views.okBtn.show()
        s.views.overwriteBox.show()
        s.handlers.valueShow()
        s.handlers.inpType_changed(1)
    opsStateUpdator = {"delete": stateForDelete, "add": stateForAdd}
    opsType.handlers.handle = ops_changed
    inpType.handlers.handle = inpType_changed
    s = ObMakr.uisOrganize(locals())
    return s
def OperationManager():
    parent = None
    prev_funcs = ObMakr.namespace()
    selected_keys = {}
    copyIt = None
    prev_ops = None 
    undoers = []
    def copy_handler(w):
        key, val = s.process.parent.process.opsComp.handlers.get_key_value()
        key = s.process.parent.process.keysDisplayer.keyValMap[key][2]
        absLoc = s.handlers.get_abs_loc(key) 
        currentLoc = s.process.parent.process.model.get_current_location()
        locId = s.handlers.get_loc_id(currentLoc)
        s.process.selected_keys[(key, locId)] = absLoc 
        s.process.copyIt = True
        s.handlers.refresh_keys()
    def cut_handler(w):
        s.handlers.copy_handler(w)
        s.process.copyIt = False
    def paste_handler(w):
        currentLoc = s.process.parent.process.model.get_current_location()
        currentLocId =s.handlers.get_loc_id(currentLoc, True)
        copiedLoc = []
        for key, locId in s.process.selected_keys:
            if locId == currentLocId:
                print("skipping same loc", key)
                continue
            absLoc = s.process.selected_keys[(key, locId)]
            vals =  s.handlers.read_content(absLoc)
            s.handlers.write2model(key, vals)
            copiedLoc.append(absLoc)
        s.process.selected_keys.clear()
        if not s.process.copyIt:
            for loc in copiedLoc:
                s.handlers.delete(loc)
        s.handlers.opsSelected(1) 
        s.handlers.refresh_keys()
    def dirList():
        results = s.process.prev_funcs.dirList()
        newResults = list(filter(lambda x: (x[0], x[1][1]) not in s.process.selected_keys, results))
        return newResults
    def set_up():
        opt = s.process.parent.process.opsComp.views.opsType.outputs.layout.options
        s.process.parent.process.opsComp.views.opsType.outputs.layout.options = list(opt) + ["cut", "copy", "paste"]
        s.process.prev_funcs.opsSelected = s.process.parent.handlers.opsChangedV2
        s.process.parent.process.opsComp.views.opsType.handlers.handle = s.handlers.opsSelected
        s.process.prev_funcs.dirList = s.process.parent.process.model.dirList
        s.process.prev_funcs.render_and_update_ops_comp = s.process.parent.handlers.render_and_update_ops_comp
        s.process.parent.handlers.render_and_update_ops_comp = s.handlers.render_and_update_ops_comp
    def render_and_update_ops_comp():
        opt = s.process.parent.process.opsComp.views.opsType.outputs.layout.value
        s.process.parent.handlers.render_keys()
        typ = s.process.parent.process.model.get_current_type()
        if opt in ["add", "delete"]:
            s.process.parent.process.opsComponentUpdateFuncs[typ]()
    def enableValueField():
        s.process.parent.process.opsComp.views.textInp.outputs.layout.disabled = False
    def opsSelected(w):
        opsComp = s.process.parent.process.opsComp
        ops = opsComp.views.opsType.outputs.layout.value
        cutCopyList = ["cut", "copy", "paste"]
        for fun in s.process.undoers:
            fun()
        if ops == "copy":
            opsComp.views.keyInp.show()
            opsComp.views.okBtn.show()
            opsComp.views.okBtn.handlers.handle = s.handlers.defs.copy_handler
            opsComp.handlers.valueHide()
            opsComp.views.overwriteBox.hide()
        elif ops == "cut":
            opsComp.views.keyInp.show()
            opsComp.views.okBtn.handlers.handle = s.handlers.defs.cut_handler
            opsComp.handlers.valueHide()
            opsComp.views.overwriteBox.hide()
            opsComp.views.okBtn.show()
        elif ops == "paste":
            opsComp.handlers.valueHide()
            opsComp.views.keyInp.hide()
            opsComp.views.overwriteBox.hide()
            opsComp.views.okBtn.handlers.handle = s.handlers.paste_handler
            if len(s.process.selected_keys) == 0:
                opsComp.views.textInp.show()
                opsComp.views.okBtn.hide()
                opsComp.views.textInp.outputs.layout.value = "keys are not selected"
                opsComp.views.textInp.outputs.layout.disabled = True
                s.process.undoers.append(s.handlers.enableValueField)
        elif ops in ["add", "delete"]:
            s.process.prev_funcs.opsSelected(w)
            s.process.selected_keys.clear()
            if s.process.prev_ops in cutCopyList:
                s.handlers.refresh_keys()
        cutCopyList = ["cut", "copy", "paste"]
        if ops in cutCopyList:
            s.process.parent.process.model.dirList = s.handlers.dirList
        else:
            s.process.parent.process.model.dirList = s.process.prev_funcs.dirList
        s.process.prev_ops = ops
    def refresh_keys():
        s.process.parent.process.opsComp.handlers.clearFields()
        s.process.parent.handlers.render_keys()
    def get_abs_loc(key):
        return s.process.parent.process.model.get_abs_loc(key)
    def get_loc_id (loc, addEntry= False):
        return s.process.parent.process.keyValueModel.process.locIndexfunc.handlers.get_index(loc, addEntry)
    def write2model(key, vals):
        if s.process.parent.process.keyValueModel.process.model.read(["meta", "type"]) == list:
            s.process.parent.process.keyValueModel.process.model.append_in_list(["value"], vals)
            return
        s.process.parent.process.keyValueModel.process.model.write(["value", key], copy.deepcopy(vals))
    def read_content(loc):
        return s.process.parent.process.keyValueModel.process.model.read(loc, False)
    def delete(loc):
        s.process.parent.process.keyValueModel.process.model.delete(loc, False) 
    s = ObMakr.uisOrganize(locals())
    return s
def KeyValueSetter():
    from timeline.t2024.generic_logger.generic_loggerV3 import ResultDisplayers
    from jupyterDB import jupyterDB
    classes = """
    .w-30px{
        width: 30px;
    }
    .fit{
        width:fit-content;
    }
    .w-250px{
        width:250px
    }
    .w-100px{
        width:100px
    }
    .w-150px{
        width:150px
    }
    .w-120px{
        width:120px
    }
    .min-height-200px{
        min-height: 200px;
    }
    .border-2px-burlywood{
        border: solid 2px Burlywood;
    }
    """

    fileLabel = Utils.get_comp({"value": "File:"}, IpywidgetsComponentsEnum.Label, bind=False, className="w-30px")
    pathText = Utils.get_comp({"value": "dictionary explorer", "disabled": True}, IpywidgetsComponentsEnum.Text, bind=False)
    opsCheckbox = Utils.get_comp({"description":"ops","indent": False}, IpywidgetsComponentsEnum.Checkbox,className="w-auto")
    metaOpsCheckbox = Utils.get_comp({"description":"metaOps","indent": False}, IpywidgetsComponentsEnum.Checkbox,className="w-auto")
    fileOpsRow = Utils.container([fileLabel, pathText, opsCheckbox,metaOpsCheckbox])
    locLabel = Utils.get_comp({"value": "Loc:"}, IpywidgetsComponentsEnum.Label, bind=False, className="w-30px")
    locInput = Utils.get_comp({"value": "/", "disabled": True}, IpywidgetsComponentsEnum.Text, bind=False)
    goBackBtn = Utils.get_comp({"icon": "arrow-circle-left"}, IpywidgetsComponentsEnum.Button, bind=False, className="w-auto")
    locRow = Utils.container([locLabel, locInput, goBackBtn])

    keyLabel = Utils.get_comp({"value": "keys:"}, IpywidgetsComponentsEnum.Label, bind=False, className="w-30px")
    keysDisplayer = ResultDisplayers()
    keysRow = Utils.container([keyLabel, keysDisplayer.views.container])

    opsLabel = Utils.get_comp({"value": "ops:"}, IpywidgetsComponentsEnum.Label, bind=False, className="w-30px")
    opsComp = OpsComponent()
    opsComp.process.global_state = jupyterDB._params
    opsRow = Utils.container([opsLabel, opsComp.views.container])
    cssCompon = Utils.get_comp({}, ComponentsLib.CSSAdder, customCss= classes)
    outputArea = Utils.get_comp({}, IpywidgetsComponentsEnum.Output)
    container = Utils.container([fileOpsRow, locRow, keysRow, opsRow,outputArea, cssCompon],
                                className="flex flex-column min-height-200px border-2px-burlywood")
    keyValueModel = KeyValueModelWithMetaV3()
    model = keyValueModel.handlers
    model.s = keyValueModel
    current_location = None
    printLeafVals = True
    def update_loc():
        loc = "/".join(map(str, s.process.model.get_current_location()))
        if loc == "":
            loc = "."
        s.views.locInput.outputs.layout.value = loc
    def ok_func(btn):
        btn.description = "confirm"
        s.process.opsComp.views.okBtn.handlers.handle = s.handlers.confirm_func
    def confirm_func(btn):
        btn.description = "ok"
        s.process.opsComp.views.okBtn.handlers.handle = ok_func
        key, val = s.process.opsComp.handlers.get_key_value()
        if key.strip() == "":
            if s.process.model.get_current_type() != list:
                raise IOError("Can not add since the key is empty")
        overwriteIt = s.process.opsComp.views.overwriteBox.outputs.layout.value
        if overwriteIt:
            key = s.process.keysDisplayer.keyValMap[key][2]
        s.process.model.write(key, val, overwrite=overwriteIt)
        s.process.opsComp.handlers.clearFields()
        s.handlers.render_keys()
    def render_keys():
        keys = s.process.model.dirList()
        keyValMap = {val[0]: val[1] for val in keys}
        s.process.keysDisplayer.handlers.set_results(keys, s.process.keysDisplayer.process.pageNr)
        s.process.keysDisplayer.keyValMap = keyValMap
    def opsComponentUpdateForList():
        checkd = s.process.opsComp.views.overwriteBox.outputs.layout.value
        s.process.opsComp.views.keyInp.outputs.layout.placeholder ="index"
        if checkd:
            s.process.opsComp.views.keyInp.show()
        else:
            s.process.opsComp.views.keyInp.hide()
    def opsComponentUpdateForDict():
        s.process.opsComp.views.keyInp.show()
        s.process.opsComp.views.keyInp.outputs.layout.placeholder ="key"
    def overwriteChecked(wid):
        typ = s.process.model.get_current_type()
        s.process.opsComponentUpdateFuncs[typ]()
    def btn_clicked(tn):
        s.process.current_btn = tn
        info = s.process.keysDisplayer.process.data[tn._parent.state.index]
        isFolder = info[-1]
        val = info[1][0]
        
        s.process.opsComp.views.keyInp.outputs.layout.value = info[0]
        key = info[1][2]
        s.process.current_location = s.process.model.get_current_location() + [key]
        s.views.outputArea.outputs.layout.clear_output()
        if isFolder:
            s.process.model.cd(key)
            s.handlers.render_and_update_ops_comp()
            s.handlers.update_loc()
        elif s.process.printLeafVals:
            with s.views.outputArea.outputs.layout:
                print(val)
    def render_and_update_ops_comp():
        s.handlers.render_keys()
        typ = s.process.model.get_current_type()
        s.process.opsComponentUpdateFuncs[typ]()
    def goBackFunc(btn):
        s.views.outputArea.outputs.layout.clear_output()
        if len(s.process.model.get_current_location()):
            s.process.model.goBack()
            s.process.keysDisplayer.process.pageNr = 1
            s.handlers.render_and_update_ops_comp()
            s.handlers.update_loc()
    def name_gtter(x):
        if type(x) == str:
            return x
        return x[0]
    def ops_checkbox_checked(wid):
        selectedValue = opsCheckbox.outputs.layout.value
        if selectedValue:
            opsRow.show()
        else:
            opsRow.hide()
    def btnUpdate(btn, data):
        _, val = data
        s.process.keysDisplayer.handlers.defs.button_state_update(btn, data)
        _, _, isFolder = val
        if isFolder:
            btn.outputs.layout.icon = "folder"
        else:
            btn.outputs.layout.icon = ""
    def delete_clicked(wid):
        wid.description = "confirm"
        s.process.opsComp.views.okBtn.handlers.handle = delete_confirm
    def delete_confirm(btn):
        btn.description = "ok"
        key, val = s.process.opsComp.handlers.get_key_value()
        if key.strip() == "":
            raise IOError("Can not delete since the key is empty")
        key = s.process.keysDisplayer.keyValMap[key][2]
        s.process.model.delete(key)
        s.process.opsComp.handlers.clearFields()
        s.process.opsComp.views.okBtn.handlers.handle = delete_clicked
        s.handlers.render_keys()
    def opsChangedV2(wid):
        s.process.opsComp.handlers.defs.ops_changed(wid)
        ops = s.process.opsComp.views.opsType.outputs.layout.value
        if ops == "add":
            s.process.opsComp.views.okBtn.handlers.handle = s.handlers.defs.ok_func
        elif ops == "delete":
            s.process.opsComp.views.okBtn.handlers.handle = s.handlers.delete_clicked
    def set_model(model):
        s.process.model = model
        s.handlers.update_loc()
        s.handlers.render_and_update_ops_comp()
    def metaOpsChecked(wid):
        s.views.outputArea.outputs.layout.clear_output()
        if not s.views.metaOpsCheckbox.outputs.layout.value:
            return 
        if s.process.current_location is None:
            return
        data = s.process.keyValueModel.process.tools.handlers.read_meta(s.process.current_location) 
        dataCopied = copy.deepcopy(data)
        s.process.metaKeyValue.process.model.set_dictionary(dataCopied)
        s.process.metaKeyValue.process.kvsForMeta.handlers.render_and_update_ops_comp()
        typ = s.process.model.get_current_type()
        s.process.opsComponentUpdateFuncs[typ]()
        with s.views.outputArea.outputs.layout:
            display(s.process.metaKeyValue.views.container.outputs.layout)
    def readAll():
        return s.process.keyValueModel.process.model_inst.process.model_inst.process.vals
    opsComponentUpdateFuncs = {list: opsComponentUpdateForList, dict: opsComponentUpdateForDict}
    opsComp.views.opsType.handlers.handle = opsChangedV2
    opsComp.views.overwriteBox.handlers.handle = overwriteChecked
    goBackBtn.handlers.handle = goBackFunc
    keysDisplayer.views.btns.handlers.handle = btn_clicked
    opsComp.views.okBtn.handlers.handle = ok_func
    opsCheckbox.handlers.handle = ops_checkbox_checked
    keysDisplayer.views.container.outputs.layout
    keysDisplayer.handlers.name_getter = name_gtter
    keysDisplayer.handlers.button_state_update = btnUpdate
    metaOpsCheckbox.handlers.handle = metaOpsChecked
    opsRow.hide()
    s = ObMakr.uisOrganize(locals())
    update_loc()
    render_and_update_ops_comp()
    return s
def translateTool():
    testCase = {1: 2, 3: {4: "a", 5: {}}}
    expOutput = {'value': {1: {'value': 2, 'meta': {'type': int}},
      3: {'value': {4: {'value': 'a', 'meta': {'type': str}},
        5: {'value': {}, 'meta': {'type': dict}}},
       'meta': {'type': dict}}},
     'meta': {'type': dict}}
    def toMetaStruct(dic):
        newDic = {}
        if type(dic) == list:
            newDic["value"] = [toMetaStruct(x) for x in dic]
        elif type(dic) == dict:
            newDic["value"] = {k: toMetaStruct(dic[k]) for k in dic}
        else:
            newDic["value"] = dic
        newDic['meta']= {'type': type(dic)}
        return newDic
    def normalDicFromMetaStruct(dic):
        typ = dic["meta"]["type"]
        if typ == list:
            return [normalDicFromMetaStruct(x) for x in dic["value"]]
        elif typ == dict:
            return {k: normalDicFromMetaStruct(dic["value"][k]) for k in dic["value"]}
        else:
            return dic["value"]
    assert testCase == normalDicFromMetaStruct(toMetaStruct(testCase))
    assert toMetaStruct(testCase) == expOutput
    s = ObMakr.variablesAndFunction(locals())
    return s
def MetaKeyValuePair():
    prevFuncs = ObMakr.namespace()
    kvsForMeta = KeyValueSetter()
    prevFuncs.btn_clicked = kvsForMeta.process.keysDisplayer.views.btns.handlers.handle
    kvsForMeta.views.metaOpsCheckbox.outputs.layout.description = "refresh"
    model = KeyValueModel()
    kvsForMeta.handlers.set_model(model)
    addCancelBtns = AddCancelBtns()
    refreshAddCancelBtns = AddCancelBtns()
    container = Utils.container([kvsForMeta.views.container, addCancelBtns.views.container], className="flex flex-column")
    transTool = translateTool()
    def new_btn_clicked(tn):
        info = s.process.kvsForMeta.process.keysDisplayer.process.data[tn._parent.state.index]
        isFolder = info[-1]
        val = info[1]
        s.process.kvsForMeta.process.opsComp.handlers.set_value(val)
        s.process.prevFuncs.btn_clicked(tn)
    def cancelled(wid):
        s.process.parent.views.metaOpsCheckbox.outputs.layout.value = False
    def saved(w):
        vals = s.process.model._model._dic
        s.process.parent.process.keyValueModel.process.tools.handlers.write_meta(s.process.parent.process.current_location, vals, True)
        s.handlers.cancelled(w)
    def refreshItInBetween(w):
        s.process.kvsForMeta.views.outputArea.outputs.layout.clear_output()
        if not s.process.kvsForMeta.views.metaOpsCheckbox.outputs.layout.value:
            return
        with s.process.kvsForMeta.views.outputArea.outputs.layout:
            display(s.process.refreshAddCancelBtns.views.container.outputs.layout)
    def refreshIt(w):
        s.handlers.refreshCancelled(w)
    def refreshCancelled(w):
        s.process.kvsForMeta.views.metaOpsCheckbox.outputs.layout.value = False
        s.process.kvsForMeta.views.outputArea.outputs.layout.clear_output()
    def get_abs_loc(key):
        return s.process.kvsForMeta.process.model.get_current_location() + [key]
    def get_loc_id(loc, addEntry=False):
        return s.process.model.locIndexfunc.handlers.get_index(loc, addEntry)
    def write2model(key, vals):
        s.process.model.write(key, vals)
    def read_content(loc):
        return DicOps.get(s.process.model._model._dic, loc)
    def delete(loc):
        locNew = loc.copy()
        lastKey = locNew.pop()
        vals = s.handlers.read_content(locNew)
        del vals[lastKey]
    def set_dictionary(dic, transform=False):
        if transform:
            dic = s.process.transTool.handlers.toMetaStruct(dic)
        if len(dic) == 0:
            dic = s.process.transTool.handlers.toMetaStruct(dic)
        s.process.parent.process.model.set_dictionary(dic)
    def set_up():
        s.process.parent.handlers.set_dictionary = s.handlers.set_dictionary
        s.process.parent.handlers.toMetaStruct = s.process.transTool.handlers.toMetaStruct
        s.process.parent.handlers.normalDicFromMetaStruct = s.process.transTool.handlers.normalDicFromMetaStruct
    addCancelBtns.views.cancelBtn.handlers.handle = cancelled
    addCancelBtns.views.confirmBtn.handlers.handle = saved
    addCancelBtns.views.confirmBtn.outputs.layout.description = "save"
    kvsForMeta.process.keysDisplayer.views.btns.handlers.handle = new_btn_clicked
    kvsForMeta.views.metaOpsCheckbox.handlers.handle = refreshItInBetween
    refreshAddCancelBtns.views.cancelBtn.handlers.handle = refreshCancelled
    refreshAddCancelBtns.views.confirmBtn.handlers.handle = refreshIt
    s = ObMakr.uisOrganize(locals())
    operationManager = OperationManager()
    kvsForMeta.process.operationManager = operationManager
    operationManager.process.parent = kvsForMeta
    operationManager.handlers.set_up()
    operationManager.handlers.get_abs_loc = get_abs_loc
    operationManager.handlers.get_loc_id = get_loc_id
    operationManager.handlers.write2model = write2model
    operationManager.handlers.read_content = read_content
    operationManager.handlers.delete = delete
    return s
def MechanismForKeyValueSetter():
    callers = {}
    existsCaller = set()
    undoers = []
    prev_funcs = ObMakr.namespace()
    def btn_state_update_new(btn, info):
        s.process.prev_funcs.button_state_update(btn, info)
        if not s.handlers.exists(EventBasic.onFirstTimeRender, info):
            s.handlers.run(EventBasic.onFirstTimeRender, info, btn.outputs.layout)
        s.handlers.run(EventBasic.onRender, info, btn.outputs.layout)
    def caller_wrapper(w):
        for func in s.process.undoers:
            func(w)
    def new_btn_clicked(w):
        info = s.process.parent.process.keysDisplayer.process.data[w._parent.state.index]
        s.process.prev_funcs.btn_clicked(w)
        s.handlers.run(EventBasic.onClicked, info, w)
    def exists(keyType, info):
        key = str(info[0])
        locId = info[1][1][1]
        return (key, locId, keyType) in s.process.callers
    def set_file(file):
        s.process.prev_funcs.set_file(file)
        s.process.callers.clear()
        s.process.parent.handlers.render_keys()
    def run(keyType: EventBasic, info, btn=None):
        key = str(info[0])
        metaInfo = {}
        if keyType == EventBasic.onClicked:
            locId = info[1][1]
            metaInfo = info[1][0]["meta"]
        elif keyType == EventBasic.onFirstTimeRender:
            locId = info[1][1][1]
            metaInfo = info[1][1][0]["meta"]
        elif keyType == EventBasic.onRender:
            locId = info[1][1][1]
            metaInfo = info[1][1][0]["meta"]
        index = (key, locId, keyType)
        if index in s.process.callers:
            pass
        elif keyType.value in metaInfo:
            s.process.callers[index] = s.handlers.load(metaInfo[keyType.value])
        else:
            return
        s.process.callers[index].handlers.run(btn)
    def load(txt):
        exp = {}
        exec(txt, None, exp)
        res = exp["res"]
        if hasattr(res.handlers, "set_parent"):
            res.handlers.set_parent(s)
        return res
    def refreshIt(w):
        s.process.callers.clear()
        s.process.parent.process.metaKeyValue.process.refreshAddCancelBtns.views.cancelBtn.handlers.handle(w)
    def set_up():
        s.process.prev_funcs.btn_clicked = s.process.parent.process.keysDisplayer.views.btns.handlers.handle
        s.process.prev_funcs.button_state_update = s.process.parent.process.keysDisplayer.handlers.button_state_update
        s.process.parent.process.keysDisplayer.views.btns.handlers.handle = s.handlers.new_btn_clicked
        s.process.parent.process.keysDisplayer.handlers.button_state_update = s.handlers.btn_state_update_new
        s.process.parent.process.metaKeyValue.process.refreshAddCancelBtns.views.confirmBtn.handlers.handle = s.handlers.refreshIt
        s.process.prev_funcs.set_file = s.process.parent.process.keyValueModel.process.model_inst.handlers.set_file
        s.process.parent.process.keyValueModel.process.model_inst.handlers.set_file = s.handlers.set_file
    s = ObMakr.variablesAndFunction(locals())
    return s
def KeyValueComponentV2():
    mkvp = MetaKeyValuePair()
    mkvp.process.kvsForMeta.views.metaOpsCheckbox.hide()
    mkvp.process.addCancelBtns.views.container.hide()
    def doNothing(w):
        pass
    def set_dictionary(dic):
        s.process.mkvp.process.model.set_dictionary(dic)
        s.process.mkvp.process.kvsForMeta.handlers.render_keys()
    def readAll():
        return s.process.mkvp.process.kvsForMeta.process.model._model._dic
    def set_file(file):
        raise IOError("not implemented yet")
    def model_changed():
        pass
    mkvp.process.addCancelBtns.views.cancelBtn.handlers.handle = doNothing
    mkvp.process.addCancelBtns.views.confirmBtn.handlers.handle = doNothing
    container = mkvp
    container.process.model._model_changed = model_changed
    s = ObMakr.uisOrganize(locals(), ["ObMakr", "MetaKeyValuePair"])
    return s
class Main:
    def key_val_app_with_meta():
        kvs = KeyValueSetter()
        metaKeyValue = MetaKeyValuePair()
        kvs.process.metaKeyValue = metaKeyValue
        metaKeyValue.process.parent = kvs
        metaKeyValue.handlers.set_up()
        realtimeFunctionality = MechanismForKeyValueSetter()
        realtimeFunctionality.process.parent = kvs
        realtimeFunctionality.handlers.set_up()
        kvs.process.realtime = realtimeFunctionality
        operationManager = OperationManager()
        kvs.process.operationManager = operationManager
        operationManager.process.parent = kvs
        operationManager.handlers.set_up()
        return kvs
    def key_val_normal():
        kvc = KeyValueComponentV2()
        return kvc
    def key_val_with_search_and_sort():
        from timeline.t2024.experiments.keyValueWithSearchAndFilter import KeyValueWithSearchAndSort
        kv = KeyValueWithSearchAndSort()
        fileRow = kv.process.container.views.fileOpsRow
        kv.process.searchComp.views.container.pop()
        fileRow.append(kv.process.searchComp.views.selected)
        kv.process.searchComp.views.selected.handlers.handle = kv.handlers.dropDownSelectedSearch
        return kv
