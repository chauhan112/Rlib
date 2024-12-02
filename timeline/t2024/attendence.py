import os
from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from basic import Main as ObjMaker
from ClipboardDB import ClipboardDB
from timeline.t2023.attendence import StringEnum
import json
from timeline.t2024.Array import Array
from FileDatabase import File
from htmlDB import htmlDB
from TimeDB import TimeDB
from OpsDB import OpsDB
from ListDB import ListDB
from datetime import datetime, timedelta
import ipywidgets as widgets

def TimeTools():
    def timeToHumanReadable(timeInSec, subSets = None):
        units = {"yr": 365*24*60*60, "day": 24*60*60, "hr": 60*60, "min": 60, "sec": 1}
        if subSets is None:
            subSets = units.keys()
        res = ""
        tl = timeInSec
        for u in subSets:
            si = units[u]
            r = tl // si
            if r != 0:
                res += f"{r} {u} "
            tl = tl % si
        return res.strip()
    s = ObjMaker.variablesAndFunction(locals())
    return s
def DiscordMessageParser():
    start_date = None
    end_date = None
    content = ""
    pipeline = [htmlDB.getParsedData, lambda x: x.find_all("li"),  
                lambda y: Array(y).filter(lambda x: len(x.attrs) == 3 and "aria-setsize" in x.attrs).array]
    def set_file(filePath):
        s.process.filePath = filePath
        s.process.content = File.getFileContent(filePath)
    def set_date_range(start_date=None, end_date=None):
        """date format (yyyy, mm, dd, hh, MM) """
        if start_date is not None:
            y, m, d, h,M  = start_date
            s.handlers.set_start_date(datetime(year=y, month=m, day=d, hour=h, minute=M))
        if end_date is not None:
            y, m, d, h,M  = end_date
            s.handlers.set_end_date(datetime(year=y, month=m, day=d, hour=h, minute=M))
    def set_start_date(datet: datetime):
        s.process.start_date = datet
        s.process.pipeline.append(lambda y: Array(y).filter(lambda x: x[0] >= s.process.start_date).array)
    def set_end_date(datet: datetime):
        s.process.end_date = datet
        s.process.pipeline.append(lambda y: Array(y).filter(lambda x: x[0] <= s.process.end_date).array)
    def get_filtered_results():
        res = s.process.content
        for f in s.process.pipeline:
            res = f(res)
        return res
    def readableMessage(arr):
        res = []
        for one in arr:
            if one.h3:
                res.append([one.h3.time.text, one.div.div.div.text])
            else:
                res.append([res[-1][0], one.div.div.div.text])
        return res
    def sanitizeDateTime(res):
        newRes = []
        for timeStamp, msg in res:
            newRes.append([s.handlers.date_time_sanitizer(timeStamp), msg])
        return newRes
    def date_time_sanitizer(timeStr):
        yst = TimeDB.yesterday()
        timeStr = timeStr.replace("Yesterday at", f"{yst[1]}/{yst[2]}/{yst[0]}")
        yst = TimeDB.today()[0]
        timeStr = timeStr.replace("Today at", f"{yst[1]}/{yst[2]}/{yst[0]}")
        tim = timeStr.replace("—","").strip().strip()
        return datetime.strptime(tim, "%m/%d/%Y %I:%M %p") 
    pipeline.append(readableMessage)
    pipeline.append(sanitizeDateTime)
    s = ObjMaker.variablesAndFunction(locals())
    return s
def AttendenceFirstRow():
    filePathWid = Utils.get_comp({"placeholder":"file path"}, IpywidgetsComponentsEnum.Text, className="w-auto")
    contentWid = Utils.get_comp({"placeholder":"content to parse"}, IpywidgetsComponentsEnum.Textarea, className="w-auto", bind = False)
    saveAlso = Utils.get_comp({"description":"save file","indent": False}, IpywidgetsComponentsEnum.Checkbox, className="w-auto")
    optionsWid = Utils.get_comp({"options": ["file",'content',"clipboard", "select files"]},IpywidgetsComponentsEnum.Dropdown, className = "w-auto")
    selectFilesWid = Utils.get_comp({},IpywidgetsComponentsEnum.Dropdown, className = "w-auto")
    container = Utils.container([optionsWid,saveAlso, contentWid,filePathWid, selectFilesWid])
    filePathWid.outputs.layout.continuous_update = False
    def filePathChanged(w):
        val = s.views.filePathWid.outputs.layout.value.strip()
        if os.path.exists(val) and os.path.isdir(val):
            from Path import Path
            files = Path.getFiles(val)
            s.views.selectFilesWid.outputs.layout.options = files
            s.views.selectFilesWid.show()
        else:
            s.views.selectFilesWid.hide()
    def nothing(w):
        pass
    def optionSelected(w):
        val = s.views.optionsWid.outputs.layout.value
        s.views.selectFilesWid.hide()
        s.views.filePathWid.handlers.handle = nothing
        if val == "file":
            s.views.filePathWid.show()
            s.views.contentWid.hide()
            s.views.saveAlso.hide()
        elif val == "content":
            s.views.filePathWid.hide()
            s.views.saveAlso.show()
            s.handlers.saveOrNot(1)
            s.views.contentWid.show()
        elif val == "clipboard":
            s.views.filePathWid.show()
            s.views.contentWid.hide()
            s.views.saveAlso.show()
            s.handlers.saveOrNot(1)
        elif val == "select files":
            s.views.filePathWid.show()
            s.views.contentWid.hide()
            s.views.saveAlso.hide()
            s.views.selectFilesWid.show()
            s.views.filePathWid.handlers.handle = s.handlers.filePathChanged
    def saveOrNot(w):
        val = s.views.saveAlso.outputs.layout.value
        if val:
            s.views.filePathWid.show()
        else:
            s.views.filePathWid.hide()
    def get_content():
        val = s.views.optionsWid.outputs.layout.value
        if val == "file":
            filePath = s.views.filePathWid.outputs.layout.value
        elif val == "content":
            return s.views.contentWid.outputs.layout.value
        elif val == "clipboard":
            return ClipboardDB.getText()
        elif val == "select files":
            filePath = s.views.selectFilesWid.outputs.layout.value
        if type(filePath) == str:
            if os.path.exists(filePath) and os.path.isfile(filePath):
                return File.getFileContent(filePath)
        return ""
    optionsWid.handlers.handle = optionSelected
    saveAlso.handlers.handle = saveOrNot
    s = ObjMaker.uisOrganize(locals())
    optionSelected(1)
    return s
def AttendenceUI():
    attendenceRow = AttendenceFirstRow()
    attendenceRow.views.optionsWid.outputs.layout.description = "attendence"
    logsRow = AttendenceFirstRow()
    logsRow.views.optionsWid.outputs.layout.description = "logs section"
    typeOfExtraction = Utils.get_comp({"options": ["discord time","messaged time"], "description":"extraction type"},
                                      IpywidgetsComponentsEnum.Dropdown, className = "w-auto")
    generateBtn = Utils.get_comp({"description":"generate"}, IpywidgetsComponentsEnum.Button, className="w-auto", bind = False)
    calculateBtn = Utils.get_comp({"description":"calculate"}, IpywidgetsComponentsEnum.Button,  bind = False)
    startTime = Utils.get_comp({"description":"start time"}, IpywidgetsComponentsEnum.DatePicker, className="w-auto", bind = False)
    endTime = Utils.get_comp({"description":"end time"}, IpywidgetsComponentsEnum.DatePicker, className="w-auto", bind = False)
    outarea = Utils.get_comp({}, ComponentsLib.CustomOutput, bind=False)
    container = Utils.container([attendenceRow.views.container,logsRow.views.container, Utils.container([typeOfExtraction, startTime, endTime]),
                                Utils.container([generateBtn, calculateBtn]), outarea], className="flex flex-column")
    memoization = {}
    attendenceDmp = DiscordMessageParser()
    logsDmp = DiscordMessageParser()
    
    someValues = ObjMaker.namespace()
    def set_up():
        now = datetime.now()
        lastMonth = datetime(year= now.year, month= now.month, day= 1) - timedelta(days=1)
        s.views.endTime.outputs.layout.value = lastMonth
        s.views.startTime.outputs.layout.value = datetime(year= lastMonth.year, month= lastMonth.month, day = 1)
    def get_keys_for_discord_time():
        return  set(map(lambda x: x[1].strip().lower(), s.process.attendenceDmp.handlers.get_filtered_results()))
    def create_options(w):
        ly = []
        s.process.msgs = s.handlers.get_keys()
        for ms in s.process.msgs:
            if ms in s.process.memoization:
                ly.append(s.process.memoization[ms])
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
                s.process.memoization[ms] = lay
                ly.append(lay)
        layout = widgets.HBox([widgets.VBox(ly), widgets.Textarea(value = json.dumps(s.handlers.extract_msg_state(), indent=4), 
                                                                disabled=True)])
        s.views.outarea.state.controller.display(layout, clear=True, ipy=True)
    def extract_msg_state():
        res = {}
        for k in s.process.memoization:
            res[k] = s.process.memoization[k].value
        return res
    def calcFunc(w):
        s.process.attendenceDmp.process.content = s.process.attendenceRow.handlers.get_content()
        s.process.logsDmp.process.content = s.process.logsRow.handlers.get_content()
        st = s.views.startTime.outputs.layout.value
        end = s.views.endTime.outputs.layout.value + timedelta(days= 1)
        
        s.process.attendenceDmp.handlers.set_date_range((st.year, st.month, st.day, 0, 0), (end.year, end.month, end.day, 0, 0))
        s.process.logsDmp.handlers.set_date_range((st.year, st.month, st.day, 0, 0), (end.year, end.month, end.day, 0, 0))
        s.views.outarea.state.controller.clear()
        day_wise_key_val, totalTime = s.handlers.day_wise_hours()
        def valFunc (key, val):
            return (key, val)
        def megerValFunc(key, val):
            if len(val) == 3:
                return (key, val[-1], val[0], val[1], "error")
            return (key, val[-1], val[0], val[1], val[-2] / (30*60))
        if (s.process.logsDmp.process.content != ""):
            logs_day_wise = s.handlers.get_counter_map()
            for ke in logs_day_wise:
                if ke not in day_wise_key_val:
                    print(ke, "does not exist in attendence")
                else:
                    logs_day_wise[ke].extend(day_wise_key_val[ke])
            day_wise_arr = s.handlers.make_array(logs_day_wise, ("date","hour", "logical logs", "total logs", 
                "expected logs nr"), megerValFunc)
        else:
            day_wise_arr = s.handlers.make_array(day_wise_key_val, ("date","hour"), valFunc)
        with s.views.outarea.state.controller._out:
            htmlDB.displayTableFromArray(day_wise_arr, displayIt=True)
            print("total hour: ", s.handlers.secs_to_hr_min(totalTime))
        s.process.someValues.day_wise_arr = day_wise_arr
    def make_array(keyVals, headers, valFunc):
        res = [headers]
        for key in keyVals:
            res.append(valFunc(key, keyVals[key]))
        return res
    def day_wise_hours():
        res = s.process.attendenceDmp.handlers.get_filtered_results()
        groups = OpsDB.group(res, lambda x: (x[0].year,x[0].month,x[0].day))
        day_wise = {}
        totalTime = 0
        for key in groups:
            try:
                per_day_grouped = ListDB.reshape(groups[key], (len(groups[key])// 2, 2))
                dayHours = s.handlers.day_time_calc(per_day_grouped)
                summed = sum(dayHours)
                totalTime += summed
                day_wise[key] = [summed, s.handlers.secs_to_hr_min(summed)]
            except:
                day_wise[key] = ["error"]
        return day_wise, totalTime
    def secs_to_hr_min(secs):
        res = ""
        remSec = secs
        hr = remSec // (60*60)
        if hr > 0:
            res += f"{hr} hr "
        remSec = remSec - hr* 60*60
        mi = remSec // (60)
        if mi > 0:
            res += f"{mi} min "
        remSec =  remSec - mi* 60
        if remSec > 0:
            res += f"{remSec} sec "
        return res.strip()
    def day_time_calc_for_discord_time(arr):
        state = s.handlers.extract_msg_state()
        res = []
        for st, end in arr:
            if state[st[1]] == "ignore" or state[end[1]] == "ignore":
                continue
            state[st[1]] == "started" and state[end[1]] == "left"
            res.append((end[0] - st[0]).seconds)
        return res
    def get_keys_for_messaged_time():
        return set(map(lambda x: s.handlers.key_getter(x[1]), s.process.attendenceDmp.handlers.get_filtered_results()))
    def key_getter(msg):
        return msg.replace("(edited)", "").strip().split("-")[0].strip().lower()
    def time_getter(msg):
        res = msg.replace("(edited)", "").strip().split("-")[-1].strip().strip(":").strip()
        res = list(map(int, res.split(":")))
        if len(res) == 1:
            res.append(0)
        return res
    def period_cal(x, y):
        a,b = x
        c,d = y
        if c < a:
            c += 12
        t1 = a *60 + b
        t2 = c * 60 + d
        re = t2-t1
        return timedelta(hours=re//60, minutes=re%60).seconds
    def get_dic_and_meaning(keys):
        dic = {}
        for ms in keys:
            if 'start' in ms:
                dic[ms] = StringEnum.STARTED
            elif 'break' in ms:
                dic[ms] = StringEnum.LEFT
            elif "done" in ms:
                dic[ms] = StringEnum.LEFT
            elif "left" in ms:
                dic[ms] = StringEnum.LEFT
            elif "back" in ms:
                dic[ms] = StringEnum.STARTED
        return dic
    def day_time_calc_for_messaged_time(arr):
        res = []
        state = s.handlers.extract_msg_state()
        for st, end in arr:
            stKey = s.handlers.key_getter(st[1])
            endKey = s.handlers.key_getter(end[1])
            if state[stKey] == "ignore" or state[endKey] == "ignore":
                continue
            state[stKey] == "started" and state[endKey] == "left"
            res.append(s.handlers.period_cal(s.handlers.time_getter(st[1]), s.handlers.time_getter(end[1])))
        return res
    def typeOfExtractionSelected(w):
        val = s.views.typeOfExtraction.outputs.layout.value
        if val == "discord time":
            s.handlers.get_keys = s.handlers.get_keys_for_discord_time
            s.handlers.day_time_calc = s.handlers.day_time_calc_for_discord_time
        elif val == "messaged time":
            s.handlers.get_keys = s.handlers.get_keys_for_messaged_time
            s.handlers.day_time_calc = s.handlers.day_time_calc_for_messaged_time
    def logsCounter(arr):
        counter = 0
        ld = None
        for nd, _ in arr:
            if ld is None:
                counter += 1
            else:
                if (nd-ld).seconds > (30 * 60):
                    counter += 1
                else:
                    continue
            ld = nd
        return counter
    def get_counter_map():
        res = s.process.logsDmp.handlers.get_filtered_results()
        groups = OpsDB.group(res, lambda x: (x[0].year,x[0].month,x[0].day))
        day_wise_counter = {}
        for key in groups:
            day_wise_counter[key] = [s.handlers.logsCounter(groups[key]), len(groups[key])]
        return day_wise_counter
    attendenceRow.views.selectFilesWid.handlers.handle = lambda x: s.process.memoization.clear()
    logsRow.views.selectFilesWid.handlers.handle = lambda x: x
    s = ObjMaker.uisOrganize(locals())
    typeOfExtractionSelected(1)
    typeOfExtraction.handlers.handle = typeOfExtractionSelected
    calculateBtn.handlers.handle = calcFunc
    generateBtn.handlers.handle = create_options
    return s

class Main:
    def gui():
        xy = AttendenceUI()
        xy.handlers.set_up()
        return xy