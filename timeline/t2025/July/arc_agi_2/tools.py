import numpy as np
from typing import Set, Tuple, List
class Labels:
    train ="train"
    test = "test"
    input="input"
    output="output"
from enum import Enum
class ColorMap(Enum):
    BLACK = 0
    RED = 2
    YELLOW = 4
    LIGHT_BLUE = 8
    GREEN = 3

class ArcQuestion:
    def __init__(self, question):
        self.question = question
    def shape(self,idx=0, inputOrOutput= Labels.input):
        return ArrayTools.shape(self.question[Labels.train][idx][inputOrOutput])
    def get(self,idx=0, inputOrOutput= Labels.input):
        return self.question[Labels.train][idx][inputOrOutput]
    def verify(self, solver):
        assert len(self.question[Labels.train]) >= 1
        for ob in self.question[Labels.train]:
            res = solver(ob[Labels.input])
            assert res.isEqual(Field(ob[Labels.output])), (ob[Labels.output], res.get())
    def getTestOutput(self, solver):
        return [{"output": solver(ob[Labels.input]).arr} for ob in self.question[Labels.test]]

class ArrayTools:
    def flipVertically(arr):
        return arr[::-1]
    def flipHorizontally(arr):
        res = np.array(arr)[:, ::-1]
        return res.tolist()
    def copy2Clipboard(arr):
        import pyperclip
        pyperclip.copy(str(arr))
    def crop(arr: List[List[int]], point1: Tuple[int, int], point2: Tuple[int, int]):
        x1,y1 = point1
        x2,y2 = point2
        return [row[y1:y2+1] for row in arr[x1:x2+1]]
    def bounding_rect(obj: Set[Tuple[int, int]]):
        min_r = min([x[0] for x in obj])
        min_c = min([x[1] for x in obj])
        max_r = max([x[0] for x in obj])
        max_c = max([x[1] for x in obj])
        return (min_r, min_c), (max_r, max_c)
    def getArea(arr: List[List[int]]):
        return len(arr) * len(arr[0])
    def shape(arr: List[List[int]]):
        return len(arr), len(arr[0])
    def flatten(arr: List[List[int]]):
        return [x for row in arr for x in row]
    def replace(arr: List[List[int]], prev_value: int, value: int):
        return [[value if x == prev_value else x for x in row] for row in arr]
    def rotate(arr: List[List[int]]):
        return np.rot90(arr).tolist()
    def isInside(arrShape: Tuple[int, int], point: Tuple[int, int]):
        sx,sy = arrShape
        x,y = point
        return 0 <= x < sx and 0 <= y < sy
    def transpose(arr: List[List[int]]):
        return np.transpose(arr).tolist()
class Field:
    def __init__(self, arr):
        self.arr = np.array(arr, dtype=int)
        self._placer = self._def_placer
    def shape(self):
        return self.arr.shape
    def _def_placer(self, firstPoint, arr, inst=None):
        sx,sy = arr.shape()
        x,y = firstPoint
        for i in range(sx):
            for j in range(sy):
                self.arr[x+i][y+j] = arr.arr[i][j]
    def place(self, firstPoint, arr,):
        assert isinstance(firstPoint, tuple), "firstPoint must be of type tuple"
        assert isinstance(arr, Field), "arr must be of type Field"
        from inspect import signature
        if len(signature(self._placer).parameters) == 3:
            self._placer(firstPoint, arr, self)
            return
        self._placer(firstPoint, arr )
    def copy(self):
        return Field(self.arr.tolist.copy())
    
    def set_shape(self, shape):
        self.arr = np.zeros(shape, dtype=int)
    def get(self):
        return self.arr.tolist()
    def isEqual(self, other):
        assert isinstance(other, Field), "other must be of type Field"
        self.shape() == other.shape()
        return (self.arr == other.arr).all()
    def replace_value(self,old_value, new_value ):
        self.arr[self.arr == old_value] = new_value