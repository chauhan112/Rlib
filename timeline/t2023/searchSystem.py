from Path import Path
from LibPath import getPath
import os
from FileDatabase import NotepadAppTextOpener
import ipywidgets as widgets
from SearchSystem import FilesContentSearch, ISearch
from timeline.t2023.links_crud_ui import ButtonsClickView, SearchEngine
from timeline.t2023.links_crud_ui import ButtonViewWithPagination

class NotepadOpener:
    def openIt(self, path, lineNr):
        nato = NotepadAppTextOpener()
        nato.setData(lineNr)
        nato.openIt(path)
class CodeSearchEngine:
    def __init__(self):
        self._een = None
        self.set_file_opener(NotepadOpener())
        self.set_result_displayer(ButtonsClickView())
        self.set_files(Path.filesWithExtension("py", getPath()))
    def get_engine(self):
        if self._een is None:
            self._displayer.set_element_maker(self._button_maker)
            self._displayer.set_btn_click_func(self._btn_click)
            self._een = SearchEngine()
            self._een.set_engine(self._fcs)
            self._een.set_result_maker(self._displayer)
            self._een.default_display(False)
        return self._een
    def set_result_displayer(self, resDisplayer):
        self._displayer = resDisplayer
    def set_file_opener(self, opener):
        self._opener = opener
    def _btn_click(self, resElemInfo):
        path, lineNr = resElemInfo
        self._opener.openIt(path, lineNr)
    def _button_maker(self, resElemInfo, onclick):
        path, lineNr = resElemInfo
        btn = widgets.Button(description=os.path.basename(path), tooltip=path, layout= {"width": "auto", 
                                                                                        "max_width": "150px"})
        if onclick is not None:
            btn.on_click(lambda x: onclick(resElemInfo))
        return btn
    def set_files(self, files):
        self._fcs = FilesContentSearch(files)
        self._een = None
class Main:
    def searchWithPagination(db: ISearch, btn_maker_func = None, btn_click_func = None):
        see = SearchEngine()
        bvvp = ButtonViewWithPagination()
        if btn_maker_func:
            bvvp.set_element_maker(btn_maker_func)
        if btn_click_func:
            bvvp.set_btn_click_func(btn_click_func)
        see.set_result_maker(bvvp)
        see.set_engine(db)
        see.default_display(False)
        return see