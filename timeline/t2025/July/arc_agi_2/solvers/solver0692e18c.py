from ...arc_agi_2 import ObjMaker
from ..tools import ArrayTools
from ..Fields import Field
def toolsAgregate():
    from .Solver0607ce86 import Solver0607ce86
    from .Solver05f2a901 import Solver05f2a901
    from .moreTools import FieldPlacers, get_cells_till, cells_in_between
    noiseRemover = Solver0607ce86()
    moveto = Solver05f2a901()
    rowMask = noiseRemover.handlers.rowMask
    s = ObjMaker.dicToNamespace({"handlers": {
        "rowMask": rowMask,
        "twoDMask": noiseRemover.handlers.twoDMask,
        "FieldPlacers": FieldPlacers,
        "get_cells_till": get_cells_till,
        "cells_in_between": cells_in_between,
        "get_max_count": noiseRemover.handlers.get_max_count,

        }, "process": {"noiseRemover": noiseRemover,
            "moveto": moveto}})
    return s
def Solver0692e18c():
    def multiplyTheShape(arr, rowMultiplier, colMultiplier):
        newArr = []
        for row in arr:
            newCol = []
            for v in row:
                for _ in range(colMultiplier):
                    newCol.append(v)
            for _ in range(rowMultiplier):
                newArr.append(newCol.copy())
        return newArr
    def solve(inp):
        vl = max(set(ArrayTools.flatten(inp)))
        masked = twoDMask(inp, lambda x: x[1] > 0)
        newObj = ArrayTools.fill2dArray(ArrayTools.invert2dArray(masked), vl)
        field = Field([])
        nbF = Field(newObj)
        x, y= ArrayTools.shape(inp)
        field.set_shape((3*x, 3*y))
        for r,c in ArrayTools.getMaskIndices(inp):
            field.place((3*r, 3*c), nbF)
        return field
    ta = toolsAgregate()
    twoDMask = ta.handlers.twoDMask
    s = ObjMaker.variablesAndFunction(locals())
    return s