from modules.mobileCode.CmdCommand import GDataSetable, IRunnable, GParentable, GController, IReturnable
import ipywidgets as widgets
class IElement:
    def callback(self):
        raise NotImplementedError("abstract method")
    def getName(self):
        raise NotImplementedError("abstract method")

class GElement(IElement, GDataSetable):
    def __init__(self, name, callback):
        self._name = name 
        self._callback = callback

    def callback(self):
        return lambda x: self._callback(self.data)
    def getName(self):
        if not type(self._name) == str:
            self._name = str(self._name)
        return self._name

class GNotebookLayoutController(IReturnable):
    instances = {}
    def __init__(self, cols = 5):
        self.nCols = cols
        
    def get(self, elements):
        btns =  []
        for ele in elements:
            btns.append(self._getBtn(ele.getName(), ele.callback()))
        hboxes = [widgets.HBox(btns[i:i+self.nCols]) for i in range(0, len(btns), self.nCols)]
        return widgets.VBox(hboxes)
        
    def _getBtn(self, name, func):
        b = widgets.Button(description =name)
        b.on_click(func)
        return b

class DefaultCallback(IRunnable, GParentable):
    def run(self, selected):
        print(selected)

class ViewRunner(IRunnable, GParentable):
    def __init__(self, callback:IRunnable = None, btnName= lambda x: x):
        self.out = widgets.Output()
        self.cnt = GNotebookLayoutController()
        self._callback = DefaultCallback()
        if callback is not None:
            self._callback.run = callback
        self._callback.setParent(self)
        self._btnName = btnName
        
    def run(self):
        display(self.out)
        elements = self.parent.lister.get()
        eles = []
        for data in elements:
            ele = GElement(self._btnName(data), self._callback.run)
            ele.setData(data)
            eles.append(ele)
        self.out.clear_output()
        with self.out:
            display(self.cnt.get(eles))
            
class Hdf5Explorer(IReturnable, GDataSetable, GParentable):
    def __init__(self):
        self.curPos = []
    def setData(self, filepath):
        import h5py
        self.exp = h5py.File(filepath, "r") 
    def _get(self, key):
        val = self.exp
        for v in self.curPos:
            val = val[v]
        if key is not None:
            val = val[key]
        return val
    
    def get(self, key = None):
        val = self._get(key)
        return ['..'] + list(val.keys())
        
    def cd(self, n):
        if (n == ".."):
            if len(self.curPos) != 0:
                self.curPos.pop()
                self.parent.cmdRunner.run()
            return 
        try:
            self.get(n)
            self.curPos.append(n)
            self.parent.cmdRunner.run()
        except Exception as e:
            print(n, self._get(n)[()])

class DicExplorerCallback(IRunnable, GParentable):
    def run(self, selected):
        exp = self.parent.parent.lister.dicExp # lister is of type DicList
        if selected == '..':
            exp.goBack()
            self.parent.run()
            return
        content = exp.getCurrentValue()
        if type(content) == dict:
            exp.cd(selected)
        self.parent.run()
        
class OSExpCallback(IRunnable, GParentable):
    def run(self, selected):
        exp = self.parent.parent.lister # lister is of type IPathOps and IChangeableList
        if exp.unprefixDir(selected) == '..':
            exp.exp.goBack()
            self.parent.run()
            return
        if exp.isdir(selected):
            exp.cd(exp.unprefixDir(selected))
        self.parent.run()
        
        #lister = OSChangeableList(os.path.abspath('.'))
        #GController(cmdRunner = ViewRunner(callback=OSExpCallback(), btnName=lister.unprefixDir), 
        #    lister = lister).run()
        