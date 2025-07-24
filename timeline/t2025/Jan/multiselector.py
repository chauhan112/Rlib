from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from basic import Main as ObjMaker

def MultiSelector():
    label = Utils.get_comp({"value": "title"}, IpywidgetsComponentsEnum.Label, bind=False)
    lister = Utils.get_comp({"rows": 10}, IpywidgetsComponentsEnum.SelectMultiple, className="w-100 p0")
    btn = Utils.get_comp({"description":"add"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    container = Utils.container([label, lister, btn], className="flex flex-column w-100")
    s = ObjMaker.uisOrganize(locals())
    return s
def SelectFromLeftRight(runSetup=True):
    left = MultiSelector()
    right = MultiSelector()
    container = Utils.container([left.views.container, right.views.container], className= "w-50")
    def setup():
        left = s.process.left
        right = s.process.right
        left.views.label.outputs.layout.value = "available"
        right.views.label.outputs.layout.value = "selected"
        left.views.btn.outputs.layout.description = ""
        left.views.btn.outputs.layout.icon = "arrow-right"
        right.views.btn.outputs.layout.description = ""
        right.views.btn.outputs.layout.icon = "arrow-left"
        s.handlers.onRightSelected(1)
        s.handlers.onLeftSelected(1)
    def set_options(left =[], right= []):
        s.process.left.views.lister.outputs.layout.options = left
        s.process.right.views.lister.outputs.layout.options = right
    def onLeftSelected(w):
        if len(s.process.left.views.lister.outputs.layout.value):
            s.process.left.views.btn.show()
        else:
            s.process.left.views.btn.hide()
    def onRightSelected(w):
        if len(s.process.right.views.lister.outputs.layout.value):
            s.process.right.views.btn.show()
        else:
            s.process.right.views.btn.hide()
    def get_selected():
        return s.process.right.views.lister.outputs.layout.value
    def values():
        return s.process.left.views.lister.outputs.layout.value, s.handlers.get_selected()
    left.views.lister.handlers.handle = onLeftSelected
    right.views.lister.handlers.handle = onRightSelected
    s = ObjMaker.uisOrganize(locals())
    if runSetup:
        setup()
    return s