from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from basic import Main as ObjMaker
from timeline.t2023.generic_logger.components import GComponent
from timeline.t2024.ui_lib.refactored_key_value_adder import Main as KVMain
from timeline.t2024.listCrudWithFilter import Main as LMain
class NewListComponent(GComponent):
    def __init__(self, **kwargs):
        lcrud = LMain.listCrud()
        lcrud.views.container.outputs.layout.add_class("w-fit")
        descriptionLabel = Utils.get_comp(dict(value = kwargs["description"], 
                                               layout= dict(width="80px", justify_content= "flex-end", margin="0px 8px 0px 0px")), 
                                         IpywidgetsComponentsEnum.Label, bind=False)
        container = Utils.container([descriptionLabel,lcrud.views.container])
        self.set_widget(container.outputs.layout)
        self.state = ObjMaker.uisOrganize(locals())
    def clear(self):
        self.set_value(self.translator([]))
    def value(self):
        return self.state.process.lcrud.handlers.values()
    def process_info(self):
        pass
    def set_value(self, val):
        self.state.process.lcrud.handlers.set_values(val)
    def is_empty(self):
        return len(self.state.process.lcrud.process.model) == 0
    def translator(self, listWithStr):
        return {"values": [{"name": k} for k in listWithStr], "meta": {}}
class KeyValueInput(GComponent):
    def __init__(self, **kwargs):
        keyVal = KVMain.key_val_with_search_and_sort()
        descriptionLabel = Utils.get_comp(dict(value = kwargs["description"], 
                                               layout= dict(width="80px", justify_content= "flex-end", margin="0px 8px 0px 0px")), 
                                         IpywidgetsComponentsEnum.Label, bind=False)
        keyVal.process.container.views.container.outputs.layout.add_class("w-fit")
        container = Utils.container([descriptionLabel,keyVal.process.container.views.container])
        self.set_widget(container.outputs.layout)
        keyVal.process.kvapwm.process.keysDisplayer.views.btns.handlers.handle = self.btn_clicked
        keyVal.process.container.views.pathText.outputs.layout.add_class("w-auto")
        self.state = ObjMaker.uisOrganize(locals())
    def clear(self):
        self.set_value({})
    def value(self):
        return self.state.process.keyVal.process.kvapwm.process.model.s.process.model_inst.process.model_inst.process.vals
    def process_info(self):
        pass
    def set_value(self, val):
        self.state.process.keyVal.process.kvapwm.handlers.set_dictionary(val)
        self.state.process.keyVal.process.kvapwm.handlers.render_and_update_ops_comp()
    def is_empty(self):
        return len(self.value()) == 0
    def btn_clicked(self,tn):
        s = self.state.process.keyVal.process.kvapwm
        kd = s.process.keysDisplayer
        
        info = kd.process.data[tn._parent.state.index]
        isFolder = info[-1]    
        val = info[1][0]["value"]

        s.process.opsComp.views.keyInp.outputs.layout.value = info[0]
        
        key = info[1][2]
        s.process.current_location = s.process.model.get_current_location() + [key]
        s.views.outputArea.outputs.layout.clear_output()
        if isFolder:
            s.process.model.cd(key)
            s.handlers.render_and_update_ops_comp()
            s.handlers.update_loc()
        elif s.process.printLeafVals:
            with s.views.outputArea.outputs.layout:
                print(val)
            
def formMkaer():
    from timeline.t2024.generic_logger.generic_loggerV4 import FormGeneratorV2, SupportedTypes
    fg2 = FormGeneratorV2()
    fg2.process.viewGenerator._creator_map[SupportedTypes.KeyValuesPair.name] = lambda **x: KeyValueInput(**x)
    fg2.process.viewGenerator._creator_map[SupportedTypes.MultipleSelect.name] = lambda **x: NewListComponent(**x)
    return fg2
def gl_ke(filename):
    import os
    from timeline.t2024.generic_logger.generic_loggerV4 import Main
    from LibsDB import LibsDB
    cnt = Main.generic_logger(filename)
    cnt.process.loggerDataView.handlers.formMaker = formMkaer
    cnt.process.container.views.container.outputs.layout
    return cnt
