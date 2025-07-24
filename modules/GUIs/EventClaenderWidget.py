import ipywidgets as widgets
import ipydatetime
import datetime
from useful.TimeDB import EventCalender
class _EventCalenderOpsWidget:
    def __init__(self):
        print("Event calender")
        from IPython.display import display
        self._defineWidgets()
        self.layout = self._createMainLayout()
        display(self.layout)

    def _defineWidgets(self):
        self._leftSide = {'width': '100px'}
        self._opsSelection = widgets.Dropdown(options=[],layout={'width':"100px"})
        self._fromW = ipydatetime.NaiveDatetimePicker()
        self._toW = ipydatetime.NaiveDatetimePicker()
        self._showOpsW = widgets.Dropdown(options=[]
                                         ,layout={'width':"100px"})
        self._okBtn = widgets.Button(description="ok",layout={"width":"100px"})
        self._eventLabel = widgets.Text(placeholder="event name")
        self._doneW = widgets.Checkbox(indent=False, layout={'width':"auto"})
        
        self._fromDateLabel = widgets.Label(value="from", layout=self._leftSide)
        self._toDateLabel = widgets.Label(value="to", layout=self._leftSide)
        
    def _createMainLayout(self):
        row1 = widgets.HBox([widgets.Label(value="calendar ops", layout=self._leftSide), self._opsSelection, 
                             self._showOpsW])
        row2 = widgets.HBox([self._fromDateLabel, self._fromW])
        self.row3 = widgets.HBox([self._toDateLabel, self._toW])
        self.row4 = widgets.HBox([widgets.Label(value="event name", layout=self._leftSide),self._eventLabel ])
        self.row5 = widgets.HBox([widgets.Label(value="event completed", layout=self._leftSide),self._doneW ])
        row6 = widgets.Box([self._okBtn], layout=widgets.Layout(display='flex',flex_flow='row-reverse',))
        return widgets.VBox([row1, row2, self.row3, self.row4, self.row5, row6], layout=widgets.Layout(display='flex', 
                                flex_flow='column', border='solid 2px BurlyWood', align_items='stretch', 
                                width='50%', min_width ="50%"))
class EventCalenderMainController:
    def __init__(self):
        self.view = _EventCalenderOpsWidget()
        self.model = EventCalenderModel()
        self._setCallbacks()
        self.view._opsSelection.options = [('add event', AddController(self)), ("update", UpdateController(self)), 
                                           ("show", ShowController(self))]
        self.view._fromW.value = self.model.nowTimeTillMin()
        self.view._toW.value = self.model.nowTimeTillMin()
        
    def _setCallbacks(self):
        self.view._opsSelection.observe(self.opsSelected, names="value")
        self.view._okBtn.on_click(self.okClicked)
    
    def opsSelected(self, change):
        ops = change['new']
        self.view._showOpsW.layout.display = 'none'
        self.view.row3.layout.display = 'none'
        self.view.row4.layout.display = None
        self.view._okBtn.description = "ok"
        self.view._doneW.disabled = True
        self.view.row5.layout.display ='none'
        ops.onSelect()
    
    def okClicked(self, btn):
        self.view._opsSelection.value.okButton()
class EventCalenderModel:
    def __init__(self):
        self.calender = EventCalender
    
    def nowTimeTillMin(self):
        from useful.TimeDB import TimeDB
        (y,m,d), (h,minu, _) =TimeDB.today()
        return datetime.datetime(y, m,d, h,minu)
    
    def dateStr(self, date):
        day = "{:0>2d}".format(date.day)
        month = "{:0>2d}".format(date.month)
        return f"{day}.{month}.{date.year}"
    def timeStr(self, date):
        hour = "{:0>2d}".format(date.hour)
        minute = "{:0>2d}".format(date.minute)
        return f"{hour}:{minute}"
class IDropdownSelection:
    def __init__(self, parent):
        self.parent = parent
    def onSelect(self):
        raise IOError("implement this method")
class IOpsController(IDropdownSelection):
    def okButton(self):
        raise IOError("implement this method")
class IShowOps(IDropdownSelection):
    def getEvents(self):
        end = self.parent.parent.view._toW.value
        begin = self.parent.parent.view._fromW.value
        interval = f"{self.parent.parent.model.dateStr(begin)}-{self.parent.parent.model.dateStr(end)}"
        return self.parent.parent.model.calender.showEvent(interval)
class ShowController(IOpsController):
    def __init__(self, parent):
        super().__init__(parent)
        
        class ShowTodayOps(IShowOps):
            def onSelect(self):
                self.parent.parent.view._fromDateLabel.value = "today"
                self.parent.parent.view.row3.layout.display = 'none'
            def getEvents(self):
                return self.parent.parent.model.calender.todayEvents()
            
        class ShowRangeOps(IShowOps):
            def onSelect(self):
                val = self.parent.parent.model.nowTimeTillMin() + datetime.timedelta(days = 1)
                self.parent.parent.view._toW.value = val

        class ShowThisWeekOps(IShowOps):
            def onSelect(self):
                val = self.parent.parent.model.nowTimeTillMin() + datetime.timedelta(days = 7)
                self.parent.parent.view._toW.value = val
    
        class ShowThisMonthOps(IShowOps):
            def onSelect(self):
                import calendar
                val = self.parent.parent.model.nowTimeTillMin()
                b, end = calendar.monthrange(val.year, val.month)
                self.parent.parent.view._toW.value = datetime.datetime(val.year, val.month, end, val.hour, val.minute)
            
        class ShowThisYearOps(IShowOps):
            def onSelect(self):
                val = self.parent.parent.model.nowTimeTillMin()
                self.parent.parent.view._toW.value = datetime.datetime(val.year, 12, 31, val.hour, val.minute)
        
        
        self.parent.view._showOpsW.observe(self.opsSelected, names="value")
        self.parent.view._showOpsW.options = [('today', ShowTodayOps(self)),
                                              ('range', ShowRangeOps(self)), 
                                              ('this week', ShowThisWeekOps(self)), 
                                              ('this month', ShowThisMonthOps(self)), 
                                              ('this year', ShowThisYearOps(self))]
    def onSelect(self): #interface method
        self.parent.view._showOpsW.layout.display = None
        self.parent.view._okBtn.description ="show"
        self.parent.view._fromDateLabel.value = "from"
        self.parent.view._toDateLabel.value = "till"
        self._selectPreProcess(self.parent.view._showOpsW.value)
        
    def opsSelected(self, change):
        ops = change['new']
        self._selectPreProcess(ops)
    
    def _selectPreProcess(self, cont):
        self.parent.view.row3.layout.display = None
        self.parent.view.row4.layout.display = 'none'
        cont.onSelect()
    
    def okButton(self):
        events = self.parent.view._showOpsW.value.getEvents()
        print(events)
class AddController(IOpsController):
    def onSelect(self):
        self.parent.view._fromDateLabel.value = "select a date" 
    
    def okButton(self):
        eventName = self.parent.view._eventLabel.value.strip()
        if(len(eventName) == 0):
            print("add event title")
            return
        date = self.parent.view._fromW.value
        dateStr = self.parent.model.dateStr(date)
        timeStr = self.parent.model.timeStr(date)
        EventCalender.setEvent(dateStr, timeStr, eventName)
        print(f"event set on {dateStr} at {timeStr}")
class UpdateController(IOpsController):
    def onSelect(self):
        self.parent.view.row5.layout.display = None
        self.parent.view._doneW.disabled = False
        self.parent.view._eventLabel.value = ""