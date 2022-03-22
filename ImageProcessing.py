import numpy as np
import cv2
import os

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
        from LibPath import getPath
        faces = cv2.CascadeClassifier(os.sep.join([getPath(), "resource","assests", "xmls", "haarcascade_frontalface_alt.xml"]))
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
        from LibPath import getPath
        from Path import Path
        return Path.joinPath(getPath(),"resource", "assests")
    def listICOFiles():
        from Path import Path
        path = ICOPath._path()
        return Path.filesWithExtension("ico", path)
    def getPathForFile(f):
        if(f.endswith(".ico")):
            return ICOPath._path() + os.sep + f
        return ICOPath._path() + os.sep + f + ".ico"