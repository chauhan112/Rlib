class Value: # for having list, dic, set as values
    def __init__(self, al):
        self.val = al
    def __str__(self):
        if type(self.val) == str:
            return f'"{self.val}"'
        return str(self.val)
        
class NamespaceManager:
    def __init__(self):
        self._funcs = {}
    def getCode(vals, prefix = "app"):
        ins = NamespaceManager()
        txt = ins._getCode(vals, prefix=prefix)
        return ins.get_class() + txt
    def sort_assign(txt):
        import ast
        vals = ast.parse(txt)
        res = []
        for line in vals.body:
            if isinstance(line, ast.Assign):
                linestr = ast.unparse(line)
                trstr = ast.unparse(line.targets[0])
                keyLoc = trstr.split(".")
                res.append(keyLoc)
        return res
    
    def _getCode(self, vals, mapped = None, loc=None, res="", prefix = "app"):
        if res == "":
            res = f"{prefix} = NameSpace()\n"
        if mapped is None:
            mapped = set()
        if loc is None:
            loc = []
        if type(vals) == dict:
            for k in vals:
                loc.append(k)
                val = vals[k]
                if tuple(loc) not in mapped and (type(val) in [dict, list, set]):
                    res += ".".join([prefix] + loc) + " = NameSpace()\n"
                    mapped.add(tuple(loc))
                
                res = self._getCode(val, mapped, loc, res, prefix)
                loc.pop()
        elif type(vals) in [set, list]:
            for val in vals:
                func_name = f"{loc[-1]}_{val}"
                clsName = loc[0]
                if clsName not in self._funcs:
                    self._funcs[clsName] = []
                self._funcs[clsName].append(func_name)
                res += ".".join([prefix] + loc + [val]) + f" = {clsName}.{func_name}\n"
                # res += ".".join([prefix] + loc + [val]) + f" = None\n"
        else:
            res += ".".join([prefix] + loc) +  " = " + str(vals) + "\n"
        return res
    
    def get_class(self):
        txt = ""
        for clsn in self._funcs:
            space = ""
            txt += f"class {clsn}:\n"
            space += " "* 4
            for fun in self._funcs[clsn]:
                txt += space + f"def {fun}():\n"
                txt += space*2 + f"pass\n"
        return txt