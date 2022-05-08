from jupyterDB import jupyterDB
import urllib
import bs4
from TreeDB import TreeDB
from htmlDB import htmlDB
from OpsDB import IOps
from modules.Explorer.personalizedWidgets import IExplorerDisplayer

class Main:
    def make_tree_from_cells(cells: list[bs4.element.Tag]):
        tm = TreeMakerFromMxCells()
        tm.set_cells(cells)
        return tm.execute()
    def tree_from_content(content: str):
        d_co = TreeDB.decodeContent(content)
        soup = d_co.soup_without_xml_part()
        return Main.make_tree_from_cells(soup.find_all("mxcell"))

    def explorer(content, displayit =True):
        doie = DrawIOExplorer()
        doie.set_content(content)
        if displayit:
            doie.display()
        return doie

class IParser:
    def parse(self):
        pass

class DrawIOExplorer(IExplorerDisplayer):
    def __init__(self):
        self.set_file_click_func(self._file_func)
        self.set_folder_click_func(self._folder_click)
        self._exp = None
        self._exp_ds = Main.explore(self._exp, 'Drawio explorer',False)
        self._trr = TreeMakerFromMxCells()

    def set_content(self, content):
        self._content = content
        self._trr.set_content(content)

    def set_cells(self, cells: list[bs4.element.Tag]):
        self._cells = cells
        self._trr.set_cells(cells)

    def set_file_path(self, file:str):
        self._file_path = file
        self._trr.set_file(file)

    def display(self):
        self._root, self._tree_dic = self._trr.execute()
        self._exp = NodeTreeExplorer(self._root)
        self._exp_ds.set_explorer(self._exp)
        self._exp_ds.set_on_folder_selected(self._fl_func)
        self._exp_ds.set_on_file_selected(self._fi_func)
        self._exp_ds.display()

    def set_file_click_func(self, func):
        self._fi_func = lambda x: func(x, self)

    def set_folder_click_func(self, func):
        self._fl_func = lambda x: func(x, self)

    def _file_func(self, x, model=None):
        from IPython.display import display
        self._exp_ds._wid.components.outputDisplay.clear_output()
        with self._exp_ds._wid.components.outputDisplay:
            display(ModuleDB.colorPrint("html", self._tree_dic[x].extra_info.value))

    def _folder_click(self, x, model=None):
        self._exp_ds._wid.components.outputDisplay.clear_output()
        with self._exp_ds._wid.components.outputDisplay:
            if x in self._tree_dic:
                display(ModuleDB.colorPrint("html", self._tree_dic[x].extra_info.value))
class TreeMakerFromMxCells(IOps):
    def __init__(self):
        self._cells_dict = {}
        self._root = None
    def set_cells(self, cells):
        self._cells = cells
        self._execute()
    def execute(self):
        return self._root, self._cells_dict
    def _execute(self):
        for cel in self._cells:
            nd = self.get_node(cel.attrs['id'])
            nd.extra_info.value = cel
            if 'parent' in cel.attrs:
                parent = self.get_node(cel.attrs['parent'])
                parent.children.append(nd)
            else:
                self._root = nd
        return self._root, self._cells_dict
    def get_node(self, idd):
        from modules.FileAnalyser.FileAnalyser import GNode
        if idd not in self._cells_dict:
            val = GNode(idd)
            self._cells_dict[idd] = val
        return self._cells_dict[idd]
    def set_content(self, content: str):
        self._cells_dict = {}
        self._content = content
        d_co = TreeDB.decodeContent(content)
        soup = d_co.soup_without_xml_part()
        self.set_cells(soup.find_all("mxcell"))
    def set_file(self, file:str):
        self._cells_dict = {}
        self._path = file
        pages = TreeDB.drawioPages(file)
        m_root = GNode("root")
        for p in pages:
            content = pages[p]
            self.set_content(content)
            root, _ = self._execute()
            p = self.get_node(p)
            p.children = root.children
            m_root.children.append(p)
        self._root = m_root
class StatusLoggerParser(IParser):
    def __init__(self):
        self._res = {}
        self._cells_dict = {}
    def _parse(self) -> dict:
        res = {}
        p_val = self._extract_content(self._cells)
        vals =[(x['content'], (float(x['geo']['x']), float(x['geo']['y']))) for x in filter(lambda x: len(
            set(x['geo'].keys()).intersection(set(['x','y']))) == 2, p_val)]
        s_vals = sorted(vals, key=lambda x: x[1])
        to = len(s_vals)//2
        keys = s_vals[:to]
        values = s_vals[to:]
        for k, v in zip(sorted(keys, key=lambda x: x[1][1]), sorted(values, key=lambda x: x[1][1])):
            res[k[0]]=v[0]
        return res
    def parse(self) -> dict:
        return self._res
    def set_cells(self, cells: list[bs4.element.Tag]):
        self._cells = cells
        self._res = self._parse()
    def set_content(self, content: str):
        from modules.Explorer.DictionaryExplorer import NodeTreeExplorer
        self._content = content
        self._dec_con = TreeDB.decodeContent(self._content)
        self._dec_soup = htmlDB.getParsedData("\n".join(self._dec_con._content.splitlines()[1:]))
        self._root, self._cells_dict = Main.make_tree_from_cells(self._dec_soup.find_all("mxcell"))
        nte = NodeTreeExplorer(self._root)
        folders, files = nte.dirList()
        res = []
        assert len(files) == 0
        assert len(folders) == 1
        nte.cd(folders[0])
        logs, files = nte.dirList()
        assert len(files) == 0
        for l in logs:
            nte.cd(l)
            cont, daystamp = nte.dirList()
            assert len(daystamp) == 1
            assert len(cont) == 1
            nte.cd(cont[0])
            titles, rows = nte.dirList()
            assert len(titles) == 1, titles
            self.set_cells([self._cells_dict[r].extra_info.value for r in rows])
            res.append({self._cells_dict[daystamp[0]].extra_info.value.attrs['value']: self._res.copy()})
            nte.goBack()
            nte.goBack()
        self._res = res
        self._nte = nte
    def sort(self, res):
        """ele = '<font color="#4c0099"><span style="font-size: 14px">Saturday,<br>02.04.2022</span></font>'"""
        from RegexDB import RegexDB, NameDicExp
        data = lambda x: RegexDB.group_name_search(NameDicExp(".*?",'date', "\d+\.\d+\.\d+", ".*"), x)
        return sorted(res, key=lambda x:list(map(int, list(data(list(x.keys())[0]).values())[0].split(".")[::-1])))
    def set_file_path(self, path:str):
        self._file_path = path
        res = {}
        pages = TreeDB.drawioPages(r"G:\My Drive\Forest\data\status logger.drawio")
        for page in pages:
            content = pages[page]
            self.set_content(content)
            res[page] = self._res.copy()
        self._res = res

    def _extract_content(self,cells):
        pars = []
        for cle in cells:
            attrs = cle.attrs
            if 'style' in attrs:
                if attrs['style'][:5]=="text;":
                    val = {}
                    if attrs['value'] == "":
                        val['content'] = cle.get_text().strip()
                    else:
                        val['content'] = attrs['value']
                    geo = cle.mxgeometry.attrs
                    val['geo'] = geo
                    pars.append(val)
        return pars

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