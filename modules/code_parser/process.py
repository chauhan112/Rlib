from useful.OpsDB import IOps
import ast

class Ast2Dic(IOps):
    def setAstObj(self, ast_obj):
        self.ast_obj = ast_obj
    def setPyCode(self, code):
        import ast
        self.setAstObj(ast.parse(code))
    def execute(self):
        return self.get_dict(self.ast_obj)
    def get_dict(self, ast_body):
        if isinstance(ast_body, ast.AST):
            res = {'type': str(type(ast_body))}
            for key in ast_body.__dict__:
                res[key] = self.get_dict(ast_body.__dict__[key])
            return res
        elif type(ast_body) == list:
            res = []
            for ele in ast_body:
                res.append(self.get_dict(ele))
            return res
        return ast_body

import re
class PyCodeTools:
    def func_names(content):
        reg = r" *def (?P<name>.+)?\("
        import re
        funcs = []
        lines = content.splitlines()
        for i, line in enumerate(lines):
            match = re.compile(reg).search(line)
            if match:
                founds = match.groupdict()
                funcs.append((i, founds['name']))
        return funcs

    def class_names(content):
        reg = r" *class (?P<name>.\w+)?(\((?P<parents>.+)\))*"
        funcs = []
        lines = content.splitlines()
        for i, line in enumerate(lines):
            match = re.compile(reg).search(line)
            if match:
                founds = match.groupdict()
                funcs.append((i, founds['name'],founds['parents']))
        return funcs

class Tools:
    def printAst(code):
        import ast
        print(ast.dump(ast.parse(code), indent=2))
