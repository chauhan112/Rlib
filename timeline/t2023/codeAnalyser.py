import ipywidgets as widgets
from timeline.t2023.generic_logger.components import SingleButtonController
from modules.Explorer.personalizedWidgets import CustomOutput
from archives.ParserDB import TypeScriptParser

class CodeAnalyserView:
    def __init__(self):
        self.filepath = widgets.Text(placeholder = "enter file path")
        self.depthplot = SingleButtonController(description ="depth", layout = {"width":"auto"})
        self.out = CustomOutput()
        self.layout = widgets.VBox([widgets.HBox([self.filepath, self.depthplot.layout]), self.out.get_layout()])
class CodeAnalyserController:
    def set_view(self, view):
        self._view = view
    def set_up(self):
        self._view.depthplot.set_clicked_func(self._depth_ana)
    def _depth_ana(self, wid):
        path = self._view.filepath.value.strip()
        from FileDatabase import File
        if path:
            code = File.getFileContent(path)
            mp = TypeScriptParser.parse_layers3(TypeScriptParser.remove_single_line_comments(TypeScriptParser.remove_empty_lines(code)))
            mp.keys()
            self._view.out.display(list(map(lambda x: len(mp[x]), mp)), True)
class Main:
    def analyserUI():
        view = CodeAnalyserView()
        cnt = CodeAnalyserController()
        cnt.set_view(view)
        cnt.set_up()
        return cnt