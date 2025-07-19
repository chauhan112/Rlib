from ..tools import ArrayTools, Labels, ColorMap
from typing import List
from ..objectedness import GridObjectGetter, GridObject
from ..Fields import Field
from ..reader import ArcQuestion

def sol_00576224(inp):
    finp = ArrayTools.flipHorizontally(inp)
    av = [Field(inp), Field(finp)]
    res = Field([])
    res.set_shape((6,6))
    for j in range(3):
        for i in range(3):
            res.place((j*2, i*2), av[j %2])
    return res

def sol_007bbfb7(inp):
    res = Field([])
    finp = Field(inp)
    res.set_shape((9,9))
    for j in range(3):
        for i in range(3):
            if inp[j][i] > 0:
                res.place((j*3, i*3), finp)
    return res

class Solver009d5c81:
    def set_question(self, question: ArcQuestion):
        self.question = question
        self.process()
    def process(self):
        from ..objectedness import Main as GridMain
        valMap = {}
        for ob in self.question.question[Labels.train]:
            inp = ob[Labels.input]
            out = ob[Labels.output]
            s, _ = sorted(GridMain.get_objs(inp, True), key=lambda x: x.area)
            b = GridMain.get_objs(out, True)[0]
            valMap[s.uid] = b.value
        self.valMap = valMap
    def solve(self, inp):
        from ..objectedness import Main as GridMain, GridObject
        s, b  = sorted(GridMain.get_objs(inp, True), key=lambda x: x.area)
        assert isinstance(b, GridObject), "b must be of type GridObject"
        b.replace_value(self.valMap[s.uid])
        res = Field([])

        res.set_shape(ArrayTools.shape(inp))
        res.place(b.bounding_rect[0],Field(b.rect_obj) )
        return res

def sol_00d62c1b(inp):
    from ..objectedness import GridObjectGetter
    grg = GridObjectGetter()
    grg.set_grid(inp)
    grg.vals_allower = lambda x: True
    objs = grg.extract_objects()
    mo =list(filter(lambda x: x.value == 0 and not x.touches_boundry(), objs))
    for m in mo:
        m.replace_value(ColorMap.YELLOW.value)
    res = Field(inp.copy())
    for m in mo:
        res.place(m.bounding_rect[0],Field(m.rect_obj) )
    return res

class Solver00dbd492:
    def get_objs(self, inp):
        grg = GridObjectGetter()
        grg.set_grid(inp)
        grg.vals_allower = lambda x: True
        objs = grg.extract_objects()
        mo: List[GridObject] =list(filter(lambda x: x.value == 0 and not x.touches_boundry(), objs))
        return mo
    def set_question(self, question: ArcQuestion):
        self.question = question
        self.process()
    def process(self):
        valMap = {}
        for ob in self.question.question[Labels.train]:
            inp = ob[Labels.input]
            out = ob[Labels.output]
            mo = self.get_objs(inp)
            for m in mo:
                x,y = list(m.obj)[0]
                ov = out[x][y]
                if m.uid in valMap:
                    assert valMap[m.uid] == ov
                else:
                    valMap[m.uid] = ov
        self.valMap = valMap
    def solve(self, inp):
        objs = self.get_objs(inp)
        res = Field(inp)
        for m in objs:
            m.replace_value(self.valMap[m.uid])
            res.place(m.bounding_rect[0],Field(m.rect_obj) )
        return res

class Solver017c7c7b:
    def check_period(self, arr: List[List[int]], s:int, s2:int):
        i = s
        j = s2
        while i < s2:
            if arr[i] != arr[j]:
                return False
            i += 1
            j += 1
            if j == len(arr):
                break
        return True
    def find_min_period(self, arr: List[List[int]]):
        arrToString = lambda row: "".join(map(str, row))
        arrString = [arrToString(v) for v in arr]
        i = 0
        j = 1
        while j < len(arrString):
            if arrString[i] == arrString[j] and self.check_period(arrString, i, j):
                return j - i
            else:
                j += 1
        return 0
    def getField(self, arr: List[List[int]]):
        def place(firstPoint, arr):
            assert isinstance(firstPoint, tuple), "firstPoint must be of type tuple"
            assert isinstance(arr, Field), "arr must be of type Field"
            sx,sy = arr.shape()
            x,y = firstPoint
            sp, sq = f.shape()
            for i in range(sx):
                p = x+i
                if p >= sp:
                    break
                for j in range(sy):
                    q = y+j
                    if q >= sq:
                        break
                    f.arr[p][q] = arr.arr[i][j]
        f = Field(arr)
        f.place = place

        return f

    def solve(self, inp):
        res = self.getField([])
        res.set_shape((9,3))
        period = self.find_min_period(inp)
        i = 0
        periodArr = ArrayTools.replace(inp, 1, 2)
        while i < 9:
            res.place((i, 0), Field(periodArr))
            i += period
        return res

def sol_025d127b(inp):
    from ..objectedness import Main as GridMain
    def isBase(ob, parentObj):
        (bcpx, bcpy) = parentObj.shape
        _, (ox, oy) = ob.bounding_rect
        if (bcpx - 1) == ox and (bcpy - 1) == oy:
            return True
        return False

    def getField(arr):
        def place(firstPoint, arr):
            sx,sy = arr.shape()
            x,y = firstPoint
            sp, sq = f.shape()
            for i in range(sx):
                p = x+i
                if p >= sp:
                    break
                for j in range(sy):
                    q = y+j
                    if q >= sq:
                        break
                    prev_val = f.arr[p][q]
                    if prev_val == 0:
                        f.arr[p][q] = arr.arr[i][j]
                    
        f = Field(arr)
        f.place = place
        return f
    def move_top(obj):
        obObj = GridMain.get_objs(obj.rect_obj,False )
        res = getField([])
        res.set_shape(obj.shape)
        res.bounding_rect = obj.bounding_rect
        for o in obObj:
            if isBase(o, obj):
                res.place(o.bounding_rect[0], Field(o.rect_obj))
            else:
                x, y = o.bounding_rect[0]
                res.place((x, y+ 1), Field(o.rect_obj))
        return res
    res = Field([])
    res.set_shape(ArrayTools.shape(inp))
    objs = GridMain.get_objs(inp, True)
    for ob in objs:
        mob = move_top(ob)
        res.place(mob.bounding_rect[0], mob)
    return res

def sol_03560426(inp):
    from ..objectedness import Main as GridMain
    objs = GridMain.get_objs(inp)
    res = Field([])
    res.set_shape(ArrayTools.shape(inp))
    sobjs = sorted(objs, key=lambda x: x.bounding_rect[0][1])

    x,y = 0,0
    for o in sobjs:
        # print(o)
        res.place((x,y), Field(o.rect_obj))
        p, q = o.shape
        y += q-1
        x += p-1
    return res