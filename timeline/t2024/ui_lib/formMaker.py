import datetime
from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum
from basic import Main as ObjMaker
def TextInput():
    container = Utils.get_comp({}, IpywidgetsComponentsEnum.Text)
    def set_value(value):
        s.views.container.outputs.layout.value = value
    def clear():
        s.views.container.outputs.layout.value = ""
    def process_info(info):
        pass
    def is_empty():
        return s.views.container.outputs.layout.value.strip() == ""
    def value():
        return s.views.container.outputs.layout.value
    s = ObjMaker.uisOrganize(locals())
    return s
def TextAreaInput():
    container = TextInput()
    container.views.container = Utils.get_comp({}, IpywidgetsComponentsEnum.Textarea)
    return container
def DateInput():
    container = Utils.get_comp({}, IpywidgetsComponentsEnum.DatePicker)
    def set_value(value):
        s.views.container.outputs.layout.value = value
    def clear():
        s.views.container.outputs.layout.value = None
    def process_info(infos):
        k = "auto"
        if k in infos and infos[k]:
            s.handlers.set_today_date()
    def set_today_date():
        s.handlers.set_value(datetime.datetime.now())
    def is_empty():
        return True
    def value():
        return s.views.container.outputs.layout.value
    s = ObjMaker.uisOrganize(locals())
    return s
def DateTimeInput():
    container = DateInput()
    container.views.container = Utils.get_comp({}, IpywidgetsComponentsEnum.NaiveDatetimePicker)
    def set_today_datetime():
        s.handlers.set_value(datetime.datetime.now())
    container.handlers.set_today_datetime = set_today_datetime
    container.handlers.defs.set_today_datetime = set_today_datetime
    return container
def TimeInput():
    dateInput = DateInput()
    dateInput.views.container = Utils.get_comp({}, IpywidgetsComponentsEnum.TimePicker)
    container = dateInput.views.container
    def process_info(infos):
        k = "auto"
        if k in infos and infos[k]:
            s.handlers.set_now_time()
    def set_now_time():
        now = datetime.datetime.now()
        s.handlers.set_value(datetime.time(now.hour, now.minute))
    s = ObjMaker.uisOrganize(locals())
    ObjMaker.dicToNamespace(dateInput.handlers.__dict__, s.handlers, True)
    return s
def BooleanInput():
    textInput = TextInput()
    textInput.views.container = Utils.get_comp({}, IpywidgetsComponentsEnum.Checkbox)
    container = textInput.views.container
    def _():
        pass
    s = ObjMaker.uisOrganize(locals())

    ObjMaker.dicToNamespace(textInput.handlers.__dict__, s.handlers, True)
    return s
def MutipleSelectInput():
    from timeline.t2024.ui_lib.listCrud import ListCRUD
    lc = ListCRUD()
    container = lc.views.container
    def set_value(value):
        s.process.lc.handlers.set_values(value)
    def clear():
        s.views.container.state.controller.set_model([])
        s.views.container.state.controller.reset()
    def process_info(infos):
        pass
    def is_empty():
        return len(s.handlers.value()) == 0
    def value():
        return s.process.lc.handlers.get_values()
    s = ObjMaker.uisOrganize(locals())
    return s
def DropdownInput():
    container = Utils.get_comp({}, IpywidgetsComponentsEnum.Dropdown)
    def set_value(value):
        s.views.container.outputs.layout.value = value
    def clear():
        s.views.container.outputs.layout.value = None
    def process_info(infos):
        k = "options"
        if k in infos and infos[k]:
            s.views.container.outputs.layout.options = infos[k]
    def is_empty():
        return True
    def value():
        return s.views.container.outputs.layout.value
    s = ObjMaker.uisOrganize(locals())
    return s
def KeyValueInput():
    from timeline.t2024.ui_lib.refactored_key_value_adder import Main as KVMain
    kv = KVMain.key_val_normal()
    container = kv.process.container.views.container
    def set_value(dic):
        s.process.kv.handlers.set_dictionary(dic)
    def clear():
        s.handlers.set_value({})
    def process_info(infos):
        pass
    def is_empty():
        return len(s.handlers.value()) == 0
    def value():
        return s.process.kv.handlers.readAll()
    s = ObjMaker.uisOrganize(locals())
    return s
def KeyValueMetaInput():
    from timeline.t2024.ui_lib.refactored_key_value_adder import Main as KVMain
    kv = KVMain.key_val_with_search_and_sort()
    container = kv.process.container.views.container
    def set_value(dic):
        s.process.kv.process.kvapwm.process.model.set_dictionary(dic)
        s.process.kv.process.kvapwm.handlers.render_and_update_ops_comp()
    def clear():
        s.handlers.set_value({'value': {}, 'meta': {'type': dict}})
    def process_info(infos):
        pass
    def is_empty():
        return len(s.handlers.value()["value"]) == 0
    def value():
        return s.process.kv.process.container.handlers.readAll()
    s = ObjMaker.uisOrganize(locals())
    return s
def FormGenerator():
    structure = {}
    saveBtn = Utils.get_comp({"description": "save"}, IpywidgetsComponentsEnum.Button)
    container = None
    comps = []
    def set_struct(dic):
        s.process.structure = dic
    def render():
        for ke in s.process.structure:
            typ = s.process.structure[ke]["type"]
            info = s.process.structure[ke]["info"]
            if typ == "Text":
                comp = TextInput()
            elif typ == "LargeText":
                comp = TextAreaInput()
            elif typ == "Checkbox":
                comp = BooleanInput()
            elif typ == "Options":
                comp = DropdownInput()
            elif typ == "Date":
                comp = DateInput()
            elif typ == "Time":
                comp = TimeInput()
            elif typ == "DateTime":
                comp = DateTimeInput()
            elif typ == "KeyValuesPair":
                comp = KeyValueInput()
            elif typ == "MultipleSelect":
                comp = MutipleSelectInput()
            elif typ == "Boolean":
                comp = BooleanInput()
            else:
                raise IOError("type not found")
            comp.handlers.process_info(info)
            labeledComp = FieldComponent(ke, comp.views.container)
            comp.views.container.state.parent = comp
            s.process.comps.append((ke, labeledComp))
    def get_layout():
        if s.process.container is not None:
            return s.process.container
        viewComps = [c.views.container for k, c in s.process.comps]
        forms = Utils.container(viewComps, className="flex flex-column")
        s.process.container = Utils.container([forms, s.views.saveBtn], className="flex flex-column")
        return s.process.container
    def reset():
        for k, c in s.process.comps:
            c.clear()
    def value():
        res = {}
        for k, com in s.process.comps:
            res[k] = com.value()
        return res
    def set_values(values):
        res = {k: c for k, c in s.process.comps}
        for k in values:
            val = values[k]
            res[k].set_value(val)
    def is_empty():
        res = True
        for k, c in s.process.s.process.comps:
            res = res and c.is_empty()
        return res
    s = ObjMaker.uisOrganize(locals())
    return s
