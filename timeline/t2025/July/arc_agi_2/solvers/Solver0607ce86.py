import numpy as np
import random
from ...arc_agi_2 import ObjMaker
from ..tools import ArrayTools, Field
# case1: we know the shape of the object
def prev_code():
    def numSize(row):
        s = 0
        for v in row:
            if v != 0:
                s += 1
        return s
    def scan_row(row, exp_row_size, errorAllowed = .2):
        candidates = {}
        j = 0
        while True:
            val = row[j]
            if val != 0:
                nr = row[j: j+exp_row_size]
                if abs(numSize(nr) - exp_row_size) < errorAllowed*exp_row_size:
                    candidates[j] = nr
            j += 1
            if j + exp_row_size > len(row):
                break
        return candidates
    def similarity_count(row1, row2):
        sc = 0
        for i in range(len(row1)):
            if row1[i] == row2[i]:
                sc += 1
        return sc
    def get_suitable_candidates_for_id(candidates, idx, keyFunc = None):
        fvc = {}
        for index in candidates:
            rw = candidates[index]
            if keyFunc is not None:
                key = keyFunc(rw)
            else:
                key = f"{rw[idx]}-{rw[(idx+1) % len(rw)]}"
                # key = rw[idx]
            if key not in fvc:
                fvc[index] = 0
            fvc[index] += 1
        return sorted(fvc, key=fvc.get)
        
    def get_suitable_candidates(candidates, row_size ):
        k=round((row_size + 1)/2)
        idxs = random.sample(range(row_size), k, )
        res = []
        for idx in idxs:
            cand = get_suitable_candidates_for_id(candidates, idx)
            res.append(set([x[0] for x in cand]))
        
        counts = {}
        for c in res:
            for k in c:
                if k not in counts:
                    counts[k] = 0
                counts[k] += 1
        
        return set(filter( lambda x: counts[x] >= (k/2), counts))
    def get_suitable_candidates_2(candidates ):
        sc = {}
        for i in range(len(candidates)):
            idx1, can1 = candidates[i]
            for j in range(i+1, len(candidates)):
                idx2, can2 = candidates[j]
                sc[(idx1, idx2)] = similarity_count(can1, can2)
        return sc
    def get_n_rows(grid, n, row_size):
        i = 0
        res = []
        fc = 0
        while True:
            candidates =scan_row(grid[i], row_size)
            if len(candidates) > 0:
                fc += 1
                res.append(grid[i])
            i += 1
            if i >= len(grid):
                break
            if fc >= n:
                break
        return res
    def get_row_indices(grid, row_size):
        krows =  get_n_rows(grid, row_size*2, row_size)
        rowIdx = random.sample(range(len(krows)), k=round((row_size + 1)/2))
        candidatesIndexs = []
        for idx in rowIdx:
            candidates =scan_row(krows[idx], row_size)
            candidatesIndexs.append(set(get_suitable_candidates(candidates, row_size)))
        return set.intersection(*candidatesIndexs)
def Solver0607ce86():
    def twoDMask(arr, checkFunc):
        return [rowMask(rr, checkFunc) for rr in arr]
    def rowMask(arr, checkFunc):
        res =[]
        for i, v in enumerate(arr):
            if checkFunc([i, v]):
                res.append(1)
            else:
                res.append(0)
        return res
    def indices(grid):
        maskedArr = twoDMask(grid, lambda x: x[1] > 0)
        arr = np.array(maskedArr)
        narr = arr.sum(axis=0)
        mx = narr.max()
        halfMax = mx//2
        rm =rowMask(narr, lambda x: x[1] > halfMax)
        res = []
        inside = False
        sizeCounter = 0
        sizes = []
        for i in range(len(rm)):
            v = rm[i]
            if v != 0:
                if not inside:
                    inside = True
                    res.append(i)
                sizeCounter += 1
            else:
                if inside:
                    sizes.append(sizeCounter)
                    sizeCounter = 0
                inside = False
        
        return res, sizes[0]
    def get_max_count(arr):
        counts = dict.fromkeys(arr, 0)
        for v in arr:
            counts[v] += 1
        return max(counts, key=counts.get)
    def solve(inp):
        cols, cs = indices(inp)
        rows, rs = indices(ArrayTools.transpose(inp))
        perfectObj = [[[] for _ in range(cs)] for _ in range(rs)]
        for r in rows:
            for c in cols:
                for i in range(rs):
                    for j in range(cs):
                        perfectObj[i][j].append(inp[r+i][c+j])
        for i, row in enumerate(perfectObj):
            for j, col in enumerate(row):
                perfectObj[i][j] = get_max_count(col)
        res = Field([])
        res.set_shape(ArrayTools.shape(inp))
        pobj = Field(perfectObj)
        for r in rows:
            for c in cols:
                res.place((r, c), pobj)
        return res
    s = ObjMaker.variablesAndFunction(locals())
    return s