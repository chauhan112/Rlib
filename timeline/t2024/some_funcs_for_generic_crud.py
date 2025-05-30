from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from basic import Main as ObjMaker
from timeline.t2024.generic_crud import AdvanceCRUDFilterer, formMaker
from jupyterDB import jupyterDB

def f_for_links_open_hochschule_compass():
    import webbrowser
    outArea = Utils.get_comp({}, IpywidgetsComponentsEnum.Output, className="w-auto", bind = False)
    btn = Utils.get_comp({"description":"open"},IpywidgetsComponentsEnum.Button)
    container = Utils.container([btn, outArea], className="flex flex-column")
    def set_data(data, ctx):
        s.process.data = data
        s.process.parent = ctx
        s.views.outArea.outputs.layout.clear_output()
        with s.views.outArea.outputs.layout:
            res = ""
            for ke in data:
                res +=  ke + ": " +  str(data[ke]) + "\n"
                res += ("-"*40) + "\n"
            print(res)
    def onClick(w):
        link = s.process.data["link"]
        baseUrl = "https://www.hochschulkompass.de"
        webbrowser.open(baseUrl + link)
    btn.handlers.handle = onClick
    s = ObjMaker.uisOrganize(locals())
    return s

def f_2nd_layer():
    from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
    from basic import Main as ObjMaker
    
    from timeline.t2024.generic_crud import AdvanceCRUDFilterer, formMaker
    adf = AdvanceCRUDFilterer()
    container = adf.views.container
    forms = {}
    def isChanged():
        s.process.parent.views.saveBtn.show()
    def set_data(vals, p):
        jupyterDB._params["temp"] = (vals, p)
        s.process.parent = p.process.parent
        # s.handlers.set_info()
    def set_info(infos):
        s.process.adf.process.cf.process.model.handlers.set_data(infos)
        s.process.adf.process.tf.handlers.setup_filters()
        cf = s.process.adf.process.cf
        model = s.process.adf.process.cf.process.model.process.dicModel
        s.process.adf.process.cf.process.model.process.dicModel.changed = lambda : None
        if model.exists(["meta", "filters", "data"]):
            s.process.adf.process.tf.handlers.onFilterChange(1)
        else:
            s.process.adf.process.cf.process.scv.process.searchComponent.views.inputText.outputs.layout.value = ""
            s.process.adf.process.cf.process.scv.process.searchComponent.views.searchType.outputs.layout.value = "any"
        s.process.adf.process.cf.process.model.process.dicModel.changed = s.handlers.isChanged
        cf.process.scv.process.crudView.views.crudView.outputs.layout.value = "u"
        cf.process.scv.process.crudView.views.crudView.outputs.layout.value = "r"
        cf.process.scv.views.keysOut.state.controller.clear()
    def get_form():
        p = s.process.adf.process.cf
        if p.process.model.process.dicModel.exists(["meta", "structure"]):
            pstr = p.process.model.process.dicModel.read(["meta", "structure"])
            kke = tuple(sorted(pstr, key =lambda x: pstr[x]["order"]))
            pstr = {k: pstr[k] for k in kke}
            if kke not in s.process.forms:
                s.process.forms[kke] = formMaker()
            p.process.form = s.process.forms[kke]
            p.process.form.handlers.set_structure(pstr)
            return ("fgv2", p.process.form)
        else:
            return ("basic", p.process.basicForm)
    adf.process.cf.handlers.get_form = get_form
    s = ObjMaker.uisOrganize(locals())
    adf.process.parent = s
    return s

def f_from_job_search():
    s = f_2nd_layer()
    def set_data(vals, p):
        jupyterDB._params["temp"] = (vals, p)
        s.process.parent = p.process.parent
        infos = vals["more info"]
        s.handlers.set_info(infos)
    s.handlers.set_data = set_data
    return s