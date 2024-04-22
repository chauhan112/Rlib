import logging
from datetime import datetime
class NameSpace:
    pass
class BasicController:
    def __init__(self) -> None:
        self.controllers = NameSpace()
        self.views = NameSpace()
    def set_model(self, model):
        self._model = model
    def set_scope(self, scope):
        self._scope = scope
class LoggerSystem:
    def __init__(self):
        self.set_level(logging.INFO)
    def set_level(self, lvl):
        self.logLevel = lvl
    def log(self, lvl, info):
        now = datetime.now()
        if lvl >= self.logLevel:
            print(now.strftime("%d.%m.%Y %H:%M:%S"), info)
    def logFunctionName(self, inst):
        if lvl >= self.logLevel:
            print(now.strftime("%d.%m.%Y %H:%M:%S"), info)
class ObjectOps:
    def make_obj():
        return NameSpace()
    def getter(obj, loc):
        val = obj
        for key in loc:
            val = getattr(val, key)
        return val
    def setter(obj, loc, val):
        if len(loc) == 0:
            return 
        innerObj = ObjectOps.getter(obj, loc[:-1])
        key = loc[-1]
        setattr(innerObj, key, val)
    def exists(obj, loc):
        val = obj
        for key in loc:
            if not hasattr(val, key):
                return False
            val = getattr(val, key)
        return True
    def setEvenIfItdoesNotExist(obj, loc, val):
        if len(loc) == 0:
            return 
        newLoc = loc[:-1]
        innerObj = obj
        for key in newLoc:
            if not ObjectOps.exists(innerObj, [key]):
                ObjectOps.setter(innerObj, [key], ObjectOps.make_obj())
            innerObj = getattr(innerObj, key)
        key = loc[-1]
        setattr(innerObj, key, val)
    def delete(obj, loc):
        if len(loc) == 0:
            return 
        innerObj = ObjectOps.getter(obj, loc[:-1])
        key = loc[-1]
        delattr(innerObj, key)
    def add_to_namespace(obj, keyValsAsList):
        """keyValsAsList : [[["key", "key2"], val],[["key2", "key2"], val2]]"""
        for loc, val in keyValsAsList:
            ObjectOps.setEvenIfItdoesNotExist(obj, loc, val)
            
def addToNameSpace(obj, dictVals, ignoring= []):
    import inspect
    from timeline.t2024.ui_lib.IpyComponents import BaseComponentV2
    for key in dictVals:
        if key in ignoring:
            continue
        val = dictVals[key]
        if inspect.isclass(val):
            pass
        elif inspect.isfunction(val):
            ObjectOps.setEvenIfItdoesNotExist(obj, ["handlers", key], val)
            ObjectOps.setEvenIfItdoesNotExist(obj, ["handlers", "defs", key], val)
        elif isinstance(val, BaseComponentV2):
            ObjectOps.setEvenIfItdoesNotExist(obj, ["views", key], val)
            if val.inputs.parent is None:
                val.inputs.parent = obj
        else:
            ObjectOps.setEvenIfItdoesNotExist(obj, ["process", key], val)
    ObjectOps.setEvenIfItdoesNotExist(obj, ["local_states"], dictVals)

class Main:
    def dicToNamespace(dictVals, obj = None):
        if obj is None:
            obj = ObjectOps.make_obj()
        for key in dictVals:
            val = dictVals[key]
            if isinstance(val, dict):
                Main.dicToNamespace(val)
                ObjectOps.setEvenIfItdoesNotExist(obj, [key], Main.dicToNamespace(val))
            else:
                ObjectOps.setEvenIfItdoesNotExist(obj, [key], val)
        return obj
    def dicToNamespaceWithIgnores(dictVals, obj = None, ignores= []):
        newDict= {key: dictVals[key] for key in dictVals if key not in ignores}
        return Main.dicToNamespace(newDict, obj)
    def variablesAndFunction(dictVals, ignoring= [], obj=None):
        if obj is None:
            obj = ObjectOps.make_obj()
        import inspect
        for key in dictVals:
            if key in ignoring:
                continue
            val = dictVals[key]
            if inspect.isclass(val):
                pass
            elif inspect.isfunction(val):
                ObjectOps.setEvenIfItdoesNotExist(obj, ["handlers", key], val)
                ObjectOps.setEvenIfItdoesNotExist(obj, ["handlers", "defs", key], val)
            else:
                ObjectOps.setEvenIfItdoesNotExist(obj, ["process", key], val)
        ObjectOps.setEvenIfItdoesNotExist(obj, ["local_states"], dictVals)
        return obj
    def uisOrganize(dictVals, ignoring= [], obj=None):
        if obj is None:
            obj = ObjectOps.make_obj()
        addToNameSpace(obj, dictVals, ignoring)
        if not ObjectOps.exists(obj, ["process"]): 
            obj.process = ObjectOps.make_obj()
        return obj