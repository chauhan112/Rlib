from modules.Explorer.model import ExplorerUtils, DictionaryExplorer
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
    def add_rwidget(self, wid: IRWidget):
        pass
    def add_ipywidget(self, wid):
        pass
    def get_child(self, nr):
        pass
class RDropdown(IRWidget):
    def __init__(self):
        self._wid = widgets.Dropdown()
    def set_options(self, options):
        self._wid.options = options
    def get(self):
        return self._wid
class Addable(IBox):
    def add_rwidget(self, wid: IRWidget):
        self.add_ipywidget(wid.get())
    def add_ipywidget(self, wid):
        self._grid.append(wid)
class VRBox(Addable, IRWidget):
    def __init__(self):
        import ipywidgets as widgets
        self._container = widgets.VBox()
        self._children = []
    def get(self):
        return self._container
    def add_ipywidget(self, wid):
        self._container.children += (wid, )
    def get_child(self, nr):
        return self._children[nr]
    def add_rwidget(self, wid: IRWidget):
        self._children.append(wid)
        self.add_ipywidget(wid.get())
class HRBox(VRBox):
    def __init__(self):
        self._children = []
        import ipywidgets as widgets
        self._container = widgets.HBox()
class HRContrainableBox(Addable):
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
    def add_ipywidget(self, wid):
        self.get()
        self._grid.append(wid)
        self._children.append(wid)
    def get_child(self, nr):
        return self._children[nr]
class GRWidgetFromIpy(IRWidget):
    def __init__(self, wid):
        self._wid = wid
    def get(self):
        return self._wid
class EmptyClass:
    def __init__(self):
        pass
class GenerateNRowsBox(Addable):
    def __init__(self, n, add_row_labels= False):
        self._number_of_rows = n
        self._box = self._make(n, add_row_labels)
    def _make(self, n, add_row_labels):
        layout = VRBox()
        for i in range(n):
            w = HRBox()
            if add_row_labels:
                w.add_ipywidget(widgets.Label(value= str(i) + " : "))
            layout.add_rwidget(w)
        return layout
    def get(self):
        return self._box.get()
    def get_child(self, nr):
        return self._box.get_child(nr)
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
        self.get() # makes sure that self._wid is created
        self._wid.components.title.value = self._title
        display(self._wid.layout)
        self._fill_values()
    def _create_layout(self):
        import ipywidgets as widgets
        from WidgetsDB import WidgetsDB
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
class Main:
    def explore(exp: IExplorer, title = "title"):
        wied = WidgetsIpyExplorerDisplayer(title)
        wied.set_explorer(exp)
        wied.display()
        return wied