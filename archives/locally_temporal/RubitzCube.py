class Side:
    Top    = 0
    Left   = 1
    Front  = 2
    Right  = 3
    Back   = 4
    Bottom = 5

class Color:
    Red    = "red"
    Green  = "green"
    Cyan   = "cyan"
    Blue   = "blue"
    Orange = "orange"
    Black  = "black"

class Cube:
    Top    = [Color.Red]   *9
    Left   = [Color.Green] *9
    Front  = [Color.Cyan]  *9
    Right  = [Color.Blue]  *9
    Back   = [Color.Orange]*9
    Bottom = [Color.Black] *9

class GridPosition:
    Top    = (0,1)
    Left   = (1,0)
    Front  = (1,1)
    Right  = (1,2)
    Back   = (1,3)
    Bottom = (2,1)

class IObject:
    def __init__(self):
        self._length = None
        self._position = None
        self._breadth = None

    def setLength(self, l):
        self._length = l

    def setBreadth(self,b):
        self._breadth = b

    def getLength(self):
        IObject.giveErrorIfNone(self._length, "set length first")
        return self._length

    def giveErrorIfNone(val, msg):
        if(val is None):
            raise IOError(msg)

    def getBreadth(self):
        IObject.giveErrorIfNone(self._breadth," set breadth first")
        return self._breadth

    def setPostion(self, pos):
        self._position = pos

    def getPosition(self):
        IObject.giveErrorIfNone(self._position, "set position first")
        return self._position

    def render(self):
        raise IOError("Not implemented yet")

    def liesInside(self, coord):
        raise IOError("Not implemented yet")

class Square(IObject):
    def __init__(self,_id, color, l, pos):
        self.id = _id
        self.color = color
        super().__init__()
        self.setLength(l)
        self.setBreadth(l)
        self.setPostion(pos)

    def render(self, canvas):
        x,y = self.getPosition()
        l = self.getLength()
        canvas.create_rectangle(x,y, x+l,y+l, outline='#ff1', fill=self.color)
        canvas.pack(fill=tk.BOTH, expand=True)

class Grid(IObject):
    def __init__(self, shape, elementsDic):
        self.shape = shape
        self.elements = elementsDic
        super().__init__()

    def render(self, canvas):
        n,m = self.shape
        ia, ib = self.getPosition()
        print(self.elements)
        for i in range(n):
            for j in range(m):
                try:
                    el = self.elements[(j,i)]
                    el.setPostion(ia+i*el.getLength(), ib+j*el.getBreadth())
                    el.render(canvas)
                except:
                    pass
class Render:
    def _common():
        from tkinter import Tk,Canvas
        root = Tk()
        canvas = Canvas(root, bg='grey')
        return root, canvas
    def render(cube):
        root, canvas = Render._common()

        class Temp:
            def generateGrid(coord, shape):
                from CryptsDB import CryptsDB
                g = Grid(shape, {})
                g.setPostion(coord)
                arr2D = ListDB.reshape(cube.Top, shape)

                squareSize = 40
                for i, row in enumerate(arr2D):
                    for j, val in enumerate(row):
                        iid = CryptsDB.generateUniqueId()
                        ob = Temp.squareObj(iid, val, g.getPosition(), (i,j),squareSize)
                        g.elements[(i,j)] = ob

                g.setLength(shape[0]*squareSize)
                g.setBreadth(shape[1]*squareSize)
                return g

            def squareObj(iid, color, parentPos, coord, squareSize = 40):
                a,b  = parentPos
                i, j = coord
                sq = Square(iid, color, squareSize)
                sq.setPostion((a + i* squareSize, b+ j * squareSize))
                return sq

        shape = (3,3)
        arr = [GridPosition.Top, GridPosition.Left,GridPosition.Front,
               GridPosition.Right,GridPosition.Back,GridPosition.Bottom]
        g = Grid((4,3),{})
        g.setPostion((20,20))
        a1, b1 = 0,0
        for a,b in arr:
            iniX, iniY = g.getPosition()
            coord = (iniX + a*a1, iniY+b*b1)
            el = Temp.generateGrid(coord, shape)
            print(el._position)
            a1 = el.getLength()
            b1 = el.getBreadth()
            g.elements[(a,b)] = el
        g.render(canvas)

        canvas.pack(fill=tk.BOTH, expand=True)
        root.mainloop()

    def renderObj(obj):
        root, canvas = Render._common()
        obj.render(canvas)
        root.mainloop()
class InputHandler:
    pass
    
class RubitzCube:
    def __init__(self):
        self.rect = None
        self.initX = 20
        self.initY = 20
        self.squareSize = 40

        self.createWindow()

    def createWindow(self):
        from tkinter import Tk,Canvas

        root = Tk()
        self.canvas = Canvas(root, bg='grey')
        self.canvas.bind("<Button-1>", self.callback)
        self.canvas.bind("<ButtonRelease-1>", self.shift)


        red, green, cyan, blue, orange, black = [lambda x, y,k=val: Diagrams.grid(self.canvas, 3,3,x,y,self.squareSize, k)
                                                   for val in ["red", "green", "cyan", "blue", "orange", "black"]]

        self.gridVal = {
            (0,1): red,
            (1,0): green,
            (1,1): blue,
            (1,2): cyan,
            (1,3): orange,
            (2,1): black
        }
        Diagrams.gridContainer(4,4, self.gridVal, self.squareSize*3)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        root.mainloop()

    def callback(self, event):
        x, y = event.x, event.y
        if(x >  self.initX  + 120 and x < self.initX +240):
            if(y > self.initY and y < self.initY + 360):
                self.rect = (x,y)
        if(y > self.initY +120 and y < self.initY + 2 *120):
            if(x > self.initX and x < self.initX + 4*120):
                self.rect = (x,y)

    def shift(self,event):
        x1, y1 = event.x, event.y
        if(self.rect is None):
            return
        x2, y2 = self.rect
        self.canvas.delete("all")
        self.initX = self.initX - x2 + x1
        self.initY = self.initY - y2 + y1
        self.rect = None
        Diagrams.gridContainer(4,4, self.gridVal, self.squareSize*3, self.initX, self.initY)

    def rotateRight(self):
        pass