import datetime
from threading import Timer
from enum import Enum
class TimerDB:
    def __init__(self, time, func):
        # time in seconds
        self.time = time
        self.func = func
        self.t = Timer(time, self._threadInitialize)
        self.t.start()
        self._running = True
    def _threadInitialize(self):
        self.func()
        self.t.cancel()  #reset timer T
        if(self._running):
            self.t = Timer(self.time, self._threadInitialize)
            self.t.start()
    def cancel(self):
        self.t.cancel()
        self._running = False
    def changeTime(self, newTime):
        self.time = newTime
        self.t.cancel()
        self.t = Timer(self.time, self._threadInitialize)
        self.t.start()
class JobStatus:
    NotStarted = 1
    Running = 2
    Finished = 3
class Scheduler:
    instance = None
    debug = None
    jobs = {}
    def _checkAndRun():
        jobsToDelete = []
        for job in Scheduler.jobs:
            if(Scheduler.jobs[job].status == JobStatus.NotStarted):
                Scheduler.jobs[job].start()
            if(Scheduler.jobs[job].status == JobStatus.Finished):
                jobsToDelete.append(job)
        for j in jobsToDelete:
            del Scheduler.jobs[j]
    def start():
        if(Scheduler.debug is None):
            Scheduler.debug = WidgetsDB.outArea()
        if(Scheduler.instance is None):
            Scheduler.instance = TimeDB.setTimer().regularlyUpdateTime(2, Scheduler._checkAndRun)
        else:
            print("Already running")
    def stop():
        Scheduler.instance.cancel()
        del Scheduler.instance
        del Scheduler.debug
        Scheduler.instance = None
        Scheduler.debug = None
    def ops():
        class IJob:
            def __init__(self,  func):
                self.func = func
                self.handler = None
                self.status = JobStatus.NotStarted
            def stop(self):
                raise IOError("implement this")
            def start(self):
                raise IOError("implement this")
            def pause(self):
                raise IOError("implement this")
        class TimerJob(IJob):
            def __init__(self, func):
                super().__init__( func)
                self.time = None
            def stop(self):
                self.handler.cancel()
                self.handler = None
                self.status = JobStatus.Finished
            def start(self):
                if(self.time is None):
                    raise IOError("Set time first")
                self.handler = TimeDB.setTimer().regularlyUpdateTime(self.time, self.func)
                self.status = JobStatus.Running
            def setTime(self, sec):
                self.time = sec
        class TimeTem:
            def nowTimeInSec():
                h, m, s = TimeDB.nowTime()
                return h*60*60 + m*60 + s
        class DayJob(IJob):
            def __init__(self, func):
                super().__init__( func)
                self.time = None
            def stop(self):
                self._stopIt = True
                self.status = JobStatus.Finished
            def start(self):
                nowTime = TimeTem.nowTimeInSec()
                remTime = self.time - nowTime
                self._stopIt = False
                TimeDB.setTimer().oneTimeTimer(remTime, self._tem)
                self.status = JobStatus.Running
            def _tem(self):
                self.func()
                if(not self._stopIt):
                    TimeDB.setTimer().oneTimeTimer(24*60*60, self.func)
            def setTime(self, clockTimeInSec):
                self.time = clockTimeInSec
        class ConditionJob(IJob):
            def __init__(self, cond, func):
                super().__init__(func)
                self.cond = cond
            def stop(self):
                self._stopIt = True
                self.status = JobStatus.Finished
            def start(self):
                self._stopIt = False
                TimeDB.setTimer().oneTimeTimer(remTime, self._tem)
                self.status = JobStatus.Running
            def _tem(self):
                if(self.cond()):
                    self.func()
                if(not self._stopIt):
                    TimeDB.setTimer().oneTimeTimer(24*60*60, self.func)
        class BigJob(IJob):
            def start(self):
                TimeDB.setTimer().oneTimeTimer(1, self._tem)
                self.status = JobStatus.Running
            def _tem(self):
                self.func()
                self.status = JobStatus.Finished
            def stop(self):
                print("Cant stop this job because it runs only once and it has started")
        class Temp:
            def add():
                class Te:
                    def _run(t, funcName = "", ):
                        from CryptsDB import CryptsDB
                        if(funcName == ""):
                            funcName = CryptsDB.generateUniqueId()
                        Scheduler.jobs[funcName] = t
                    def run_everySec(sec, func, funcName= ""):
                        t = TimerJob(func)
                        t.setTime(sec)
                        Te._run(t, funcName)
                    def run_everyDay(clockTimeInSec, func, funcName= ""):
                        t = DayJob(func)
                        t.setTime(sec)
                        Te._run(t, funcName)
                    def runWithCondition(cond, func, funcName= ""):
                        Te._run(ConditionJob(cond, func), funcName)
                    def bigJob(func,funcName= ""):
                        Te._run(BigJob(func), funcName)
                return Te
            def archive():
                class Tem:
                    def _pickle():
                        from PickleCRUDDB import PickleCRUD
                        return PickleCRUD("temps", loc= ["rlibs","Scheduler"])
                    def add(idNr):
                        Temp.stop(idNr)
                        a = Tem._pickle()
                        a.add(['jobs archive', idNr], Scheduler.jobs[idNr])
                        del Scheduler.jobs[idNr]
                    def show(key, reg = False ):
                        from SearchSystem import MultilineStringSearch
                        a = MultilineStringSearch(Tem.showAll(), allRes=True)
                        ind = a.search(key, reg=reg)
                        vals = []
                        for i in ind:
                            vals.append(a.container[i])
                        return vals
                    def showAll():
                        a = Tem._pickle()
                        keys = a.read(["jobs archive"]).keys()
                        return list(keys)
                    def remove(idNr):
                        a = Tem._pickle()
                        a.delete(["jobs archive", idNr])
                return Tem
            def removeJob(idNr):
                Scheduler.jobs[idNr].stop()
                del Scheduler.jobs[idNr]
            def stop(idNr):
                t = Scheduler.jobs[idNr]
                t.stop()
            def ids():
                return list(Scheduler.jobs.keys())
        return Temp
class TimeDB:
    def weekday(date:tuple = None):
        """
        date = tuple(yr, month, day)
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        """
        import calendar
        weekdays = calendar.day_name
        if(date is None):
            return weekdays[datetime.datetime.now().weekday()]
        year, month, day = date
        d = calendar.weekday(year, month, day)
        return weekdays[d]
    def today():
        n = datetime.datetime.now()
        return (n.year, n.month, n.day), (n.hour, n.minute, n.second)
    def nowTime():
        date, time = TimeDB.today()
        return time
    def weekDates(n = 0):
        l = datetime.datetime.now().weekday() + 1
        return [TimeDB.nDaysBefore(i*-1) for i in range(7*n-l, 7*(n + 1)-l, 1)]
    def month():
        n = datetime.datetime.now()
        return n.month
    def getTimeStamp(date = None):
        if(date is None):
            date, time = TimeDB.today()
        if(type(date) == int):
            date = TimeDB.nDaysBefore(-1 * date)
        day = TimeDB.weekday(date)
        date = ".".join(['{:0>2d}'.format(i) for i in date[::-1]])
        timeStamp = f"{day}, {date}"
        return timeStamp
    def yesterday():
        return TimeDB.nDaysBefore(1)
    def nDaysBefore(n):
        from datetime import date, timedelta
        k = datetime.date.today() - datetime.timedelta(days=n)
        return k.year,k.month,k.day
    def fileNameTimeStamp(stamp=None):
        import re
        if(stamp is None):
            stamp = TimeDB.getTimeStamp()
        return re.sub("[,| |\.]+", "_", stamp)
    def setTimer():
        import threading
        class Temp:
            def oneTimeTimer(timeInSec, func, params = ()):
                t = threading.Timer(timeInSec,func, params)
                t.start()
            def regularlyUpdateTime(time, func):
                return TimerDB(time, func)
        return Temp
    def modifiedTime(filePath, asFloat = True):
        import os
        tem = os.path.getmtime(filePath)
        if(asFloat):
            return tem
        raise IOError("Not Implemented yet")
    def names():
        import calendar
        class Temp:
            def ofWeek():
                return list(calendar.day_name)
            def ofMonth():
                return list(calendar.month_name)[1:]
            def today():
                import datetime
                n = datetime.datetime.now().weekday()
                weekNames = Temp.ofWeek()
                return weekNames[n]
            def thisMonth():
                return Temp.ofMonth()[TimeDB.month()-1]
        return Temp
    def dateCheckCondition(date):
        class Temp:
            def between(fromDate, toDate):
                """date format: (yyyy, mm, dd) inclusive"""
                toNu = lambda y,m,d : y*365 + m*31 + d
                return toNu(*date) >= toNu(*fromDate) and toNu(*date) <= toNu(*toDate)
            def inLastNWeek(n=1):
                return Temp.inLastNDays(n*7)
            def inLastNMonth(n = 1):
                y1, m1, _ = TimeDB.nDaysBefore(n*30.4)
                y2, m2, _ = TimeDB.nDaysBefore(0)
                return Temp.inMonth((y1, m1), (y2, m2))
            def inLastNDays(n=1):
                return Temp.between(TimeDB.nDaysBefore(n), TimeDB.nDaysBefore(0) )
            def inMonth(bMonth, endMonth):
                # bMonth/endMonth = (yyyy, mm)
                fromDate = (bMonth[0], bMonth[1], 1)
                toDate = (endMonth[0], endMonth[1], 31)
                return Temp.between(fromDate, toDate)
        return Temp
    def timeIt():
        class Temp:
            def start(self):
                self.startTime = time.time()
            def end(self):
                return time.time() - self.startTime
        return Temp()
class EventCalender:
    def _pickle():
        from PickleCRUDDB import PickleCRUD
        return PickleCRUD("oldInfos", loc= ["LifeLogs", "events"])
    def setEvent(date: str, time:str, eventDescription:str):
        """ date - dd.mm.yyyy 16.06.2021, time - 1800, 18:00"""
        pi = EventCalender._pickle()
        try:
            pi.read([date, time])
            print("There is already an event in this time.")
        except:
            pi.add([date, time], eventDescription, True)
    def monthsEvent(allEvents = False):
        (y,m,d), _ = TimeDB.today()
        dates = [(y,m, i) for i in range(32)]
        if(not allEvents):
            dates = filter(lambda x: x[2]>=d, dates)
        return EventCalender._founds(dates)
    def _founds(dates):
        from WordDB import WordDB
        pi = EventCalender._pickle()
        founds = {}
        for y,m,d in dates:
            strval = f"{WordDB.formatting().integer(d, 2, '0')}.{WordDB.formatting().integer(m, 2, '0')}.{y}"
            try:
                a = pi.read([strval])
                founds[strval] = a
            except:
                pass
        return founds
    def weekEvents(nextWeek = 0, allEvents = False):
        weekDates = TimeDB.weekDates(nextWeek)
        (y,m,d), _ = TimeDB.today()
        if(not allEvents):
            weekDates = filter(lambda x: x[2]>=d, weekDates)
        return EventCalender._founds(weekDates)
    def todayEvents():
        (y,m,d), _ = TimeDB.today()
        return EventCalender._founds([(y,m,d)])
    def showEvent(timeInterval = None):
        # timeInterval: 10.08.2021-12.08.2021
        comparableDate = lambda date: "".join(date.split(".")[::-1])
        if(timeInterval is None):
            be = comparableDate(TimeDB.getTimeStamp().split(", ")[-1])
            end = "a"
        else:
            be, end = [comparableDate(val) for val in timeInterval.split("-")]
        sortedDics = EventCalender.showAllEvents()
        newDic = {}
        for key in sortedDics:
            k = comparableDate(key)
            if(k >= be and k <= end):
                newDic[key] = sortedDics[key]
        return newDic
    def showAllEvents():
        dic = EventCalender._pickle().getContent()
        newDic = {}
        keys = sorted(dic, key = lambda x: "".join(x.split(".")[::-1]))
        for key in keys:
            newDic[key] = dic[key]
        return newDic
    def upcoming(n = 5):
        dates = [TimeDB.nDaysBefore(-1*i) for i in range(0, n+1)]
        return EventCalender._founds(dates)