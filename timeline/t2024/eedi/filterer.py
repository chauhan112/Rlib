from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from useful.basic import Main as ObjMaker
from timeline.t2024.osExplorer import OSExplorer
from timeline.t2024.ListResultDisplayer import ListResultDisplayer
from jupyterDB import jupyterDB
from SerializationDB import SerializationDB

def MisConceptsFilterer():
    lrd = ListResultDisplayer()
    lrd.handlers.set_up()
    lrd.handlers.labelFunc = lambda x: x[1]
    oe = lrd.process.exp
    oe.views.outputDisplayer.outputs.layout.remove_class("h-600px")
    oe.views.outputDisplayer.outputs.layout.add_class("h-max-600px")
    oe.views.title.outputs.layout.value = "misconceptions filter"
    lrd.process.title = oe.views.title.outputs.layout.value
    oe.views.filterSearch.outputs.layout.add_class("w-100")
    oe.views.location.hide()
    oe.views.filterSearch.outputs.layout.remove_class("w-auto")
    oe.views.filterSearch.outputs.layout.add_class("p0")
    misconceptions = jupyterDB._params["eedi"].process.mis_map.values.tolist()
    oe.process.mainList = misconceptions
    oe.process.filteredList = oe.process.mainList.copy()
    oe.process.filterByText = []
    oe.process.toRemoveId = []
    oe.views.container.outputs.layout
    removeBtn = Utils.get_comp({"description":"remove"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    filteredPrint = Utils.get_comp({"description":"allFiltered"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    filterOut = Utils.get_comp({"description":"filterOut"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    while len(oe.views.buttons.outputs.renderedStates) > 1:
        oe.views.buttons.pop()
    oe.views.buttons.append(removeBtn)
    oe.views.buttons.append(filteredPrint)
    oe.views.buttons.append(filterOut)

    def getOptions(filteredList):
        trSize = 90
        newList = []
        for k,v in filteredList:
            if len(v) > trSize:
                newList.append([v[:trSize] + "...", k])
            else:
                newList.append([v, k])
        return newList
    def getValue(index, allData):
        for k, val in allData:
            if k == index:
                return val
        return ""
    def render():
        s.process.lrd.handlers.set_all_options(s.handlers.getOptions(oe.process.filteredList))
    def onReset(w):
        oe.process.toRemoveId = []
        oe.process.filteredList = oe.process.mainList.copy()
        oe.views.filterSearch.outputs.layout.value = ""
        s.handlers.onFilterOut(1)
        s.handlers.render()
    def folderSelected(val):
        pass
    def fileSelected(val):
        oe.views.outputDisplayer.outputs.layout.clear_output()
        with oe.views.outputDisplayer.outputs.layout:
            print(getValue(val, oe.process.mainList))
    def onFilterOut(w):
        newList = []
        wordsFilter = list(filter(lambda x: x != "", oe.views.filterSearch.outputs.layout.value.split(",")))
        wordsFilter = list(map(lambda x: x.strip().lower(), wordsFilter))
        for k, v in oe.process.filteredList:
            found = False
            if k in oe.process.toRemoveId:
                continue
            if len(wordsFilter) == 0:
                found = True
            valLower = v.lower()
            for w in wordsFilter:
                if w in valLower:
                    found = True
                    break
            if found:
                newList.append([k,v])
        oe.process.filteredList = newList
        render()
    def onRemove(w):
        oe.process.toRemoveId.append(oe.views.lister.outputs.layout.value)
        onFilterOut(1)
        render()
    def onPrint(w):
        oe.views.outputDisplayer.outputs.layout.clear_output()
        with oe.views.outputDisplayer.outputs.layout:
            print(oe.process.filteredList)
    oe.views.buttons.outputs.renderedStates[0].outputs.layout.description = "reset list"
    oe.views.buttons.outputs.renderedStates[0].handlers.handle = onReset
    oe.handlers.fileSelected = fileSelected
    oe.views.filterSearch.handlers.handle = lambda x: x
    removeBtn.handlers.handle = onRemove
    filteredPrint.handlers.handle = onPrint
    filterOut.handlers.handle = onFilterOut
    container = oe.views.container
    s = ObjMaker.uisOrganize(locals())
    render()
    return s