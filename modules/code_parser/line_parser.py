class ILineParser:
    def checker(self):
        pass
    def get(self):
        pass

from useful.RegexDB import RegexDB, NameDicExp

class GLine(ILineParser, GDataSetable):
    def __init__(self, reg:NameDicExp):
        self.reg = reg
    def checker(self):
        line = self.data
        self.found = RegexDB.group_name_search(self.reg, line)
        return len(self.found) != 0
    def get(self):
        return self.found

class ClassLine(GLine):
    def __init__(self):
        reg = NameDicExp(
                NameDicExp('', 'spaces', ' *', 'class '),
                'cls_name', '.+?',
                NameDicExp('(\(', 'base', '.*', '\))*:'))
        super().__init__(reg)

class FuncDefLine(GLine):
    def __init__(self):
        reg = NameDicExp(
                NameDicExp('', 'spaces', " *", 'def '),
                'func', '.+?',
                NameDicExp('\(', 'params', '.*', '\):')
            )
        super().__init__(reg)

class UsesCallLine(GLine):
    def __init__(self):
        reg = NameDicExp(NameDicExp('', 'spaces', " *", '.*=* '),'uses', '([a-zA-Z0-9]+\(*\)*\.)+.*\(\)', '.*')
        super().__init__(reg)

class Statement(GLine):
    def __init__(self):
        reg = NameDicExp(NameDicExp('', 'spaces', " *", ''),'statement', '.*', '')
        super().__init__(reg)
    def checker(self):
        super().checker()
        return '=' not in self.data

class Assignment(GLine):
    def __init__(self):
        reg = NameDicExp(NameDicExp('', 'spaces', " *", ''),'left', '.*?', NameDicExp(' *= *', 'right', '.*',''))
        super().__init__(reg)