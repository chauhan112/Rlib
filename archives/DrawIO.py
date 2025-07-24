from useful.jupyterDB import jupyterDB
import urllib
import bs4
from useful.TreeDB import TreeDB
from useful.htmlDB import htmlDB
from useful.OpsDB import IOps
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
        from modules.Explorer.personalizedWidgets import WidgetsIpyExplorerDisplayer
        self.set_file_click_func(self._file_func)
        self.set_folder_click_func(self._folder_click)
        self._exp = None
        self._exp_ds = WidgetsIpyExplorerDisplayer('Drawio explorer')
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
        from modules.Explorer.DictionaryExplorer import NodeTreeExplorer
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
        from useful.ModuleDB import ModuleDB
        self._exp_ds._wid.components.outputDisplay.clear_output()
        with self._exp_ds._wid.components.outputDisplay:
            display(ModuleDB.colorPrint("html", self._tree_dic[x].extra_info.value))

    def _folder_click(self, x, model=None):
        from useful.ModuleDB import ModuleDB
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
        from modules.FileAnalyser.FileAnalyser import GNode
        self._cells_dict = {}
        self._path = file
        pages = TreeDB.drawioPages(file)
        m_root = GNode("root")
        for p in pages:
            content = pages[p]
            d_co = TreeDB.decodeContent(content)
            soup = d_co.soup_without_xml_part()
            self.set_cells(soup.find_all("mxcell"))
            p = self.get_node(p)
            p.children = self._root.children
            m_root.children.append(p)
        self._root = m_root
class StatusLoggerParser(IParser):
    def __init__(self):
        self._res = {}
        self._cells_dict = {}
        self._extr = ExtractGeometryInfo()
    def _parse(self) -> dict:
        res = {}
        self._extr.set_cells(self._cells)
        p_val = self._extr.execute()
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
        from useful.RegexDB import RegexDB, NameDicExp
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

class ExtractGeometryInfo(IOps):
    def set_cells(self, cells):
        self._cells = cells

    def execute(self):
        pars = []
        for cle in self._cells:
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

class SortHorizontallyAndSplitIntoColumns(IOps):
    def __init__(self, arr: list[tuple] =None, cols_nr: int=None):
        self.set_values(arr)
        self.set_nr_of_cols(cols_nr)
    def set_nr_of_cols(self, nr: int):
        self._cols_nr = nr
    def set_values(self, arr: list[tuple]):
        self._arr = arr
    def execute(self):
        res = []
        size = len(self._arr)//self._cols_nr
        for i in range(self._cols_nr):
            res.append(self._arr[i*size: (i+1)* size])
        return res
    def set_dic(self, p_val: list[dict]):
        """
        p: elements in p_val are of type dict{'content', 'geo':{x, y, height, width}}
            check result of ExtractGeometryInfo class
        """
        vals =[(x['content'], (float(x['geo']['x']), float(x['geo']['y']))) for x in filter(lambda x: len(
            set(x['geo'].keys()).intersection(set(['x','y']))) == 2, p_val)]
        self._arr = s_vals = sorted(vals, key=lambda x: x[1])

class SortVerticallyAndExtract(IOps):
    def set_values(self, arr: list[tuple]):
        self._arr = arr
    def execute(self):
        arr = self._arr
        arr = sorted(arr, key=lambda x: x[1][1])
        arr = [e[0] for e in arr]
        new_arr = []
        for ele in arr:
            if ele.strip() == "..":
                new_arr.append([ele])
            else:
                new_arr.append(TreeDB.decodeContent(ele).soup_without_xml_part().strings)
        return ['\n'.join(val) for val in new_arr]
class DailyScrumParser(IParser):
    def parse(self):
        results = {}
        for page in pages:
            results[page] = []
            exp.cd(page)
            p, el = exp.dirList()
            assert len(p) == 1 and len(el) == 0
            exp.cd(p[0])
            pp, els = exp.dirList()
            assert len(els) == 0
            for day_scrum in pp:
                exp.cd(day_scrum)
                sec, header = exp.dirList()
                assert len(sec) == 2 and len(header) == 1
                ssec = sorted(sec, key=lambda x: int(trr.get_node(x).extra_info.value.mxgeometry['y']))
                upper, lower = ssec
                res = []
                for s in ssec:
                    exp.cd(s)
                    subsec, logs = exp.dirList()
                    assert len(subsec) == 0
                    res.append(self._make_result(logs))
                    exp.goBack()
                top, bottom = res
                # not ccomplete yet
                
    def _make_result(self, keys):
        res = {}
        mxcelss = [self._tree._cells_dict[x].extra_info.value for x in keys]
        egi = ExtractGeometryInfo()
        egi.set_cells(mxcelss)
        vals_geo = egi.execute()
        shasic = SortHorizontallyAndSplitIntoColumns()
        shasic.set_dic(vals_geo)
        shasic.set_nr_of_cols(4)
        cols = shasic.execute()
        key = cols[1]
        d_time = cols[2]
        s_time = cols[3]
        svae = SortVerticallyAndExtract()
        svae.set_values(key)
        res['name'] = svae.execute()
        svae.set_values(d_time)
        res['given duration'] = svae.execute()
        svae.set_values(s_time)
        res['start time'] = svae.execute()
        return res