dic = {'model': {'scope': None,
  'tables': {'loggerData': ['read', 'create', 'delete', 'update', "readAll"],
   'logger': {'columns': ['read', 'create', 'delete', 'update', "readAll"],
    'readAll': {}},
   'metaInfo': {'add', 'delete', 'read', 'update'}},
  'viewModel': {'logger': {}, 'loggerData': {}, 'history': {}},
                "constants": {"strings":{}}},
 'views': {'logger': {'groups': {}, 'main': {}},
  'loggerData': {'groups': {}, 'main': {}},
  'layout': {},
  'extraUis': {'btnConfirm', 'output'}},
 'controllers': {'logger': {},
  'loggerData': {'nameDecider'},
  'wrappers': {'logger': {}, 'loggerData': {}}, "instances": {}},
      }


class NamespaceManager:
    def getCode(vals, mapped = None, loc=None, res="", prefix = "app"):
        if mapped is None:
            mapped = set()
        if loc is None:
            loc = []
        if type(vals) == dict:
            for k in vals:
                loc.append(k)
                if tuple(loc) not in mapped:
                    res += ".".join([prefix] + loc) + " = NameSpace()\n"
                    mapped.add(tuple(loc))
                val = vals[k]
                res = NamespaceManager.getCode(val, mapped, loc, res, prefix)
                loc.pop()
        elif type(vals) in [set, list]:
            for val in vals:
                res += ".".join([prefix] + loc + [val]) + " = None\n"
        else:
            res += ".".join([prefix] + loc) +  " = " + str(vals) + "\n"
        return res
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
