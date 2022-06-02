from modules.FileAnalyser.FileAnalyser import IExplorer
from modules.mobileCode.tree import LayerDicList, LayeredDisplayElements, Goback
from modules.mobileCode.CmdCommand import GController, CmdCommandHandler
class TerminalDicExplorer(IExplorer):
    def __init__(self, dic,callOnElement=lambda parent, val: val, cmds = []):
        display_elements = LayeredDisplayElements('l')
        display_elements._runAfter = True
        display_elements.setCommand(Goback('b'))
        self.controller = GController(dic, lister= LayerDicList(3),cmdRunner= CmdCommandHandler(extraCommands= cmds,
                                        callback= self.callbackFunc), displayer=display_elements )
        self.callOnElement = callOnElement
    def callbackFunc(self, ele):
        cdVal = ele.getCurrentValue()
        lastPos = ele.parent.parent.elementsDisplayer._lastPos
        exp = ele.parent.parent.lister
        lastPos.append(cdVal)
        from ListDB import ListDB
        content = ListDB.dicOps().get(exp.dicExp._content, exp.dicExp.currentPath + [cdVal])
        if (type(content) == dict):
            exp.dicExp.cd(cdVal)
        else:
            self.callOnElement(self, content)
    def explore(self):
        self.controller.run()
