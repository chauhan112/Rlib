from collections import namedtuple
from typing import Tuple
BoundingRect = namedtuple("BoundingRect", ["top_left", "bottom_right"])
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
    