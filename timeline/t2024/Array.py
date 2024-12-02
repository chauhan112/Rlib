class Array:
    def __init__(self, arr):
        self.array = arr
    def map(self, func):
        if type(func) == list:
            self._funcs = func
            return Array(list(map(self.funcToIter, self.array)))
        return Array(list(map(func, self.array)))
    def funcToIter(self, ele):
        res = ele
        for fun in self._funcs:
            res = fun(res)
        return res
    def filter(self, func):
        if type(func) == list:
            self._funcs = func
            return Array(list(filter(self.funcToIter, self.array)))
        return Array(list(filter(func, self.array)))
    def index(self):
        return Array(list(zip(range(len(self.array)), self.array)))
    def reshape(self, size:int):
        col = len(self.array) // size
        from ListDB import ListDB
        return Array(ListDB.reshape(self.array, (col, size)))
    def count(self):
        return len(self.array)
    def sum(self):
        return sum(self.array)
    def join(self, sep):
        return sep.join(self.array)
    def toDict(self, keyFunc, valueFunc):
        return Dictt({keyFunc(k): valueFunc(k) for k in self.array})
    def sort(keyFunc = None):
        return Array(sorted(self.array, key= keyFunc))

class Dictt:
    def __init__(self, dic):
        self.dic = dic
    def values(self):
        return Array(list(self.dic.values()))
    def keys(self):
        return Array(list(self.dic.keys()))
    def sortKeys(self):
        return Dictt({k: self.dic[k] for k in sorted(self.dic)})
    def sortValues(self):
        return Dictt({ k: v for k, v in sorted(self.dic.items(), key=lambda item: item[1]) })
    def reverseKeyValue(self):
        return Dictt({self.dic[k]: k for k in self.dic})