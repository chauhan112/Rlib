from modules.Explorer.personalizedWidgets import IRWidget, IBox, HRContrainableBox, GenerateNRowsBox
from modules.GUIs.model import KeyManager
import ipywidgets as widgets
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
        
class IButtonMaker:
    def get(self):
        pass
class ButtonMaker(IButtonMaker):
    def __init__(self):
        self._btn = None
        self._func = None
    def set_info(self, btn_info: IDisplayableResult):
        self._info = btn_info
    def get(self):
        if self._btn is None:
            from useful.WidgetsDB import WidgetsDB
            name = self._info.get_button_name()
            key = self._info.get_btn_key()
            tooltip = self._info.get_tool_tip()
            self._btn = WidgetsDB.mButton(name, key, self._func)
            self._btn.tooltip = tooltip
        return self._btn
    def set_callback(self, func):
        self._func = func
        
class INumberOfDisplayer:
    def get_layout(self):
        pass
    def set_callback_func(self, func):
        pass
    def set_elements(self, elements: list[IDisplayableResult]):
        pass
class AllDisplayer(INumberOfDisplayer):
    def __init__(self):
        self.set_ncols(6)
    def get_layout(self):
        from useful.WidgetsDB import WidgetsDB
        import ipywidgets as widgets
        output = WidgetsDB.searchEngine().resultWidget()
        output.searchRes.clear_output()
        self._result_area = output.buttonRes
        output.display()
        with output.searchRes:
            elements = []
            for res in self._results:
                info = res.get_result_info()
                callbackFunc = (lambda val: lambda param: self.callback(val))(info)
                btn = ButtonMaker()
                btn.set_callback(callbackFunc)
                btn.set_info(res)
                elements.append(btn.get())
            display(WidgetsDB.getGrid(self._ncols, elements))
        return output
    def callback(self, info):
        self._result_area.clear_output()
        with self._result_area:
            self._callback(info)
            
    def set_callback_func(self, func):
        self._callback = func
    def set_elements(self, elements:list[IDisplayableResult]):
        self._results = elements
    def set_ncols(self, ncols):
        self._ncols = ncols
class PageSelectioOpsWidget(IRWidget):
    def __init__(self):
        box_layout = widgets.Layout(display='flex',flex_flow='row', align_items='stretch') 
        self._bn = widgets.HBox([widgets.Button(description =str(i+1),layout={"width": "auto"}) for i in range(5)])
        self._pageLeft = widgets.Label("...")
        self._pageMax = widgets.Label("pMax")
        self._pageRight = widgets.Label("...")
        self._pageTxt = widgets.BoundedIntText( min=0, max=2,layout ={"width":"80px"} )
        self._gotoPage = widgets.Button(description="go", layout={"width":"auto"})
        pager = widgets.HBox([self._pageLeft, self._bn ,self._pageRight,self._pageMax, 
                                    self._pageTxt, self._gotoPage], layout=box_layout)
        self._pager = HideableWidget()
        self._pager.set_widget(pager)
        
    def get(self):
        return self._pager.get()
class IHideable:
    def hide(self):
        pass
    def show(self):
        pass
class HideableWidget(IHideable, IRWidget):
    def set_widget(self, wid):
        self._wid = wid
    def show(self):
        self._wid.layout.display = None
    def hide(self):
        self._wid.layout.display = 'none'
    def get(self):
        return self._wid
    def hideIt(wid):
        wid.layout.display = 'none'
    def showIt(wid):
        wid.layout.display = None
class DisplayNElement(IRWidget, INumberOfDisplayer):
    def __init__(self):
        self._key_mgr = None 
        self._buttons = HRContrainableBox()
        self._buttons.set_width(6)
        self._pager_wid = PageSelectioOpsWidget()
        self.set_limit(40)
        self._set_default_layout()
        self._set_pager_widget_callbacks()
        
    def _set_pager_widget_callbacks(self):
        for ch in self._pager_wid._bn.children:
            ch.on_click(self._page_clicked)
        self._pager_wid._gotoPage.on_click(lambda x: self._page_selected(self._pager_wid._pageTxt.value))
        
    def _page_clicked(self, btn: widgets.Button):
        self._page_selected(int(btn.description))
        
    def _page_selected(self, page):
        self._key_mgr.setCurrentPageIndex(page)
        btns_title = self._key_mgr.getButtonIndices()
        for i, title in enumerate(btns_title):
            ch = self._pager_wid._bn.children[i]
            ch.description = str(title)
        
        elements = self._key_mgr.getKeysForCurrentPageIndex()
        for i in range(self._limit):
            val = self._buttons.get_child(i)
            if i < len(elements):
                btn = val.get()
                btn.description = elements[i].get_button_name()
                btn._info = elements[i].get_result_info()
                btn.tooltip = elements[i].get_tool_tip()
                val.show()
            else:
                val.hide()
    def _set_default_layout(self):
        nrows = 2
        self._res_row_id = 1
        self._page_row_id = 0
        gnrb = GenerateNRowsBox(nrows)
        hc = HRContrainableBox()
        hc.set_width(1)
        hc.add_widget(self._pager_wid._pager)
        gnrb.set_row_widgets([hc, self._buttons])
        self.set_layout(gnrb)

    def set_limit(self, val):
        from useful.WidgetsDB import WidgetsDB
        self._limit = val
        self._buttons.clear()
        for i in range(self._limit):
            hs = HideableWidget()
            hs.set_widget(WidgetsDB.mButton(str(i), i, self._btn_callback))
            self._buttons.add_widget(hs)

    def _btn_callback(self, btn):
        self._callback(btn._info)
    
    def set_elements(self, elements: list[IDisplayableResult]):
        self._elements = elements
        self._key_mgr = None
        
    def get(self):
        import math
        wid = self._layout
        if self._key_mgr is None:
            self._key_mgr = KeyManager(self._elements)
            self._key_mgr.set_limit_per_page(self._limit)
            self._total_pages = math.ceil(len(self._elements) / self._limit)
            self._pager_wid._pageMax.value = str(self._total_pages)
            self._pager_wid._pageTxt.max = self._total_pages
        if len(self._key_mgr.getButtonIndices()) == 1:
            wid.get_child(self._page_row_id).get_child(0).hide()
        else:
            wid.get_child(self._page_row_id).get_child(0).show()
        self._page_selected(1) 
        return wid.get()
    
    def set_layout(self, box: IBox):
        self._layout = box
        self._layout.get()
    def set_callback_func(self, func):
        self._callback = func
    def get_layout(self):
        return self.get()
class JupyterResultDisplayer(IResultDisplayer):
    def __init__(self):
        from useful.WidgetsDB import WidgetsDB
        self._results = None
        self._area = WidgetsDB.searchEngine().resultWidget()
        self.set_displayer_way(AllDisplayer())

    def set_result(self, results: list[IDisplayableResult]):
        self._results = results

    def set_callback(self, callback):
        def m_callback(info):
            self._area.buttonRes.clear_output()
            with self._area.buttonRes:
                callback(info)
        self._callback = m_callback
        
    def display(self):
        self._area.display()
        self._way.set_elements(self._results)
        self._way.set_callback_func(self._callback)
        lay = self._way.get_layout()
        self._area.searchRes.clear_output()
        with self._area.searchRes:  
            display(lay)
        return lay
    def set_displayer_way(self, way :INumberOfDisplayer):
        self._way = way
       
    def get_result_layout(self):
        self._way.set_elements(self._results)
        self._way.set_callback_func(self._callback)
        return self._way.get_layout()
        