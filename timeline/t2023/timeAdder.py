import ipywidgets as widgets
class HourAdder:
    def __init__(self,):
        self._hour = 0
        self._min = 0
        self._history = []
    def add(self, timeStr: str):
        self._history.append(timeStr)
        hor, mi = map(int, timeStr.split(":"))
        self._min += mi
        if self._min >= 60:
            self._hour += self._min // 60
            self._min = self._min % 60
        self._hour += hor
    def __repr__(self):
        return f"{self._hour}:{self._min}"
class TimeAdderLC:
    def __init__(self):
        self._layout =None
    def set_time_adder(self, adder):
        self._adder = adder
    def get_layout (self):
        if self._layout is None:
            self._timeWi = widgets.Text(placeholder="hh:mm")
            self._btnWi = widgets.Button(description="add")
            self._out = widgets.Output()
            self._layout = widgets.HBox([self._timeWi,self._btnWi, self._out])
        return self._layout
    def set_up(self):
        self._btnWi.on_click(self._add)
    def _add(self, btn):
        if self._timeWi.value.strip() != "":
            self._adder.add(self._timeWi.value.strip())
        self._out.clear_output()
        with self._out:
            print(self._adder)