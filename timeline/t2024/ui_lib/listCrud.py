from basic import Main as ObjMaker
from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from timeline.t2024.generic_logger.generic_loggerV3 import AddCancelBtns, ResultDisplayers
from SearchSystem import MultilineStringSearch
def ListCRUD():
    opsWid = Utils.get_comp({"options": ["add",'update',"delete"]},IpywidgetsComponentsEnum.Dropdown, className = "w-auto")
    textWid = Utils.get_comp({"placeholder":"add word"}, IpywidgetsComponentsEnum.Text, className="w-auto", bind = False)
    addConfirm = AddCancelBtns()
    addConfirm.views.cancelBtn.outputs.layout.description = "add"
    addConfirm.views.confirmBtn.hide()
    output = Utils.get_comp({}, ComponentsLib.CustomOutput)
    container = Utils.container([Utils.container([opsWid, textWid, addConfirm.views.container]), output], className="flex flex-column")
    searcher = MultilineStringSearch([], True)
    model = []
    resultDisplayer = ResultDisplayers()
    currentIndex = None
    opsWid.state.undoers = []
    def set_values(model):
        s.process.model = model
        s.handlers.displayModelValue()
    def get_values():
        return s.process.model
    def update_btn_value():
        s.process.addConfirm.views.cancelBtn.outputs.layout.description = s.process.addConfirm.views.cancelBtn.state.nextValue
    def displayModelValue():
        s.views.output.state.controller.display(str(s.process.model), True)
    def opsChanged(w):
        for func in opsWid.state.undoers:
            func()
        opsWid.state.undoers.clear()
        typ = s.views.opsWid.outputs.layout.value
        if typ == "add":
            s.process.addConfirm.views.cancelBtn.outputs.layout.description = "add"
            s.process.addConfirm.views.cancelBtn.handlers.handle = s.handlers.onAdd
            s.handlers.displayModelValue()
        elif typ == "update":
            s.process.addConfirm.views.cancelBtn.outputs.layout.description = "search"
            s.process.addConfirm.views.cancelBtn.handlers.handle = s.handlers.onSearch
        elif typ == "delete":
            s.process.addConfirm.views.cancelBtn.outputs.layout.description = "search"
            s.process.addConfirm.views.cancelBtn.handlers.handle = s.handlers.onSearch
    def onSearch(w):
        val = s.views.textWid.outputs.layout.value.strip()
        s.process.searcher.set_container(s.process.model)
        res = s.process.searcher.search(val, case=False)
        s.process.resultDisplayer.handlers.set_results(res, reverseIt=False)
        s.views.output.state.controller.display(s.process.resultDisplayer.views.container.outputs.layout, True, True)
    def onAdd(w):
        val = s.views.textWid.outputs.layout.value.strip()
        if val == "":
            return
        s.process.model.append(val)
        s.views.textWid.outputs.layout.value  = ""
        s.handlers.displayModelValue()
    def name_getter(x):
        if type(x) == str:
            return x
        return s.process.model[x]
    def result_btn_clicked(w):
        typ = s.views.opsWid.outputs.layout.value
        index = s.process.resultDisplayer.process.data[w._parent.state.index]
        s.process.currentIndex = index
        s.process.current_btn = w
        if typ == "update":
            val = s.process.model[index]
            s.views.textWid.outputs.layout.value = val
            s.process.addConfirm.views.cancelBtn.handlers.handle = s.handlers.update_confirm
            s.process.addConfirm.views.cancelBtn.outputs.layout.description = "confirm"
        elif typ == "delete":
            s.process.addConfirm.views.cancelBtn.handlers.handle = s.handlers.delete_confirm
            s.process.addConfirm.views.cancelBtn.outputs.layout.description = "confirm"
    def update_confirm(w):
        val = s.views.textWid.outputs.layout.value
        s.process.model[s.process.currentIndex] = val
        s.views.textWid.outputs.layout.value  = ""
        s.views.opsWid.outputs.layout.value = "add"
        s.handlers.displayModelValue()
    def delete_confirm(w):
        del s.process.model[s.process.currentIndex]
        s.process.addConfirm.views.cancelBtn.outputs.layout.description = "search"
        s.process.addConfirm.views.cancelBtn.handlers.handle = s.handlers.onSearch
        s.handlers.onSearch(w)
    resultDisplayer.handlers.name_getter = name_getter
    resultDisplayer.views.btns.handlers.handle = result_btn_clicked
    addConfirm.views.cancelBtn.handlers.handle = onAdd
    opsWid.handlers.handle = opsChanged
    s = ObjMaker.uisOrganize(locals())
    opsChanged(1)
    return s
