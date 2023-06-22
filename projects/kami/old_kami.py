import random
from collections import deque
import pixiedust
import numpy as np
def getMinimalCoverage(conn):
    minCov = set([])
    for key in conn:
        for val in conn[key]:
            pair = [key, val]
            pair.sort()
            minCov.add(tuple(pair))
    return minCov

def colorSelector(rel, val):
    g = {}
    for nebor in rel.getNebors(val):
        try:
            g[colorMap[nebor]] +=  1
        except:
            g[colorMap[nebor]] = 1
    sorted_g = {k: v for k, v in sorted(g.items(), key=lambda item: item[1], reverse = True)}
    for key in sorted_g:
        yield key

def optionSelector(rel):
    minKeyGroup = getMinkey(rel)
    for min_ in minKeyGroup:
        g = {}
        for i in min_:
            g[i] = len(rel.getNebors(i))

        sorted_g = {k: v for k, v in sorted(g.items(), key=lambda item: item[1], reverse = True)}
        for key in sorted_g:
            yield key

def getMinkey(rel):
    groups = grouper(rel)
    sorted_groups = {k: v for k, v in sorted(groups.items(), key=lambda item: item[0])}
    for key in sorted_groups:
        yield sorted_groups[key]

def getLevel(rel,r_v):
    k = {}
    lvl = 0
    children = [r_v]
    goneThrough = []

    while len(children) != 0:
        temp = children 
        children = []
        for i in temp:
            if (i not in goneThrough):
                k[i] = lvl
                goneThrough.append(i)
                children += rel.getNebors(i)
        lvl += 1
    return k, lvl-1

def grouper(rel):
    mapFunction = lambda x : getLevel(rel,x)[1]
    k = rel.total
    g = {}
    while k >= 1:
        l = mapFunction(k)
        try:
            g[l].append(k)
        except:
            g[l] = [k]

        k -= 1
    return g

class Relation:
    def __init__(self, conns, total):
        self.rel  = getMinimalCoverage(conns)
        self.total =total

    def getNebors(self,val):
        g = []
        for a,b in self.rel:
            if(val in (a,b)):
                if(val == a):
                    g.append(b)
                else:
                    g.append(a)
        return g
class Kami:
    def __init__(self, conns, colorMap):
        self.data = conns
        self.colorMap = colorMap
        self.traceback = []

    def merge(self):
        pass

    def getLevel(self,r_v):
        k = {}
        lvl = 0
        children = [r_v]
        goneThrough = []

        while len(children) != 0:
            temp = children 
            children = []
            for i in temp:
                if (i not in goneThrough):
                    k[i] = lvl
                    goneThrough.append(i)
                    children += self.data[i]
            lvl += 1
        return k, lvl-1

    def grouper(self,mapFunction = lambda x : self.getLevel(x)[1]):
        k = len(self.data)
        g = {}
        while k >= 1:
            l = mapFunction(k)
            try:
                g[l].append(k)
            except:
                g[l] = [k]

            k -= 1
        return g

    def colorSelector(self,val):
        g = {}
        for nebor in self.data[val]:
            try:
                g[self.colorMap[nebor]] +=  1
            except:
                g[self.colorMap[nebor]] = 1
        sorted_g = {k: v for k, v in sorted(g.items(), key=lambda item: item[1], reverse = True)}
        for key in sorted_g:
            yield key

    def optionSelector(self,minKeyGroup):
        groups = self.grouper()
        minKeyGroup = groups[min(list(groups.keys()))]
        g = {}
        for i in minKeyGroup:
            for v in self.data[i]:
                if(v in minKeyGroup):
                    try:
                        g[v] += 1
                    except:
                        g[v] = 1
        sorted_g = {k: v for k, v in sorted(g.items(), key=lambda item: item[1], reverse = True)}
        for key in sorted_g:
            yield key
connections = {
    1: [4,2],
    2: [1,3,4,5,10, 22,28],
    3: [2,5,6],
    4: [1,2,28],
    5: [2,3,6,10],
    6: [3,5,7,8,10],
    7: [6,8,12,9],
    8: [7,6],
    9: [7,11,12,13],
    10: [2,5,6,11,22],
    11: [9,10,22,13,21,24,25,27],
    12: [7,9,13],
    13: [9,11,12,14,21],
    14: [13,15,21],
    15: [14,16,21],
    16: [15,21,20,17],
    17: [16,18,19],
    18: [17,19],
    19: [17,18,20,11,16,26],
    20: [21,16,19],
    21: [13,14,15,16,20,11],
    22: [2,11,23,24],
    23: [22,24,27,28],
    24: [11,22,23,27],
    25: [11, 26,27,33,35],
    26: [19,25,35],
    27: [28,29,23,24,11,25,33,32,30],
    28: [2,4,23,27],
    29: [28,20,31],
    30: [27,29,31,32],
    32: [27,30,31,33,34],
    31: [29,30,32],
    33: [27,32,34,35,25],
    34: [32,33],
    35: [33,25,26]}
color_equivalency = [
                     [1, 3, 7, 10, 13, 15, 28, 29, 24, 32, 25, 17, 20],
                     [4, 5, 8, 22, 27, 9, 21, 19, 31, 34, 35],
                     [2, 6, 11, 12, 14, 16, 18, 23, 26, 30, 33]
                    ]
colorMap = {}
for i,row in enumerate(color_equivalency):
    for index in row:
        colorMap[index] = i
sagaLvl5 = {
    1: [2, 23],
 2: [1, 23, 3],
 3: [2, 5, 4],
 4: [5, 6, 3],
 5: [4, 3],
 6: [9, 7, 4, 8],
 7: [6],
 8: [9, 11, 6],
 9: [6, 8, 10],
 10: [11, 9, 24, 25],
 11: [10, 24, 13, 8, 12],
 12: [13, 11],
 13: [12, 11, 14],
 14: [33, 15, 16, 13],
 15: [31, 16, 30, 29, 14],
 16: [15, 17, 14],
 17: [16, 19, 18],
 18: [19, 21, 17],
 19: [18, 17],
 20: [21, 22],
 21: [20, 18, 22],
 22: [23, 20, 21],
 23: [22, 2, 1],
 24: [11, 10, 25],
 25: [26, 10, 24],
 26: [28, 25, 27],
 27: [51, 28, 26],
 28: [26, 52, 27],
 29: [15],
 30: [32, 31, 15],
 31: [15, 30, 32, 36],
 32: [30, 31],
 33: [14, 35, 34],
 34: [35, 39, 33],
 35: [34, 33],
 36: [37, 38, 31],
 37: [36, 38],
 38: [36, 37, 39],
 39: [41, 34, 40, 38],
 40: [41, 39],
 41: [40, 39],
 42: [43, 47, 44],
 43: [42, 44],
 44: [42, 43],
 45: [48, 52, 47, 46],
 46: [47, 48, 49, 45],
 47: [42, 46, 45],
 48: [46, 45, 52, 49],
 49: [51, 50, 46, 48],
 50: [49, 51],
 51: [49, 27, 50],
 52: [28, 48, 45]}

color_equivalency = [
    {1, 3, 6, 10, 12, 16, 18, 22, 26, 29, 30, 33, 36, 39, 42, 46, 51, 52},
 {5, 7, 8, 13, 15, 19, 21, 23, 24, 27, 32, 35, 37, 40, 44, 47, 48, 50},
 {2, 4, 9, 11, 14, 17, 20, 25, 28, 31, 34, 38, 41, 43, 45, 49}]

colorMap = {}
for i,row in enumerate(color_equivalency):
    for index in row:
        colorMap[index] = i
rel = Relation(sagaLvl5,52)
grouper(rel)
# for i in optionSelector(rel):
#     print(i)