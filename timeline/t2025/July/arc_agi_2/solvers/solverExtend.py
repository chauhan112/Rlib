from ..twoD_tools import Vector, ExtendTools, BoundingRect
from collections import namedtuple
from ..objectedness import GridObject, Main as GridMain
from ..tools import ArrayTools, Field
from basic import Main as ObjMaker

DirRes = namedtuple("DirRes", ["val", "rect", "arr", "dir"])
class SolverExtenderTools:
    @staticmethod
    def get_value_if_exist(arr, obj: GridObject):
        a,b = obj.bounding_rect[0]
        for i,j in obj.obj:
            v = arr[i-a][j-b]
            obj_copy = SolverExtenderTools.makeGridCopy(obj)
            obj_copy.replace_value(v)
            if v != 0:
                return True, obj_copy
        return False, 0
    @staticmethod
    def displace_by_shape(initPos:Vector, shape:Vector,di:Vector):
        mask =  di + initPos + di * shape
        return BoundingRect(mask, shape + mask - 1)
    @staticmethod
    def makeGridCopy ( grid:GridObject ):
        gb = GridObject()
        gb.set_grid(grid.grid)
        gb.set_objects(grid.obj)
        return gb
    @staticmethod
    def getField(inp):
        def place(firstPoint, arr):
            assert isinstance(firstPoint, tuple), "firstPoint must be of type tuple"
            assert isinstance(arr, Field), "arr must be of type Field"
            sx,sy = arr.shape()
            sp, sq = res.shape()
            x,y = firstPoint
            for i in range(sx):
                nx = x+i
                if nx >= sp or nx < 0:
                    continue
                for j in range(sy):
                    ny = y+j
                    if ny >= sq or ny < 0:
                        continue
                    if res.arr[nx][ny] == 0:
                        res.arr[x+i][y+j] = arr.arr[i][j]
        res = Field(inp)
        res.place = place
        return res
class SolverExtender045e512c:
    def getDirValMap(self, inp, mainObj:GridObject):
        dirValMap = {}
        for di in self._directions:
            brect = SolverExtenderTools.displace_by_shape(self._iniVec, self._shape, di)
            arr = ArrayTools.crop(inp, brect.top_left, brect.bottom_right)
            f, v = SolverExtenderTools.get_value_if_exist(arr, mainObj)
            if f:
                dirValMap[di] = DirRes(v, brect, arr, di)
        return dirValMap

    def solve(self,inp):
        objs = GridMain.get_objs(inp, True)
        mainObj = max(objs, key=lambda x: x.area)
        self._directions = ExtendTools.get_dirs()
        br = ExtendTools.bounding_rect(mainObj.bounding_rect)
        self._iniVec = br.top_left
        self._shape = Vector(*mainObj.shape)
        dirValMap = self.getDirValMap(inp, mainObj)

        res = SolverExtenderTools.getField([])
        res.set_shape(ArrayTools.shape(inp))
        res.place(mainObj.bounding_rect[0], Field(mainObj.rect_obj))
        self._area = ExtendTools.bounding_rect(((0,0), res.shape()))
                
        for k in dirValMap:
            self.extend(dirValMap[k],res)

        return res

    def extend(self,dirRes: DirRes, field: Field):
        initPos = dirRes.rect.top_left
        ob = dirRes.val
        field.place(initPos, Field(ob.rect_obj))
        area = self._area
        rect = dirRes.rect
        while ExtendTools.intersects(area, rect) or ExtendTools.is_inside_rect(rect, area):
            rect = SolverExtenderTools.displace_by_shape(rect.top_left, self._shape, dirRes.dir)
            field.place(rect.top_left, Field(ob.rect_obj))
def Solver05269061():
    def get_coord(ind, shape):
        sx, sy = shape
        if ind < sx:
            return ind, 0
        yco = ind - sx
        if yco >= (sy-1):
            raise ValueError("Index out of range")
        return sx-1, yco + 1
    def iterator(shape):
        i = 0
        while True:
            try:
                yield get_coord(i, shape)
            except ValueError:
                break
            i += 1
    def get_encoding(arr):
        cm = {}
        shp = ArrayTools.shape(arr)
        for i, (x,y) in enumerate(iterator(shp)):
            v = arr[x][y]
            if v != 0 and v not in cm:
                cm[v] = x+y
        
        ncm = {}
        t = len(cm)
        for v in cm:
            k = cm[v]
            ncm[k%t] = v
        return ncm, t

    def fill_diagonal(arr, val, bottom_left_cord, shape):
        x,y = bottom_left_cord
        sx,sy = shape
        while x >= 0 and y < sy:
            arr[x][y] = val
            x -= 1
            y += 1
    def solve(inp):
        import copy
        cm, t = get_encoding(inp)
        inpCopy = copy.deepcopy(inp)
        shp = ArrayTools.shape(inp)
        for x,y in iterator(shp):
            v = x+y
            fill_diagonal(inpCopy, cm[v%t], (x,y), shp)
        return Field(inpCopy)
    s = ObjMaker.variablesAndFunction(locals())
    return s