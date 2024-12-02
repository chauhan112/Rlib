import numpy as np
def p007bbfb7(inp):
    def fill(x,y):
        for i, row in enumerate(inp):
            for j, v in enumerate(row):
                out[x*3 + i][y*3+j] = v
    out = [[0]* 9 for i in range(9)]
    for i, row in enumerate(inp):
        for j, v in enumerate(row):
            if v != 0:
                fill(i, j)
    return out
def equal(arr1, arr2):
    if (len(arr1) != len(arr2)):
        return False
    for arr1row, arr2row in zip(arr1, arr2):
        if len(arr1row) != len(arr2row):
            return False
        for v1,v2 in zip(arr1row, arr2row):
            if v1 != v2:
                return False
    return True
def npEqual(arr1, arr2):
    return np.array_equal(np.array(arr1), np.array(arr2))
def verifyMySolution(solutionFunc, data):
    trains = data["train"]
    res = True
    for qu in trains:
        inp = qu["input"]
        out = qu["output"]
        res = res and npEqual(solutionFunc(inp), out)
    return res
    
def get_unequal_dim_questions(data):
    d = data
    res = []
    i = "input"
    o = "output"
    t = "train"
    te = "test"
    for k in d:
        pd = d[k]
        tds = pd[t]
        for td in tds:
            if np.array(td[i]).shape != np.array(td[o]).shape:
                res.append(k)
                break
    return res