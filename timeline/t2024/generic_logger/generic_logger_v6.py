from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from basic import Main as ObjMaker


from datetime import datetime
from useful.TimeDB import TimeDB
def TimeToolsForLog():
    def getTodayKey():
        return s.handlers.nDayBeforeStamp(0)
    def nowStamp():
        t = datetime.now()
        return datetime.timestamp(t)
    def nDayBeforeStamp(n):
        return datetime.timestamp(datetime(*TimeDB.nDaysBefore(n)))
    s = ObjMaker.variablesAndFunction(locals())
    return s
    
def generic_logger_model():
    parent = None
    def read(loc):
        return s.process.parent.process.logger.process.model.read(loc)
    def readAll():
        return s.process.parent.process.logger.process.model.readAll()
    def write(loc, val, overwrite=False):
        return s.process.parent.process.logger.process.model.write(loc, val, overwrite)
    def exists(loc):
        return s.process.parent.process.logger.process.model.exists(loc)
    def delete(loc):
        s.process.parent.process.logger.process.model.delete(loc)
    def keys(loc):
        if len(loc) == 0:
            return s.handlers.readAll().keys()
        return s.handlers.read(loc).keys()
    s = ObjMaker.variablesAndFunction(locals())
    return s

def GenericLoggerV6(filename):
    from timeline.t2024.generic_logger.generic_logger_v5 import gl_ke
    cnt = gl_ke(filename)
    return GenericLoggerWithCnt(cnt)

def GenericLoggerWithCnt(oldLogger):
    from timeline.t2024.generic_logger.metaCrud import UpdateMenuBar
    cnt = oldLogger
    umb = UpdateMenuBar()
    umb.process.parent = cnt.process.updateForm
    umb.handlers.setup()
    cnt.process.loggerDataView.process.container.views.customToggler = Utils.get_comp({"options": ["default",'custom']},
                        IpywidgetsComponentsEnum.ToggleButtons, className = "w-auto")
    cnt.process.container.views.customToggler = Utils.get_comp({"options": ["default",'custom']},
                                    IpywidgetsComponentsEnum.ToggleButtons, className = "w-auto")
    resultOut = cnt.process.container.views.container.pop()
    cnt.process.container.views.container.append(cnt.process.container.views.customToggler)
    cnt.process.container.views.container.append(resultOut)
    resultOutForData = cnt.process.loggerDataView.process.container.views.container.pop()
    cnt.process.container.views.container.append(cnt.process.loggerDataView.process.container.views.customToggler)
    cnt.process.container.views.container.append(resultOutForData)

    cnt.process.container.views.customToggler.hide()
    cnt.process.loggerDataView.process.container.views.customToggler.hide()
    container = cnt.process.container.views.container
    model = generic_logger_model()
    model.process.parent = cnt
    customRenderedStates = {}
    ttl = TimeToolsForLog()
    prevOnSearch = None
    def exists(ops, typ = "logger"):
        """
        typ : logger|data
        """
        K = s.process.cnt.process.logger.process.K
        model = s.process.cnt.process.logger.process.model
        p = s.process.cnt
        tbId = model.read([K.tables, K.table2Id, p.process.current_button.description])
        mapp = {
            "r": "read",
            "c": "create",
            "u": "update",
            "d": "delete"        
        }
        return model.exists([K.meta, tbId, "dicData", mapp[ops] + "-" + typ])
    def read(ops, typ = "logger"):
        """
        typ : logger|data
        """
        K = s.process.cnt.process.logger.process.K
        model = s.process.cnt.process.logger.process.model
        p = s.process.cnt
        tbId = model.read([K.tables, K.table2Id, p.process.current_button.description])
        mapp = {
            "r": "read",
            "c": "create",
            "u": "update",
            "d": "delete"        
        }
        return model.read([K.meta, tbId, "dicData", mapp[ops] + "-" + typ])
    def allLoggerData():
        pass
    def filteredLoggerData():
        pass
    def onResultBtnClickLogger(w):
        p = s.process.cnt
        p.handlers.result_button_clicked_undo(w)
        p.process.loggerDataView.handlers.result_button_clicked_undo(w)
        p.process.current_button = w
        p.process.current_button.add_class("selected")
        p.process.res_undoers.append(s.handlers.remove_btn_css)
        crd = p.handlers.current_ops_value()
        p.process.history.append("result btn clicked for logger for operations", crd, 
            p.process.current_button.description)
        if s.handlers.exists(crd, "logger"):
            pass
        elif crd == "u":
            p.handlers.update_state(w)
        elif crd == "d":
            p.handlers.delete_inbetween(w)
        elif crd == "r":
            p.handlers.read_logger(w)
    def onResultBtnClickedLoggerData(w):
        p = s.process.cnt.process.loggerDataView
        p.handlers.result_button_clicked_undo(w)
        p.process.current_button = w
        p.process.current_button.add_class("selected")
        p.process.res_undoers.append(p.handlers.remove_btn_css)
        crd = p.handlers.current_ops_value()
        p.process.parent.process.history.append("results btn clicked in logger data for ops", crd, 
            p.process.current_button.description)
        p.process.container.views.customToggler.hide()
        if s.handlers.exists(crd, "data"):
            p.process.container.views.customToggler.show()
            p.process.parent.process.res_undoers.append(lambda x: p.process.container.views.customToggler.hide())
            p.process.parent.process.undoers.append(lambda x: p.process.container.views.customToggler.hide())
            p.process.undoers.append(lambda x: p.process.container.views.customToggler.hide())
            s.handlers.onToggleData(1)
        else:
            s.handlers.renderingData(crd,p,w)
    def onToggleData(w):
        p = s.process.cnt.process.loggerDataView
        crd = p.handlers.current_ops_value()
        if p.process.container.views.customToggler.outputs.layout.value == "default":
            s.handlers.renderingData(crd,p,w)
        else:
            customRendering = s.handlers.get_rendered_state(crd, "data")
            current_logger = p.process.parent.process.current_button.description
            vals = p.process.searcher._data[p.handlers.get_log_data_index()]
            customRendering.handlers.set_data(vals, s)
            p.process.container.views.resultsOut.state.controller.clear()
            with p.process.container.views.resultsOut.state.controller._out:
                display(customRendering.views.container.outputs.layout)
    def renderingData(crd,p,w):
        if crd == "u":
            p.handlers.update_state(w)
        elif crd == "d":
            p.handlers.delete_inbetween(w)
        elif crd == "r":
            p.handlers.read_logger_data(w)
    def get_rendered_state(ops, typ):
        p = s.process.cnt
        content = s.handlers.read(ops, typ)
        k = (p.process.current_button.description, ops, typ)
        if k in s.process.customRenderedStates:
            return s.process.customRenderedStates[k]
        xx = {}
        exec(content, xx)
        f = xx["f"]
        s.process.customRenderedStates[k] = f()
        return s.process.customRenderedStates[k]
    def onSearchOfData(w):
        ttl = s.process.ttl
        currentLogger = s.process.cnt.process.current_button.description
        loggerId = s.process.model.handlers.read(["tables", 'table-name-to-uuid', currentLogger])
        if not s.process.model.handlers.exists(["meta", loggerId, "used"]):
            s.process.model.handlers.write(["meta", loggerId, "used"], {})
        k = ttl.handlers.getTodayKey()
        if not s.process.model.handlers.exists(["meta", loggerId, "used", k]):
            s.process.model.handlers.write(["meta", loggerId, "used", k], [])
        openedRes = s.process.model.handlers.read(["meta", loggerId, "used", k]).copy()
        openedRes.append(ttl.handlers.nowStamp())
        s.process.model.handlers.write(["meta", loggerId, "used", k], openedRes, True)
        s.handlers.prevOnSearch(w)
    cnt.process.loggerDataView.process.resultDisplayer.views.btns.handlers.handle = onResultBtnClickedLoggerData
    cnt.process.loggerDataView.process.container.views.customToggler.handlers.handle = onToggleData
    prevOnSearch = cnt.process.loggerDataView.process.container.process.searchComponent.views.searchBtn.handlers.handle
    cnt.process.loggerDataView.process.container.process.searchComponent.views.searchBtn.handlers.handle = onSearchOfData
    s = ObjMaker.uisOrganize(locals())
    cnt.process.timeline = ObjMaker.namespace()
    cnt.process.timeline.t2024 = ObjMaker.namespace()
    cnt.process.timeline.t2024.v6 = s
    return s