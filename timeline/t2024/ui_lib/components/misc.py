from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from timeline.t2024.Array import Array
from useful.basic import Main as ObjMaker, ObjectOps
import string
def DropdownWithFilter():
    title = Utils.get_comp({"placeholder":"filter title"}, IpywidgetsComponentsEnum.Text, className="w-fit")
    lister = Utils.get_comp({"rows": 10}, IpywidgetsComponentsEnum.Select, className="w-auto position-abs coord")
    classes = """
    .position-abs{
        position: absolute;
    }
    .position-rel{
        position: relative;
        height: 204px;
    }
    .coord{
        top: 28px;
        width: 178px;
        z-index: 2;
    }
    """
    customCss = Utils.get_comp({}, ComponentsLib.CSSAdder)
    customCss.outputs.layout.content = classes
    options = []
    container = Utils.container([title, lister, customCss], className="flex flex-column w-fit position-rel")
    def onTextChange(w):
        textval = title.outputs.layout.value.strip()
        lister.outputs.layout.options = Array(s.process.options).filter(lambda x: textval in x).array[:20]
        
        try:
            lister.handlers.handle =  s.handlers.doNothing
            lister.outputs.layout.value = None
            lister.handlers.handle =  s.handlers.onSelected
        except:
            pass
        s.handlers.update_lister()
    def onSelected(w):
        title.handlers.handle = s.handlers.doNothing
        title.outputs.layout.value = lister.outputs.layout.value
        title.handlers.handle = s.handlers.onTextChange
        lister.hide()
    def doNothing(w):
        pass
    def set_options(options):
        s.process.options = options
        lister.outputs.layout.options = options[:20]
        s.handlers.update_lister()
    def update_lister():
        if len(lister.outputs.layout.options) == 0:
            lister.hide()
        else:
            lister.show()
    title.handlers.handle = onTextChange
    lister.handlers.handle = onSelected
    
    s = ObjMaker.uisOrganize(locals())
    return s
    
def Keyboard():
    classes = """
    .width {
        width:7rem
    }
    .width-half{
        width: 4rem;
    }
    .tgl-btns button{
        width:auto;
    }
    """
    def doNothing(w):
        pass
    title = Utils.get_comp({"placeholder":"filter title"}, IpywidgetsComponentsEnum.Text, bind=False)
    lister = Utils.get_comp({"rows": 4, "options": string.ascii_lowercase}, IpywidgetsComponentsEnum.ToggleButtons, className="tgl-btns")
    customCss = Utils.get_comp({}, ComponentsLib.CSSAdder)
    backBtn = Utils.get_comp({"icon":"arrow-left"}, IpywidgetsComponentsEnum.Button, className="w-auto")
    customCss.outputs.layout.content = classes
    container = Utils.container([Utils.container([title, backBtn]), lister, customCss], className="flex flex-column w-fit")
    lister.handlers.handle = doNothing
    lister.outputs.layout.value = None
    def onSelected(w):
        if s.views.lister.outputs.layout.value:
            s.views.title.outputs.layout.value += s.views.lister.outputs.layout.value
        s.views.lister.outputs.layout.value = None
    lister.handlers.handle = onSelected
    backBtn.handlers.handle = lambda x: ObjectOps.setter(title.outputs.layout, ["value"], "")
    s = ObjMaker.uisOrganize(locals())
    return s