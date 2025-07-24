from modules.Explorer.personalizedWidgets import GenerateNRowsBox
import ipywidgets as widgets
from useful.jupyterDB import jupyterDB
class IOpsBtn:
    def display(self):
        pass
class ButtonsWithParent:
    def set_view(self, view):
        self._gnrb = view
    def set_parent(self, parent):
        self._parent = parent
class DisplayOps(IOpsBtn, ButtonsWithParent):
    def display(self):
        row2 = self._gnrb.get_child(1)
        out = row2.get_child(0)
        section = self._gnrb.get_child(0).get_child(0)
        jupyterDB.startUp().Ops().__dict__[section.value]().display()
class UpdateOps(IOpsBtn, ButtonsWithParent):
    def __init__(self):
        self._update_btn = widgets.Button(description="update", layout= widgets.Layout(width="auto"))
        self._update_btn.on_click(self._confirm)
        self._text_field = widgets.Textarea(layout={'width':'auto'})
        self._confirmer = Confirmer()
        self._confirmer.set_callback(self._callback)
    def _confirm(self, btn):
        out = self._gnrb.get_child(1).get_child(0)
        with out:
            self._confirmer.display()
    def display(self):
        out = self._gnrb.get_child(1).get_child(0)
        out.clear_output()
        section = self._gnrb.get_child(0).get_child(0)
        self._text_field.value = "\n".join(jupyterDB.startUp().Ops().__dict__[section.value]().getContent())
        with out:
            display(widgets.HBox([self._text_field, self._update_btn]))
    def _callback(self, btn):
        content = self._text_field.value
        section = self._gnrb.get_child(0).get_child(0)
        jupyterDB.startUp().Ops().__dict__[section.value]().delete("1:-1")
        jupyterDB.startUp().Ops().__dict__[section.value]().add(content)
        self.display()
class Confirmer(IOpsBtn):
    def __init__(self):
        self._confirm_btn = widgets.Button(description="confirm", layout= widgets.Layout(width="auto"))
    def set_callback(self, callback):
        self._callback = callback
        self._confirm_btn.on_click(self._callback)
    def display(self):
        display(self._confirm_btn)
class DeleteOps(IOpsBtn,ButtonsWithParent):
    def __init__(self):
        self._area = widgets.Text(placeholder="int or range(1:2)")
        self._del_btn = widgets.Button(description="delete", layout={"width": "auto"})
        self._del_btn.on_click(self._confirm)
        self._confirmer = Confirmer()
        self._confirmer.set_callback(self._callback)
        
    def set_confirmer(self, conformer: Confirmer):
        self._confirmer = conformer
        self._confirmer.set_callback(self._callback)
    def _confirm(self, btn):
        out = self._gnrb.get_child(1).get_child(0)
        with out:
            self._confirmer.display()
    def display(self):
        out = self._gnrb.get_child(1).get_child(0)
        out.clear_output()
        with out:
            self._parent._ops['display'].display()
            display(widgets.HBox([self._area, self._del_btn]))
    def _callback(self, btn):
        content = self._area.value.strip()
        if content =="":
            return 
        if ":" not in content:
            content = int(content)
        section = self._gnrb.get_child(0).get_child(0)
        jupyterDB.startUp().Ops().__dict__[section.value]().delete(content)
        self.display()
class StartUpGUI:
    def __init__(self):
        self._out = widgets.Output()
        self._ops = {
            'display' : DisplayOps(),
            'update': UpdateOps(),
            'delete': DeleteOps()
        }
        self._make_layout()
    def _make_layout(self):
        self._gnrb = GenerateNRowsBox(2)
        for v in self._ops.values():
            v.set_view(self._gnrb)
            v.set_parent(self)
        row = self._gnrb.get_child(0)
        row.add_widget(widgets.Dropdown(options=['office', 'home', 'both'], 
                                description="section", 
                                layout=widgets.Layout(width='20%')))
        row.add_widget(widgets.Dropdown(options=['display', 'delete', 'update'], 
                                description="ops", 
                                layout=widgets.Layout(width='20%')))
        row.add_widget(widgets.Button(description="ok", layout=widgets.Layout(width='auto')))
        row2 = self._gnrb.get_child(1)
        row2.add_widget(self._out)        
        btn = row.get_child(2).on_click(self._okey)
    def _okey(self, btn):
        self._out.clear_output()
        row = self._gnrb.get_child(0)
        with self._out:
            self._ops[row.get_child(1).value].display()
    def display(self):
        return self._gnrb.get()