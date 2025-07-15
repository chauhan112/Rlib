from basic import Main as ObjMaker
from ..twoD_tools import Vector
from enum import Enum
from typing import List
from ..tools import ArrayTools
import copy
import numpy as np
def LinesTools():
    def orientation(obj: GridObject):
        (x1, y1) = obj.bounding_rect[0]
        (x2, y2) = obj.bounding_rect[1]
        vec = Vector(x2 - x1, y2 - y1)
        if vec.x > vec.y: # vertical direction
            return "vertical"
        return "horizontal"
    def get_slope(p1:Vector, p2:Vector)->float:
        return (p2.y - p1.y)/(p2.x - p1.x)
    s = ObjMaker.variablesAndFunction(locals())
    return s
def Solver05a7bcf2():
    def rotx(arr, times=1):
        for _ in range(times):
            arr = ArrayTools.rotate(arr)
        return arr
    def get_colored_objs(objs: List[GridObject]):
        y = []
        b = []
        r = []
        for ob in objs:
            if ob.value == ColorMap.YELLOW.value:
                y.append(ob)
            elif ob.value == ColorMap.LIGHT_BLUE.value:
                b.append(ob)
            elif ob.value == ColorMap.RED.value:
                r.append(ob)
        return y, b, r
    def get_move_direction(obj: GridObject,target:GridObject):
        (x1, y1) = target.bounding_rect[0]
        (x2, y2) = target.bounding_rect[1]
        vec = Vector(x2 - x1, y2 - y1)
        if vec.x > vec.y: # vertical direction
            if obj.bounding_rect[0][0] < vec.x:
                return ToGoDirection.right
            else:
                return ToGoDirection.left
        else:
            if obj.bounding_rect[0][1] < vec.y:
                return ToGoDirection.down
            else:
                return ToGoDirection.up
    def get_objs_and_directions(inp):
        objs = GridMain.get_objs( inp, True)
        y,b, r = solver.handlers.get_colored_objs(objs)
        assert len(b) == 1
        assert len(r) == 1
        b = b[0]
        r = r[0]
        direction = solver.handlers.get_move_direction(y[0], b)
        return y, b, r, direction
    def solve(inp):
        _, _, _, direction = get_objs_and_directions(inp)
        rotMap = {ToGoDirection.right: 3, ToGoDirection.up: 2, ToGoDirection.left: 1, ToGoDirection.down: 0}
        rot = rotMap[direction]
        newArr = solver.handlers.rotx(inp, rot)
        res = solve_down_oriented(newArr)
        return Field(solver.handlers.rotx(res.arr.tolist(), (-rot % 4)))
    def solve_down_oriented(inp):
        ys, b, r, direction = get_objs_and_directions(inp)
        def notIsInside(point):
            shape = ArrayTools.shape(inp)
            return not ArrayTools.isInside(shape, point)
        def fillYellowTill(arr, ob):
            for i, r in enumerate(arr):
                for j, c in enumerate(r):
                    if (i,j) in ob.obj:
                        return
                    arr[i][j] = ColorMap.YELLOW.value
        def get_gridObj(pos, arr):
            go = GridObject()
            go.set_grid(copy.deepcopy(arr))
            go.set_objects(pos)
            return go
        res = Field(inp)
        for yob in ys:
            cells= get_cells_till(yob, Vector(*direction.value), notIsInside)
            go = get_gridObj(cells, inp)
            narr = go.rect_obj
            sobjs = GridMain.get_objs(narr, False)
            
            redObj = list(filter(lambda x: x.value == ColorMap.RED.value, sobjs))[0]
            blueOb  = list(filter(lambda x: x.value == ColorMap.LIGHT_BLUE.value, sobjs))[0]
            field = get_field(narr)
            field.arr = np.full(field.arr.shape, ColorMap.LIGHT_BLUE.value, dtype=int)
            fillYellowTill(field.arr, blueOb)

            x, y = redObj.shape

            redField = Field(redObj.rect_obj)
            redField.replace_value(ColorMap.BLACK.value, ColorMap.LIGHT_BLUE.value)
            field.place((-x,0), redField )
            yob.replace_value(ColorMap.GREEN.value)
            res.place(go.bounding_rect[0], field)
            res.place(yob.bounding_rect[0], Field(yob.rect_obj))
        return res
    s = ObjMaker.variablesAndFunction(locals())
    return s
class ToGoDirection(Enum):
    up = (-1,0)
    down = (1,0)
    left = (0,-1)
    right =(0,1)
def FieldPlacers():
    def place_only_at_zero(value):
        return value == 0
    def placing_codition(value):
        place_only_at_zero(value)
    def partial_outside_place(firstPoint, arr, inst):
        sx,sy = arr.shape()
        sp, sq = inst.shape()
        x,y = firstPoint
        for i in range(sx):
            nx = x+i
            if nx >= sp or nx < 0:
                continue
            for j in range(sy):
                ny = y+j
                if ny >= sq or ny < 0:
                    continue
                if s.handlers.placing_codition(inst.arr[nx][ny]):
                    inst.arr[x+i][y+j] = arr.arr[i][j]
    def full_inside_place(firstPoint, arr, inst):
        sx,sy = arr.shape()
        x,y = firstPoint
        sp, sq = inst.shape()
        for i in range(sx):
            p = x+i
            if p >= sp:
                break
            for j in range(sy):
                q = y+j
                if q >= sq:
                    break
                if s.handlers.placing_codition(inst.arr[p][q]):
                    inst.arr[p][q] = arr.arr[i][j]
    s = ObjMaker.variablesAndFunction(locals())
    return s
def get_field(arr):
    f = Field(arr)
    placers = FieldPlacers()
    f._placer = placers.handlers.full_inside_place
    placers.handlers.placing_codition = lambda x: True
    return f
def cells_in_between(obj: GridObject, tillObj: GridObject, direction:Vector):
    return get_cells_till(obj, direction, lambda x: x in tillObj.obj)
def get_cells_till(obj: GridObject, direction:Vector, breakCondition):
    res = set()
    dis = 1
    collided = False
    while True:
        for pos in obj.obj:
            newPos = Vector(*pos) + direction * dis
            if newPos in obj.obj:
                continue
            if breakCondition(newPos):
                collided = True
                break
            res.add(newPos)
        dis += 1
        if collided:
            break
        
    return res