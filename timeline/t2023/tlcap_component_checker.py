from dataclasses import dataclass
import json, os
from useful.FileDatabase import File
import ipywidgets as widgets
from modules.Explorer.personalizedWidgets import GenerateNRowsBox
from timeline.t2023.tlcap.app_deploy import AppDeployment
class ViewType:
    Custom = "CUSTOM"
    LCAP = "BASE"
@dataclass
class ViewComponent:
    typ: ViewType
    innerComponents: list
    content: dict
    name: str
    idd: str
class ContainerChildren:
    def set_data(self, dat):
        STATIC_ACCORDION
class ViewExtractorForSingleUI:
    def set_component(self, view: ViewComponent):
        self._view = view
    def set_content(self, data: dict):
        if "type" in data:
            if data['type'] in ["COMPONENT", "GRID"]:
                self.set_component(self._make_component(data))
                return
        print(type(data))
        print(data)
        raise IOError("Not a UI component")
    def _make_component(self, data):
        # print(data.keys(), data)
        # print()
        if 'projection' in data:
            name = "projection"
            inner = []
            # if 'content' not in data[name]:
            #     print(data["componentName"])
            if data["componentName"] in ["STATIC_ACCORDION", "TABS", "DYNAMIC_TABLE"]:
                return ViewComponent(data['type'], [], data, data["componentName"], data["id"])

            # for ke in data[name]:
            for ele in data[name]["content"]:
                inner.append(self._make_component(ele))
            return ViewComponent(data['type'], inner, data, data["componentName"], data["id"])
        elif 'componentName' in data:
            return ViewComponent(data['type'], [], data, data["componentName"], data["id"])
        elif 'children' in data:
            inner = []
            name = "children"
            for ele in data[name]:
                inner.append(self._make_component(ele))
            return ViewComponent(data['type'], inner, data, data["componentName"], data["id"])
        if 'type' not in data:
            print(data.keys(), data)
            print()
        return ViewComponent(data['type'], [], data, data['component']['ref'], data["id"])
    def _key_re(self, name, data):
        inner = []
        for ke in data[name]:
            for ele in data[name][ke]:
                inner.append(self._make_component(ele))
        return ViewComponent(data['type'], inner, data, data["componentName"], data["id"])
    def get_components(self):
        comps = [(self._view.typ, self._view.name)]
        comps += self._get_components(self._view)
        return comps

    def _get_components(self, data: ViewComponent):
        res = []
        for el in data.innerComponents:
            res.append((el.typ, el.name))
            res += self._get_components(el)
        return res
class ViewExtractorApp:
    def __init__(self):
        self._components = []
    def set_ui_content(self, content: dict):
        self._components = self._extract_comps(content)
    def _extract_comps(self, content: dict):
        res = []
        vefsui = ViewExtractorForSingleUI()
        if 'views' in content:
            for ele in content['views']:
                vefsui.set_content(ele)
                res +=vefsui.get_components()
        elif 'projection' in content:
            vefsui.set_content(content)
            res +=vefsui.get_components()
        return res
    def get_components(self):
        return self._components

    def set_application_content(self, content: dict):
        self._data = content
        res = {}
        res[content['result']['productName']] = self._get_app_lvl_components(content['result'])
        for imp in content['result']['resolvedIncludes']:
            #print("\n", imp['pk']['name'])
            res[imp['pk']['name']] = self._get_app_lvl_components(imp)
        self._components = res
    def set_file(self, filepath):
        self.set_application_content(json.loads(File.getFileContent(filepath)))
    def _get_app_lvl_components(self, content: dict):
        comps = content['resources']['components']
        uis = list(filter(lambda x: x['name'] not in ["MainTemplate", "MyApp"], comps))
        res = {}
        for comp in uis:

            if comp['name'] in ['CInboxPageComponent', 'subInbox', "MessageCont","ContainerWithMsgs"]:
                #print(comp['name'])
                continue
            res[comp['name']] = self._extract_comps(comp)
        return res
    def get_component_used_freq(self):
        flattened = []
        res = self.get_components()
        for k in res:
            for kk, vv in res[k].items():
                flattened += vv
        freq = {}
        for val in flattened:
            if val not in freq:
                freq[val] = 0
            freq[val] += 1
        keys = sorted(freq, key =lambda x: freq[x], reverse=True)
        return {k: freq[k] for k in keys}
class Main:
    def get_freq(file):
        vea = ViewExtractorApp()
        vea.set_file(file)
        return vea.get_component_used_freq()
    def get_components(file):
        vea = ViewExtractorApp()
        vea.set_file(file)
        return vea.get_components()
    def get_ui(path="json"):
        from useful.TimeDB import TimeDB
        uic = UICompSearcherController()
        uic.set_model(FilesModel(path))
        view =TLCapUIComponentsSearchView()
        view._make_layout()
        uic.set_ui(view)
        uic.setup()
        uic._ui.filterWid.value =TimeDB.getTimeStamp().split(", ")[-1].replace(".", "")
        return uic
class FilesModel:
    def __init__(self, path):
        from useful.Path import Path
        self._path = path
        self._files = list(map(lambda x: (os.path.basename(x),x),Path.filesWithExtension("json",self._path)))
class TLCapUIComponentsSearchView:
    def __init__(self):
        self.gnrb =None
        self.out = None
    def _make_layout(self):
        self.out=widgets.Output()
        self.gnrb = GenerateNRowsBox(1)
        nrb = self.gnrb.get_child(0)
        self.filterWid = widgets.Text(placeholder ="filter", layout={'width':"100px"})
        nrb.add_widget(self.filterWid)
        self.drop = widgets.Dropdown(layout={'width':"auto"})
        nrb.add_widget(self.drop)
        self.uiSearchFreqbtn = widgets.Button(description= "get UIs freq", layout={'width':"auto"})
        nrb.add_widget(self.uiSearchFreqbtn)
        self.uiSearchBtn = widgets.Button(description= "get UIs", layout={'width':"auto"})
        nrb.add_widget(self.uiSearchBtn)
        self.depPrinter = widgets.Button(description= "dependencies", layout={'width':"auto"})
        nrb.add_widget(self.depPrinter)
        self.configPrinter = widgets.Button(description= "Configs variables", layout={'width':"auto"})
        nrb.add_widget(self.configPrinter)
        self.configForPasting = widgets.Button(description= "pasting configs", layout={'width':"auto"})
        nrb.add_widget(self.configForPasting)
        self.copyFilePath = widgets.Button(description= "copyFilePath", layout={'width':"auto"})
        nrb.add_widget(self.copyFilePath)
        # self.openModules = widgets.Button(description= "openImportedModules", layout={'width':"auto"})
        # nrb.add_widget(self.openModules)
    def display(self):
        if self.gnrb is None:
            self._make_layout()
        from IPython.display import display
        display(widgets.VBox([self.gnrb.get(), self.out]))
    @property
    def layout(self):
        if self.gnrb is None:
            self._make_layout()
        return widgets.VBox([self.gnrb.get(), self.out])
class UICompSearcherController:
    def __init__(self):
        self._depInstance = AppDeployment()
    def set_ui(self, ui_model: TLCapUIComponentsSearchView):
        self._ui = ui_model
    def set_model(self, model: FilesModel):
        self._model = model
    def setup(self):
        self._ui.drop.options = self._model._files
        self._ui.filterWid.observe(self._on_filtered, ["value"])
        self._ui.uiSearchFreqbtn.on_click(self._find_ui_freq)
        self._ui.uiSearchBtn.on_click(self._find_ui)
        self._ui.depPrinter.on_click(self._dep_print)
        self._ui.configPrinter.on_click(self._config_print)
        self._ui.configForPasting.on_click(self._config_to_paste)
        self._ui.copyFilePath.on_click(self._copy_file_path)
        # self._ui.openModules.on_click(self._open_imported_modules)
    def _copy_file_path(self, wid):
        from ancient.ClipboardDB import ClipboardDB
        ClipboardDB.copy2clipboard(os.path.abspath(self._ui.drop.value))
        self._ui.out.clear_output()
        with self._ui.out:
            print("copied")
    def _dep(self, func):
        filepath = self._ui.drop.value
        if filepath != self._depInstance._filepath:
            self._depInstance.set_file(filepath)
        self._ui.out.clear_output()
        with self._ui.out:
            func()
    def _dep_print(self, wid):
        self._dep(self._depInstance.printAllDependencies)
    def _config_print(self, wid):
        self._dep(self._depInstance.printAllConfigs)
    def _config_to_paste(self, wid):
        self._dep(self._depInstance.printConfigsForConfigEditing)
    def _on_filtered(self, wid):
        self._ui.drop.options = list(filter(lambda x: self._ui.filterWid.value in x[0],self._model._files))
    def _find_ui(self, btn):
        self._ui.out.clear_output()
        with self._ui.out:
            display(Main.get_components(self._ui.drop.value))
    def _find_ui_freq(self, btn):
        self._ui.out.clear_output()
        with self._ui.out:
            display(Main.get_freq(self._ui.drop.value))
    def _open_imported_modules(self, btn):
        self._pa_viewer = None
        def ins():
            self._pa_viewer = self._depInstance.open_all_imported_modules()
        self._dep(ins)