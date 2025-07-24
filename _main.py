def Abc():
    from basic import Main as ObjMaker
    from modules.rlib_notebook_tools.instructions_tool import GNotebookLayoutController
    from timeline.t2024.Array import Array
    parent = None
    def get_bsc():
        from useful.jupyterDB import jupyterDB
        callers = jupyterDB._params["rlib"].kvs.process.realtime.process.callers
        for (k,idd,t), v in callers.items():
            if k == "work-calc2":
                return v.process.att
    def timetofloat(timestr):
        res = timestr.split("hr")
        if len(res) == 1:
            return valueForMin(res[0])/60
        else:
            
            return int(res[0]) + valueForMin(res[1])/60 
    def valueForMin(val):
        newVal= val.strip().strip("min").strip()
        if newVal == "":
            return 0
        return int(newVal)
    def simpleCalc(index):
        bsc = s.handlers.get_bsc()
        rems = Array(bsc.process.someValues.day_wise_arr[1:]).filter(lambda x: x[1] != "error")
        remsSize = 0
        total = rems.map(lambda x: x[index]).sum()
        for _, hr, ll, tl, ex in rems.array:
            if timetofloat(hr) > 5:
                remsSize += 2
            else:
                remsSize += 1
        return (total + remsSize )/ 2
    def advanceCalc():
        bsc = s.handlers.get_bsc()
        def effective_hour(hr, nl):
            def funcCalc(nl, y):
                if nl < y-1:
                    return 0.5 * nl + (y-1-nl) * 0.1
                return hr
            thr = 0
            if hr <= 1: 
                pass
            elif hr <= 5:
                exp_log = hr* 2
                thr += funcCalc(nl, exp_log)
            elif hr <= 9:
                thr += 5
                exp_log = ((hr-5) * 2) - 1
                thr += funcCalc(nl - 8, exp_log)
            return thr
        return Array(bsc.process.someValues.day_wise_arr[1:]).filter(lambda x: x[1] != "error").map(
                lambda x: effective_hour(timetofloat(x[1]), int(x[2])  + (int(x[3]) - int(x[2]))/2)).sum()
    def run(x):
        output = s.process.parent.process.parent.views.outputArea
        output.outputs.layout.clear_output()
        with output.outputs.layout:
            print("simple method (here i just give each day one extra logs and divide the remaining by 2 to calculated the effective work)")
            print("if there are some error in attendence, then i would need to manually calculte for that")
            print("--"* 20)
            print("result: ", simpleCalc(2))
            print("\n"*2)
            print("result based on total logs: ", simpleCalc(3))
            
    def set_parent(parent):
        s.process.parent = parent
    s = ObjMaker.variablesAndFunction(locals())
    return s
res = Abc()