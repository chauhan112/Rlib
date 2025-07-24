from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from basic import Main as ObjMaker
from ancient.ClipboardDB import ClipboardDB
import json

def ListFilterSettings():
    titleWid = Utils.get_comp({"placeholder":"give title"}, IpywidgetsComponentsEnum.Text, className="w-auto", bind = False)
    funcINp = Utils.get_comp({"placeholder":"func content"}, IpywidgetsComponentsEnum.Textarea, className="w-auto", bind = False)
    interpretJson = Utils.get_comp({"placeholder":"paste json to copy function content"}, IpywidgetsComponentsEnum.Textarea, 
                                   className="w-auto", bind = False)
    copyBtn = Utils.get_comp({"description":"copy func"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    copyFuncText = Utils.get_comp({"description":"copy func from text"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    interpretor = Utils.container([interpretJson, copyBtn, copyFuncText], className="flex flex-column")
    btn = Utils.get_comp({"description":"copy to clip"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    container = Utils.container([Utils.container([titleWid, funcINp, btn], className="flex flex-column"), interpretor])
    
    def onCopy(w):
        content = funcINp.outputs.layout.value
        title = s.views.titleWid.outputs.layout.value
        contentToCopy= f'{{"filter": {{"options": [["{title}", ["search", [[], "exec",  {json.dumps(content)}, false]]]]}}}}'
        ClipboardDB.copy2clipboard(contentToCopy)
    def onCopyFunc(w):
        vals = interpretJson.outputs.layout.value
        valsdic = json.loads(vals)
        ClipboardDB.copy2clipboard(valsdic["filter"]["options"][0][1][1][2])
    def onCopyFromText(w):
        vals = interpretJson.outputs.layout.value
        ClipboardDB.copy2clipboard(vals.replace("\\n", "\n"))
    btn.handlers.handle = onCopy
    copyBtn.handlers.handle = onCopyFunc
    copyFuncText.handlers.handle = onCopyFromText
    s = ObjMaker.uisOrganize(locals())
    return s