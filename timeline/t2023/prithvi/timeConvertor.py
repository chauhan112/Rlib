import ipywidgets as widgets
from datetime import datetime
import pytz

class NameSpace:
    pass
class TimeConvertorView:
    def __init__(self):
        options = [('Germany', 'Europe/Berlin'), ('India', 'Asia/Kolkata'), ('Nepal', 'Asia/Kathmandu')]
        self.local = NameSpace()
        self.target = NameSpace()
        self.local.dp = widgets.Dropdown(options= options,layout = {"width": "auto"})
        self.local.tp = widgets.TimePicker()
        self.target.dp = widgets.Dropdown(options=options,layout = {"width": "auto"})
        self.target.tp = widgets.TimePicker(  )
        line1 = widgets.HBox([self.local.dp, self.local.tp])
        line2 = widgets.HBox([self.target.dp, self.target.tp])
        self.layout = widgets.VBox([line1, line2])
class TimeConvertorController:
    def set_up(self):
        self._view.local.dp.observe(self.conversion_tgt_to_local, names='value')
        self._view.target.dp.observe(self.conversion_local_to_tgt, names='value')
        self._view.local.tp.observe(self.conversion_local_to_tgt, names='value')
        self._view.target.tp.observe(self.conversion_tgt_to_local, names='value')
    def set_view(self, view):
        self._view = view
    def _conversion(self, local, target):
        local_time = local.tp.value
        target_time = target.tp.value
        current_date = datetime.now().date()
        if local_time:
            local_dt = datetime.combine(current_date, local_time)
            local_tz_name = local.dp.value
            target_tz_name = target.dp.value
            local_tz = pytz.timezone(local_tz_name)
            tgt_tz = pytz.timezone(target_tz_name)
            local_country_dt = local_tz.localize(local_dt)
            tgt_country_dt = local_country_dt.astimezone(tgt_tz)
            target.tp.value = tgt_country_dt.time()
    
    def conversion_local_to_tgt(self, time):
        self._conversion(self._view.local, self._view.target)

    def conversion_tgt_to_local(self, time):
        self._conversion(self._view.target,self._view.local)

class Main:
    def timeconvertor():
        view = TimeConvertorView()
        controller = TimeConvertorController()
        controller.set_view(view)
        controller.set_up()
        return controller
