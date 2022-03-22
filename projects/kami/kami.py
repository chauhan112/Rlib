import numpy as np
import cv2
from modules.Explorer.personalizedWidgets import IBox, GenerateNRowsBox
from modules.Explorer.DictionaryExplorer import Node
import os
from SerializationDB import SerializationDB
GRID_SIZE = (28,10)
class IAnalyser:
    def analyse(self):
        pass
class ISolver:
    def solve(self):
        pass
class IKamiObj:
    def get_id(self):
        pass
    def get_nebors(self):
        pass
    def get_color(self):
        pass
class ITextable:
    def get_text_pos(self):
        pass
    def get_index(self):
        pass
class KamiObject(IKamiObj, ITextable):
    def __init__(self, index, contour, bound):
        self._index = index
        self._con = contour
        self._bound = bound
        self._nebors = []
    def get_contour(self):
        return self._con
    def get_index(self):
        return self._index
    def get_color_bound(self):
        return self._bound
    def add_nebor(self, nebor):
        self._nebors.append(nebor)
    def get_id(self):
        return self._index
    def get_nebors(self):
        return self._nebors
    def get_color(self):
        return self._bound
    def get_text_pos(self):
        return self.get_centeroid(self._con)
    def get_centeroid(self, cnt):
        length = len(cnt)
        sum_x = np.sum(cnt[..., 0])
        sum_y = np.sum(cnt[..., 1])
        return int(sum_x / length), int(sum_y / length)
class IColorBoundSelector:
    def get_bounds(self):
        pass
class ColorBoundFromPickle(IColorBoundSelector):
    def __init__(self, pkl):
        self._file = pkl
    def get_bounds(self):
        return SerializationDB.readPickle(self._file)
    def add_color_from_image(self, image_path):
        mcbfi = ManualColorBoundFromImageCV2(image_path)
        val = mcbfi.get_bounds()
        self.add_given_color(val)
    def add_given_color(self, colors_dict= {}):
        vals = self.get_bounds()
        vals.update(colors_dict)
        SerializationDB.pickleOut(vals, self._file)
class ManualColorBoundFromImageCV2(IColorBoundSelector):
    def __init__(self, img):
        self._img = img
        self._bounds = {}
    def export(self, name):
        if not name.endswith(".pkl"):
            name += ".pkl"
        SerializationDB.pickleOut(self._bounds, name)
    def get_bounds(self):
        from ImageProcessing import ImageProcessing as imp
        bounds = {}
        while True:
            value = imp.selectColorHSV(self._img)
            name = input("name color: ")
            bounds[name] = value
            if input("Are there more colors (y/n)?").strip().lower() != "y":
                break
        self._bounds = bounds
        return self._bounds
class IContourDetector:
    def get_contour(self):
        pass
class IOps:
    def execute(self):
        pass
class DrawContour(IOps):
    def __init__(self, imgPath, contours):
        self._img = imgPath
        self.set_contour_number(-1)
        self.set_color((0,255,0))
        self.set_width(1)
        self.set_contour(contours)
    def show(self):
        file = "test.png"
        self.save(file)
        File.openFile(file)
#         File.deleteFiles([file])
    def save(self, name):
        import cv2
        from ImageProcessing import ImageProcessing
        img_data = ImageProcessing.getCV2Image(self._img, 'PIL')
        cv2.drawContours(img_data, self._contours, self._cnt_nr, self._color, self._size)
        if not name.endswith(".png"):
            name += ".png"
        cv2.imwrite(name, img_data)
    def set_contour_number(self, nr):
        self._cnt_nr = nr
    def set_color(self, color):
        self._color = color
    def set_width(self, size):
        self._size = size
    def set_contour(self, cont):
        self._contours = cont
class CV2ContourDetector(IContourDetector):
    def __init__(self, img):
        self.set_image(img)
        self._contour = []
        self._bounds = []
        self.set_filter_area_size(1)
    def add_color_bound(self, lower, upper):
        self._bounds.append((lower, upper))
    def get_contour(self):
        from ImageProcessing import Contour
        for bound in self._bounds:
            self._contour += Contour.getAllContours(self._img, bound)
        self._contour = Contour.filterContourWithArea(self._contour, self._min_area)
        return self._contour
    def set_image(self, img):
        self._img = img
        self._contour = None
    def export(self, pkl):
        cont = self.get_contour()
        if not pkl.endswith(".pkl"):
            pkl += ".pkl"
        SerializationDB.pickleOut(cont, pkl)
    def set_filter_area_size(self, value):
        self._min_area = value
class ContourFromPickle(IContourDetector):
    def __init__(self, pkl):
        self._file = pkl
    def get_contour(self):
        return SerializationDB.readPickle(self._file)
class IProximityDetector:
    def get_nebors(self):
        pass
    def set_image(self, img):
        pass
class ISerializable:
    def get_data(self):
        pass
class IImage:
    def save(self, name):
        pass
    def display(self):
        pass
class CVImage(IImage):
    def __init__(self, data = None):
        self.data = data
    def set_image(self, img_path):
        self.data = cv2.imread(img_path)
        self._path = img_path
    def display(self):
        import matplotlib.pyplot as plt
        data = cv2.cvtColor(self.data, cv2.COLOR_BGR2RGB)
        plt.imshow(data)
        plt.show()
    def save(self, name):
        if not name.endswith(".png"):
            name += ".png"
        cv2.imwrite(name, self.data)
    def display_in_window(self):
        cv2.imshow('image',self.data)
        cv2.waitKey(0)
    def open_in_program(self):
        from FileDatabase import File
        file = "test.png"
        self.save(file)
        File.openFile(file)
class MatplotImage(IImage):
    def __init__(self, data = None):
        self.data = data
        if self.data is not None:
            self._cv_img = CVImage(cv2.cvtColor(self.data, cv2.COLOR_RGB2BGR))
    def display(self):
        self._cv_img.display()
    def save(self, name):
        self._cv_img.save(name)
    def display_in_window(self):
        self._cv_img.display_in_window()
    def open_in_program(self):
        self._cv_img.open_in_program()
    def set_image(self, img_path):
        data = cv2.imread(img_path)
        self.data = data[:,:,::-1]
        self._path = img_path
        self._cv_img = CVImage(data)
class ContourOps:
    def add_text(text, pos, img : CVImage, font_scale = 0.5):
        cv2.putText(img.data, text, pos, cv2.FONT_HERSHEY_COMPLEX, font_scale, (0, 0, 0))
    def drawContours(img: CVImage, contour, width=1):
        cv2.drawContours(img.data, np.array([contour]), 0, (0, 255, 0), width)
    def drawPoint(img: CVImage, pos):
        cv2.circle(img.data, pos, radius=0, color=(0, 0, 0), thickness=-1)
    def fill_with_color(img :CVImage, contour, color = (255,255,255)):
        cv2.drawContours(img.data, [contour], -1, color, -1)
class IStrategy:
    def execute(self):
        pass
class NumberKamiImage(IOps):
    def __init__(self, img_path):
        self.set_image(img_path)
        self._objs: list[ITextable] = []
    def set_image(self, img_path):
        self._imgg = CVImage()
        self._imgg.set_image(img_path)
    def execute(self):
        for obj in self._objs:
            pos = obj.get_text_pos()
            ContourOps.add_text(str(obj.get_index()), pos, self._imgg, 1)
    def get_img(self):
        return self._imgg
    def set_contour_finders(self, detector: IContourDetector):
        self._contour_detector = detector
        contours = self._contour_detector.get_contour()
        onsj = []
        for i, c in enumerate(contours):
            onsj.append(KamiObject(i+1, c, ''))
        self._objs = onsj
    def _old_pos(self, cont):
        x,y,w,h = cv2.boundingRect(cont)
        pos = (x + w//2, y+h//2)
        return pos
    def _get_pos(self, cont):
        rect = cv2.minAreaRect(cont)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        pos = np.int0(box.sum(axis=0)/4)
        return pos
    def set_objects(self, objs: list[ITextable]):
        self._objs = objs
class MakeObjects(IOps):
    def __init__(self, img_path, min_area_size = 10):
        self.set_image(img_path)
        self._onjs = []
        self._min_area = min_area_size
    def set_image(self, img_path):
        self._imgg = CVImage()
        self._imgg.set_image(img_path)
        self._img_path = img_path
    def execute(self):
        onjs = []
        index = 0
        for name in self._bounds:
            l, h = self._bounds[name]
            c2cd = CV2ContourDetector(self._img_path)
            c2cd.add_color_bound(l, h)
            c2cd.set_filter_area_size(self._min_area)
            contours = c2cd.get_contour()
            for c in contours:
                onjs.append(KamiObject(index, c, (l,h)))
                index += 1
        self._onjs = onjs
    def get_objects(self):
        return self._onjs
    def set_color_bounds_dict(self, bounds):
        self._bounds = bounds
class PairwiseStrategy(IStrategy):
    def __init__(self, skipper=5):
        self._skipper = skipper
        self._min_nebor_count = 2
        self._distance_between_nebor = 10
    def execute(self, domains):
        import scipy.spatial.distance
        for i, obj in enumerate(domains):
            c = obj.get_contour()[::self._skipper,:,:]
            for nextObj in domains[i+1:]:
                nebor_cont = nextObj.get_contour()[::self._skipper,:,:]
                X = c.reshape((c.shape[0],2))
                Y = nebor_cont.reshape((nebor_cont.shape[0],2))
                dist = scipy.spatial.distance.cdist( X, Y )
                if len(dist[dist < self._distance_between_nebor]) > self._min_nebor_count:
                    nextObj.add_nebor(obj)
                    obj.add_nebor(nextObj)
class DistanceCalc(IStrategy):
    def __init__(self, skipper=5):
        self._skipper = skipper
        self._min_nebor_count = 1
    def execute(self, domains):
        for i, obj in enumerate(domains):
            c = obj.get_contour()
            for nextObj in domains[i+1:]:
                nebor_count = 0
                found = False
                for point in c[::self._skipper]:
                    nebor_cont = nextObj.get_contour()
                    for n_point in nebor_cont[::self._skipper]:
                        if self.is_near(point, n_point):
                            nebor_count += 1
                        if nebor_count > self._min_nebor_count:
                            nextObj.add_nebor(obj)
                            obj.add_nebor(nextObj)
                            found = True
                            break
                    if found:
                        break
    def is_near(self, p1, p2):
        return np.linalg.norm(p1-p2) < 5
class KamiNeborDetector(IProximityDetector):
    def __init__(self, min_area = 10):
        self.set_strategy(PairwiseStrategy(skipper=10))
        self._objs = None
        self._min_area = min_area
    def get_nebors(self):
        if self._objs is None:
            self._objs = self._process()
        self._strategy.execute(self._objs)
        return self._objs
    def set_strategy(self, stra:IStrategy):
        self._strategy = stra
    def set_image(self, img):
        self._img_path = img
    def _process(self):
        mo = MakeObjects(self._img_path, self._min_area)
        mo.set_color_bounds_dict(self._ranges)
        mo.execute()
        return mo.get_objects()
    def set_color_bound(self, ranges):
        self._ranges = ranges
    def set_color_bound_detector(self, dete: IColorBoundSelector):
        self._detector = dete
        self._ranges = dete.get_bounds()
class IQuestion:
    def get_info(self):
        pass
class ExportQuestion(IQuestion):
    def __init__(self):
        self._objs = None
    def get_info(self):
        if self._objs is None:
            self._objs = self._detector.get_data()
        return self._objs
    def set_serializable(self, detector: ISerializable):
        self._detector = detector
    def export(self, pklname):
        if not pklname.endswith(".pkl"):
            pklname += ".pkl"
        SerializationDB.pickleOut(self._detector.get_data(), pklname)
class QuestionFromPickle(IQuestion):
    def __init__(self, pkl):
        self._pkl = pkl
    def get_info(self):
        return SerializationDB.readPickle(self._pkl)
class ISolutionStrategy:
    def execute(self):
        pass
    def set_questions(self, questions):
        self._questions = questions
class NeborCountStrategy(ISolutionStrategy): # not finished yet
    def __init__(self, questions):
        self._steps = -1
        self.set_questions(questions)
    def execute(self):
        self._steps = 0
        vals = OpsDB.group(self._questions, lambda x: len(x._nebors))
        starts = vals[max(vals)]
        for starting_pos in starts:
            colors = OpsDB.group(vals[9][0]._nebors,
                        lambda x: self._get_color_bound_as_tuple(x.get_color_bound()))
            for color in colors:
                self._fill(color, starting_pos)
        return self._steps
    def _fill(self, color, pos):
        pass
    def _get_color_bound_as_tuple(self, bound):
        l, h = bound
        return (tuple(l), tuple(h))
class ISplitter:
    def get(self, pos):
        pass
class ImageSplitterIntoBlocks(ISplitter):
    def set_image(self, path):
        self._path = path
        self._img = MatplotImage()
        self._img.set_image(path)
    def set_grid(self, grid_size):
        self._size = grid_size
    def get(self, pos):
        (xl, xu), (yl,yu) = self._get_pixel(pos)
        block = self._img.data[xl:xu,yl:yu,:]
        return MatplotImage(block)
    def _get_pixel(self, pos):
        x, y = pos
        fac_x, fac_y, _ = self._img.data.shape
        fac_x, fac_y = fac_x / self._size[0], fac_y / self._size[1]
        return (int(x* fac_x), int((x+1)* fac_x)),(int(y*fac_y),int((y+1)*fac_y))
class MosaicRectPiece:
    def __init__(self):
        self.color = {
            'left': None,
            'right': None,
            'top': None,
            'bottom': None
        }
    def set_image_data(self, img_data):
        self.color['left'] = self._get_color_for(img_data[:,:5])
        self.color['right'] = self._get_color_for(img_data[:,-5:])
        self.color['top'] = self._get_color_for(img_data[:5,:])
        self.color['bottom'] = self._get_color_for(img_data[-5:,:])
        self._data = img_data
        if len(set(self.color.values())) > 2:
            raise IOError("error in parsing img data")
    def set_colors_domain(self, colors):
        self._color_map = colors
    def _get_color_for(self, data):
        hsv_data = cv2.cvtColor(data,cv2.COLOR_RGB2HSV)
        val = 0
        res = None
        for name in self._color_map:
            l, u = self._color_map[name]
            frame_threshed = cv2.inRange(hsv_data, l, u)
            frame_threshed = frame_threshed.sum()
            if frame_threshed > val:
                res = name
                val = frame_threshed
        return res
    def _get_central_data(self, data):
        a, b, _ = data.shape
        ma, mb = int(a/2),int(b/2)
        return data[ma-2:ma+2, mb-2: mb+2]
class KamiPart(IKamiObj):
    def __init__(self, _id, color, pos =set(), mosaic_piece_data= None):
        self._positions = pos
        self._nebors = set()
        self._id = _id
        self._color = color
        self._img_piece_data = mosaic_piece_data
    def merge(self, kami_part):
        self._id = kami_part._id
        assert self._color == kami_part._color
        self._positions = self._positions.union(kami_part._positions)
        self._nebors = kami_part._nebors.union(self._nebors)
    def get_id(self):
        return self._id
    def get_nebors(self):
        return self._nebors
    def get_color(self):
        return self._color
class SummarizeTheQuestion(IOps):
    def __init__(self, vals: list[IKamiObj]):
        self._vals = vals
    def get_relation_dict(self):
        dic = {}
        for val in self._vals:
            nebors = val.get_nebors()
            dic[val.get_id()] = []
            for n in nebors:
                dic[val.get_id()].append(n.get_id())
        return dic
    def get_colors(self):
        dic = {}
        for val in self._vals:
            color = val.get_color()
            if color in dic:
                dic[color].append(val.get_id())
            else:
                dic[color] = [val.get_id()]
        return dic
    def execute(self):
        return self.get_relation_dict(), self.get_colors()
class PictureSplitMethod(IProximityDetector, ISerializable):
    def __init__(self):
        self._nebor_finder = None
    def set_image(self, path):
        self._img_path = path
    def _get_mosaic_grids(self, path):
        self._splitter = ImageSplitterIntoBlocks()
        self._splitter.set_image(path)
        self._splitter.set_grid(self._grid_size)
        n, m = self._grid_size
        res = []
        for i in range(n):
            row = []
            for j in range(m):
                mrp = MosaicRectPiece()
                mrp.set_colors_domain(self._ranges)
                mrp.set_image_data(self._splitter.get((i,j)).data)
                row.append(mrp)
            res.append(row)
        return res
    def get_nebors(self):
        if self._nebor_finder is None:
            self._vals = self._get_mosaic_grids(self._img_path)
            self._nebor_finder = NeborFinder()
            self._nebor_finder.set_domain(self._vals)
        return self._nebor_finder.execute()
    def set_color_bound(self, ranges):
        self._ranges = ranges
    def set_color_bound_detector(self, dete: IColorBoundSelector):
        self._detector = dete
        self._ranges = dete.get_bounds()
    def set_grid_size(self, grid_size):
        self._grid_size = grid_size
    def get_data(self):
        vals = self.get_nebors()
        rel, colors = SummarizeTheQuestion(vals).execute()
        pos = {}
        for val in vals:
            pos[val.get_id()] = val._positions
        return {'relation': rel, 'color': colors, 'positions': pos}
class NeborFinder:
    def set_domain(self, vals: list[MosaicRectPiece]):
        self._val = vals
        self._initialize(vals)
        self._identify_objs(vals)
        self._find_nebors(vals)
    def execute(self):
        vals = set(self._lister.values())
        for i, val in enumerate(vals):
            val._id = i
        return vals
    def _initialize(self, vals):
        self._lister = {}
        ids = 0
        for i, row in enumerate(vals):
            for j, mrp in enumerate(row):
                colors = set(mrp.color.values())
                for c in colors:
                    self._lister[(i,j,c)] = KamiPart(ids, c, set([(i,j)]), mrp)
                    ids += 1
    def _identify_objs(self, vals):
        for i, row in enumerate(vals):
            for j, mrp in enumerate(row):
                if i != 0:
                    top = vals[i-1][j]
                    c = top.color['bottom']
                    if c == mrp.color['top']:
                        self._merge((i-1,j), (i,j), c)
                if j != 0:
                    left = vals[i][j-1]
                    c = left.color['right']
                    if c == mrp.color['left']:
                        self._merge((i,j), (i,j-1), c)
    def _find_nebors(self, vals):
        for i, row in enumerate(vals):
            for j, mrp in enumerate(row):
                # case 1: inside a box can be a nebor
                colors = set(mrp.color.values())
                if len(colors) == 2:
                    c1,c2 = colors
                    self._add_nebor(self._lister[(i,j,c1)], self._lister[(i,j,c2)])
                # case 2: check boundary
                if i != 0:
                    top = vals[i-1][j]
                    if top.color['bottom'] != mrp.color['top']:
                        self._add_nebor(self._lister[(i-1,j,top.color['bottom'])],
                                        self._lister[(i,j,mrp.color['top'])])
                if j != 0:
                    left = vals[i][j-1]
                    if left.color['right'] != mrp.color['left']:
                        self._add_nebor(self._lister[(i, j-1, left.color['right'])],
                                        self._lister[(i,j, mrp.color['left'])])
    def _add_nebor(self,a: KamiPart, b: KamiPart):
        a._nebors.add(b)
        b._nebors.add(a)
    def _merge(self, pos1, pos2, color):
        val = self._lister[(*pos1, color)]
        val2 = self._lister[(*pos2, color)]
        val.merge(val2)
        for pos in val._positions.union(self._lister[(*pos2, color)]._positions):
            self._lister[(*pos, color)] = val
class KamiObjs(ITextable):
    def __init__(self, _id, positions, color):
        self._positions = positions
        self._color = color
        self._id = _id
    def set_img_splitter(self, splitter): 
        # the reason for setting splitter like this instead of giving image as input is to save 
        # processing power because there can be many
        # kami objects but the splitter is same for all the kami objects
        self._splitter = splitter
    def set_color_map(self, color_map):
        self._color_map = color_map
    def get_text_pos(self):
        found, pos = self._check_for_all_side_color()
        if found:
            x, y = self._splitter._get_pixel(pos)
            val = x[0], y[0]
        val = self._find_triangular_centroid(pos)
        x,y = val
        return y,x
    def _find_triangular_centroid(self, pos):
        mrp = self._get_mosaic_part(pos)
        (x1,x2), (y1,y2) = self._splitter._get_pixel(pos)
        p1,p2,p3,p4 = (x1,y1),(x1,y2), (x2,y2),(x2,y1)
        tri_map = {
            'top': set([p1, p2]),
            'left': set([p1, p4]),
            'right': set([p2,p3]),
            'bottom': set([p3,p4])
        }
        points = set()
        for col in mrp.color:
            if mrp.color[col] == self._color:
                points = points.union(tri_map[col])
        x, y= 0,0
        for a, b in points:
            x += a
            y += b
        return  int(x/len(points)), int(y/len(points))
    def _check_for_all_side_color(self):
        first = None
        for pos in self._positions:
            mrp = self._get_mosaic_part(pos)
            if first is None:
                first = pos
            if len(set(mrp.color.values())) == 1:
                return True, pos
        return False, first
    def _get_mosaic_part(self, pos):
        mrp = MosaicRectPiece()
        mrp.set_colors_domain(self._color_map)
        mrp.set_image_data(self._splitter.get(pos).data)
        return mrp
    def get_index(self):
        return str(self._id)
class Nebor2VerticesForDijeckstra(IOps):
    def __init__(self):
        self._res = None
    def set_kami_objects(self, nebors: list[IKamiObj]):
        self._nebors = nebors
        vertices = {}
        for oj in self._nebors:
            vertices[oj.get_id()] = {}
            for obj in oj.get_nebors():
                vertices[oj.get_id()][obj.get_id()] = 1
        self._res = vertices
    def set_dictionary_relations(self, rel):
        dic = {}
        for key in rel:
            dic[key] = {}
            for neb in rel[key]:
                dic[key][neb] = 1
        self._res = dic
    def execute(self):
        return self._res
class DistanceSolverOperation(IOps):
    def __init__(self, questions: list[IKamiObj], parts: list[IKamiObj]):
        self.set_questions(questions)
        self.set_parts(parts)
    def set_questions(self, questions: list[IKamiObj]):
        self._que = questions
        self._vertices = Nebor2VerticesForDijeckstra(questions).execute()
        self._colormap = {oj.get_id(): np.array(oj.get_color_bound()) for oj in questions}
    def set_parts(self, parts: list[IKamiObj]):
        parts = sorted(parts, key =lambda x : x.get_id())
        self._parts = parts
    def execute(self):
        questions, parts = self._que, self._parts
        dj = Dijkstra(self._vertices.keys(), self._vertices)
        parts_color = self._colormap[parts[0].get_id()]
        res = {}
        for i in range(1, len(parts)):
            a = parts[i-1].get_id()
            b = parts[i].get_id()
            parent, path_weight = dj.find_route(a, b)
            path = Dijkstra.generate_path(parent, a, b)
            path_val = len(path)
            for val in path:
                if np.array_equal(self._colormap[val] , parts_color):
                    path_val -= 1
            res[(a, b)] = path, path_val
        return res
class DistanceCalcWithDijektra:
    def __init__(self):
        self._parent = None
    def set_pkl_path(self, pkl):
        self.set_info(QuestionFromPickle(pkl).get_info())
    def set_info(self, infos):
        from ListDB import ListDB
        self._info = infos
        self._relation = self._info['relation']
        self._color_map = ListDB.dicOps().reverseKeyValue(infos['color'])
    def generate_path(self, to, initial_pos = None):
        from AIAlgoDB import Dijkstra
        if initial_pos is not None:
            self.set_initial_pos(initial_pos)
        self._graph = self._make_relation_distance_dic()
        dj = Dijkstra(self._relation.keys(), self._graph)
        self._parent, _ = dj.find_route(self._start, to)
        return dj.generate_path(self._parent, self._start, to)
    def set_initial_pos(self, start_pos):
        self._start = start_pos
    def calc_path_cost(self, from_= None, to = None, path = None):
        if from_ is not None:
            self.set_initial_pos(from_)
        if to is not None:
            path = self.generate_path(to)
        if self._parent is None:
            print("parent map is not created. Run generate path to calcute parent map.")
            return
        c = 0
        for i in range(1, len(path)):
            c += self._graph[path[i-1]][path[i]]
        return c
    def _make_relation_distance_dic(self):
        from ListDB import ListDB
        dic = {}
        for key in self._relation:
            dic[key] = {}
            for neb in self._relation[key]:
                val = 1
                if self._color_map[self._start] == self._color_map[neb]:
                    val = 0
                dic[key][neb] = val
        return dic
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
class OneToEveryOnePathCostCheck(IOps):
    def set_info(self, infos):
        self._infos = infos
    def path(self):
        func = lambda _f, t, i: Main.hypothesis().distance(f, t, i).path()
        return self._iter(func)
    def _iter(self, func):
        color_info = self._infos['color']
        res = {}
        for color in color_info:
            vals = color_info[color]
            res[color] = {}
            for i in range(len(vals)):
                _from = vals[i]
                for j in range(i+1, len(vals)):
                    to = vals[j]
                    res[color][(_from, to)] = func(_from, to, infos)
        return res
    def cost(self):
        func = lambda _f, t, i: Main.hypothesis().distance(f, t, i).cost()
        return self._iter(func)
    def calc_common_part(self, color):
        paths_color_map = self.path()
        return CommonOfValsList(paths[color].values()).execute()
class CommonOfValsList(IOps):
    def __init__(self, vals: list[list]):
        self._vals = vals
    def execute(self):
        common = None
        for val in self._vals:
            if common is None:
                common = set(val)
            common = set(val).intersection(common)
        return common
class KamiGraphTreeMakerWithColor(IOps):
    def set_initial_pos(self, init_pos):
        self._root = init_pos
        self._node_map = {}
    def set_pickle(self, pkl):
        self._pkl_path = pkl
        qfi = QuestionFromPickle(pkl)
        qus = qfi.get_info()
        self.set_info(qus)
    def execute(self):
        visited = set([])
        stack = [self._root]
        while len(stack) > 0:
            key = stack.pop()
            visited.add(key)
            this_node = self.get_node(key)
            for c in self._color_options:
                if c != self._color_map[key]:
                    children = self._children_node_with_color(c, visited, key)
                    if len(children) > 0:
                        cn = Node(c)
                        this_node.children.append(cn)
                        for child_key in children:
                            node = self.get_node(child_key)
                            cn.children.append(node)
                            stack.insert(0, child_key)
        root_node = self._node_map[self._root]
        MinDepthInverseCalculator(root_node).execute()
        return root_node
    def _children_node_with_color(self,color,  visited, key):
        nebors = self._graph[key]
        res = []
        for neb in nebors:
            if neb not in visited and self._color_map[neb] ==color:
                res.append(neb)
        return res
    def get_color_node(self, key):
        c = self._color_map[key]
        cn = Node(c)
        return cn
    def get_node(self, key):
        if key not in self._node_map:
            n = Node(key)
            self._node_map[key] = n
            n.extra_info.depth = 0
        return self._node_map[key]
    def set_info(self, info):
        from ListDB import ListDB
        ListDB.dicOps().reverseKeyValue(info['color'])
        self._graph = info['relation']
        self._color_map = ListDB.dicOps().reverseKeyValue(info['color'])
        self._color_options = list(info['color'].keys())
class DepthCaculator(IOps):
    def __init__(self, root: Node):
        self._root = root
        self._max_dep = 0
    def execute(self):
        self._assign(self._root)
    def _assign(self, node: Node, depth = 0):
        if depth > self._max_dep:
            self._max_dep = depth
        node.extra_info.depth = depth
        for child_node in node.children:
            self._assign(child_node, depth + 1)
class MaxDepthInverseCalculator(IOps):
    def __init__(self, root: Node):
        self._root = root
    def execute(self):
        self._root.extra_info.depth = self._assign(self._root)
    def _assign(self, node):
        if len(node.children) == 0:
            node.extra_info.depth = 0
            return 0
        depths = []
        for child in node.children:
            child.extra_info.depth = self._assign(child)
            depths.append(child.extra_info.depth)
        return max(depths) + 1
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
            def split_method(colors= None, grid_size = GRID_SIZE):
                vals = Main.nebors_finder(img_path, color_map).split_method(grid_size)
                Temp.only_kami_objs(vals, grid_size, colors)
            def only_kami_objs(vals, grid_size = GRID_SIZE, colors= None):
                kamiObjs = Temp._kami_objects_to_kami_numberable_objects(vals, grid_size, colors)
                nki = NumberKamiImage(img_path)
                nki.set_objects(kamiObjs)
                nki.execute()
                nki.get_img().open_in_program()
            def _kami_objects_to_kami_numberable_objects(vals, grid_size, colors=None):
                if colors is None:
                    colors = list(color_map.keys())
                splitter = ImageSplitterIntoBlocks()
                splitter.set_image(img_path)
                splitter.set_grid(grid_size)
                kamiObjs =[]
                for vla in vals:
                    if vla._color not in colors:
                        continue
                    obj = KamiObjs(vla._id, vla._positions, vla._color)
                    obj.set_color_map(color_map)
                    obj.set_img_splitter(splitter)
                    kamiObjs.append(obj)
                return kamiObjs
            def from_pickle(pkl, ids = None):
                vals = SerializationDB.readPickle(pkl)
                kamiParts = []
                for col in vals['color']:
                    for _id in vals['color'][col]:
                        if ids is None:
                            kamiParts.append(KamiPart(_id, col, vals['positions'][_id]))
                        elif _id in ids:
                            kamiParts.append(KamiPart(_id, col, vals['positions'][_id]))
                Temp.only_kami_objs(kamiParts)
            def save_as_pickle(outfile= None):
                psm = PictureSplitMethod()
                psm.set_image(img_path)
                psm.set_color_bound(color_map)
                psm.set_grid_size(GRID_SIZE)
                eq = ExportQuestion()
                eq.set_serializable(psm)
                if outfile is None:
                    outfile = img_path + '.pkl'
                eq.export(outfile)
        return Temp
    def color_bound_detector(img_path, out_file_name= None):
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
                import os
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
class KamiSolver(ISolver):
    def __init__(self):
        self._problem_data = None
    def set_image(self, img):
        pass
    def set_problem_data(self, data):
        self._problem_data = data
    def solve(self):
        pass
    def set_problem(self, problem: IQuestion):
        self._problem_data = problem.get_info()
        self._problem = problem
class AnalyserGUI(IBox):
    def __init__(self):
        self._lay = self._get_layout()
    def _get_layout(self):
        from WidgetsDB import WidgetsDB
        import ipywidgets as widgets
        from Path import Path
        lay = GenerateNRowsBox(4)
        row1 = lay.get_child(0)
        row1.add_ipywidget(widgets.Label(value = "Current image:: "))
        row1.add_ipywidget(widgets.Dropdown())
        row1.add_ipywidget(WidgetsDB.button('open'))
        row1.add_ipywidget(WidgetsDB.button('number'))
        row2 = lay.get_child(1)
        row2.add_ipywidget(widgets.Label(value = "dirs:: "))
        row2.add_ipywidget(widgets.Dropdown(options= Path.getDir('kami-images')))
        row2.add_ipywidget(WidgetsDB.button('update'))
        return lay
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
        self._lay.get_child(0).add_ipywidget(WidgetsDB.button('display'))
        display_btn = self._lay.get_child(0).get_child(4)
        def display_img(img_path):
            mi = MatplotImage()
            mi.set_image(img_path)
            mi.display()
        display_btn.on_click(lambda x: display_img(self._lay.get_child(0).get_child(1).value))
class NewNode(Node):
    @property
    def value(self):
        return f"{self.idd}-{self.extra_info.color}: d-{self.extra_info.depth}"
class ISolverStrategy:
    def get_steps(self):
        pass
class KamiSolverTreeMethod(ISolverStrategy):
    def set_max_steps(self, max_steps):
        self._max_steps = max_steps
    def _set_initial_pos(self, init_pos):
        self._root = init_pos
        self._node_map = {}
    def set_pickle(self, pkl):
        self._pkl_path = pkl
        qfi = QuestionFromPickle(pkl)
        qus = qfi.get_info()
        self.set_info(qus)
    def get_steps(self, optimize=True):
        if optimize:
            vals = self._optimized()
        else:
            vals = self._graph
        for i in vals:
            print(i)
            self._set_initial_pos(i)
            ndo = self._execute()
            if ndo.extra_info.depth <= self._max_steps:
                break
        steps = []
        st = self._max_steps
        while True:
            st -= 1
            for c in ndo.children:
                if c.extra_info.depth == st:
                    steps.append((ndo.idd, c.extra_info.color))
                    ndo = c
                    break
            if st <= 0:
                break
        return steps
    def _execute(self):
        n = NewNode(self._root)
        n.extra_info.color = self._color_map[n.idd]
        n.extra_info.merged = set([n.idd])
        self._find(n)
        MinDepthInverseCalculator(n).execute()
        return n
    def _optimized(self):
        from ListDB import ListDB
        from modules.Explorer.DictionaryExplorer import Graph2NodeTreeMakerBreadthFirstSearch
        res ={}
        for key in self._graph:
            n = Graph2NodeTreeMakerBreadthFirstSearch(self._graph, key)
            res[key] = n.execute().extra_info.depth
        return ListDB.sortDicBasedOnValue(res)
    def _find(self, node, depth = 0):
        if depth > self._max_steps:
            return
        node.extra_info.depth = depth
        for c in self._color_options:
            if c != node.extra_info.color:
                new_node = NewNode(node.idd)
                merged = [v for v in node.extra_info.merged]
                children = self._get_merged_children(merged)
                for child in children:
                    if c == self._color_map[child]:
                        merged.append(child)
                if len(merged) > len(node.extra_info.merged):
                    new_node.extra_info.merged = set(merged)
                    node.children.append(new_node)
                    new_node.extra_info.color = c
                    self._find(new_node, depth+1)
    def _get_merged_children(self, keys):
        given = set(keys)
        res = []
        for key in keys:
            res += self._graph[key]
        res = set(res)
        return list(res.difference(given))
    def set_info(self, info):
        from ListDB import ListDB
        ListDB.dicOps().reverseKeyValue(info['color'])
        self._graph = info['relation']
        self._color_map = ListDB.dicOps().reverseKeyValue(info['color'])
        self._color_options = list(info['color'].keys())
class MinDepthInverseCalculator(IOps):
    def __init__(self, root: Node):
        self._root = root
    def execute(self):
        self._root.extra_info.depth = self._assign(self._root)
    def _assign(self, node, min_depth =0 ):
        if len(node.children) == 0:
            node.extra_info.depth = 0
            return 0
        depths = []
        for child in node.children:
            child.extra_info.depth = self._assign(child)
            depths.append(child.extra_info.depth)
        return min(depths) + 1
class ExtractImagesFrom6ImageSet(IOps):
    def __init__(self, target_path = "."):
        self._target_path = target_path
    def set_image(self, path):
        self._img = MatplotImage()
        self._img.set_image(path)
    def execute(self):
        folder = self._target_path + os.sep + os.path.basename(self._img._path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        for i in [0,1]:
            for j in [0,1,2]:
                self._save(i,j, folder+ os.sep + f"{i}{j}.png")
    def _save(self, xi,yi, path):
        xl, xh = 221,589
        yl, yh = 39,266
        dy = 70.33
        dx = 235
        width = yh-yl
        height = xh-xl
        shift_y = (dy + width)*yi
        shift_x = (dx + height)*xi
        ly, hy = round(yl + shift_y) ,round(yl + shift_y + width)
        lx, hx = round(xl + shift_x) ,round(xl + shift_x + height)
        MatplotImage(self._img.data[lx:hx, ly:hy]).save(path)
class RemoveLowerPartOfLever(IOps):
    def execute(self):
        MatplotImage(self._img.data[:-144,:]).save(self._img._path)
    def set_image(self, img):
        self._img = MatplotImage()
        self._img.set_image(img)