from IPython.core.display import HTML,display
class ArtDB:
    def __init__(self):
        self.canvas = """<canvas id="paper" width="900" height="800" style="border:1px solid #d3d3d3;"/>"""
        display(HTML(self.canvas))
        self.codes = """
            var c = document.getElementById("paper");
            var ctx = c.getContext("2d");
            ctx.beginPath();
        """
        self.canvasIndicator = False
    
    def line(self, initialPos, finalPos, color = "#000"):
        x1,y1 = initialPos
        x2,y2 = finalPos
        self.codes += f"""
            ctx.moveTo({x1}, {y1});
            ctx.lineTo({x2}, {y2});
            ctx.strokeStyle = "{color}";
            ctx.stroke();
            """
        
    def get(self):
        content = f"<script> \n{self.codes}\n</script>"

        return  HTML(content)


import numpy as np
import matplotlib.pyplot as plt

class IObject:
    def get(self):
        pass

class DisplayableObject(IObject):
    def display(self):
        val = self.get()
        plt.imshow(val)
        plt.axis('off')
        plt.show()
    def save(self, name= "untitled.png"):
        val = self.get()
        fig = plt.figure()
        plt.axis('off')
        plt.imshow(val)
        fig.savefig(name, dpi=fig.dpi)
    def set_color(self, c):
        self._color = c
    def get_color_dimension(self):
        return len(self._color)

class BlankImage(DisplayableObject):
    def __init__(self):
        self.set_color((255,255,255))
        self.set_size((200,200))
        self._val = None
        
    def set_size(self, size):
        self._size = size
        
    def get(self):
        if self._val is None:
            x,y = self._size
            self._val = np.full((x, y, 3), self._color)
        return self._val

class Rectangle(DisplayableObject):
    def __init__(self, w, h):
        self._h = h
        self._w = w
    def get(self):
        bi = BlankImage()
        bi.set_size((self._w, self._h))
        bi.set_color(self._color)
        return bi.get()

class RCanvas(BlankImage):
    def addObject(self, pos, obj: IObject):
        val = self.get()
        x,y = pos
        obj_val = obj.get()
        w,h,_ = obj_val.shape
        val[x:x+w, y:y+h] =  obj_val #add masking system to insert one object from another

class Grid(DisplayableObject):
    def set_grid_area_size(self, size):
        self._garea_size = size
    def set_grid_cell_size(self, size ):
        self._gcell_size = size
    def set_color_for_cell_pos(self, pos, color):
        pass
    def set_color_for_cells(self, cells_pos, color):
        for pos in cells_pos:
            self.set_color_for_cell_pos(pos, color)
    def get(self):
        pass
