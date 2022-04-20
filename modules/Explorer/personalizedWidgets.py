from modules.Explorer.model import ExplorerUtils, DictionaryExplorer
from InterfaceDB import EmptyClass
class IRWidget:
    def get(self):
        pass
class IExplorer:
    def cd(self, key):
        pass
    def dirList(self):
        pass
    def goBack(self):
        pass
class IController:
    def run(self):
        pass
    def set_view_model(self, model: IRWidget):
        pass
class IExplorerDisplayer:
    def display(self):
        pass
class IRepondable:
    def set_callback(self, callback: IController):
        pass
class IBox:
    def add_widget(self, wid: IRWidget):
        pass
    def get_child(self, nr):
        pass
    def clear(self):
        pass
class RDropdown(IRWidget):
    def __init__(self):
        import ipywidgets as widgets
        self._wid = widgets.Dropdown()
    def set_options(self, options):
        self._wid.options = options
    def get(self):
        return self._wid
class Addable(IBox):
    def add_widget(self, wid):
        self._children.append(wid)
        if isinstance(wid, IRWidget):
            self._grid.append(wid.get())
        else:
            self._grid.append(wid)
class VRBox(Addable, IRWidget):
    def __init__(self):
        import ipywidgets as widgets
        self._container = widgets.VBox()
        self._children = []
    def get(self):
        return self._container
    def add_widget(self, wid):
        self._children.append(wid)
        if isinstance(wid, IRWidget):
            self._container.children += (wid.get(), )
        else:
            self._container.children += (wid, )
        
    def get_child(self, nr):
        return self._children[nr]
    def clear(self):
        self._container.children = ()
        self._children.clear()
class HRBox(VRBox):
    def __init__(self):
        import ipywidgets as widgets
        self._children = []
        self._container = widgets.HBox()
class HRContrainableBox(Addable, IRWidget):
    def __init__(self):
        self._grid = None
        self._children = []
    def set_width(self, width):
        from WidgetsDB import WidgetsDB
        self._width = width
        self._grid = WidgetsDB.getGrid(self._width, displayIt=False)
    def get(self):
        if self._grid is None:
            print("set width first")
            return
        return self._grid.mainLayout
    def get_child(self, nr):
        return self._children[nr]
    def clear(self):
        self._children.clear()
        self._grid.clearGrid()
class GRWidgetFromIpy(IRWidget):
    def __init__(self, wid):
        self._wid = wid
    def get(self):
        return self._wid
class GenerateNRowsBox(IRWidget):
    def __init__(self, n, add_row_labels= False):
        self._number_of_rows = n
        self._box = None
        self.set_row_widgets([HRBox() for i in range(n)])
        self._add_labels = add_row_labels
    def _make(self):
        import ipywidgets as widgets
        layout = VRBox()
        for i in range(self._number_of_rows):
            w = self._rows_widgets[i]
            if self._add_labels:
                w.add_widget(widgets.Label(value= str(i) + " : "))
            layout.add_widget(w)
        return layout
    def get(self):
        if self._box is None:
            self._box = self._make()
        return self._box.get()
    def get_child(self, nr):
        self.get()
        return self._box.get_child(nr)
    def set_row_widgets(self, row_widgets: list[IBox]):
        self._rows_widgets = row_widgets
class MetaExplorer(IExplorer):
    def __init__(self, exp: IExplorer):
        self._exp = exp
    def cd(self, key):
        if(key == '..'):
            return self._exp.goBack()
        if(key == '.'):
            return
        self._exp.cd(key)
    def goBack(self):
        self._exp.goBack()
    def dirList(self):
        folders, files = self._exp.dirList()
        folders = ['.','..'] + folders
        return folders, files
class DicExplorerAdapter(DictionaryExplorer):
    def dirList(self):
        return self.keys()
class WidgetsIpyExplorerDisplayer(IExplorerDisplayer, VRBox):
    def __init__(self, title=''):
        self._title = title
        self._wid = None
        self._exp = None
    def set_explorer(self, explorer: IExplorer):
        self._exp = explorer
        self._mexp = MetaExplorer(self._exp)
    def display(self):
        from IPython.display import display
        self.get() # makes sure that self._wid is created
        self._wid.components.title.value = self._title
        display(self._wid.layout)
        self._fill_values()
    def _create_layout(self):
        from WidgetsDB import WidgetsDB
        import ipywidgets as widgets
        wid = EmptyClass()
        wid.components = EmptyClass()
        wid.components.title, wid.components.dropdown, wid.components.text, wid.components.selection, \
            wid.components.outputDisplay = WidgetsDB._basicFileExplorerIO()
        wid.components.footer = HRContrainableBox()
        wid.components.footer._btns = {}
        max_buttons_in_a_row = 4
        wid.components.dropdown = widgets.Text()
        wid.components.disabled = True
        wid.components.footer.set_width(max_buttons_in_a_row)
        top = widgets.HBox(children=[wid.components.dropdown, wid.components.text],
                           layout = widgets.Layout(width = 'auto'))
        inputs = widgets.VBox([wid.components.title, top, wid.components.selection, wid.components.footer.get()],
                            layout = widgets.Layout(width = 'auto', max_width = "50%"))
        wid.layout = widgets.HBox([inputs, wid.components.outputDisplay])
        return wid
    def get(self):
        if self._wid is None:
            self._wid = self._create_layout()
        return self._wid
    def add_button(self, idd, button_widget):
        if idd in self._wid.components.footer._btns:
            return
        self._wid.components.footer._btns[idd] = button_widget
        self._wid.components.footer.add_widget(button_widget)
    def _fill_values(self):
        try:
            self._wid.components.selection.unobserve(self._on_dirlist_select, names = 'value')
        except Exception as e:
            pass
        folders, files = self._mexp.dirList()
        self._wid.components.selection.options = ExplorerUtils.dirsWithIcon(folders) + files
        self._wid.components.selection.observe(self._on_dirlist_select, names = 'value')
    def _on_dirlist_select(self, change):
        if(change['new'][0] == ExplorerUtils.dirIcon()):
            value = change['new'].replace(ExplorerUtils.dirIcon(), '').strip()
            self._mexp.cd(value)
            self._wid.components.text.value = ''
            self._update_loc(value)
            self._fill_values()
        else:
            self._wid.components.text.value = change['new']
            # clicked on file
        self._wid.components.outputDisplay.clear_output()
    def _update_loc(self, val):
        value = self._wid.components.dropdown.value
        vals = value.split("/")
        txt = '/'.join(vals + [val])
        if val == '..':
            txt = '/'.join(vals[:-1])
        self._wid.components.dropdown.value = txt
class SearchWidget(IRWidget):
    def __init__(self):
        self._gnrb = GenerateNRowsBox(2)
        self._initialize()
    def _initialize(self):
        import ipywidgets as widgets
        self._txt_wid = widgets.Text(placeholder="search text word")
        self._search_btn = widgets.Button(description="search")
        self._out = widgets.Output(layout=widgets.Layout(width='auto'))
        self._reg_widgets = widgets.Checkbox(description="reg", indent=False, layout={'width':"auto"})
        ch = self._gnrb.get_child(0)
        ch.add_widget(self._txt_wid)
        ch.add_widget(self._reg_widgets)
        ch.add_widget(self._search_btn)
        self._gnrb.get_child(1).add_widget(self._out)
        self._search_btn.on_click(self._on_search_click)
    def _on_search_click(self, btn_info):
        search_string = self._txt_wid.value.strip()
        self._out.clear_output()
        reg = self._reg_widgets.value
        with self._out:
            self._db.search(search_string, reg=reg)
    def set_database(self, db):
        self._db = db
    def get(self):
        return self._gnrb.get()
        
class Main:
    def explore(exp: IExplorer, title = "title"):
        wied = WidgetsIpyExplorerDisplayer(title)
        wied.set_explorer(exp)
        wied.display()
        return wied
    def gui_for_db(db):
        sw = SearchWidget()
        sw.set_database(db)
        return sw.get()