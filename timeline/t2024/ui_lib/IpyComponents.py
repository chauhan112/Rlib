from timeline.t2024.experiments.morphism.withCIT.morphismWithCIT import IpywidgetsComponentsEnum, ComponentsLib
from basic import NameSpace
import ipywidgets as widgets
from modules.SearchSystem.modular import HideableWidget
class BaseComponentV2:
    def __init__(self):
        self.outputs = NameSpace()
        self.inputs = NameSpace()
        self.inputs.parent = None
        self.inputs.bind = True
        self.inputs.customCss = ""
        self.state = NameSpace()
        self.inputs.className = ""
        self.handlers = NameSpace()
        self.handlers.defs = NameSpace()
        self.handlers.defs.wrapper = self._handler_wrapper
        self.handlers.handle = self._def_handler
        self.handlers.defs.handle = self._def_handler
    def set_inputs(self, **args):
        for key in args:
            val = args[key]
            setattr(self.inputs, key, val)
    def _def_handler(self, wid):
        print(wid)
    def _handler_wrapper(self, wid):
        self.handlers.handle(wid)
    def hide(self):
        HideableWidget.hideIt(self.outputs.layout)
    def show(self):
        HideableWidget.showIt(self.outputs.layout)
    def update_classes(self):
        if self.inputs.className:
            for clsName in self.inputs.className.split():
                self.outputs.layout.add_class(clsName)
class IpywidgetComponentV2(BaseComponentV2):
    def render(self):
        if self.inputs.typeOfWidget == IpywidgetsComponentsEnum.Button:
            self.outputs.layout = widgets.Button(**self.inputs.params)
            self.outputs.layout.on_click(self.handlers.defs.wrapper)
        elif self.inputs.typeOfWidget == IpywidgetsComponentsEnum.Output:
            self.outputs.layout = widgets.Output(**self.inputs.params)
        elif self.inputs.typeOfWidget == ComponentsLib.ListAndJsonNavigator:
            from timeline.t2023.advance_pickle_crud import Main as KeyValueAdderView
            self.outputs.layout, self.state.controller = KeyValueAdderView.keyValueCrud({})
        elif self.inputs.typeOfWidget == ComponentsLib.CSSAdder:
            from timeline.t2024.ui_lib.components.cssAdder import AddCSSWidget
            self.outputs.layout = AddCSSWidget()
            self.outputs.layout.content = self.inputs.customCss
        elif self.inputs.typeOfWidget == ComponentsLib.CustomOutput:
            from modules.Explorer.personalizedWidgets import CustomOutput
            self.state.controller = CustomOutput()
            self.outputs.layout = self.state.controller.get_layout()
        elif self.inputs.typeOfWidget == ComponentsLib.ListNavigator:
            from timeline.t2023.viewsCollection import Main as ViewsCollection
            self.outputs.layout, self.state.controller = ViewsCollection.get_list_maker()
        elif self.inputs.typeOfWidget == ComponentsLib.IpyWrapper:
            self.outputs.layout = self.inputs.value
        else:
            self.outputs.layout = getattr(widgets, self.inputs.typeOfWidget.name)(**self.inputs.params)
            if self.inputs.bind:
                self.outputs.layout.observe(self.handlers.defs.wrapper, ["value"])
        self.outputs.layout._parent = self
        self.update_classes()
    def update_layout(self):
        for key in self.inputs.params:
            val = self.inputs.params[key]
            setattr(self.outputs.layout, key, val)
class RepeaterComponentV2(BaseComponentV2):
    def _def_handler_wrapper(self, wid):
        self.state.selected = wid
        self.handlers.handle(wid)
    def render(self):
        self.outputs.renderedStates = []
        self.handlers.defs.wrapper = self._def_handler_wrapper
        for omniComponent in self.inputs.inp_components:
            self._child_prep(omniComponent)
            omniComponent.inputs.parent = self
            self.outputs.renderedStates.append(omniComponent)
        self.outputs.layout = widgets.Box([comp.outputs.layout for comp in self.outputs.renderedStates])
        self.update_classes()
    def update_layout(self):
        for comp in self.outputs.renderedStates:
            comp.update_layout()
    def append(self, omniComponent):
        self._child_prep(omniComponent)
        omniComponent.inputs.parent = self
        self.outputs.renderedStates.append(omniComponent)
        self.outputs.layout.children = [comp.outputs.layout for comp in self.outputs.renderedStates]
    def pop(self):
        popped = self.outputs.renderedStates.pop()
        self.outputs.layout.children = [comp.outputs.layout for comp in self.outputs.renderedStates]
        return popped
    def _child_prep(self, omniComponent):
        if omniComponent.handlers.handle != omniComponent.handlers.defs.wrapper:
            omniComponent.handlers.handle = self.handlers.defs.wrapper
    def clear(self):
        self.outputs.renderedStates.clear()
        self.outputs.layout.children = [comp.outputs.layout for comp in self.outputs.renderedStates]
class Utils:
    def get_comp(infos, typ, **args):
        ic = IpywidgetComponentV2()
        ic.set_inputs(params = infos, typeOfWidget= typ, **args)
        ic.render()
        return ic
    def container(comps, **args):
        rc = RepeaterComponentV2()
        rc.set_inputs(inp_components = comps, **args)
        rc.render()
        return rc
    def wrapper(wid):
        bc = BaseComponentV2()
        bc.outputs.layout = wid
        return bc