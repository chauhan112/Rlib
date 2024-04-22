import ipywidgets as widgets
import os
import calendar
import datetime

class TimelineDB:
    def getMonthPath(monthNr, year = None, months = None):
        from TimeDB import TimeDB
        if months is None:
            months = ['1. jan',
                 '2. feb',
                 '3. mar',
                 '4. apr',
                 '5. may',
                 '6. jun',
                 '7. jul',
                 '8. aug',
                 '9. sep',
                 '10. oct',
                 '11. nov',
                 '12. dec']
        m = ''
        if(type(monthNr) == int):
            m = months[monthNr]
        elif(type(monthNr)==str):
            fil = list(filter(lambda x: monthNr.lower() in x, months))
            if(len(fil)== 1):
                m = fil[0]
            else:
                raise IOError("not unique letters combination")
        else:
            raise IOError("Invalid type. Only str or int is allowed 0 for jan")
        if year is None:
            year = TimeDB.today()[0][0]
        return os.sep.join([TimelineDB.getYearPath(year), m])

    def getYearPath(year):
        from LibsDB import LibsDB
        return os.sep.join([LibsDB.cloudPath().replace("\\", os.sep),'timeline', str(year)])
    
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
        display(self.get_layout())
    def get_layout(self):
        if self._layout is not None:
            self._layout.layout.display = None
            return self._layout
        self._layout = widgets.Button(description="ok")
        self._layout.layout.width = "auto"
        self._layout.on_click(self._clicked)
        return self._layout
    def _clicked(self, btnInfo):
        self._layout.layout.display ="none"
        if self._params is not None:
            self._func(self._params)
        else:
            self._func()
class Tools:
    def migrateRlibItValues(rlib):
        from SerializationDB import SerializationDB
        from TimeDB import TimeDB
        from Path import Path
        m = TimeDB.month() - 2
        months = list(calendar.month_name)[1:]
        short_months_with_indices = [ "0" + str(i+1) + "_" + val[:3] if len(str(i+1)) == 1 else str(i+1) + "_" + val[:3] for i, val in enumerate(months)]
        y = None
        if m < 0:
            y = datetime.datetime.now().year - 1
            m = -1 % 12 # last month of last year (december)
        base = TimelineDB.getMonthPath(m, y, short_months_with_indices)
        file = Path.filesWithExtension("pkl", os.sep.join([base, "_rajaDB"]))[0]
        vals = SerializationDB.readPickle(file)['instructions']
        for k in vals:
            val = vals[k]
            rlib.it.add(k, val)
    def make_new_dirs_and_ipynbs():
        months = list(calendar.month_name)[1:]
        short_months_with_indices = [ "0" + str(i+1) + "_" + val[:3] if len(str(i+1)) == 1 else str(i+1) + "_" + val[:3] for i, val in enumerate(months)]
        year_loc = os.path.dirname(os.path.abspath(".")) # '/home/chauh-ra/MEGA/cloud/timeline/2024'

        month_fullpaths = [year_loc + os.sep + mth for mth in short_months_with_indices]
        for dirpath in month_fullpaths:
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            spaceIpynb = dirpath + os.sep + "space"
            jupyterDB.createJupyterNotebook(spaceIpynb)
       