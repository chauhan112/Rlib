class Machine:
    def __init__(self, val, price):
        self.day, self.cost, self.resale, self.factor = val
        self._price = price - self.cost
    def tillCost(self, till):
        return (till - self.day) * self.factor + self._price
class Comp:
    AMore = 1
    ALess = 2
    Undecided = 3
class BranchAndBound:
    def __init__(self):
        self._breaker_map = {}
        self.pathId = 0
        self._all_paths = {}
        self._cost = {}
    def isGreater(self, a,b):
        p,r = a
        pp, rr = b

        if r > rr:
            if p >= pp:
                return Comp.AMore
            return Comp.Undecided
        elif r < rr:
            if p > pp:
                return Comp.Undecided
            return Comp.ALess

        if p >= pp:
            return Comp.AMore
        return Comp.ALess
    def _delete_path(self, pathId, curLvl):
        # delete the path and its corresponding checkpoints
        for lvl in self._breaker_map:
            if lvl >= curLvl:
                self._breaker_map[lvl].clear()
        if pathId in self._all_paths:
            self._all_paths[pathId]
        
    def isReplaceable(self, price, rate, lvl, pathId):
        # check the current path is redundant
        if lvl not in self._breaker_map:
            return False
        if len(self._breaker_map[lvl]) == 0:
            return False
        for p, r, l, path_id in self._breaker_map[lvl]:
            comp = self.isGreater((price, rate), (p, r))
            if comp == Comp.AMore:
                self._delete_path(path_id, lvl)
            elif comp == Comp.ALess:
                return True
        return False
    def add_point(self, lvl, price, rate, path_id):
        # adds a checkpoint
        # each checkpoint is jsut price and rate, with extra info used for deleting or updating the map
        if lvl not in self._breaker_map:
            self._breaker_map[lvl] = []
        self._breaker_map[lvl].append((price, rate, lvl, path_id))
    def add_path(self, path, path_id, price, sp):
        # add a new path
        if path_id in self._all_paths:
            raise 
        self._all_paths[path_id] = path
        if price < sp:
            price = sp
        self._cost[path_id] = price
class DataStr:
    def __init__(self, mx_Day, machines, initialMoney):
        self._max_day = mx_Day
        self.setMachines(machines)
        self._initial_money = initialMoney
    def setMachines(self, machines):
        self._machines = sorted(machines)
    def tillCalc(self, mId):
        if (mId + 1) >= len(self._machines):
            return self._max_day
        return self._machines[mId+1][0]
    def canItBeBought(self,mId, price, sp):
        d, c, r, p = self._machines[mId]
        if price >= c:
            return True
        return sp >= c
class Solver:
    def __init__(self):
        self.set_branch_and_bound_structure(BranchAndBound())
    def set_case(self, case):
        self._case = case
        self.set_input_data(DataStr(self._case.maxDays, self._case.machines, self._case.initialCost))
        self.set_branch_and_bound_structure(BranchAndBound())
    def set_input_data(self, ds):
        self._ds = ds
    def set_branch_and_bound_structure(self, bb):
        self._bb = bb
    def _update(self, price, path, mId, crnt_mchn=None):
        if crnt_mchn is None:
            sp = price
        else:
            sp = price - crnt_mchn.factor + crnt_mchn.resale
        if mId >= len(self._ds._machines):
            self._bb.add_path(path, self._bb.pathId, price, sp)
            return
        rate = 0
        if crnt_mchn is not None:
            rate = crnt_mchn.factor
        if self._bb.isReplaceable(price, rate, mId, self._bb.pathId):
            return
        self._bb.add_point(mId,price, rate, self._bb.pathId)
        if self._ds.canItBeBought(mId, price, sp):
            np = price
            if crnt_mchn is not None:
                np = crnt_mchn.tillCost(self._ds.tillCalc(mId))
            self._update(np, path, mId+1, crnt_mchn)

            self._bb.pathId += 1
            crnt_mchn = Machine(self._ds._machines[mId], price)
            np = crnt_mchn.tillCost(self._ds.tillCalc(mId))
            self._update(np, path + [mId], mId+1, crnt_mchn)

        else:
            np = price
            if crnt_mchn is not None:
                np = crnt_mchn.tillCost(self._ds.tillCalc(mId))
            self._update(np, path, mId+1, crnt_mchn)
    def solve(self):
        self._update(self._ds._initial_money, [], 0)
        return max(self._bb._cost.values())
class Output:
    def set_reader(self, reader):
        self._reader = reader
    def set_writer(self, writer):
        self._writer = writer
    def set_solver(self, solver):
        self._solver = solver
    def getResult(self):
        for i, case in enumerate(self._reader._cases):
            self._solver.set_case(case)
            self._writer.write(i+1, self._solver.solve())
class Case:
    def __init__(self):
        self.machines = []
    def set_header(self, header):
        a = header
        if type(header) == str:
            a = list(map(int,header.strip().split()))
        self.nrOfMachines, self.initialCost, self.maxDays = a

    def add_machine(self, line):
        a = line
        if type(line) == str:
            a = list(map(int, line.strip().split()))
        self.machines.append(a)
class Reader:
    def __init__(self):
        self._cases = []
    def set_filename(self, filename):
        self._file = filename
        self._parse_cases(self.getFileContent(filename))
    def _parse_cases(self, content):
        contentLines = content.strip().splitlines()
        i = 0
        while True:
            case = Case()
            case.set_header(contentLines[i])
            if case.maxDays == 0 and case.initialCost == 0 and case.nrOfMachines == 0:
                break
            i+=1 
            for j in range(case.nrOfMachines):
                case.add_machine(contentLines[i])
                i += 1
            self._cases.append(case)
    def getFileContent(self,filename):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
class PrintWriter:
    def write(self, caseNr, result):
        print(f"case {caseNr}: {result}")


# r = Reader()
# r.set_filename("snapshot_input.txt")
# out = Output()
# out.set_reader(r)
# out.set_writer(PrintWriter())
# out.set_solver(Solver())
# out.getResult()
