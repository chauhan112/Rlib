from .solver0692e18c import toolsAgregate
from ..twoD_tools import Vector
from ..tools import ArrayTools, Field
from ...arc_agi_2 import ObjMaker, Labels
from ..objectedness import Main as GridMain

import copy

def Solver_06df4c85():
    def grouper(arr, keyFunc= lambda x:x):
        res = {}
        for x in arr:
            k = keyFunc(x)
            if k in res:
                res[k].append(x)
            else:
                res[k] = [x]
        return res
    def get_empty_field(inp):
        field = Field([])
        field.set_shape(ArrayTools.shape(inp))
        return field
    def placeObjs(field, objs):
        for o in objs:
            field.place(o.bounding_rect[0], Field(o.rect_obj))
    def fillSpacesBetween(field, objA, objB, value):
        res = ta.process.moveto.handlers.get_direction_to_move(objA, objB)
        if res:
            cellsToFill = ta.handlers.cells_in_between(objA, objB, Vector(*res.value))
            for x, y in cellsToFill:
                field.arr[x][y] = value
    def separateObjs(objs, binFunc):
        a = []
        b= []
        for o in objs:
            if binFunc(o):
                a.append(o)
            else:
                b.append(o)
        return a, b
    def placer(firstPoint, arr, inst=None):
        sx,sy = arr.shape()
        x,y = firstPoint
        for i in range(sx):
            for j in range(sy):
                tval = arr.arr[i][j]
                if tval == 0:
                    continue 
                inst.arr[x+i][y+j] = arr.arr[i][j]
    def solve(inp):
        objs = GridMain.get_objs(inp, False)
        mx= max([x.area for x in objs])
        grid, smallObjs = separateObjs(objs, lambda x: x.area == mx)
        assert len(grid) == 1
        grid = grid[0]
        groups = grouper(smallObjs, lambda x:x.value)
        field = get_empty_field(inp)
        for k in groups:
            objs = groups[k]
            for i in range(len(objs)):
                for j in range(i+1, len(objs)):
                    objA = objs[i]
                    objB = objs[j]
                    placeObjs(field, [objA, objB])
                    fillSpacesBetween(field, objA, objB, k)
        field._placer = placer
        field.place(grid.bounding_rect[0], Field(grid.rect_obj))
        return field
    ta = toolsAgregate()
    s = ObjMaker.variablesAndFunction(locals())
    return s
def solve_070dd51e(inp):
    solver = Solver_06df4c85()
    objs = GridMain.get_objs(inp, False)
    ta = solver.process.ta
    groups =solver.handlers.grouper(objs, lambda x:x.value)
    field = solver.handlers.get_empty_field(inp)
    field._placer = solver.handlers.placer
    quesObjs= []
    for k in groups:
        assert len(groups[k]) == 2
        objA, objB = groups[k]
        x,y =ta.process.moveto.handlers.get_direction_to_move(objA, objB).value
        if x == 0: # move horizontally
            solver.handlers.placeObjs(field, [objA, objB])
            solver.handlers.fillSpacesBetween(field, objA, objB, k)
        else:
            quesObjs.append([k,objA, objB])
    for k,oa, ob in quesObjs:
        solver.handlers.placeObjs(field, [oa, ob])
        solver.handlers.fillSpacesBetween(field, oa, ob, k)
    return field
def solver08ed6ac7():
    colorMap = {}
    def set_question(ques):
        outA = ques.get(0,Labels.output)
        objs = GridMain.get_objs(outA)
        sob = sorted(objs, key=lambda x: x.area)
        s.process.colorMap = {i: sob[i].value for i in range(len(sob))}
    def solve(inp):
        field = Field([])
        field.set_shape(ArrayTools.shape(inp))
        objs = GridMain.get_objs(inp)
        sob = sorted(objs, key=lambda x: x.area)
        for i in range(len(sob)):
            ob:GridObject = sob[i]
            ob.replace_value(s.process.colorMap[i])
            field.place(ob.bounding_rect[0], Field(ob.rect_obj))
        return field
    s = ObjMaker.variablesAndFunction(locals())
    return s
    
def Solver09629e4f():
    def get_subsections_count(inp):
        res = []
        for i in range(0,len(inp),4):
            for j in range(0,len(inp[0]),4):
                res.append([(i,j), get_count((i,j), inp)])
        return res
                    
    def get_count(pos, inp):
        a,b = pos
        c = 0
        for i in range(3):
            for j in range(3):
                if inp[a+i][b+j] > 0:
                    c += 1
        return c

    def fill_section(inp, pos, val):
        i,j = pos
        for a in range(3):
            for b in range(3):
                inp[i+a][j+b] = val

    def solve(inp):
        sc =get_subsections_count(inp)
        pos, c = min(sc, key=lambda x: x[1])
        a,b = pos
        inpCopy = copy.deepcopy(inp)
        for i in range(3):
            for j in range(3):
                v = inp[a+i][b+j]
                fill_section(inpCopy, (i*4,j*4), v)
        return Field(inpCopy)
    s = ObjMaker.variablesAndFunction(locals())
    return s
ConnectObjects = Solver_06df4c85