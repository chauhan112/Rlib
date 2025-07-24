from useful.RegexDB import RegexDB, NameDicExp
from useful.TimeDB import TimeDB
from useful.htmlDB import htmlDB
from useful.jupyterDB import jupyterDB
from useful.ListDB import ListDB
import ipywidgets as widgets
from modules.Explorer.personalizedWidgets import CustomOutput
import datetime
import json
from useful.FileDatabase import File


class StringEnum:
    IGNORE = "ignore"
    STARTED = "started"
    LEFT = "left"
    MONTH = "month"
    HOUR ="hour"
    MINUTE = "minute"
    DAY = "day"
    YEAR ="year"
    NOON = "noon"
class Attendence:
    def _compare_date_format(self, disCordDate):
        day = disCordDate.replace("—", "").strip().split()[0].split("/")
        dd = day[-1]
        if dd.lower() == "yesterday":
            return TimeDB.yesterday()
        elif dd.lower() == "today":
            return TimeDB.today()[0]
        return (int(day[-1]), int(day[0]), int(day[1]))
    def _parser_attendence_line(self, line):
        res = RegexDB.group_name_search(NameDicExp("", "typ", "[a-zA-Z]+",
            NameDicExp(r" *(\-)* *", "time", r"[0-9]+( |:)*[0-9]*", ".*")), line)
        assert len(res) != 0
        return res
    def _words_to_meaning(self, word):
        return word.lower().replace("back", StringEnum.STARTED).replace("break", StringEnum.LEFT)
    def _date_comparer(self, date):
        return TimeDB.dateCheckCondition(date).between(self._start, self._end)
    def set_start_time(self, date):
        "format (yyyy, mm, dd)"
        self._start = date
    def set_end_time(self, date):
        "format (yyyy, mm, dd)"
        self._end = date
    def set_ol_content(self, content= None):
        if content is None:
            content = jupyterDB.clip().text()
        self._content = content
        soup = htmlDB.getParsedData(content)
        self._allMsgs = htmlDB.getTags("li", soup)
        res = []
        for one in self._allMsgs:
            if one.h3:
                res.append([one.h3.time.text, one.div.div.div.text])
            else:
                res.append([res[-1][0], one.div.div.div.text])
        self._msg_readable = res
    def _time_parser(self, x):
        try:
            res = list(map(lambda x: int(x), x.strip().split(":")))
        except:
            print(x)
        if len(res) == 1:
            res.append(0)
        return res
    def _period_cal(self, x, y):
        a,b = x
        c,d = y
        if c < a:
            c += 12
        t1 = a *60 + b
        t2 = c * 60 + d
        re = t2-t1
        return re//60, re%60
    def calculate_hours_from_message_time(self):
        # user message time log along with time of start
        abc = list(map(lambda x: [self._compare_date_format(x[0]), x[1]], self._msg_readable))
        filterd = list(filter(lambda x: self._date_comparer(x[0]), abc))
        filterd = list(filter(lambda x: RegexDB.isThereRegexMatch("\d+", x[-1]), filterd))
        times = list(map(lambda x: [x[0], self._parser_attendence_line(x[-1])], filterd))
        timesSt = list(map(lambda x: [x[0],{k: self._words_to_meaning(x[1][k]) for k in x[1]}], times))
        timesSt = list(map(lambda x: [x[0],*x[1].values()], timesSt))
        timesSt = list(map(lambda x: [x[0],x[1], self._time_parser(x[2])], timesSt))
        from useful.ListDB import ListDB
        timep = ListDB.reshape(timesSt, (len(timesSt)//2, 2))
        hrs = list(map(lambda x: self._period_cal(x[0][-1], x[-1][-1]), timep))
        toh, tom = 0, 0
        for x, y in hrs:
            toh += x
            tom += y
        return toh + tom//60, tom%60
    def _discord_time_parser(self, timeStr):
        yst = TimeDB.yesterday()
        timeStr = timeStr.replace("Yesterday at", f"{yst[1]}/{yst[2]}/{yst[0]}")
        yst = TimeDB.today()[0]
        timeStr = timeStr.replace("Today at", f"{yst[1]}/{yst[2]}/{yst[0]}")
        tim = timeStr.replace("—","").strip().strip()
        y = 365 * 24 * 60
        m = 30* 24* 60
        d = 24 * 60
        hr = 60
        filterMapper = NameDicExp("", StringEnum.MONTH, "[0-9]+", NameDicExp("/", StringEnum.DAY, "[0-9]+",
                NameDicExp("/", StringEnum.YEAR, "[0-9]{4}", NameDicExp(" ", StringEnum.HOUR, "[0-9]+", NameDicExp(":",
                StringEnum.MINUTE, "[0-9]+", NameDicExp(" ",StringEnum.NOON, "[A-Z]+", ""))))))
        timeP = RegexDB.group_name_search(filterMapper, tim)
        if timeP[StringEnum.NOON] == "PM":
            if timeP[StringEnum.HOUR] != "12":
                timeP[StringEnum.HOUR]= int(timeP[StringEnum.HOUR]) + 12
        return int(timeP[StringEnum.YEAR])* y + int(timeP[StringEnum.MONTH])* m +int(timeP[StringEnum.DAY])* d + \
                int(timeP[StringEnum.HOUR])* hr + int(timeP[StringEnum.MINUTE])
    def set_string_mapper(self, mmper):
        "for mapping the message to started, left or ignored"
        self._msg_mapper = mmper
    def get_all_messages(self):
        dic = {}
        rf = list(filter(lambda x: self._date_comparer(self._compare_date_format(x[0])), self._msg_readable))
        for t, m in rf:
            dic[m.strip().lower()] = t
        return dic
    def calculate_hours_from_discord_message_time(self):
        # user message time log along without time of log
        rf = list(filter(lambda x: self._date_comparer(self._compare_date_format(x[0])), self._msg_readable))
        ff = list(map(lambda x: [x[0], x[-1], self._msg_mapper[x[-1].strip().lower()]], rf))
        self._fgi = list(filter(lambda x: x[-1] != StringEnum.IGNORE, ff))
        # verifies that there is started and left not started  or left consequetively
        if self._fgi[0][-1] == "left":
            self._fgi.pop(0)
        prev = None
        for a,b,c in self._fgi:
            if c == prev:
                print(a, b, c)
                assert False
            prev = c
        gr = ListDB.reshape(self._fgi, (len(self._fgi)//2, 2))
        totalMinues = sum(map(lambda x: (self._discord_time_parser(x[1][0]) - self._discord_time_parser(x[0][0])), gr))
        return (totalMinues//60, totalMinues%60)
class TimeCalculatorView:
    def __init__(self):
        self.deflay = {'width': "auto"}
        self.contentwid = widgets.Textarea(placeholder = "html content or file path", layout = {'width': "60%", 'height': "70px"})
        self.startWid = widgets.DatePicker(layout = self.deflay, description="start time")
        self.endWid = widgets.DatePicker(layout = self.deflay, description="end time")
        self.typWid = widgets.Dropdown(options = ["message time", "messaged time"], description="type of extraction")
        self.generate_exceptions = widgets.Button(description="generate")
        self.out = CustomOutput()
        self.contentType = widgets.Dropdown(layout = self.deflay, options = ["file", "text", "clipboard"])
        self.calcBtn = widgets.Button(description="calculate")
        self.out2 = CustomOutput()
        self.layout = widgets.VBox([
            widgets.HBox([self.contentwid, self.contentType]),
            self.typWid,
            self.generate_exceptions,
            widgets.HBox([self.startWid, self.endWid]),
            self.calcBtn,
            self.out.get_layout(),
            self.out2.get_layout()
        ])
class TimeCalculatorController:
    def __init__(self):
        self._memoization = {}
    def set_attendence_model(self, model: Attendence):
        self._model = model
    def set_view(self, view: TimeCalculatorView):
        self._view = view
    def set_up(self):
        now = datetime.datetime.now()
        yr = now.year
        pmt = now.month - 1
        if (now.month - 1) == 0:
            yr = yr -1 
            pmt = 12
        self._view.startWid.value = datetime.date(yr, pmt, now.day)
        self._view.endWid.value = datetime.date(now.year, now.month, now.day)
        self._view.generate_exceptions.on_click(self._on_generate_func)
        self._view.calcBtn.on_click(self._calc)
    def _calc(self, nt):
        self._set_values()
        self._model.set_string_mapper(self._extract_dict())
        hr, mi = self._model.calculate_hours_from_discord_message_time()
        self._view.out2.clear()
        with self._view.out2._out:
            print(f"hours: {hr} \nminutes: {mi}")
    def _extract_dict(self):
        res = {}
        for k in self._memoization:
            res[k] = self._memoization[k].value
        return res
    def _set_values(self):
        st = self._view.startWid.value
        dn = self._view.endWid.value
        self._model.set_start_time((st.year, st.month, st.day))
        self._model.set_end_time((dn.year, dn.month, dn.day))
        if self._view.contentType.value == "file":
            content = File.getFileContent(self._view.contentwid.value.strip())
        elif self._view.contentType.value == "text":
            content = self._view.contentwid.value
        elif self._view.contentType.value == "clipboard":
            from ancient.ClipboardDB import ClipboardDB
            content = ClipboardDB.getText()
        self._model.set_ol_content(content)
    def _on_generate_func(self, btn):
        self._set_values()
        msgs = self._model.get_all_messages()
        wid = self._create_option(msgs)
        self._view.out.display(wid, ipy=True, clear=True)
    def _create_option(self, msgs):
        ly = []
        for ms in msgs:
            if ms in self._memoization:
                ly.append(self._memoization[ms])
            else:
                lay = widgets.Dropdown(options = [StringEnum.LEFT, StringEnum.IGNORE, StringEnum.STARTED],
                                       description=ms)
                if 'start' in ms:
                    lay.value = StringEnum.STARTED
                elif 'break' in ms:
                    lay.value = StringEnum.LEFT
                elif "done" in ms:
                    lay.value = StringEnum.LEFT
                elif "back" in ms:
                    lay.value = StringEnum.STARTED
                self._memoization[ms] = lay
                ly.append(lay)
        return widgets.HBox([widgets.VBox(ly), widgets.Textarea(value = json.dumps(self._extract_dict(), indent=4), 
                                                                disabled=True)])
class Main:
    def calculate_view():
        tcv = TimeCalculatorView()
        tcc = TimeCalculatorController()
        tcc.set_view(tcv)
        tcc.set_attendence_model(Attendence())
        tcc.set_up()
        return tcc