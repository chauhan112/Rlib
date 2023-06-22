import ipywidgets as widgets
import os
class TimerSetView:
    def __init__(self):
        self.layout = None
        self.set_time_selector(widgets.IntSlider(min = 1, max= 60, description = "minutes"))
    def _make_layout(self):
        self.titleTextWid = widgets.Text(description= "Give title", value = "Focus time")
        self.setBtn = widgets.Button(layout={"width":"auto"}, description= "set")
        self.out = widgets.Label(value="")
        self.layout = widgets.HBox([self.titleTextWid, self.timeInMinu, self.setBtn, self.out])
    def display(self):
        if self.layout is None:
            self._make_layout()
        display(self.layout)
    def set_time_selector(self, wid):
        self.timeInMinu = wid
class TimerController:
    def set_view(self, view: TimerSetView):
        self._ui = view
    def setup(self):
        self._ui._make_layout()
        self._ui.setBtn.on_click(self._on_set_click)
    def _on_set_click(self, wid):
        from LibsDB import LibsDB
        from nice_design.notification import LinuxNotifier
        title = self._ui.titleTextWid.value
        if title.strip() == "":
            title = "Focus time"
        timeInSec = self._ui.timeInMinu.value* 60
        ln = LinuxNotifier(title=title, msg="finished", time_period=timeInSec)
        music = os.sep.join([LibsDB.cloudPath(), "Global", "music","ton",'mixkit-doorbell-single-press-333.wav'])
        ln.set_music(music)
        ln.notify()
        self._ui.out.value="done"
        from TimeDB import TimeDB
        TimeDB.setTimer().oneTimeTimer(5, self._cleartime)
    def _cleartime(self):
        self._ui.out.value=""
class MainLC:
    tc = None
    def timerSetterWidget():
        if MainLC.tc is None:
            tc = TimerController()
            tc.set_view(TimerSetView())
            tc._ui.set_time_selector(widgets.ToggleButtons(description="minutes",options=map(lambda x: (str(x), x), range(1,11)), button_style='info',style={"button_width": "auto"},value = 4))
            tc.setup()
            MainLC.tc = tc
        MainLC.tc._ui.display()
class Confirmer:
    def __init__(self):
        self._layout = None
        self._params = None
    def set_callback_function(self, func):
        self._func = func
    def set_params(self, params):
        self._params = params
    def display(self):
        from IPython.display import display
        if self._layout is not None:
            self._layout.layout.display = None
            display(self._layout)
            return
        self._layout = widgets.Button(description="ok")
        self._layout.layout.width = "auto"
        self._layout.on_click(self._clicked)
        display(self._layout)
    def _clicked(self, btnInfo):
        self._layout.layout.display ="none"
        if self._params is not None:
            self._func(self._params)
        else:
            self._func()
class Tools:
    def migrateRlibItValues(rlib):
        import datetime
        from SerializationDB import SerializationDB
        from TimeDB import TimeDB
        from Path import Path
        from TimelineDB import TimelineDB
        m = TimeDB.month() - 2
        y = None
        if m < 0:
            y = datetime.datetime.now().year - 1
            m = -1 % 12 # last month of last year (december)
        base = TimelineDB.getMonthPath(m, y)
        file = Path.filesWithExtension("pkl", os.sep.join([base, "_rajaDB"]))[0]
        vals = SerializationDB.readPickle(file)['instructions']
        for k in vals:
            val = vals[k]
            rlib.it.add(k, val)
