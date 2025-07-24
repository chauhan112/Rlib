import ipywidgets as widgets
from useful.WidgetsDB import WidgetsDB
from useful.ListDB import ListDB
from modules.GUIs.model import KeyManager
from useful.SerializationDB import SerializationDB

class OpsWid:
    def __init__(self):
        self._ok = widgets.Button(description="ok", layout={'width':"70px"})
        self._confirm = widgets.Button(description="confirm",layout={'width' :"70px"})
        self._key = widgets.Text(placeholder="key", layout={"width":"20%"})
        self._value = widgets.Text(placeholder="value or variable", layout={"width":"30%"})
        self._isVar = widgets.Checkbox(description="var",indent=False, layout={'width':"auto"})
        self._override = widgets.Checkbox(description="overwrite",indent=False, layout={'width':"auto"})
        self._newKeyName =widgets.Text(placeholder="new key name", layout={'width':"auto"})
        self._opsOption = widgets.Dropdown(options=[], layout =widgets.Layout(width="20%"))
        self._opsContentArea = widgets.HBox([])
        self._mode = widgets.Checkbox(description="ops",indent=False,layout= widgets.Layout(width="20%"))
    
class PickleOpsWidget:
    def __init__(self, path = None, displayIt = True):
        print("pickle ops")
        self._declarewidgets()
        if(path is not None):
            self.set_file(path)
        self.mainLayout = self._createMainLayout()
        if displayIt:
            display(self.mainLayout)
    def set_file(self, file):
        self._filesList = widgets.Text(disabled=True, value=file, layout= {"width":"50%"})
    def _declarewidgets(self):
        box_layout = widgets.Layout(display='flex',flex_flow='row', align_items='stretch') 
        self._bn = widgets.HBox([widgets.Button(description =str(i+1),layout={"width": "auto"}) for i in range(5)])
        self._pageLeft = widgets.Label("...")
        self._pageMax = widgets.Label("pMax")
        self._pageRight = widgets.Label("...")
        self._pageTxt = widgets.BoundedIntText( min=1, max=2,layout ={"width":"80px"} )
        self._gotoPage = widgets.Button(description="go", layout={"width":"auto"})
        self._pager = widgets.HBox([self._pageLeft, self._bn ,self._pageRight,self._pageMax, 
                                    self._pageTxt, self._gotoPage], layout=box_layout)
        self._keysSection = WidgetsDB.getGrid(5, displayIt= False)
        self._pager.layout.visibility = "hidden" # visible
        self._keysSect = widgets.VBox([self._keysSection.mainLayout, self._pager])
        self._path  = widgets.Text(value="/",disabled= True, layout=widgets.Layout(width="50%",))
        self._lastKey = widgets.Text(value="",disabled= True, layout=widgets.Layout(width="10%",))
        self._gobackPath = widgets.Button(icon="fa-arrow-circle-left", layout={"width":"auto"})
        self._filesList = widgets.Dropdown(options=[], layout=widgets.Layout(width ="50%"))
        self.opsSec = OpsWid()
        self._opsrow = widgets.HBox([widgets.Label("ops:", layout={"width":"30px"}), self.opsSec._opsOption,
                                     self.opsSec._opsContentArea], justify_content='space-between')
        self._opsrow.layout.display = "none" # "flex"
        self.output = WidgetsDB.outArea(False)
        
        
    def _createMainLayout(self):
        return widgets.HBox([widgets.Box([widgets.Box([widgets.Label("File:", layout=widgets.Layout(width ="30px")), 
                                         self._filesList, self.opsSec._mode]),
                 widgets.Box([widgets.Label("Loc:", layout=widgets.Layout(width ="30px")),self._path,
                              self._lastKey,self._gobackPath]),
                 widgets.Box([widgets.Label("keys:", layout=widgets.Layout(width ="30px")),self._keysSect]),
                 self._opsrow] , layout=widgets.Layout(  display='flex',  flex_flow='column',  
                                                       border='solid 2px BurlyWood', align_items='stretch', width="100%", min_height="200px", padding="3px"
            )), self.output.out])

class PickleExpController:
    def __init__(self, file = None, displayIt = True):
        from useful.jupyterDB import jupyterDB
        self._options = jupyterDB.pickle().listDir()
        self.set_view(PickleOpsWidget(file, displayIt=displayIt))
        self.set_model(PickleOpsModel())
        self.maxNumberOfKeysPerPage = 20
        self._setCallbacks()
        self.setDefaults()
        
        if(file is None):
            self.view._filesList.options = self._options
            self.view._filesList.observe(self.readFile, names="value")
        else:
            self.model.loadFile(file)
            self.updateGUI()
        self.opsCont = PickleOpsController(self)
    def set_view(self, view):
        self.view = view
    def set_model(self, model):
        self.model = model
    def set_file(self, pklfile):
        self.model.loadFile(pklfile)
        self.updateGUI()
    def set_dic_data(self, data: dict):
        pass
    def setDefaults(self):
        self.keyManager = None
        for i in range(self.maxNumberOfKeysPerPage):
            button = WidgetsDB.button("none", self.keyClicked)
            button.layout.display = "none"
            self.view._keysSection.append(button)
            
    def keyClicked(self, button):
        value = button.description
        self.model.goForward(value)
        self.opsCont.view._key.value = value
        self.sync()
        
    def sync(self):
        if(self.model.isDic()):
            self.keyManager = KeyManager(self.model.getKeys())
            self.updateGUI()
        else:
            self.view.output.clear()
            self.view._lastKey.value = self.model._loc[-1]
            content = self.model.value() 
            with self.view.output.out:
                if(type(content) == str):
                    print(content)
                else:
                    display(content)
            self.model.goback()
        self.view._path.value = "/".join(self.model._loc)
        
    def _setCallbacks(self):
        for ch in self.view._bn.children:
            ch.on_click(self.pageNrSelected)
        self.view._gotoPage.on_click(lambda x: self.jump2Page(int(self.view._pageTxt.value)))
        self.view._gobackPath.on_click(self.goback)
    def goback(self, btn):
        self.model.goback()
        self.view._lastKey.value=""
        self.sync()
        
    def pageNrSelected(self, btn):
        self.jump2Page(int(btn.description))
        
    def jump2Page(self, n):
        for ch in self.view._bn.children:
            ch.style.button_color = None
        self.keyManager.setCurrentPageIndex(n)
        self.makePagerButtons(n)
        self.showKeyButtons()
    
    def readFile(self,selectWid):
        self.model.loadFileFromDB(selectWid['new'])
        self.updateGUI()
    
    def updateGUI(self):
        self.view._path.value = "/".join(self.model._loc)
        self.keyManager = KeyManager(self.model.getKeys())
        if(self.keyManager.totalNrOfPages() < 2):
            self.view._pager.layout.visibility = "hidden"
        else:
            self.view._pager.layout.visibility = "visible"
            self.makePagerButtons(1)
            self.view._pageMax.value = str(self.keyManager.totalNrOfPages())
            self.view._pageTxt.max = self.keyManager.totalNrOfPages()
        self.showKeyButtons()
        
    def makePagerButtons(self, initVal):
        vals = self.keyManager.getButtonIndices()
        i = 0
        for ch in self.view._bn.children:
            if(i < len(vals)):
                ch.description = str(vals[i])
                ch.layout.display = None
                if(initVal == vals[i]):
                    ch.style.button_color = "lightblue"
                else:
                    ch.style.button_color = None
            else:
                ch.layout.display = "none"
            i += 1    
        
    def showKeyButtons(self):
        keyList = self.keyManager.getKeysForCurrentPageIndex()
        assert len(keyList) <= self.maxNumberOfKeysPerPage
        i = 0
        for box in self.view._keysSection._vbox.children:
            for butt in box.children:
                if(i < len(keyList)):
                    butt.description = keyList[i]
                    butt.tooltip = keyList[i]
                    butt.layout.display = None
                else:
                    butt.layout.display = "none"
                i += 1

class PickleOpsController:
    def __init__(self, parentCont):
        self.parent = parentCont
        self.view = self.parent.view.opsSec
        self._setCallbacks()
        self._create_ops = CreateOps(self)
        self.view._opsOption.options = [("..",NothingDoOps(self)),("add", self._create_ops), 
                                        ("delete", DeleteOps(self)), ("update", UpdateOps(self)) ]
        
    def _setCallbacks(self):
        self.view._opsOption.observe(self.opsSelected, names="value")
        self.view._mode.observe(self.showOpsMode, names="value")
        
    def opsSelected(self, change):
        ops = change['new']
        self.view._opsContentArea.children = ops.getGui()
        
    def showOpsMode(self,change):
        if(change['new']):
            self.parent.view._opsrow.layout.display = "flex" 
        else:
            self.parent.view._opsrow.layout.display = "none"
            
class OpContInterface:
    def __init__(self, parentCont):
        self.parent = parentCont
        self.confirmingFunc = None
        
    def ok(self, btn):
        raise IOError("not implemented yet")
    
    def confirm(self, btn):
        raise IOError("not implemented yet")
    
    def getGui(self):
        raise IOError("not implemented yet")
    
    def confirmOrOk(self,okShow):
        self.parent.parent.view.output.clear()
        a = "none"
        b = None
        if(okShow):
            a = None
            b = "none"
        self.parent.view._confirm.layout.display = b
        self.parent.view._ok.layout.display = a
        
    def connectCallbacks(self):
        self.parent.view._ok._click_handlers.callbacks = []
        self.parent.view._confirm._click_handlers.callbacks = []
        self.parent.view._ok.on_click(self.ok)
        self.parent.view._confirm.on_click(self.confirm)
        
class NothingDoOps(OpContInterface):
    def ok(self, btn):
        pass
    def confirm(self, btn):
        pass
    def getGui(self):
        return []
    
class CreateOps(OpContInterface):
    def getGui(self):
        super().confirmOrOk(True)  
        super().connectCallbacks()  
        return [self.parent.view._key, self.parent.view._value, self.parent.view._isVar, self.parent.view._override,
                self.parent.view._ok, self.parent.view._confirm]

    def ok(self, btn):
        key = self.parent.view._key.value.strip()
        val = self.parent.view._value.value
        out = self.parent.parent.view.output
        out.clear()
        if(key == ""):
            out.add2Output(widgets.HTML(f"<font face='comic sans ms' color ='red'>key is empty</font>"))
            return 
        if(self.parent.parent.model.alreadyExists(key) and not self.parent.view._override.value):
            out.add2Output(widgets.HTML(f"<font face='comic sans ms' color ='Thistle'>key already exist</font>"))
            return
        if(self.parent.view._isVar.value):
            val = self._param[val]
        self.confirmingFunc = lambda : self.parent.parent.model.add(key, val)
        super().confirmOrOk(False) 
    def confirm(self, btn):
        self.confirmingFunc()
        super().confirmOrOk(True)
        self.confirmingFunc = None
        self.parent.parent.sync()
    def set_globals(self, param):
        self._param = param
class DeleteOps(OpContInterface):
    def getGui(self):
        super().confirmOrOk(True)
        super().connectCallbacks() 
        self.parent.parent.sync()
        self.parent.view._key.value = ""
        return [self.parent.view._key, self.parent.view._ok, self.parent.view._confirm]
    
    def ok(self, btn):
        key = self.parent.view._key.value.strip()
        if(not self.parent.parent.model.alreadyExists(key)):
            self.parent.parent.view.output.add2Output(widgets.HTML(
                f"<font face='comic sans ms' color ='red'> key doesnot exist</font>"))
            return
        self.confirmingFunc = lambda : self.parent.parent.model.delete(key)
        super().confirmOrOk(False)
    
    def confirm(self, btn):
        self.confirmingFunc()
        super().confirmOrOk(True)
        self.confirmingFunc = None
        
class UpdateOps(OpContInterface):
    def getGui(self):
        super().confirmOrOk(True)
        super().connectCallbacks()  
        return [self.parent.view._key,self.parent.view._newKeyName, self.parent.view._ok, self.parent.view._confirm]
    def ok(self, btn):
        key = self.parent.view._key.value.strip()
        newKey = self.parent.view._newKeyName.value.strip()
        if(key == "" or newKey == ""):
            self.parent.parent.view.output.add2Output(widgets.HTML(
                f"<font face='comic sans ms' color ='red'>key cannot be empty</font>"))
            return 
        val = self.parent.parent.model.value()[key]
        self.confirmingFunc = lambda : [self.parent.parent.model.delete(key), 
                                        self.parent.parent.model.add(newKey, val)]
        super().confirmOrOk(False)
    
    def confirm(self, btn):
        self.confirmingFunc()
        super().confirmOrOk(True)
        self.confirmingFunc = None
        
class PickleOpsModel:
    def __init__(self):
        self._loc = []
        self.content = {}
        self.filePath = None
        self._sync = True
        
    def loadFileFromDB(self, fileName):
        from useful.jupyterDB import jupyterDB
        self._loc = []
        self.content = jupyterDB.pickle().read(fileName)
        self.filePath = jupyterDB.pickle().path(fileName)
        self._sync = True
    
    def loadFile(self, filepath):
        self.content = SerializationDB.readPickle(filepath)
        self._loc = []
        self.filePath = filepath
        self._sync = True
        
    def getKeys(self):
        val = ListDB.dicOps().get(self.content, self._loc)
        if(type(val) == dict):
            return list(val.keys())
        raise IOError("value is not a dictionary")
    
    def isDic(self):
        val = ListDB.dicOps().get(self.content, self._loc)
        return type(val) == dict
        
    def value(self):
        return ListDB.dicOps().get(self.content, self._loc)
    
    def goForward(self, key):
        self._loc.append(key)
        
    def goback(self):
        if(len(self._loc) > 0):
            self._loc.pop()

    def add(self, key, val):
        from useful.SerializationDB import SerializationDB
        ListDB.dicOps().add(self.content,self._loc + [key], val)
        if self._sync:
            SerializationDB.pickleOut(self.content, self.filePath)
    def alreadyExists(self, key):
        try:
            ListDB.dicOps().get(self.content, self._loc + [key])
        except:
            return False
        return True
    def delete(self, key):
        ListDB.dicOps().delete(self.content, self._loc + [key])
        if self._sync:
            SerializationDB.pickleOut(self.content, self.filePath)
    def set_dictionary(self, dic):
        self.content = dic
        self._loc = []
        self._sync = False
    def set_base_location(self, loc):
        self._loc = loc
        self._baseloc = loc
    