from FileDatabase import File
class Directions:
    Left = (0, -2)
    Right = (0, 2)
    TopLeft = (-1,-1)
    TopRight = (1,-1)
    BottomLeft = (-1, 1)
    BottomRight = (1,1)
class Vector:
    def subtract(vec1, vec2):
        x1, y2 = vec1
        x2,y1 = vec2
        return x2-x1, y2-y1
    def add(vec1, vec2):
        x1, y2 = vec1
        x2,y1 = vec2
        return x2+x1, y2+y1
class HexCoordType:
    OddR = 0
    EvenR = 1
    OddQ = 2
    EvenQ = 3
class HexDoubledCoordinate:
    def __init__(self):
        self.set_type(HexCoordType.OddR)
        self.set_displacements([Directions.Left, Directions.Right, Directions.TopLeft, Directions.TopRight, 
                                Directions.BottomLeft, Directions.BottomRight ])
    def set_type(self, typ: HexCoordType):
        self._type = typ
    def get_nebors(self, pos):
        x, y= pos
        neborts = [(x-1, y-1), (x+1, y+1), (x-1, y+1), (x+1, y-1), (x, y+2), (x, y-2)]
        return sorted([v for v in neborts if self.is_inside_the_space(v)])
    def set_dimension(self, dimX, dimY):
        self._dim = (dimX, dimY)
    def is_inside_the_space(self, pos):
        x,y = pos
        mx, my = self._dim
        if self._type == HexCoordType.OddR:
            my = my * 2
        if x >= 0 and y >= 0:
            if x < mx and y < my:
                return True
        return False
    def get_axial_coords(self, pos, direction = None):
        if direction is not None:
            return self._repeat_in_direction(direction, pos)
        res = []
        for dis in self._directions:
            res += self._repeat_in_direction(dis, pos)
        return res
        
    def _repeat_in_direction(self, displacement, pos):
        res = []
        while True:
            x,y = pos
            pos = Vector.add(pos, displacement)
            if (self.is_inside_the_space(pos)):
                res.append(pos)
            else:
                break
        return res
    def get_coordinate_for(self, row, col):
        if self._type == HexCoordType.OddR:
            return row, col * 2 + row % 2
        return row* 2 + col % 2, col
    def original_coord(self, pos):
        row, col = pos
        if self._type == HexCoordType.OddR:
            return row, self._polisher((col - row%2) / 2)
        return self._polisher((row - col % 2) / 2), col
    def _polisher(self, num):
        if (int(num) -num) == 0:
            return int(num)
        return num
    def set_displacements(self, directions):
        self._directions = directions
class HexCubeCoordinate:
    pass
class CellType:
    EmptyCell = "O"
    Trap = "X"
    Wasp = "W"
class BeeHive:
    def set_content(self, content):
        self._content = content
        self._arr_content = list(map(lambda row: row.strip().strip("-").split("-"), 
                                     self._content.strip().splitlines()))
        self._shape = len(self._arr_content), len(self._arr_content[0])
    def set_file(self, filepath):
        self.set_content(File.getFileContent(filepath))
    def get_cell_count(self):
        count = 0
        for letter in self._content:
            if letter == CellType.EmptyCell:
                count += 1
        return count
    def get_wasp_loc(self):
        for i, row in enumerate(self._arr_content):
            for j, val in enumerate(row):
                if val == CellType.Wasp:
                    return (i, j)
    def get_nr_cells_nebor_to_wasp(self):
        loc = self.get_wasp_loc()
        hcs = HexCoordinateSystem()
        hcs.determine_type_from_content(self._content)
        hcs.set_array(self._arr_content)
        c = 0
        nebors = hcs.get_nebors(loc)
        for x,y in nebors:
            if self._arr_content[x][y] == CellType.EmptyCell:
                c +=1 
        return c
class HexType:
    Minus = 0
    NotMinus = 1
class HexCoordinateSystem:
    def __init__(self):
        self.set_type(HexType.NotMinus)
    def set_type(self, hexType):
        self._hxType = hexType
    def set_array(self, arr):
        self._arr = arr
        self._row_nr = len(arr)
        self._col_nr = 0
        if len(arr) != 0:
            self._col_nr = len(arr[0])
    def set_dimension(self, dimX, dimY):
        self._row_nr = dimX
        self._col_nr = dimY
    def get_nebors(self, pos: tuple):
        x,y = pos
        allPos = [(x, y-1), (x, y+1), (x-1, y), (x-1, y+1), (x+1, y), (x+1, y+1)]
        if (self._hxType == HexType.Minus and x % 2 == 1) or (self._hxType == HexType.NotMinus and x % 2 == 0):
            allPos = [(x-1, y-1), (x-1, y), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y)]
        return sorted(filter(self._is_pos_in_grid, allPos))
    def _is_pos_in_grid(self, pos: tuple):
        x,y = pos
        if x >= self._row_nr or y >= self._col_nr:
            return False
        if x < 0 or y < 0: 
            return False
        return True
    def determine_type_from_content(self, content):
        ll = content.strip()[0]
        if ll == "-":
            self.set_type(HexType.Minus)
    def _repeat_in_direction(self, displacement, pos):
        res = []
        while True:
            x,y = pos
            pos = Vector.add(pos, displacement)
            if (self._is_pos_in_grid(pos)):
                res.append(pos)
            else:
                break
        return res
    def get_radial_pos(self, pos):
        nebors = self.get_nebors(pos)
        r_pos = []
        pos_disp = self._cordinate_translation( pos )
        col_size = self._col_nr
        self._col_nr = col_size*2
        for p in nebors:
            displa = Vector.subtract(pos_disp, self._cordinate_translation(p))
            r_pos += self._repeat_in_direction(displa, pos_disp)
        self._col_nr = col_size
        return list(map(self._cordinate_translation_inverse, r_pos))
    def _cordinate_translation(self, pos):
        x, y= pos
        if (self._hxType == HexType.Minus and x % 2 == 1) or (self._hxType == HexType.NotMinus and x % 2 == 0):
            return x, y*2
        return x, y *2 +1
    def _cordinate_translation_inverse(self, pos):
        x, y= pos
        if (self._hxType == HexType.Minus and x % 2 == 1) or (self._hxType == HexType.NotMinus and x % 2 == 0):
            return x, y/2
        return x, (y-1)/2
class Level2:
    def load_file(file):
        from WordDB import WordDB
        content = File.getFileContent(file)
        contentList = WordDB.regexSplit("\n\n+", content)[1:]
        bhs = []
        for c in contentList:
            bh = BeeHive()
            bh.set_content(c)
            bhs.append(bh)
        return bhs
    def solve(files):
        for file in files:
            bhs = Level2.load_file(file)
            content = ""
            for bh in bhs:
                content += str(bh.get_nr_cells_nebor_to_wasp()) + "\n"
            File.overWrite(file.replace("in", "out"), content)
class Level3:
    def solve(files):
        for f in files:
            bhs = Level2.load_file(f)
            out = f.replace("in", "out")
            cont = ""
            for bh in bhs:
                cont += Level3.solve_one(bh) +"\n"
            File.overWrite(out, cont)
    def solve_one(bh):
        hdc = HexDoubledCoordinate()
        hdc.set_dimension(*bh._shape)
        wasp = hdc.get_coordinate_for(*bh.get_wasp_loc())
        for dire in hdc._directions:
            axis = hdc.get_axial_coords( wasp, dire)
            backToCoord =  list(map(hdc.original_coord,axis ))
            found = True
            for x,y in backToCoord:
                if bh._arr_content[x][y] == CellType.Trap:
                    return "TRAPPED"
                    
            if found:
                return "FREE"

        return "TRAPPED"
