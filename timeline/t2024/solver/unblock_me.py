from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from basic import Main as ObjMaker
from timeline.t2024.Array import Array
from useful.jupyterDB import jupyterDB
import numpy as np
import cv2

def Block():
    idd, direction, size, x,y = [None] * 5
    cache = {}
    def set_content(content):
        s.process.content = " ".join(content)
        s.process.idd, s.process.direction, s.process.x, s.process.y, s.process.size = Array(content).map(parse).array
        s.handlers.get_body_coords()
    def parse(x):
        if x in ["h", "v"]:
            return x
        return int(x)
    def prefunc():
        s.handlers.unoccupy()
        s.process.prev_x, s.process.prev_y = s.process.x, s.process.y
    def postFunc():
        s.handlers.get_body_coords()
        s.process.content = s.handlers._get_content()
    def movedTo(tx, ty):
        if not canBeMovedTo(tx,ty):
            return
        s.handlers.prefunc()
        if s.process.direction == "h":
            s.process.x = tx
        else:
            s.process.y = ty
        s.handlers.postFunc()
    def canBeMovedTo(x,y):
        if s.process.direction == "h":
            coords = [(x + i, y) for i in range(s.process.size)]
        else:
            coords = [(x, y + i) for i in range(s.process.size)]
        for c in coords:
            xx,yy = c
            if s.process.parent.handlers.isOutSide(xx,yy):
                return False
            cc = s.process.parent.handlers.get_space(xx,yy)
            if not s.handlers.isFree(cc):
                return False
        return True
    def _get_content():
        return f"{s.process.idd} {s.process.direction} {s.process.x} {s.process.y} {s.process.size}"
    def movedBy(d):
        s.handlers.movedTo(*s.handlers.get_coord_to_move_by_x(d))
    def get_coord_to_move_by_x(d):
        if s.process.direction == "h":
            return (s.process.x +d , s.process.y)
        else:
            return (s.process.x , s.process.y+d)
            
    def isFree(nm):
        if nm.isFree:
            if not hasattr(nm, "idd"):
                return True
            if nm.idd in [s.process.idd, None]:
                return True
        else:
            if nm.idd == s.process.idd:
                return True
        return False
    def unoccupy():
        coords = s.handlers.get_body_coords()
        for x in coords:
            x.isFree = True
            x.idd = None
    def occupyWithCurrent(nm):
        nm.isFree = False
        nm.idd = s.process.idd
    def get_body_coords():
        x, y= s.process.x, s.process.y
        if (x,y) in s.process.cache:
            list(map(occupyWithCurrent, s.process.cache[(x,y)]))
            return s.process.cache[(x,y)]
        if s.process.direction == "h":
            res = [s.handlers.occupy_space(x + i, y) for i in range(s.process.size)]
        else:
            res = [s.handlers.occupy_space(x, y + i) for i in range(s.process.size)]
        s.process.cache[(x,y)] = res
        return s.process.cache[(x,y)]
    def occupy_space(x,y):
        nm = s.process.parent.handlers.get_space(x, y)
        nm.isFree = False
        nm.idd = s.process.idd
        return nm
    s = ObjMaker.variablesAndFunction(locals())
    return s
def Board():
    x,y = None, None
    blocks =  []
    gridState = {}
    def set_content(content):
        inp = content.strip().split()
        s.process.x, s.process.y, _ = list(map(int, inp[:3]))
        s.process.gridState.clear()
        s.process.blocks = Array(sorted(Array(inp[3:]).reshape(5).array)).map(lambda x: s.handlers.makeBlock(x)).array
        s.process.mainBlock = s.process.blocks[0]
        
    def makeBlock(content):
        b = Block()
        b.process.parent = s
        b.handlers.set_content(content)
        return b
    def isSolved():
        p = max(s.process.mainBlock.handlers.get_body_coords(), key = lambda x: x.coords[0]).coords[0]
        remainingToMove = s.process.x - p

        for i in range(remainingToMove):
            space = s.handlers.get_space(p + i+ 1, s.process.mainBlock.process.y)
            if not space.isFree:
                return False
        return True
            
    def isOutSide(x,y):
        return x < 1 or x > s.process.x or y < 1 or y > s.process.y
        
    def get_space(x,y):
        if s.handlers.isOutSide(x,y):
            raise IOError("lies outside")
        if (x,y) in s.process.gridState:
            return s.process.gridState[(x,y)]
        nm = ObjMaker.namespace()
        nm.isFree = True
        nm.coords = (x, y)
        nm.idd = None
        s.process.gridState[(x,y)] = nm
        return nm
    
    s = ObjMaker.variablesAndFunction(locals())
    return s
def GenericSolver():
    allStates = set()
    orderedStates =[]
    path = []
    def reset():
        s.process.allStates = set()
        s.process.orderedStates = []
        s.process.path = []
    def solve():
        while True:
            if s.handlers.isSolved():
                break
            step = s.handlers.getNextStep()
            if step is None:
                s.handlers.goBack()
                continue
            
            nextState = s.handlers.getNextStateForStep(step)
            if nextState in s.process.allStates:
                s.handlers.skipAllBranch(step)
            else:
                s.handlers.goForward(step)
                s.process.orderedStates.append(nextState)
                s.process.allStates.add(nextState)
    def getNextStateForStep(step):
        pass
    def goForward(step):
        s.process.path.append(step)
    def goBack():
        pass
    def isSolved():
        return True
    def skipAllBranch(step):
        pass
    def getNextStep():
        pass
    s = ObjMaker.variablesAndFunction(locals())
    return s
def UnBlockMeSolver():
    board = Board()
    genericSolver = GenericSolver()
    def set_puzzle(inp):
        board = s.process.board
        board.handlers.set_content(inp)
        gs = s.process.genericSolver
        gs.handlers.reset()
        s.process.idsToBlock = {b.process.idd: b for b in board.process.blocks}
        gs.process.pathPossibilities = {tuple(gs.process.path): s.handlers.getAllMovesExcept()}
        
        
        gs.handlers.getNextStateForStep = s.handlers.getNextStateForStep
        gs.handlers.getNextStep = s.handlers.getNextStep
        gs.handlers.goBack = s.handlers.goBack
        gs.handlers.isSolved = board.handlers.isSolved
        gs.handlers.goForward = s.handlers.goForward
        gs.process.allStates.add(gs.handlers.getNextStateForStep((None,0)))
    def getAllMovePossibilities(b):
        res = set()
        goBy = 1
        while True:
            if b.handlers.canBeMovedTo(*b.handlers.get_coord_to_move_by_x(goBy)):
                res.add(goBy)
            else:
                break
            goBy += 1
        goBy = -1
        while True:
            if b.handlers.canBeMovedTo(*b.handlers.get_coord_to_move_by_x(goBy)):
                res.add(goBy)
            else:
                break
            goBy -= 1
        return res
    def getAllMovesExcept(b =None):
        bo = s.process.board
        res = []
        for bl in bo.process.blocks:
            idd = bl.process.idd
            if b is not None and b.process.idd == idd:
                continue
            allPos = s.handlers.getAllMovePossibilities(bl)
            for x in allPos:
                res.append((idd, x))
        return res
    def getNextStep():
        gs = s.process.genericSolver
        xx = gs.process.pathPossibilities[tuple(gs.process.path)]
        if len(xx):
            return xx.pop()
        return None
    def goBack():
        gs = s.process.genericSolver
        idd, moveBy = gs.process.path.pop()
        b = s.process.idsToBlock[idd]
        if b.handlers.canBeMovedTo(*b.handlers.get_coord_to_move_by_x(-moveBy)):
            prev_x, prev_y = b.process.x, b.process.y
            b.handlers.movedBy(-moveBy)
            assert b.process.x == prev_x - moveBy or b.process.y == prev_y - moveBy
        else:
            raise IOError("something went wrong. cant go back")
            
        
    def goForward(step):
        gs = s.process.genericSolver
        gs.process.path.append(step)
        idd, moveBy = step
        b = s.process.idsToBlock[idd]
        if b.handlers.canBeMovedTo(*b.handlers.get_coord_to_move_by_x(moveBy)):
            b.handlers.movedBy(moveBy)
        else:
            raise IOError("something went wrong. cant go forward")
        gs.process.pathPossibilities[tuple(gs.process.path)] = s.handlers.getAllMovesExcept(b)
    def solve():
        s.process.genericSolver.handlers.solve()
        return s.process.genericSolver.process.path
    
    def getNextStateForStep(step):
        idd, y = step
        bo = s.process.board
        if idd is None:
            return f"{bo.process.x} {bo.process.y} {len(bo.process.blocks)} " + \
                " ".join(Array(bo.process.blocks).map(lambda x: x.handlers._get_content()).array)
        b = s.process.idsToBlock[idd]
        if b.handlers.canBeMovedTo(*b.handlers.get_coord_to_move_by_x(y)):
            b.handlers.movedBy(y)
            res = f"{bo.process.x} {bo.process.y} {len(bo.process.blocks)} " + \
                    " ".join(Array(bo.process.blocks).map(lambda x: x.handlers._get_content()).array)
            b.handlers.movedBy(-y)

        return res
    s = ObjMaker.variablesAndFunction(locals())
    return s
class UnblockMeVisualizer:
    def __init__(self, board_size=(6,6),cell_size=100 ):
        self.offset = 4
        self.board = None
        self.board_margin = 4
        self.set_params(board_size, cell_size)
    def set_params(self, board_size=(6,6), cell_size=100):
        self.board_size = board_size
        x,y = board_size
        self.cell_size = cell_size
        self.board_width = x * cell_size + self.board_margin
        self.board_height = y * cell_size + self.board_margin
    def create_board(self):
        board = np.ones((self.board_height, self.board_width, 3), dtype=np.uint8) * 255
        self.board = board
        x, y = self.board_size
        cell_size = self.cell_size
        width = x * cell_size
        height =y * cell_size
        for i in range(y+1):
            p1 = (0, i * self.cell_size)
            p2 = (width, i * self.cell_size)
            cv2.line(board, p1 ,p2 , (200, 200, 200), 1)
        for i in range(x+1):
            p1 = (i * self.cell_size, 0)
            p2 = (i * self.cell_size, height)
            cv2.line(board, p1,p2 , (200, 200, 200), 1)
        return board
    def add_block(self, board, block, color=(0, 0, 255)):
        """
        Add a block to the board
        
        :param board: Board image
        :param block: Tuple (x, y, width, height, index) representing block position and size and index
        :param color: BGR color of the block
        :return: Updated board image
        """
        x, y, width, height, index = block
        p1 = (x * self.cell_size, y * self.cell_size)
        p2 = ((x + width) * self.cell_size, (y + height) * self.cell_size)
        pm = ((p1[0] + p2[0]) //2 , (p1[1] + p2[1]) //2)
        cv2.rectangle(board, p1, p2, color, -1) 
        cv2.rectangle(board, p1, p2, (0, 0, 0), 2)  # Outline
        cv2.putText(board,str(index), pm, cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
        return board
    def visualize_board(self, blocks, output_path=None):
        board = self.board
        if self.board is None:
            board = self.create_board()
        colors = [
            (0, 0, 255),      # Red (main block)
            (0, 255, 0),      # Green
            (255, 0, 0),      # Blue
            (0, 255, 255),    # Yellow
            (255, 0, 255)     # Magenta
        ]
        oc = colors[-2]
        for i, block in enumerate(blocks):
            color = colors[0] if i == 0 else oc
            board = self.add_block(board, block, color)
        ll  = np.ones((self.board_height + 2*self.offset, self.board_width + 2*self.offset, 3), dtype=np.uint8) * 255
        ll[self.offset:-self.offset, self.offset: -self.offset] = board
        if output_path is not None:
            cv2.imwrite(output_path, ll)
        return board
    def reset(self):
        self.create_board()
def MakeAnimation():
    grid = None
    cellSize = 100
    output_path='unblock_me_board.png'
    board = Board()
    visualizer = UnblockMeVisualizer()
    def translatorBA(x, y, gx, gy, s):
        # catcoder to unblockvisualizer
        return x-1, gy-s-y+1
    def tranCoorBA(pos, size, orien, index):
        grid = s.process.grid 
        if orien == "h":
            return (*s.handlers.translatorBA(*pos, *grid, 1), size, 1, index)
        x, y = s.handlers.translatorBA(*pos, *grid, size)
        return (x,y, 1, size,index)
    def tranCoorAB(x,y,width, height, grid, name= ""):
        isH = width > height
        if isH:
            x, y= translatorAB(x,y,*grid, 1)
            return ("h", x , y, width)
        x, y= translatorAB(x,y,*grid, height)
        return ("v", x,y, height)
    def translatorAB(x, y, gx, gy, s):
        return x+1, gy-s-y+1
    def update_params():
        board = s.process.board
        s.process.grid = (board.process.x ,board.process.y )
        visualizer = s.process.visualizer
        visualizer.set_params(s.process.grid, s.process.cellSize)
    def makeCat(grid, blocks): # claude blocks to catcoder blocks (needed to load the game in html)
        res = " ".join(list(map(str, grid))) + f" {len(blocks)} "
        tIndex, (x, y, width, height, index) = list(filter(lambda x:x[1][-1] == "T" ,enumerate(blocks)))[0]
        o, nx,ny,s = tranCoorAB(x, y, width, height, grid)
        res += f"0 {o} {nx} {ny} {s} "
        i = 1
        for p, (x, y, width, height, index) in enumerate(blocks):
            if tIndex ==p:
                continue
            o, nx,ny,s = tranCoorAB(x, y, width, height, grid)
            res += f"{i} {o} {nx} {ny} {s} "
            i += 1
        return res.strip()
    def makeImage():
        board = s.process.board
        s.handlers.update_params()
        blks = list(map(lambda bl: s.handlers.tranCoorBA((bl.process.x, bl.process.y), bl.process.size, 
            bl.process.direction, bl.process.idd), board.process.blocks))
        return s.process.visualizer.visualize_board(blks, s.process.output_path)
    def inpToImage(inp):
        s.process.board.handlers.set_content(inp)
        return s.handlers.makeImage()
    def makeAnimations(inps, output_filename= "test.gif", duration=500):
        imgs = []
        s.process.output_path = None
        for inp in inps:
            imgs.append(Image.fromarray(cv2.cvtColor(s.handlers.inpToImage(inp), cv2.COLOR_BGR2RGB)))
        print("images are created. now saving")
        imgs[0].save(
            output_filename, 
            save_all=True, 
            append_images=imgs[1:], 
            optimize=False, 
            duration=duration, 
            loop=True
        )
        print("saving done")
        s.process.output_path = 'unblock_me_board.png'
    def makeVideo(inps, output_path= "unblock_me_animation2.mp4",fps=24):
        s.process.output_path = None
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        s.process.board.handlers.set_content(inps[0])
        s.handlers.update_params()
        w = s.process.visualizer.board_width 
        h = s.process.visualizer.board_height
        out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))
        s.process.output_path = None
        for inp in inps:
            x = s.handlers.inpToImage(inp)
            # print(x.shape)
            out.write(x)
        out.release()
        s.process.output_path = 'unblock_me_board.png'
    def convertToTopLeftOpenCV(arr, tpos): # for converting github code to visualizer from claude
        narr = []
        for index, size, o, (y,x) in arr:
            if o == "H":
                narr.append((x,y,size, 1, index))
            else:
                narr.append((x,y,1, size, index))
        y, x = tpos
        narr.append((x,y, 2, 1, "T"))
        return narr
    s = ObjMaker.variablesAndFunction(locals())
    return s
def SolverImprovement():
    ubs = UnBlockMeSolver()
    def getNextStateForStep(step):
        def oneEle(idd):
            pp = " ".join(list(map(str, sorted(ubs.handlers.getAllMovePossibilities(ubs.process.board.process.blocks[idd])))))
            return f"{idd}({pp})"
        idd, y = step
        res = []
        b = None
        if idd is not None:
            b = ubs.process.idsToBlock[idd]
        for gb in ubs.process.board.process.blocks:
            if idd != gb.process.idd:
                if b is not None:
                    b.handlers.movedBy(y)
                res.append(oneEle(gb.process.idd))
                if b is not None:
                    b.handlers.movedBy(-y)
        bb = ",".join(res)
        return bb
    def getAllIntersectingBlocks(b):
        if b.process.direction == "h":
            coords = list(zip([b.process.x]*ubs.process.board.process.y , range(1, ubs.process.board.process.y+1)))
        else:
            coords = list(zip(range(1, ubs.process.board.process.x+1), [b.process.y]* ubs.process.board.process.x))
        nms = Array(coords).map(lambda x: ubs.process.board.handlers.get_space(x[0],x[1])).filter(lambda x: hasattr(x, "idd")
                ).filter(lambda x: x.idd != b.process.idd).filter(lambda x: x.idd is not None).map(lambda x: x.idd).array
        return set(nms)
    def getPriority(b):
        largeNumber = ubs.process.board.process.x*ubs.process.board.process.y
        def _getIdsPriority(b, priority, vals):
            ids = getAllIntersectingBlocks(b)
            found = False
            for idd in ids:
                if idd not in vals:
                    vals[idd] = priority + 1
                    _getIdsPriority(ubs.process.idsToBlock[idd], priority + 1, vals)
                    found = True
        vals = {b.process.idd: largeNumber+1}
        _getIdsPriority(b, 0, vals)
        for bb in ubs.process.board.process.blocks:
            if bb.process.idd not in vals:
                vals[bb.process.idd] = largeNumber
        return vals
    def getAllMovesExcept(b=None):
        res = prevMovesExcept(b)
        if b is not None:
            pp = getPriority(b)
            res =sorted(res, key = lambda x: pp[x[0]], reverse=True)
        return res
    def filterOutSomeSteps(b=None):
        res = getAllMovesExcept(b)
        newRes = []
        for idd, s in res:
            currentSt = getNextStateForStep((idd, 0))
            stt = getNextStateForStep((idd, s))
            if currentSt == stt:
                continue
            newRes.append((idd, s))
        return newRes
    def getPriority2(b):
        door = ubs.process.board.process.mainBlock.process.y, ubs.process.board.process.x
        def distanceCalc(p1,p2):
            x1,y1 = p1
            x2,y2 = p2
            return abs(x1-x2) + abs(y1-y2)
        def calcDis(bb):
            coords = bb.handlers.get_body_coords()
            return min([distanceCalc(c.coords, door) for c in coords])
                
        vals = {b.process.idd: calcDis(b)}
        for bb in ubs.process.board.process.blocks:
            vals[bb.process.idd] = calcDis(bb)
        return vals
    def getAllMovesExcept2(b=None): # did not make an improvement either
        bo = ubs.process.board
        res = {}
        for bl in bo.process.blocks:
            idd = bl.process.idd
            if b is not None and b.process.idd == idd:
                continue
            allPos = ubs.handlers.getAllMovePossibilities(bl)
            res[idd] = list(allPos)
        newRes = []
        i = 0
        added = True
        while added:
            added = False
            for k in res:
                val = res[k]
                if i < len(val):
                    newRes.append((k, val[i]))
                    added = True
        return newRes
    def solve():
        ubs.handlers.set_puzzle(inp)
        steps = ubs.handlers.solve()
        print(len(ubs.process.genericSolver.process.orderedStates))
        jupyterDB.clip().copy(" ".join(Array(steps).map(lambda x: " ".join(list(map(str, x)))).array))
    def solveAll():
        inps = ["6 6 10 0 h 3 4 2 1 h 5 2 2 2 v 1 5 2 3 h 3 5 3 4 v 4 2 2 5 h 5 6 2 6 v 2 4 3 7 v 6 3 3 8 h 1 3 2 9 h 1 1 2",  
               "6 5 3 0 h 2 3 3 1 h 2 5 5 2 v 6 2 2",
               "6 6 12 0 h 3 4 2 1 h 2 3 2 2 h 1 1 3 3 h 1 2 3 4 v 1 3 2 5 v 1 5 2 6 v 3 5 2 7 h 4 6 3 8 v 4 1 2 9 h 4 3 2 10 v 5 4 2 11 v 6 4 2",
               "6 6 8 0 h 1 4 2 1 h 1 3 2 2 v 2 1 2 3 v 3 4 2 4 v 3 2 2 5 h 3 1 2 6 v 4 3 3 7 v 5 3 3",
               "12 12 8 0 h 1 7 2 1 v 6 7 5 2 h 3 8 3 3 v 3 4 4 4 v 7 2 5 5 v 9 5 4 6 v 9 9 3 7 v 9 3 2"]
        for inp in inps: 
            print(f"solving: \n{inp}")
            ubs.handlers.set_puzzle(inp)
            ubs.handlers.solve()
            print("steps:", len(ubs.process.genericSolver.process.orderedStates))
    prevMovesExcept = ubs.handlers.getAllMovesExcept
    # prevHandler = ubs.handlers.getNextStateForStep
    ubs.handlers.getAllMovesExcept = filterOutSomeSteps
    s = ObjMaker.variablesAndFunction(locals())
    
    return s