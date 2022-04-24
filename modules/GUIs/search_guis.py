from nice_design.interfaces import IDatabaseGUI, IAbout
import ipywidgets as widgets
from modules.SearchSystem.modular import HideableWidget
import datetime
from modules.SearchSystem.modular import JupyterResultDisplayer
from modules.Explorer.personalizedWidgets import GenerateNRowsBox, SearchWidget, RCheckbox
from OpsDB import OpsDB
from Path import Path
from Database import Database
import os
class IOps:
    def callback(self):
        pass
class GOps:
    def set_parent(self, parent):
        self._gnrb = parent._gnrb
        self._hw = parent._hw
        self._sw = parent._sw
class InLastNXXX(GOps):
    def callback(self):
        from jupyterDB import jupyterDB
        out = self._gnrb.get_child(2).get_child(0)
        out.clear_output()
        self._hw.hide()
        inLastFunc = self._gnrb.get_child(0).get_child(1).value
        n =  self._gnrb.get_child(0).get_child(0).value
        with out:
            db = jupyterDB.codeDumper().db(filterFunc=lambda x: jupyterDB.codeDumper().tools().dateCheckCondition(x)
                                      .__dict__[inLastFunc](n))
            self._sw.set_database(db)
            display(self._sw.get())
class Between(GOps):
    def __init__(self):
        self._okey_set = False
    def callback(self):
        out = self._gnrb.get_child(2).get_child(0)
        out.clear_output()
        if not self._okey_set:
            self._gnrb.get_child(1).get_child(2).on_click(self._ok_clicked)
        self._hw.show()
    def _ok_clicked(self, btn):
        from jupyterDB import jupyterDB
        fd = self._gnrb.get_child(1).get_child(0)
        td = self._gnrb.get_child(1).get_child(1)
        out = self._gnrb.get_child(2).get_child(0)
        out.clear_output()
        with out:
            frm = fd.value.year, fd.value.month, fd.value.day
            to = td.value.year, td.value.month, td.value.day
            self._sw.set_database(jupyterDB.codeDumper().db(filterFunc=lambda x: jupyterDB.codeDumper()
                                                      .tools().dateCheckCondition(x).between(frm, to)))
            display(self._sw.get())
class NDaysBefore(GOps):
    def callback(self):
        from jupyterDB import jupyterDB
        out = self._gnrb.get_child(2).get_child(0)
        out.clear_output()
        self._hw.hide()
        nday = self._gnrb.get_child(0).get_child(0).value
        if nday >0 :
            nday = nday* -1
        with out:
            self._sw.set_database(jupyterDB.codeDumper().db(nday=nday))
            display(self._sw.get())
class CodeDumperSearchGUI(IDatabaseGUI, IAbout):
    def __init__(self):
        self._make_layout()
        self._set_callbacks()
    def _make_layout(self):
        self._gnrb = GenerateNRowsBox(3)
        self._hw = HideableWidget()
        self._hw.set_widget(self._gnrb.get_child(1).get())
        self._hw.hide()
        self._gnrb.get_child(0).add_widget(widgets.BoundedIntText(description="n",min=0, layout ={"width":"auto"} ))
        self._gnrb.get_child(0).add_widget(
            widgets.Dropdown(
                options=['n days back', 'between', 'inLastNWeek', 'inLastNMonth', 'inLastNDays'],
                description="filter",
                layout=widgets.Layout(width='auto')
            )
        )
        self._gnrb.get_child(0).add_widget(widgets.Button(description="filter"))
        self._gnrb.get_child(1).add_widget(widgets.DatePicker( description='from',
                                    value = datetime.date.today()  - datetime.timedelta(1)))
        self._gnrb.get_child(1).add_widget(widgets.DatePicker(description="to", value=datetime.date.today()))
        self._gnrb.get_child(1).add_widget(widgets.Button(description="ok"))
        self._gnrb.get_child(2).add_widget(widgets.Output())
        self._gnrb.get_child(0).get_child(2).on_click(self._filterFunc)
        self._sw = SearchWidget()
    def _set_callbacks(self):
        inlastNxx = InLastNXXX()
        self._filters= {
            'n days back': NDaysBefore(),
            'between': Between(),
            'inLastNWeek': inlastNxx, 'inLastNMonth': inlastNxx, 'inLastNDays': inlastNxx
        }
        for vl in self._filters.values():
            vl.set_parent(self)
    def display(self):
        display(self._gnrb.get())
        return self._gnrb.get()
    def _filterFunc(self,btn):
        value = self._gnrb.get_child(0).get_child(1).value
        self._filters[value].callback()
    def display_info(self):
        return "search in daily logged code"
class PdfSearchGUI(IDatabaseGUI, IAbout):
    def __init__(self):
        self._make_layout()
    def _make_layout(self):
        self._gnrb = GenerateNRowsBox(2)
        self._gnrb.get_child(0).add_widget(widgets.Text(placeholder="path or variable name"))
        self._is_path_wid = RCheckbox(description="is path", indent = False, layout={'width': 'auto'})
        self._gnrb.get_child(0).add_widget(self._is_path_wid.get())
        self._gnrb.get_child(0).add_widget(widgets.Checkbox(
            description="walk", indent = False,  layout={'width': 'auto'}))
        self._gnrb.get_child(0).add_widget(widgets.Button(description="execute"))
        self._gnrb.get_child(1).add_widget(widgets.Output())
        self._hw = HideableWidget()
        self._hw.set_widget(self._gnrb.get_child(0).get_child(2))
        self._hw.hide()
        self._is_path_wid.on_changed(self._show_on_path_selected)
        self._sw = SearchWidget()
        self._gnrb.get_child(0).get_child(-1).on_click(self._pdf_search)
    def display(self):
        display(self._gnrb.get())
        return self._gnrb.get()
    def display_info(self):
        return "search in pdf files and or variables in the notebook"
    def _show_on_path_selected(self, btn):
        if self._is_path_wid.get().value:
            self._hw.show()
        else:
            self._hw.hide()
    def _pdf_search(self, btn):
        path = self._gnrb.get_child(0).get_child(1)
        val = self._gnrb.get_child(0).get_child(0).value.strip()
        if not path.value:
            files = jupyterDB._params[val]
        else:
            files = Path.filesWithExtension('pdf', val, walk=self._gnrb.get_child(0).get_child(2).value)
        out = self._gnrb.get_child(1).get_child(0)
        out.clear_output()
        with out:
            self._sw.set_database(Database.pdfDB(files))
            display(self._sw.get())
class IguiOps:
    def run(self):
        pass
    def info(self):
        pass
class ListCondaEnv(IguiOps):
    def run(self):
        out = gnrb.get_child(2).get_child(0)
        with out:
            print(OpsDB.cmd().run("conda env list"))
    def info(self):
        return ""
class CreateCondaEnv(IguiOps):
    def run(self):
        out = gnrb.get_child(2).get_child(0)
        out.clear_output()
        gnrb.get_child(1).get_child(1).description = "with latest python"
        btn = gnrb.get_child(1).get_child(2)
        btn._click_handlers.callbacks = []
        btn.on_click(self._execute)
    def _execute(self, btn):
        out = gnrb.get_child(2).get_child(0)
        out.clear_output()
        name = gnrb.get_child(1).get_child(0).value.strip()
        yesOrNo = gnrb.get_child(1).get_child(1).value
        if " " in name:
            print("there can not be space in the name")
            return
        withpyton = {True : "python", False :""}
        with out:
            print(OpsDB.cmd().run(f"conda create -n {name} {withpyton[yesOrNo]}"))
    def info(self):
        return "creating a new environment"
class DeleteCondaEnv(IguiOps):
    def run(self):
        out = gnrb.get_child(2).get_child(0)
        out.clear_output()
        gnrb.get_child(1).get_child(1).description = "delete everything"
        btn = gnrb.get_child(1).get_child(2)
        btn._click_handlers.callbacks = []
        btn.on_click(self._execute)
    def _execute(self, btn):
        out = gnrb.get_child(2).get_child(0)
        out.clear_output()
        name = gnrb.get_child(1).get_child(0).value.strip()
        yesOrNo = gnrb.get_child(1).get_child(1).value
        del_evrything = {True : "--all", False :""}
        with out:
            print(OpsDB.cmd().run(f"conda remove -n {name} {del_evrything[yesOrNo]}"))
    def info(self):
        return 'deleting old environment'
class CondaEnvCrudOpsGUI:
    def __init__(self):
        self._ops_map = {
            'list': ListCondaEnv(),
            'create': CreateCondaEnv(),
            'delete': DeleteCondaEnv()
        }
        self._make_layout()
    def _make_layout(self):
        self._gnrb = GenerateNRowsBox(3)
        self._gnrb.get_child(0).add_widget(widgtes.Dropdown(description="ops", options=list(ops_map.keys())))
        self._gnrb.get_child(0).add_widget(widgtes.Button(description="select"))
        self._gnrb.get_child(1).add_widget(widgtes.Text(description="name of env"))
        self._gnrb.get_child(1).add_widget(widgtes.Checkbox(description="with latest python"))
        self._gnrb.get_child(1).add_widget(widgtes.Button(description="confirm", layout={'width':'auto'}))
        self._gnrb.get_child(2).add_widget(widgtes.Output())
    def display(self):
        return self._gnrb.get()
    def _callback(self, btn):
        out = self._gnrb.get_child(2).get_child(0)
        out.clear_output()
        ops_index = self._gnrb.get_child(0).get_child(0).value
        with out:
            self._ops_map[ops_index].run()
            print(self._ops_map[ops_index].info())
class GeneralFileSearchGUI(GOps):
    def callback(self):
        path = self._gnrb.get_child(0).get_child(2)
        val = self._gnrb.get_child(0).get_child(1).value.strip()
        if not path.value:
            files = jupyterDB._params[val]
        else:
            files = Path.filesWithExtension(self._ext, val, walk=self._gnrb.get_child(0).get_child(3).value)
        out = self._gnrb.get_child(1).get_child(0)
        out.clear_output()
        with out:
            self._sw.set_database(self._func(files))
            display(self._sw.get())
    def set_extension(self, ext):
        self._ext = ext
    def set_database_func(self, func):
        self._func = func
class PdfFileSearchGUI(GeneralFileSearchGUI):
    def __init__(self):
        self.set_extension("pdf")
        self.set_database_func(Database.pdfDB)
class IpynbSearchGUI(GeneralFileSearchGUI):
    def __init__(self):
        self.set_extension("ipynb")
        self.set_database_func(Database.ipynbDB)
class VideoSearchGUI(GOps):
    def callback(self):
        path = self._gnrb.get_child(0).get_child(2)
        val = self._gnrb.get_child(0).get_child(1).value.strip()
        if not path.value:
            val = jupyterDB._params[val]
        out = self._gnrb.get_child(1).get_child(0)
        out.clear_output()
        with out:
            self._sw.set_database(Database.videoDB(val))
            display(self._sw.get())
class PathsSearchGUI(GOps):
    def callback(self):
        path = self._gnrb.get_child(0).get_child(1)
        val = self._gnrb.get_child(0).get_child(1).value.strip()
        if not path.value:
            files = jupyterDB._params[val]
        else:
            files = Path.getFiles(val, walk=self._gnrb.get_child(0).get_child(3).value)
        out = self._gnrb.get_child(1).get_child(0)
        out.clear_output()
        with out:
            self._sw.set_database(Database.pathDB(files))
            display(self._sw.get())
class AnyExtensionTextFileSearchGUI(GeneralFileSearchGUI):
    def __init__(self):
        self.set_database_func(Database.textFilesDB)
        self._ok = widgets.Button(description="ok", layout ={'width':'auto'})
        self._ext_wid = widgets.Text(placeholder="extension")
        self._ok.on_click(self._now_call)
    def callback(self):
        out = self._gnrb.get_child(1).get_child(0)
        out.clear_output()
        with out:
            display(widgets.HBox([self._ext_wid, self._ok]))
    def _now_call(self, tbn):
        val = self._ext_wid.value.strip()
        if val == "":
            return
        self.set_extension(val)
        super().callback()
class FileSearchGUI(IDatabaseGUI, IAbout):
    def __init__(self):
        self._ops = {
            'pdf': PdfFileSearchGUI(),
            'ipynb': IpynbSearchGUI(),
            'videos': VideoSearchGUI(),
            'paths': PathsSearchGUI(),
            'custom': AnyExtensionTextFileSearchGUI()
        }
        self._make_layout()
        for val in self._ops.values():
            val.set_parent(self)
    def _make_layout(self):
        self._gnrb = GenerateNRowsBox(2)
        self._gnrb.get_child(0).add_widget(widgets.Dropdown(options=list(self._ops.keys())))
        self._gnrb.get_child(0).add_widget(widgets.Text(placeholder="path or variable name"))
        self._is_path_wid = RCheckbox(description="is path", indent = False, layout={'width': 'auto'})
        self._gnrb.get_child(0).add_widget(self._is_path_wid.get())
        self._gnrb.get_child(0).add_widget(widgets.Checkbox(
            description="walk", indent = False,  layout={'width': 'auto'}))
        self._gnrb.get_child(0).add_widget(widgets.Button(description="execute"))
        self._gnrb.get_child(1).add_widget(widgets.Output())
        self._hw = HideableWidget()
        self._hw.set_widget(self._gnrb.get_child(0).get_child(3))
        self._hw.hide()
        self._is_path_wid.on_changed(self._show_on_path_selected)
        self._sw = SearchWidget()
        self._gnrb.get_child(0).get_child(-1).on_click(self._search)
    def display(self):
        display(self._gnrb.get())
        return self._gnrb.get()
    def display_info(self):
        return "search in files and or variables in the notebook"
    def _show_on_path_selected(self, btn):
        if self._is_path_wid.get().value:
            self._hw.show()
        else:
            self._hw.hide()
    def _search(self, btn):
        out = self._gnrb.get_child(1).get_child(0)
        out.clear_output()
        with out:
            val = self._gnrb.get_child(0).get_child(0).value
            self._ops[val].callback()
class SyntaxSearchGUI(IAbout, IDatabaseGUI):
    def __init__(self):
        self._make_layout()
        self._set_ops()
    def _make_layout(self):
        self._gnrb = GenerateNRowsBox(2)
        self._gnrb.get_child(0).add_widget(widgets.Dropdown(options= ['git', 'python', 'notepad', 'german_language',
                            'sympy', 'cpp', 'nodejs', 'ubuntu', 'regexs'], layout = {'width': 'auto'}))
        self._gnrb.get_child(0).add_widget(widgets.Text(placeholder="search word", layout = {'width': 'auto'}))
        self._gnrb.get_child(0).add_widget(widgets.Button(description="search"))
        self._gnrb.get_child(1).add_widget(widgets.Output())
        self._gnrb.get_child(0).get_child(2).on_click(self._callback)
    def _set_ops(self):
        from jupyterDB import jupyterDB
        si = jupyterDB.syntax().db_ops()
        self._ops_map = {k: si.__dict__[k].db() for k in si.__dict__}
        from javascript.Nodejs import Nodejs
        self._ops_map['nodejs'] = Nodejs.syntax()
        from NumericalAnalysis import NumericalAnalysis
        self._ops_map['sympy'] = NumericalAnalysis.sympySyntax()
        from cpp.Cpp import Cpp
        self._ops_map['cpp'] = Cpp.syntax()
        from UbuntuDB import UbuntuDB
        self._ops_map['ubuntu'] = UbuntuDB.commands()
        from RegexDB import RegexDB
        self._ops_map['regexs'] = RegexDB.regexs()
    def _callback(self, btn):
        out = self._gnrb.get_child(1).get_child(0)
        out.clear_output()
        lang = self._gnrb.get_child(0).get_child(0).value
        with out:
            self._ops_map[lang].search(self._gnrb.get_child(0).get_child(1).value)
    def display(self):
        display(self._gnrb.get())
        return self._gnrb.get()
    def display_info(self):
        options = " ".join(self._gnrb.get_child(0).get_child(0).options)
        return options
from archives.locally_temporal.Android import Android
from archives.locally_temporal.DB_SWT import DB_SWT
from archives.locally_temporal.DataScience import DataScience
class ISubSearch:
    def execute(self):
        pass
class GSubSearchWithParent(ISubSearch):
    def set_parent(self, parent):
        self._parent = parent
        self._sw = parent._sw
class GSubjectWithOptionsSearch(ISubSearch):
    def __init__(self):
        self._layout = None
        self._make_layout()
    def set_options(self, options):
        self._options = options
        self._funcs_wid = widgets.Dropdown(options=self._options, layout = {'width': 'auto'})
    def _make_layout(self):
        self._search_btn = widgets.Button(description="search")
        self._out = widgets.Output()
    def execute(self):
        if self._layout is None:
            self._layout = widgets.VBox([widgets.HBox([self._funcs_wid, self._search_btn]), self._out])
        display(self._layout)
class AndroidSearchGUI(GSubSearchWithParent):
    def __init__(self):
        self._gsub = GSubjectWithOptionsSearch()
        self._gsub.set_options(['fileNameSearch', 'pdfFiles', 'fileContentSearch', 'xmlFiles', 'allXmlFiles'])
        self._gsub._search_btn.on_click(self._clicked)
    def _clicked(self, btn):
        self._gsub._out.clear_output()
        self._sw.set_database(Android.__dict__[self._gsub._funcs_wid.value]())
        with self._gsub._out:
            display(self._sw.get())
    def execute(self):
        self._gsub.execute()
class SWT_Technik(GSubSearchWithParent):
    def execute(self):
        self._sw.set_database(DB_SWT.swt().docs())
        display(self._sw.get())
class DBSub(GSubSearchWithParent):
    def __init__(self):
        self._gsub = GSubjectWithOptionsSearch()
        self._gsub.set_options(['docs', 'exercises'])
        self._ops = {
            'docs': DB_SWT.db().docs(),
            'exercises': DB_SWT.db().exercise().contentSearch()
        }
        self._gsub._search_btn.on_click(self._clicked)
    def execute(self):
        self._gsub.execute()
    def _clicked(self, btn):
        self._gsub._out.clear_output()
        self._sw.set_database(self._ops[self._gsub._funcs_wid.value])
        with self._gsub._out:
            display(self._sw.get())
class DataScienceSearchGUI(GSubSearchWithParent):
    def __init__(self):
        from DataStorageSystem import UrlsTable
        from LibsDB import LibsDB
        from Path import Path
        self._gsub = GSubjectWithOptionsSearch()
        self._gsub._search_btn.on_click(self._clicked)
        self._ops = {
            'links': UrlsTable(dbPklFile=Path.joinPath(LibsDB.cloudPath(), 'timeline', '6. sixth semester', 
                                                       'Data Science', 'ops', 'exam_prep', '_rajaDB', 
                                                       'TBN77cLo1ktTmGW.pkl')),
            'docs paths': DataScience.docs().pathDB(),
            'solution': DataScience.docs().solutions().pdfForm(),
            'question': DataScience.docs().contentDB(),
            'exercises': DataScience.exercises().contentDB()
        }
        self._gsub.set_options(list(self._ops.keys()))
    def execute(self):
        self._gsub.execute()
    def _clicked(self, btn):
        self._gsub._out.clear_output()
        self._sw.set_database(self._ops[self._gsub._funcs_wid.value])
        with self._gsub._out:
            display(self._sw.get())
class MathSearchGUI(GSubSearchWithParent):
    def __init__(self):
        self._gsub = GSubjectWithOptionsSearch()
        self._gsub._search_btn.on_click(self._clicked)
        self._set_ops()
    def _set_ops(self):
        self._ops = {}
    def _clicked(self, btn):
        self._gsub._out.clear_output()
        self._sw.set_database(self._ops[self._gsub._funcs_wid.value])
        with self._gsub._out:
            display(self._w.get())
# class LinearAlgebraSearchGUI(MathSearchGUI):
#     def _set_ops(self):
#         self._ops = {
#             'docs': ,
#             'la 1 exercise': ,
#             'la 1 solution': ,
#             'la 1 solution mine': ,
#             'la 2 exercise': ,
#             'la 2 solution': ,
#         }
# class AnalysisSearchGUI(MathSearchGUI):
#     def _set_ops(self):
#         self._ops = {
#             'analysis 1 docs': ,
#             'analysis 1 exercises cw': ,
#             'analysis 1 exercises hw': ,
#             'analysis 1 solutions cw': ,
#             'analysis 1 solutions hw': ,
#             'analysis 1 docs': ,
#         }
# class NumericalAnalysisSearchGUI(MathSearchGUI):
#     def _set_ops(self):
#         self._ops = {
#             'analysis 1 docs': ,
#             'analysis 1 exercises': ,
#             'analysis 1 solutions': ,
#             'analysis 1 docs': ,
#         }
# class Sto(MathSearchGUI):
#     def _set_ops(self):
#         pass
class BachelorSubjectSearchGUI(IAbout, IDatabaseGUI):
    def __init__(self):
        self._ops_map = {
                'android': AndroidSearchGUI(),
                'software': SWT_Technik(),
                'database': DBSub(), 
                'data science': DataScienceSearchGUI()
            }
        self._make_layout()
        for val in self._ops_map.values():
            val.set_parent(self)
    def _make_layout(self):
        self._gnrb = GenerateNRowsBox(3)
        self._gnrb.get_child(0).add_widget(widgets.Dropdown(options=["android", "software", 'database', 'data science', 
                                                              'maths', 'machine learning', 'ihk'],
                                                    layout= {'width':'auto'} ))
        self._gnrb.get_child(0).add_widget(widgets.Button(description="select"))
        self._out = widgets.Output()
        self._gnrb.get_child(2).add_widget(self._out)
        self._gnrb.get_child(0).get_child(1).on_click(self._ok_clicked)
        self._sw = SearchWidget()
    def display(self):
        display(self._gnrb.get())
        return self._gnrb.get()

    def display_info(self):
        return " ".join(self._ops_map.keys())
    def _ok_clicked(self, btn):
        self._out.clear_output()
        with self._out:
            sub =self._gnrb.get_child(0).get_child(0).value
            if sub in self._ops_map:
                self._ops_map[sub].execute()
            else:
                print('not implemented yet')