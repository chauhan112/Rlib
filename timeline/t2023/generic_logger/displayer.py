from timeline.t2023.generic_logger import NewRenderer, StringEnums, SupportedTypes, IModifier
from basic import NameSpace
from timeline.t2023.generic_logger.components import SingleButtonController
import ipywidgets as widgets
from modules.SearchSystem.modular import HideableWidget
from timeline.t2023.generic_logger.tools import LogReader
import datetime
from modules.Explorer.personalizedWidgets import CustomOutput
from useful.SerializationDB import SerializationDB
from useful.LibsDB import LibsDB
from basic import NameSpace
import re
from timeline.t2023.generic_logger.components import KeyValueInput

class ViewCreator:
    def __init__(self):
        self._renderer = None
        self._layout = None
        self._key_ops = {}
        self._out = CustomOutput()
        self.set_readable_layout_maker(self._def_readable_lay)
    def set_readable_layout_maker(self, func):
        self._get_readable_lay = func
    def get_visualizer(self):
        if self._renderer is None:
            self._renderer = NewRenderer.creator()
            self._renderer.set_scope(self._bsc._scope)
            self._renderer._structure = self._bsc._model.read(self._bsc.controllers.ldcc._cur_btn.description)["structure"]
        res = []
        for key in self._renderer._structure:
            if key in self._key_ops:
                row = self._key_ops[key]
            else:
                row = self._make_row(key)
                row.controller.cnt.set_info(row.controller.infos)
                row.controller.cnt.process_info()
                row.controller.cnt.set_value(self._data[key])
                row.view.sbc.set_clicked_func(self._btn_clicked)
                self._set_editable_status(row.controller.infos, row.view.sbc.layout)
                self._key_ops[key] = row
            res.append(row.view.layout)
        res.append(self._out.get_layout())
        return widgets.VBox(res)
    def add_custom_layout(self, key: str, lyCnt):
        self._key_ops[key] = lyCnt
    def set_basic_controller(self, bsc):
        self._bsc = bsc
    def _make_row(self, key):
        typ = self._renderer._structure[key][StringEnums.TYPE]
        infos = self._renderer._structure[key][StringEnums.INFO]
        wid = self._renderer._creator_map[typ](description=key)
        abc = NameSpace()
        abc.controller = NameSpace()
        abc.controller.type = typ
        abc.controller.key = key
        abc.controller.infos = infos
        abc.controller.cnt = wid
        abc.view = NameSpace()
        abc.view.editable = wid.layout()
        abc.view.editable.disabled = True
        abc.view.editable.layout.width ="auto"
        ly, setter = self._readable_view_and_controller(key)
        abc.view.readable = ly
        abc.controller.rsetter = setter
        abc.view.sbc = SingleButtonController(icon="edit", layout={"width":"auto"}, button_style="success")
        abc.view.sbc.layout._cnt = abc
        if abc.view.readable:
            HideableWidget.hideIt(abc.view.editable)
            abc.view.layout = widgets.HBox([abc.view.sbc.layout, abc.view.editable, abc.view.readable])
        else:
            abc.view.layout = widgets.HBox([abc.view.sbc.layout, abc.view.editable])
        return abc
    def _readable_view_and_controller(self, key):
        typ = self._renderer._structure[key][StringEnums.TYPE]
        if typ in [SupportedTypes.KeyValuesPair.name, SupportedTypes.MultipleSelect.name]:
            return self._def_readable_lay(key), self._set_readable_vals
        return None, lambda *x: x
    def set_data(self, data):
        self._data = data
    def _def_readable_lay(self, key):
        forma = lambda x: f"""<font face='comic sans ms' color ='darkcyan'>{x}</font>"""
        
        content = str(self._data[key])
        if type(self._data[key]) == str:
            content = "<br>".join(self._data[key].splitlines())
        return widgets.HTML(forma(key) + ": " + content + "<br>")
    def _btn_clicked(self, btm):
        cnt = btm._cnt
        if btm.button_style != "danger":
            btm.button_style = "danger"
        else:
            btm.button_style = "success"
        if cnt.view.readable:
            if btm.button_style == "success":
                HideableWidget.hideIt(cnt.view.editable)
                HideableWidget.showIt(cnt.view.readable)
            else:
                HideableWidget.showIt(cnt.view.editable)
                HideableWidget.hideIt(cnt.view.readable)
        else:
            if btm.button_style == "success":
                cnt.view.editable.disabled = True
            else:
                cnt.view.editable.disabled = False
    def update_values(self):
        for key in self._key_ops:
            row = self._key_ops[key]
            row.controller.cnt.set_info(row.controller.infos)
            row.controller.cnt.process_info()
            row.controller.cnt.set_value(self._data[key])
            row.view.sbc.layout._key = key
            row.controller.rsetter(row, self._data[key])
    def _set_readable_vals(self, row, *pram):
        key = row.view.sbc.layout._key
        new_val = self._get_readable_lay(key)
        row.view.readable.value = new_val.value
    def _set_editable_status(self, infos, wid):
        k = "disabled"
        if k in infos:
            wid.disabled = infos[k]
class OpsView:
    def __init__(self):
        self.update = SingleButtonController(description="update", layout={"width":"auto"})
        self.close = SingleButtonController(description="close", layout={"width":"auto"})
        self.layout = widgets.HBox([self.update.layout, self.close.layout])
class EditableDisplayer(IModifier):
    def __init__(self):
        self.set_log_reader(LogReader())
        self._cur_version = None
        self.set_display_and_edit(ViewCreator())
        self._dispalyed = False
        self.set_ops_view(OpsView())
        self._funcs = []
        self.set_display_func(self._def_displayer_func)
    def set_display_func(self, func):
        self._disp_func = func
    def set_log_reader(self, lr):
        self._lr = lr
    def set_display_and_edit(self, dae):
        self._dae = dae
    def set_basic_controller(self, bsc):
        self._bsc = bsc
    def set_ops_view(self, view):
        self._ops_view = view
    def set_up(self):
        self._ui = NameSpace()
        self._ui.controllers = NameSpace()
        self._ui.controllers.parent = self._bsc
        self._ui.controllers.lr = self._lr
        self._ui.controllers.dae = self._dae
        self._ui.views = NameSpace()
        self._ui.views.ops_view = self._ops_view
        self._dae._out.display(self._ops_view.layout, ipy=True)
        self._ops_view.update.set_clicked_func(self._update)
        self._ops_view.close.set_clicked_func(self._close)
        self._lr.set_basic_controller(self._bsc)
        self._dae.set_basic_controller(self._bsc)
        self._lr.set_select_func(self._displayer_func)
        self._lr.set_up()
        self._lr._bc.views.ev.headerWid.title.value = self._bsc.controllers.ldcc._cur_btn.description
        self._logger_name = self._bsc.controllers.ldcc._cur_btn.description
        for func in self._funcs:
            func(self)
    def _displayer_func(self, wid, *param):
        self._disp_func(wid, self)
    def _def_displayer_func(self, wid, *param):
        val = self._lr._bc.views.ev.fileFoldersListWid.value
        vals = self._lr._bc._model._data[val]
        self._dae.set_data(vals)
        if not self._dispalyed:
            self._lr._bc.views.ev.outputDisplay.display(self._dae.get_visualizer(), clear=True, ipy=True)
        else:
            self._dae.update_values()
        self._dispalyed = True
    def get_layout(self):
        return self._lr.get_layout()
    def update_data(self, versionNr):
        if self._cur_version != versionNr:
            self._lr._bc._model.update_data()
            self._cur_version = versionNr
    def _update(self, btn, *param):
        self._common(lambda x: x)
    def _close(self, btn, *param):
        def close_func(vals):
            vals['status'] = "close"
            vals['more info']["completed-time"] = datetime.datetime.now()
            return vals
        self._common(close_func)
    def set_close_func(self, func):
        self._close_func = func
    def _common(self, fucn):
        vals = {}
        for ke in self._dae._key_ops:
            cont = self._dae._key_ops[ke].controller.cnt
            vals[ke] = cont.value()
        assert len(vals) != 0
        vals = fucn(vals)
        cotnent = self._bsc._model.read(self._logger_name)
        keyIndex = self._lr._bc.views.ev.fileFoldersListWid.value
        cotnent["data"][keyIndex]= vals
        self._bsc._model.add(self._logger_name, cotnent, True)
        self._bsc.controllers.ldcc._changed_tracker += 1
        self.update_data(self._bsc.controllers.ldcc._changed_tracker)
        self._bsc.controllers.ldcc._update_reader_data()
    def add_to_setup_funcs(self, func):
        self._funcs.append(func)
class SearchViewType:
    def __init__(self):
        self.tgI = widgets.TagsInput(allow_duplicates=False )
        self.options = widgets.Dropdown(layout = {"width": "auto"}, )
        self.sbc = SingleButtonController(description="ok", layout = {"width": "auto"})
        self.layout = widgets.HBox([self.options, self.tgI, self.sbc.layout])
class ExtraFunc:
    def __init__(self):
        self.set_key_word_map({})
        self.set_view(SearchViewType())
        self._sect = SerializationDB.readPickle(LibsDB.picklePath("temps.pkl"))["2023"]['filterOps']
        self._ed = None
    def set_editable_displayer(self, ed):
        self._ed = ed
    def set_view(self, view):
        self._view = view
    def set_up(self):
        ed = self._get_ed()
        ed._ui.controllers.ef._view.options.options = list(self._sect.keys())
        ed._ui.controllers.ef._view.options.observe(self._set_tags_nd_click, "value")
        self._view.sbc.set_clicked_func(self._filterIt)
    def _set_tags_nd_click(self, wid):
        ed = self._get_ed()
        ed._ui.controllers.ef._view.tgI.value = self._sect[ed._ui.controllers.ef._view.options.value]
        ed._ui.controllers.ef._view.sbc.layout.click()
    def set_controller(self, cnt):
        self._bsc = cnt
    def _filterIt(self, btn):
        from modules.rlib_notebook_tools.instructions_tool import GNotebookLayoutController
        from timeline.t2023.generic_logger import LoggerSearch
        ed = self._get_ed()
        ed._lr._bc.views.ev.headerWid.currentPath.disabled = False
        data = self._bsc._model.read(ed._logger_name)['data']
        ls = LoggerSearch()
        ls.set_container(data)
        ls.set_search_type("concatenated")
        txtx = self._filter_txt()
        vals = list(map(lambda x: (data[x]['name'], x), data))
        if txtx != "[]":
            res = ls.search(txtx)
            vals = list(map(lambda x: (data[x]['name'], x), res))
        k = ed._lr._bsc.controllers.exp.views.ev.headerWid.title
        k.value = ed._logger_name + " - " + str(len(vals))
        ed._lr._bc.views.ev.fileFoldersListWid.options = vals
    def set_key_word_map(self, dic):
        self._key_word_map = dic
    def _filter_txt(self):
        ed = self._get_ed()
        struc = self._bsc._model.read(ed._logger_name)["structure"]
        filterTxt = ""
        for key in self._view.tgI.value:
            if key in struc['status']['info']['options']:
                filterTxt += f",{{'status': '{key}'}}"
            elif key in struc['task-type']['info']['options']:
                filterTxt += f",{{'task-type': '{key}'}}"
            elif key in self._key_word_map:
                filterTxt += self._key_word_map[key]
            else:
                filterTxt += f",{key}"
        filterTxt = filterTxt.strip(",")
        return f"[{filterTxt}]"
    def _get_ed(self):
        if self._ed is None:
            self._ed = self._bsc.controllers.cdr._modifiers['8a307311e6d04bb9814a7755b86f8ea3Tasks/r']
        return self._ed
class NewDisplaySystem:
    def set_controller(self, cont):
        self._cnt = cont
    def set_up(self):
        self._cnt._ui.controllers.ef.set_key_word_map({'html': ""})
        self._cnt.set_display_func(self._disp_u)
        self._cnt._ui.controllers.ef._view.tgI.allowed_tags = ["open", "close", "office", "coding", "home", "html"]
    def _disp_u(self, bt, *param):
        lr = self._cnt._lr
        val = lr._bc.views.ev.fileFoldersListWid.value
        vals = lr._bc._model._data[val]
        if "html" in self._cnt._ui.controllers.ef._view.tgI.value:
            lr._bc.views.ev.outputDisplay.display(lr._get_html_view(vals), clear=True, ipy=False)
            self._cnt._dispalyed = False
        else:
            self._cnt._dae.set_data(vals)
            if not self._cnt._dispalyed:
                self._cnt._lr._bc.views.ev.outputDisplay.display(self._cnt._dae.get_visualizer(), clear=True, ipy=True)
            else:
                self._cnt._dae.update_values()
            self._cnt._dispalyed = True
class SubtasksInTasks:
    def __init__(self):
        from timeline.t2023.generic_logger.subtasks import Main
        self.set_field_to_change("description")
        self.set_subtasker(Main.subtasks())
    def set_field_to_change(self, name):
        self._field_name = name
    def set_subtasker(self, subCnt):
        self._sub_task_controller = subCnt
    def set_editor_displayer(self, edis):
        self._edi_disp = edis
    def set_up(self):
        self._prev_func = self._edi_disp._disp_func
        self._edi_disp.set_display_func(self._selector)
    def _selector(self, wid, *param):
        self._prev_func(wid, *param)
        row = self._edi_disp._dae._key_ops[self._field_name]
        ui_dis = self._sub_task_controller.views.stv.displayer
        ui_dis.observe(self._update_description, names=["value"])
        ui_dis.continuous_update = False
        row.controller.rsetter = self._setter
    def _update_description(self, wid):
        row = self._edi_disp._dae._key_ops[self._field_name]
        txt = self._sub_task_controller.views.stv.displayer.value
        row.controller.cnt.layout().value = re.split(r'(\*-){10,}', txt)[0].strip()
    def _setter(self, row, *vals):
        if "sub-tasks" in self._edi_disp._dae._data["more info"]:
            self._sub_task_controller._model.set_dic(self._edi_disp._dae._data["more info"]['sub-tasks'])
            self._set_sub_task_view()
            self._sub_task_controller.views.stv.displayer.value = self._get_txt_func()
        else:
            self._revert_to_text_area_view()
    def _editButtonClicked(self, btn):
        self._edi_disp._dae._btn_clicked(btn)
        self._btn_clor_view(btn)
    def _btn_clor_view(self, btn):
        if btn.button_style == "success":
            HideableWidget.hideIt(self._sub_task_controller.views.stv.opsRow)
            self._sub_task_controller.views.stv.displayer.disabled = True
        else:
            HideableWidget.showIt(self._sub_task_controller.views.stv.opsRow)
            self._sub_task_controller.views.stv.displayer.disabled = False
    def _get_txt_func(self,*param):
        txt = self._sub_task_controller.controllers.td._def_get_text()
        res = self._edi_disp._dae._data[self._field_name] +  "\n"*2 + "*-"*20 + "\n"*2 +"sub tasks\n"+ txt
        return res
    def _set_sub_task_view(self):
        row = self._edi_disp._dae._key_ops[self._field_name]
        if hasattr(row.controller, "lastViewType") and row.controller.lastViewType == "subtask":
            return 
        row.view.editable = self._sub_task_controller.views.stv.layout
        row.view.readable = None
        row.view.layout.children = [row.view.sbc.layout, widgets.Label(self._field_name, layout={"width":"80px", "justify_content":"flex-end", "margin":"0px 8px 0px 0px"}), 
                                    row.view.editable]
        row.view.sbc.set_clicked_func(self._editButtonClicked)
        self._sub_task_controller.controllers.td.set_get_txt_func(self._get_txt_func)
        row.controller.lastViewType = "subtask"
        self._btn_clor_view(row.view.sbc.layout)
    def _revert_to_text_area_view(self):
        row = self._edi_disp._dae._key_ops[self._field_name]
        if hasattr(row.controller, "lastViewType") and row.controller.lastViewType == "textarea":
            return 
        
        row.controller.rsetter = self._setter
        row.view.editable = row.controller.cnt.layout()
        row.view.readable = None
        row.view.layout.children = [row.view.sbc.layout, row.view.editable]
        row.controller.rsetter = lambda *x: x
        row.view.sbc.set_clicked_func(self._edi_disp._dae._btn_clicked)
        row.controller.lastViewType = "textarea"
class FooderView:
    def __init__(self):
        self.dropDown = widgets.Dropdown(layout={"width":"auto"})
        self.co = CustomOutput()
        self.createBtn =widgets.Button(description="create", layout = {"align_self": "flex-end", })
        self.date_placeholder = CustomOutput()
        self.layout = widgets.HBox([self.dropDown, widgets.VBox([self.date_placeholder.get_layout(), 
                                                                 self.co.get_layout(), self.createBtn])])
class FooderController:
    def __init__(self):
        self._name = "fooder"
        self._rendered = False
        self._strings = NameSpace()
        self._strings.relation = "relation"
        self._strings.foods = "foods"
        self._strings.last_added_time = "last-added-time" # time when the field was last added or updated
        self._strings.conclusion = "conclusion"
        self._strings.data = "data"
        self._strings.structure = "structure"
        self._strings.date = "date"
        self._strings.value = "value"
    def set_up(self):
        if not self._rendered:
            self._set_up_rendered_view()
        fooder = self._bsc.app._model.read(self._name)
        structure = fooder[self._strings.structure]
        self._bsc.views.fv.dropDown.options = filter(lambda x: x != self._strings.date, structure.keys())
        self._bsc.views.fv.dropDown.observe(self._on_changed, [self._strings.value])
        date = self._bsc.views.rendered._key_view_map[self._strings.date].layout()
        self._bsc.views.fv.createBtn.on_click(self._save)
        self._bsc.views.fv.date_placeholder.display(date, ipy=True)
        date.observe(lambda x: self._set_saved_values(),[self._strings.value])
        
    def _set_up_rendered_view(self):
        self._rendered = True
        ren = self._bsc.app.controllers.ldcc._rendererCreator()
        ren.set_model(self._name, self._bsc.app._model)
        ren.set_scope(self._bsc.app._scope)
        ren.render()
        self._bsc.views.rendered = ren
        
    def set_basic(self, basc):
        self._bsc = basc
    def _on_changed(self, dwi):
        bl = self._bsc.views.rendered._key_view_map[self._bsc.views.fv.dropDown.value]
        self._set_saved_values()
        self._bsc.views.fv.co.display(bl.layout(), clear=True,ipy=True)
    def _save(self, btn):
        self._add(self._bsc.views.fv.dropDown.value, 
                  self._bsc.views.rendered._key_view_map[self._bsc.views.fv.dropDown.value].value(),
                 self._bsc.views.rendered._key_view_map[self._strings.date].value())

    def _set_saved_values(self):
        rc = RelationCrud()
        rc.set_info(self._bsc.app._model.read(self._bsc.controllers.fc._name))
        date = self._bsc.views.rendered._key_view_map[self._strings.date].value()
        bl = self._bsc.views.rendered._key_view_map[self._bsc.views.fv.dropDown.value]
        if not rc.exists(date):
            if self._bsc.views.fv.dropDown.value:
                bl.set_value({self._strings.foods:[], self._strings.conclusion: "", 
                    self._strings.last_added_time: datetime.datetime.now()})
            return
        
        vals = rc.read_vals(date)
        key = self._bsc.views.fv.dropDown.value
        if key:
            if key in vals:
                bl.set_value(vals[key])
            else:
                bl.set_value({self._strings.foods:[], self._strings.conclusion: "", 
                    self._strings.last_added_time: datetime.datetime.now()})
            
    def _add(self, typoffood, val, date):
        rc = RelationCrud()
        rc.set_info(self._bsc.app._model.read(self._bsc.controllers.fc._name))
        if not rc.exists(date):
            rc.add(date)
        idd = rc.read_id(date)
        infos = rc.get_info()
        data = infos[rc._strings.data]
        if idd in data:
            vals = data[idd]
            vals[typoffood] = val
        else:
            vals = {typoffood: val}
        data[idd] = vals
        self._bsc.app._model.add(self._bsc.controllers.fc._name, infos, True)
class RelationCrud:
    def __init__(self):
        self._strings = NameSpace()
        self._strings.relation = "relation"
        self._strings.data = "data"
        self._strings.key_index = "key-index"
    def set_info(self, info):
        self._info = info
    def get_info(self):
        return self._info
    def exists(self, date):
        if self._strings.relation in self._info:
            key = (date.day, date.month, date.year)
            return key in self._info[self._strings.relation]
        return False
    def add(self, date):
        key = (date.day, date.month, date.year)
        if self.exists(date):
            return 
        if self._strings.relation not in self._info:
            self._info[self._strings.relation] = {}
        if key not in self._info[self._strings.relation]:
            self._info[self._strings.relation][key] = self._info[self._strings.key_index]
            self._info[self._strings.key_index] += 1
        
    def read_vals(self, date):
        key = (date.day, date.month, date.year)
        idd = self._info[self._strings.relation][key]
        return self._info[self._strings.data][idd]
    
    def read_id(self, date):
        key = (date.day, date.month, date.year)
        return self._info[self._strings.relation][key]