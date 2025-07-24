from timeline.t2024.experiments.morphismWithEvents.morphism import HideableWidget, NameSpace, Parents, Utils, ComponentsLib, IpywidgetsComponentsEnum,BaseComponent, widgets, ValsWrapper
from useful.SerializationDB import SerializationDB
class Main:
    def jsonExplorer():
        je = JSONExplorer()
        je.set_inputs(cssPrefix = "", className="JSONExplorer", comingFrom="JSONExplorer", parentLoc ="")
        je.set_parent_state(Parents())
        je.render()
        je.parents.cssAdder.content = je.parents.globalCSS
        return je
class JSONExplorer(BaseComponent):
    def render(self):
        pre = self.inputs.cssPrefix
        self.outputs.components = NameSpace()
        self.outputs.components.navigation = Utils.get_repeater_omni(comingFrom="Navigation", className="Naviagtion", components= [
            Utils.get_button_omni(comingFrom="Navigation-Menu", className="Menu-items", btnInfo={"icon": "check"}),
            Utils.get_button_omni(comingFrom="Navigation-Menu", className="Menu-items", btnInfo={"icon": "plus"}),
            Utils.get_button_omni(comingFrom="Navigation-Menu", className="Menu-items", btnInfo = {"icon": "edit"}),
            Utils.get_button_omni(comingFrom="Navigation-Menu", className="Menu-items", btnInfo = {"icon": "trash"}),
            Utils.get_button_omni(comingFrom="Navigation-Menu", className="Menu-items", btnInfo = {"icon": "cut"}),
            Utils.get_button_omni(comingFrom="Navigation-Menu", className="Menu-items", btnInfo = {"icon": "copy"}),
            Utils.get_button_omni(comingFrom="Navigation-Menu", className="Menu-items", btnInfo = {"icon": "paste"}),
            Utils.get_button_omni(comingFrom="Navigation-Menu", className="Menu-items", btnInfo = {"icon": "cog"})
        ])
        self.outputs.components.breadCrumb = Utils.makeOmniStructure(comingFrom="breadcrumb", className="breadcrumb", childParamss = {
            "linksArray": [], "cssPrefix": ""}, uiType=ComponentsLib.BreadCrumb)
        self.outputs.components.resultDisplayer = Utils.makeOmniStructure(comingFrom="resultDisplayer", className="resultDisplayer", childParamss = {
            "cssPrefix": ""}, uiType=ComponentsLib.ButtonResultDisplayer)
        self.outputs.components.pagination = Utils.makeOmniStructure(comingFrom="Pagination", className="Pagination", childParamss = {
            "cssPrefix": "asnsn", "selected_button_class_name": "selectedButton"}, uiType=ComponentsLib.Paginator)
        self.outputs.components.outArea = Utils.makeOmniStructure(comingFrom="displayArea", className="DisplayArea", childParamss ={
            "params": ValsWrapper(), "typeOfWidget":IpywidgetsComponentsEnum.Output, "handlersInitializer": None}, uiType=ComponentsLib.Ipywidget)
        bc = Utils.get_repeater_omni(comingFrom="page", className="PageContent", components=[
            Utils.get_label_omni(comingFrom="tile", className="title-header", value="JSON Explorer"),
            Utils.get_repeater_omni(comingFrom="PageBody", className="PageBody", components= [
                self.outputs.components.navigation,
                Utils.get_repeater_omni(comingFrom="PageBodyContent", className="PageBodyContent", components= [
                    self.outputs.components.breadCrumb,
                    self.outputs.components.resultDisplayer,
                    self.outputs.components.pagination,
                    self.outputs.components.outArea
                ])

            ])
        ])
        bc.set_parent_state(self.parents)
        bc.inputs.parent = self
        bc.render()
        self.outputs.localCss = f"""
        .PageContent{pre}{{
            width: 50%;
            min-height: 400px;
            max-height: 600px;
            flex-direction: column;
            border: 1px solid gray;
            overflow: auto;
        }}
        .title-header{pre}{{
            font-size: 2rem;
            min-height: 3rem;
            border-bottom: 1px solid gray;
            align-items: center;
            margin: 0;
            padding-left: 2rem;

        }}
        .Menu-items{pre}{{
            min-height: 3rem;
            font-size: 2rem;
            color: #86A7FC;
            border-radius: 2px;
            background-color: unset;
            width: unset;
        }}
        .Naviagtion{pre}{{
            flex-direction: column;
            border-right: 1px solid gray;
            min-width: fit-content;
            max-width: fit-content;
            overflow: auto;
            flex: 1;
            height: unset;
            /*position: sticky;
            top:0;*/
        }}
        .PageBody{pre}{{
            overflow: auto;
            flex: 1;
        }}
        .PageBodyContent{pre}{{
            flex-direction: column;
            padding-left: 10px;
        }}
        .DisplayArea{pre}{{
            /*max-height: 200px;*/
            overflow: auto;
        }}
        .{self.inputs.selected_menu_name}{{
            background-color: #007bff;
            color: white;
        }}
        """
        self.parents.globalCSS += self.outputs.localCss
        self.outputs.layout = bc.outputs.layout
        self.outputs.instance = bc
    def update_layout(self):
        pass # does need to update thiss
class CreateNewKeyPage(BaseComponent):
    def render(self):
        valueTypeOptions = ["int", "float", "boolean", "var", "empty list", "empty dict", "largeText", "text"]
        self.outputs.components = NameSpace()
        self.outputs.components.keyname = Utils.get_ipy_omni("keyName", "InputText", {"description": "key name", "continuous_update":False}, IpywidgetsComponentsEnum.Text)
        self.outputs.components.valueType = Utils.get_ipy_omni("valueType", "typeOfValue", {"description":"select a value type", "options": valueTypeOptions, "value": "text"},
                                                             IpywidgetsComponentsEnum.Dropdown)
        self.outputs.components.valueTextArea = Utils.get_ipy_omni("valueTextArea", "valueSectionTextArea", {"description":"value", "continuous_update":False},
                                                                   IpywidgetsComponentsEnum.Textarea)
        self.outputs.components.valueText = Utils.get_ipy_omni("valueText", "valueSectionText", {"description":"value", "continuous_update":False}, IpywidgetsComponentsEnum.Text)
        self.outputs.components.valueBoolean = Utils.get_ipy_omni("valueBoolean", "valueBoolean", {"description":"value"}, IpywidgetsComponentsEnum.Checkbox)
        self.outputs.components.valueInt = Utils.get_ipy_omni("valueInt", "valueInt", {"description":"value"}, IpywidgetsComponentsEnum.IntText)
        self.outputs.components.valueFloat = Utils.get_ipy_omni("valueFloat", "valueFloat", {"description":"value"}, IpywidgetsComponentsEnum.FloatText)
        self.outputs.components.btns = Utils.get_repeater_omni(comingFrom="ButtonInCreate", className="BtnsSection", components= [
            Utils.get_button_omni("CancelBtn", "CancelBtn", {"description":"cancel"}),
            Utils.get_button_omni("SaveBtn", "SaveBtn", {"description":"save"})])
        cnk = Utils.get_repeater_omni(comingFrom="CreateNewKey", className="CreateNewKey", components= [
            self.outputs.components.keyname,
            self.outputs.components.valueType,
            self.outputs.components.valueTextArea,
            self.outputs.components.valueText,
            self.outputs.components.valueBoolean,
            self.outputs.components.valueInt,
            self.outputs.components.valueFloat,
            self.outputs.components.btns,
            Utils.get_ipy_omni("OutputArea", "displayArea", {}, IpywidgetsComponentsEnum.Output),
        ])
        cnk.set_parent_state(self.parents)
        cnk.render()
        cnk.inputs.parent = self
        self.outputs.layout = cnk.outputs.layout
        self.outputs.instance = cnk
        self.outputs.components.valueComponent = self.outputs.components.valueText.outputs.layout
        self.outputs.localCss = """
            .CreateNewKey{
                flex-direction: column;
            }
            .SaveBtn, .CancelBtn{
                width: fit-content;
            }
            .BtnsSection{
                width: inherit;
                justify-content: flex-end;
            }
            .CancelBtn{
                margin-right: 4rem;
                background-color: #f8f9fa;
            }

            .valueSectionTextArea{
                width: auto;
                flex-grow: unset;
            }

            """
        self.parents.globalCSS += self.outputs.localCss
    def _hideValueInputs(self):
        HideableWidget.hideIt(self.outputs.components.valueTextArea.outputs.layout)
        HideableWidget.hideIt(self.outputs.components.valueBoolean.outputs.layout)
        HideableWidget.hideIt(self.outputs.components.valueText.outputs.layout)
        HideableWidget.hideIt(self.outputs.components.valueInt.outputs.layout)
        HideableWidget.hideIt(self.outputs.components.valueFloat.outputs.layout)
    def set_up(self):
        self._hideValueInputs()
        HideableWidget.showIt(self.outputs.components.valueText.outputs.layout)
    def get_default_handler(self):
        return self._default_handler
    def _default_handler(self, payload):
        if (payload.inputs.comingFrom != "valueType"):
            return
        self._hideValueInputs()
        p = self.outputs.components.valueText.outputs.layout
        if payload.outputs.layout.value in ["text", "var"]:
            p = self.outputs.components.valueText.outputs.layout
            HideableWidget.showIt(self.outputs.components.valueText.outputs.layout)
        elif payload.outputs.layout.value == "largeText":
            p = self.outputs.components.valueTextArea.outputs.layout
            HideableWidget.showIt(self.outputs.components.valueTextArea.outputs.layout)
        elif payload.outputs.layout.value == "boolean":
            p = self.outputs.components.valueBoolean.outputs.layout
            HideableWidget.showIt(self.outputs.components.valueBoolean.outputs.layout)
        elif payload.outputs.layout.value == "int":
            p = self.outputs.components.valueInt.outputs.layout
            HideableWidget.showIt(self.outputs.components.valueInt.outputs.layout)
        elif payload.outputs.layout.value == "float":
            p = self.outputs.components.valueFloat.outputs.layout
            HideableWidget.showIt(self.outputs.components.valueFloat.outputs.layout)

        self.outputs.components.valueComponent = p

def firstRender():
    vals = stateManager.model.helper.readAll()
    stateManager.results.data=list(vals.keys())
    stateManager.results.dataLen = len(stateManager.results.data)
    HideableWidget.hideIt(je.outputs.components.breadCrumb.outputs.layout)
    btns = je.outputs.components.resultDisplayer.outputs.instance.outputs.components.btns
    for i in range(len(btns)):
        if i < stateManager.results.dataLen:
            btns[i].outputs.layout.description = stateManager.results.data[i]
        else:
            btns[i].outputs.instance.hide()
    if len(stateManager.breadCrumb.values) == 0:
        HideableWidget.hideIt(je.outputs.components.resultDisplayer.outputs.instance.outputs.components.backButton.outputs.layout)
    stateManager.pagination.pageCount = (stateManager.results.dataLen // stateManager.pagination.pageSize) + 1
    if stateManager.pagination.pageCount <= 1:
        HideableWidget.hideIt(je.outputs.components.pagination.outputs.layout)


# ------------------------------


import math

def selectBtnWithNumber(val):
    stateManager.pagination.currentPageNr = val
    if stateManager.pagination.currentSelected:
        pNr = int(stateManager.pagination.currentSelected.description)
    updatePaginationButtons()
    if stateManager.pagination.currentSelected:
        if pNr == stateManager.pagination.currentPageNr:
            return
        stateManager.pagination.currentSelected.remove_class(je.outputs.components.pagination.outputs.instance.inputs.selected_button_class_name)
    for btn in je.outputs.components.pagination.outputs.instance.outputs.components.btns:
        if int(btn.outputs.layout.description) == val:
            stateManager.pagination.currentSelected = btn.outputs.layout
            stateManager.pagination.currentSelected.add_class(je.outputs.components.pagination.outputs.instance.inputs.selected_button_class_name)
            break
    renderResults(get_data_for_currentPage())
    selectSelections()
def printer_wrapper(payload):
    printer(payload)
def printer(payload):
    location = payload.get_this_location()
    stateManager.debug.payload = payload
    name = payload.inputs.comingFrom
    stateManager.debug.payload = payload
    outAreaLocation = je.outputs.components.outArea.outputs.instance.get_this_location()
    # print(location,location[:len(outAreaLocation)])
    if (location[:len(outAreaLocation)] != outAreaLocation):
        je.outputs.components.outArea.outputs.layout.clear_output()
        with je.outputs.components.outArea.outputs.layout:
            if name == "paginationButton":
                val = int(payload.outputs.layout.description)
                selectBtnWithNumber(val)
            elif name == "gotoButtonPagination":
                selectBtnWithNumber(je.outputs.components.pagination.outputs.instance.outputs.components.gotoInput.outputs.layout.value)
            elif name == "nextButtonPagination":
                nex = int(stateManager.pagination.currentSelected.description) + 1
                if nex > stateManager.pagination.pageCount:
                    nex = 1
                selectBtnWithNumber(nex)
            elif name == "gobackButtonPagination":
                prev = int(stateManager.pagination.currentSelected.description) - 1
                if prev < 1:
                    prev = stateManager.pagination.pageCount
                selectBtnWithNumber(prev)
            elif name == "Navigation-Menu":
                if stateManager.navigation.currentSelected:
                    stateManager.navigation.currentSelected.remove_class(je.inputs.selected_menu_name)
                    if stateManager.navigation.currentSelected.icon == "check":
                        unselectSelections()
                        showAllNavs()
                if isThisNavigationSelected(payload) and stateManager.navigation.currentSelected:
                    if payload.inputs.params["icon"] in ["plus", "edit", "cog"]:
                        displayBodyArea()
                    elif payload.inputs.params["icon"] == "check":
                        unselectSelections()
                    stateManager.navigation.currentSelected = None
                    return
                stateManager.navigation.currentSelected = payload.outputs.layout
                if stateManager.navigation.currentSelected.icon == "check":
                    showNavForSelections()
                stateManager.navigation.currentSelected.add_class(je.inputs.selected_menu_name)
                navigationSelected(payload)
            elif name == "searched-item":
                if stateManager.navigation.currentSelected is None:
                    key = stateManager.results.data[payload.inputs.parent.inputs.index]
                    content = stateManager.model.helper.read(key)
                    if type(content) == dict:
                        stateManager.model.loc.append(key)
                        stateManager.model.helper.set_baseloc(stateManager.model.loc)
                        renderResultsAndPagination()
                        je.outputs.components.breadCrumb.outputs.instance.append(key)
                    else:
                        print(content)
                elif stateManager.navigation.currentSelected.icon == "trash":
                    stateManager.pages.list.confirmDialog.inputs.parent = je.outputs.components.outArea.outputs.instance
                    stateManager.pages.list.createPage.instance.outputs.components.btns.inputs.parent = stateManager.pages.list.confirmDialog
                    je.outputs.components.outArea.outputs.layout.clear_output()
                    stateManager.pages.list.confirmDialogState.lastClicked = payload
                    display(stateManager.pages.list.confirmDialog.outputs.layout)
                    display(stateManager.pages.list.outAreaForPages)
                elif stateManager.navigation.currentSelected.icon == "edit":
                    stateManager.results.lastSelected = payload
                    HideableWidget.hideIt(je.outputs.components.breadCrumb.outputs.layout)
                    HideableWidget.hideIt(je.outputs.components.pagination.outputs.layout)
                    HideableWidget.hideIt(je.outputs.components.resultDisplayer.outputs.layout)
                    stateManager.pages.list.editPage.instance.inputs.parent = je.outputs.components.outArea.outputs.instance
                    stateManager.pages.list.editPage.instance.inputs.comingFrom = "editPage"
                    updateEditPage(payload)
                    with je.outputs.components.outArea.outputs.layout:
                        display(stateManager.pages.list.editPage.instance.outputs.layout)
                        display(stateManager.pages.list.outAreaForPages)
                elif stateManager.navigation.currentSelected.icon == "check":
                    if payload.outputs.layout.description in stateManager.results.selections.selected:
                        payload.outputs.layout.remove_class("SearchResultsSearchedItemSelected")
                        stateManager.results.selections.selected.remove(payload.outputs.layout.description)
                    else:
                        stateManager.results.selections.selected.add(payload.outputs.layout.description)
                        payload.outputs.layout.add_class("SearchResultsSearchedItemSelected")
            elif name == "backButton":
                if len(stateManager.model.loc) > 0:
                    stateManager.model.loc.pop()
                    renderResultsAndPagination()
                    je.outputs.components.breadCrumb.outputs.instance.pop()
            elif name == "bread-crumb-item":
                for i in range(je.outputs.components.breadCrumb.outputs.instance.outputs.count - payload.inputs.parent.index- 1):
                    je.outputs.components.breadCrumb.outputs.instance.pop()
                    stateManager.model.loc.pop()
                renderResultsAndPagination()
            else:
                stateManager.debug.payload = payload
                print(payload.outputs.__dict__,  name)
    else:
        createPageLoc = ""
        createPageLoc = stateManager.pages.list.createPage.instance.get_this_location()
        defaultBinder(stateManager.pages.list.editPage, payload)

        if location[:len(createPageLoc)] == createPageLoc:
            stateManager.pages.list.outAreaForPages.clear_output()
            with stateManager.pages.list.outAreaForPages:
                print(payload.inputs.__dict__)
                stateManager.pages.list.createPage.handler(payload)
                create_page_handler(payload)
        elif location == '/page/PageBody/PageBodyContent/displayArea/Confirm Dialog/ButtonInCreate/SaveBtn': # deleting the key
            with stateManager.pages.list.outAreaForPages:
                stateManager.model.helper.delete(stateManager.results.data[stateManager.pages.list.confirmDialogState.lastClicked.inputs.parent.inputs.index])
                HideableWidget.hideIt(stateManager.pages.list.confirmDialogState.lastClicked.outputs.layout)

                displayBodyArea()
                unsetNavAndClearOutput()
                renderResultsAndPagination()
        elif location in ['/page/PageBody/PageBodyContent/displayArea/Confirm Dialog/ButtonInCreate/CancelBtn', 
                          '/page/PageBody/PageBodyContent/displayArea/editPage/CreateNewKey/ButtonInCreate/CancelBtn',
                         '/page/PageBody/PageBodyContent/displayArea/settingPage/ButtonInCreate/CancelBtn']:
            displayBodyArea()
            unsetNavAndClearOutput()
        elif location == '/page/PageBody/PageBodyContent/displayArea/editPage/CreateNewKey/ButtonInCreate/updateBtn':
            key = stateManager.pages.list.editPage.instance.outputs.components.keyname.outputs.layout.value
            value = stateManager.pages.list.editPage.instance.outputs.components.valueComponent.value
            typ = stateManager.pages.list.editPage.instance.outputs.components.valueType.outputs.layout.value
            addKey(key, value, typ, True)
        elif location == '/page/PageBody/PageBodyContent/displayArea/settingPage/ButtonInCreate/SaveBtn': # save for setting page
            comp1 = stateManager.pages.list.settingPage.outputs.instance.outputs.renderedStates[0].outputs.instance.outputs.renderedStates[0]
            stateManager.pagination.pageSize = comp1.outputs.layout.value
            displayBodyArea()
            unsetNavAndClearOutput()
            renderResultsAndPagination()
            selectBtnWithNumber(1)
        else:
            stateManager.pages.list.outAreaForPages.clear_output()
            with stateManager.pages.list.outAreaForPages:
                print(payload.inputs.__dict__)
def unsetNavAndClearOutput():
    stateManager.navigation.currentSelected.remove_class(je.inputs.selected_menu_name)
    stateManager.navigation.currentSelected = None
    stateManager.pages.list.outAreaForPages.clear_output()
def displayBodyArea():
    je.outputs.components.outArea.outputs.layout.clear_output()
    HideableWidget.showIt(je.outputs.components.breadCrumb.outputs.layout)
    HideableWidget.showIt(je.outputs.components.pagination.outputs.layout)
    HideableWidget.showIt(je.outputs.components.resultDisplayer.outputs.layout)
def isThisNavigationSelected(payload):
    return stateManager.navigation.currentSelected == payload.outputs.layout
def navigationSelected(payload):
    iconType = payload.inputs.params["icon"]
    displayBodyArea()
    if iconType == "check":
        pass
    elif iconType == "plus":
        HideableWidget.hideIt(je.outputs.components.breadCrumb.outputs.layout)
        HideableWidget.hideIt(je.outputs.components.pagination.outputs.layout)
        HideableWidget.hideIt(je.outputs.components.resultDisplayer.outputs.layout)
        stateManager.pages.list.createPage.instance.set_inputs(parent=je.outputs.components.outArea.outputs.instance, comingFrom="createPage")
        stateManager.pages.list.createPage.instance.outputs.components.btns.inputs.parent = stateManager.pages.list.createPage.instance
        with je.outputs.components.outArea.outputs.layout:
            display(stateManager.pages.list.createPage.instance.outputs.layout)
            display(stateManager.pages.list.outAreaForPages)
    elif iconType == "cog":
        HideableWidget.hideIt(je.outputs.components.breadCrumb.outputs.layout)
        HideableWidget.hideIt(je.outputs.components.pagination.outputs.layout)
        HideableWidget.hideIt(je.outputs.components.resultDisplayer.outputs.layout)
        stateManager.pages.list.settingPage.set_inputs(parent=je.outputs.components.outArea.outputs.instance, comingFrom="settingPage")
        stateManager.pages.list.createPage.instance.outputs.components.btns.inputs.parent = stateManager.pages.list.settingPage
        with je.outputs.components.outArea.outputs.layout:
            display(stateManager.pages.list.settingPage.outputs.layout)
            display(stateManager.pages.list.outAreaForPages)
def renderResultsAndPagination():
    stateManager.results.data = list(stateManager.model.helper.readAll().keys())
    
    # stateManager.pagination.currentPageNr = 1
    updatePaginationButtons()
    renderResults(get_data_for_currentPage())
    if len(stateManager.results.data) < stateManager.pagination.pageSize:
        HideableWidget.hideIt(je.outputs.components.pagination.outputs.layout)
    else:
        HideableWidget.showIt(je.outputs.components.pagination.outputs.layout)
def renderResults(data):
    for i, btn in enumerate(je.outputs.components.resultDisplayer.outputs.instance.outputs.components.btns):
        if i < len(data):
            btn.inputs.index, btn.outputs.layout.description = data[i]
            HideableWidget.showIt(btn.outputs.layout)
        else:
            HideableWidget.hideIt(btn.outputs.layout)
def get_data_for_currentPage():
    res = []
    fromStart = stateManager.pagination.pageSize * (stateManager.pagination.currentPageNr-1)
    till = stateManager.pagination.pageSize * (stateManager.pagination.currentPageNr)
    for i in range(fromStart, till):
        if i >= len(stateManager.results.data):
            break
        res.append((i, stateManager.results.data[i]))
    return res
def create_page_handler(payload):
    if payload.inputs.params["description"] == "cancel":
        displayBodyArea()
        unsetNavAndClearOutput()
    elif payload.inputs.params["description"] == "save":
        key = stateManager.pages.list.createPage.instance.outputs.components.keyname.outputs.layout.value
        value = stateManager.pages.list.createPage.instance.outputs.components.valueComponent.value
        # if stateManager.model.helper.exists(key):
        #     print("key already exists please select override options")
        #     return
        typ = stateManager.pages.list.createPage.instance.outputs.components.valueType.outputs.layout.value
        addKey(key, value, typ)
        renderResultsAndPagination()
def addKey(key, value, typ, override=False):
    if typ == 'empty list':
        value =  []
    elif typ == 'empty dict':
        value = {}
    elif typ == "var":
        value = stateManager.model.variableStates[value]
    if key == "":
        raise IOError("Cant create key with empty string")
    stateManager.model.helper.write(key, value, override)
    displayBodyArea()
    stateManager.navigation.currentSelected.remove_class(je.inputs.selected_menu_name)
    stateManager.navigation.currentSelected = None
    renderResultsAndPagination()
def defaultBinder(comp, payload):
    try:
        comp_loc = comp.instance.get_this_location()
        location = payload.get_this_location()
        if location[:len(comp_loc)] == comp_loc:
            comp.handler(payload)
    except:
        pass
def updateEditPage(payload):
    key = stateManager.results.data[stateManager.results.lastSelected.inputs.parent.inputs.index]
    value = stateManager.model.helper.read(stateManager.results.data[stateManager.results.lastSelected.inputs.parent.inputs.index])
    stateManager.pages.list.editPage.instance.outputs.components.keyname.outputs.layout.value = key
    stateManager.pages.list.editPage.instance.outputs.components.keyname.outputs.layout.disabled = True
    if type(value) == int:
        stateManager.pages.list.editPage.instance.outputs.components.valueType.outputs.layout.value = "int"
        stateManager.pages.list.editPage.instance.outputs.components.valueInt.outputs.layout.value = value
    elif type(value) == dict:
        stateManager.pages.list.editPage.instance.outputs.components.valueType.outputs.layout.value = "empty dict"
        stateManager.pages.list.outAreaForPages.clear_output()
        with stateManager.pages.list.outAreaForPages:
            print(value)
            print("Value will be overriden with empty dict if you update")
    elif type(value) == list:
        stateManager.pages.list.editPage.instance.outputs.components.valueType.outputs.layout.value = "empty list"
        stateManager.pages.list.outAreaForPages.clear_output()
        with stateManager.pages.list.outAreaForPages:
            print(value)
            print("Value will be overriden with empty list if you update")
    elif type(value) == float:
        stateManager.pages.list.editPage.instance.outputs.components.valueType.outputs.layout.value = "float"
        stateManager.pages.list.editPage.instance.outputs.components.valueFloat.outputs.layout.value = value
    elif type(value) == bool:
        stateManager.pages.list.editPage.instance.outputs.components.valueType.outputs.layout.value = "float"
        stateManager.pages.list.editPage.instance.outputs.components.valueBoolean.outputs.layout.value = value
    elif type(value) == str and "\n" not in value: # text
        stateManager.pages.list.editPage.instance.outputs.components.valueType.outputs.layout.value = "text"
        stateManager.pages.list.editPage.instance.outputs.components.valueText.outputs.layout.value = value
    elif type(value) == str and "\n" in value: # textarea
        stateManager.pages.list.editPage.instance.outputs.components.valueType.outputs.layout.value = "text"
        stateManager.pages.list.editPage.instance.outputs.components.valueText.outputs.layout.value = value
def updatePaginationButtons():
    stateManager.pagination.pageCount  = math.ceil(len(stateManager.results.data) / stateManager.pagination.pageSize)
    btnDescrs = getButtonIndices(stateManager.pagination.currentPageNr + 1)
    for i, btn in enumerate(je.outputs.components.pagination.outputs.instance.outputs.components.btns):
        if i < len(btnDescrs):
            btn.outputs.layout.description = str(btnDescrs[i])
            HideableWidget.showIt(btn.outputs.layout)
        else:
            HideableWidget.hideIt(btn.outputs.layout)
def getButtonIndices(currentPageNr):
    n = stateManager.pagination.pageCount
    if(n < 6):
        return list(range(1, n+1))
    if(currentPageNr < 4):
        return [1,2,3,4,5]
    if(currentPageNr >= (n -2)):
        return [n-4, n-3,n-2,n-1,n]
    return [currentPageNr-2, currentPageNr-1, currentPageNr, currentPageNr+1, currentPageNr+2]
def selectSelections():
    for i, btn in enumerate(je.outputs.components.resultDisplayer.outputs.instance.outputs.components.btns):
        if btn.outputs.layout.description in stateManager.results.selections.selected:
            btn.outputs.layout.add_class("SearchResultsSearchedItemSelected")
        else:
            btn.outputs.layout.remove_class("SearchResultsSearchedItemSelected")
def unselectSelections():
    for i, btn in enumerate(je.outputs.components.resultDisplayer.outputs.instance.outputs.components.btns):
        if btn.outputs.layout.description in stateManager.results.selections.selected:
            btn.outputs.layout.remove_class("SearchResultsSearchedItemSelected")
    stateManager.results.selections.selected.clear()
def showNavForSelections():
    for navOmni in je.outputs.components.navigation.outputs.instance.outputs.renderedStates:
        lay = navOmni.outputs.instance.outputs.layout
        if lay.icon not in ["trash", "cut", "copy", "check"]:
            HideableWidget.hideIt(lay)
def showAllNavs():
    for navOmni in je.outputs.components.navigation.outputs.instance.outputs.renderedStates:
        lay = navOmni.outputs.instance.outputs.layout
        HideableWidget.showIt(lay)

# ---------------

from timeline.t2024.experiments.namespace_generic_logger import DictionaryCRUD
stateManager = NameSpace()
stateManager.pagination = NameSpace()
stateManager.pagination.currentSelected = None
stateManager.pagination.pageCount = 0
stateManager.pagination.currentPageNr = 0
stateManager.pagination.pageSize = 20
stateManager.model = NameSpace()
stateManager.model.data = SerializationDB.readPickle("../../2024/02_Feb/pagination.pkl")
stateManager.model.loc = []
stateManager.model.helper = DictionaryCRUD()
stateManager.model.helper.set_dictionary(stateManager.model.data)
stateManager.navigation = NameSpace()
stateManager.navigation.currentSelected = None
stateManager.breadCrumb = NameSpace()
stateManager.breadCrumb.values = []
stateManager.pages = NameSpace()
stateManager.pages.name = ""
stateManager.pages.list = NameSpace()
stateManager.results = NameSpace()
stateManager.debug = NameSpace()
stateManager.pages.list.outAreaForPages = widgets.Output()
stateManager.model.variableStates ={}
stateManager.pages.list.confirmDialogState = NameSpace()


parent = Parents()
cnkp = CreateNewKeyPage()
cnkp.set_parent_state(parent)
cnkp.render()
cnkp.parents.cssAdder.content = cnkp.parents.globalCSS
cnkp.set_up()
stateManager.pages.list.createPage = NameSpace()
stateManager.pages.list.createPage.instance = cnkp
stateManager.pages.list.createPage.handler = cnkp.get_default_handler()

enkp = CreateNewKeyPage()
enkp.set_parent_state(parent)
enkp.set_inputs(comingFrom = "edit field", className="EditPage")
enkp.render()
enkp.parents.cssAdder.content = enkp.parents.globalCSS
enkp.set_up()
stateManager.pages.list.editPage = NameSpace()
stateManager.pages.list.editPage.instance = enkp
stateManager.pages.list.editPage.handler = enkp.get_default_handler()
stateManager.pages.list.editPage.instance.outputs.components.btns.outputs.instance.outputs.renderedStates[1].outputs.layout.description = "update"
stateManager.pages.list.editPage.instance.outputs.components.btns.outputs.instance.outputs.renderedStates[1].outputs.instance.inputs.comingFrom = "updateBtn"

stateManager.pages.list.confirmDialog = Utils.get_repeater_omni("Confirm Dialog", "ConfirmationDialog", [
    Utils.get_label_omni("ConfirmHeader", "title-header", "Do you really want to delete it?"),
    stateManager.pages.list.createPage.instance.outputs.components.btns])
stateManager.pages.list.confirmDialog.set_parent_state(parent)
stateManager.pages.list.confirmDialog.render()
stateManager.pages.list.confirmDialog.outputs.localCSS = """
.ConfirmationDialog{
    flex-direction: column;
}

"""
stateManager.pages.list.confirmDialog.get_this_location = lambda : BaseComponent.get_this_location(stateManager.pages.list.confirmDialog)

stateManager.pages.list.settingPage = Utils.get_repeater_omni("SettingPage", "SettingPage", [
    Utils.get_repeater_omni("ParameterSettingGroup", "ParameterSettingGroup", [
        Utils.get_ipy_omni("ResultDisplaySize", "ResultDisplaySize", 
                           widgetInfo= {"description": "result display size", "tooltip":"result display size","max": 20, "min": 5}, 
                           typ=IpywidgetsComponentsEnum.BoundedIntText)
    ]),
    stateManager.pages.list.createPage.instance.outputs.components.btns])
stateManager.pages.list.settingPage.set_parent_state(parent)
stateManager.pages.list.settingPage.render()
stateManager.pages.list.settingPage.outputs.localCSS = """
.SettingPage{
    flex-direction: column;
}
.ParameterSettingGroup{
    flex: 1
}

"""
stateManager.pages.list.settingPage.get_this_location = lambda : BaseComponent.get_this_location(stateManager.pages.list.settingPage)
stateManager.results.selections = NameSpace()
stateManager.results.selections.selected = set()



je = JSONExplorer()
je.set_parent_state(parent)
je.set_inputs(cssPrefix = "", parentLoc="", selected_menu_name="selected_menu", comingFrom="")

je.render()
je.parents.cssAdder.content = je.parents.globalCSS
je.parents.cssAdder.content += stateManager.pages.list.confirmDialog.outputs.localCSS
je.outputs.components.pagination.outputs.instance.outputs.components.gotoInput.outputs.instance.inputs.params = {"min": 1, "max": 5}
je.outputs.components.pagination.outputs.instance.outputs.components.gotoInput.outputs.instance.update_layout()
renderResultsAndPagination()
parent.cssAdder.content += """
.SearchResultsSearchedItemSelected{
    border: 1px dotted;
    background-color: #c1c1c1;
}

"""
stateManager.pages.list.createPage.instance.set_inputs(parent=je.outputs.components.outArea.outputs.instance, comingFrom="createPage")
je.outputs.layout
