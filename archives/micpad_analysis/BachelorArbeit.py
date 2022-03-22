import ipywidgets as widgets
from ProjectAnalysis import ProjectAnalysis
from lib.Libs import Libs
import os

class BachelorArbeit:
    def __init__(self,redesignedPath, oldProjectPath):
        self._oldProjectPath = oldProjectPath
        self._newProjectPath = redesignedPath
        self._oldMic = None
        self._newMic = None
        
    def preprocess(self):
        class Redesign:
            index = 0
            files = Libs.path().filesWithExtensions(['h', 'cpp'], self._oldProjectPath)
            def openScript():
                File.openFile(Redesign.currentFile())
            def reset(index = 0):
                Redesign.index = index
            def currentFile():
                return Redesign.files[Redesign.index]
            def nextt():
                if(Redesign.index >= len(Redesign.files)):
                    print("All files opened")
                    return
                Redesign.index += 1
                
        class Temp:
            def button(name, callbackFunc = None, tooltip = ''):
                b = widgets.Button(description=name, tooltip= str(tooltip))
                if(callbackFunc is not None):
                    b.on_click(callbackFunc)
                return b
            def add(x):
                name = x.description
                currentFileName = os.path.basename(Redesign.currentFile())
                copy2File = Libs.path().joinPath(self._newProjectPath, "module", name, currentFileName)
                clipContent = Libs.clip().text()
                clipContent = "\n\n"+"\n".join(clipContent.splitlines())
                Libs.fileOps().appendToFile(copy2File, clipContent)
            def clear(x):
                pass
            def openContent(x):
                name = x.description
                currentFileName = os.path.basename(Redesign.currentFile())
                copy2File = Libs.path().joinPath(self._newProjectPath, "module", name, currentFileName)
                Libs.fileOps().openFile(copy2File)
        print("add")
        display(widgets.HBox([Temp.button("Model", Temp.add),
                      Temp.button("View", Temp.add), 
                      Temp.button("Controller", Temp.add)]))
        print("open")
        display(widgets.HBox([Temp.button("Model", Temp.openContent),
                      Temp.button("View", Temp.openContent), 
                      Temp.button("Controller", Temp.openContent)]))
                      
    def oldMICpad(self):
        if(self._oldMic is None):
            self._oldMic = ProjectAnalysis(self._oldProjectPath, 'old MICpad')
        return self._oldMic
            
        
    def redesignedMICpad(self):
        if(self._newMic is None):
            self._newMic = ProjectAnalysis(self._newProjectPath, 'redesigned MICpad')
        return self._newMic
        
    def calculateTheImproveMent(self, optimalComplexity = 3.5):
        old = self.oldMICpad()
        new = self.redesignedMICpad()
        cn = new.total().numberOfComplexity()
        co = old.total().numberOfComplexity()
        mn = new.total().numberOfMethods()
        mo = old.total().numberOfMethods()
        predCom = mn * optimalComplexity
        tot= co - predCom

        improved = co - cn
        return improved *100/ tot