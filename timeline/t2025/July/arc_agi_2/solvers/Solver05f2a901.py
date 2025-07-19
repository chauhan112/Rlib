from .solver05a7bcf2 import Solver05a7bcf2
from .solverExtend import SolverExtenderTools
from typing import Tuple
from ...arc_agi_2 import ObjMaker
from ..objectedness import Main as GridMain, GridObject
from ..tools import ColorMap, ToGoDirection, ExtendTools
from ..Fields import Field
from .moreTools import rotx

def Solver05f2a901():
    def get_red_blue(inp):
        objs = GridMain.get_objs(inp)
        assert len(objs) == 2
        redObj = list(filter(lambda x: x.value == ColorMap.RED.value, objs))[0]
        blueOb  = list(filter(lambda x: x.value == ColorMap.LIGHT_BLUE.value, objs))[0]
        return redObj, blueOb
    def inRange(x, rang: Tuple[int, int], inclusive=False):
        if inclusive:
            return rang[0] <= x <= rang[1]
        return rang[0] < x < rang[1]
    def get_direction_to_move(obj: GridObject,target:GridObject):
        ob_rect = ExtendTools.bounding_rect(obj.bounding_rect)
        t_rect = ExtendTools.bounding_rect(target.bounding_rect)
        oxRange = ob_rect.top_left.x, ob_rect.bottom_right.x
        oyRange = ob_rect.top_left.y, ob_rect.bottom_right.y
        isInXRange = inRange(t_rect.top_left.x, oxRange,True) or inRange(t_rect.bottom_right.x, oxRange, True)
        isInYRange = inRange(t_rect.top_left.y, oyRange, True) or inRange(t_rect.bottom_right.y, oyRange, True)
        if isInXRange:
            if t_rect.top_left.y < ob_rect.top_left.y:
                return ToGoDirection.left
            elif t_rect.top_left.y > ob_rect.top_left.y:
                return ToGoDirection.right
        elif isInYRange:
            if t_rect.top_left.x < ob_rect.top_left.x:
                return ToGoDirection.up
            elif t_rect.top_left.x > ob_rect.top_left.x:
                return ToGoDirection.down
    def solve_down_oriented(inp):
        res = Field(inp)
        redOb, blueOb = get_red_blue(inp)
        rc = SolverExtenderTools.makeGridCopy(redOb)
        rc.replace_value(ColorMap.BLACK.value)
        res.place(rc.bounding_rect[0], Field(rc.rect_obj))
        k = blueOb.bounding_rect[0][0] -redOb.bounding_rect[1][0] -1
        x,y = redOb.bounding_rect[0]
        res.place((x+k, y), Field(redOb.rect_obj))
        return res
    def solve(inp):
        redOb, blueOb = get_red_blue(inp)
        direction = get_direction_to_move(redOb, blueOb)
        rotMap = {ToGoDirection.right: 3, ToGoDirection.up: 2, ToGoDirection.left: 1, ToGoDirection.down: 0}
        rot = rotMap[direction]
        newArr = rotx(inp, rot)
        res = solve_down_oriented(newArr)
        return Field(rotx(res.arr.tolist(), (-rot % 4)))
    solver = Solver05a7bcf2()

    s = ObjMaker.variablesAndFunction(locals())
    return s
