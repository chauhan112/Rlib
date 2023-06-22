from enum import Enum
class FuncType(Enum):
    Method = 1
    Function = 2
    Variable = 3
class ClassProperties:
    def get_type(ins, name):
        def adasd():
            pass
        class M:
            def add(self):
                pass
            def aa():
                pass
        mm = M()
        
        if type(getattr(mm, "add")) == type(getattr(ins, name)):
            return FuncType.Method
        elif type(adasd) == type(getattr(ins, name)):
            return FuncType.Function
        else:
            return FuncType.Variable