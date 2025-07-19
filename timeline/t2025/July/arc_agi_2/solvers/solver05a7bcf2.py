from ...arc_agi_2 import ObjMaker
from typing import List
from ..tools import ArrayTools, ColorMap, ToGoDirection,Vector
import copy
from ..objectedness import Main as GridMain, GridObject
import numpy as np
from ..Fields import Field
from .moreTools import get_cells_till, FieldPlacers, rotx

def Solver05a7bcf2():
    def get_field(arr):
        f = Field(arr)
        placers = FieldPlacers()
        f._placer = placers.handlers.full_inside_place
        placers.handlers.placing_codition = lambda x: True
        return f
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
        (x,y), _ = obj.bounding_rect
        if vec.x > vec.y: # vertical direction
            if y < y1:
                return ToGoDirection.right
            else:
                return ToGoDirection.left
        else:
            if x < x1:
                return ToGoDirection.down
            else:
                return ToGoDirection.up
    def get_objs_and_directions(inp):
        objs = GridMain.get_objs( inp, True)
        y,b, r = get_colored_objs(objs)
        assert len(b) == 1
        assert len(r) == 1
        b = b[0]
        r = r[0]
        direction = get_move_direction(y[0], b)
        return y, b, r, direction
    def solve(inp):
        _, _, _, direction = get_objs_and_directions(inp)
        rotMap = {ToGoDirection.right: 3, ToGoDirection.up: 2, ToGoDirection.left: 1, ToGoDirection.down: 0}
        rot = rotMap[direction]
        newArr = rotx(inp, rot)
        res = solve_down_oriented(newArr)
        return Field(rotx(res.arr.tolist(), (-rot % 4)))
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

