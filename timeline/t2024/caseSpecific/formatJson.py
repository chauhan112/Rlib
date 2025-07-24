from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from useful.basic import Main as ObjMaker
import json

def FormatJson():
    textWid = Utils.get_comp({"placeholder":"json content goes here"}, IpywidgetsComponentsEnum.Textarea, className="w-auto", bind = False)
    btn = Utils.get_comp({"description":"format"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    resultSection = Utils.get_comp({"placeholder":"formatted json results", "disabled": True}, IpywidgetsComponentsEnum.Textarea, className="w-auto hmin-300px", bind = False)
    container = Utils.container([Utils.container([textWid, btn]), resultSection],className = "flex-column")
    def onClick(w):
        c = s.views.textWid.outputs.layout.value.strip()
        if c:
            s.views.resultSection.outputs.layout.value = json.dumps(json.loads(c), indent=2)
    btn.handlers.handle = onClick
    s = ObjMaker.uisOrganize(locals())
    return s
