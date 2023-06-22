from ListDB import ListDB
from FileDatabase import File

class Tournament:
    def __init__(self, v=None):
        self.set_value(v)
    def set_value(self, v):
        self._v = v
        self._content = v
    def set_players(self, players: str):
        self.set_objects(Utils.makeObjs(players))
    def set_combinations(self, coms: str):
        self.set_objects([Tournament(l) for l in coms])
    @property
    def content(self):
        return self._content
    def _compare_repeat(self, a, b, count = 0):
        if a.v == b.v :
            return Utils.makeNew(a,b,a)
        elif a.v == "R" and b.v == "P":
            return Utils.makeNew(a,b,b)
        elif a.v == "R" and b.v == "S":
            return Utils.makeNew(a,b,a)
        elif a.v == "P" and b.v == "S":
            return Utils.makeNew(a,b,b)
        else:
            if count > 2:
                raise IOError("Err")
            return self._compare_repeat(b, a, count + 1)
    def set_objects(self, objs: list):
        self._objs = objs
        self._v = self._evalualt(objs).v
        self._content = "".join([r.content for r in self._objs])
    def _evalualt(self, objs):
        if len(objs) == 2:
            return self._compare_repeat(objs[0], objs[1])
        return self._compare_repeat(self._evalualt(objs[: int(len(objs)/ 2)]), self._evalualt(objs[int(len(objs)/ 2): ]))
    def set_string(self, string):
        objs = []
        for i in string:
            objs.append(Tournament(i))
        self.set_objects(objs)
    @property
    def v(self):
        if self._v:
            return self._v
        raise IOError("v not calculated")
    @property
    def vcontent(self):
        return "".join([r.v for r in self._objs])
    def get_next_round(self):
        lvl = ListDB.reshape(self._objs, (len(self._objs)/2, 2))
        trs = ""
        for eles in lvl:
            tr = Tournament()
            tr.set_objects(eles)
            trs += (tr.v)
        tr = Tournament()
        tr.set_combinations(trs)
        return tr
    def get_optimal_for_s(self):
        ob = Tournament()
        ob.set_objects(self._objs)
        res = self._objs
        for i in range(2):
            res = Utils.getNextLevel(res)
            ob = Tournament()
            ob.set_objects(res)
        return ob
class Utils:
    def makeNew(a, b, r):
        obj = Tournament()
        obj._content = a.content + b.content
        obj._v = r.v
        return obj
    def makeObj(letter, nr):
        objs = []
        for i in range(nr):
            objs.append(Tournament(letter))
        return objs
    def makeObjs(inp):
        aas = inp.split()
        aam = {}
        for a in aas:
            aam[a[-1]] = int(a[:-1])
        res = []
        for k, v in aam.items():
            res += Utils.makeObj(k, v)
        return res
    def mappv(objs):
        count = {"R":[], "P": [], "S":[]}
        for o in objs:
            count[o.v].append(o)
        return count
    def get_arrangement(pattern, values):
        res = []
        for p in pattern:
            res.append(values[p].pop())
        return res
    def getNextLevel(objs):
        values = Utils.mappv(objs)
        r, p, s = [len(x) for x in  values.values()]
        res = ""
        if p >= r:
            res += "RP"* r
            res += "P" * (p-r)
            res += "S" * s
        else:
            res += "RP"* p
            rl = r-p
            if s == 1:
                res = "R" * rl + res + "S"* s
            else:
                res = res + "R" * rl + "S"* s
        tot = Utils.get_arrangement(res, values)
        lvl = ListDB.reshape(tot, (len(tot)/2, 2))
        combins = []
        for el in lvl:
            ob = Tournament()
            ob.set_objects(el)
            combins.append(ob)
        return combins
class Reader:
    def read(self):
        pass
class Writer:
    def write(self, out: str):
        pass
class Level1:
    def solve(files):
        for fi in files:
            Level1.solve_a_file(fi)
    def read(file):
        content = File.getFileContent(file)
        cl = content.strip().splitlines()[1:]
        return cl
    def solve_a_file(file):
        cl = Level1.read(file)
        tr = Tournament()
        con = ""
        for pl in cl:
            tr.set_combinations(pl)
            con += tr.v +"\n"
        out = file.replace("in", "out")
        outPath = os.path.dirname(out)
        if not os.path.exists(outPath):
            os.makedirs(outPath)
        File.overWrite(out, con)
class Level2:
    def solve(files):
        for file in files:
            tr = Tournament()
            lc = Level1.read(file)
            res = ""
            for t in lc:
                tr.set_combinations(t)
                res += tr.get_next_round().get_next_round().content +"\n"
            out = file.replace("in", "out")
            outPath = os.path.dirname(out)
            if not os.path.exists(outPath):
                os.makedirs(outPath)
            File.overWrite(out, res)
class Level3:
    def solve(files):
        for file in files:
            cl = File.getFileContent(file).strip().splitlines()[1:]
            co = ""
            for pl in cl:
                tr.set_players(pl)
                co += Level3.remove_rock(Level3.remove_rock(tr))._content + "\n"
            out = file.replace("in", "out")
            outPath = os.path.dirname(out)
            if not os.path.exists(outPath):
                os.makedirs(outPath)
            File.overWrite(out, co)
    def remove_rock(tournament: Tournament):
        objs = tournament._objs
        values = Utils.mappv(objs)
        r, p, s = [len(x) for x in  values.values()]
        res = ""
        if p >= r:
            res += "RP"* r
            res += "P" * (p-r)
            res += "S" * s
        else:
            res += "RP"* p
            rl = r-p
            if s == 1:
                res = "R" * rl + res + "S"* s
            else:
                res = res + "R" * rl + "S"* s
        tot = Utils.get_arrangement(res, values)
        lvl = ListDB.reshape(tot, (len(tot)/2, 2))
        combins = []
        for el in lvl:
            ob = Tournament()
            ob.set_objects(el)
            combins.append(ob)
        tr = Tournament()
        tr.set_objects(combins)
        return tr
class Level4:
    def solve(files):
        for file in files:
            cl = File.getFileContent(file).strip().splitlines()[1:]
            co = ""
            for pl in cl:
                tr.set_players(pl)
                co += Level4._solve_tournament(tr) + "\n"
            out = file.replace("in", "out")
            outPath = os.path.dirname(out)
            if not os.path.exists(outPath):
                os.makedirs(outPath)
            File.overWrite(out, co)
    def _solve_tournament(ob):
        res = ob._objs
        while ob.v != "S":
            res = Utils.getNextLevel(res) 
            ob = Tournament()
            ob.set_objects(res)
        return ob.content