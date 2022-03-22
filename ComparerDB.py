from WordDB import WordDB
from InterfaceDB import ISearchSystem
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
            return ComparerDB.regexSearch(word, content)
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
    def pickle_search(data, compareFunc, loc=[], searchInKey=False):
        founds = []
        if type(data) == dict:
            for key in data:
                if searchInKey and compareFunc(key):
                    founds.append((loc + [key], data[key]))
                founds += ComparerDB.pickle_search(data[key], compareFunc, loc + [key], searchInKey)
        elif type(data) in [list, set]:
            for i, val in enumerate(data):
                founds += ComparerDB.pickle_search(val, compareFunc, loc + [i], searchInKey)
        else:
            if compareFunc(data):
                founds.append((loc, data))
        return founds
    def default_compare(word, con):
        if type(con) == str and type(word) == str:
            return word in con
        return word == con