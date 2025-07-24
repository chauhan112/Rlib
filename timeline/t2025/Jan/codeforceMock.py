from useful.basic import Main as ObjMaker
def MockTestCodeForces():
    lines = []
    def set_text(text):
        s.process.lines = text.strip().splitlines()
        s.process.index = 0
    def inputt():
        s.process.index += 1
        return s.process.lines[s.process.index-1]
    def reset():
        s.process.index = 0
    s = ObjMaker.variablesAndFunction(locals())
    return s