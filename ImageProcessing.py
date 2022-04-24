import numpy as np
import cv2
import os
from SerializationDB import SerializationDB
from OpsDB import IOps
from LibPath import *
class ImageProcessing:
    def showImgFromFile(imgPath):
        from PIL import Image
        return Image.open(imgPath)
    def image2text(imagePath):
        from LibsDB import LibsDB
        import pytesseract
        tesseractPath = LibsDB.cloudPath() + r"\global\code\libs\Tesseract-OCR\tesseract.exe"
        pytesseract.pytesseract.tesseract_cmd = tesseractPath
        return pytesseract.image_to_string(imagePath)
    def images2pdf(images, name):
        import img2pdf
        if(not name.endswith(".pdf")):
            name += ".pdf"
        with open(name, "wb") as f:
            f.write(img2pdf.convert(images))
    def selectColorHSV(image_path, imgTyp = "PIL"):
        print("Enter ESC to quit")
        def nothing(x):
            pass
        img = ImageProcessing.getCV2Image(image_path, imgTyp)
        cv2.namedWindow('marking')
        cv2.createTrackbar('H Lower','marking',0,255,nothing)
        cv2.createTrackbar('H Higher','marking',255,255,nothing)
        cv2.createTrackbar('S Lower','marking',0,255,nothing)
        cv2.createTrackbar('S Higher','marking',255,255,nothing)
        cv2.createTrackbar('V Lower','marking',0,255,nothing)
        cv2.createTrackbar('V Higher','marking',255,255,nothing)
        while(True):
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            hL = cv2.getTrackbarPos('H Lower','marking')
            hH = cv2.getTrackbarPos('H Higher','marking')
            sL = cv2.getTrackbarPos('S Lower','marking')
            sH = cv2.getTrackbarPos('S Higher','marking')
            vL = cv2.getTrackbarPos('V Lower','marking')
            vH = cv2.getTrackbarPos('V Higher','marking')
            LowerRegion = np.array([hL,sL,vL],np.uint8)
            upperRegion = np.array([hH,sH,vH],np.uint8)
            redObject = cv2.inRange(hsv,LowerRegion,upperRegion)
            kernal = np.ones((1,1),"uint8")
            red = cv2.morphologyEx(redObject,cv2.MORPH_OPEN,kernal)
            red = cv2.dilate(red,kernal,iterations=1)
            res1=cv2.bitwise_and(img, img, mask = red)
            cv2.imshow("Masking ",res1)
            k = cv2.waitKey(200) & 0xFF # large wait time to remove freezing
            if k == 113 or k == 27:
                cv2.destroyAllWindows()
                break
        return np.array([hL, sL, vL]), np.array([hH, sH, vH])
    def pilImage2CVImage(imgC):
        open_cv_image = np.array(imgC)
        img = open_cv_image[:, :, ::-1].copy()
        return img
    def getCV2Image(img, imgTyp = 'PIL'):
        from ClipboardDB import ClipboardDB
        if(type(img) == str ):
            if(img != ''):
                frame = cv2.imread(img)
            else:
                imgC = ClipboardDB.getImage()
                frame = ImageProcessing.pilImage2CVImage(imgC)
        else:
            if(imgTyp == "PIL"):
                frame = ImageProcessing.pilImage2CVImage(img)
            else:
                frame = img
        return frame
    def fitImage2Screen(filename = None, cv2Img = None):
        if(filename is None and cv2Img is None):
            return
        import cv2
        import ctypes
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        W,H = screensize
        if(filename is not None):
            oriimg = cv2.imread(filename)
        else:
            oriimg = cv2Img
        height, width, depth = oriimg.shape
        if(height < H and width < W):
            return oriimg
        scaleWidth = float(W)/float(width)
        scaleHeight = float(H)/float(height)
        if scaleHeight>scaleWidth:
            imgScale = scaleWidth
        else:
            imgScale = scaleHeight
        newX,newY = oriimg.shape[1]*imgScale, oriimg.shape[0]*imgScale
        newimg = cv2.resize(oriimg,(int(newX),int(newY)))
        return newimg
    def detectFace(path = ""):
        import cv2, os
        from ClipboardDB import ClipboardDB
        faces = cv2.CascadeClassifier(os.sep.join([resourcePath(),"assests", "xmls", "haarcascade_frontalface_alt.xml"]))
        if(path == ""):
            img = ClipboardDB.getImage()
        else:
            img = cv2.imread(path)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detections = faces.detectMultiScale(gray_img, scaleFactor = 1.1, minNeighbors = 6)
        for (x,y,w,h) in detections:
            cv2.rectangle(img, (x,y), (x+w, h+y), (0, 255, 0), 2)
        cv2.imshow("detected face", ImageProcessing.fitImage2Screen(cv2Img = img))
        cv2.waitKey(0)
    def rescale(img, percent= 0.5):
        from PIL import Image
        basewidth = int(img.size[0] * percent)
        hsize = int(img.size[1] * percent)
        return img.resize((basewidth,hsize), Image.ANTIALIAS)
    def wordCloud(content, getObj = False):
        from IPython.display import SVG, display
        from wordcloud import WordCloud
        wordcloud = WordCloud(background_color="white").generate(content)
        class Temp:
            def svg():
                class svgtme:
                    def __init__(self, wordcloud):
                        self.svg = wordcloud.to_svg()
                    def display(self):
                        return SVG(self.svg)
                    def save(self, name):
                        File.createFile(name, self.svg())
                s = svgtme(wordcloud)
                display(s.display())
                return s
            def photoDisplay():
                return wordcloud.to_image()
            def arr():
                return wordcloud.to_array()
        return Temp
class Contour:
    def getAllContours( img = '' ,hsvBoundLimits = None,  contourLimitSize = 300, imgTyp= "PIL" ):
        img = ImageProcessing.getCV2Image(img)
        if(hsvBoundLimits is None):
            hsvBoundLimits = ImageProcessing.selectColorHSV(img, "CV2")
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        for l_b, u_b in [hsvBoundLimits]:
            mask = cv2.inRange(hsv, np.array(l_b), np.array(u_b))
            kernal = np.ones((2,2), np.uint8)
            mask = cv2.erode(mask, kernal, iterations=1)
            ret, thresh = cv2.threshold(mask, 20, 255, 0)
            cont, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        return cont
    def filterContourWithArea(conts, min_area):
        contours = []
        for c in conts:
            if(cv2.contourArea(c) > min_area):
                contours.append(c)
        return contours
    def drawContours( img , contours , contourNr , imgTyp = 'PIL'):
        img_data = ImageProcessing.getCV2Image(img, imgTyp)
        cv2.drawContours(img_data, contours, contourNr, (0, 255, 0), 1)
    #     plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        Contour.showImages({str(contourNr): img_data})
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return img_data
    def showImages( imgs ):
        for title in imgs:
            cv2.namedWindow(title, cv2.WINDOW_NORMAL)
            cv2.imshow(title,imgs[title])
class ShowImage:
    def displayDCMImage(filename):
        import matplotlib.pyplot as plt
        import pydicom
        dataset = pydicom.dcmread(filename)
        import os
        # Normal mode:
        print()
        print("Filename.........:", os.path.basename(filename))
        print()
        pat_name = dataset.PatientName
        display_name = pat_name.family_name + ", " + pat_name.given_name
        print("Patient's name...:", display_name)
        print("Patient id.......:", dataset.PatientID)
        print("Modality.........:", dataset.Modality)
        if 'PixelData' in dataset:
            rows = int(dataset.Rows)
            cols = int(dataset.Columns)
            print("Image size.......: {rows:d} x {cols:d}, {size:d} bytes".format(
                rows=rows, cols=cols, size=len(dataset.PixelData)))
            if 'PixelSpacing' in dataset:
                print("Pixel spacing....:", dataset.PixelSpacing)
        # use .get() if not sure the item exists, and want a default value if missing
        print("Slice location...:", dataset.get('SliceLocation', "(missing)"))
        # plot the image using matplotlib
        plt.imshow(dataset.pixel_array, cmap=plt.cm.bone)
        plt.show()
    def gif(path):
        from PIL import Image
        import base64
        class GIF:
            def __init__(self, path):
                self.path = path
            def frames(self):
                im = Image.open(self.path)
                frames = [im]
                try:
                    while 1:
                        im.seek(im.tell()+1)
                        frames.append(im)
                except EOFError:
                    pass
                return frames
            def animate(self):
                from IPython import display
                with open(self.path, 'rb') as fd:
                    b64 = base64.b64encode(fd.read()).decode('ascii')
                return display.HTML(f'<img src="data:image/gif;base64,{b64}" />')
        return GIF(path)
class ICOPath:
    def _path():
        from Path import Path
        return Path.joinPath(resourcePath(), "assests")
    def listICOFiles():
        from Path import Path
        path = ICOPath._path()
        return Path.filesWithExtension("ico", path)
    def getPathForFile(f):
        if(f.endswith(".ico")):
            return ICOPath._path() + os.sep + f
        return ICOPath._path() + os.sep + f + ".ico"
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
        bounds = {}
        while True:
            value = ImageProcessing.selectColorHSV(self._img)
            name = input("name color: ")
            bounds[name] = value
            if input("Are there more colors (y/n)?").strip().lower() != "y":
                break
        self._bounds = bounds
        return self._bounds
class ImageRequiring:
    def set_image(self, img_path: str):
        self._img_path = img_path
class HSVMasking:
    def set_mask(self, lower, upper):
        import numpy as np
        self._lower = np.array(lower)
        self._upper = np.array(upper)
class ApplyMask(IOps, ImageRequiring, HSVMasking):
    def execute(self):
        import numpy as np
        img = cv2.imread(self._img_path)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        redObject = cv2.inRange(hsv,self._lower,self._upper)
        kernal = np.ones((1,1),"uint8")
        red = cv2.morphologyEx(redObject,cv2.MORPH_OPEN,kernal)
        red = cv2.dilate(red,kernal,iterations=1)
        res1=cv2.bitwise_and(img, img, mask = red)
        return CVImage(res1)
class ReplacePartOfImage(IOps, ImageRequiring, HSVMasking):
    def execute(self):
        img = cv2.imread( self._img_path )
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self._lower, self._upper)
        bak = img.copy()
        bak[mask > 0] = self._color
        return CVImage(bak)
    def set_replacing_color(self, target_color:tuple):
        self._color = target_color
class MakeAnimation(IOps):
    def __init__(self):
        self.set_output_filename("movie.gif")
    def set_images(self, images):
        self._images = images
    def execute(self):
        import imageio
        images = []
        for filename in self._images:
            images.append(imageio.imread(filename))
        imageio.mimsave(self._output_name, images, duration=self._duration)
    def set_duration_between_frames(self, duration):
        self._duration = duration
    def set_output_filename(self, name):
        self._output_name = name