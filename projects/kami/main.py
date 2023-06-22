from projects.kami.kami import PictureSplitMethod, KamiNeborDetector, NumberKamiImage, CV2ContourDetector
from projects.kami.kami import KamiPart, IFontWriter,ExportQuestion, QuestionFromPickle, KamiObjs
from projects.kami.kami import DistanceCalcWithDijektra, KamiSolverTreeMethod, ImageSplitterIntoBlocks
from ImageProcessing import ColorBoundFromPickle
from modules.Explorer.personalizedWidgets import IBox, GenerateNRowsBox
from SerializationDB import SerializationDB
GRID_SIZE = (28,10)
class Main:
    def nebors_finder(img_path, color_map):
        class Temp:
            def split_method(grid_size = GRID_SIZE):
                psm = PictureSplitMethod()
                psm.set_image(img_path)
                psm.set_color_bound(color_map)
                psm.set_grid_size(grid_size)
                return psm.get_nebors()
            def contour_method(min_area = 30):
                knd = KamiNeborDetector(min_area)
                knd.set_image(img_path)
                knd.set_color_bound(color_map)
                return knd.get_nebors()
        return Temp
    def number_kami_image(img_path, color_map):
        class Temp:
            def contour_method(colors=None, size=30):
                if colors is None:
                    colors = color_map.keys()
                nki = NumberKamiImage(img_path)
                ccd = CV2ContourDetector(img_path)
                ccd.set_filter_area_size(size)
                for ke in colors:
                    l, u = color_map[ke]
                    ccd.add_color_bound(l, u)
                nki.set_contour_finders(ccd)
                nki.execute()
                nki.get_img().open_in_program()
            def split_method(colors= None, grid_size = GRID_SIZE, writer: IFontWriter = None):
                vals = Main.nebors_finder(img_path, color_map).split_method(grid_size)
                Temp.only_kami_objs(vals, grid_size, colors, writer)
            def only_kami_objs(vals: list[KamiPart], grid_size = GRID_SIZE, colors= None, writer: IFontWriter = None):
                kamiObjs = Temp._kami_objects_to_kami_numberable_objects(vals, grid_size, colors)
                nki = NumberKamiImage(img_path)
                nki.set_objects(kamiObjs)
                if writer is not None:
                    nki.set_font_writer(writer)
                nki.execute()
                nki.get_img().open_in_program()
            def _kami_objects_to_kami_numberable_objects(vals: list[KamiPart], grid_size, colors=None):
                if colors is None:
                    colors = list(color_map.keys())
                splitter = ImageSplitterIntoBlocks()
                splitter.set_image(img_path)
                splitter.set_grid(grid_size)
                kamiObjects =[]
                for vla in vals:
                    if vla._color not in colors:
                        continue
                    obj = KamiObjs(vla._id, vla._positions, vla._color)
                    obj.set_color_map(color_map)
                    obj.set_img_splitter(splitter)
                    kamiObjects.append(obj)
                return kamiObjects
            def from_pickle(pkl:str, ids = None, writer: IFontWriter=None):
                vals = SerializationDB.readPickle(pkl)
                kamiParts = []
                for col in vals['color']:
                    for _id in vals['color'][col]:
                        if ids is None:
                            kamiParts.append(KamiPart(_id, col, vals['positions'][_id]))
                        elif _id in ids:
                            kamiParts.append(KamiPart(_id, col, vals['positions'][_id]))
                Temp.only_kami_objs(kamiParts, writer= writer)
            def save_as_pickle(outfile:str= None, ignore_color = None):
                psm = PictureSplitMethod()
                psm.set_image(img_path)
                psm.set_color_bound(color_map)
                psm.set_grid_size(GRID_SIZE)
                psm.set_ignore_color(ignore_color)
                eq = ExportQuestion()
                eq.set_serializable(psm)
                if outfile is None:
                    outfile = img_path + '.pkl'
                eq.export(outfile)
        return Temp
    def color_bound_detector(img_path, out_file_name= None):
        from ImageProcessing import ManualColorBoundFromImageCV2
        mcbc = ManualColorBoundFromImageCV2(img_path)
        vals = mcbc.get_bounds()
        if out_file_name is None:
            return vals
        mcbc.export(out_file_name)
    def project():
        class Temp:
            def display_all(set_nr):
                from Path import Path
                path = f'kami-images/set-{set_nr}/'
                pngs = Path.filesWithExtension('png', path)
                for png in pngs:
                     Temp.number(png).split()
            def number(img_path):
                pkl_path = os.path.dirname(img_path) + os.sep + "colors.pkl"
                colormap = ColorBoundFromPickle(pkl_path).get_bounds()
                class Tem:
                    def contour():
                        Main.number_kami_image(img_path, colormap).contour_method()
                    def split():
                        Main.number_kami_image(img_path, colormap).split_method()
                return Tem
        return Temp
    def hypothesis():
        class Temp:
            def nebor():
                class Tem:
                    def get_key_depth_map(pkl):
                        from ListDB import ListDB
                        from modules.Explorer.DictionaryExplorer import Graph2NodeTreeMakerBreadthFirstSearch
                        qfi = QuestionFromPickle(pkl)
                        rel = qfi.get_info() ['relation']
                        res ={}
                        for key in rel:
                            n = Graph2NodeTreeMakerBreadthFirstSearch(rel, key)
                            res[key] = n.execute().extra_info.depth
                        return ListDB.sortDicBasedOnValue(res)
                    def explorer_for_depth_analysis(pkl, index):
                        qfi = QuestionFromPickle(pkl)
                        rel = qfi.get_info() ['relation']
                        from modules.Explorer.DictionaryExplorer import NodeTreeExplorer, Graph2NodeTreeMakerBreadthFirstSearch, Main
                        Main.explore(NodeTreeExplorer(Graph2NodeTreeMakerBreadthFirstSearch(rel, index).execute()))
                return Tem
            def distance( fr, to, pkl = None, infos = None):
                if pkl is not None:
                    infos = QuestionFromPickle(pkl).get_info()
                if infos is None:
                    print('Give info')
                    return
                class Tem:
                    def path():
                        dcwd = Tem._dcwd_init()
                        return dcwd.generate_path(to)
                    def _dcwd_init():
                        dcwd = DistanceCalcWithDijektra()
                        dcwd.set_info(infos)
                        dcwd.set_initial_pos(fr)
                        return dcwd
                    def cost():
                        dcwd = Tem._dcwd_init()
                        return dcwd.calc_path_cost(fr, to)
                return Tem
        return Temp
    def save(img_path, color_pickle, outpath=None, ignore_colors = []):
        pass
    def solve(img_path, max_steps, pkl = None):
        if pkl is None:
            pkl = img_path + "_colors.pkl"
            if not os.path.exists(pkl):
                Main.color_bound_detector(img_path, pkl)
        color_bounds = ColorBoundFromPickle(pkl).get_bounds()
        qfi_pkl = img_path +'.pkl'
        if not os.path.exists(qfi_pkl):
            Main.number_kami_image(img_path, color_bounds).save_as_pickle()
        vals = Main.nebors_finder(img_path, color_bounds).split_method()
        kst = KamiSolverTreeMethod()
        kst.set_max_steps(max_steps)
        kst.set_pickle(qfi_pkl)
        Main.number_kami_image(img_path, color_bounds).from_pickle(qfi_pkl)
        return kst.get_steps()
class AnalyserTool:
    def __init__(self, img_path):
        self._path = img_path
        self._color_map = ColorBoundFromPickle(os.path.dirname(self._path) + os.sep + "colors.pkl").get_bounds()
        self._pkl_path = img_path + '.pkl'
    def get_key_depth_map(self):
        return Main.hypothesis().nebor().get_key_depth_map(self._pkl_path)
    def show_image_with_numbers(self, numbers = None, all_with_number = None):
        if all_with_number is not None:
            vals = self.get_key_depth_map()
            numbers = [v for v in vals if vals[v] == all_with_number]
        Main.number_kami_image(self._path, self._color_map).from_pickle(self._pkl_path, numbers)
    def get_pkl_info(self):
        qfi = QuestionFromPickle(self._pkl_path)
        return qfi.get_info()
class AnalyserGUI(IBox):
    def __init__(self):
        self._lay = self._get_layout()
    def _get_layout(self):
        from WidgetsDB import WidgetsDB
        import ipywidgets as widgets
        from Path import Path
        lay = GenerateNRowsBox(4)
        row1 = lay.get_child(0)
        row1.add_widget(widgets.Label(value = "Current image:: "))
        row1.add_widget(widgets.Dropdown())
        row1.add_widget(WidgetsDB.button('open'))
        row1.add_widget(WidgetsDB.button('number'))
        row2 = lay.get_child(1)
        row2.add_widget(widgets.Label(value = "dirs:: "))
        row2.add_widget(widgets.Dropdown(options= Path.getDir(self._path)))
        row2.add_widget(WidgetsDB.button('update'))
        return lay
    def set_kami_images_path(self, path):
        self._path = path
    def get(self):
        return self._lay.get()
    def add_events(self):
        open_btn = self._lay.get_child(0).get_child(2)
        open_btn.on_click(lambda x: File.openFile(self._lay.get_child(0).get_child(1).value))
        number_btn = self._lay.get_child(0).get_child(3)
        number_btn.on_click(lambda x: AnalyserTool(
            self._lay.get_child(0).get_child(1).value).show_image_with_numbers())
        def assign(x):
            lay._lay.get_child(0).get_child(1).options = \
                Path.filesWithExtension("png",lay._lay.get_child(1).get_child(1).value)
        update_btn = self._lay.get_child(1).get_child(2)
        update_btn.on_click(assign)
    def old_operations(self):
        # 1-> display
        self._lay.get_child(0).add_widget(WidgetsDB.button('display'))
        display_btn = self._lay.get_child(0).get_child(4)
        def display_img(img_path):
            mi = MatplotImage()
            mi.set_image(img_path)
            mi.display()
        display_btn.on_click(lambda x: display_img(self._lay.get_child(0).get_child(1).value))