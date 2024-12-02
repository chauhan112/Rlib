import datetime
import ipywidgets as widgets
from timeline.t2023.advance_pickle_crud import Main as KeyValueAdderView
from timeline.t2023.viewsCollection import Main as ViewsCollection

class SingleButtonController:
    def __init__(self, **kwargs):
        self.layout = widgets.Button(**kwargs)
        self.layout.on_click(self._btn_clicked)
        self.set_clicked_func(self._do_nothing)
    def _do_nothing(self, wid):
        pass
    def set_clicked_func(self, func):
        self._clicked_func = func
    def _btn_clicked(self, wid):
        self._clicked_func(wid)
        
class IComponent:
    def clear(self):
        raise NotImplementedError("abstract method")
    def value(self):
        raise NotImplementedError("abstract method")
    def process_info(self):
        raise NotImplementedError("abstract method")
    def layout(self):
        raise NotImplementedError("abstract method")
    def set_value(self, val):
        raise NotImplementedError("abstract method")
    def is_empty(self):
        raise NotImplementedError("abstract method")
    def set_info(self, infos):
        raise NotImplementedError("abstract method")
class GComponent(IComponent):
    def set_widget(self, wid):
        self._widget = wid
    def set_info(self, infos):
        self._infos = infos
    def layout(self):
        return self._widget
    def set_value(self, val):
        self._widget.value = val
    def is_empty(self):
        return True
class IPyWidget(GComponent):
    def default_funcs(self):
        self.set_info({})
        self.set_reset_func(self._default_value_resetter_func)
        self.set_value_getter_func(self._default_value_getter_func)
        self.set_info_processor(self.default_processor_func)
    def default_processor_func(self, wid):
        k = "disabled"
        if k in self._infos:
            wid.disabled = self._infos[k]
    def set_reset_func(self, func):
        self._reset_func = func
    def _default_value_getter_func(self, wid):
        return wid.value
    def _default_value_resetter_func(self, wid):
        wid.value = ""
    def set_value_getter_func(self, func):
        self._value_getter_func = func
    def value(self):
        return self._value_getter_func(self._widget)
    def clear(self):
        self._reset_func(self._widget)
    def set_info_processor(self, processor_func):
        self._processor_func= processor_func
    def process_info(self):
        self._processor_func(self._widget)
class TextInput(IPyWidget):
    def __init__(self, **kwargs):
        self.default_funcs()
        self.set_widget(widgets.Text(**kwargs))
    def is_empty(self):
        return self._widget.value.strip() == ""
class TextAreaInput(IPyWidget):
    def __init__(self, **kwargs):
        self.default_funcs()
        self.set_widget(widgets.Textarea(**kwargs))
    def is_empty(self):
        return self._widget.value.strip() == ""
class DateInput(IPyWidget):
    def __init__(self, **kwargs):
        self.default_funcs()
        self.set_widget(widgets.DatePicker(**kwargs))
        self.set_reset_func(self._clear_func)
        self.set_current_value_func(self._default_current_value_func)
        self.set_info_processor(self._info_processor)
    def set_current_value_func(self, val_func):
        self._value_func = val_func
    def _clear_func(self, wid):
        wid.value = None
    def _default_current_value_func(self, wid):
        now = datetime.datetime.now()
        wid.value = now
    def _info_processor(self, wid):
        self.default_processor_func(wid)
        k = "auto"
        if k in self._infos and self._infos[k]:
            self._value_func(self._widget)
            self.set_reset_func(self._value_func)
class GTimeDate(IPyWidget):
    def clear(self):
        self._datetime.clear()
    def value(self):
        return self._datetime.value()
    def process_info(self):
        self._datetime.set_info(self._infos)
        self._datetime.process_info()
    def layout(self):
        return self._datetime._widget
    def set_value(self, val):
        self._datetime.set_value(val)
class TimeInput(GTimeDate):
    def __init__(self, **kwargs):
        self._datetime = DateInput()
        self._datetime.set_widget(widgets.TimePicker(**kwargs))
        self._datetime.set_current_value_func(self._current_value_func)
    def _current_value_func(self, wid):
        now = datetime.datetime.now()
        wid.value = datetime.time(now.hour, now.minute)
class DateTimeInput(GTimeDate):
    def __init__(self, **kwargs):
        self._datetime = DateInput()
        self._datetime.set_widget(widgets.NaiveDatetimePicker(**kwargs))
class BooleanOptionInput(IPyWidget):
    def __init__(self, **kwargs):
        self.default_funcs()
        self.set_widget(widgets.Checkbox(**kwargs))
        self.set_reset_func(self._reset_funcx)
    def _reset_funcx(self, wid):
        wid.value = False
class MultipleSelect(GComponent):
    def __init__(self, **kwargs):
        ly, self._controller = ViewsCollection.get_list_maker()
        self._description = widgets.Label(kwargs["description"], 
            layout={"width":"80px", "justify_content":"flex-end", "margin":"0px 8px 0px 0px"})
        self.set_widget(widgets.HBox([self._description, ly]))
        ly.add_class("w-fit")
    def clear(self):
        self._controller.set_model([])
        self._controller.reset()
    def value(self):
        return self._controller._model
    def process_info(self):
        pass
    def set_value(self, val):
        self._controller.set_model(val)
        self._controller.update()
    def is_empty(self):
        return len(self.value()) == 0
class DropdownInput(IPyWidget):
    def __init__(self, **kwargs):
        self.default_funcs()
        self.set_widget(widgets.Dropdown(**kwargs))
        self.set_reset_func(self._resett_func)
        self.set_info_processor(self._process_info)
    def _resett_func(self, wid):
        wid.value = None
    def _process_info(self, wid):
        self.default_processor_func(wid)
        k = "options"
        if k in self._infos:
            wid.options = self._infos[k]
class KeyValueInput(GComponent):
    def __init__(self, **kwargs):
        ly, self._controller = KeyValueAdderView.keyValueCrud({})
        ly.add_class("w-fit")
        self._controller._basic._view.opsView.valueTextareaWidg.layout.width =""
        self._controller._basic._view.opsView.valueTextareaWidg.add_class("w-100")
        self._controller._basic._view.opsView.valueTextareaWidg.add_class("textarea-h-150px")
        self._controller._basic._view.opsRow.add_class("grid")
        self._controller._basic._view.opsRow.add_class("grid-column-repeat-auto-7")
        self._controller._basic._view.opsView.value._hbox.add_class("order-1")
        self._controller._basic._view.opsView.value._hbox.add_class("span-all-columns")
        self._controller._basic._view.opsView.value._hbox.add_class("w-100")
        self._controller._basic._view.opsView.valueWidg.layout.width =""
        self._controller._basic._view.opsView.valueWidg.add_class("w-100")
        self._description = widgets.Label(kwargs["description"], 
            layout={"width":"80px", "justify_content":"flex-end", "margin":"0px 8px 0px 0px"})
        self.set_widget(widgets.HBox([self._description, ly]))
    def clear(self):
        self._controller._basic._model.set_dictionary({})
        self._controller._update_keys()
    def value(self):
        return self._controller._basic._model.content
    def process_info(self):
        pass
    def set_value(self, val):
        self._controller._basic._model.set_dictionary(val)
        self._controller._update_keys()
    def is_empty(self):
        return len(self.value()) == 0
