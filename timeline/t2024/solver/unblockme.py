direction = {
    'h': (1,0),
    'v': (0,1)
}
class Utils:
    def vectorAdd(a, b):
        return a[0]+b[0], a[1]+b[1]
    def scalarMult(k, vec):
        return k*vec[0], k* vec[1]
    def subtract(a, b):
        return Utils.vectorAdd(a, Utils.scalarMult(-1, b))
    def liesBetween(firstVec, lastVec, valVec):
        dis = Utils.subtract(firstVec, lastVec) 
        return Utils.equal(Utils.absValue(dis), Utils.vectorAdd(Utils.absValue(Utils.subtract(firstVec, valVec)), 
                                                Utils.absValue(Utils.subtract(lastVec, valVec))))
    def absValue(vec):
        return tuple(map(abs, vec))
    def equal(ve1, ve2):
        return (ve1[0] == ve2[0]) and (ve1[1] == ve2[1])
    def makeBlocker(idd, board, cell):
        blkr = Blockers(idd)
        blkr.set_board(board)
        blkr.set_blocking_cell(cell)
        return blkr
class Block:
    def __init__(self, content=None):
        self._body = None
        self.id = None
        self._direction = None
        self._size = None
        self._intersected_point = None
        self._decider(content)
    def _decider(self, content):
        if content is None:
            return
        if type(content) == str:
            self.set_string(content)
        elif type(content) == list:
            self.set_content_as_list(content)
    def _parse(self, content):
        self._content = content
        self.id = int(self._content[0])
        self._direction = self._content[1]
        self._size = int(self._content[-1])
    @property
    def body(self):
        if self._body is not None:
            return self._body
        a = self._content
        unit = direction[self._direction]
        res = [(int(a[2]), int(a[3]))]
        for i in range(self.length-1):
            b = Utils.vectorAdd(res[-1], direction[a[1]])
            res.append(b)
        self._body = res
        return self._body
    @property
    def orientation(self):
        return self._direction
    @property
    def length(self):
        return self._size
    def intersects(self, anotherBlock):
        self._intersected_point = set(self.body).intersection(set(anotherBlock.body))
        anotherBlock._intersected_point = self._intersected_point
        return len(self._intersected_point) != 0
    def moveBy(self, d):
        unitVec = direction[self._direction]
        tra = Utils.scalarMult(d, unitVec)
        new = []
        for el in self.body:
            new.append(Utils.vectorAdd(el, tra))
        return new
    def set_string(self, content):
        self.set_content_as_list(content.strip().split())
    def set_content_as_list(self, content):
        self._parse(content)
    def set_body(self, body):
        self._body = body
        self._size = len(self._body)
class Board:
    def __init__(self):
        self._intersected = None
    def set_dimension(self, dim):
        self._dim = dim
    def set_objects(self, objs: list[Block]):
        self._objects = objs
        self._obj_dic_based_on_id = {x.id:x for x in self._objects}
    def set_objects_as_list(self, objs: list[list[str]]):
        self.set_objects([Block(x) for x in objs])
    def isMovable(self, object_id):
        obj = self._obj_dic_based_on_id[object_id]
        return self._moveByUnit(obj.moveBy(-1), object_id) or self._moveByUnit(block.moveBy(1), object_id)
    def isMovableByX(self, object_id, val):
        obj = self._obj_dic_based_on_id[object_id]
        return self._moveByUnit(obj.moveBy(val), object_id)
    def move(self,obj_id, byX):
        obj = self._obj_dic_based_on_id[obj_id]
        obj.set_body(obj.moveBy(byX))
    def _moveByUnit(self, body: list[tuple], object_id: int):
        a = Block()
        a.set_body(body)
        return not (self.isOutside(a) or self.intersects(a,self._not_ids(object_id)))
    def intersects(self, obj: Block, objsId: list[int]):
        for id_ in objsId:
            v = self._obj_dic_based_on_id[id_]
            if obj.intersects(v):
                self._intersected = v
                return True
        return False
    def _not_ids(self, obj_id):
        res = []
        for i in self._obj_dic_based_on_id:
            if i != obj_id:
                res.append(i)
        return res
    def isOutside(self, obj: Block):
        return self._boundryCheck(obj.body[0]) or self._boundryCheck(obj.body[-1])
    def _boundryCheck(self, point):
        dim = self._dim
        if point[0] <=0 or point[1] <= 0:
            return True
        if point[0] > dim[0] or point[1] > dim[1]:
            return True
        return False
    def set_string_input_format(self, inp):
        ll = inp.split()
        self.set_dimension(list(map(int, ll[:2])))
        nr = int(ll[2])
        objs = [ll[i*5+3: (i+1)*5 + 3] for i in range(nr)]
        self.set_objects_as_list(objs)
class TargetBlock:
    def __init__(self, idd):
        self._block_id = idd
    def set_board(self, board: Board):
        self._board = board
        self._destination_calculate()
    def set_destination(self, cell_pos):
        self._destination = cell_pos
    def _destination_calculate(self):
        b: Block = self._board._obj_dic_based_on_id[self._block_id]
        if b.orientation == "h":
            self.set_destination((self._board._dim[0], b.body[-1][-1]))
    def calc_move_to_reach_destination(self):
        b: Block = self._board._obj_dic_based_on_id[self._block_id]
        return self._destination[0] - b.body[-1][0]
    def isSolved(self):
        return self._board.isMovableByX(self._block_id, self.calc_move_to_reach_destination())
    def get_intersected_block_and_point(self):
        self.isSolved()
        return self._board._intersected.id, self._board._intersected._intersected_point.pop()
class Blockers:
    def __init__(self, idd):
        self._idd = idd
    def set_board(self, board: Board):
        self._board = board
        self._empty_board = Board()
        self._empty_board.set_dimension(self._board._dim)
    def set_blocking_cell(self, cell_coord):
        self._freeing_cell = cell_coord
    def free_up(self, val):
        b: Block = self._board._obj_dic_based_on_id[self._idd]
        b.set_body(b.moveBy(val))
    def possible_moves(self):
        b: Block = self._board._obj_dic_based_on_id[self._idd]
        ra, rb = Utils.subtract(self._freeing_cell, b.body[0]), Utils.subtract(b.body[-1], self._freeing_cell)
        if b.orientation == "v":
            return self._filterMoves([ra[1]+1, rb[1]-1], b)
        return self._filterMoves([ra[0]+1, rb[0]-1], b)
    def _filterMoves(self, moves, block: Block):
        self._empty_board.set_objects([block])
        return list(filter(lambda x: self._empty_board.isMovableByX(block.id, x), moves))
    def isMovableByX(self, x):
        return self._board.isMovableByX(self._idd, x)
    def doesMoveFreeUpTheBlockingCell(self, y):
        b: Block = self._board._obj_dic_based_on_id[self._idd]
        shift = lambda x:  Utils.vectorAdd(b.body[x], Utils.scalarMult(y, direction[b.orientation]))
        a, b = shift(0), shift(-1)
        # print(direction[b.orientation])
        return not Utils.liesBetween(a, b, self._freeing_cell)
    def get_intersected_block_and_point(self):
        return self._board._intersected.id, self._board._intersected._intersected_point.pop()
def solution(inp):
    board = Board()
    board.set_string_input_format(inp)

    tb = TargetBlock(0)
    tb.set_board(board)
    el_id, point = tb.get_intersected_block_and_point()

    stack = [(el_id, point)]
    while len(stack) != 0:
        idd, pt = stack.pop()
        bl: Blockers = Utils.makeBlocker(idd,board, pt)
        pm = bl.possible_moves()
        toAdd = []
        freed = False
        for m in pm:
            if not bl.isMovableByX(m):
                toAdd.append(bl.get_intersected_block_and_point())
            else:
                freed = True
                bl.free_up(m)
                print(bl._idd, m)
        if not freed:
            stack += toAdd
    return tb.isSolved()
