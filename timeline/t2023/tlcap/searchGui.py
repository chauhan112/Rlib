import ipywidgets as widgets
from modules.Explorer.personalizedWidgets import GenerateNRowsBox
from timeline.t2022.TLCAP import Main as FinderKeeper
from useful.TimeDB import TimeDB
from useful.Path import Path
import os

class FilesModel:
    def __init__(self, path):
        self._path = path
        self._files = list(map(lambda x: (os.path.basename(x),x),Path.filesWithExtension("json",self._path)))
class SearView:
    def __init__(self):
        self.gnrb =None
        self.out = None
    def _make_layout(self):
        self.out=widgets.Output()
        self.gnrb = GenerateNRowsBox(1)
        nrb = self.gnrb.get_child(0)
        self.filterWid = widgets.Text(placeholder ="filter", layout={'width':"100px"})
        nrb.add_widget(self.filterWid)
        self.drop = widgets.Dropdown(layout={'width':"auto"})
        nrb.add_widget(self.drop)
        self.searchWid = widgets.Text(layout={'width':"auto"})
        nrb.add_widget(self.searchWid)
        self.wordCheckBox = widgets.Checkbox(indent=False, layout={'width':"auto"}, description= "word")
        nrb.add_widget(self.wordCheckBox)
        self.regCheckbox = widgets.Checkbox(indent=False, layout={'width':"auto"}, description="reg")
        nrb.add_widget(self.regCheckbox)
        self.searchBtn = widgets.Button(description= "search")
        nrb.add_widget(self.searchBtn)
    def display(self):
        if self.gnrb is None:
            self._make_layout()
        from IPython.display import display
        display(widgets.VBox([self.gnrb.get(), self.out]))
class UIController:
    def set_ui(self, ui_model: SearView):
        self._ui = ui_model
    def set_model(self, model: FilesModel):
        self._model = model
    def _on_word_checkbox_selected(self, wid):
        self._ui.regCheckbox.value = self._ui.wordCheckBox.value
    def _find_content(self, wid):
        reg = self._ui.regCheckbox.value
        content = self._ui.searchWid.value
        if self._ui.wordCheckBox.value:
            content = "\\b"+self._ui.searchWid.value+"\\b"
            reg=True
        self._ui.out.clear_output()
        if self._ui.drop.value and self._ui.searchWid.value != "":
            with self._ui.out:
                print(FinderKeeper.getAllHardCodedValues(self._ui.drop.value, content, reg=reg))
    def setup(self):
        self._ui._make_layout()
        self._ui.drop.options = self._model._files
        self._ui.wordCheckBox.observe(self._on_word_checkbox_selected, ["value"])
        self._ui.filterWid.observe(self._on_filtered, ["value"])
        self._ui.searchBtn.on_click(self._find_content)
    def _on_filtered(self, wid):
        self._ui.drop.options = list(filter(lambda x: self._ui.filterWid.value in x[0],self._model._files))



from useful.ExplorerDB import ExplorerDB
from useful.ListDB import ListDB
from useful.FileDatabase import File
import json

class ExpView:
    def __init__(self):
        self.gnrb = None
    def _make_layout(self):
        if self.gnrb is not None:
            return 
        self.gnrb = GenerateNRowsBox(1)
        row = self.gnrb.get_child(0)
        self.filepathWid = widgets.Text(layout={'width':"auto"}, description= "file")
        row.add_widget(self.filepathWid)
        self.locTextWid = widgets.Text(layout={'width':"auto"},  description= "location")
        row.add_widget(self.locTextWid)
        self.searchBtn = widgets.Button(layout={'width':"auto"}, description= "open")
        row.add_widget(self.searchBtn)
        self.storeInVariableBtn = widgets.Button(layout={'width':"auto"}, description= "store")
        row.add_widget(self.storeInVariableBtn)
        self.infoLabel = widgets.Label()
        row.add_widget(self.infoLabel)
    def display(self):
        from IPython.display import display
        display(self.gnrb.get())
    @property
    def layout(self):
        return self.gnrb.get()
class ExpController:
    def set_view(self, view: ExpView):
        self._ui = view
    def _btn_click(self, wid):
        path = self._ui.filepathWid.value.strip()
        loc = self._parseAList(self._ui.locTextWid.value)
        if path != "" and loc is not None:
            data = json.loads(File.getFileContent(path))
            ExplorerDB.dicExplorer(ListDB.dicOps().get(data, loc))
    
    def _on_store_clicked(self, wid):
        from useful.TimeDB import TimeDB
        path = self._ui.filepathWid.value.strip()
        loc = self._parseAList(self._ui.locTextWid.value)
        if path != "" and loc is not None:
            self._space['res'] = ListDB.dicOps().get(json.loads(File.getFileContent(path)), loc)
            self._ui.infoLabel.value ="stored in variable `res`"
        else:
            self._ui.infoLabel.value ="Enter parameters"
        TimeDB.setTimer().oneTimeTimer(5, self._clear_info)
    def _clear_info(self):
        self._ui.infoLabel.value = ""
    def setup(self):
        self._ui._make_layout()
        self._ui.searchBtn.on_click(self._btn_click)
        self._ui.storeInVariableBtn.on_click(self._on_store_clicked)
    def _parseAList(self, stringArr):
        res = {}
        try:
            exec("b="+stringArr, {}, res)
        except:
            return None
        return res["b"]
    def set_space(self, space={}):
        self._space = space
        
class Main:
    def displayContentSearcher(folder = "json"):
        uic = UIController()
        uic.set_model(FilesModel(folder))
        uic.set_ui(SearView())
        uic.setup()
        uic._ui.filterWid.value =TimeDB.getTimeStamp().split(", ")[-1].replace(".", "")
        return uic
    def jsonExplorer(space={}):
        ec = ExpController()
        ec.set_view(ExpView())
        ec.setup()
        ec.set_space(space)
        return ec
