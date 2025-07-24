from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from useful.basic import Main as ObjMaker
from timeline.t2024.ui_lib.refactored_key_value_adder import Main as KVMain
from timeline.t2024.generic_logger.generic_loggerV3 import AddCancelBtns
from timeline.t2024.generic_logger.generic_loggerV4 import Constants

def MetaCRUDV2():
    K = Constants()
    acb = AddCancelBtns()
    kvn = KVMain.key_val_normal()
    addBtn = Utils.get_comp({"description":"add"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    acb.views.container.hide()
    container = Utils.container([kvn.process.container.views.container, addBtn, acb.views.container], className ="flex flex-column")
    parent = None
    def readAll():
        return s.process.kvn.handlers.readAll()
    def save():
        p = s.process.parent
        tbId = p.process.logger.process.model.read([K.tables, K.table2Id, p.process.current_button.description])
        p.process.logger.process.model.write([K.meta, tbId, "dicData"], s.handlers.readAll(), True)
        s.views.addBtn.hide()
    def set_content(content):
        s.process.kvn.handlers.set_dictionary(content)
        s.views.addBtn.show()
    def reset():
        s.handlers.set_content({})
    def onAdd(w):
        s.process.acb.views.container.show()
    def onCancel(w):
        s.process.acb.views.container.hide()
    def onConfirm(w):
        s.handlers.save()
        s.process.acb.views.container.hide()
    def loadDataFromTable(tableName):
        p = s.process.parent
        tbId = p.process.logger.process.model.read([K.tables, K.table2Id, tableName])
        if p.process.logger.process.model.exists([K.meta, tbId, "dicData"]):
            s.handlers.set_content(p.process.logger.process.model.read([K.meta, tbId, "dicData"]))
        else:
            s.handlers.set_content({})
    acb.views.cancelBtn.handlers.handle = onCancel
    acb.views.confirmBtn.handlers.handle = onConfirm
    addBtn.handlers.handle = onAdd
    s = ObjMaker.uisOrganize(locals())
    return s
def UpdateMenuBar():
    mcv2 = MetaCRUDV2()
    parent = None # parent is updateForm
    prev_toggle = None
    container = mcv2.views.container
    def onToggle(w):
        p = s.process.parent
        opt = p.views.toogleButtons.outputs.layout.value
        if opt == "meta":
            p.views.outArea.state.controller.display(s.process.mcv2.views.container.outputs.layout, True, True)
            s.process.mcv2.handlers.loadDataFromTable(p.process.parent.process.current_button.description)
        else:
            s.process.prev_toggle(w)
    def res_button_clicker_parent(w):
        p = s.process.parent
        s.process.previous_btn_res_clicker(w)
        crd = p.process.parent.process.container.process.crudView.views.crudView.outputs.layout.value
        if crd == "u":
            s.handlers.onToggle(1)
    def setup():
        p = s.process.parent
        s.process.prev_toggle = p.views.toogleButtons.handlers.handle
        p.views.toogleButtons.handlers.handle = s.handlers.onToggle
        p.handlers.toggled = s.handlers.onToggle
        p.process.metaCrud = s.process.mcv2
        s.process.mcv2.process.parent = p.process.parent
        p.handlers.update_uis = s.handlers.updatUis
        s.process.previous_btn_res_clicker = p.process.parent.process.resultDisplayer.views.btns.handlers.handle
        p.process.parent.process.resultDisplayer.views.btns.handlers.handle = s.handlers.res_button_clicker_parent
    def updatUis(w):
        pass
    s = ObjMaker.uisOrganize(locals())
    return s