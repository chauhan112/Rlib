from modules.Explorer.model import IExplorer
import ast
class AstExplorer(IExplorer):
    def __init__(self):
        self._cur_map = None
    def cd(self, key):
        self._pos.append(self._cur_map[key])
    def dirList(self):
        val: ast.AST = self._pos[-1]
        not_fields = []
        if type(val) == list:
            self._cur_map = {str(n): n for n in val}
        elif isinstance(val, ast.AST) :
            self._cur_map = {}
            for v in val._fields:
                value = val.__getattribute__(v)
                if isinstance(value, ast.AST) or (type(value) == list and len(value) != 0):
                    self._cur_map[v] = value
            not_fields = filter(lambda x: not (x.startswith("_") or x in self._cur_map), dir(val))
        fields = list(self._cur_map.keys())
        return list(fields), list(not_fields)
    def goBack(self):
        if len(self._pos)> 1:
            self._pos.pop()
    def set_model(self, ast_model: ast.AST):
        self._model = ast_model
        self._pos = [self._model]
    def set_content(self, content: str):
        self._content = content
        self.set_model(ast.parse(content))
    def set_file(self, file: str):
        from FileDatabase import File
        self._file_path = file
        self.set_content(File.getFileContent(file))

class MyAstAttributeExplorer(IExplorer):
    def __init__(self):
        self._cur_map = None
        self.set_method_name("get_classes")
        self.set_name_func(self._default_name_func)
    def set_content(self, content: str):
        from modules.code_parser.ast_parser import Main as ParserMain
        self._content = content
        self.set_model(ParserMain.parse(content))
    def set_file(self, file:str):
        from modules.code_parser.ast_parser import Main as ParserMain
        self._file = file
        self.set_model(ParserMain.parse(file_path=file))
    def set_model(self, model):
        self._model = model
        self._pos = [self._model]
    def set_method_name(self, name: str):
        self._method =name
        if name == "get_imports":
            self.set_name_func(lambda x: x)
        elif name == "get_dependency":
            self.set_name_func(lambda x: x[0])
    def cd(self, key):
        self._pos.append(self._cur_map[key])
    def dirList(self):
        if self._method not in dir(self._pos[-1]):
            return [], []
        self._cur_map = {self._func(m): m for m in self._pos[-1].__getattribute__(self._method)()}
        folders = []
        files = []
        for key in self._cur_map:
            val = self._cur_map[key]
            if self._method in dir(val):
                if len(val.__getattribute__(self._method)()) != 0:
                    folders.append(key)
                else:
                    files.append(key)
            else:
                files.append(key)
        return folders, files
    def goBack(self):
        if len(self._pos) > 1:
            self._pos.pop()
    def set_name_func(self, func):
        self._func = func
    def _default_name_func(self,att):
        return att.get_name()

class Main:
    def _file_select(a):
        val = ae._pos[-1].__getattribute__(a)
        out = exp._wid.components.outputDisplay
        out.clear_output()
        with out:
            print(val)
    def ast_explorer(content: str=None, path: str=None):
        from modules.Explorer.DictionaryExplorer import Main as EMain
        ae = AstExplorer()
        if content is None:
            ae.set_file(path)
        else:
            ae.set_content(content)
        exp = EMain.explore(ae, displayit=False)
        exp.set_on_file_selected(Main._file_select)
        exp.display()
        return exp
    
    def my_ast_explorer(path):
        ae = AstAttributeExplorer()
        ae.set_file(path)
        from modules.Explorer.DictionaryExplorer import Main as EMain
        return EMain.explore(ae)