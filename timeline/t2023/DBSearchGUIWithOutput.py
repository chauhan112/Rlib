import ipywidgets as widgets
from modules.Explorer.personalizedWidgets import CustomOutput
class SearchWidgetWithOutputVisible:
    def __init__(self):
        self._layout = None
        self.set_clicked_output_region(CustomOutput())
        self.set_output_clickable_region(CustomOutput())
    def _make_layout(self):
        if self._layout is None:
            self._txt_wid = widgets.Text(placeholder="search text word")
            self._search_btn = widgets.Button(description="search", layout = {"width":"auto" })
            self._reg_widgets = widgets.Checkbox(description="reg", indent=False, layout={'width':"auto"})
            self._layout = widgets.VBox([widgets.HBox([self._txt_wid, self._reg_widgets, self._search_btn]), 
                                         self._coout.get_layout(), self._click_display_region.get_layout()])
        return self._layout
    def set_database(self, db ):
        self._db = db
    def set_up(self):
        self._search_btn.on_click(self._search)
    def _search(self, vbtbn):
        search_string = self._txt_wid.value.strip()
        reg = self._reg_widgets.value
        self._db.default_display(False)
        res = self._db.search(search_string, reg=reg)
        self._coout.display(res, ipy=True, clear=True)
    def set_output_clickable_region(self, clickable_region):
        self._coout = clickable_region
    def set_clicked_output_region(self, out):
        self._click_display_region = out