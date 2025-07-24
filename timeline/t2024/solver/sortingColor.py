from useful.basic import Main as ObjMaker
import cv2
from ancient.ImageProcessing import ImageProcessing, Contour, CVImage
import numpy as np
from skimage import color

def ColorSorting():
    image_path = None
    def filterFunc(x):
        a = cv2.contourArea(x)
        return a < 50000 and a > 40000
    def set_image(image_path):
        s.process.image_path = image_path
        s.process.img_data = ImageProcessing.getCV2Image(image_path, "PIL")
        c = Contour.getAllContours(image_path, ([  0,   0, 201],[128,  47, 255]))
        nc = list(filter(s.handlers.filterFunc, c))
        nc = sorted(nc, key=lambda x: tuple(x[0][0][::-1]))
        nc = nc[:-2]
        s.process.bottles = nc
        s.handlers.calcRectanglesAroundBottles()
    def bottlesAreas():
        for cc in s.process.bottles:
            print(cv2.contourArea(cc))
    def calcRectanglesAroundBottles():
        img_data = s.process.img_data.copy()
        cropped = []
        for c in s.process.bottles:
            rect = cv2.boundingRect(c)
            x,y,w,h = rect
            k = int(h*.1)
            s_cropped = img_data[y+k: y+h, x: x+w]
            cropped.append(s_cropped)
            cv2.rectangle(img_data,(x,y+k),(x+w,y+h),(0,255,0),2)
        s.process.rectangles = cropped
        s.process.image_with_rectangles = img_data
        s.process.allSegs = [s.handlers.getSegs(cr) for cr in cropped]
    def getSegs(cropped):
        h, w, _ = cropped.shape
        seg = h//4
        first = seg//2
        res = [first + seg* i  for i in range(4)]
        a = w//2
        l= 24
        hl = l//2
        segs = [cropped[b-hl: b+hl, a - hl: a + hl] for b in res]
        return segs
    def displayRectangle(nr = -1):
        if nr == -1:
            CVImage(s.process.image_with_rectangles).display_in_window()
            return
        s_cropped = s.process.rectangles[nr]
        h, w, _ = s_cropped.shape
        l = 24
        hl= l//2
        nco = s_cropped.copy()
        seg = h//4
        first = seg//2
        res = [first + seg* i  for i in range(4)]
        a = w//2
        for b in res:
            cv2.rectangle(nco, (a-hl,b-hl),(a+hl,b+hl), (0,255,0))
        CVImage(nco).display_in_window()
    def showSegs(btlNr, nr, inAll=False):
        if not inAll:
            cv2.imshow("Show",s.process.allSegs[btlNr][nr])
            cv2.waitKey()  
            cv2.destroyAllWindows()
            return 
        img_data = s.process.img_data.copy()
        hsv = cv2.cvtColor(s.process.allSegs[btlNr][nr], cv2.COLOR_BGR2HSV)
        lb = hsv.min(1).min(0)
        up = hsv.max(1).max(0)
        img_hsv = cv2.cvtColor(img_data, cv2.COLOR_BGR2HSV)
        redObject = cv2.inRange(img_hsv,lb,up)
        kernal = np.ones((1,1),"uint8")
        red = cv2.morphologyEx(redObject,cv2.MORPH_OPEN,kernal)
        red = cv2.dilate(red,kernal,iterations=1)
        res1=cv2.bitwise_and(img_data, img_data, mask = red)
        CVImage(res1).display_in_window()
    def verify(arr):
        iv = {}
        for row in arr:
            for v in row:
                if v not in iv:
                    iv[v] = 0
                iv[v] += 1
        for v in iv.values():
            assert v == 4
    def get_resulting_array():
        def meanIt():
            mas = []
            for b in cs.process.allSegs:
                rb = []
                for sec in b:
                    rb.append(sec.reshape((-1,3)).mean(0))
                mas.append(rb)
            return mas
        def sortedCoord(mas):
            narr = np.array(mas).reshape(-1,3)
            darr = []
            for i in range(len(narr)):
                d = []
                for j in range(len(narr)):
                    d.append(s.handlers.delta_e(narr[i], narr[j]))
                darr.append(d)
            darr = np.array(darr)
            srted = np.argsort(darr, axis=1)
            coords = np.column_stack([srted.flatten()//4, srted.flatten()%4]).reshape((narr.shape[0],narr.shape[0],-1))
            first4Similar = coords[:, :4]
            return first4Similar
        def indexed(first4Similar):
            iarr = {}
            index = 0
            for r in first4Similar:
                rr = []
                added = False
                for c in r:
                    co = tuple(c)
                    if co not in iarr:
                        added = True
                        iarr[co] = index
                if added:
                    index += 1
            return iarr
        iarr = indexed(sortedCoord(meanIt()))
        ires = []
        for i in range(12):
            l = []
            for j in range(4):
                l.append(iarr[(i,j)])
            ires.append(l)
        s.handlers.verify(ires)
        return ires
    def rgb_to_lab(rgb_pixel):
        rgb_pixel = np.array(rgb_pixel, dtype=np.float64).reshape(1, 1, 3)
        rgb_pixel = rgb_pixel / 255.0
        lab_pixel = color.rgb2lab(rgb_pixel)
        return lab_pixel[0, 0]
    
    def delta_e(rgb1, rgb2):
        lab1 = rgb_to_lab(rgb1)
        lab2 = rgb_to_lab(rgb2)
        
        delta_l = lab2[0] - lab1[0]  # L difference
        delta_a = lab2[1] - lab1[1]  # A difference
        delta_b = lab2[2] - lab1[2]  # B difference
        
        delta_e = np.sqrt(delta_l**2 + delta_a**2 + delta_b**2)
        return delta_e
    s = ObjMaker.variablesAndFunction(locals())
    return s
class Layer:
    def __init__(self, layerNr = -1):
        self.value = None
        self.next = None
        self.state = None
        self.layerNr = layerNr
        self.possibilities = None
class Bottle:
    def __init__(self,data = None, index= None):
        self.index = index
        if data is None:
            self.data = []
        else:
            self.data = data
    def canPour(self, target):
        if target.index == self.index:
            return False
        if len(target.data) >= 4: # target is full
            return False
        if len(self.data) == 0: # this bottle is empty
            return False
        if len(target.data) == 0: # target is empty
            return True
        return self.data[-1] == target.data[-1]
    def pour(self, target):
        pourCount = 0
        while self.canPour(target):
            pourCount += 1
            target.data.append(self.data.pop())
        return pourCount
def Solver():
    statesValues = []
    steps = []
    counter = 0
    lastLayer = Layer(0)
    allStates = set()
    statesTrackCount = 10
    debug = False
    def isFullAndSame(row):
        if len(row) < 4:
            return False
        v = row[0]
        for e in row:
            if e != v:
                return False
        return True
    def calPosibilities():
        bottles = s.process.bottles
        res = []
        for i in range(len(bottles)):
            a = bottles[i]
            if s.handlers.isFullAndSame(a.data):
                continue
            for j in range(len(bottles)):
                if i == j:
                    continue
                b = bottles[j]
                if a.canPour(b):
                    res.append((i,j))
        return res
    def isSolved():
        bottles = s.process.bottles
        for b in bottles:
            row = b.data
            if len(row) == 0:
                continue
            if not s.handlers.isFullAndSame(row):
                return False
        return True
    def undo(a,b,t):
        bottles = s.process.bottles
        for i in range(t):
            bottles[b].data.append(bottles[a].data.pop())
        for bo in bottles:
            assert len(bo.data) < 5
        if s.process.debug:
            print(s.handlers.pprinter(a,b))
        s.process.steps.pop()
    def get_state():
        bottles = s.process.bottles
        return str(sorted([b.data for b in bottles]))
    def addStates(a,b):
        i = s.process.counter
        s.process.steps.append((a,b))
        if len(s.process.statesValues)  < s.process.statesTrackCount:
            s.process.statesValues.append((i, s.handlers.pprinter(a,b)))
        else:
            s.process.statesValues[i%s.process.statesTrackCount] = (i, s.handlers.pprinter(a,b))
    def undoIfNoPossible():
        bottles = s.process.bottles
        if s.handlers.isSolved():
            return "solved"
        a,b,t = s.process.lastLayer.prev.revertInfo
        s.handlers.undo(b,a,t)
        s.process.lastLayer = s.process.lastLayer.prev
        return "undoing"
    def pprinter (x=None,y=None):
        bottles = s.process.bottles
        res = ""
        for i, b in enumerate(bottles):
            if i == x:
                res += f">b-{i} : " + str(b.data) + "\n"
            elif i == y:
                res += f"<b-{i} : " + str(b.data) + "\n"
            else:
                res += f"b-{i}  : "+ str(b.data) + "\n"
        return res
    def solve_with_memo():
        s.process.counter += 1
        while True:
            while len(s.process.lastLayer.possibilities) == 0:
                rr = s.handlers.undoIfNoPossible()
                if rr == "solved":
                    return rr
            a, b = s.process.lastLayer.possibilities.pop()
            t = s.process.bottles[a].pour(s.process.bottles[b])
            s.handlers.addStates(a,b)
            if s.handlers.get_state() in s.process.allStates:
                print("collision", s.handlers.get_state(), s.process.counter)
                s.handlers.undo(b,a,t)
            else:
                break
        s.process.lastLayer.revertInfo = (a,b,t)
        s.process.lastLayer.next = Layer(s.process.lastLayer.layerNr + 1)
    
        s.process.allStates.add(s.handlers.get_state())
        s.process.lastLayer.next.possibilities = s.handlers.calPosibilities()
        s.process.lastLayer.next.prev = s.process.lastLayer
        s.process.lastLayer = s.process.lastLayer.next
        if s.process.debug:
            print(s.handlers.pprinter(a,b))
    def set_game(arr):
        s.process.bottles = [Bottle(x[::-1], i) for i,x in enumerate(arr)]
        s.process.lastLayer.possibilities = s.handlers.calPosibilities()
    s = ObjMaker.variablesAndFunction(locals())
    return s
    
def ListLooper():
    data = None
    index = 0
    def reset():
        s.process.index = 0
    def next():
        p = s.process.index 
        if s.handlers.hasNext():
            s.process.index += 1
            return s.process.data[p]
    def hasNext():
        return s.process.index < len(s.process.data)
    def prev():
        p = s.process.index
        if s.handlers.hasPrev():
            s.process.index -= 1
            return s.process.data[p]
    def hasPrev():
        return s.process.index > 0
    
    s = ObjMaker.variablesAndFunction(locals())
    return s
def WhileLooper():
    data = None
    def brCon(st):
        return False
    def start():
        while True:
            if s.handlers.brCon(s):
                break
            s.handlers.process(s)
    def process(ctx):
        print("ello")
    s = ObjMaker.variablesAndFunction(locals())
    return s

def Out():
    opsWid = Utils.get_comp({},IpywidgetsComponentsEnum.Output, className = "w-auto")
    opsWid2 = Utils.get_comp({},IpywidgetsComponentsEnum.Output, className = "w-auto")
    btn = Utils.get_comp({"description":"add"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    container = Utils.container([btn, Utils.container([opsWid, opsWid2], className="flex flex-row")])
    s = ObjMaker.uisOrganize(locals())
    return s
    
class Main:
    def solve():
        barr = [
         [0, 1, 2, 3],
         [3, 1, 1, 4],
         [5, 6, 2, 5],
         [7, 8, 4, 9],
         [3, 10, 5, 7],
         [6, 8, 2, 10],
         [2, 0, 3, 11],
         [9, 6, 5, 4],
         [8, 1, 11, 0],
         [11, 9, 6, 4],
         [0, 10, 10, 7],
         [7, 9, 11, 8],[],[]]
        barr = [[1,2,1,2],[2,1,2,1],[]]
        barr =[[1,2,3,1],[3,1,2,3],[3,1,2,2],[],[]]
        barr = [[0, 1, 2, 3],
         [4, 5, 6, 6],
         [3, 2, 0, 7],
         [4, 3, 8, 8],
         [6, 7, 9, 8],
         [2, 3, 4, 1],
         [10, 1, 0, 7],
         [4, 0, 10, 5],
         [5, 9, 1, 11],
         [5, 11, 9, 6],
         [9, 10, 11, 8],
         [10, 11, 7, 2],[],[]]
        sol = Solver()
        # sol.process.debug = True
        sol.handlers.set_game(barr)
        for i in range(1000):
            if sol.handlers.isSolved():
                break
            sol.handlers.solve_with_memo()
        print(sol.process.steps)
    def extractArray(img_path):
        cs = ColorSorting()
        cs.handlers.set_image(img_path)
        cs.handlers.get_resulting_array()