from useful.basic import Main as ObjMaker
from timeline.t2024.experiments.keyValueWithSearchAndFilter import SearchFnc
def LoggerSearchWithSort():
    searcher = SearchFnc()
    def values(x):
        return str(s.process.tempData[x])
    def fieldGetter(x):
        vals = s.process.tempData[x]
        if s.process.field not in vals:
            return ""
        return str(vals[s.process.field])
    def apply(content):
        abc = content.copy()
        if abc["field"] == "--":
            s.process.searcher.handlers.key_getter = s.handlers.values
        else:
            s.process.field = abc["field"]
            s.process.searcher.handlers.key_getter = s.handlers.fieldGetter
            del abc["field"]
        s.process.searcher.handlers.set_values(s.process.tempData)
        typ = abc["type"]
        if typ == "search":
            return s.process.searcher.handlers.search(abc["value"])
        elif typ == "sort":
            return s.process.searcher.handlers.sort(s.process.tempData, abc["value"])
        elif typ == "group":
            return s.process.searcher.handlers.grouper(abc["value"])
        return []

    def search(contentStr, case=False, refg=False):
        """
            infos: dict {field: "",
                         type: sort|search|group|combined,
                         value:  {type: none|reg|case|word, value: str|list[str] } -> search
                                 {reverse: True} -> for sorting
                                 {values: list[str]} -> for group
                                 list[allAbove] -> for combined
                       }
        """

        infos = eval(contentStr)

        if type(infos) == list:
            for ele in infos:
                res = s.handlers.apply(ele)
                s.process.tempData = {k: s.process.tempData[k] for k in res}
            return res
        return s.handlers.apply(infos)
    def set_data(data):
        s.process.data = data
        s.process.tempData = data
    s = ObjMaker.variablesAndFunction(locals())
    return s

def NewSearchSystem():
    from timeline.t2024.listCrudWithFilter import SearchComplex
    advanceSearcher = LoggerSearchWithSort()
    locSearcher = SearchComplex()
    prev_func = ObjMaker.namespace()
    def set_up():
        searchComp = s.process.parent.process.loggerDataView.process.container.process.searchComponent
        searchBtn = searchComp.views.searchBtn
        options = searchComp.views.searchType.outputs.layout.options
        searchComp.views.searchType.outputs.layout.options = list(options) +["loc"]
        s.process.prev_func.search_clicked = searchBtn.handlers.handle
        searchBtn.handlers.handle = s.handlers.search_clicked
    def search_clicked(w):
        searchComp = s.process.parent.process.loggerDataView.process.container.process.searchComponent
        typ = searchComp.views.searchType.outputs.layout.value
        if typ == "fields":
            res = s.handlers.advance_search()
            s.process.parent.process.loggerDataView.handlers.set_up_searcher()
            s.process.parent.process.loggerDataView.handlers.display_search_results(res)
        elif typ == "loc":
            data = s.handlers.read_data()
            s.process.locSearcher.process.values = data
            searchCriteria = eval(searchComp.views.inputText.outputs.layout.value)
            res = s.process.locSearcher.handlers.locSearch(searchCriteria, False)
            s.process.parent.process.loggerDataView.handlers.set_up_searcher()
            s.process.parent.process.loggerDataView.handlers.display_search_results(res)
        else:
            s.process.prev_func.search_clicked(w)
    def read_data():
        current_logger = s.process.parent.process.current_button.description
        data = s.process.parent.process.logger_data.handlers.readAll(current_logger)
        return data
    def advance_search():
        data = s.handlers.read_data()
        s.process.advanceSearcher.handlers.set_data(data)
        searchComp = s.process.parent.process.loggerDataView.process.container.process.searchComponent
        word = searchComp.views.inputText.outputs.layout.value
        return s.process.advanceSearcher.handlers.search(word)
    s = ObjMaker.variablesAndFunction(locals())
    return s
