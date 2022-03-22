from jupyterDB import jupyterDB
import urllib

class DrawIOWord:
    def __init__(self,val, parentId = 1, geometry = None, color = '#ba0000',align = "left"):
        self._id = 2
        self.val = val
        self.geometry = geometry
        self.color = color
        self.parentId = parentId
        self.align = align
        
    def string(self):
        geoVal = self.geometry.string()
        if(self.geometry is None):
            geoVal = '{}'
        return f"""<mxCell id="{self._id}" parent="{self.parentId}" """ \
                f"""style="text;html=1;resizable=0;points=[];autosize=1;align={self.align};verticalAlign="""\
                f"""top;spacingTop=-4;strokeColor=none;" value=\'&lt;font color="#00cccc"&gt;""" \
                f"""{self.val}&lt;/font&gt;\' vertex="1">{geoVal}</mxCell>"""
    def setGeometry(self, geometry):
        self.geometry = geometry
    
    def setId(self, val):
        self._id = val

class DrawIO:
    def __init__(self, words):
        self.words = words
        self.maxX = 0
        self.maxY = 0
        self._update()
    
    def _string(self, sth = ''):
        val = ''
        for w in self.words:
            val += w.string()
        return f'<mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/>{sth + val}</root></mxGraphModel>'
    def copy(self):
        jupyterDB.clip().copy(urllib.parse.quote(self._string()))
    
    def merge(self, anotherDrawio):
        self.words += anotherDrawio.words
        self._update()
        
    def _setMaxes(self, geometry):
        x = geometry.x + geometry.w
        y = geometry.y + geometry.h
        if(self.maxX < x):
            self.maxX = x
        if(self.maxY < y):
            self.maxY = y
    def _update(self, ids = 2):
        for w in self.words:
            w.setId(ids)
            w.geometry.w = len(w.val)* 6 + 20
            self._setMaxes(w.geometry)
            ids += 1
        
class DrawIOGeometry:
    def __init__(self, x= 0, y= 0, h= 20, w =20):
        self.x= x
        self.y = y
        self.h =h
        self.w = w
        
    def string(self):
        return f'<mxGeometry as="geometry" height="{self.h}" width="{self.w}" x="{self.x}" y="{self.y}"/>'
    
def lineOne(left='..', middle= "..", right= "..", y = 0):
    words = [DrawIOWord(left, geometry=DrawIOGeometry(x = 0, y=y), align="right"), 
     DrawIOWord(middle, geometry=DrawIOGeometry(x = 80, y=y)),
     DrawIOWord(right, geometry=DrawIOGeometry(x = 230, y=y))]
    return DrawIO(words)
    
    
def dailyScrum():
    pass

def waterFallContainer():
    pass

def container(iid = 2, parent = 1):
    drawIO = DrawIO([])
    inc = 0
    for i in range(10):
        drawIO.merge(lineOne(y = inc))
        inc += 22
    contain = f"""<mxCell connectable="0" id="{iid}" parent="{parent}" style="group;strokeColor=#000000;"""\
                f"""opacity=30;" value="" vertex="1"><mxGeometry as="geometry" height="{drawIO.maxX+2}" """ \
                f"""width="{drawIO.maxY+2}" x="0" y="0"/></mxCell>"""
    s = iid +1
    for w in drawIO.words:
        w.parentId = iid
        w._id = s
        s += 1
    jupyterDB.clip().copy(urllib.parse.quote(drawIO._string(contain)))