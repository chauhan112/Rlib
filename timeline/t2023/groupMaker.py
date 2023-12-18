from Path import Path
from SerializationDB import SerializationDB
from timeline.t2023.treeOps import Main

class OpsGroupMaker:
    def __init__(self):
        filepath = Path.filesWithExtension("pkl", "_rajaDB")[0]
        self.set_instructions_keys(list(SerializationDB.readPickle(filepath)["instructions"].keys()))
        self._gr = {}
    def set_instructions_keys(self, keys):
        self._arr = keys
        self._used = set()
        self._ref = {}
    def enumAndShowAllOps(self, cnt):
        txt = ""
        self._ref.clear()
        i = 0
        for val in self._arr:
            if val not in self._used:
                txt += f"{i+1}. {val}\n"
                self._ref[i+1] = val
                i += 1
        cnt._bsc._view.txtArea.value = txt
    def addOps(self, cnt):
        inp = cnt.get_user_input()
        name = self._ref[int(inp.strip())]
        content = cnt._bsc._model._pcrud.value()
        if name not in content:
            cnt._bsc._model._pcrud.add(name, {})
            self._used.add(name)
        OpsGroupMaker.enumAndShowAllOps(cnt)
    def addMultiple(self, cnt):
        inp = cnt.get_user_input()
        vals = list(map(int, inp.strip().split("-")))
        content = cnt._bsc._model._pcrud.value()
        for i in range(vals[0], vals[1]+1):
            name = ref[i]
            if name not in content:
                cnt._bsc._model._pcrud.add(name, {})
                self._used.add(name)
        OpsGroupMaker.enumAndShowAllOps(cnt)
    def set_up(self):
        self._bsc.add_ops("addOps", OpsGroupMaker.addOps, "add an ops")
        self._bsc.add_ops("mo", OpsGroupMaker.addMultiple, "add range of ops")
        self._bsc.add_ops("lsOps", OpsGroupMaker.enumAndShowAllOps, "make the group for the ops")
    def get_maker(self):
        self._bsc = Main.runWithDic(self._gr)
        return self._bsc._view.layout
        
        
from timeline.t2023.advance_pickle_crud import Main as DicExplorer
from basic import NameSpace
import ipywidgets as widgets
from modules.SearchSystem.modular import HideableWidget

class GrouperController:
    def set_up(self):
        self._view = NameSpace()
        self._view.layout, self._cnt = DicExplorer.keyValueCrud(self._group)
        self._cnt._key_view._memoization.clear()
        HideableWidget.hideIt(self._cnt._basic._view.fileView.opsCheckbox)
        self._view.layout.layout.border = None
        self._view.layout.layout.min_height = None
        self._cnt.set_key_updator(self._update_keys)
        self._cnt._key_view.set_element_maker(self._make_btn)
        self._cnt.set_key_selected_func(self._key_selected)
        self.set_leaf_click_func(lambda x: x)
        self.set_not_leaf_fun(lambda x: x)
        self.set_additional_sorter(lambda x: x)
    def _key_selected(self, btn):
        self._cnt._current_key = None
        self._cnt._basic._view.outputSection.clear()
        vals = self._cnt._basic._model.value()
        key = btn.description
        cur_val = vals[key]
        if type(cur_val) == dict and len(cur_val) != 0:
            self._cnt._basic._model.goForward(btn.description)
            self._update_keys()
            self._not_leaf_func(btn)
        else:
            self._leaf_clicked(btn)
    def _make_btn(self, btnDes, clickFunc=None):
        vals = self._cnt._basic._model.value()
        cur_val = vals[btnDes]
        if type(cur_val) == dict and len(cur_val) != 0:
            btn = widgets.Button(description= btnDes, layout= {"width":"auto"}, icon ="folder")
        else:
            btn = widgets.Button(description= btnDes, layout= {"width":"auto",})
        if clickFunc is not None:
            btn.on_click(clickFunc)
        return btn
    def _update_keys(self):
        vals = self._cnt._basic._model.value()
        keys = self._sorter_func(vals)
        keys = sorted(keys, key= lambda x: type(vals[x]) == dict and len(vals[x]) != 0, reverse=True)
        self._cnt._key_view.set_container(keys)
        self._cnt._basic._view.keysView.displayerWidg.display(self._cnt._key_view.get_layout(),ipy=True, clear=True)
    def set_leaf_click_func(self, fucn):
        self._leaf_clicked = fucn
    def set_not_leaf_fun(self, func):
        self._not_leaf_func = func
    def set_group_dic(self, gr):
        self._group = gr
    def set_additional_sorter(self, sorter):
        self._sorter_func = sorter