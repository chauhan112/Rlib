from timeline.t2024.ui_lib.components.cssAdder import AddCSSWidget
import os
from useful.LibsDB import LibsDB

def cssUpdator(state):
    from timeline.t2024.ui_lib.IpyComponents import IpywidgetsComponentsEnum, Utils
    from timeline.t2024.experiments.models import LocalStorageTableOps, ModelInitializer
    from basic import addToNameSpace
    ModelInitializer.initialize()
    app_name = "css_updator"
    key = "jupyter-css"
    cssContent = LocalStorageTableOps.read(app_name, key)["value"]
    cssEditorArea = Utils.get_comp({"placeholder":"css code", "value": cssContent}, IpywidgetsComponentsEnum.Textarea, className= "w-100 hmin-300px p0", bind=False)
    updateBtn = Utils.get_comp({"description":"update"}, IpywidgetsComponentsEnum.Button)
    updator = Utils.container([cssEditorArea, updateBtn], className="flex flex-column w-100")
    def update_callback(x = None):
        val = cssEditorArea.outputs.layout.value
        LocalStorageTableOps.update(app_name, key, val)
    updateBtn.handlers.handle = update_callback
    addToNameSpace(state, locals(), ["state"])

class Main:
    loaded = None
    ui = None
    def updatorLC(viewOnly=True):
        from basic import NameSpace
        state = NameSpace()
        cssUpdator(state)
        if viewOnly:
            return state.views.updator.outputs.layout
        return state
    def crudUI(returnController=False):
        from timeline.t2024.tailwind.twcrudOps import TailWindCRUDOps
        twcrud = TailWindCRUDOps()
        twcrud.process.CSSMain = Main
        twcrud.process.model.set_file(os.sep.join([LibsDB.cloudPath(), "timeline","2024","06_Jun","twcss.pkl"]))
        if returnController:
            return twcrud
        return twcrud.views.container.outputs.layout
    def loadInCssComponent(content = None):
        acw = AddCSSWidget()
        if content is None:
            Main.ui = Main.crudUI(True)
            acw.content = Main.ui.handlers.toText()
            Main.loaded = acw
        else:
            acw.content = content
        return acw
    