import ipywidgets as widgets
import time
class IModel:
    def set_value(self, key, value):
        raise NotImplementedError("not implemented error")
class PklFile(IModel):
    def __init__(self, file= None):
        if file is not None:
            self.set_file(file)
    def set_file(self, file):
        from nice_design.dicrud import DictionaryCRUD
        self._dc = DictionaryCRUD()
        self._file_path = file
        self._dc.set_file(self._file_path)
        self._dc.set_location("2022")
        if "class PklFile" not in self._dc.read():
            self._dc.add("class PklFile", {})
        self._dc.set_location(["2022", "class PklFile"])
    def set_value(self, key, value):
        self._dc.add(key, value, overwrite=True)
class TimePeriodCalculator:
    def __init__(self):
        self._layout = None
        self._out = widgets.Output()
        self._t0 = None
        self._t1 = None
    def set_start_stop_widget(self, start_stop):
        self._start_stop_btn = start_stop
        self._start_stop_btn.on_click(self._start_stop_clicked)
    def set_reset_btn(self, resetBtn):
        self._reset_btn = resetBtn
        self._reset_btn.on_click(self._reset_clicked)
    def _start_stop_clicked(self, val):
        self._out.clear_output()
        with self._out:
            if self._t0 is None:
                self._t0 = time.time()
                self._t1 = None
                self._start_stop_btn.description = "stop"
                print("timer started")
            elif self._t1 is None:
                self._t1 = time.time()
                self._start_stop_btn.description = "start"
                timeCount = self._t1 -self._t0
                print("timer set for", timeCount, "sec")
                self._t0 = None
                self._model.set_value("timer", timeCount)
    def _reset_clicked(self, val):
        self._out.clear_output()
        with self._out:
            print("timer set to 2 min")
            self._model.set_value("timer", 2*60)
    def display(self):
        if self._layout is not None:
            return self._layout
        self._layout = widgets.VBox([widgets.HBox([self._start_stop_btn, self._reset_btn]), self._out])
        return self._layout
    def set_model(self, model: IModel):
        self._model = model

class Main:
    def get_gui():
        tpc = TimePeriodCalculator()
        tpc.set_start_stop_widget(widgets.Button(description="start", layout= widgets.Layout(width="auto")))
        tpc.set_reset_btn(widgets.Button(description="reset", layout= widgets.Layout(width="auto")))
        tpc.set_model(PklFile(LibsDB.picklePath("temps")))
        tpc.display()