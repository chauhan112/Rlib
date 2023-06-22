import pyautogui as pg
import time
from FileDatabase import File

class Image:
    def set_img_path(self, name: str):
        self._path = name
        self._data = cv2.imread(name,1)
    @property
    def data(self):
        return self._data
    def show(self,img):
        cv2.imshow('showing window',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
class ArrayFromImage:
    def __init__(self):
        self.set_top_left((0, 0))
        self.set_bottom_right((570, 570))
    def set_image(self, img: Image):
        self._img = img
    def set_dimension(self, dim:tuple):
        self._dim = dim
    def set_top_left(self, point: tuple):
        self._p1 = point
    def set_bottom_right(self, point: tuple):
        self._p2 = point
    def getArray(self):
        size = self._dim[0]
        point1 = self._p1
        point2 = self._p2

        gap= (point2[0]-point1[0]) // size
        mid=gap//2
        midPoint=(point1[0]+mid,point1[1]+mid)

        arr=[]
        for i in range(size):
            row=[]
            for j in range(size):
                point = (midPoint[0]+gap*j, midPoint[1]+gap*i)
                b,g,r = (self._img.data[point[1], point[0]])
                row.append((b,g,r))
            arr.append(row)
        return self._getColorCode(arr)

    def _getColorCode(self,arr):
        from itertools import chain
        flatten_list = list(chain.from_iterable(arr))

        for i in range(len(flatten_list)):
            if sum(flatten_list[i]) < 50 or flatten_list.count(flatten_list[i])!=2:
                flatten_list[i]=0
        c=1
        for i in range(len(flatten_list)):
            if type(flatten_list[i])==tuple:
                temp=flatten_list[i]
                flatten_list[i]=c
                pos=flatten_list.index(temp)
                flatten_list[pos]=c
                c+=1
        new_arr=[[0 for i in range(len(arr))] for j in range(len(arr[0]))]
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                new_arr[i][j]=flatten_list[i*len(arr[0])+j]
        return new_arr
        
    def save(self, filename: str):
        if filename.endswith(filename):
            filename += ".txt"
        File.createFile(filename, str(self.getArray()))
class IPosition:
    def get_position(self) -> tuple:
        raise NotImplementedError("abstract method")
    def about(self):
        raise NotImplementedError("abstract method")
class IConfigurable:
    def set_position(self, pos: tuple):
        raise NotImplementedError("abstract method")
class GConfPos(IPosition, IConfigurable):
    def get_position(self):
        return self._pos
    def set_position(self, pos: tuple):
        self._pos = pos
class GoBack(GConfPos):
    def about(self):
        return "position pixel of back method"
class CalculableLevelPos(IPosition):
    def set_level1_box_position(self, box1: IPosition):
        self._b1_pos = box1
    def set_indices(self, pos: tuple):
        self._pos = pos
    def get_position(self):
        i, j = self._pos
        x, y = self._b1_pos.get_position()
        size_of_small_level_square = 82 
        return x + size_of_small_level_square*j, y + size_of_small_level_square*i
class TopLeftPlayArea(GConfPos):
    def about(self):
        return "top left point of play area"
class Level1SmallBoxPosition(GConfPos):
    def about(self):
        return "in level sections, position of first level box"
class CentralRandomPosition(GConfPos):
    def about(self):
        return "random position on the game area screen"
class FlowAutoLevelExtraction:
    def __init__(self):
        self._goback: IPosition  = GoBack()
        self._lvl1pos: IPosition = Level1SmallBoxPosition()
        self._topleft = TopLeftPlayArea()
        self._crp = CentralRandomPosition()
        self._cal_pos = CalculableLevelPos()
        self._cal_pos.set_level1_box_position(self._lvl1pos)

    def scanStoreData(self,nof_pages=5):
        for i in range(1,nof_pages+1):
            self._singlePage(page=i,boardSize=4+i)
            pg.mouseDown(*self._crp.get_position(),button='left')
            pg.moveRel(-200,0,.2)
            pg.mouseUp()
            time.sleep(0.5)

    def _singlePage(self,page,boardSize,row=6,col=5):
        afi = ArrayFromImage()
        img = Image()
        board_dim = (570, 570)
        afi.set_dimension(board_dim)
        for i in range(row):
            for j in range(col):
                self._cal_pos.set_indices((i, j))
                x,y= self._cal_pos.get_position()
                pg.click(x,y,duration=0.5)
                pg.moveTo(*self._goback.get_position(),0.35)
                pg.screenshot('temp.png',region=(*self._topleft.get_position(), *board_dim))
                time.sleep(.3)
                img.set_img_path("temp.png")
                afi.set_image(img)
                afi.save('page'+str(page)+'-game'+str(col*i+j+1))
                pg.click(*self._goback.get_position())

    def readGameData(self,page,game,location=r"C:\Users\19410\My Drive\Raju Dai\current\gameData"):
        name=location+'\\'+'page'+str(page)+'-game'+str(game)+'.txt'
        return eval(File.getFileContent(name))
class Main:
    def extract_array(img_path,top_left, bottom_right, dim = (5,5)):
        afi = ArrayFromImage()
        img = Image()
        img.set_img_path(img_path)
        afi.set_image(img)
        afi.set_top_left(top_left)
        afi.set_bottom_right(bottom_right)
        afi.set_dimension(dim)
        return afi.getArray()
        
    def automate_extraction(goback_pos : tuple,
                            level1_box_position : tuple,
                            random_pos_on_game_area : tuple,
                            top_left_board_area_pos : tuple ):
        fale = FlowAutoLevelExtraction()
        fale._goback.set_position(goback_pos)
        fale._lvl1pos.set_position(level1_box_position)
        fale._crp.set_position(random_pos_on_game_area)
        fale._topleft.set_position(top_left_board_area_pos)
        fale.scanStoreData()