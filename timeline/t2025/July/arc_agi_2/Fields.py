import numpy as np
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
        return self.shape() == other.shape() and (self.arr == other.arr).all()
    def replace_value(self,old_value, new_value ):
        self.arr[self.arr == old_value] = new_value