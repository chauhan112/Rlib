from basic import Main as ObjMaker

def SameRenderer():
    from timeline.t2024.ui_lib.IpyComponents import IpywidgetsComponentsEnum, Utils, ComponentsLib
    container = Utils.get_comp({"description": "as"}, IpywidgetsComponentsEnum.Button)
    parent = None
    previous_update_log_action = None
    handlers_connected = False
    def set_up():
        if not s.process.handlers_connected:
            form = s.process.parent.process.loggerDataView.handlers.get_form()
            dpdn = form.handlers.fieldUi("status")
            ly = dpdn.layout()
            ly.observe(s.handlers.status_updated, ["value"])
            s.process.handlers_connected = True
        s.process.previous_update_log_action = s.process.parent.process.loggerDataView.handlers.update_logger_data
        s.process.parent.process.loggerDataView.handlers.update_logger_data = s.handlers.update_data
        s.process.parent.process.res_undoers.append(set_up_undo)
    def update_data(w):
        s.handlers._add_time("modified-time")
        s.process.previous_update_log_action(w)
    def set_up_undo(w):
        s.process.parent.process.loggerDataView.handlers.update_logger_data = s.process.previous_update_log_action
    def status_updated(w):
        val = w["new"]
        if val == "open":
            s.handlers.unset_completed_time()
        elif val == "close":
            s.handlers.set_completed_time()
    def _add_time(key):
        import datetime
        form = s.process.parent.process.loggerDataView.handlers.get_form()
        mrif = form.handlers.fieldUi("more info")
        prev_loc = mrif._controller._basic._model._loc
        mrif._controller._basic._model._loc = []
        mrif._controller._basic._model.add(key, val=datetime.datetime.now())
        mrif._controller._basic._model._loc = prev_loc
        mrif._controller._update_keys()
    def set_completed_time():
        s.handlers._add_time("completed-time")
    def _remove_time(key):
        form = s.process.parent.process.loggerDataView.handlers.get_form()
        mrif = form.handlers.fieldUi("more info")
        prev_loc = mrif._controller._basic._model._loc
        mrif._controller._basic._model._loc = []
        if mrif._controller._basic._model.alreadyExists(key):
            mrif._controller._basic._model.delete(key)
        mrif._controller._basic._model._loc = prev_loc
        mrif._controller._update_keys()
    def unset_completed_time():
        s.handlers._remove_time("completed-time")
    def set_parent(parent):
        s.process.parent = parent
        s.handlers.set_up()
    def get_layout():
        return s.process.parent.process.loggerDataView.process.container.process.searchComponent.views.container.outputs.layout
        return s.process.parent.process.loggerDataView.process.container.views.searchWithResults.outputs.layout
    s = ObjMaker.variablesAndFunction(locals())
    return s.handlers

def OSDisplayer():
    from timeline.t2024.osExplorer import OSExplorer
    from useful.ModuleDB import ModuleDB
    from IPython.display import display
    def DataLoggerModel():
        path = "/"
        sizeCount = 100
        pageNr = 1
        data = []
        def read(key):
            return s.process.data[key]
        def goBack():
            pass
        def cd(x):
            pass
        def dirList():
            return [], list(map(lambda x: s.handlers.option_comp(x), s.handlers.get_data_for_current_page()))
        def set_data(values):
            s.process.data = values
            s.process.dataList = list(values.keys())
            s.process.pageNr = 1
        def option_comp(key):
            keyId = key
            if type(key) == tuple:
                index, keyId = key
            val = s.handlers.read(keyId)
            return (val["title"], keyId)
        def get_data_for_current_page():
            res = []
            fromStart = s.process.sizeCount * (s.process.pageNr-1)
            till = s.process.sizeCount * (s.process.pageNr)
            for i in range(fromStart, till):
                if i >= len(s.process.dataList):
                    break
                res.append((i, s.process.dataList[i]))
            return res
        def filterByTitle(filterWord):
            dirs, files = s.handlers.dirList()
            return list(filter(lambda x: filterWord in x[0], files))

        s = ObjMaker.variablesAndFunction(locals())
        s.handlers.path = path
        s.handlers.instance = s
        return s.handlers
    def SyntaxViewer():
        explorer = OSExplorer()
        explorer.views.buttons.pop()
        model = DataLoggerModel()
        explorer.process.model = model
        def set_parent(parent):
            s.process.parent = parent
            cnt = parent
            s.process.model.set_data(cnt.process.logger_data.handlers.readAll(cnt.process.current_button.description))
        def fileSelected(key):
            s.process.explorer.views.outputDisplayer.outputs.layout.clear_output()
            with s.process.explorer.views.outputDisplayer.outputs.layout:
                val = s.process.model.read(key)
                print(val["type"] + ":", val["title"])
                print(list(map(lambda x: val[x], filter(lambda x: x not in ["type", "title", "content" ], val))))
                print("-"*20)
                
                if val["type"] in ["python", "cpp", "javascript"]:
                    display(ModuleDB.colorPrint(val["type"], val["content"]))
                else:
                    print(val["content"])
        def set_page_nr(pagrNr):
            s.process.model.instance.process.pageNr = pagrNr
            s.process.explorer.handlers.render()
        def get_layout():
            s.process.explorer.handlers.render()
            cnt = s.process.parent
            cnt.process.loggerDataView.process.container.process.searchComponent.views.container.hide()
            cnt.process.res_undoers.append(cnt.process.loggerDataView.handlers.showSearchComponent)
            cnt.process.loggerDataView.process.undoers.append(cnt.process.loggerDataView.handlers.showSearchComponent)
            cnt.process.res_undoers.append(cnt.process.loggerDataView.handlers.clear_key)
            return s.process.explorer.views.container.outputs.layout
        def filterOut(x):
            out =[]
            word = s.process.explorer.views.filterSearch.outputs.layout.value
            if word.strip() == "":
                out = s.process.model.filterByTitle(word)
            else:
                cnt = s.process.parent
                try:
                    cnt.process.loggerDataView.process.searcher.set_container(s.process.model.instance.process.data)
                    out2 = cnt.process.loggerDataView.process.searcher.search_in_fields(word, False, False)
                    out = list(map(lambda x: s.process.model.option_comp(x), out2))
                except Exception as e:
                    out = s.process.model.filterByTitle(word)
            s.process.explorer.views.lister.outputs.layout.options = out
        s = ObjMaker.variablesAndFunction(locals())
        explorer.handlers.fileSelected = fileSelected
        explorer.views.filterSearch.handlers.handle = filterOut
        s.handlers.instance = s
        return s.handlers
    return SyntaxViewer() 
