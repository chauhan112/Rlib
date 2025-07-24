from basic import Main as ObjMaker

def KamiColorObj():
    value = 0
    nebors = set()
    color = ""
    nr = -1
    paths = []
    def get_state_string():
        return s.process.color
    def ids():
        return ",".join(map(lambda x: str(x.process.nr), s.process.paths))
    s = ObjMaker.variablesAndFunction(locals())
    return s

def Question():
    relations = None
    def set_relations_and_color(rels, colrMap):
        s.process.relations = rels
        s.process.colorMap = colrMap
        s.process.colorMapReverse = s.handlers.revKV(colrMap)
        s.process.relations_dense = s.handlers.fillAll(rels)
        kos = []
        nl = s.process.relations_dense
        for k in nl:
            ko = KamiColorObj()
            ko.process.nr = k
            ko.process.color = cmRev[k]
            ko.process.nebors= set(nl[k])
            kos.append(ko)
        s.process.keyColorObject = kos
        s.process.kcoMap = {l.process.nr: l for l in kos}
    def fillAll(nm):
        import copy
        nl = copy.deepcopy(nm)
        for k in nl:
            for v in nl[k]:
                if k not in nl[v]:
                    nl[v].append(k)
        return {k: sorted(nl[k]) for k in nl}
    def revKV(cm):
        cmRev = {}
        for k in cm:
            for v in cm[k]:
                cmRev[v] = k
        return cmRev
    s = ObjMaker.variablesAndFunction(locals())
    return s
def DepCalc():
    question = Question()
    def fdc(sn):
        kov = s.process.question.process.kcoMap
        n = kov[sn]
        mp = {sn:0}
        qu = n.process.nebors
        ly = 1
        while True:
            nq = set()
            for nn in qu:
                if nn not in mp:
                    mp[nn] = ly
                    nq = nq.union(kov[nn].process.nebors)
            ly += 1
            qu = nq.difference(set(mp))
            if len(qu) == 0:
                break
        return max(mp.values())
    def calculate():
        from useful.ListDB import ListDB
        kov = s.process.question.process.kcoMap
        r = {}
        for k in kov:
            r[k] = fdc(k)
        return ListDB.sortDicBasedOnValue(r)
    s = ObjMaker.variablesAndFunction(locals())
    return s
def KamiDijkstraTesting():
    question = Question()
    def fkmo(a,b):
        return fkm(a.process.nr, b.process.nr)
    def fkm(a, b):
        return tuple(sorted([a, b]))
    def fdc(a, b):
        if a.process.color == b.process.color:
            return 1
        return 2
    def fninr(a, b, res):
        k = fkmo(a,b)
        return k in res
    def fid(a,b):
        return a.process.nr != b.process.nr
    def distance_calculator(nma):
        res = {}
        for a in nma:
            for b in nma[a]:
                kab = fkm(a, b)
                if kab not in res:
                    res[kab] = 1
                for c in nma[b]:
                    ao = kvo[a]
                    co = kvo[c]
                    if fid(ao, co):
                        if not fninr(ao, co, res):
                            res[fkmo(ao, co)] = fdc(ao,co)
        return res
    def fakg(a, dres):
        if a not in dres:
            dres[a] = {}
        return dres[a]
    def md(a,b,d, res):
        ac = fakg(a, res)
        bc = fakg(b, res)
        ac[b] = d
        bc[a] = d
    def vertices_maker(res):
        dres = {}
        for b,e in res:
            t = res[(b,e)]
            md(b,e,t, dres)
        return dres
    def get_dijkstra(start, end):
        from ancient.AIAlgoDB import Dijkstra
        nm = s.process.question.process.relations
        res = s.handlers.distance_calculator(s.process.question.process.relations_dense)
        dres = s.handlers.vertices_maker(res)
        dj = Dijkstra(list(nm.keys()), dres)
        p, v = dj.find_route(start, end)
        return p, v, dj.generate_path(p, start, end)

    s = ObjMaker.variablesAndFunction(locals())
    return s
nm = {1: [2],
 2: [3, 4, 5, 7],
 3: [30],
 4: [11],
 5: [9],
 6: [8, 9, 10],
 7: [8],
 8: [29],
 9: [12],
 10: [12, 29],
 11: [12, 13],
 12: [19, 21],
 13: [14],
 14: [15, 16, 17, 24],
 15: [],
 16: [18],
 17: [19],
 18: [20, 22],
 19: [20],
 20: [21],
 21: [22],
 22: [23, 31, 33],
 23: [24, 25],
 24: [],
 25: [26],
 26: [27, 28, 35, 36],
 27: [],
 28: [30],
 29: [30, 31, 34],
 30: [],
 31: [32],
 32: [33, 34],
 33: [35],
 34: [36],
 35: [],
 36: []}
cm = {'red': [2, 8, 9, 10, 14, 18, 19, 21, 26, 31, 33, 34],
 'black': [5, 6, 7, 11, 16, 17, 20, 23, 30, 32, 35, 36],
 'white': [1, 3, 4, 12, 13, 15, 22, 24, 25, 27, 28, 29]}
