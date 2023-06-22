import cv2
import numpy as np
class IResizer:
    def resize(self, data: list[list]):
        pass
class RescaleWithFactor(IResizer):
    def set_scale(self, scale: float):
        self._scale = scale
    def resize(self, frame: np.ndarray):
        scale = self._scale
        width = int(frame.shape[1] * scale)
        height = int(frame.shape[0] * scale)
        dimensions = (width,height)
        return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)
class FitToScreen(IResizer):
    def resize(self, img:np.ndarray):
        from win32api import GetSystemMetrics
        screen_w, screen_h = GetSystemMetrics(0), GetSystemMetrics(1)
        h,w,channel_nbr = img.shape
        # img get w of screen and adapt h
        h = h * (screen_w / w)
        w = screen_w
        if h > screen_h: #if img h still too big
            # img get h of screen and adapt w
            w = w * (screen_h / h)
            h = screen_h
        w, h = w*0.9, h*0.9 # because you don't want it to be that big, right ?
        w, h = int(w), int(h) # you need int for the cv2.resize
        return cv2.resize(img, (w, h))
class NoResizer(IResizer):
    def resize(self, frame):
        return frame
class GCVFrame:
    def set_title(self, title: str):
        self._title = title
    def set_resizer(self, resizer: IResizer):
        self._resizer = resizer
class CVImage(GCVFrame):
    def __init__(self):
        self.set_title("image")
        self.set_resizer(NoResizer())
    def set_file(self, file:str):
        self._path = file
        self._data = img = cv2.imread(self._path)
    def display(self):
        cv2.imshow(self._title, self._resizer.resize(self._data))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
class CVVideo(GCVFrame):
    def __init__(self):
        self.set_title("video")
        self.set_resizer(NoResizer())
    def set_file(self, video_path: str):
        self._path = video_path
    def display(self):
        capture = cv2.VideoCapture(self._path)
        while True:
            isTrue, frame = capture.read()
            if isTrue:    
                cv2.imshow(self._title, self._resizer.resize(frame))
                key=cv2.waitKey(200) & 0xFF
                if key == 27:
                    break
            else:
                break

        capture.release()
        cv2.destroyAllWindows()
class Main:
    def image_display(path, displayit = True):
        img = CVImage()
        img.set_file(path)
        if displayit:
            img.display()
        return img
    def video_display(path, displayit=True):
        video_player = CVVideo()
        video_player.set_file(path)
        if displayit:
            video_player.display()
        return video_player