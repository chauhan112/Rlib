import numpy as np
from typing import Set, Tuple, List
from enum import Enum
from collections import namedtuple
from typing import Tuple
BoundingRect = namedtuple("BoundingRect", ["top_left", "bottom_right"])

class Labels:
    train ="train"
    test = "test"
    input="input"
    output="output"
class ColorMap(Enum):
    BLACK = 0
    RED = 2
    YELLOW = 4
    LIGHT_BLUE = 8
    GREEN = 3
class ToGoDirection(Enum):
    up = (-1,0)
    down = (1,0)
    left = (0,-1)
    right =(0,1)
class ArrayTools:
    @staticmethod
    def flipVertically(arr):
        return arr[::-1]
    @staticmethod
    def flipHorizontally(arr):
        res = np.array(arr)[:, ::-1]
        return res.tolist()
    @staticmethod
    def copy2Clipboard(arr):
        import pyperclip
        pyperclip.copy(str(arr))
    @staticmethod
    def crop(arr: List[List[int]], point1: Tuple[int, int], point2: Tuple[int, int]):
        x1,y1 = point1
        x2,y2 = point2
        return [row[y1:y2+1] for row in arr[x1:x2+1]]
    @staticmethod
    def bounding_rect(obj: Set[Tuple[int, int]]):
        min_r = min([x[0] for x in obj])
        min_c = min([x[1] for x in obj])
        max_r = max([x[0] for x in obj])
        max_c = max([x[1] for x in obj])
        return (min_r, min_c), (max_r, max_c)
    @staticmethod
    def getArea(arr: List[List[int]]):
        return len(arr) * len(arr[0])
    @staticmethod
    def shape(arr: List[List[int]]):
        return len(arr), len(arr[0])
    @staticmethod
    def flatten(arr: List[List[int]]):
        return [x for row in arr for x in row]
    @staticmethod
    def replace(arr: List[List[int]], prev_value: int, value: int):
        return [[value if x == prev_value else x for x in row] for row in arr]
    @staticmethod
    def rotate(arr: List[List[int]]):
        return np.rot90(arr).tolist()
    @staticmethod
    def isInside(arrShape: Tuple[int, int], point: Tuple[int, int]):
        sx,sy = arrShape
        x,y = point
        return 0 <= x < sx and 0 <= y < sy
    @staticmethod
    def transpose(arr: List[List[int]]):
        return np.transpose(arr).tolist()
class Vector(namedtuple("Vector", ["x", "y"])):
    def __radd__(self, other):
        return self + other
    def __add__(self, other):
        if isinstance(other, int):
            return Vector(self.x + other, self.y + other)
        return Vector(self.x + other.x, self.y + other.y)
    def __mul__(self, other):
        if isinstance(other, int):
            return Vector(self.x * other, self.y * other)
        return Vector(self.x * other.x, self.y * other.y)
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
    def __str__(self):
        return f"({self.x}, {self.y})"
    def __rmul__(self, other):
        return self * other
    def __sub__(self, other):
        if isinstance(other, int):
            return Vector(self.x - other, self.y - other)
        return Vector(self.x - other.x, self.y - other.y)
    def __rsub__(self, other):
        if isinstance(other, int):
            return Vector(other - self.x, other - self.y)
        return Vector(other.x - self.x, other.y - self.y)
class ExtendTools:
    @staticmethod
    def is_inside_rect(rect1: BoundingRect, rect2: BoundingRect):
        """Check if rect1 is inside rect2."""
        p1, p2 = rect1
        return ExtendTools.is_point_inside_rect(p1, rect2) and \
            ExtendTools.is_point_inside_rect(p2, rect2)
    @staticmethod
    def intersects(rect1: BoundingRect, rect2: BoundingRect):
        """Check if rect1 and rect2 intersect."""
        p1, p2 = rect1
        if ExtendTools.is_point_inside_rect(p1, rect2):
            return True
        if ExtendTools.is_point_inside_rect(p2, rect2):
            return True
        return False
    @staticmethod
    def is_point_inside_rect(point: Vector, rect: BoundingRect, inclusive=False):
        """Check if point is inside rect."""
        if inclusive:
            return point.x >= rect.top_left.x and \
                point.x <= rect.bottom_right.x and \
                point.y >= rect.top_left.y and \
                point.y <= rect.bottom_right.y
        return point.x >= rect.top_left.x and \
            point.x < rect.bottom_right.x and \
            point.y >= rect.top_left.y and \
            point.y < rect.bottom_right.y
    @staticmethod
    def bounding_rect(ps: Tuple[Tuple[int, int], Tuple[int, int]]):
        p1, p2 = ps
        return BoundingRect(Vector(*p1),Vector(*p2))
    @staticmethod
    def get_dirs(include_center=False):
        from itertools import product
        dirs = set(product([0,1,-1], [0,1,-1]))
        if not include_center:
            dirs.remove((0,0))
        return [Vector(*x) for x in dirs]