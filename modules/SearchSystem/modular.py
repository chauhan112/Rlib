class IDisplayableResult:
    def get_button_name(self):
        pass
    def get_tool_tip(self):
        pass
    def get_result_info(self):
        pass
    def get_btn_key(self):
        pass

class GDisplayableResult(IDisplayableResult):
    def __init__(self, name, tooltip, res_info, btn_key = None):
        self._name = name
        self._tooltip = tooltip
        self._res = res_info
        self._key = btn_key
        if btn_key is None:
            self._key = name
    def get_button_name(self):
        return self._name
    def get_tool_tip(self):
        return self._tooltip
    def get_result_info(self):
        return self._res
    def get_btn_key(self):
        return self._key

class IResultDisplayer:
    def set_result(self, results: list[IDisplayableResult]):
        pass
    def set_callback(self, callback):
        pass
    def display(self):
        pass
        
class JupyterResultDisplayer(IResultDisplayer):
    def __init__(self):
        self._results = None
        self._nCols = 6
        
    def set_result(self, results: list[IDisplayableResult]):
        self._results = results
    
    def set_callback(self, callback):
        self._callback = callback
    
    def display(self):
        from WidgetsDB import WidgetsDB
        import ipywidgets as widgets
        output = WidgetsDB.searchEngine().resultWidget()
        output.searchRes.clear_output()
        display(widgets.VBox([output.searchRes, output.buttonRes]))
        with output.searchRes:
            display(WidgetsDB.getGrid(self._nCols, [self.displayItem(key= x.get_btn_key(), name=x.get_button_name(), 
                callbackFunc = lambda param: self.callback(x.get_result_info(), output.buttonRes), 
                                                            tooltip=x.get_tool_tip()) for x in self._results]))
        return output
    
    def callback(self, info, resSect):
        resSect.clear_output()
        with resSect:
            self._callback(info)
            
    def displayItem(self,key, name, callbackFunc, tooltip=None):
        from WidgetsDB import WidgetsDB
        b = WidgetsDB.mButton(name, key, callbackFunc)
        b.tooltip = tooltip
        return b