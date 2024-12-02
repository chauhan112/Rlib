from basic import NameSpace, LoggerSystem
from enum import Enum
from timeline.t2024.ui_lib.components.cssAdder import AddCSSWidget
import ipywidgets as widgets
from modules.SearchSystem.modular import HideableWidget
import logging
import math

class ComponentsLib(Enum):
    Text = 1
    LargeText = 2
    Checkbox = 3
    Options = 4
    Date = 5
    Time = 6
    DateTime = 7
    Label = 8
    Placeholder = 9
    BreadCrumb = 10
    JsonNavigator = 11
    ListNavigator = 12
    ListAndJsonNavigator = 13
    Button = 14
    Repeater = 15
    Ipywidget = 16
    ButtonResultDisplayer = 17
    Paginator = 18
    CSSAdder = 19
    CustomOutput = 20
    IpyWrapper = 21
class IpywidgetsComponentsEnum(Enum):
    IntSlider            = 1
    FloatSlider          = 2
    FloatLogSlider       = 3
    IntRangeSlider       = 4
    FloatRangeSlider     = 5
    IntProgress          = 6
    FloatProgress        = 7
    BoundedIntText       = 8
    BoundedFloatText     = 9
    IntText              = 10
    FloatText            = 11
    ToggleButton         = 12
    Checkbox             = 13
    Valid                = 14
    Dropdown             = 15
    RadioButtons         = 16
    Select               = 17
    SelectionSlider      = 18
    SelectionRangeSlider = 19
    ToggleButtons        = 20
    SelectMultiple       = 21
    Text                 = 22
    Textarea             = 23
    Combobox             = 24
    Password             = 25
    Label                = 26
    HTML                 = 27
    HTMLMath             = 28
    Image                = 29
    Button               = 30
    Output               = 31
    TagsInput            = 32
    ColorsInput          = 33
    PlayAnimationWidget  = 34
    DatePicker           = 35
    TimePicker           = 36
    DatetimePicker       = 37
    NaiveDatetimePicker  = 38
    ColorPicker          = 39
    FileUpload           = 40
    GameController       = 41
    Box                  = 42
    HBox                 = 43
    VBox                 = 44
    GridBox              = 45
    Accordion            = 46
    Tabs                 = 47
    Stack                = 48
class CSSManager:
    def __init__(self):
        self.cssAdder = AddCSSWidget()
        self.classNames = set()
        self._keys = []
        self._keySet = set()
        self._content_vals = {}
    def add(self, key, value):
        if key not in self._keySet:
            self._keySet.add(key)
            self._keys.append(key)
            self._content_vals[key] = value
        else:
            print(key, "aleady exists")
            self._content_vals[key] += value

    def update(self):
        self.cssAdder.content = self.get_content()
    def get_content(self):
        res =""
        for k in self._keys:
            res += self._content_vals[k] + "\n"
        return res
class GlobalStructure:
    def __init__(self):
        self.cssManager = CSSManager()
        self.logger = LoggerSystem()
class BaseComponent:
    def __init__(self):
        self.outputs = NameSpace()
        self.inputs = NameSpace()
        self.inputs.parent = None
        self.inputs.comingFrom = ""
        self.inputs.bind = True
        self.inputs.cssPrefix =""
        self.state = NameSpace()
        self.inputs.className = ""
        self.handlers = NameSpace()
        self.handlers.defs = NameSpace()
        self.handlers.handle = self._def_handler
        self.handlers.defs.handle = self._def_handler
        self.handlers.defs.wrapper = self._handler_wrapper


    def set_global_state(self, state: GlobalStructure):
        self.gstate = state
    def set_inputs(self, **args):
        for key in args:
            val = args[key]
            setattr(self.inputs, key, val)
    def get_location(self):
        if self.inputs.parent:
            return (self.inputs.parent.get_location() + "/" + self.inputs.comingFrom).strip("/")
        return self.inputs.comingFrom
    def _def_handler(self, wid):
        print(self.get_location(), wid)
    def _handler_wrapper(self, wid):
        self.handlers.handle(wid)
class IpywidgetComponent(BaseComponent):
    def render(self):
        self.handlers.handle = self._default_handler
        self.handlers.defs.handle = self._default_handler
        if self.inputs.typeOfWidget.value == IpywidgetsComponentsEnum.Button.value:
            self.outputs.layout = widgets.Button(**self.inputs.params)
            self.outputs.layout.on_click(self._clicked)
        elif self.inputs.typeOfWidget.value == IpywidgetsComponentsEnum.Output.value:
            self.outputs.layout = widgets.Output(**self.inputs.params)
        else:
            self.outputs.layout = getattr(widgets, self.inputs.typeOfWidget.name)(**self.inputs.params)
            if self.inputs.bind:
                self.outputs.layout.observe(self._clicked, ["value"])
        if hasattr(self.inputs, "handlersInitializer") and self.inputs.handlersInitializer:
            self.inputs.handlersInitializer(self)
    def update_layout(self):
        for key in self.inputs.params:
            val = self.inputs.params[key]
            setattr(self.outputs.layout, key, val)
    def _default_handler(self, params):
        print(params)
    def _clicked(self, wid):
        self.gstate.logger.log(logging.INFO, self.handlers.handle.__name__ + " "+"handler location: " + self.get_location())
        self.handlers.handle({"wid": wid, "owner": self})
class OmniComponent(BaseComponent):
    def render(self):
        if self.inputs.uiType.value == ComponentsLib.Repeater.value:
            self.outputs.instance = RepeaterComponent()
        elif self.inputs.uiType.value == ComponentsLib.Ipywidget.value:
            self.outputs.instance = IpywidgetComponent()
        elif self.inputs.uiType.value == ComponentsLib.BreadCrumb.value:
            self.outputs.instance = BreadCrumbComponent()
        elif self.inputs.uiType.value == ComponentsLib.ButtonResultDisplayer.value:
            self.outputs.instance = ResultDisplayer()
        elif self.inputs.uiType.value == ComponentsLib.Paginator.value:
            self.outputs.instance = PaginationComponent()
        else:
            raise NotImplementedError("component not implemented error")
        self.outputs.instance.set_global_state(self.gstate)
        self.outputs.instance.set_inputs(**self.inputs.childParams)
        self.outputs.instance.inputs.parent = self
        self.outputs.instance.render()
        self.outputs.instance.handlers.handle = self.handlers.defs.wrapper
        self.outputs.layout = self.outputs.instance.outputs.layout
        if self.inputs.className.strip() != "":
            self.gstate.cssManager.classNames.add(self.inputs.className)
            self.outputs.layout.add_class(self.inputs.className)
    def update_layout(self):
        self.outputs.instance.update_layout()
    def get_this_location(self):
        if hasattr(self.inputs, "parent"):
            return self.inputs.parent.get_this_location()
        return ""
class RepeaterComponent(BaseComponent):
    def render(self):
        self.outputs.renderedStates = []
        for omniComponent in self.inputs.inp_components:
            omniComponent.inputs.parent = self
            omniComponent.set_global_state(self.gstate)
            omniComponent.render()
            omniComponent.handlers.handle = self.handlers.defs.wrapper
            self.outputs.renderedStates.append(omniComponent)
        self.outputs.layout = widgets.Box([comp.outputs.layout for comp in self.outputs.renderedStates])
        if self.inputs.className:
            self.outputs.layout.add_class(self.inputs.className)

    def update_layout(self):
        for comp in self.outputs.renderedStates:
            comp.update_layout()
    def append(self, omniComponent):
        omniComponent.inputs.parent = self
        omniComponent.set_global_state(self.gstate)
        omniComponent.render()
        omniComponent.handlers.handle = self._handler_wrapper
        self.outputs.renderedStates.append(omniComponent)
        self.outputs.layout.children = [comp.outputs.layout for comp in self.outputs.renderedStates]
    def pop(self):
        self.outputs.renderedStates.pop()
        self.outputs.layout.children = [comp.outputs.layout for comp in self.outputs.renderedStates]
class PaginationComponent(BaseComponent):
    def render(self):
        pre = self.inputs.cssPrefix
        comps = []
        self.outputs.components = NameSpace()
        self.outputs.components.backBtn = Utils.get_ipy_omni("gobackButtonPagination" + pre, {"description":"prev"},IpywidgetsComponentsEnum.Button ,"prev")
        comps.append(self.outputs.components.backBtn)
        self.outputs.components.btns = []
        for i in range(5):
            btn = Utils.get_ipy_omni("PaginationButton"+ pre, {"description":str(i+1)} , IpywidgetsComponentsEnum.Button, "btns")
            comps.append(btn)
            self.outputs.components.btns.append(btn)

        self.outputs.components.nextBtn = Utils.get_ipy_omni("nextButtonPagination"+ pre, {"description":"next"},IpywidgetsComponentsEnum.Button, "next")
        comps.append(self.outputs.components.nextBtn)
        self.outputs.components.maxPageLabel = Utils.get_ipy_omni("maxPagePaginationButton"+ pre, { "value": "5"},
            IpywidgetsComponentsEnum.Label, bind= False)
        comps.append(self.outputs.components.maxPageLabel)
        self.outputs.components.gotoInput = Utils.get_ipy_omni("gotoIntInputPagination" + pre, { "min": 1, "max": 5}, IpywidgetsComponentsEnum.BoundedIntText,"gotoIntInput",
                                                              bind= False)
        comps.append(self.outputs.components.gotoInput)
        self.outputs.components.gotoBtn = Utils.get_ipy_omni("gotoButtonPagination"+ pre, { "description": "go"}, IpywidgetsComponentsEnum.Button, "goBtn")
        comps.append(self.outputs.components.gotoBtn)
        om = Utils.get_repeater_omni(self.inputs.className+ pre, comps)
        om.set_global_state(self.gstate)
        om.inputs.parent = self
        self.outputs.localCss = f"""
        .PaginationButtons{pre}{{
            width: 100%;
            background-color: unset;
            display: flex;
            justify-content: center;

        }}
        .gobackButtonPagination{pre},.nextButtonPagination{pre},.gotoButtonPagination{pre}, .PaginationButton{pre}{{
            background-color: unset;
            color: #007bff;
            width: auto;
        }}
        .gotoButtonPagination{pre}{{
            background-color: #007bff;
            color: white;
        }}
        .PaginationButton{pre}:focus:enabled{{
            outline: 0;

        }}
        .gotoIntInputPagination{pre}{{
            color: #007bff;
            width: 80px;
        }}

        .PaginationButton{pre}{{
            width:auto;
        }}
        .{self.inputs.selected_button_class_name}{{
            background-color: #007bff;
            color: white;
        }}

        """
        om.render()
        om.handlers.handle = self.handlers.defs.wrapper
        self.gstate.cssManager.add(self.get_location(), self.outputs.localCss)
        self.outputs.layout = om.outputs.layout
        self.outputs.instance = om
        self._bind()
    def _bind(self):
        self.handlers.defs.pageNumberSelected = self._page_btn_selected
        self.handlers.defs.prevClicked = self._prev_clicked
        self.handlers.defs.nextClicked = self._next_clicked
        self.handlers.defs.select_page_nr = self._select_btn_with_number
        self.handlers.defs.goto_click = self._goto_clicked
        self.handlers.handlerForPageNr = lambda nr: nr
        for btn in self.outputs.components.btns:
            btn.handlers.handle  = self._btns_handler_wrapper
        self.outputs.components.backBtn.handlers.handle = self.handlers.defs.prevClicked
        self.outputs.components.nextBtn.handlers.handle = self.handlers.defs.nextClicked
        self.outputs.components.gotoBtn.handlers.handle = self.handlers.defs.goto_click
        self.state.selectedBtn = self.outputs.components.btns[0].outputs.layout
        self.state.selectedBtn.add_class(self.inputs.selected_button_class_name)
        self.state.maxPageSize = 5
    def _btns_handler_wrapper(self, info):
        self.handlers.defs.pageNumberSelected(info)
    def _page_btn_selected(self, info):
        btn = info["wid"]
        if self.state.selectedBtn == btn:
            return
        self._select_btn_with_number(int(btn.description))
    def _prev_clicked(self, info):
        btn = info["wid"]
        val = int(self.state.selectedBtn.description)
        if val == 1:
            val = self.outputs.components.gotoInput.outputs.layout.max
        else:
            val -= 1
        self._select_btn_with_number(val)
    def _next_clicked(self, info):
        btn = info["wid"]
        val = int(self.state.selectedBtn.description)
        if val == self.outputs.components.gotoInput.outputs.layout.max:
            val = 1
        else:
            val += 1
        self._select_btn_with_number(val)
    def _goto_clicked(self, info):
        btn = info["wid"]
        val = self.outputs.components.gotoInput.outputs.layout.value
        self._select_btn_with_number(val)
    def _select_btn_with_number(self, nr):
        self.state.selectedBtn.remove_class(self.inputs.selected_button_class_name)
        self._update_buttons_description(nr)
        for btn in self.outputs.components.btns:
            if btn.outputs.layout.description == str(nr):
                self.state.selectedBtn = btn.outputs.layout
                self.state.selectedBtn.add_class(self.inputs.selected_button_class_name)
                self.handlers.handlerForPageNr(nr)
                break
    def _update_buttons_description(self, nr):
        pagesNr = self._windowCalc(nr, self.state.maxPageSize)
        for i, btn in enumerate(self.outputs.components.btns):
            if i < len(pagesNr):
                btn.outputs.layout.description = str(pagesNr[i])
                HideableWidget.showIt(btn.outputs.layout)
            else:
                HideableWidget.hideIt(btn.outputs.layout)
    def _windowCalc(self, n, total):
        t = total
        if n < 3:
            res = range(6)
        elif n > (t-3):
            res = range(t-4, t+1)
        else:
            res = range(n-2, n+3)
        return list(filter(lambda x: x > 0 and x < t+1, res))
    def update_total_pages(self, total):
        self.state.maxPageSize = total
        self._update_buttons_description(len(self.state.selectedBtn.description))
        self.outputs.components.gotoInput.outputs.layout.max = self.state.maxPageSize
        self.outputs.components.maxPageLabel.outputs.layout.value = str(self.state.maxPageSize)
class BreadCrumbComponent(BaseComponent):
    def render(self):
        pre = self.inputs.cssPrefix
        comps = []
        for i, key in enumerate(self.inputs.linksArray):
            struct = Utils.get_ipy_omni("links" + pre, {"description": key}, IpywidgetsComponentsEnum.Button, "breadCrumItem")
            sep = Utils.get_ipy_omni("separator" + pre,{ "value": "/", "bind":False }, IpywidgetsComponentsEnum.Label, "separator")
            struct.inputs.index = i
            if i != 0:
                comps.append(sep)
            comps.append(struct)

        breadCrumb = Utils.get_repeater_omni( className=self.inputs.className + pre, comps=comps, comingFrom="BreadCrumb")
        breadCrumb.set_global_state(self.gstate)
        breadCrumb.render()
        breadCrumb.handlers.handle = self.handlers.defs.wrapper
        breadCrumb.inputs.parent = self
        self.outputs.localCss = f"""
        .links{pre}{{
            display: inline-block;
            width: auto;
            padding: 0;
            background: unset;
            color: blue;
            text-decoration: underline;


        }}
        .links{pre}:hover:enabled{{
            display: inline-block;
            width: auto;
            padding: 0;
            background: unset;
            color: blue;
            text-decoration: underline;
            box-shadow: unset;

        }}
        .links{pre}:focus:enabled{{
            opacity: .8;
            outline: unset;
            box-shadow: unset;
            color: red;
        }}

        .links{pre}:last-child{{
            color: unset;
            text-decoration: none;
            pointer-events: none;
        }}

        """
        self.gstate.cssManager.add(self.get_location(), self.outputs.localCss)
        self.outputs.layout = breadCrumb.outputs.layout
        self.outputs.instance = breadCrumb
        self.outputs.count = len(self.inputs.linksArray)
    def append(self, element: str):
        pre = self.inputs.cssPrefix
        struct = Utils.get_ipy_omni("links" + pre, {"description": element}, IpywidgetsComponentsEnum.Button)
        if self.outputs.count != 0:
            sep = Utils.get_ipy_omni("separator" + pre, { "value": "/", "bind":False }, IpywidgetsComponentsEnum.Label)
            self.outputs.instance.outputs.instance.append(sep)
        struct.index = self.outputs.count
        self.outputs.count += 1

        self.outputs.instance.outputs.instance.append(struct)
    def pop(self):
        self.outputs.instance.outputs.instance.pop()
        if len(self.outputs.instance.outputs.instance.outputs.renderedStates) > 0:
            self.outputs.instance.outputs.instance.pop()
        self.outputs.count -= 1
class ResultDisplayer(BaseComponent):
    def render(self):
        pre = self.inputs.cssPrefix
        comps = []
        backButton = Utils.get_ipy_omni("SearchResultsBackButton" + pre , {"icon":"arrow-left"}, IpywidgetsComponentsEnum.Button, "backbtn")
        self.outputs.components = NameSpace()
        self.outputs.components.backButton = backButton
        self.outputs.components.btns = []
        comps.append(backButton)
        for i in range(20):
            resultComponent = Utils.get_ipy_omni("SearchResultsSearchedItem" + pre ,{"description":"arrow-left", "tooltip": "awesome"},
                                                       IpywidgetsComponentsEnum.Button, "search-items")
            resultComponent.inputs.index = i
            comps.append(resultComponent)
            self.outputs.components.btns.append(resultComponent)
        res_displayer = Utils.get_repeater_omni(comps=comps, className=self.inputs.className + pre)
        res_displayer.inputs.parent = self
        self.outputs.localCss = f"""
            .SearchResultsBackButton{pre}{{
                height: 2.5rem;
                width: 3rem;
                font-size: 1.5rem;
            }}

            .SearchResultsSearchedItem{pre}{{
                height: 2.5rem;
                max-width: 5rem;
                white-space: normal;
                line-height: 1rem;
                padding: unset;
            }}
            .{self.inputs.className}{pre}{{
                width: 100%;
                flex-wrap: wrap;
            }}

            """
        res_displayer.set_global_state(self.gstate)
        res_displayer.render()
        res_displayer.handlers.handle = self.handlers.defs.wrapper
        self.gstate.cssManager.add(self.get_location(), self.outputs.localCss)
        self.outputs.layout = res_displayer.outputs.layout
        self.outputs.instance = res_displayer
        self._bind()
    def set_data(self, data):
        self.state.data = data
        if not hasattr(self.state, "pageNr"):
            self.state.pageNr = 1
        if not hasattr(self.state, "pageSize"):
            self.state.pageSize = 20
        self.state.totalPages = math.ceil(len(self.state.data)/self.state.pageSize)
    def update(self):
        data = self._data_for_currentPage()
        for i, btn in enumerate(self.outputs.components.btns):
            if i < len(data):
                btn.inputs.index, btn.outputs.layout.description = data[i]
                HideableWidget.showIt(btn.outputs.layout)
            else:
                HideableWidget.hideIt(btn.outputs.layout)
    def _btns_handler_wrapper(self, info):
        self.handlers.btn_handler(info)
    def _data_for_currentPage(self):
        res = []
        fromStart = self.state.pageSize * (self.state.pageNr-1)
        till = self.state.pageSize * (self.state.pageNr)
        for i in range(fromStart, till):
            if i >= len(self.state.data):
                break
            res.append((i, self.state.data[i]))
        return res
    def _bind(self):
        self.handlers.btn_handler = self.handlers.handle
        for btn in self.outputs.components.btns:
            btn.handlers.handle  = self._btns_handler_wrapper
class Utils:
    def get_omni_component(className,comingFrom, childParams, uiType):
        omn = OmniComponent()
        omn.set_inputs(className=className, comingFrom = comingFrom,childParams=childParams, uiType=uiType)
        return omn
    def get_ipy_omni(className, infos, compType, comingFrom="", **args):
        return Utils.get_omni_component(className, comingFrom, {"params": infos, "typeOfWidget":compType, **args}, ComponentsLib.Ipywidget)
    def get_repeater_omni(className, comps, comingFrom=""):
        return Utils.get_omni_component(className, comingFrom,{"inp_components": comps}, ComponentsLib.Repeater)
    def get_button_omni(className, btnInfo, comingFrom=""):
        return Utils.get_omni_component(className, comingFrom, {"params": btnInfo, "typeOfWidget":IpywidgetsComponentsEnum.Button}, ComponentsLib.Ipywidget)
