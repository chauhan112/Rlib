from timeline.t2024.experiments.morphism.withCIT.morphismWithCIT import BaseComponent, GlobalStructure, NameSpace, Utils, ComponentsLib, IpywidgetsComponentsEnum, HideableWidget, widgets
import logging
import math
from timeline.t2024.experiments.namespace_generic_logger import DictionaryCRUD
from timeline.t2023.dep_extractor.dependency_extractor import DicOps as DO
from ListDB import ListDB
import copy

class JSONExplorerView(BaseComponent):
    def render(self):
        self.state.css = NameSpace()
        self.state.css.menuName = "menu-item"
        pre = self.inputs.cssPrefix
        self.outputs.components = NameSpace()
        self.outputs.components.navigation = Utils.get_repeater_omni( className="Naviagtion", comps= [
            Utils.get_button_omni(self.state.css.menuName, btnInfo={"icon": "check"}),
            Utils.get_button_omni(self.state.css.menuName, btnInfo={"icon": "plus"}),
            Utils.get_button_omni(self.state.css.menuName, btnInfo = {"icon": "edit"}),
            Utils.get_button_omni(self.state.css.menuName, btnInfo = {"icon": "trash"}),
            Utils.get_button_omni(self.state.css.menuName, btnInfo = {"icon": "cut"}),
            Utils.get_button_omni(self.state.css.menuName, btnInfo = {"icon": "copy"}),
            Utils.get_button_omni(self.state.css.menuName, btnInfo = {"icon": "paste"}),
            Utils.get_button_omni(self.state.css.menuName, btnInfo = {"icon": "cog"})
        ], comingFrom="menu")
        self.outputs.components.breadCrumb = Utils.get_omni_component( className="breadcrumb", comingFrom="breadcrumb", childParams = {
            "linksArray": [], "cssPrefix": ""}, uiType=ComponentsLib.BreadCrumb)
        self.outputs.components.resultDisplayer = Utils.get_omni_component("resultDisplayer", "resultDisplayer", {"className": "resultDisplayer"},
                                                                           uiType=ComponentsLib.ButtonResultDisplayer)

        self.outputs.components.pagination = Utils.get_omni_component( "Pagination", "Pagination", childParams = {
            "cssPrefix": "asnsn", "selected_button_class_name": "selectedButton"}, uiType=ComponentsLib.Paginator)
        self.outputs.components.outArea = Utils.get_omni_component(className="DisplayArea",comingFrom="DisplayArea", childParams ={
            "params": {}, "typeOfWidget":IpywidgetsComponentsEnum.Output}, uiType=ComponentsLib.Ipywidget)
        bc = Utils.get_repeater_omni(className="PageContent", comps=[
            Utils.get_ipy_omni( "title-header", {"value":"JSON Explorer"}, IpywidgetsComponentsEnum.Label),
            Utils.get_repeater_omni(className="PageBody", comps= [
                self.outputs.components.navigation,
                Utils.get_repeater_omni(className="PageBodyContent", comps= [
                    self.outputs.components.breadCrumb,
                    self.outputs.components.resultDisplayer,
                    self.outputs.components.pagination,
                    self.outputs.components.outArea
                ])

            ])
        ])
        bc.set_global_state(self.gstate)
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
        .{self.state.css.menuName}{pre}{{
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
        self.gstate.cssManager.add(self.get_location(), self.outputs.localCss)
        self.outputs.layout = bc.outputs.layout
        self.outputs.instance = bc
    def update_layout(self):
        pass # does need to update thiss
class JSONController:
    def set_view(self, view):
        self.view = view
    def set_state(self, state):
        self.state = state
    def emptyDisplayArea(self):
        jsonExp = self.view
        HideableWidget.hideIt(jsonExp.outputs.components.breadCrumb.outputs.layout)
        HideableWidget.hideIt(jsonExp.outputs.components.pagination.outputs.layout)
        HideableWidget.hideIt(jsonExp.outputs.components.resultDisplayer.outputs.layout)
    def pageNrHandler(self, nr):
        jsonExp = self.view
        jsonExp.gstate.logger.log(logging.DEBUG, "pageNrHandler")
        jsonExp.outputs.components.resultDisplayer.outputs.instance.state.pageNr = nr
        jsonExp.outputs.components.resultDisplayer.outputs.instance.update()
    def update_results_and_pagination(self, results: list):
        jsonExp = self.view
        jsonExp.outputs.components.resultDisplayer.outputs.instance.set_data(results)
        jsonExp.outputs.components.resultDisplayer.outputs.instance.update()
        maxPages = jsonExp.outputs.components.resultDisplayer.outputs.instance.state.totalPages
        if maxPages not in [0,1]:
            HideableWidget.showIt(jsonExp.outputs.components.pagination.outputs.layout)
            jsonExp.outputs.components.pagination.outputs.instance.update_total_pages(maxPages)
        else:
            HideableWidget.hideIt(jsonExp.outputs.components.pagination.outputs.layout)
    def showBasicContent(self):
        jsonExp = self.view
        HideableWidget.showIt(jsonExp.outputs.components.breadCrumb.outputs.layout)
        val = jsonExp.outputs.components.resultDisplayer.outputs.instance.state.totalPages
        if val > 1:
            HideableWidget.showIt(jsonExp.outputs.components.pagination.outputs.layout)
        HideableWidget.showIt(jsonExp.outputs.components.resultDisplayer.outputs.layout)
    def readContent(self, info):
        jsonExp = self.view
        stateManager  = self.state
        indexSelected = info["owner"].inputs.parent.inputs.index
        key = jsonExp.outputs.components.resultDisplayer.outputs.instance.state.data[indexSelected]
        jsonExp.outputs.components.outArea.outputs.layout.clear_output()
        val = stateManager.model.helper.read(key)
        if type(val)== dict:
            stateManager.model.loc.append(key)
            stateManager.model.helper.set_baseloc(stateManager.model.loc)
            self.update_results_and_pagination(list(stateManager.model.helper.readAll().keys()))
            jsonExp.outputs.components.breadCrumb.outputs.instance.append(key)
        elif type(val)== list:
            stateManager.model.loc.append(key)
            stateManager.model.helper.set_baseloc(stateManager.model.loc)
            self.update_results_and_pagination(list(range(len(stateManager.model.helper.readAll()))))
            jsonExp.outputs.components.breadCrumb.outputs.instance.append(f"[{key}]")
        else:
            with jsonExp.outputs.components.outArea.outputs.layout:
                print(str(val)[:10000])
    def goBack(self,payload):
        jsonExp = self.view
        stateManager  = self.state
        if len(stateManager.model.loc) > 0:
            stateManager.model.loc.pop()
            stateManager.model.helper.set_baseloc(stateManager.model.loc)
            self.update_results_and_pagination(list(stateManager.model.helper.readAll().keys()))
            jsonExp.outputs.components.breadCrumb.outputs.instance.pop()
    def breadCrumbClicked(self, payload):
        jsonExp = self.view
        stateManager  = self.state
        indexSelected = payload["owner"].inputs.parent.index
        for i in range(jsonExp.outputs.components.breadCrumb.outputs.instance.outputs.count - indexSelected- 1):
            jsonExp.outputs.components.breadCrumb.outputs.instance.pop()
            stateManager.model.loc.pop()
        stateManager.model.helper.set_baseloc(stateManager.model.loc)
        self.update_results_and_pagination(list(stateManager.model.helper.readAll().keys()))
    def menuHandler(self, info):
        jsonExp = self.view
        stateManager  = self.state
        jsonExp.outputs.components.outArea.outputs.layout.clear_output()
        menuOps = info["wid"].icon
        if stateManager.menus.selectedMenu:
            if hasattr(stateManager.menus.handlers, stateManager.menus.selectedMenu.icon):
                getattr(stateManager.menus.handlers, stateManager.menus.selectedMenu.icon).undo()
            stateManager.menus.selectedMenu.remove_class("MenuSelected")
        if stateManager.menus.selectedMenu == info["wid"]:
            stateManager.menus.selectedMenu = None
            return
        wid = info["wid"]
        wid.add_class("MenuSelected")
        stateManager.menus.selectedMenu = wid
        if hasattr(stateManager.menus.handlers, menuOps):
            getattr(stateManager.menus.handlers, menuOps).do(info)
        else:
            print(menuOps, "is not implemented yet")
class JSONExplorer(BaseComponent):
    def _state_init(self):

        stateManager = NameSpace()
        stateManager.controller = JSONController()
        stateManager.menus = NameSpace()
        stateManager.menus.selectedMenu = None

        stateManager.pages = NameSpace()
        stateManager.pages.list = NameSpace()
        cnkp = CreateNewKeyPage()
        cnkp.set_global_state(self.gstate)
        cnkp.render()
        cnkp.set_up()
        stateManager.pages.list.createPage = cnkp
        stateManager.pages.list.outAreaForPages = widgets.Output()


        stateManager.model = NameSpace()
        stateManager.model.data = {}
        stateManager.model.loc = []
        stateManager.model.helper = DictionaryCRUD()
        stateManager.model.helper.set_dictionary(stateManager.model.data)
        stateManager.model.variableStates = {}
        stateManager.globalHandlers = NameSpace()
        stateManager.globalHandlers.emptyDisplayArea = stateManager.controller.emptyDisplayArea
        stateManager.globalHandlers.showBasicContent = stateManager.controller.showBasicContent
        stateManager.globalHandlers.update_results_and_pagination = stateManager.controller.update_results_and_pagination
        stateManager.globalHandlers.readContent = stateManager.controller.readContent
        stateManager.globalHandlers.pageNrHandler = stateManager.controller.pageNrHandler
        stateManager.menus.ops = NameSpace()

        stateManager.menus.handlers = NameSpace()
        stateManager.menus.handlers.plus = AddMenuOps()
        stateManager.menus.handlers.plus.set_components(cancel= stateManager.pages.list.createPage.outputs.components.btns.outputs.instance.outputs.renderedStates[0],
            save = stateManager.pages.list.createPage.outputs.components.btns.outputs.instance.outputs.renderedStates[1],
            stateManager = stateManager, displayArea = self.outputs.instance.outputs.components.outArea.outputs.layout, app= self.outputs.instance)
        stateManager.menus.handlers.edit = EditMenuOps()
        stateManager.menus.handlers.edit.set_components(cancel= stateManager.menus.handlers.plus.params.cancel,
            save = stateManager.menus.handlers.plus.params.save,app= self.outputs.instance,
            stateManager = stateManager, displayArea = stateManager.menus.handlers.plus.params.displayArea)
        stateManager.menus.handlers.trash = DeleteMenuOps()
        stateManager.menus.handlers.trash.set_components(cancel= stateManager.menus.handlers.plus.params.cancel,
            save = stateManager.menus.handlers.plus.params.save,app= self.outputs.instance,
            stateManager = stateManager, displayArea = stateManager.menus.handlers.plus.params.displayArea)
        stateManager.menus.handlers.cog = SettingMenuOps()
        stateManager.menus.handlers.cog.set_components(cancel= stateManager.menus.handlers.plus.params.cancel,
            save = stateManager.menus.handlers.plus.params.save, app= self.outputs.instance,
            stateManager = stateManager, displayArea = stateManager.menus.handlers.plus.params.displayArea)
        stateManager.menus.handlers.check = SelectComponentsMenuOps()
        stateManager.menus.handlers.check.set_components(cancel= stateManager.menus.handlers.plus.params.cancel,
            save = stateManager.menus.handlers.plus.params.save, app= self.outputs.instance,
            stateManager = stateManager, displayArea = stateManager.menus.handlers.plus.params.displayArea)
        sizeInput = Utils.get_ipy_omni("ResultDisplaySize", {"description": "result display size", "tooltip":"result display size","max": 20, "min": 5},
                                   IpywidgetsComponentsEnum.BoundedIntText, bind=False)
        settingPage = Utils.get_repeater_omni("SettingPage", [
            Utils.get_repeater_omni("ParameterSettingGroup", [sizeInput]),
            stateManager.pages.list.createPage.outputs.components.btns])
        settingPage.set_global_state(self.gstate)
        settingPage.render()
        settingPage.outputs.components = NameSpace()
        settingPage.outputs.components.sizeInput = sizeInput
        stateManager.pages.list.settingPage = settingPage
        stateManager.pages.list.settingPage.outputs.localCSS = """
        .SettingPage{
            flex-direction: column;
        }
        .ParameterSettingGroup{
            flex: 1
        }

        """
        return stateManager
    def render(self):
        jsonExp = JSONExplorerView()
        jsonExp.set_global_state(self.gstate)
        jsonExp.set_inputs(selected_menu_name = "MenuSelected", comingFrom="JSONExplorer")
        jsonExp.render()
        # set data
        self.outputs.instance = jsonExp
        self.state = self._state_init()
        controller = self.state.controller
        for menu in jsonExp.outputs.components.navigation.outputs.instance.outputs.renderedStates:
            setattr(self.state.menus.ops, menu.outputs.layout.icon, menu)
        jsonExp.outputs.components.pagination.outputs.instance.handlers.handlerForPageNr = controller.pageNrHandler
        jsonExp.gstate.logger.set_level(logging.CRITICAL)

        controller.set_view(jsonExp)
        controller.set_state(self.state)
        jsonExp.outputs.components.resultDisplayer.outputs.instance.handlers.btn_handler = controller.readContent
        jsonExp.outputs.components.resultDisplayer.handlers.handle = controller.goBack
        jsonExp.outputs.components.breadCrumb.handlers.handle = controller.breadCrumbClicked



        jsonExp.gstate.cssManager.update()
        jsonExp.gstate.cssManager.cssAdder.content += self.state.pages.list.settingPage.outputs.localCSS
        jsonExp.gstate.cssManager.cssAdder.content += """
        .SearchResultsSearchedItemSelected{
            border: 1px dotted;
            background-color: #c1c1c1;
        }

        """

        jsonExp.outputs.components.navigation.handlers.handle = controller.menuHandler

        self.outputs.layout = jsonExp.outputs.layout
        self.set_data({})
    def set_data(self, data):
        self.state.model.data = data
        self.state.model.helper.set_dictionary(self.state.controller.state.model.data)
        self.state.controller.update_results_and_pagination(list(self.state.model.data.keys()))
class CreateNewKeyPage(BaseComponent):
    def _setup_enums(self):
        self.state.typeOptions = NameSpace()
        self.state.typeOptions.int = "int"
        self.state.typeOptions.float = "float"
        self.state.typeOptions.bool = "boolean"
        self.state.typeOptions.var = "var"
        self.state.typeOptions.empty_list = "empty list"
        self.state.typeOptions.empty_dict = "empty dict"
        self.state.typeOptions.text = "text"
        self.state.typeOptions.large_text = "large text"
    def render(self):
        self._setup_enums()
        valueTypeOptions = list(self.state.typeOptions.__dict__.values())
        self.outputs.components = NameSpace()
        self.outputs.components.keyname = Utils.get_ipy_omni("InputText", {"description": "key name", "continuous_update":False}, IpywidgetsComponentsEnum.Text, bind=False)
        self.outputs.components.valueType = Utils.get_ipy_omni("typeOfValue", {"description":"select a value type", "options": valueTypeOptions, "value": "text"},
                                                             IpywidgetsComponentsEnum.Dropdown)
        self.outputs.components.overrideComp = Utils.get_ipy_omni("Overwrite", {"description":"overwrite"}, IpywidgetsComponentsEnum.Checkbox, bind=False)
        self.outputs.components.valueTextArea = Utils.get_ipy_omni("valueSectionTextArea", {"description":"value"}, IpywidgetsComponentsEnum.Textarea, bind=False)
        self.outputs.components.valueText = Utils.get_ipy_omni("valueSectionText", {"description":"value"}, IpywidgetsComponentsEnum.Text, bind=False)
        self.outputs.components.valueBoolean = Utils.get_ipy_omni("valueBoolean", {"description":"value"}, IpywidgetsComponentsEnum.Checkbox, bind=False)
        self.outputs.components.valueInt = Utils.get_ipy_omni("valueInt", {"description":"value"}, IpywidgetsComponentsEnum.IntText, bind=False)
        self.outputs.components.valueFloat = Utils.get_ipy_omni("valueFloat", {"description":"value"}, IpywidgetsComponentsEnum.FloatText, bind=False)
        self.outputs.components.btns = Utils.get_repeater_omni( className="BtnsSection", comps= [
            Utils.get_button_omni("CancelBtn",{"description":"cancel"}, "CancelBtn"),
            Utils.get_button_omni("SaveBtn",{"description":"save"}, "SaveBtn")])
        self.outputs.components.outArea = Utils.get_ipy_omni("displayArea", {}, IpywidgetsComponentsEnum.Output, bind=False)
        cnk = Utils.get_repeater_omni(className="CreateNewKey", comps= [
            self.outputs.components.keyname,
            self.outputs.components.valueType,
            self.outputs.components.overrideComp,
            self.outputs.components.valueTextArea,
            self.outputs.components.valueText,
            self.outputs.components.valueBoolean,
            self.outputs.components.valueInt,
            self.outputs.components.valueFloat,
            self.outputs.components.btns,
            self.outputs.components.outArea,
        ])
        cnk.set_global_state(self.gstate)
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
        self.gstate.cssManager.add(self.get_location(), self.outputs.localCss)
        self.outputs.components.valueType.handlers.handle = self._default_handler
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
        self.outputs.components.outArea.outputs.layout.clear_output()
        wid = payload["owner"].outputs.layout
        self._hideValueInputs()
        p = self.outputs.components.valueText.outputs.layout
        if wid.value in [self.state.typeOptions.text,self.state.typeOptions.var]:
            p = self.outputs.components.valueText.outputs.layout
            HideableWidget.showIt(self.outputs.components.valueText.outputs.layout)
        elif wid.value == self.state.typeOptions.large_text:
            p = self.outputs.components.valueTextArea.outputs.layout
            HideableWidget.showIt(self.outputs.components.valueTextArea.outputs.layout)
        elif wid.value == self.state.typeOptions.bool:
            p = self.outputs.components.valueBoolean.outputs.layout
            HideableWidget.showIt(self.outputs.components.valueBoolean.outputs.layout)
        elif wid.value == self.state.typeOptions.int:
            p = self.outputs.components.valueInt.outputs.layout
            HideableWidget.showIt(self.outputs.components.valueInt.outputs.layout)
        elif wid.value == self.state.typeOptions.float:
            p = self.outputs.components.valueFloat.outputs.layout
            HideableWidget.showIt(self.outputs.components.valueFloat.outputs.layout)

        self.outputs.components.valueComponent = p
    def get_values(self):
        key = self.outputs.components.keyname.outputs.layout.value
        override = self.outputs.components.overrideComp.outputs.layout.value
        valType = self.outputs.components.valueType.outputs.layout.value
        value = self.outputs.components.valueComponent.value
        if valType == self.state.typeOptions.var:
            value = self.state.values[value]
        elif valType == self.state.typeOptions.empty_dict:
            value = {}
        elif valType == self.state.typeOptions.empty_list:
            value = []
        return key, override, value
    def update(self, key, value):
        self.outputs.components.outArea.outputs.layout.clear_output()
        self.outputs.components.keyname.outputs.layout.value = key
        if type(value) == int:
            self.outputs.components.valueType.outputs.layout.value = self.state.typeOptions.int
            self.outputs.components.valueInt.outputs.layout.value = value
        elif type(value) == dict:
            self.outputs.components.valueType.outputs.layout.value = self.state.typeOptions.empty_dict
            with self.outputs.components.outArea.outputs.layout:
                print(value)
                print("Value will be overriden with empty dict if you update")
        elif type(value) == list:
            self.outputs.components.valueType.outputs.layout.value = self.state.typeOptions.empty_list
            with self.outputs.components.outArea.outputs.layout:
                print(value)
                print("Value will be overriden with empty list if you update")
        elif type(value) == float:
            self.outputs.components.valueType.outputs.layout.value = self.state.typeOptions.float
            self.outputs.components.valueFloat.outputs.layout.value = value
        elif type(value) == bool:
            self.outputs.components.valueType.outputs.layout.value = self.state.typeOptions.bool
            self.outputs.components.valueBoolean.outputs.layout.value = value
        elif type(value) == str and "\n" not in value and len(value) < 30: # text
            self.outputs.components.valueType.outputs.layout.value = self.state.typeOptions.text
            self.outputs.components.valueText.outputs.layout.value = value
        else: # textarea
            self.outputs.components.valueType.outputs.layout.value = self.state.typeOptions.large_text
            self.outputs.components.valueTextArea.outputs.layout.value = value
class IMenuOps:
    def __init__(self):
        self.params = NameSpace()
    def do(self):
        pass
    def undo(self):
        pass
    def set_components(self, **kwargs):
        for k in kwargs:
            setattr(self.params, k, kwargs[k])
class AddMenuOps(IMenuOps):
    def do(self, *info):
        self.params.cancel.handlers.handle = self.cancelled
        self.params.save.handlers.handle = self.save_callback
        self.params.stateManager.globalHandlers.emptyDisplayArea()
        self.params.displayArea.clear_output()
        with self.params.displayArea:
            display(self.params.stateManager.pages.list.createPage.outputs.layout)
    def cancelled(self, info):
        self.params.stateManager.menus.selectedMenu.remove_class("MenuSelected")
        self.params.stateManager.menus.selectedMenu = None
        self.undo()
    def undo(self, *info):
        self.params.stateManager.globalHandlers.showBasicContent()
        self.params.displayArea.clear_output()
    def save(self):
        key, overwrite, value = self.params.stateManager.pages.list.createPage.get_values()
        self.params.stateManager.model.helper.write(key, value, overwrite)
    def save_callback(self, info):
        self.save()
        self.cancelled(info)
        self.params.stateManager.pages.list.createPage.outputs.components.keyname.outputs.layout.value = ""
        self.params.stateManager.globalHandlers.update_results_and_pagination(list(self.params.stateManager.model.helper.readAll().keys()))
class EditMenuOps(IMenuOps):
    def do(self, *param):
        self.params.app.outputs.components.resultDisplayer.outputs.instance.handlers.btn_handler = self.key_clicked_for_edit
        HideableWidget.hideIt(self.params.stateManager.pages.list.createPage.outputs.components.overrideComp.outputs.layout)
        self.params.stateManager.pages.list.createPage.outputs.components.keyname.outputs.layout.disabled = True
    def undo(self, *param):
        self.params.app.outputs.components.resultDisplayer.outputs.instance.handlers.btn_handler = self.params.stateManager.globalHandlers.readContent
        self.params.stateManager.pages.list.createPage.update("", "")
        self.params.stateManager.globalHandlers.showBasicContent()
        self.params.displayArea.clear_output()
        self.params.stateManager.pages.list.createPage.outputs.components.keyname.outputs.layout.disabled = False
        HideableWidget.showIt(self.params.stateManager.pages.list.createPage.outputs.components.overrideComp.outputs.layout)
    def key_clicked_for_edit(self, info):
        self.editClickedForData(info)
        self.params.stateManager.globalHandlers.emptyDisplayArea()
        self.params.displayArea.clear_output()
        self.params.cancel.handlers.handle = self.cancelled
        self.params.save.handlers.handle = self.update_callback
        with self.params.displayArea:
            display(self.params.stateManager.pages.list.createPage.outputs.layout)
    def editClickedForData(self, info):
        indexSelected = info["owner"].inputs.parent.inputs.index
        key = self.params.app.outputs.components.resultDisplayer.outputs.instance.state.data[indexSelected]
        value = self.params.stateManager.model.helper.read(key)
        self.params.stateManager.pages.list.createPage.update(key, value)
    def cancelled(self, info):
        self.params.stateManager.menus.selectedMenu.remove_class("MenuSelected")
        self.params.stateManager.menus.selectedMenu = None
        self.undo()
    def update_callback(self, info):
        key, overwrite, value = self.params.stateManager.pages.list.createPage.get_values()
        self.params.stateManager.model.helper.write(key, value, True)
        self.cancelled(info)
class DeleteMenuOps(IMenuOps):
    def do(self, *payload):
        self.params.displayArea.clear_output()
        self.params.app.outputs.components.resultDisplayer.outputs.instance.handlers.btn_handler = self.key_clicked_for_delete
    def undo(self, *payload):
        self.params.displayArea.clear_output()
        self.params.app.outputs.components.resultDisplayer.outputs.instance.handlers.btn_handler = self.params.stateManager.globalHandlers.readContent
    def key_clicked_for_delete(self, payload):
        self.params.displayArea.clear_output()
        indexSelected = payload["owner"].inputs.parent.inputs.index
        key = self.params.app.outputs.components.resultDisplayer.outputs.instance.state.data[indexSelected]
        self.params.keySelected = key
        self.params.cancel.handlers.handle = self.cancelled
        self.params.save.handlers.handle = self.delete_callback
        with self.params.displayArea:
            display(self.params.stateManager.pages.list.createPage.outputs.components.btns.outputs.layout)
    def cancelled(self, payload):
        self.params.stateManager.menus.selectedMenu.remove_class("MenuSelected")
        self.params.stateManager.menus.selectedMenu = None
        self.undo()
    def delete_callback(self, payload):
        self.params.stateManager.model.helper.delete(self.params.keySelected)
        self.cancelled(payload)
        self.params.stateManager.globalHandlers.update_results_and_pagination(list(self.params.stateManager.model.helper.readAll().keys()))
class SettingMenuOps(IMenuOps):
    def do(self, *info):
        self.params.cancel.handlers.handle = self.cancelled
        self.params.save.handlers.handle = self.save_callback
        self.params.stateManager.globalHandlers.emptyDisplayArea()
        self.params.displayArea.clear_output()
        with self.params.displayArea:
            display(self.params.stateManager.pages.list.settingPage.outputs.layout)
    def undo(self, *info):
        self.params.stateManager.globalHandlers.showBasicContent()
        self.params.displayArea.clear_output()
    def cancelled(self, info):
        self.params.stateManager.menus.selectedMenu.remove_class("MenuSelected")
        self.params.stateManager.menus.selectedMenu = None
        self.undo()
    def save_callback(self, info):
        pageSize = self.params.stateManager.pages.list.settingPage.outputs.components.sizeInput.outputs.layout.value
        self.params.app.outputs.components.resultDisplayer.outputs.instance.state.pageSize = pageSize
        self.params.app.outputs.components.resultDisplayer.outputs.instance.state.totalPages = math.ceil(
            len(self.params.app.outputs.components.resultDisplayer.outputs.instance.state.data) / pageSize
        )
        maxPages = self.params.app.outputs.components.resultDisplayer.outputs.instance.state.totalPages
        if maxPages not in [0,1]:
            HideableWidget.showIt(self.params.app.outputs.components.pagination.outputs.layout)
            self.params.app.outputs.components.pagination.outputs.instance.update_total_pages(maxPages)
        else:
            HideableWidget.hideIt(self.params.app.outputs.components.pagination.outputs.layout)
        self.cancelled(info)
class SelectComponentsMenuOps(IMenuOps):
    def do(self, *param):
        self.params.current_sub_menu = None
        self.hide_menus()
        self.params.selected = set()
        self.params.app.outputs.components.resultDisplayer.outputs.instance.handlers.btn_handler = self.selected_callback
        self.params.app.outputs.components.pagination.outputs.instance.handlers.handlerForPageNr = self.paginate_with_selection
        self.params.app.outputs.components.navigation.handlers.handle = self.menu_callback
    def undo(self, *param):
        self.params.app.outputs.components.resultDisplayer.outputs.instance.handlers.btn_handler = self.params.stateManager.globalHandlers.readContent
        self.params.app.outputs.components.pagination.outputs.instance.handlers.handlerForPageNr = self.params.stateManager.globalHandlers.pageNrHandler
        self.unselectSelections()
        self.params.selected.clear()
        self.show_menus()
        self.params.app.outputs.components.navigation.handlers.handle = self.params.stateManager.controller.menuHandler
        self.params.stateManager.globalHandlers.update_results_and_pagination(list(self.params.stateManager.model.helper.readAll().keys()))
    def selected_callback(self, info):
        btn = info["wid"]
        indexSelected = info["owner"].inputs.parent.inputs.index
        key = self.params.app.outputs.components.resultDisplayer.outputs.instance.state.data[indexSelected]

        if key in self.params.selected:
            self.params.selected.remove(key)
            btn.remove_class("SearchResultsSearchedItemSelected")
        else:
            self.params.selected.add(key)
            btn.add_class("SearchResultsSearchedItemSelected")
    def paginate_with_selection(self, info):
        self.params.stateManager.globalHandlers.pageNrHandler(info)
        self.selectSelections()
    def selectSelections(self):
        for i, btn in enumerate(self.params.app.outputs.components.resultDisplayer.outputs.instance.outputs.components.btns):
            if btn.outputs.layout.description in self.params.selected:
                btn.outputs.layout.add_class("SearchResultsSearchedItemSelected")
            else:
                btn.outputs.layout.remove_class("SearchResultsSearchedItemSelected")
    def unselectSelections(self):
        for i, btn in enumerate(self.params.app.outputs.components.resultDisplayer.outputs.instance.outputs.components.btns):
            if btn.outputs.layout.description in self.params.selected:
                btn.outputs.layout.remove_class("SearchResultsSearchedItemSelected")
        self.params.selected.clear()
    def menu_callback(self, info):
        self.params.app.outputs.components.outArea.outputs.layout.clear_output()
        menuOps = info["wid"].icon
        self._new_state = {
            "check": {"undo": self.cancelled, "do": self.cancelled},
            "trash": {"do": self.delete_selected, "undo": self.delete_undo},
            "cut": {"do":self.cut_selected,"undo": self.cut_undo},
            "copy": {"do": self.copy_selected, "undo": self.copy_undo},
            "paste": {"do": self.paste_selected, "undo": self.paste_undo}
        }
        if menuOps in self._new_state:
            if self.params.current_sub_menu:
                self._new_state[self.params.current_sub_menu]["undo"](info)
            self.params.current_sub_menu = menuOps
            self._new_state[menuOps]["do"](info)
    def cancelled(self, *info):
        self.params.stateManager.menus.selectedMenu.remove_class("MenuSelected")
        self.params.stateManager.menus.selectedMenu = None
        self.undo()
    def hide_menus(self):
        for navMenu in self.params.app.outputs.components.navigation.outputs.instance.outputs.renderedStates:
            if navMenu.outputs.layout.icon not in ["check", "cut", "copy", "trash"]:
                HideableWidget.hideIt(navMenu.outputs.layout)
    def show_menus(self):
        for navMenu in self.params.app.outputs.components.navigation.outputs.instance.outputs.renderedStates:
            if navMenu.outputs.layout.icon not in ["check", "cut", "copy", "trash"]:
                HideableWidget.showIt(navMenu.outputs.layout)
    def copy_selected(self, info):
        self._cut_copy_selected("copy", lambda x: copy.deepcopy(x))
        HideableWidget.hideIt(self.params.stateManager.menus.ops.cut.outputs.layout)
        HideableWidget.showIt(self.params.stateManager.menus.ops.copy.outputs.layout)
    def delete_selected(self, info):
        self.params.cancel.handlers.handle = self.delete_undo
        self.params.save.handlers.handle = self.delete_from_model
        with self.params.displayArea:
            display(self.params.stateManager.pages.list.createPage.outputs.components.btns.outputs.layout)
    def delete_from_model(self, info):
        for k in self.params.selected:
            self.params.stateManager.model.helper.delete(k)
        self.cancelled(info)
        self.params.stateManager.globalHandlers.update_results_and_pagination(list(self.params.stateManager.model.helper.readAll().keys()))
        self.delete_undo(info)
    def cut_selected(self, info):
        self._cut_copy_selected("cut", lambda x: x)
        HideableWidget.hideIt(self.params.stateManager.menus.ops.copy.outputs.layout)
        HideableWidget.showIt(self.params.stateManager.menus.ops.cut.outputs.layout)
    def _cut_copy_selected(self, ops, valWrapper):
        self.params.opsTodo = ops
        self.params.current_location = self.params.stateManager.model.loc.copy()
        self.params.app.outputs.components.resultDisplayer.outputs.instance.handlers.btn_handler = self.params.stateManager.globalHandlers.readContent
        self.params.selectedWithValues = {key:valWrapper(self.params.stateManager.model.helper.read(key)) for key in self.params.selected}
        self.unselectSelections()
        self.params.stateManager.globalHandlers.update_results_and_pagination(list(filter(lambda x: x not in self.params.selectedWithValues,
                                                                              self.params.stateManager.model.helper.readAll().keys())))
        HideableWidget.hideIt(self.params.stateManager.menus.ops.trash.outputs.layout)
        HideableWidget.showIt(self.params.stateManager.menus.ops.paste.outputs.layout)
    def paste_selected(self, info):
        self.params.cancel.handlers.handle = self.paste_undo
        self.params.save.handlers.handle = self.paste_do
        with self.params.displayArea:
            display(self.params.stateManager.pages.list.createPage.outputs.components.btns.outputs.layout)
    def paste_do(self, info):
        if len(self.params.current_location) == len(self.params.stateManager.model.loc):
            self.params.displayArea.clear_output()
            with self.params.displayArea:
                print("you are tring to paste at same location. Please choose a different location")
            return
        if self.params.opsTodo == "cut":
            DicOps.migrate(self.params.stateManager.model.data, self.params.selectedWithValues, self.params.current_location, self.params.stateManager.model.loc)
            self.cut_undo(info)
        elif self.params.opsTodo == "copy":
            DicOps.copy(self.params.stateManager.model.data, self.params.selectedWithValues, self.params.current_location, self.params.stateManager.model.loc)
            self.copy_undo(info)
        self.paste_undo(info)
    def paste_undo(self, info):
        HideableWidget.showIt(self.params.stateManager.menus.ops.trash.outputs.layout)
        HideableWidget.hideIt(self.params.stateManager.menus.ops.paste.outputs.layout)
        self.params.stateManager.globalHandlers.update_results_and_pagination(list(self.params.stateManager.model.helper.readAll().keys()))
        self.cancelled()
        self.params.app.outputs.components.outArea.outputs.layout.clear_output()
        self.params.selectedWithValues = {}
    def copy_undo(self, info):
        HideableWidget.showIt(self.params.stateManager.menus.ops.cut.outputs.layout)
        self.params.app.outputs.components.resultDisplayer.outputs.instance.handlers.btn_handler = self.selected_callback
    def cut_undo(self,info):
        HideableWidget.showIt(self.params.stateManager.menus.ops.copy.outputs.layout)
        self.params.app.outputs.components.resultDisplayer.outputs.instance.handlers.btn_handler = self.selected_callback
    def delete_undo(self, info):
        self.params.app.outputs.components.outArea.outputs.layout.clear_output()
class DicOps:
    def migrate(dic, keysAndValues, fromLoc, toLoc, createToLoc=False):
        DicOps.copy(dic, keysAndValues, fromLoc, toLoc, createToLoc)
        for key in keysAndValues:
            ListDB.dicOps().delete(dic, fromLoc + [key])
    def copy(dic, keysAndValues, fromLoc, toLoc, createToLoc=False):
        if not createToLoc and not DicOps.locationExists(dic,toLoc ) :
            raise IOError("please create the target location first or set the param: createToLoc=True")
        if fromLoc == toLoc:
            raise IOError("target location and origin location are same")
        for key in keysAndValues:
            val = keysAndValues[key]
            DO.addEventKeyError(dic, toLoc + [key], val)

    def locationExists(dic, loc):
        from ListDB import ListDB
        try:
            ListDB.dicOps().get(dic, loc)
            return True
        except:
            return False
        return False
class Main:
    def jsonExplorer():
        je = JSONExplorer()
        je.set_global_state(GlobalStructure())
        je.render()
        return je
