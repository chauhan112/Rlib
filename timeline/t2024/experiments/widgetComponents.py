import anywidget
import traitlets
import ipywidgets as widgets
from pymitter import EventEmitter
from timeline.t2024.ui_lib.components.cssAdder import AddCSSWidget
from dataclasses import dataclass

class CSSClassable:
    def __init__(self):
        self.className = None
    def assign_random_class_name(self):
        if self.className is None:
            from CryptsDB import CryptsDB
            self.className = "css" +  CryptsDB.generateUniqueId()
class TextWidget(anywidget.AnyWidget):
    _esm = """export function render({ model, el }) {
    const textNode = document.createTextNode(model.get("r_name"));
    let container = document.createElement("div");
    container.appendChild (textNode)

    container.style.cssText = model.get("r_cssText")
    model.on("change:r_name", () => {
        container.innerHTML = model.get("r_name");
    });
    model.on("change:r_cssText", () => {
        container.style.cssText = model.get("r_cssText");
    });
    el.appendChild(container);
    }
    """
    r_name = traitlets.Unicode(default_value="Button").tag(sync=True)
    r_cssText = traitlets.Unicode(default_value="").tag(sync=True)
class TextWidgetWithClick(anywidget.AnyWidget):
    _esm = """export function render({ model, el }) {
    const textNode = document.createTextNode(model.get("r_name"));
    let tag = model.get("r_tag");
    let container = document.createElement(tag);
    
    container.appendChild (textNode)
    let a = new Set(model.get("r_events"))
    if (a.has("click")){
        container.addEventListener("click", () => {
            let val = model.get("r_eventType")
            let words = val.split("-")
            let count = 0
            if (words.length > 1){
                count = Number(words[1])
            }
            count += 1
            model.set("r_eventType", `clicked-${count}`);
            model.save_changes();
        });
    }
    let updateProperties = () => {
        let properties = model.get("r_properties")
        for (let member in properties){
            let val = properties[member]
            container.setAttribute(member, val)
        }
    };
    updateProperties()
    model.on("change:r_name", () => {
        container.innerHTML = model.get("r_name");
    });
    model.on("change:r_properties_changed", () => {
        updateProperties()
    });
    el.appendChild(container);
    }
    """
    r_eventType = traitlets.Unicode().tag(sync=True)
    r_name = traitlets.Unicode(default_value="Button").tag(sync=True)
    r_state = None
    r_events = traitlets.List(default_value=[]).tag(sync = True)
    r_tag = traitlets.Unicode(default_value="span").tag(sync=True)
    r_properties = traitlets.Dict(default_value={}).tag(sync = True)
    r_properties_changed = traitlets.Int(0).tag(sync = True)
class PlaceHolderWidget(anywidget.AnyWidget):
    _esm = """export function render({ model, el }) {
    let container = document.createElement("div");
    container.innerHTML = model.get("r_innerHtml")
    let a = new Set(model.get("r_events"))
    if (a.has("click")){
        container.addEventListener("click", () => {
            let val = model.get("r_eventType")
            let words = val.split("-")
            let count = 0
            if (words.length > 1){
                count = Number(words[1])
            }
            count += 1
            model.set("r_eventType", `clicked-${count}`);
            model.save_changes();
        });
    }
    let updateProperties = () => {
        let properties = model.get("r_properties")
        for (let member in properties){
            let val = properties[member]
            container.setAttribute(member, val)
        }
    };
    updateProperties()
    model.on("change:r_innerHtml", () => {
        container.innerHTML = model.get("r_innerHtml");
    });
    model.on("change:r_properties_changed", () => {
        updateProperties()
    });
    el.appendChild(container);
    }
    """
    r_eventType = traitlets.Unicode().tag(sync=True)
    r_state = None
    r_properties = traitlets.Dict(default_value={}).tag(sync = True)
    r_properties_changed = traitlets.Int(0).tag(sync = True)
    r_innerHtml = traitlets.Unicode(default_value="").tag(sync=True)
    r_events = traitlets.List(default_value=[]).tag(sync = True)
@dataclass
class DataStructureForPlaceholderWidget:
    tag_properties = {}
    layout = None
    className = "placeholder"
    css_properties = ""
    emitter = None
    css_adder = None
    innerHtml = "<span> Hello There </span>"
class PlaceholderWrapper:
    def __init__(self):
        self.state_default = self.get_default_state()
        self.set_state(self.state_default)
    def set_state(self, state):
        self.state = state
    def get_default_state(self):
        state = DataStructureForPlaceholderWidget()
        state.css_properties = f"""
            .{state.className}{{
                display: block;
                padding: 10px 10px;
                background-color: #e9ecef;
                border-radius: 4px;
            }}
        """
        state.css_adder = AddCSSWidget()
        state.css_adder.content = state.css_properties
        state.emitter = EventEmitter()
        return state
    def get_layout(self):
        if self.state.layout is None:
            self.state.layout = PlaceHolderWidget(r_events= ["click"])
            self.state.layout.r_innerHtml = self.state.innerHtml
            self.state.layout.observe(self._clicked, ["r_eventType"])
            self.state.layout.add_class(self.state.className)
        return self.state.layout
    def _clicked(self, payload):
        self.state.emitter.emit("clicked", payload)
@dataclass
class DataStructureForCustomButton:
    name = "Button"
    css_properties = ""
    placeHolder = None
    width = None
    className = "Button-101"
    layout = None
    payload = None
class CustomButton:
    def __init__(self):
        self.state_default = self.get_default_state()
        self.set_state(self.state_default)
    def set_state(self, state):
        self.state = state
    def get_default_state(self):
        state = DataStructureForCustomButton()
        state.placeHolder = PlaceholderWrapper()
        state.placeHolder.state.className = state.className
        state.placeHolder.get_layout()
        state.placeHolder.state.layout.r_properties = {"class":state.className}
        state.css_properties = f"""
        .{state.className}{{
            display: block;
            padding: 10px 10px;
            background-color: #e9ecef;
            border-radius: 4px;
            width: fit-content;
            user-select: none;
        }}
        """
        state.placeHolder.state.layout.css_properties = state.css_properties
        state.placeHolder.state.layout.r_innerHtml = state.name
        if state.width:
            state.placeHolder.state.r_properties["style"] = "width:" + state.width
        state.placeHolder.state.css_adder.content = state.css_properties
        return state
    def get_layout(self):
        if self.state.layout is None:
            self.state.layout = self.state.placeHolder.state.layout
        return self.state.layout
@dataclass
class DataStructureForBreadCrumb:
    tag_properties = {}
    layout = None
    className = "breadcrumb"
    classItem = "breadcrumb-item"
    data = [] # holds the input of the widgets
    crumbsWidget = []
    separator = None
    css_properties = ""
    emitter = None
    css_adder = None
class BreadCrumb:
    def __init__(self):
        self.state_default = self.get_default_state()
        self.set_state(self.state_default)
    def get_default_state(self):
        state = DataStructureForBreadCrumb()
        state.separator =  Main.text("/")
        state.separator.r_properties = {"style": "display: inline-block;color:#6c757d; padding-right: 0.5rem;padding-left: 0.5rem;"}
        state.css_properties = f"""
            .{state.className}{{
                display: flex;
                padding: 10px 10px;
                margin-bottom: 10px;
                background-color: #e9ecef;
                border-radius: 4px;
            }}

            .{state.classItem}{{
                cursor:pointer;
            }}
        """
        state.emitter = EventEmitter()
        state.css_adder = AddCSSWidget()
        state.css_adder.content = state.css_properties
        return state
    def set_state(self, state):
        self.state = state
    def get_layout(self):
        if self.state.layout is None:
            self.state.crumbsWidget.clear()
            for label, val in self.state.data:
                wid = Main.text(label, ["click"])
                wid.state = [label, val]
                wid.r_properties = self.state.tag_properties
                wid.add_class(self.state.classItem)
                wid.observe(self._clicked, ["r_eventType"])
                self.state.crumbsWidget.append(wid)
                self.state.crumbsWidget.append(self.state.separator)
            if len(self.state.crumbsWidget) != 0:
                self.state.crumbsWidget.pop()
            self.state.layout = widgets.HBox(self.state.crumbsWidget)
            self.state.layout.add_class(self.state.className)
        return self.state.layout
    def add(self, label, val = None):
        if val is None:
            val = label
        self._data.append((label, val))
    def _clicked(self, state):
        self.state.emitter.emit("clicked", state)
@dataclass
class DataStructureForEventSystem:
    instance = None
    comingFrom = ""
    parentLoc = ""
@dataclass
class DataStructureForPagination:
    event = DataStructureForEventSystem()
    uiComponents = None
    leftLabel = "..."
    rigthLabel = "..."
    maxLabel = "pMax"
    cssAdder = None
    css_properties = ""
    className = "Pagination"
    selected_button = None
    selected_button_class_name = "pagination-selected"
class PaginationWidget:
    def __init__(self):
        box_layout = widgets.Layout(display='flex',flex_flow='row', align_items='stretch')
        self.btns = [widgets.Button(description =str(i+1),layout={"width": "auto"}) for i in range(5)]
        self.btnsWrapper = widgets.HBox(self.btns)
        self.pageLeft = widgets.Button(description="prev", layout={"width":"auto"})
        self.pageMax = widgets.Label("pMax")
        self.pageRight = widgets.Button(description="next", layout={"width":"auto"})
        self.pageTxt = widgets.BoundedIntText( min=0, max=2,layout ={"width":"80px"} )
        self.gotoPage = widgets.Button(description="go", layout={"width":"auto"})
        self.layout = widgets.HBox([self.pageLeft, self.btnsWrapper ,self.pageRight,self.pageMax,
                                    self.pageTxt, self.gotoPage], layout=box_layout)
class PaginationWidgetWrapper:
    def __init__(self):
        self.default_state = self.get_default_state()
        self.set_state(self.default_state)
        self.update_layout()
        self._clicked_bounded = False
    def get_default_state(self):
        state = DataStructureForPagination()
        state.uiComponents = PaginationWidget()
        state.event.instance = EventEmitter()
        state.event.comingFrom = "Pagination"
        state.css_properties = """
            .Pagination{
                width: 100%;
                background-color: unset;
                display: flex;
                justify-content: center;

            }
            .goto-page,.page-button{
                background-color: unset;
                color: #007bff;
            }
            .goto-page{
                background-color: #007bff;
                color: white;
            }
            .page-button:focus:enabled{
                outline: 0;

            }
            .page-nr-input input{
                color: #007bff;
            }
            """ + f"""
            .{state.selected_button_class_name}{{
                background-color: #007bff;
                color: white;
            }}
        """

        state.cssAdder = AddCSSWidget()
        return state
    def set_state(self, state):
        self.state = state
    def update_layout(self):
        self.state.uiComponents.layout.add_class(self.state.className)
        self.state.cssAdder.content = self.state.css_properties
        self.state.uiComponents.pageLeft.add_class("page-button")
        self.state.uiComponents.pageRight.add_class("page-button")
        self.state.uiComponents.gotoPage.add_class("goto-page")
        self.state.uiComponents.pageMax.add_class("max-page")
        for btn in self.state.uiComponents.btns:
            btn.add_class("page-button")
    def get_layout(self):
        if not self._clicked_bounded:
            self.setup()
        return self.state.layout
    def setup(self):
        self._clicked_bounded = True
        for btn in self.state.uiComponents.btns:
            btn.on_click(self._clicked)
        self.state.uiComponents.pageLeft.on_click(lambda x: self.state.event.instance.emit("clicked", {"type": "pageLeft", "button": x}))
        self.state.uiComponents.pageRight.on_click(lambda x: self.state.event.instance.emit("clicked", {"type": "pageRight", "button": x}))
        self.state.uiComponents.gotoPage.on_click(lambda x: self.state.event.instance.emit("clicked", {"type": "gotoPage", "button": x}))
    def _clicked(self, wid):
        if self.state.selected_button is not None:
            self.state.selected_button.remove_class(self.state.selected_button_class_name)
        self.state.event.instance.emit("clicked", wid)
        self.state.selected_button = wid
        self.state.selected_button.add_class(self.state.selected_button_class_name)
@dataclass
class DataStructureForJSONExplorer:
    event = DataStructureForEventSystem()
    breadCrumbs = None
    pagination = None
    uiComponents = None
    cssAdder = None
    css_properties = ""
    className = "JSONExplorer"
class ExplorerGUIForJSON:
    def __init__(self):
        self.breadcrum = BreadCrumb()
        self.pagination = PaginationWidgetWrapper()
        self.add_btn = Main.iconButton()
        self.result_buttons = []
        self.output_area = widgets.Output()
        self.output_area.add_class("ExplorerGUIForJSON-output")
        self.headerTitle = widgets.Label()
        self.headerTitle.add_class("ExplorerGUIForJSON-label")
        self.navigation = widgets.Box()
        self.navigation.add_class("ExplorerGUIForJSON-navigation")
        self.body = widgets.Box()
        self.body.add_class("ExplorerGUIForJSON-body")
class ExplorerGUIForJSONWrapper:
    def __init__(self):
        self.default_state = self.get_default_state()
        self.set_state(self.default_state)
        self.update_layout()
        self._clicked_bounded = False
    def get_default_state(self):
        state = DataStructureForJSONExplorer()
        state.cssAdder = AddCSSWidget()
        return state
    def set_state(self, state):
        self.state = state
    def update_layout(self):
        pass
    def get_layout(self):
        pass
    def setup(self):
        pass
    def _clicked(self, wid):
        pass

class Main:
    def text(label, events = None):
        tw = TextWidgetWithClick()
        if events:
            tw.r_events = events
        tw.r_name = label
        return tw
    def breadCrumbExample():
        bc = BreadCrumb()
        bc.state.data = [("a", "a"), ("bas", "asb")]
        bc.get_layout()        
        return bc
    def iconButton():
        phww = PlaceholderWrapper()
        phww.state.innerHtml = '<i class="fa fa-plus center"></i>'
        phww.state.css_adder.content = f"""
            .{phww.state.className}{{
                height: 3rem;
                display: flex;
                align-items: center;
                justify-content: center;
                width: 3rem;
                background-color: #EEF5FF;
                user-select: none;
                border-radius: 4px;
                font-size: 2rem;
                color: #86B6F6;
                transition: color 0.1s ease-out;
            }}
            .{phww.state.className}:active{{
                background-color: #B4D4FF;
                color: #86B6F6;
            }}

            .{phww.state.className}:hover{{
                color: #176B87;
            }}
        """
        return phww
