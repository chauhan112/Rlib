from useful.WordDB import WordDB
import re
class ComparerDB:
    def inCompare(leftIn, right, case = False):
        if(not case):
            leftIn = leftIn.lower()
            right = right.lower()
        return leftIn in right
    def regexSearch(regex, word):
        return WordDB.regexMatchFound(regex, word)
    def has(word, content, case = False, reg = False):
        if(reg):
            return re.search(word,content) != None
        return ComparerDB.inCompare(word, content, case)
    def hasExtension(file, exts):
        if(type(exts) == str):
            exts = [exts]
        tr = False
        for ext in exts:
            tr = tr or file.endswith("." + ext) or file.endswith("." + ext.upper())
        return tr
    def lineSearch(word, content, case = True, reg = False, firstOnly = True):
        if(type(content) == str):
            content = content.splitlines()
        res = []
        for j in range(len(content)):
            if(ComparerDB.has(word, content[j], case, reg)):
                if(firstOnly):
                    res.append(j)
                    break
                else:
                    res.append(j)
        return res
    def pickle_search(data, compareFunc, loc=[], searchInKey=False, founds =None):
        if founds is None:
            founds = []
        if type(data) == dict:
            for key in data:
                if searchInKey and compareFunc(key):
                    founds.append((loc + [key], data[key]))
                ComparerDB.pickle_search(data[key], compareFunc, loc + [key], searchInKey, founds)
        elif type(data) in [list, set]:
            for i, val in enumerate(data):
                ComparerDB.pickle_search(val, compareFunc, loc + [i], searchInKey, founds)
        else:
            if compareFunc(data) and (loc, data) not in founds :
                founds.append((loc, data))
        return founds
    def default_compare(word, con):
        if type(con) == str and type(word) == str:
            return word in con
        return word == con

class SearchInDictionary:
    def __init__(self,):
        self.set_search_func(self._default_search)
        self.set_search_in_key_also(False)
    def set_search_in_key_also(self, ke):
        self._in_key_only = ke
    def set_dic(self, dic):
        self._data = dic
    def set_search_func(self, func):
        self._func = func
    def _default_search(self, word, container):
        if type(container) == str and type(word) == str:
            return ComparerDB.has(word, container,self._case, self._reg)
        return word == container
    def search(self, word, case=False, reg= False):
        self._reg = reg
        self._case = case
        return ComparerDB.pickle_search(self._data, lambda x: self._func(word, x),searchInKey=self._in_key_only,)
