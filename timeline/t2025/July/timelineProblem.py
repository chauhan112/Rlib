import json
import bisect
from collections import namedtuple
State = namedtuple("State", ["bg", "map"])
TestCase = namedtuple("TestCase", ["name", "before", "op", "results"])
from useful.basic import Main as ObjMaker
class IntervalMap:
    def __init__(self, val_begin):
        self.val_begin = val_begin
        self.m_map = []
    def __str__(self):
        map_str = ", ".join([f"({k}, '{v}')" for k, v in self.m_map])
        return f"IntervalMap(val_begin='{self.val_begin}', m_map={{{map_str}}})"
    def assign(self, key_start, key_end, value):
        if key_start == key_end:
            return
        l = bisect.bisect_right(self.m_map, (key_start, ""))
        r = bisect.bisect_right(self.m_map, (key_end, ""))
        ev = self.get_val_at(key_end)
        self.erase(l, r-l)
        self.put(key_start, value)
        self.put(key_end, ev)
        
    def erase(self, index, num):
        for _ in range(num):
            del self.m_map[index]
    def put(self, k, v):
        i = bisect.bisect_right(self.m_map, (k, v))
        if (i-1) >= 0: # has prev val
            pk, pv = self.m_map[i-1]
            if k != pk:
                if pv != v:
                    self.m_map.insert(i, (k, v))
            else:
                npv = self.get_val_at(k-1)
                if npv == v:
                    del self.m_map[i-1]
                else:
                    self.m_map[i-1] = (k, v)        
        else:
            if self.val_begin != v:
                self.m_map.insert(i, (k, v))

    def get_val_at(self, i):
        index = bisect.bisect_right(self.m_map, (i, "Z")) - 1
        if index < 0:
            return self.val_begin
        return self.m_map[index][1]

def compareStates(state1, state2):
    if (state1.bg != state2.bg):
        return False, "bg does not match"
    if len(state1.map) != len(state2.map):
        return False, "Size does not match"
    for i in range(len(state1.map)):
        if (state1.map[i] != state2.map[i]):
            return False, "value does not match"
    return True, ""

def runTests():
    testCases = [
        TestCase(
            name = "Splitting an Existing Interval",
            before=State(bg="A", map=[(10, 'B'), (20, 'A')]),
            op = (12, 15, 'C'),
            results=State(bg="A", map=[ (10, 'B'), (12, 'C'), (15, 'B'), (20, 'A') ]),
        ),
        TestCase(
            name = "Overwriting and Merging",
            before=State(bg="A", map=[(10, 'B'), (20, 'A')]),
            op = (10, 20, 'A'),
            results=State(bg="A", map=[]),
        ),
        TestCase(
            name = "Extending an Interval and Overwriting Another",
            before=State(bg="A", map=[(10, 'B'), (20, 'C')]),
            op =(15, 25, 'B'),
            results=State(bg="A", map=[(10, 'B'), (25, 'C')]),
        ),
        TestCase(
            name = "Assignment that interacts with m_valBegin",
            before=State(bg="A", map=[(10, 'B')]),
            op =(0, 5, 'C'),
            results=State(bg="A", map=[(0, 'C'), (5, 'A'), (10, 'B')]),
        ),
        TestCase(
            name = 'A "No-Op" Assignment',
            before=State(bg="A", map=[(10, 'B'), (20, 'A')]),
            op =(12, 18, 'B'),
            results=State(bg="A", map=[ (10, 'B'), (20, 'A')]),
        ),
        TestCase(
            name="Assignment on an Empty Map",
            before=State(bg="A", map=[]),
            op=(10, 20, 'B'),
            results=State(bg="A", map=[(10, 'B'), (20, 'A')]),
        ),
        TestCase(
            name="Overwriting Multiple Intervals",
            before=State(bg="A", map=[(10, 'B'), (20, 'C'), (30, 'D')]),
            op=(15, 35, 'E'),
            results=State(bg="A", map=[(10, 'B'), (15, 'E'), (35, 'D')]),
        ),
        TestCase(
            name="Assignment Merging with m_valBegin",
            before=State(bg="A", map=[(10, 'B'), (20, 'C')]),
            op=(10, 20, 'A'),
            results=State(bg="A", map=[(20, 'C')]),
        ),
        TestCase(
            name="Assignment Overwriting the Final Interval",
            before=State(bg="A", map=[(10, 'B')]),
            op=(15, 25, 'A'),
            results=State(bg="A", map=[(10, 'B'), (15, 'A'), (25, 'B')]),
        ),
        TestCase(
            name="Assignment with an Empty Range",
            before=State(bg="A", map=[(10, 'B'), (20, 'C')]),
            op=(15, 15, 'X'),
            results=State(bg="A", map=[(10, 'B'), (20, 'C')]),
        ),TestCase(
            name="Assignment Touching an Interval Start",
            before=State(bg="A", map=[(10, 'B'), (20, 'C')]),
            op=(5, 10, 'D'),
            results=State(bg="A", map=[(5, 'D'), (10, 'B'), (20, 'C')]),
        ),
        TestCase(
            name="Assignment Causing Forward Merge",
            before=State(bg="A", map=[(10, 'B'), (20, 'C')]),
            op=(15, 20, 'C'),
            results=State(bg="A", map=[(10, 'B'), (15, 'C')]),
        ),
        TestCase(
            name="Assignment Covering Entire Map",
            before=State(bg="A", map=[(10, 'B'), (20, 'C')]),
            op=(0, 30, 'D'),
            results=State(bg="A", map=[(0, 'D'), (30, 'C')]),
        ),
        TestCase(
            name="No-Op Assignment Matching m_valBegin",
            before=State(bg="A", map=[(10, 'B')]),
            op=(0, 5, 'A'),
            results=State(bg="A", map=[(10, 'B')]),
        ),
        TestCase(
            name="Merge With Both Neighbors",
            before=State(bg="A", map=[(10, 'B'), (20, 'A'), (30, 'B')]),
            op=(20, 30, 'B'),
            results=State(bg="A", map=[(10, 'B')]),
        )
    ]

    for ts in testCases:
        print(ts.name, end=": ")
        im = IntervalMap(ts.before.bg)
        im.m_map = ts.before.map.copy()
        im.assign(*ts.op)
        r, msg = compareStates(State(im.val_begin, im.m_map), ts.results)
        assert(r), msg
        print("PASS")
    s = ObjMaker.variablesAndFunction(locals())
    return s


def conversionTools():
    
    def getMapString(m_map):
        return "{" +", ".join([f"{{{k}, '{v}'}}" for k, v in m_map]) + "}"

    def get_state_string(state):
        return f"{{'{state.bg}', {getMapString(state.map)}}}"

    for ts in testCases:
        print(f"{{{json.dumps(ts.name)}, {get_state_string(ts.before)}, {{{ts.op[0]}, {ts.op[1]}, '{ts.op[2]}'}}, {get_state_string(ts.results)}}}", end=", \n")
    
    s = ObjMaker.variablesAndFunction(locals())
    return s