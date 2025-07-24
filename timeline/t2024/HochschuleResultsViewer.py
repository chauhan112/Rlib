from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from useful.basic import Main as ObjMaker

def LoadOrSaveComp():
    keysOption = Utils.get_comp({"options": ["add",'update',"delete"]},IpywidgetsComponentsEnum.Dropdown, className = "w-auto", bind = False)
    keyInput = Utils.get_comp({"placeholder":"enter key name"}, IpywidgetsComponentsEnum.Text, className="w-auto", bind = False)
    loadBtn = Utils.get_comp({"description":"load"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    saveBtn = Utils.get_comp({"description":"save"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    loadContainer = Utils.container([keysOption, loadBtn])
    saveContainer = Utils.container([keyInput, saveBtn])
    loadContainer.hide()
    saveContainer.hide()
    container = Utils.container([loadContainer, saveContainer])
    s = ObjMaker.uisOrganize(locals())
    return s
def HochschuleResultsViewer():
    from timeline.t2024.generic_crud import Main
    from LibsDB import LibsDB
    from timeline.t2024.tailwind.twcrudOps import DictionaryModel
    from jupyterDB import jupyterDB
    af = Main.crud_with_renderer()
    lsc = LoadOrSaveComp()
    cf = af.process.cf
    headers = ['Studiengang', 'link', 'Hochschule', 'Abschluss', 'Studienform', 'Studienort', 'Studientyp']
    struc = {k: {'type': 'Text', 'info': {}, 'order': i} for i, k in enumerate(headers)}
    cf.process.model.process.dicModel.add(["meta", "structure"], struc)
    loadBtn = Utils.get_comp({"description":"loadDataFromClip"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    resetDataBtn = Utils.get_comp({"description":"clear data"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    loadFromFileBtn = Utils.get_comp({"description":"load from file"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    saveToFileBtn = Utils.get_comp({"description":"saveToFile"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    deleteBtn = Utils.get_comp({"description":"delete"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    container = Utils.container([Utils.container([loadBtn, resetDataBtn, loadFromFileBtn, deleteBtn, saveToFileBtn, lsc.views.container]), 
                                 af.views.container], className ="flex flex-column")
    dm = DictionaryModel()
    loc = ["timeline", "2024", "12_Dec", "web-scrap-hochschulecompass"]
    dm.set_file(LibsDB.picklePath("temps"))
    
    def onReset(w):
        cf = s.process.cf
        cf.process.model.handlers.set_data({})
    def onLoadFromClip(w):
        content = jupyterDB.clip().text()
        from htmlDB import htmlDB
        b = htmlDB.getParsedData(content)
        founds = htmlDB.searchOnSoup(dict(tagName="tr", attr= dict(role="row")), b)#len()
        t = []
        for f1 in founds:
            rows = f1.find_all("td")
            r = []
            for i in range(6):
                r.append(rows[i].text)
            r.append(f1["data-link"])
            t.append(r)
        for sg, h,a,sf,so,st,l in t:
            d = {"Studiengang" : sg,
                "Hochschule" : h,
                "Abschluss" : a,
                "Studienform" : sf,
                "Studienort" : so,
                "Studientyp" : st,
                "link" : "https://www.hochschulkompass.de" + l}
            s.process.cf.process.model.handlers.add_data(d)
    def onLoadFromParsedData(w):
        content = s.process.dm.read(s.process.loc)
        lsc = s.process.lsc
        lsc.views.keysOption.outputs.layout.options = list(content.keys())
        lsc.views.loadContainer.show()
        lsc.views.loadBtn.handlers.handle  = s.handlers.onLoadFromFile
        s.process.lsc.views.loadBtn.outputs.layout.description = "load"
    def onLoadFromFile(w):
        lsc = s.process.lsc
        key = lsc.views.keysOption.outputs.layout.value
        vals = s.process.dm.read(loc +[key])
        cf.process.model.handlers.set_data(vals)
        lsc.views.loadContainer.hide()
    def onSaveToFile(w):
        s.process.lsc.views.saveContainer.show()
    def onSave(w):
        lsc = s.process.lsc
        key = lsc.views.keyInput.outputs.layout.value
        s.process.dm.update(loc + [key], cf.process.model.process.dicModel.s.process.model)
        lsc.views.saveContainer.hide()
        lsc.views.keyInput.outputs.layout.value = ""
    def onDeleteIm(w):
        s.handlers.onLoadFromParsedData(w)
        lsc.views.loadBtn.handlers.handle  = s.handlers.onDelete
        s.process.lsc.views.loadBtn.outputs.layout.description = "delete"
    def onDelete(w):
        key = lsc.views.keysOption.outputs.layout.value
        vals = s.process.dm.delete(loc +[key])
        lsc.views.loadContainer.hide()
    lsc.views.saveBtn.handlers.handle  = onSave
    lsc.views.loadBtn.handlers.handle  = onLoadFromFile
    resetDataBtn.handlers.handle = onReset
    loadBtn.handlers.handle = onLoadFromClip
    loadFromFileBtn.handlers.handle = onLoadFromParsedData
    deleteBtn.handlers.handle = onDeleteIm
    saveToFileBtn.handlers.handle = onSaveToFile
    s = ObjMaker.uisOrganize(locals())
    return s