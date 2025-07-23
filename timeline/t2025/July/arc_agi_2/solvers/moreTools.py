from ...arc_agi_2 import ObjMaker
from ..tools import Vector, ArrayTools
from ..objectedness import  GridObject

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
    def overlap_with_transparent(firstPoint, arr, inst):
        sx,sy = arr.shape()
        x,y = firstPoint
        for i in range(sx):
            for j in range(sy):
                tval = arr.arr[i][j]
                if tval == 0:
                    continue 
                inst.arr[x+i][y+j] = arr.arr[i][j]
    s = ObjMaker.variablesAndFunction(locals())
    return s
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
def rotx(arr, times=1):
    for _ in range(times):
        arr = ArrayTools.rotate(arr)
    return arr