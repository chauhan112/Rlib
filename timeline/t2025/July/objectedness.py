from collections import deque
from typing import List, Set, Tuple
from .tools import ArrayTools
import copy
import pprint

class GridObject:
    def set_grid(self, grid):
        self.grid = grid
    def set_objects(self, obj):
        self.obj = obj
        self.bounding_rect = ArrayTools.bounding_rect(obj)
        self.rect_obj = ArrayTools.crop(self.grid, self.bounding_rect[0], self.bounding_rect[1])
        self.shape = ArrayTools.shape(self.rect_obj)
        x,y = self.shape
        self.area =x*y
        p = ArrayTools.flatten(self.rect_obj)
        self.uid = ",".join(map(str, p))
        x,y = list(self.obj)[0]
        self.value = self.grid[x][y]
    def replace_value(self, new_value):
        grid = copy.deepcopy(self.grid)
        for x,y in self.obj:
            grid[x][y] = new_value
        self.rect_obj = ArrayTools.crop(grid, self.bounding_rect[0], self.bounding_rect[1])
        self.value = new_value
    def touches_boundry(self ):
        p1,p2 = self.bounding_rect
        s1,s2 = ArrayTools.shape(self.grid)
        return p1[0] == 0 or p1[1] == 0 or p2[0] == s1-1 or p2[1] == s2-1
    def translate(self, r: int, c: int) -> Set[Tuple[int, int]]:
        return {(x+r, y+c) for x,y in self.obj}
    def __str__(self) -> str:
        return "\n".join([
        f"shape: {self.shape}",
        f"area: {self.area}",
        f"value: {self.value}",
        f"{pprint.pformat(self.rect_obj)}"
        ])
class GridObjectGetter:
    def __init__(self):
        self.set_diagonal(False)
    def set_diagonal(self, diagonal: bool ):
        self.is_diagonal = diagonal
        self._directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if diagonal:
            self._directions.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])
    def set_grid(self, grid):
        self.grid = grid
        self.rows, self.cols = len(grid), len(grid[0])
    def is_valid(self, r: int, c: int) -> bool:
        grid = self.grid
        return 0 <= r < self.rows and 0 <= c < self.cols and self.vals_allower(grid[r][c]) and (r, c) not in self._visited
    def flood_fill(self, start_r: int, start_c: int) -> Set[Tuple[int, int]]:
        """Find all connected pixels using BFS."""
        component = set()
        queue = deque([(start_r, start_c)])
        while queue:
            r, c = queue.popleft()
            if (r, c) in self._visited:
                continue
            component.add((r, c))
            self._visited.add((r, c))
            
            for dr, dc in self._directions:
                new_r, new_c = r + dr, c + dc
                if self.is_valid(new_r, new_c) and self.is_same_condition((new_r, new_c), (start_r, start_c), component):
                    queue.append((new_r, new_c))
        
        return component
    def extract_objects(self) -> List[Set[Tuple[int, int]]]:
        self._visited = set()
        objects = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.vals_allower(self.grid[r][c]) and (r, c) not in self._visited:
                    component = self.flood_fill(r, c)
                    objects.append(component)
        
        res = []
        for obj in objects:
            gb = GridObject()
            gb.set_grid(self.grid)
            gb.set_objects(obj)
            res.append(gb)
        return res
    def vals_allower(self, val: int) -> bool:
        return val != 0
    def get_val (self, point: Tuple[int, int]) -> int:
        return self.grid[point[0]][point[1]]
    def is_same_condition(self, point: Tuple[int, int], other_point: Tuple[int, int], *args) -> bool:
        return self.get_val(point) == self.get_val(other_point)
class Main:
    @staticmethod
    def get_objs(arr, diagonal=False):
        go = GridObjectGetter()
        go.set_grid(arr)
        go.set_diagonal(diagonal)
        return go.extract_objects()