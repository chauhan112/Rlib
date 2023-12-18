from timeline.t2023.advance_pickle_crud import Main as PickleCrudOps
from modules.SearchSystem.modular import HideableWidget
from LibsDB import LibsDB
from SystemInfo import SystemInfo
from SerializationDB import SerializationDB
import threading
import subprocess
import platform
from basic import NameSpace
class Functionality:
    def console_open(self, path):
        device = self.app.controller.utils.device_unique_identifier()
        mapped_path = self.app.controller.pathMapper.map(device, path)
        if device == self.app.model.enums.devices.GamingLaptop:
            self.app.controller.utils.function_to_run_on_thread = self.app.controller.core.window.console.open
        elif device == self.app.model.enums.devices.Laptop2019:
            self.app.controller.utils.function_to_run_on_thread = self.app.controller.core.window.console.open
        elif device == self.app.model.enums.devices.OpenSuseOffice:
            self.app.controller.utils.function_to_run_on_thread = self.app.controller.core.opensuse.console.open
        else:
            print("unknown device detected")
            return
        self.app.controller.utils.run_on_thread(mapped_path)
    def explorer_open(self, path):
        device = self.app.controller.utils.device_unique_identifier()
        mapped_path = self.app.controller.pathMapper.map(device, path)
        if device == self.app.model.enums.devices.GamingLaptop:
            self.app.controller.utils.function_to_run_on_thread = self.app.controller.core.window.explorer.open
        elif device == self.app.model.enums.devices.Laptop2019:
            self.app.controller.utils.function_to_run_on_thread = self.app.controller.core.window.explorer.open
        elif device == self.app.model.enums.devices.OpenSuseOffice:
            self.app.controller.utils.function_to_run_on_thread = self.app.controller.core.opensuse.explorer.open
        else:
            print("unknown device detected")
            return
        self.app.controller.utils.run_on_thread(mapped_path)
    def path_mapper(self, device, path):
        if (device, path) in self.app.controller.pathMapper.value:
            return self.app.controller.pathMapper.value[(device, path) ]
        return path
    def device_unique_identifier(self):
        uname = platform.uname()
        if SystemInfo.getName() == "linux-ier9":
            return self.app.model.enums.devices.OpenSuseOffice
        elif uname.system == "Windows" and uname.machine == "AMD64":
            return self.app.model.enums.devices.GamingLaptop
        return self.app.model.enums.devices.Unknown
    def get_current_path(self, wid):
        key = wid.description
        prev_size = len(self.app.views._model._loc)
        self.app.views._parent._key_clicked_default(wid)
        after_size = len(self.app.views._model._loc)
        val = self.app.views._model.value()
        if after_size == prev_size:
            val = val[key]
        return val
    def is_console(self):
        return self.app.views._model._loc[0] != "paths"
    def console_opener_opensuse(path):
        subprocess.run(["konsole", "--workdir", path])
    def console_opener_laptop2022(path):
        subprocess.run(['start', 'cmd', '/K', 'cd', path, '&&', "call", r"C:\Users\rajab\miniconda3\Scripts\activate.bat" , 
                         r"C:\Users\rajab\miniconda3"], shell=True)
    def console_opner_laptop2019(path):
        raise IOError("not defined")
    def explorer_opener_opensuse(path):
        subprocess.run(["dolphin", path])
    def explorer_opener_laptop2022(path):
        subprocess.run(["explorer", path])
    def explorer_opner_laptop2019(path):
        raise IOError("not defined")
    def function_to_run_on_thread_wrapper(self, path):
        try:
            self.app.controller.utils.function_to_run_on_thread(path)
        except Exception as e:
            print(f"Error opening folder: {e}")
class ConsoleFuncNFolderFunc:
    def __init__(self):
        self._opener_app = ["konsole", "--workdir"]
    def on_component_select(self, wid):
        val = self.app.controller.viewsValue.get_current_path(wid)
        if type(val) == str:
            if self.app.controller.utils.is_console():
                self.app.controller.console.open(val)
            else:
                self.app.controller.explorer.open(val)
    def set_up(self):
        self.app.data = self.app.dataloader.load()
        
        lay, cont = PickleCrudOps.keyValueCrud(self.app.data)
        HideableWidget.hideIt(cont._basic._view.locationView.lastKeyWidg)
        cont._basic._view.layout.layout.border = None
        HideableWidget.hideIt(cont._basic._view.keysView.labelWidg)
        HideableWidget.hideIt(cont._basic._view.opsRow)
        cont._basic._view.layout.layout.min_height = None
        HideableWidget.hideIt(cont._basic._view.outputSection.get_layout())
        cont.set_key_selected_func(self.on_component_select)
        self.layout = lay
        
        self.app.views = cont._basic       
        self.app.controller.component_select_func = self.on_component_select
        self.app.controller.utils.function_to_run_on_thread = self._open_folder
        self.app.controller.utils.run_on_thread = self._open_in_thread
        
        ff = Functionality()
        ff.app = self.app
        
        self.app.controller.console.open = ff.console_open
        self.app.controller.explorer.open = ff.explorer_open
        self.app.controller.pathMapper.map = ff.path_mapper

        self.app.controller.utils.device_unique_identifier = ff.device_unique_identifier
        self.app.model.enums.devices.GamingLaptop = 1
        self.app.model.enums.devices.OpenSuseOffice = 2
        self.app.model.enums.devices.Laptop2019 = 3
        self.app.model.enums.devices.Unknown = 4
        self.app.controller.viewsValue.get_current_path = ff.get_current_path
        self.app.controller.utils.is_console = ff.is_console
        self.app.controller.core.window.explorer.open = Functionality.explorer_opener_laptop2022
        self.app.controller.core.opensuse.explorer.open = Functionality.explorer_opener_opensuse
        self.app.controller.core.window.console.open = Functionality.console_opener_laptop2022
        self.app.controller.core.opensuse.console.open = Functionality.console_opener_opensuse
        
    def structure_setup(self):
        self.app = NameSpace()
        self.app.controller  = NameSpace()
        self.app.model = NameSpace()
        self.app.controller.utils =NameSpace()
        self.app.dataloader = NameSpace()
        self.app.controller.pathMapper = NameSpace()
        self.app.controller.console = NameSpace()
        self.app.controller.explorer = NameSpace()
        self.app.controller.pathMapper = NameSpace()
        self.app.model.enums = NameSpace()
        self.app.model.enums.devices = NameSpace()
        self.app.controller.viewsValue = NameSpace()
        self.app.controller.core = NameSpace()
        self.app.controller.core.window = NameSpace()
        self.app.controller.core.window.explorer = NameSpace()
        self.app.controller.core.opensuse = NameSpace()
        self.app.controller.core.opensuse.explorer = NameSpace()
        self.app.controller.core.window.console = NameSpace()
        self.app.controller.core.opensuse.console = NameSpace()
        
    def _open_in_thread(self, folder_path):
        folder_thread = threading.Thread(target=self.app.controller.utils.function_to_run_on_thread, args=(folder_path,))
        folder_thread.start()
    def _open_folder(self, path):
        try:
            subprocess.run(self._opener_app + [path])
        except Exception as e:
            print(f"Error opening folder: {e}")
class Main:
    def console_and_folder_opener():
        cfff = ConsoleFuncNFolderFunc()
        cfff.structure_setup()
        cfff.app.dataloader.load = lambda : SerializationDB.readPickle(LibsDB.picklePath("globals"))["pathsNConsoles"]
        cfff.set_up()
        
        cfff.app.views._parent.set_mode_selector(lambda x: x)
        HideableWidget.showIt(cfff.app.views._view.fileView.opsCheckbox)
        HideableWidget.hideIt(cfff.app.views._view.fileView.pathTextWidg)
        HideableWidget.hideIt(cfff.app.views._view.fileView.labelWidg)
        cfff.app.views._view.fileView.opsCheckbox.description = "explorer"
        def is_console(app):
            return not app.views._view.fileView.opsCheckbox.value
        cfff.app.controller.utils.is_console = lambda : is_console(cfff.app)
        return cfff