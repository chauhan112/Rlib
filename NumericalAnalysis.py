from ListDB import ListDB
import numpy as np
from MarkdownToolsDB import MarkdownToolsDB as m

class NumericalAnalysis:
    def bisectionFormula(func,interval,tolerance = 1e-6, maxIter = 1e6):
        def sign(a):
            if(a > 0):
                return 1
            elif(a < 0):
                return -1
            return 0
        l, u = interval
        traker = {}
        traker[sign(func(l))] = l
        traker[sign(func(u))] = u
        if(len(traker) != 2):
            raise IOError("Values of interval must lie on different region of the XY plane")
        count = 1 
        while True:
            l,u = list(traker.values())
            avg = (l+u)/2
            val = func(avg)
            if( abs(val) < tolerance or count > maxIter):
                break
            traker[sign(val)] = avg
            count +=1
        return avg
            
    def sympySyntax():
        from Database import Database
        syntaxes = {
            'unknown function' : "d = symbols(\"d\" , cls = Function)",
            'symbol' : "x = symbols('x')",
            'symbols': "x,y,z = symbols('x y z')",
            'integrate': ""
        }   
        return Database.dicDB(syntaxes)

    def newtonMethod(f, df, tolerance = 1e-6, initialValue = 0, maxIter = 1e6):
        x = initialValue
        count = 1
        while True:
            val = f(x)
            if( abs(val) < tolerance or count > maxIter):
                break
            x = x - f(x)/df(x)
            count += 1
            print(count)
        print(f"iterated: {count}")
        return x
            
    def Newton_Interpolationspolynom():
        pass
    
    def getMatrix(matStr, oneDigit = False, printed = False):
        from WordDB import WordDB
        matStr = matStr.strip().replace("−", "-").split("\n")
        regex = "[0-9\-\+]+"
        if(oneDigit):
            regex = "\-*\d"
        arr = [[val[i:j] for i, j in WordDB.searchWordWithRegex(regex, val)] for val in matStr]
        
        if(not printed):
            m.dispjoin(m.matrix(arr))
        else:
            k = ",\n".join(["[" + ",".join(row)+ "]" for row in arr])
            print(f"[{k}]")
        
    def multiply(a, b):
        a = np.array(a)
        b = np.array(b)
        return a.dot(b)

    def getPermutationMatrix(arr):
        permutationArr = NumericalAnalysis.permute(arr) - 1
        dim = len(arr) + 1 
        iden = np.array([[float(i == j) for i in range(dim)] for j in range(dim)])
        return iden[permutationArr].T   

    def permute(arr):
        arr = np.array(arr) - 1
        newArr = list(range(len(arr) + 1))
        for i in range(len(arr)):
            if(arr[i] == i):
                continue
            a = newArr[i]
            newArr[i] = newArr[arr[i]]
            newArr[arr[i]] = a
        return np.array(newArr) + 1

    def jacobiInterativeSolution(funcs, initialValues, nrIterations = 10):
        vals = initialValues
        print(f"Intial values:")
        print(vals)
        lastValue = vals
        for i in range(nrIterations):
            newVals = []
            for j, f in enumerate(funcs):
                arr = [val for k, val in enumerate(vals) if k != j]
                newVals.append(f(*arr))
            vals = newVals
            print(f"Iterations {i+1} :")
            print(vals)
            if(abs(sum([j- i for j,i in zip(vals, lastValue) ])) < 1e-4):
                break
            lastValue = vals
        return vals
    
    def getLinks(word, case = False):
        impLinks = {
            "LU decomposition":"http://people.duke.edu/~ccc14/sta-663-2016/08_LinearAlgebra2.html",
            "algorithm archive": "https://www.netlib.org/"
        }
        ListDB.searchInDic(word, impLinks, case)
    
    def lu_decompose(matrix):
        import scipy
        return scipy.linalg.lu(matrix)

class CountingTools:
    def permutation(lst, n = None): 
        if(n is None):
            n = len(lst)
        from itertools import permutations
        return list(permutations(lst, n))

    def combination(lst, r = None):
        if(r is None):
            r = len(lst)
        from itertools import combinations 
        return list(combinations(lst, r)) 
    
    