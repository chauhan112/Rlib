DISCOURSE_TYPE = ['Lead', 'Position', 'Evidence', 'Claim', 'Concluding Statement', 'Counterclaim', 'Rebuttal']
import os
from useful.FileDatabase import File

class Range:
    def __init__(self, l, r, discourse_type):
        self.left = l
        self.right = r
        self.dtype = discourse_type

class Project:
    def __init__(self):
        import pandas as pd
        self._train_csv_path = r"D:\TimeLine\2022\kaggle\feedback-prize-2021\train.csv"
        self._project_path = r"D:\TimeLine\2022\kaggle\feedback-prize-2021"
        self._df = pd.read_csv(self._train_csv_path)
    
    def visualizer(self, filename):
        arr = []
        val = self._df[self._df.id == os.path.basename(filename).replace(".txt", "")]
        for i in range(len(val)):
            row = val.iloc[i]
            arr.append(Range(int(row.discourse_start), int(row.discourse_end), row.discourse_type))
        cc = ColorCode()
        cc.set_file_path(filename)
        cc.set_color_map(arr)
        cc.display()
        self._cc = cc

class ColorCode:
    def __init__(self):
        self._res = None
        self._color_map = {'Lead': 'Green',
             'Position': 'RoyalBlue',
             'Evidence': 'PaleVioletRed',
             'Claim': 'SlateGray',
             'Concluding Statement': 'Peru',
             'Counterclaim': 'Pink',
             'Rebuttal': 'Plum'}

    def set_string(self, data: str):
        self._data = data
        
    def set_file_path(self, path: str):
        self._data = File.getFileContent(path)
    
    def _colorize(self):
        if self._res is not None:
            return self._res
        new_data = ""
        ini = 0
        for ran in self._color_codes:
            br = ""
            if ini == 0:
                br = "<br>"
            l, r = ran.left, ran.right
            new_data += self._data[ini:l] + br + ran.dtype +" :" + \
                f"<font color='{self._color_map[ran.dtype]}'>{self._data[l:r] }</font>"
            ini = r
        new_data += self._data[ini:]
        self._res = new_data
        return new_data
    
    def display(self):
        from IPython.display import HTML, display
        display(HTML(self._colorize()))
    
    def set_color_map(self, color_codes: list[Range]):
        self._color_codes = color_codes