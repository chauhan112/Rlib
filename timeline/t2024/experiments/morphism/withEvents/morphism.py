from useful.basic import NameSpace
from enum import Enum
from types import SimpleNamespace
from timeline.t2024.ui_lib.components.cssAdder import AddCSSWidget
import ipywidgets as widgets
from pymitter import EventEmitter
from modules.SearchSystem.modular import HideableWidget

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
class ValsWrapper:
    def __init__(self, **vals):
        self.vals = vals
class NestedNamespaceUpdated(SimpleNamespace):
    def __init__(self, dictionary, **kwargs):
        super().__init__(**kwargs)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__setattr__(key, NestedNamespaceUpdated(value))
            elif isinstance(value, ValsWrapper):

                self.__setattr__(key, value.vals)
            else:
                self.__setattr__(key, value)

class Parents:
    def __init__(self):
        self.globalCSS = ""
        self.events = EventEmitter()
        self.cssAdder = AddCSSWidget()
class BaseComponent:
    def __init__(self):
        self.outputs = NameSpace()
    def set_parent_state(self, parent: Parents):
        self.parents = parent
    def set_inputs(self, **args):
        self.inputs = NestedNamespaceUpdated(args)
    def get_this_location(self):
        if hasattr(self.inputs, "parent"):
            return self.inputs.parent.get_this_location() + "/" + self.inputs.comingFrom
        return self.inputs.comingFrom
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
        self.outputs.instance.set_parent_state(self.parents)
        self.outputs.instance.set_inputs(**self.inputs.childParams)
        self.outputs.instance.inputs.parent = self
        self.outputs.instance.render()
        self.outputs.layout = self.outputs.instance.outputs.layout
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
            omniComponent.set_parent_state(self.parents)
            omniComponent.render()
            self.outputs.renderedStates.append(omniComponent)
        self.outputs.layout = widgets.Box([comp.outputs.layout for comp in self.outputs.renderedStates])
        self.outputs.layout.add_class(self.inputs.className)

    def update_layout(self):
        for comp in self.outputs.renderedStates:
            comp.update_layout()
    def append(self, omniComponent):
        omniComponent.inputs.parent = self
        omniComponent.set_parent_state(self.parents)
        omniComponent.render()
        self.outputs.renderedStates.append(omniComponent)
        self.outputs.layout.children = [comp.outputs.layout for comp in self.outputs.renderedStates]
    def pop(self):
        self.outputs.renderedStates.pop()
        self.outputs.layout.children = [comp.outputs.layout for comp in self.outputs.renderedStates]
class IpywidgetComponent(BaseComponent):
    def render(self):
        bind = True
        if self.inputs.typeOfWidget.value == IpywidgetsComponentsEnum.Label.value:
            self.outputs.layout = widgets.Label(**self.inputs.params)
        elif self.inputs.typeOfWidget.value == IpywidgetsComponentsEnum.Button.value:
            self.outputs.layout = self._make_buttons()
            bind = False
        elif self.inputs.typeOfWidget.value == IpywidgetsComponentsEnum.BoundedIntText.value:
            self.outputs.layout = widgets.BoundedIntText(**self.inputs.params)
        elif self.inputs.typeOfWidget.value == IpywidgetsComponentsEnum.Text.value:
            self.outputs.layout = widgets.Text(**self.inputs.params)
        elif self.inputs.typeOfWidget.value == IpywidgetsComponentsEnum.Textarea.value:
            self.outputs.layout = widgets.Textarea(**self.inputs.params)
        elif self.inputs.typeOfWidget.value == IpywidgetsComponentsEnum.IntText.value:
            self.outputs.layout = widgets.IntText(**self.inputs.params)
        elif self.inputs.typeOfWidget.value == IpywidgetsComponentsEnum.FloatText.value:
            self.outputs.layout = widgets.FloatText(**self.inputs.params)
        elif self.inputs.typeOfWidget.value == IpywidgetsComponentsEnum.Dropdown.value:
            self.outputs.layout = widgets.Dropdown(**self.inputs.params)
        elif self.inputs.typeOfWidget.value == IpywidgetsComponentsEnum.Output.value:
            self.outputs.layout = widgets.Output(**self.inputs.params)
            bind = False
        elif self.inputs.typeOfWidget.value == IpywidgetsComponentsEnum.Checkbox.value:
            self.outputs.layout = widgets.Checkbox(**self.inputs.params)
        else:
            raise NotImplementedError("Component Does not exists")
        if bind:
            self.outputs.layout.observe(self._clicked, ["value"])
        if hasattr(self.inputs, "handlersInitializer") and self.inputs.handlersInitializer:
            self.inputs.handlersInitializer(self)
        if self.inputs.className.strip() != "":
            self.outputs.layout.add_class(self.inputs.className)
    def update_layout(self):
        for key in self.inputs.params:
            val = self.inputs.params[key]
            setattr(self.outputs.layout, key, val)
    def _make_buttons(self):
        btn = widgets.Button(**self.inputs.params)
        btn.on_click(self._clicked)
        return btn
    def _clicked(self, wid):
        self.parents.events.emit("all", self)
    def hide(self):
        HideableWidget.hideIt(self.outputs.layout)
    def show(self):
        HideableWidget.showIt(self.outputs.layout)
class BreadCrumbComponent(BaseComponent):
    def render(self):
        pre = self.inputs.cssPrefix
        comps = []
        for i, ele in enumerate(self.inputs.linksArray):
            key = ele
            val = i
            if type(ele) == tuple:
                key, val = ele
            struct = Utils.makeOmniStructure(comingFrom="bread-crumb-item", className="links" + pre, childParamss={
                    "params": ValsWrapper(description= key), "typeOfWidget":IpywidgetsComponentsEnum.Button,
                "handlersInitializer": None}, uiType=ComponentsLib.Ipywidget)
            sep = Utils.makeOmniStructure(comingFrom="separator", className="separator" + pre, childParamss ={ "params": ValsWrapper(value= "/"),
                            "typeOfWidget":IpywidgetsComponentsEnum.Label, "handlersInitializer": None},
                                    uiType=ComponentsLib.Ipywidget)
            struct.inputs.index = i
            if i != 0:
                comps.append(sep)
            comps.append(struct)

        breadCrumb = Utils.get_repeater_omni(comingFrom=self.inputs.comingFrom, className=self.inputs.className + pre, components=comps)
        breadCrumb.set_parent_state(self.parents)
        breadCrumb.render()
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
        self.parents.globalCSS += self.outputs.localCss
        self.outputs.layout = breadCrumb.outputs.layout
        self.outputs.instance = breadCrumb
        self.outputs.count = len(self.inputs.linksArray)
    def append(self, element: str):
        pre = self.inputs.cssPrefix
        struct = Utils.makeOmniStructure(comingFrom="bread-crumb-item", className="links" + pre, childParamss={
                    "params": ValsWrapper(description= element), "typeOfWidget":IpywidgetsComponentsEnum.Button,
                "handlersInitializer": None}, uiType=ComponentsLib.Ipywidget)
        if self.outputs.count != 0:
            sep = Utils.makeOmniStructure(comingFrom="separator", className="separator" + pre, childParamss ={ "params": ValsWrapper(value= "/"),
                                "typeOfWidget":IpywidgetsComponentsEnum.Label, "handlersInitializer": None},
                                        uiType=ComponentsLib.Ipywidget)
            self.outputs.instance.outputs.instance.append(sep)
        struct.index = self.outputs.count
        self.outputs.count += 1

        self.outputs.instance.outputs.instance.append(struct)
    def pop(self):
        self.outputs.instance.outputs.instance.pop()
        if len(self.outputs.instance.outputs.instance.outputs.renderedStates) > 0:
            self.outputs.instance.outputs.instance.pop()
        self.outputs.count -= 1
    def update_layout(self):
        self.render()
class ResultDisplayer(BaseComponent):
    def render(self):
        pre = self.inputs.cssPrefix
        comps = []
        backButton = Utils.makeOmniStructure(comingFrom="backButton", className="SearchResultsBackButton" + pre , childParamss={
                    "params": ValsWrapper(icon = "arrow-left"), "typeOfWidget":IpywidgetsComponentsEnum.Button,
                "handlersInitializer": None}, uiType=ComponentsLib.Ipywidget, parentLoc ="")
        backButton.set_parent_state(self.parents)
        self.outputs.components = NameSpace()
        self.outputs.components.backButton = backButton
        self.outputs.components.btns = []
        comps.append(backButton)
        for i in range(20):
            resultComponent = Utils.makeOmniStructure(comingFrom="searched-item", className="SearchResultsSearchedItem" + pre ,
                                                      childParamss={ "params": ValsWrapper(description = "arrow-left", tooltip= "awesome"),
                                                                    "typeOfWidget":IpywidgetsComponentsEnum.Button, "handlersInitializer": None},
                                                      uiType=ComponentsLib.Ipywidget, parentLoc ="")
            resultComponent.set_parent_state(self.parents)
            resultComponent.inputs.index = i
            comps.append(resultComponent)
            self.outputs.components.btns.append(resultComponent)
        res_displayer = Utils.get_repeater_omni(components=comps,comingFrom=self.inputs.comingFrom, className=self.inputs.className + pre)
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
        res_displayer.set_parent_state(self.parents)
        res_displayer.render()
        self.parents.globalCSS += self.outputs.localCss
        self.outputs.layout = res_displayer.outputs.layout
        self.outputs.instance = res_displayer
    def update_layout(self):
        pass
    def set_array(self, arr):
        self.inputs.data = arr
class PaginationComponent(BaseComponent):
    def render(self):
        pre = self.inputs.cssPrefix
        comps = []
        self.outputs.components = NameSpace()
        self.outputs.components.backBtn = Utils.makeOmniStructure(comingFrom="gobackButtonPagination", className="gobackButtonPagination" + pre,
                                                                  childParamss ={ "params": ValsWrapper(description= "prev"),
                                                                                 "typeOfWidget":IpywidgetsComponentsEnum.Button},
                                                                  uiType=ComponentsLib.Ipywidget)
        comps.append(self.outputs.components.backBtn)
        self.outputs.components.btns = []
        for i in range(5):
            btn = Utils.makeOmniStructure(comingFrom="paginationButton", className="PaginationButton"+ pre, childParamss ={
                "params": ValsWrapper(description= str(i+1)), "typeOfWidget":IpywidgetsComponentsEnum.Button}, uiType=ComponentsLib.Ipywidget)
            comps.append(btn)
            self.outputs.components.btns.append(btn)
        self.outputs.components.nextBtn = Utils.makeOmniStructure(
            comingFrom="nextButtonPagination",
            className="nextButtonPagination"+ pre,
            childParamss ={ "params": ValsWrapper(description= "next"), "typeOfWidget":IpywidgetsComponentsEnum.Button},
            uiType=ComponentsLib.Ipywidget
        )
        comps.append(self.outputs.components.nextBtn)
        self.outputs.components.maxPageLabel = Utils.makeOmniStructure(comingFrom="maxPagePaginationButton", className="maxPagePaginationButton"+ pre,
                                                                       childParamss ={ "params": ValsWrapper(value= "pMax"),
                                                                                      "typeOfWidget":IpywidgetsComponentsEnum.Label,
                                                                                      "handlersInitializer": None},
                                                                       uiType=ComponentsLib.Ipywidget)
        comps.append(self.outputs.components.maxPageLabel)
        self.outputs.components.gotoInput = Utils.makeOmniStructure(comingFrom="gotoIntInputPagination", className="gotoIntInputPagination"+ pre,
                                                                    childParamss ={ "params": ValsWrapper(min= 0, max = 1),
                                                                                   "typeOfWidget":IpywidgetsComponentsEnum.BoundedIntText},
                                                                    uiType=ComponentsLib.Ipywidget)
        comps.append(self.outputs.components.gotoInput)
        self.outputs.components.gotoBtn = Utils.makeOmniStructure(comingFrom="gotoButtonPagination", className="gotoButtonPagination"+ pre,
                                                                  childParamss ={ "params": ValsWrapper(description= "go"),
                                                                                 "typeOfWidget":IpywidgetsComponentsEnum.Button},
                                                                  uiType=ComponentsLib.Ipywidget)
        comps.append(self.outputs.components.gotoBtn)
        om = Utils.makeOmniStructure(uiType=ComponentsLib.Repeater, childParamss={"inp_components": comps}, comingFrom=self.inputs.comingFrom, className=self.inputs.className+ pre)
        om.set_parent_state(self.parents)
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
        self.parents.globalCSS += self.outputs.localCss
        self.outputs.layout = om.outputs.layout
        self.outputs.instance = om
    def update_layout(self):
        pass # does need to update thiss

class Utils:
    def get_button_omni(comingFrom, className, btnInfo):
        return Utils.makeOmniStructure(comingFrom=comingFrom, className=className, childParamss ={ "params": ValsWrapper(**btnInfo),
                                        "typeOfWidget":IpywidgetsComponentsEnum.Button, "handlersInitializer": None,
                                        "comingFrom":comingFrom, "className":className},
                                                uiType=ComponentsLib.Ipywidget)
    def get_repeater_omni(comingFrom, className, components):
        return Utils.makeOmniStructureWithoutArgs(uiType=ComponentsLib.Repeater, childParamss={"inp_components": components,
                                            "comingFrom":comingFrom, "className":className}, comingFrom=comingFrom, className=className)
    def get_label_omni(comingFrom, className, value, parentLoc=""):
        return Utils.makeOmniStructure(comingFrom=comingFrom, className=className, childParamss ={ "params": ValsWrapper(value= value),
                                        "typeOfWidget":IpywidgetsComponentsEnum.Label, "handlersInitializer": None, "comingFrom":comingFrom,
                                        "className":className},
                                                uiType=ComponentsLib.Ipywidget, parentLoc = parentLoc)
    def get_ipy_omni(comingFrom, className, widgetInfo:dict, typ, parentLoc=""):
        return Utils.makeOmniStructure(comingFrom=comingFrom, className=className, childParamss ={ "params": ValsWrapper(**widgetInfo),
                                        "typeOfWidget":typ,"comingFrom":comingFrom, "className":className},
                                                uiType=ComponentsLib.Ipywidget, parentLoc = parentLoc)
    def makeOmniStructure(uiType= ComponentsLib.Ipywidget, childParamss={}, comingFrom ="", className="", **args):
        omni = OmniComponent()
        abc = {**args, **childParamss, "comingFrom": comingFrom, "className":className}
        omni.set_inputs(childParams= ValsWrapper(**abc),comingFrom=comingFrom, className=className, uiType = uiType)
        return omni
    def makeOmniStructureWithoutArgs(uiType= ComponentsLib.Ipywidget, childParamss= {}, **args):
        omni = OmniComponent()
        omni.set_inputs(childParams= ValsWrapper(**childParamss), uiType = uiType, **args)
        return omni
