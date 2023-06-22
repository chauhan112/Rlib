import ipywidgets as widgets
from PickleCRUDDB import PickleCRUD
from IPython.display import display
import os
class Model:
    def set_file(self, pklFile):
        self._crud = PickleCRUD(pklFile, loadFromMain=False)
class View:
    def __init__(self):
        self._filePathWid = widgets.Text(placeholder ="file (creates if it does not exists")
        self._keyWid = widgets.Select(options=[".", ".."],rows=5 )
        self._opsWid = widgets.Select( options=["Read", "Create", "Update", "Delete"],layout={"width":"auto"}, rows=5)
        self._perfromBtn = widgets.Button(layout={"width":"auto"},description="perform")
        self._goInBtn = widgets.Button(layout={"width":"auto"},description="stepIn")
        self._fileLoadBtn = widgets.Button(layout={"width":"auto"},description="load")
        self._out = widgets.Output()
        self._layout = widgets.VBox([widgets.HBox([self._filePathWid, self._fileLoadBtn]) ,
                                     widgets.HBox([self._keyWid, self._opsWid, self._perfromBtn,self._goInBtn]), self._out])
    @property
    def layout(self):
        return self._layout
class PickleController:
    def __init__(self):
        self.setUpCreateView()
        self.setUpDeleteConfirm()
        self._updating = True
    def set_scope(self, scope):
        self._scope = scope
    def set_view(self, view):
        self._view = view
        self._view._perfromBtn.on_click(self._perform_ops)
        self._view._fileLoadBtn.on_click(self._load_content)
        self._view._goInBtn.on_click(self._step_in)
    def _step_in(self, btn):
        key = self._view._keyWid.value.strip()
        if key not in [".",".."]:
            content = self._model._crud.read(key)
            if type(content) == dict:
                self._model._crud.set_location(self._model._crud.loc +[key])
                self.update()
        elif key == "..":
            if len(self._model._crud.loc) != 0:
                self._model._crud.loc.pop()
                self.update()

    def _load_content(self, btn):
        self._fileChecker()
        self.update()
    def set_model(self, model):
        self._model = model
    def update(self):
        self._view._keyWid.options  = [".", ".."] + list(self._model._crud.getContent().keys())
    def _perform_ops(self, btn):
        self._view._out.clear_output()
        with self._view._out:
            if self._view._opsWid.value == "Create":
                self._updating = False
                display(self._cv.layout)
            elif self._view._opsWid.value == "Read":
                key = self._view._keyWid.value.strip()
                if key not in [".",".."]:
                    print(self._model._crud.read(key))
                elif key == "..":
                    print("going back")
            elif self._view._opsWid.value == "Update":
                self._updating = True
                display(self._cv.layout)
            elif self._view._opsWid.value == "Delete":
                key = self._view._keyWid.value.strip()
                if key not in [".",".."]:
                    display(self._deleteConfirmWid)
    def _fileChecker(self):
        val = self._view._filePathWid.value.strip()
        if val != "":
            dirpath = os.path.dirname(val)
            if dirpath != "" and not os.path.exists(dirpath):
                os.makedirs(dirpath)
            self._filePath = val
            if not self._filePath.endswith(".pkl"):
                self._filePath += ".pkl"
        else:
            self._filePath = "pickleCrud.pkl"
        self._model.set_file(self._filePath)
    def _creating(self, btn):
        key = self._cv._keyToCreate.value.strip()
        value = self._cv._valueToCreate.value.strip()
        if self._cv._isVar.value:
            value = self._scope[value]
        try:
            self._model._crud.read(key)
            if self._updating:
                self._model._crud.add(key, value, overwrite=True)
                self.update()
        except Exception as e:
            print(e)
            self._model._crud.add(key, value)
            self.update()

    def _deleting(self, btn):
        key = self._view._keyWid.value.strip()
        if key not in [".",".."]:
            self._model._crud.delete(key)
            self.update()
            self._view._out.clear_output()
    def setUpDeleteConfirm(self):
        self._deleteConfirmWid = widgets.Button(description="confirm")
        self._deleteConfirmWid.on_click(self._deleting)
    def setUpCreateView(self):
        self._cv = CreateView()
        self._cv._createBtn.on_click(self._creating)
class CreateView:
    def __init__(self):
        self._keyToCreate = widgets.Text(placeholder="key")
        self._valueToCreate = widgets.Text(placeholder="value")
        self._isVar = widgets.Checkbox(description="is var", indent=False, layout={'width':"auto"})
        self._createBtn = widgets.Button(layout={"width":"auto"},description="create")
        self._errorInfo = widgets.Output()
        self._layout = widgets.VBox([widgets.HBox([self._keyToCreate,self._valueToCreate, self._isVar, self._createBtn]), self._errorInfo])
    @property
    def layout(self):
        return self._layout
class Main:
    def pickleCrudGui(displayIt=True):
        pc = PickleController()
        model = Model()
        pc.set_model(model)
        view = View()
        pc.set_view(view)
        if displayIt:
            display(pc._view.layout)
        return pc
