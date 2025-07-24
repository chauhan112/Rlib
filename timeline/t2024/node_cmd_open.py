from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from useful.basic import Main as ObjMaker
import platform
import threading
import subprocess

def OpenCmdOnthread():
    textWid = Utils.get_comp({"placeholder":"enter path"}, IpywidgetsComponentsEnum.Text, className="w-auto", bind = False)
    btn = Utils.get_comp({"description":"open node cmd with conda"},IpywidgetsComponentsEnum.Button, className = "w-auto")
    container = Utils.container([textWid, btn])
    def console_opener_laptop2022(path):
        subprocess.run([r"C:\Users\rajab\Desktop\stuffs\global\experiments\2024\nodeNConda.bat", path], shell=True)
    def open_in_thread(func, folder_path):
        folder_thread = threading.Thread(target=func, args=(folder_path,))
        folder_thread.start()
    def onBtnClicked(w):
        uname = platform.uname()
        if uname.system == "Windows" and uname.machine == "AMD64":
            path =  s.views.textWid.outputs.layout.value.strip()
            open_in_thread(console_opener_laptop2022, path )
    btn.handlers.handle = onBtnClicked
    def run(x):
        output = s.process.parent.process.parent.views.outputArea
        output.outputs.layout.clear_output()
        with output.outputs.layout:
            display(container.outputs.layout)
    def set_parent(parent):
        s.process.parent = parent
    s = ObjMaker.uisOrganize(locals())
    return s
