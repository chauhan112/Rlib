from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from basic import Main as ObjMaker
from FileDatabase import File
from timeline.t2024.Array import Array
from Path import Path

def LawnPath():
    path = ""
    rect = None
    pathsCoord = []
    def solve(ctx):
        pass
    def set_path(path):
        s.process.path = path
    def make_pathCoord():
        pc = []
        minX, maxX, minY, maxY = 0,0,0,0
        x,y = 0,0
        pc.append((x,y))
        for l in s.process.path:
            if l == "W":
                y -= 1
            elif l == "A":
                x -= 1
            elif l == "S":
                y += 1
            elif l == "D":
                x += 1
            minX = min([x, minX])
            minY = min([y, minY])
            maxX = max([x, maxX])
            maxY = max([y, maxY])
            pc.append((x,y))
        s.process.rect = (minX, minY), (maxX, maxY)
        def shift(pos):
            x,y = pos
            return x-minX, y-minY
        s.process.pathsCoord = Array(pc).map(shift).array
    def fit_rectangle():
        if s.process.rect is not None:
            return s.process.rect
        s.handlers.make_pathCoord()
        return s.process.rect
    def length_breadth():
        (x1,y1), (x2,y2) = s.handlers.fit_rectangle()
        xx = x2-x1 + 1, y2-y1+1
        return xx
    s = ObjMaker.variablesAndFunction(locals())
    return s
def LawnFields():
    directions = ["W", "D", "S", "A"]
    def set_file(file):
        s.process.file = file
        s.process.content = File.getFileContent(file)
        s.process.paths = s.process.content.strip().splitlines()[1:]
    def solve(ctx, *params):
        pass
    s = ObjMaker.variablesAndFunction(locals())
    return s
def Levels():
    files = None
    def makeLawnPath(path):
        def solve(ctx):
            (x1,y1), (x2,y2) = lp.handlers.fit_rectangle()
            xx = x2-x1 + 1, y2-y1+1
            return " ".join(list(map(str, xx)))
        lp = LawnPath()
        lp.handlers.set_path(path)
        lp.handlers.solve = solve
        return lp
    def init_level2():
        def makeLawnField():
            lf = LawnFields()
            def set_file(file):
                lf.process.file = file
                lf.process.content = File.getFileContent(file)
                lf.process.paths = Array(lf.process.content.strip().splitlines()[1:]).map(s.handlers.makeLawnPath).array
            lf.handlers.set_file = set_file
            return lf
        def write():
            for f in s.process.files:
                outFile = f + ".out"
                lff = s.process.content[f]
                res = []
                for pa in lff.process.paths:
                    res.append(pa.handlers.solve(pa))
                out = "\n".join(res)
                File.overWrite(outFile, out)
        s.handlers.write = write
        s.handlers.makeLawnField = makeLawnField
    def makeLawnField():
        return LawnFields()
    def set_files(files):
        def lf(f):
            lff = s.handlers.makeLawnField()
            lff.handlers.set_file(f)
            return lff
        s.process.files = files
        s.process.content = {file: lf(file) for file in files}
    def set_folder(folder):
        s.process.folder_loc = folder
        s.handlers.set_files(Path.filesWithExtension("in", folder))
    def solve(path):
        dirO = ["W", "D", "S", "A"]
        res ={k:0 for k in dirO}
        for l in path:
            res[l] += 1
        return (" ".join(Array(dirO).map(lambda x: res[x]).map(str).array))
    def write():
        for f in s.process.files:
            outFile = f + ".out"
            lff = s.process.content[f]
            res = []
            for pa in lff.process.paths:
                res.append(s.handlers.solve(pa))
            out = "\n".join(res)
            File.overWrite(outFile, out)
    def init_level1():
        pass
    s = ObjMaker.variablesAndFunction(locals())
    return s
def LawnField3():
    lp = LawnPath()
    def set_info(info):
        # info = info.strip()
        s.process.info = info
        s.process.dimension = list(map(int, info[0].split()))
        s.process.field = info[1:-1]
        s.process.lp.handlers.set_path(info[-1])
        s.process.treeLoc = s.handlers.findTreeLoc()
    def isPathValid():
        lp = s.process.lp
        x, y= lp.handlers.length_breadth()
        a = x* y
        xx,yy = s.process.dimension
        if xx != x or yy != y:
            return False
        if len(lp.process.pathsCoord) <= (a-2): # cell is missing
            return False
        if len(lp.process.pathsCoord) != len(set(lp.process.pathsCoord)): # overlap
            return False
        if s.process.treeLoc in lp.process.pathsCoord:
            return False
        return True
    def findTreeLoc():
        x, y= s.process.dimension
        for i in range(y):
            for j in range(x):
                if s.process.field[i][j] == "X":
                    return j,i
        raise IOError("no tree found")
    s = ObjMaker.variablesAndFunction(locals())
    return s
def Level3():
    lvls = Levels()
    def parse(content):
        col = content.strip().splitlines()[1:]
        r = []
        i = 0
        while i < len(col):
            il = col[i]
            x, y= list(map(int, il.split()))
            i += 1
            p = [il]
            for j in range(y):
                p.append(col[i])
                i += 1
            p.append(col[i])
            i += 1
            r.append(p)
        return r
    def set_files(files):
        s.process.files = files
        s.process.lf = {f: Array(s.handlers.parse(File.getFileContent(f))).map(makeLawnField).array for f in files}
    def makeLawnField(info):
        lf = LawnField3()
        lf.handlers.set_info(info)
        return lf
    def write():
        for f in s.process.files:
            outFile = f + ".out"
            lff = s.process.lf[f]
            res = []
            for lf in lff:
                if lf.handlers.isPathValid():
                    res.append("VALID")
                else:
                    res.append("INVALID")
            out = "\n".join(res)
            File.overWrite(outFile, out)
    lvls.handlers.set_files = set_files
    s = ObjMaker.variablesAndFunction(locals())
    return s
def FieldVisualizer():
    import cv2
    from timeline.t2024.solver.unblock_me import UnblockMeVisualizer
    ubv = UnblockMeVisualizer()
    def drawLine(c1, c2):
        x1, y1 = c1
        x2, y2 = c2
        p1 = int((x1 + .5) * ubv.cell_size), int((y1 +.5)* ubv.cell_size)
        p2 = int((x2 + .5) * ubv.cell_size), int((y2 +.5)* ubv.cell_size)
        cv2.line(ubv.board, p1 ,p2 , (255, 0, 255), 2)
    def drawTreeLoc(p1):
        x1, y1 = p1
        x,y = int((x1 + .5) * ubv.cell_size)-10, int((y1 +.5)* ubv.cell_size)-10
        cv2.rectangle(ubv.board, (x,y) ,(x+20, y+20) , (0, 255, 0), -1)
    def display(lf):
        ubv.set_params(lf.process.dimension, 60)
        ubv.reset()
        ubv.visualize_board([], output_path="lol.png");
        drawTreeLoc(lf.process.treeLoc)
        for i in range(1, len(lf.process.lp.process.pathsCoord)):
            p1 = lf.process.lp.process.pathsCoord[i-1]
            p2 = lf.process.lp.process.pathsCoord[i]
            drawLine(p1,p2)
        ubv.visualize_board([], output_path="lol.png");
        File.openFile("lol.png")
    s = ObjMaker.variablesAndFunction(locals())
    return s
def LawnField4():
    lf3 = LawnField3()
    def set_file(file):
        s.process.file = file
        s.process.content = File.getFileContent(file)
        s.process.lns = s.handlers.parse(s.process.content)
    def parse(content):
        col = content.strip().splitlines()[1:]
        r = []
        i = 0
        while i < len(col):
            il = col[i]
            x, y= list(map(int, il.split()))
            i += 1
            p = [il]
            for j in range(y):
                p.append(col[i])
                i += 1
            r.append(p)
        return r
    def set_info(info):
        lf = s.process.lf3
        lf.process.info = info
        lf.process.dimension = list(map(int, info[0].split()))
        lf.process.field = info[1:]
        lf.process.treeLoc = lf.handlers.findTreeLoc()
    def treeLoc():
        return s.process.lf3.process.treeLoc
    def signature():
        x,y = s.handlers.treeLoc()
        gx,gy = s.process.lf3.process.dimension
        return {"top": y, "left": x, "right": gx-x-1, "bottom": gy-y-1}
    s = ObjMaker.variablesAndFunction(locals())
    return s
def generateField(grid, treeLoc):
    x,y = grid
    tx,ty = treeLoc
    res = ""
    for i in range(y):
        for j in range(x):
            if j == tx and i == ty:
                res += "X"
            else:
                res += "."
        res += "\n"
    return res.strip()
def rotate(lf, times):
    mainField = lf.process.lf3.process.field
    def rotateOnce(field):
        n =[]
        for i in range(len(field[0])-1, -1, -1):
            a = ""
            for j in range(len(field)):
                a += field[j][i]
            n.append(a)
        return n
    field = mainField.copy()
    p = times%4
    for i in range(p):
        field = rotateOnce(field)
    return field
def rotMap(times):
    direc = ["W", "A", "S", "D"]
    p = times%4
    res = {k: direc[(i+p)%4] for i, k in enumerate(direc)}
    return res
def lawnFromField(fieldStr):
    lf = LawnField4()
    field = fieldStr.splitlines()
    lf.process.lf3.process.field = field
    lf.process.lf3.process.dimension = len(field[0]), len(field)
    lf.process.lf3.process.treeLoc = lf.process.lf3.handlers.findTreeLoc()
    return lf
def stringFromField(lf):
    if type(lf) == list:
        return "\n".join(lf)
    return "\n".join(lf.process.lf3.process.field)
def translatePath(path, mmp):
    np = ""
    for k in path:
        np += mmp[k]
    return np
def ZigZagRunner():
    lf = None
    x,y = 0,0
    occupiedLoc = set()
    res = []
    def goInDirection(ctx):
        pass
    def goInOppositeDirection(ctx):
        pass
    def moveByOne(ctx):
        pass
    def checkBreak(x,y,ctx):
        return True
    def zigzag():
        occupiedLoc, res = s.process.occupiedLoc, s.process.res
        while True:
            s.handlers.goInDirection(s)
            nx,ny, letter = s.handlers.moveByOne(s)
            if s.handlers.checkBreak(nx,ny, s): 
                break
            s.process.x, s.process.y = nx,ny
            res.append(letter)
            occupiedLoc.add((nx,ny))
            s.handlers.goInOppositeDirection(s)

            nx,ny, letter = s.handlers.moveByOne(s)
            if s.handlers.checkBreak(nx,ny, s): 
                break
            s.process.x, s.process.y = nx,ny
            res.append(letter)
            occupiedLoc.add((nx,ny))
    def goVerticalCondition(x,y, ctx):
        return y >= 0 and y < ctx.process.gy and (x,y) not in ctx.process.occupiedLoc
    def goUpByOne(ctx):
        x,y = s.process.x, s.process.y
        return x, y-1, "W"
    def set_goUp():
        s.handlers.goCondition = s.handlers.goVerticalCondition
        s.handlers.getNextOne = s.handlers.goUpByOne
    def set_goDown():
        s.handlers.goCondition = s.handlers.goVerticalCondition
        s.handlers.getNextOne = s.handlers.goDownByOne
    def set_goLeft():
        s.handlers.goCondition = s.handlers.goHorizontalCondition
        s.handlers.getNextOne = s.handlers.goLeftByOne
    def set_goRight():
        s.handlers.goCondition = s.handlers.goHorizontalCondition
        s.handlers.getNextOne = s.handlers.goRightByOne
    def goCondition(x,y,ctx):
        raise IOError("Not set yet")
    def goHorizontalCondition(x,y,ctx):
        return x>= 0 and x < ctx.process.gx and (x,y) not in ctx.process.occupiedLoc
    def getNextOne(ctx):
        raise IOError("Not set yet")
    def goRightByOne(ctx):
        x,y = s.process.x, s.process.y
        return x+1, y, "D"
    def goLeftByOne(ctx):
        x,y = s.process.x, s.process.y
        return x-1, y, "A"
    def goDownByOne(ctx):
        x,y = s.process.x, s.process.y
        return x, y+1, "S"
    def go():
        occupiedLoc, res = s.process.occupiedLoc, s.process.res
        while True:
            nx,ny, letter = s.handlers.getNextOne(s)
            if s.handlers.goCondition(nx,ny, s):
                s.process.x, s.process.y = nx,ny
                res.append(letter)
                occupiedLoc.add((nx,ny))
            else:
                break
    def goTillRight(ctx):
        ctx.handlers.set_goRight()
        ctx.handlers.go()
    def goTillLeft(ctx):
        ctx.handlers.set_goLeft()
        ctx.handlers.go()
    def goTillDown(ctx):
        ctx.handlers.set_goDown()
        ctx.handlers.go()
    def goTillUp(ctx):
        ctx.handlers.set_goUp()
        ctx.handlers.go()
    def set_lawn(lf):
        s.process.lf = lf
        s.process.tx,s.process.ty = lf.handlers.treeLoc()
        s.process.gx, s.process.gy = lf.process.lf3.process.dimension
    def resultAsString():
        return "".join(s.process.res)
    s = ObjMaker.variablesAndFunction(locals())
    return s
def CasesForLevel4():
    solvers = {}
    def goUp(x,y,gx,gy, res, occupiedLoc):
        while True:
            if y-1 < 0 or (x, y-1) in occupiedLoc:
                break
            else:
                y = y-1
                res.append("W")
                occupiedLoc.add((x,y))
        return x,y
    def goDown(x,y,gx,gy, res, occupiedLoc):
        while True:
            if y+1 < gy:
                y = y+1
                res.append("S")
                occupiedLoc.add((x,y))
            else:
                break
        return x,y
    def goLeft(x,y,gx,gy, res, occupiedLoc):
        while True:
            if x-1 < 0 or (x-1, y) in occupiedLoc:
                break
            else:
                x = x-1
                res.append("A")
                occupiedLoc.add((x,y))
        return x,y
    def goRight(x,y,gx,gy, res, occupiedLoc):
        while True:
            if x+1 < gx:
                x = x+1
                res.append("D")
                occupiedLoc.add((x,y))
            else:
                break
        return x, y
    def get_case():
        t,l,r,b = s.process.oriVal
        
        if (t%2, r%2) == (1, 1):
            return 1
        elif (t%2, b%2) == (1,0):
            return 2
        elif (l%2, t%2, r%2, b%2) == (0,0,0,0):
            return 3
        return -1
    def _set_up():
        lf = s.process.lf
        tx,ty = lf.handlers.treeLoc()
        gx,gy = lf.process.lf3.process.dimension
        occupiedLoc = set([(tx,ty)])
        res = []
        return tx,ty,gx,gy,occupiedLoc, res
    def case1Sol():
        tx,ty,gx,gy,occupiedLoc,res = s.handlers._set_up()
        x, y = tx-1, ty
        occupiedLoc.add((x,y))
        x, y = goUp(x,y,gx,gy, res, occupiedLoc)
        while True: 
            x, y = goRight(x,y,gx,gy, res, occupiedLoc)
            if (y+1) >= ty:
                break
            y += 1
            res.append("S")
            occupiedLoc.add((x,y))
            x,y = goLeft(x,y,gx,gy, res, occupiedLoc)
            y += 1
            res.append("S")
            occupiedLoc.add((x,y))
            
        # make zigzag till left
        while True:
            # go down 
            x, y = goDown(x,y,gx,gy, res, occupiedLoc)
            if x-1 < 0: # go one left else exit (because it has visited all nodes)
                break
            x = x-1
            res.append("A")
            occupiedLoc.add((x,y))
            x,y = goUp(x,y,gx,gy, res, occupiedLoc)

            if x-1 < 0: # go one left else exit (because it has visited all nodes)
                break
            x = x-1
            res.append("A")
            occupiedLoc.add((x,y))
        return "".join(res)
    def case2Sol():
        tx,ty,gx,gy,occupiedLoc,res = s.handlers._set_up()
        x, y = tx-1, ty
        occupiedLoc.add((x,y))
        toRemove = []
        trx, tryy = tx, ty
        while True:
            if trx + 1 < gx - 2:
                trx += 1
                toRemove.append((trx, tryy))
            else:
                break
        while True:
            if tryy + 1 < gy:
                tryy += 1
                toRemove.append((trx, tryy))
            else:
                break
        for pp in toRemove:
            occupiedLoc.add(pp)
        x, y = goUp(x,y,gx,gy, res, occupiedLoc)
        while True:
            x, y = goRight(x,y,gx,gy, res, occupiedLoc)
            if (y+1) >= gy:
                break
            y = y+1
            res.append("S")
            occupiedLoc.add((x,y))
            x,y = goLeft(x,y,gx,gy, res, occupiedLoc)
            if (y+1) >= gy:
                break
            y = y+1
            res.append("S")
            occupiedLoc.add((x,y))
        for pp in toRemove:
            occupiedLoc.remove(pp)
        
        while True:
            if x-1 < 0:
                break
            x -= 1
            res.append("A")
            occupiedLoc.add((x,y))
            x, y= goUp(x,y,gx,gy, res, occupiedLoc)
            
            if x-1 < 0:
                break
            x -= 1
            res.append("A")
            occupiedLoc.add((x,y))
            x, y= goDown(x,y,gx,gy, res, occupiedLoc)
        return "".join(res)
    def case3Sol():
        def goRightOneStep(x,y):
            x += 1
            res.append("D")
            occupiedLoc.add((x,y))
            return x,y
        tx,ty,gx,gy,occupiedLoc,res = s.handlers._set_up()
        
        x, y = tx-1, ty
        occupiedLoc.add((x,y))
        x, y = goUp(x,y,gx,gy, res, occupiedLoc)
        x, y = goLeft(x,y,gx,gy, res, occupiedLoc)
        
        while True:
            x, y = goDown(x,y,gx,gy, res, occupiedLoc)
            if x+1 >= gx:
                break
            x, y = goRightOneStep(x,y)
            if (x+2) == gx:
                while True:
                    if y-1 < ty:
                        break
                    y -= 1
                    res.append("W")
                    occupiedLoc.add((x,y))
                while True:
                    if y-1 < 0:
                        break
                    y -= 1
                    res.append("W")
                    occupiedLoc.add((x,y))
                    x, y= goLeft(x,y,gx,gy, res, occupiedLoc)
                    y-=1 
                    res.append("W")
                    occupiedLoc.add((x,y))
                    x,y = goRight(x,y,gx-1,gy, res, occupiedLoc)
                x +=1 
                res.append("D")
                occupiedLoc.add((x,y))
            elif x >= tx+1:
                while True:
                    if y-1 < ty:
                        break
                    y -= 1
                    res.append("W")
                    occupiedLoc.add((x,y))
                if x+1 >= gx:
                    break
                x, y = goRightOneStep(x,y)
            else:
                x, y= goUp(x,y,gx,gy, res, occupiedLoc)
                if x+1 >= gx:
                    break
                x, y = goRightOneStep(x,y)
        return "".join(res)
    def set_lawn(lf):
        s.process.lf = lf
        pp = lf.handlers.signature()
        top, left, right, bottom = "top", "left", "right","bottom"
        s.process.oriVal = pp[top], pp[left], pp[right], pp[bottom]
        
        s.process.solvers = {
            1: s.handlers.case1Sol,
            2: s.handlers.case2Sol,
            3: s.handlers.case3Sol
        }
    def solve():
        lf = s.process.lf
        nr = s.handlers.get_case()
        if nr != -1:
            return s.process.solvers[nr]()
        else:
            x,y = s.handlers.getRotTime()
            if x:
                mmp = rotMap(-y)
                lff = lawnFromField("\n".join(rotate(lf, y)))
                s.handlers.set_lawn(lff)
                nr= s.handlers.get_case()
                path = s.process.solvers[nr]()
                s.handlers.set_lawn(lf)
                return (translatePath(path, mmp))
            else:
                print("not solved")
    def getRotTime():
        t,l,r,b = s.process.oriVal
        ov = [t, r,b,l]
        for i in range(1, 4):
            a = ov[i-1]
            b = ov[i]
            if a % 2 == 1 and b % 2== 1:
                return True, i-1
        for i in range(1, 4): #(t%2, b%2)
            a = ov[i]
            b = ov[(i+2)%4]
            if a % 2 == 1 and b % 2== 0:
                return True, i
        return False, -1
    def printLawn():
        lf = s.process.lf
        print("\n".join(lf.process.lf3.process.field))
    s = ObjMaker.variablesAndFunction(locals())
    return s
def allCasesMaker():
    def getCaseAfterRotatation(lwn):
        lf.handlers.set_info(lwn)
        c4lf.handlers.set_lawn(lf)
        cs = c4lf.handlers.get_case()
        if cs != -1:
            return cs
        x,y = c4lf.handlers.getRotTime()
        if x:
            lff = lawnFromField("\n".join(rotate(lf, y)))
            c4lf.handlers.set_lawn(lff)
            return c4lf.handlers.get_case()
        return -1
    files = Path.filesWithExtension("in", "catcoder\\lawn mower\\level4")
    c4lf = CasesForLevel4()
    lf = LawnField4()
    lns = []
    for f in files:
        lf.handlers.set_file(f)
        lns += lf.process.lns
    res = {1:[],2:[],3:[],-1:[]}
    for lwn in lns:
        res[getCaseAfterRotatation(lwn)].append(lwn)
    for nr in res:
        print(nr, len(res[nr]))
    return res
def solve4():
    def solve(lwn):
        lf = LawnField4()
        c4lf = CasesForLevel4()
        lf.handlers.set_info(lwn)
        c4lf.handlers.set_lawn(lf)
        return c4lf.handlers.solve()
    def solveAll():
        files = Path.filesWithExtension("in", "catcoder\\lawn mower\\level4")
        lfp = LawnField4()
        for f in files:
            lfp.handlers.set_file(f)
            lns = lfp.process.lns
            outPath = f+".out"
            res = ""
            for lwn in lns:
                res += solve(lwn) + "\n"
            File.overWrite(outPath, res)
    s = ObjMaker.variablesAndFunction(locals())
    return s
def Level5Solver():
    c4lf = CasesForLevel4()
    lf = LawnField4()
    def bothSidesOdd(lf):
        zzr = ZigZagRunner()
        zzr.handlers.set_lawn(lf)
        zzr.process.y = zzr.process.ty +1 
        zzr.process.x = zzr.process.tx 
        zzr.process.occupiedLoc.add((zzr.process.tx,zzr.process.ty))
        zzr.process.occupiedLoc.add((zzr.process.x,zzr.process.y))
        def checkBreak(x,y,ctx):
            return x > ctx.process.tx+1
        def tilly(x,y,ctx):
            return ctx.handlers.goVerticalCondition(x,y,ctx) and y < ctx.process.gy - 1
        def goInDire(ctx):
            ctx.handlers.set_goDown()
            ctx.handlers.goCondition = tilly
            ctx.handlers.go()
        zzr.handlers.checkBreak = checkBreak
        zzr.handlers.goInDirection = goInDire
        zzr.handlers.goInOppositeDirection = zzr.handlers.goTillUp
        zzr.handlers.moveByOne = zzr.handlers.goRightByOne
        zzr.handlers.zigzag()
        def notVertical(x,y,ctx):
            return not ctx.handlers.goVerticalCondition(x,y,ctx)
        zzr.handlers.checkBreak = notVertical
        zzr.handlers.goInDirection = zzr.handlers.goTillRight
        zzr.handlers.goInOppositeDirection = zzr.handlers.goTillLeft
        zzr.handlers.moveByOne = zzr.handlers.goDownByOne
        zzr.handlers.zigzag()
        zzr.handlers.checkBreak = notVertical
        zzr.handlers.goInDirection = zzr.handlers.goTillUp
        zzr.handlers.goInOppositeDirection = zzr.handlers.goTillDown
        zzr.handlers.moveByOne = zzr.handlers.goRightByOne
        zzr.handlers.zigzag()
        return zzr.handlers.resultAsString()
    def rightSideEven(lf):
        zzr = ZigZagRunner()
        zzr.handlers.set_lawn(lf)
        zzr.process.y = zzr.process.ty +1 
        zzr.process.x = zzr.process.tx 
        zzr.process.occupiedLoc.add((zzr.process.tx,zzr.process.ty))
        zzr.process.occupiedLoc.add((zzr.process.x,zzr.process.y))
        def notVertical(x,y,ctx):
            return not ctx.handlers.goVerticalCondition(x,y,ctx)
        def notHorizontal(x,y,ctx):
            return not ctx.handlers.goHorizontalCondition(x,y,ctx)
        def tilly(x,y,ctx):
            if x == ctx.process.gx - 1:
                return ctx.handlers.goVerticalCondition(x,y,ctx)
            return ctx.handlers.goVerticalCondition(x,y,ctx) and y < ctx.process.gy - 1
        def goInDire(ctx):
            ctx.handlers.set_goDown()
            ctx.handlers.goCondition = tilly
            ctx.handlers.go()
        zzr.handlers.checkBreak = notHorizontal
        zzr.handlers.goInDirection = goInDire
        zzr.handlers.goInOppositeDirection = zzr.handlers.goTillUp
        zzr.handlers.moveByOne = zzr.handlers.goRightByOne
        zzr.handlers.zigzag()
        
        zzr.handlers.checkBreak = notVertical
        zzr.handlers.goInDirection =zzr.handlers.goTillLeft 
        zzr.handlers.goInOppositeDirection = zzr.handlers.goTillRight
        zzr.handlers.moveByOne = zzr.handlers.goUpByOne
        zzr.handlers.zigzag()
        return zzr.handlers.resultAsString()
    def leftZero(lf):
        zzr = ZigZagRunner()
        zzr.handlers.set_lawn(lf)
        zzr.process.y = zzr.process.ty +1 
        zzr.process.x = zzr.process.tx 
        zzr.process.occupiedLoc.add((zzr.process.tx,zzr.process.ty))
        zzr.process.occupiedLoc.add((zzr.process.x, zzr.process.y))
        def notVertical(x,y,ctx):
            return not ctx.handlers.goVerticalCondition(x,y,ctx)
        def notHorizontal(x,y,ctx):
            return not ctx.handlers.goHorizontalCondition(x,y,ctx)
        def notInside(x,y,ctx):
            return notVertical(x,y,ctx) or notHorizontal(x,y,ctx)
        zzr.handlers.checkBreak = notInside
        zzr.handlers.goInDirection = zzr.handlers.goTillDown
        zzr.handlers.goInOppositeDirection = zzr.handlers.goTillUp
        zzr.handlers.moveByOne = zzr.handlers.goRightByOne
        zzr.handlers.zigzag()
        return zzr.handlers.resultAsString()
    def flip(lf, mmp):
        field = lf.process.lf3.process.field
        mmp["A"], mmp["D"] = mmp["D"], mmp["A"]
        return lawnFromField(stringFromField([f[::-1] for f in field])), mmp
    def isOnEdge(lf):
        pos = lf.process.lf3.process.treeLoc
        grid = lf.process.lf3.process.dimension
        x,y = pos
        gx,gy = grid
        if x==0 or y==0:
            return True
        if x+1 == gx or y+1 == gy:
            return True
        return False
    def solve(lwn):
        lf = s.process.lf
        lf.handlers.set_info(lwn)
        if s.handlers.isOnEdge(lf):
            return s.handlers.solveOnEdge(lf)
        else:
            s.process.c4lf.handlers.set_lawn(lf)
            return s.process.c4lf.handlers.solve()
    def solveOnEdge(lf):
        rnr = s.handlers.rotTime(lf)
        mmp = rotMap(-rnr)
        rlf = lawnFromField(stringFromField(rotate(lf, rnr)))
        sig = rlf.handlers.signature()
        if sig["left"] == 0:
            path = s.handlers.leftZero(rlf)
            return translatePath(path, mmp)
        elif sig["right"] % 2 == 0:
            path = s.handlers.rightSideEven(rlf)
            return translatePath(path, mmp)
        elif sig["left"] %2 == 0:
            nrlf, mmp = s.handlers.flip(rlf, mmp)
            path = s.handlers.rightSideEven(nrlf)
            return translatePath(path, mmp)
        path = s.handlers.bothSidesOdd(rlf)
        return translatePath(path, mmp)
    def rotTime(lf):
        pos = lf.process.lf3.process.treeLoc
        grid = lf.process.lf3.process.dimension
        x,y = pos
        gx,gy = grid
        if y == 0:
            return 0
        elif x == 0:
            return 3
        elif x+1 == gx:
            return 1
        return 2
    s = ObjMaker.variablesAndFunction(locals())
    return s
def solvedLevel5():
    def solveAll():
        files = Path.filesWithExtension("in", "catcoder\\lawn mower\\level5")
        lf = LawnField4()
        l5s = Level5Solver()
        
        for f in files:
            lf.handlers.set_file(f)
            outPath = f+".out"
            res = ""
            for ll in lf.process.lns:
                path = l5s.handlers.solve(ll)
                lff = LawnField4()
                lff.handlers.set_info(ll)
                lff.process.lf3.process.lp.handlers.set_path(path)
                res += path + "\n"
                
            File.overWrite(outPath, res)
def Level6Solver():
    def rotNr(lf):
        pos = lf.process.lf3.process.treeLoc
        grid = lf.process.lf3.process.dimension
        x,y = pos
        gx,gy = grid
        if x == 0 and y == 0:
            return 0, True
        elif x == gx-1 and y == 0:
            return 1, True
        elif x == gx-1 and y== gy-1:
            return 2, True
        elif x == 0 and y == gy-1:
            return 3, True
        elif x == 0:
            return 3, False
        elif y == 0:
            return 0, False
        elif x == gx-1:
            return 1, False
        elif y == gy-1:
            return 2, False
        raise IOError()
    def notInCorner(lf):
        zzr = ZigZagRunner()
        zzr.handlers.set_lawn(lf)
        tx,ty = zzr.process.tx,zzr.process.ty
        zzr.process.occupiedLoc.add((tx,ty))
        zzr.process.occupiedLoc.add((zzr.process.x, zzr.process.y))
        
        def breakCon(x,y,c):
            return x > c.process.tx+1
        def tillTy(x,y,c):
            return y < c.process.ty+2
        def goTillDown(c):
            zzr.handlers.set_goDown()
            zzr.handlers.goCondition = tillTy
            zzr.handlers.go()
        zzr.handlers.checkBreak = breakCon
        zzr.handlers.goInDirection = zzr.handlers.goTillUp
        zzr.handlers.goInOppositeDirection = goTillDown
        zzr.handlers.moveByOne = zzr.handlers.goRightByOne
        zzr.handlers.zigzag()
        
        def notHo(x,y,c):
            return not zzr.handlers.goHorizontalCondition(x,y,c)
        zzr.handlers.checkBreak = notHo
        zzr.handlers.goInDirection = zzr.handlers.goTillUp
        zzr.handlers.goInOppositeDirection = goTillDown
        zzr.handlers.moveByOne = zzr.handlers.goRightByOne
        zzr.handlers.zigzag()
        
        def breakCon2(x,y,c):
            return x < 2
        
        zzr.handlers.checkBreak = breakCon2
        zzr.handlers.goInDirection = zzr.handlers.goTillDown
        zzr.handlers.goInOppositeDirection =  zzr.handlers.goTillUp
        zzr.handlers.moveByOne = zzr.handlers.goLeftByOne
        zzr.handlers.zigzag()
        
        def notVer(x,y,c):
            return not zzr.handlers.goVerticalCondition(x,y,c)
        zzr.handlers.checkBreak = notVer
        zzr.handlers.goInDirection = zzr.handlers.goTillLeft
        zzr.handlers.goInOppositeDirection =  zzr.handlers.goTillRight
        zzr.handlers.moveByOne = zzr.handlers.goUpByOne
        zzr.handlers.zigzag()
        return zzr.handlers.resultAsString()
    def solveForCorner(lf):
        zzr = ZigZagRunner()
        zzr.handlers.set_lawn(lf)
        tx,ty = zzr.process.tx,zzr.process.ty
        zzr.process.x, zzr.process.y = x, y+2
        zzr.process.occupiedLoc.add((tx,ty))
        zzr.process.occupiedLoc.add((zzr.process.x, zzr.process.y))
        
        def isInside(x,y,ctx):
            return y >= 0 and y < ctx.process.gy and x >= 0 and x < ctx.process.gx
        def notInside(x,y,ctx):
            isInsideAndNotInoccupied = isInside(x,y,ctx) and (x,y) not in ctx.process.occupiedLoc
            return not isInsideAndNotInoccupied
        def goCond(x,y,ctx):
            return y > 1 
        def tillUp(ctx):
            ctx.handlers.set_goUp()
            ctx.handlers.goCondition = goCond
            ctx.handlers.go()
        def breakCon(x,y,ctx):
            return notInside(x,y,ctx) or x >= ctx.process.gx-2
        zzr.handlers.checkBreak = breakCon
        zzr.handlers.goInDirection = zzr.handlers.goTillDown
        zzr.handlers.goInOppositeDirection = tillUp
        zzr.handlers.moveByOne = zzr.handlers.goRightByOne
        zzr.handlers.zigzag()
        
        def breakCon2(x,y,ctx):
            return y < 2
        zzr.handlers.checkBreak = breakCon2
        zzr.handlers.goInDirection = zzr.handlers.goTillRight
        zzr.handlers.goInOppositeDirection = zzr.handlers.goTillLeft
        zzr.handlers.moveByOne = zzr.handlers.goUpByOne
        zzr.handlers.zigzag()
        
        
        zzr.handlers.checkBreak = notInside
        zzr.handlers.goInDirection = zzr.handlers.goTillUp
        zzr.handlers.goInOppositeDirection = zzr.handlers.goTillDown
        zzr.handlers.moveByOne = zzr.handlers.goLeftByOne
        zzr.handlers.zigzag()
        return zzr.handlers.resultAsString()
    def solveOnEdges(lff):
        nr, isOnCorner = rotNr(lff)
        lf2 = lawnFromField(stringFromField(lff))
        mmp = rotMap(-nr)
        nlff = lawnFromField(stringFromField(rotate(lff, nr)))
        path = ""
        if isOnCorner:
            path = solveForCorner(nlff)
        else:
            path = notInCorner(nlff)
        np = translatePath(path, mmp)
        lf2.process.lf3.process.lp.handlers.set_path(np)
        return np
    def solveAll(files):
        for f in files:
            lf.handlers.set_file(f)
            outPath = f+".out"
            res = ""
            for ll in lf.process.lns:
                
                lff = LawnField4()
                lff.handlers.set_info(ll)
                # lff.process.lf3.process.lp.handlers.set_path(path)
                res += solve(lff) + "\n"
                
            File.overWrite(outPath, res)
    def isOnEdge(lf):
        pos = lf.process.lf3.process.treeLoc
        grid = lf.process.lf3.process.dimension
        x,y = pos
        gx,gy = grid
        if x==0 or y==0:
            return True
        if x+1 == gx or y+1 == gy:
            return True
        return False
    def solveClosedLoop(lff):
        odd = (lff.handlers.signature()["top"] % 2 != 0)
        zzr = ZigZagRunner()
        zzr.handlers.set_lawn(lff)
        tx,ty = zzr.process.tx,zzr.process.ty
        x,y = zzr.process.x, zzr.process.y
        zzr.process.occupiedLoc.add((tx,ty))
        if (x,y) == (tx,ty):
            zzr.process.x, zzr.process.y = tx+1, ty
        zzr.process.occupiedLoc.add((zzr.process.x, zzr.process.y))
        def notVertical(x,y,ctx):
            return not ctx.handlers.goVerticalCondition(x,y,ctx)
        def notHorizontal(x,y,ctx):
            return not ctx.handlers.goHorizontalCondition(x,y,ctx)
        def notInside(x,y,ctx):
            return notVertical(x,y,ctx) or notHorizontal(x,y,ctx)
        def breakCon(x,y,ctx):
            return y == ctx.process.ty
        def goCondition(x,y,ctx):
            return ctx.handlers.goHorizontalCondition(x,y,ctx) and x > 0
        def goTillLeft(ctx):
            ctx.handlers.set_goLeft()
            ctx.handlers.goCondition = goCondition
            ctx.handlers.go()
        zzr.handlers.checkBreak = breakCon
        zzr.handlers.goInDirection = zzr.handlers.goTillRight
        zzr.handlers.goInOppositeDirection = goTillLeft
        zzr.handlers.moveByOne = zzr.handlers.goDownByOne
        zzr.handlers.zigzag()
        
        def goCond(x,y,ctx):
            return ctx.handlers.goVerticalCondition(x,y,ctx) and y < ctx.process.ty+2
        def goDirec(ctx):
            ctx.handlers.set_goDown()
            ctx.handlers.goCondition = goCond
            ctx.handlers.go()
        def breakConOdd(x,y,ctx):
            return x < ctx.process.tx - 1 or not goCondition(x,y,ctx)
        def breakConEven(x,y,ctx):
            return x > ctx.process.tx + 1 or not goCondition(x,y,ctx)
        zzr.handlers.checkBreak = breakConEven 
        if odd:
            zzr.handlers.checkBreak = breakConOdd
        zzr.handlers.goInDirection = goDirec
        zzr.handlers.goInOppositeDirection = zzr.handlers.goTillUp
        zzr.handlers.moveByOne = zzr.handlers.goRightByOne
        if odd:
            zzr.handlers.moveByOne = zzr.handlers.goLeftByOne 
        zzr.handlers.zigzag()
        
        def notIn(x,y,ctx):
            return not goCondition(x,y,ctx)
        zzr.handlers.checkBreak = notIn
        zzr.handlers.goInDirection = zzr.handlers.goTillUp
        zzr.handlers.goInOppositeDirection = goDirec
        zzr.handlers.zigzag()
        
        zzr.handlers.checkBreak = notInside
        
        zzr.handlers.goInDirection = zzr.handlers.goTillRight
        zzr.handlers.goInOppositeDirection = goTillLeft 
        if odd:
            zzr.handlers.goInDirection =goTillLeft 
            zzr.handlers.goInOppositeDirection = zzr.handlers.goTillRight
        zzr.handlers.moveByOne = zzr.handlers.goDownByOne
        zzr.handlers.zigzag()
        zzr.handlers.goInDirection =zzr.handlers.goTillDown
        zzr.handlers.goInOppositeDirection = zzr.handlers.goTillUp
        zzr.handlers.moveByOne = zzr.handlers.goLeftByOne
        zzr.handlers.zigzag()
        return zzr.handlers.resultAsString()
    def solve(lff):
        if isOnEdge(lff):
            return solveOnEdges(lff)
        else:
            nlff = lawnFromField(stringFromField(lff))
            return solveClosedLoop(nlff)
    s = ObjMaker.variablesAndFunction(locals())
    return s