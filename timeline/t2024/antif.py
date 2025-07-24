from useful.basic import Main as ObjMaker
from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum
def ExecFilterers():
    instances = {}
    parent = None
    prev_on_change = None
    def load(content):
        xx= {}
        exec(content, xx)
        return xx["f"]
    def execute(key, content, ctx):
        if key not in s.process.instances:
            s.process.instances[key] = s.handlers.load(content)
        return s.process.instances[key](ctx)
    s = ObjMaker.variablesAndFunction(locals())
    return s
def CaseBlock():
    casesRunner = {}
    undoers = []
    def run(case):
        for func in s.process.undoers:
            func(s)
        if case in s.process.casesRunner:
            s.process.casesRunner[case](case, s)     
        s.handlers.postRun(case, s)
    def postRun():
        pass
    s = ObjMaker.variablesAndFunction(locals())
    return s
def NewDropDown():
    dropdown = Utils.get_comp({"options": ["add",'update',"delete"]},IpywidgetsComponentsEnum.Dropdown, className = "w-auto")
    def onDefault(w, ctx):
        pass
    keysWithActions = {}
    undoers = []
    def postProcessing(ctx):
        pass
    def onChange(w):
        val = s.views.dropdown.outputs.layout.value
        for func in s.process.undoers:
            func(s)

        if val in s.process.keysWithActions:
            s.process.keysWithActions[val](val, s)
        else:
            s.handlers.onDefault(val, s)
        
        s.handlers.postProcessing(s)
    dropdown.handlers.handle = onChange
    s = ObjMaker.uisOrganize(locals())
    return s