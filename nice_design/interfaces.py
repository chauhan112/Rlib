class IDatabaseGUI:
    def display(self):
        raise NotImplementedError("abstract method")

class IAbout:
    def display_info(self):
        raise NotImplementedError("abstract method")

class ClassNode:
    def __init__(self):
        self.cls = className
        self.ins = None
        self.key = None
        self.search_words = ""
class LazyInstantiate:
    def __init__(self):
        self._db_map = {}
    def get_db(self, key):
        if key not in self._db_map:
            self._db_map[key] = self._ops[key]()
        return self._db_map[key]
    def set_ops_map(self, ops_map: dict):
        self._ops = ops_map