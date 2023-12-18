class JsonExplorer:
    def __init__(self):
        from basic import NameSpace
        self._res = NameSpace()
    def key_clicked(self, btn, *param):
        cnt = self._cnt
        cnt._current_key = None
        cnt._basic._view.outputSection.clear()
        val = cnt._basic._model.value()
        if cnt._basic._model.isDic():
            cnt._basic._model.goForward(btn.description)
            cnt._basic._view.locationView.locationWidg.value = "/".join(map(str,cnt._basic._model._loc))
            cnt._basic._view.opsView.keyWidg.value = btn.description
        elif type(val) == list:
            cnt._basic._model.goForward(int(btn.description))
            cnt._basic._view.locationView.locationWidg.value = "/".join(map(str,cnt._basic._model._loc))
        val = cnt._basic._model.value()
        if cnt._basic._model.isDic():
            cnt._update_keys()
        elif type(val) == list:
            self._res.tt = val
            cnt._update_keys()
        elif type(val) in [str, int]:
            cnt._basic._view.outputSection.clear()
            with cnt._basic._view.outputSection._out:
                print(val)
            cnt._basic._model.goback()
        else:    
            cnt._basic._view.outputSection.display(type(val), ipy=False, clear=True)
            cnt._basic._model.goback()
    def update_keys(self,):
        cnt = self._cnt
        val = cnt._basic._model.value()
        if type(val) == list:
            keys = list(map(str, range(len(val))))
            cnt._key_view.set_container(keys)
        else:
            cnt._key_view.set_container(cnt._basic._model.getKeys())
        cnt._basic._view.keysView.displayerWidg.display(cnt._key_view.get_layout(),ipy=True, clear=True)
    def goback_func(self, btn, *param):
        cnt = self._cnt
        sizeBefore = len(cnt._basic._model._loc)
        cnt._basic._model.goback()
        cnt._basic._view.locationView.locationWidg.value = "/".join(map(str,cnt._basic._model._loc))
        if len(cnt._basic._model._loc) != sizeBefore:
            cnt._update_keys()
        cnt._basic._view.outputSection.clear()
    def set_file(self, file):
        self._file_path = file
        from FileDatabase import File
        import json
        self._data = json.loads(File.getFileContent(file))
        from timeline.t2023.advance_pickle_crud import Main
        self._ly, self._cnt = Main.keyValueCrud(self._data)
        from modules.SearchSystem.modular import HideableWidget
        HideableWidget.hideIt(self._cnt._basic._view.fileView.opsCheckbox)
        self._cnt.set_key_selected_func(self.key_clicked)
        self._cnt.set_key_updator(self.update_keys)
        self._cnt.set_goback_func(self.goback_func)
class Main:
    def jsonExplorer(file):
        je = JsonExplorer()
        je.set_file(file)
        return je._cnt._basic._view.layout, je
