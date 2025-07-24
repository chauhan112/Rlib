import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from OpsDB import IOps
import pandas as pd
from ancient.ImageProcessing import IImage
import cv2, os
from Path import Path
from RegexDB import RegexDB, NameDicExp

class IImageReader:
    def get_data(self):
        raise NotImplementedError("implement this func")
    def set_image(self, path: str):
        raise NotImplementedError("implement this func")
    
class PILReader(IImageReader):
    def set_image(self, path):
        self._path = path
    def get_data(self):
        return Image.open(self._path)
class ReaderAndNormalize(IImageReader):
    def __init__(self):
        self._pil_reader = PILReader()
        self._data = None
    def set_image(self, img:str):
        self._pil_reader.set_image(img)
        self._data = None
    def get_data(self):
        image = self._pil_reader.get_data()
        if self._data is None:
            self._data = np.interp(image, [np.min(image), np.max(image)], [0,255])
        return self._data
class PlotNxMImages(IOps):
    def __init__(self):
        self.set_image_reader(PILReader())
        self._images_data = None
        self._titles = None
    def set_images(self, images:list[str]):
        self._images = images
        self._images_data = None
    def _read_data(self):
        self._images_data = []
        for p in self._images:
            self._reader.set_image(p)
            self._images_data.append(self._reader.get_data())
    def set_row_col_dim(self, dim):
        self._dim = dim
    def execute(self):
        if self._images_data is None:
            self._read_data()
        if self._titles is None:
            self.set_titles(['']* len(self._images_data))
        x, y = self._dim
        total = x*y
        if total > len(self._images_data):
            total = len(self._images_data)
        plt.subplots(figsize=(15,15))
        for i in range(total):
            image = self._images_data[i]
            plt.subplot(x,y, i + 1)
            plt.title(self._titles[i])
            plt.imshow(image)
        plt.show()
    def set_images_data(self, images_data: list[np.ndarray]):
        self._images_data = images_data
    def set_titles(self, titles: list):
        self._titles = titles
    def set_image_reader(self, reader: IImageReader):
        self._reader = reader
class KaggleProject:
    def __init__(self):
        from modules.Explorer.ZipFileExplorerDisplayer import NewZipFileExplorer
        self._csv_op = CSVOps()
        self._explorer = NewZipFileExplorer(r"D:\TimeLine\ai\uw-madison-gi-tract-image-segmentation.zip")
    def set_file_path(self, path):
        self._path = path
    @property
    def csv_files(self):
        return Path.filesWithExtension("csv", self._path)
    @property
    def png_files(self):
        return Path.filesWithExtension("png", self._path)
    def csv_ops(self, csv:str):
        self._csv_op.set_csv(csv)
        return self._csv_op
    @property
    def explorer(self):
        return self._explorer.display()
class ImagesOperations:
    def set_images(self, images: list):
        self._images = images
    def nxm_plotter(self):
        pass
class CSVOps:
    def set_csv(self, csv_path:str):
        self._path = csv_path
        self.pd = pd.read_csv(self._path)
class RLEDecoder(IOps):
    def __init__(self):
        self.set_color(1)
    def set_color(self, color):
        self._color = color
    def set_mask_rle(self, mask: str):
        self._mask_rle = mask
    def set_shape(self, shape: tuple):
        self._shape = shape
    def execute(self):
        color = self._color
        s = np.array(self._mask_rle.split(), dtype=int)
        starts = s[0::2] - 1
        lengths = s[1::2]
        ends = starts + lengths
        if len(self._shape)==3:
            h, w, d = self._shape
            img = np.zeros((h * w, d), dtype=np.float32)
        else:
            h, w = self._shape
            img = np.zeros((h * w,), dtype=np.float32)
        for lo, hi in zip(starts, ends):
            img[lo : hi] = color
        return img.reshape(self._shape)
class NormalizedImage(IImage):
    def __init__(self):
        self._size = None
    def set_image(self, img):
        ran = ReaderAndNormalize()
        ran.set_image(img)
        self.data = ran.get_data()
    def save(self, name):
        if not name.endswith(".png"):
            name += ".png"
        cv2.imwrite(name, self.data)
    def display(self):
        import matplotlib.pyplot as plt
        if self._size is not None:
            plt.figure(figsize=self._size)
        plt.imshow(self.data)
        plt.show()
    def set_size(self, size:tuple):
        self._size = size
class NormalizedImageRGB(NormalizedImage):
    def set_image(self, img: str):
        self._path = img
        _img = np.tile(np.expand_dims(cv2.imread(self._path, cv2.IMREAD_ANYDEPTH)/65535., axis=-1), 3)
        _img = ((_img-_img.min())/(_img.max()-_img.min())).astype(np.float32)
        self.data = _img
class ImageWithRLEEncoder(IImage):
    def __init__(self):
        self._vals = {}
        self._rle_decoder = RLEDecoder()
        self.set_size(None)
    def add_encode(self, values, legend = None):
        if pd.isna(values):
            self._vals[legend] = np.zeros((self.data.shape[:2]))
            return
        self._rle_decoder.set_mask_rle(values)
        self._rle_decoder.set_shape(self.data.shape[:2])
        img = self._rle_decoder.execute()
        self._vals[legend] = img
    def display(self):
        seg_overlay = self.compute_overlays()
        if self._size is not None:
            plt.figure(figsize=self._size)
        plt.imshow(seg_overlay)
        plt.axis(False)
        plt.show()

    def compute_overlays(self):
        arr = [self._vals[i] for i in ['large_bowel', "small_bowel", "stomach"]]
        _seg_rgb = np.stack(arr, axis=-1).astype(np.float32)
        seg_overlay = cv2.addWeighted(src1=self.data, alpha=0.99, src2=_seg_rgb, beta=0.33, gamma=0.0)
        return seg_overlay

    def set_image(self, img: str):
        self._path= img
        self._img_mdoel = NormalizedImageRGB()
        self._img_mdoel.set_image(self._path)
        self.data = self._img_mdoel.data
        self._vals = {}
    def set_size(self, fig_size: tuple):
        self._size = fig_size
    def save(self, filename):
        self.display()
        plt.savefig(filename)
class CaseAndSliceInfoFromPath(IOps):
    def set_path(self, path):
        self._path = path
    def execute(self):
        gres = NameDicExp(".*", "case", "case\d+_day\d+", NameDicExp('.+', "slice", "slice_\d+", ".*"))
        return RegexDB.group_name_search(gres, self._path)
class AnnotatedImage(IImage):
    def set_dataframe(self, data: pd.DataFrame):
        self._df = data
        self._casifp = CaseAndSliceInfoFromPath()
        
    def set_image(self, img: str):
        self._img_path = img
        self._iwre = ImageWithRLEEncoder()
        self._iwre.set_image(self._img_path)
        
        self._casifp.set_path(self._img_path)
        self._info = self._casifp.execute()
        if len(self._info) == 0:
            raise IOError("Missing information of case and slice")

    def display(self):
        self._add_overlays()
        self._iwre.display()
    def _add_overlays(self):
        vals =self._df[self._df.id == '_'.join(self._info.values())]
        for i in range(len(vals)):
            row = vals.iloc[i]
            self._iwre.add_encode(row.segmentation, row['class'])
    def save(self, filename):
        self._add_overlays()
        img = NormalizedImage()
        img.data = self._iwre.compute_overlays() * 255
        img.data = img.data[:,:,::-1]
        img.save(filename)
class MakeAnimationForCase(IOps):
    def __init__(self):
        self.set_out_folder(".animation-images")
    def set_case(self, case_id:str):
        self._case_id = case_id
    def set_out_folder(self, folder):
        self._out_folder = folder
    def execute(self):
        from WidgetsDB import WidgetsDB
        out_path = os.sep.join([self._out_folder, self._case_id])
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        from ancient.ImageProcessing import MakeAnimation
        cases = list(filter(lambda x: self._case_id in x, self._kp.png_files))
        progressBar = WidgetsDB.progressBar(len(cases))
        for i, f in enumerate(cases):
            ai = AnnotatedImage()
            ai.set_dataframe(self._data)
            ai.set_image(f)
            ai.save(f"{out_path}/{i}.png")
            progressBar.value = i
        ma = MakeAnimation()
        ma.set_images(sorted(Path.filesWithExtension("png", out_path),
                             key=lambda x: int(os.path.basename(x).replace(".png", ""))))
        ma.set_duration_between_frames(.1)
        ma.set_output_filename(os.sep.join([self._out_folder, self._case_id]))
        ma.execute()
        progressBar.value = i + 1
    def set_project_path(self, path):
        self._kp = KaggleProject()
        self._kp.set_file_path(path)
        self._data = self._kp.csv_ops(self._kp.csv_files[1]).pd

class IAnimation:
    def save(self, filename):
        pass
    def display(self):
        pass
    def set_duration_between_frames(self, interval):
        pass
    def set_fps(self, fps: int):
        pass

class GAnimationFromImages(IAnimation):
    def _set_output_file(self, name:str):
        if not name.endswith(".gif"):
            name += '.gif'
        self._outfile = name
    def set_images(self, images):
        self._images= images

    def set_duration_between_frames(self, interval: float):
        self.set_fps(int(1 / interval))

    def set_fps(self, fps: int):
        self._fps = fps

class AnimationMakerFromImageReader(GAnimationFromImages):
    def __init__(self):
        self._images_data = None
        self.set_fps(12)
        self._anim = None
    def set_image_reader(self, reader: IImageReader):
        self._reader = reader
    def _read_data(self):
        self._images_data = []
        for pah in self._images:
            self._reader.set_image(pah)
            self._images_data.append(self._reader.get_data())
        self._images_data = np.stack(self._images_data)
    def _animate(self, save_to =None):
        from matplotlib import animation, rc
        import matplotlib.pyplot as plt
        rc('animation', html='jshtml')
        if self._images_data is None:
            self._read_data()
        fig = plt.figure(figsize=(8,8))
        plt.axis('off')
        im = plt.imshow(self._images_data[0])
        plt.title(f"Animation of images", fontweight="bold")

        def animate_func(i):
            im.set_array(self._images_data[i])
            return [im]
        plt.close()
        self._anim = animation.FuncAnimation(fig, animate_func, frames = self._images_data.shape[0], interval = 1000//self._fps)
        return self._anim
    def display(self):
        if self._anim is not None:
            return self._anim
        return self._animate()
    def save(self, out_path: str):
        if not out_path.endswith(".gif"):
            out_path += ".gif"
        anim = self.display()
        anim.save(out_path, fps=10, writer='imagemagick')

class Main:
    def nxm_plot(images, dim, display= False):
        pnmi = PlotNxMImages()
        pnmi.set_images(images)
        pnmi.set_row_col_dim(dim)
        pnmi.set_image_reader(ReaderAndNormalize())
        if display:
            pnmi.execute()
        return pnmi

    def annoted_image(img_path, data: pd.DataFrame):
        ai = AnnotatedImage()
        ai.set_dataframe(data)
        ai.set_image(img_path)
        ai.display()
        return ai

    def make_animation(case_id, project_path):
        mafc = MakeAnimationForCase()
        mafc.set_case(case_id)
        mafc.set_project_path(project_path)
        mafc.execute()
        return mafc
    def animation_for_images(images: list, displayIt= True):
        amfir = AnimationMakerFromImageReader()
        amfir.set_image_reader(ReaderAndNormalize())
        amfir.set_images(images)
        if displayIt:
            display(amfir.display())
        return amfir
