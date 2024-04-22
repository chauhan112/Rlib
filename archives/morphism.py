from dataclasses import dataclass
from enum import Enum
from timeline.t2024.ui_lib.components.cssAdder import AddCSSWidget
from timeline.t2024.ui_lib.components.widgetComponents import DataStructureForEventSystem
import ipywidgets as widgets
from pymitter import EventEmitter
from DataStructure import DataStructure
from types import SimpleNamespace

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
    def __init__(self, vals):
        self.vals = vals
class NestedNamespaceUpdated(SimpleNamespace):
    def __init__(self, dictionary, **kwargs):
        super().__init__(**kwargs)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__setattr__(key, NestedNamespace(value))
            elif isinstance(value, ValsWrapper):
                
                self.__setattr__(key, value.vals)
            else:
                self.__setattr__(key, value)
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
@dataclass
class UIInfo:
    instance = None
    className = ""
    info = None  # can be of different structure based on the UI component # it can be a dictionary as well
    uiType = None
@dataclass
class CssStyling:
    css_properties = ""
    css_adder = None
@dataclass
class DataStructureForUIComponent:
    event = None
    uiInfo = None
    cssStyling = None
    layout = None
class OmniComponentUI:
    def __init__(self):
        self.state_default = self.get_default_state()
        self.set_state(self.state_default)
    def get_default_state(self):
        state = Utils.get_state()
        state.event.comingFrom = "OmniComponentUI"
        state.uiInfo.className = "OmniComponentUI"
        return state
    def set_state(self, state):
        self.state = state
    def render(self):
        if self.state.uiInfo.uiType.value == ComponentsLib.Label.value:
            self.state.uiInfo.instance = LabelComponent()
        elif self.state.uiInfo.uiType.value == ComponentsLib.Button.value:
            self.state.uiInfo.instance = ButtonComponent()
        elif self.state.uiInfo.uiType.value == ComponentsLib.Repeater.value:
            self.state.uiInfo.instance = RepeaterComponent()
        elif self.state.uiInfo.uiType.value == ComponentsLib.Ipywidget.value:
            self.state.uiInfo.instance = IpywidgetComponent()
        elif self.state.uiInfo.uiType.value == ComponentsLib.BreadCrumb.value:
            self.state.uiInfo.instance = BreadCrumbComponent()
        else:
            raise NotImplementedError("component not implemented error")
        self.state.uiInfo.instance.set_state(self.state)
        self.state.uiInfo.instance.render()
        self.state.uiInfo.className = self.state.uiInfo.instance.state.uiInfo.className
        self.state.uiInfo.instance.state.event.parentLoc = self.state.event.parentLoc + "/" + self.state.event.comingFrom
        self.state.layout = self.state.uiInfo.instance.state.layout
    def update_layout(self):
        self.state.uiInfo.instance.update_layout()
class Utils:
    def get_state():
        state = DataStructureForUIComponent()
        state.cssStyling = CssStyling()
        state.cssStyling.css_adder = AddCSSWidget()
        state.cssStyling.css_adder.content = state.cssStyling.css_properties
        state.event = DataStructureForEventSystem()
        state.event.instance = EventEmitter()
        state.event.comingFrom = "OmniComponentUI"
        state.uiInfo = UIInfo()
        state.uiInfo.className = "OmniComponentUI"
        return state
@dataclass
class DataStructureForButton:
    description ="Button"
@dataclass
class DataStructureForLabel:
    value ="Label"
class ButtonComponent:
    def __init__(self):
        self.state_default = self.get_default_state()
        self.set_state(self.state_default)
    def get_default_state(self):
        state = Utils.get_state()
        state.event.comingFrom = "Button23934"
        state.uiInfo.className = "Button23934"
        state.uiInfo.uiType = ComponentsLib.Button
        state.uiInfo.info = DataStructureForButton()
        return state
    def set_state(self, state):
        self.state = state
    def render(self):
        self.state.layout = widgets.Button(description = self.state.uiInfo.info.description)
        self.state.layout.on_click(self._clicked)
        self.state.layout.add_class(self.state.uiInfo.className)
    def update_layout(self):
        self.state.layout.description = self.state.uiInfo.info.description
    def _clicked(self, wid):
        self.state.event.instance.emit("all", {"widget": wid, "loc": (self.state.event.parentLoc + "/" + self.state.event.comingFrom).strip("/"), "type": "clicked"})
class LabelComponent:
    def __init__(self):
        self.state_default = self.get_default_state()
        self.set_state(self.state_default)
    def get_default_state(self):
        state = Utils.get_state()
        state.event.comingFrom = "Label0219021"
        state.uiInfo.className = "Label0219021"
        state.uiInfo.uiType = ComponentsLib.Label
        state.uiInfo.info = DataStructureForLabel()
        return state
    def set_state(self, state):
        self.state = state
    def render(self):
        self.state.layout = widgets.Label(value = self.state.uiInfo.info.value)
        self.state.layout.add_class(self.state.uiInfo.className)
    def update_layout(self):
        self.state.layout.value = self.state.uiInfo.info.value
@dataclass
class DataStructureForRepeater:
    inp_components = [] # list of structure for omnicomponent
    renderedStates = [] # list of rendered states which can be accessed
class RepeaterComponent:
    def __init__(self):
        self.state_default = self.get_default_state()
        self.set_state(self.state_default)
    def get_default_state(self):
        state = Utils.get_state()
        state.event.comingFrom = "Repeater3243453"
        state.uiInfo.className = "Repeater3243453"
        state.uiInfo.uiType = ComponentsLib.Repeater
        state.uiInfo.info = DataStructureForRepeater()
        return state
    def set_state(self, state):
        self.state = state
    def render(self):
        for comp in self.state.uiInfo.info.inp_components:
            omniComponent = OmniComponentUI()
            omniComponent.set_state(comp)
            omniComponent.state.event.instance = self.state.event.instance
            omniComponent.render()
            omniComponent.state.event.parentLoc = self.state.event.parentLoc + "/" + self.state.event.comingFrom
            self.state.uiInfo.info.renderedStates.append(omniComponent)
        self.state.layout = widgets.Box([comp.state.layout for comp in self.state.uiInfo.info.renderedStates])
        self.state.layout.add_class(self.state.uiInfo.className)

    def update_layout(self):
        self.state.layout.value = self.state.uiInfo.info.value
@dataclass
class DataStructureForIpyWidget:
    params = {}
    handlersInitializer = None
    typeOfWidget = IpywidgetsComponentsEnum.Label
class IpywidgetComponent:
    def __init__(self):
        self.state_default = self.get_default_state()
        self.set_state(self.state_default)
    def get_default_state(self):
        state = Utils.get_state()
        state.uiInfo.info = DataStructureForIpyWidget()
        state.event.comingFrom = "IpywidgetComponent/"+ state.uiInfo.info.typeOfWidget.name
        state.uiInfo.className = "IpywidgetComponent"+ state.uiInfo.info.typeOfWidget.name + "2134"
        state.uiInfo.uiType = ComponentsLib.Ipywidget
        return state
    def set_state(self, state):
        self.state = state
    def render(self):
        if self.state.uiInfo.info.typeOfWidget.value == IpywidgetsComponentsEnum.Label.value:
            self.state.layout = widgets.Label(**self.state.uiInfo.info.params)
        elif self.state.uiInfo.info.typeOfWidget.value == IpywidgetsComponentsEnum.Button.value:
            self.state.layout = widgets.Button(**self.state.uiInfo.info.params)
        else:
            raise NotImplementedError("Component Does not exists")
        if self.state.uiInfo.info.handlersInitializer:
            self.state.uiInfo.info.handlersInitializer(self.state)
        if self.state.uiInfo.className.strip() != "":
            self.state.layout.add_class(self.state.uiInfo.className)
    def update_layout(self):
        for key in self.state.uiInfo.info.params:
            val = self.state.uiInfo.info.params[key]
            setattr(self.state.layout, key, val)

def makeStructure(comingFrom ="", className = "", info={}, uiType = ComponentsLib.Label, isChild=True):
    state = DataStructureForUIComponent()
    
    state.event = DataStructureForEventSystem()
    
    if(not isChild):
        state.cssStyling = CssStyling()
        state.cssStyling.css_adder = AddCSSWidget()
        state.cssStyling.css_adder.content = state.cssStyling.css_properties
        state.event.instance = EventEmitter()
    
    state.event.comingFrom = comingFrom
    state.uiInfo = UIInfo()
    state.uiInfo.className = className
    if type(info) == dict and len(info) != 0:
        info = NestedNamespaceUpdated(info)
    state.uiInfo.info = info
    state.uiInfo.uiType = uiType
    return state
@dataclass
class DataStructureForBreadCrumb:
    linksArray = [] #[str, str] or [(str, any), (str, any)] 
    prefixToInnerClassNames = ""
class BreadCrumbComponent:
    def __init__(self):
        self.state_default = self.get_default_state()
        self.set_state(self.state_default)
    def get_default_state(self):
        state = Utils.get_state()
        state.uiInfo.info = DataStructureForBreadCrumb()
        state.event.comingFrom = "BreadCrumb"
        state.uiInfo.className = "BreadCrumb"
        state.uiInfo.uiType = ComponentsLib.BreadCrumb
        return state
    def set_state(self, state):
        self.state = state
    def render(self):
        pre = self.state.uiInfo.info.prefixToInnerClassNames
        
        comps = []
        for i, ele in enumerate(self.state.uiInfo.info.linksArray):
            key = ele
            val = i
            if type(ele) == tuple:
                key, val = ele
            struct = makeStructure(comingFrom="bread-crumb-item", className="links"+ pre, info={"params": ValsWrapper({"description": key}), 
                            "typeOfWidget":IpywidgetsComponentsEnum.Button, "handlersInitializer": None}, uiType=ComponentsLib.Ipywidget)
            sep = makeStructure(comingFrom="separator", className="separator" + pre, info= {"value": "/"}, uiType=ComponentsLib.Label)
            if i != 0:
                comps.append(sep)
            comps.append(struct)
            
        breadCrumb = OmniComponentUI()
        breadCrumb.set_state(makeStructure(comingFrom=self.state.event.comingFrom, className="bread-crumb-main" + pre, uiType=ComponentsLib.Repeater ,info= {"inp_components": comps,
            "renderedStates": []}, isChild=False))
        breadCrumb.render()
        self.state.cssStyling.css_adder.content = f"""
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
        self.state.layout = breadCrumb.state.layout
        self.state.uiInfo.instance = breadCrumb
        
    def update_layout(self):
        self.render()
    def _add_click_handler(self, state):
        state.layout._key = state
        state.layout.on_click(self._click)
    def _click(self, wid):
        state = wid._key
        self.state.event.emit("all", {"widget": wid, "loc": (self.state.event.parentLoc + "/" + self.state.event.comingFrom + "/" +state.event.comingFrom).strip("/"), "type": "clicked"})
class Main: 
    def example1():
        bc = OmniComponentUI()
        bc.set_state(makeStructure(comingFrom="repeaterTest", className="auwom", uiType=ComponentsLib.Repeater ,info= {"inp_components": [
            makeStructure(comingFrom="label", className="label", info= {"value": "super"}, uiType=ComponentsLib.Label),
            makeStructure(comingFrom="button-item", className="btn", info= {"description": "hloo"}, uiType=ComponentsLib.Button),
            makeStructure(comingFrom="button-item", className="btn", info= {"description": "coole"}, uiType=ComponentsLib.Button),
            makeStructure(comingFrom="button-item", className="btn", info= {"description": "asdaw"}, uiType=ComponentsLib.Button),
            makeStructure(comingFrom="ipylabel", className="idont", info={"params": ValsWrapper({"value": "kk"}), "typeOfWidget": IpywidgetsComponentsEnum.Label, 
                                                                          "handlersInitializer": None}, uiType=ComponentsLib.Ipywidget)
        ], "renderedStates": []}, isChild=False))
        bc.render()
        bc.state.event.instance.on("all", print)
        bc.state.layout
        return bc    
    def jsonOrDicExplorer():
        bc = OmniComponentUI()
        bc.set_state(makeStructure(comingFrom="page", className="PageContent", uiType=ComponentsLib.Repeater ,info= {"inp_components": [
            makeStructure(comingFrom="tile", className="title-header", info= {"value": "super"}, uiType=ComponentsLib.Label),
            makeStructure(comingFrom="PageBody", className="PageBody", uiType=ComponentsLib.Repeater ,info= {"inp_components": [
                makeStructure(comingFrom="Navigation", className="Naviagtion", uiType=ComponentsLib.Repeater ,info= {"inp_components": [
                    makeStructure(comingFrom="Navigation-Cut-Menu", className="Menu-items", info={"params": ValsWrapper({"icon": "cut"}), "typeOfWidget": 
                                                                    IpywidgetsComponentsEnum.Button, "handlersInitializer": None}, uiType=ComponentsLib.Ipywidget),
                    
                    makeStructure(comingFrom="Navigation-Cut-Menu", className="Menu-items", info={"params": ValsWrapper({"icon": "paste"}), "typeOfWidget": 
                                                                    IpywidgetsComponentsEnum.Button, "handlersInitializer": None}, uiType=ComponentsLib.Ipywidget),
                ], "renderedStates": []}),
                makeStructure(comingFrom="PageBodyContent", className="PageBodyContent", uiType=ComponentsLib.Repeater ,info= {"inp_components": [
                    makeStructure(comingFrom="breadcrumb", className="breadcrumb", info= {"value": "breadcrumb"}, uiType=ComponentsLib.Label),

                ], "renderedStates": []})

            ], "renderedStates": []})
        ], "renderedStates": []}, isChild=False))
        bc.render()
        bc.state.event.instance.on("all", print)
        bc.state.cssStyling.css_adder.content = """
        .PageContent{
            width: 100%;
            height: 400px;
            flex-direction: column;
            border: 1px solid gray;
        }
        .title-header{
            font-size: 2rem;
            height: 3rem;
            border-bottom: 1px solid gray;
            align-items: center;
            margin: 0;
            padding-left: 2rem;

        }
        .Menu-items{
            width: 3rem;
            height: 3rem;
            font-size: 2rem;
            color: #86A7FC;
            border-radius: 2px;
            background-color: unset;
        }
        .Naviagtion{
            flex-direction: column;
            height: 100%;
            border-right: 1px solid gray;
        }
        .PageBody{
            height: 100%;
        }
        """
        bc.state.layout
        return bc