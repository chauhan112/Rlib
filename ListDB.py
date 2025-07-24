from WordDB import WordDB
from ComparerDB import ComparerDB
class ListDB:
    def sortDicBasedOnValue(dic):
        return { k: v for k, v in sorted(dic.items(), key=lambda item: item[1]) }
    def sorted_keys(arr):
        import numpy as np
        return np.argsort(arr)
    def reshape(arr, shape):
        from functools import reduce
        from operator import mul

        class Temp:
            def multiply(shape):
                t = 1
                for s in shape:
                    t *= s
                return t

        if Temp.multiply(shape) != len(arr):
            raise IOError("shape mismatched")

        if len(shape) == 1:
            return arr
        n = reduce(mul, shape[1:])
        return [ListDB.reshape(arr[i*n:(i+1)*n], shape[1:]) for i in range(len(arr)//n)]

    def listMap(func, container):
        return list(map(func, container))

    def listFilter(func, arr):
        return list(filter(func, arr))

    def flatten(arr):
        newArr = []
        for row in arr:
            if( type(row ) not in [list, tuple]):
                newArr.append(row)
            else:
                newArr += ListDB.flatten(row)
        return newArr

    def dicTo2dArray(dic):
        res = []
        for key in dic:
            res.append([key, dic[key]])
        return res

    def keepUnique(redundantElementsList, orderImportant = False):
        if(orderImportant):
            return ListDB._keepUniqueNOrder(redundantElementsList)
        return list(set(redundantElementsList))

    def _keepUniqueNOrder(redundantElementsList):
        seen = set()
        seen_add = seen.add
        return [x for x in redundantElementsList if not (x in seen or seen_add(x))]

    def reList(container, copyIt = True):
        # see TestDB for example and uses
        from ancient.ClipboardDB import ClipboardDB
        from RegexDB import RegexDB
        if(isinstance(container, str)):
            container = container.splitlines()
        temp = list(map(lambda x: RegexDB.regexSearch(RegexDB.lookAhead("\d\. ", ".*"),x)[0], container))
        result = [str(i + 1)+ ". " + val for i, val in enumerate(temp)]
        if(copyIt):
            ClipboardDB.copy2clipboard("\n".join(result))
        return result

    def branchPath(dic, maxLevel = None, currentLevel = 1):
        # see TestDB for example
        res = []
        if(maxLevel is not None):
            if(currentLevel == maxLevel):
                return [[k] for k in(dic.keys())]
        for k in dic:
            if(isinstance(dic[k], dict)):
                [res.append([k] + ele) for ele in ListDB.branchPath(dic[k], maxLevel, currentLevel + 1)]
            else:
                res.append([k])
        return res

    def dicOps():
        class Dic:
            def add(dic, loc, val):
                locStr = Dic._toLocStr(loc)
                exec(f"dic{locStr} = val")
            def get(dic, loc):
                val = dic
                for x in loc:
                    val = val[x]
                return val
            def delete(dic, loc):
                val = Dic._toLocStr(loc)
                exec(f"del dic{val}")
            def flatten(dic):
                newDic = {}
                for key in dic:
                    if(type(dic[key]) == dict):
                        temp = Dic.flatten(dic[key])
                        newDic.update(temp)
                    else:
                        newDic[key] = dic[key]
                return newDic

            def flatten2(nested):
                import collections
                for key, value in nested.items():
                    if isinstance(value, collections.Mapping):
                        for inner_key, inner_value in flatten2(value):
                            yield inner_key, inner_value
                    else:
                        yield key, value

            def addEvenKeyError(dic, loc, val):
                subDic = dic
                for key in loc:
                    try:
                        subDic[key]
                    except:
                        subDic[key] = {}
                    subDic = subDic[key]
                ListDB.dicOps().add(dic, loc, val)

            def sizeOfDicInBytes(dic):
                import gc
                import sys

                def get_obj_size(obj):
                    marked = {id(obj)}
                    obj_q = [obj]
                    sz = 0
                    while obj_q:
                        sz += sum(map(sys.getsizeof, obj_q))
                        all_refr = ((id(o), o) for o in gc.get_referents(*obj_q))
                        new_refr = {o_id: o for o_id, o in all_refr if o_id not in marked and not isinstance(o, type)}
                        obj_q = new_refr.values()
                        marked.update(new_refr.keys())
                    return sz
            def reverseKeyValue(mainDic):
                dic = {}
                for k in mainDic:
                    for v in mainDic[k]:
                        if(v in dic):
                            print(v+" already exists")
                        else:
                            dic[v] = k
                return dic
            def mapDictValues(dic, func):
                newDic = {}
                for key in dic:
                    if type(dic[key]) == dict:
                        newDic[key] = ListDB.dicOps().mapDictValues(dic[key], func)
                    else:
                        newDic[key] = func(dic[key])
                return newDic
            def _toLocStr(loc):
                locStr = ""
                for l in loc:
                    if(type(l) == str):
                        locStr += "["+ f"\"{l}\"]"
                    else:
                        locStr += "["+ str(l) + "]"
                return locStr
            def depth_calculator(dic, depth = 0 ):
                maxDep = depth
                if type(dic) == dict:
                    for ke in dic:
                        newdp = Dic.depth_calculator(dic[ke], depth + 1)
                        if maxDep < newdp:
                            maxDep = newdp
                return maxDep
        return Dic
    def dic_iterator(dic, res = [], res_append_checker = lambda x, cont: True,
                 parent_val = False, leaf_checker = lambda x: True):
        if type(dic) == dict:
            for k in dic:
                val = dic[k]
                parent_val =  res_append_checker(k,dic)
                ListDB.dic_iterator(val, res,  res_append_checker, parent_val)
        elif type(dic) == list:
            for i,val in enumerate(dic):
                parent_val =  res_append_checker(val, dic)
                ListDB.dic_iterator(val, res,  res_append_checker, parent_val)
        else:
            if parent_val and leaf_checker(dic):
                res.append( dic)
        return res
