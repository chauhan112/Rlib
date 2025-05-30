from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from basic import Main as ObjMaker
from LibsDB import LibsDB
def NewRlibItTools():
    import os
    from timeline.t2024.ui_lib.refactored_key_value_adder import Main
    kvs = Main.key_val_app_with_meta()
    goToRootBtn = Utils.get_comp({"icon":"square-root-alt"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    kvs.views.locRow.append(goToRootBtn)
    container = kvs.views.container
    def onClick(w):
        kvs = s.process.kvs
        while len(kvs.process.model.s.process.loc) > 0:
            kvs.process.model.s.process.loc.pop()
        kvs.process.model.set_baseloc(kvs.process.model.s.process.loc)
        kvs.views.outputArea.outputs.layout.clear_output()
        kvs.process.keysDisplayer.process.pageNr = 1
        kvs.handlers.render_and_update_ops_comp()
        kvs.handlers.update_loc()
    def set_up():
        kvs = s.process.kvs
        filename = os.sep.join([LibsDB.cloudPath(), 'timeline', '2024', '05_May', "new_rlib_it.pkl"])
        kvs.process.keyValueModel.process.model.set_file(filename)
        kvs.process.printLeafVals = False
        s.views.goToRootBtn.handlers.handle = s.handlers.onClick
    s = ObjMaker.uisOrganize(locals())
    return s