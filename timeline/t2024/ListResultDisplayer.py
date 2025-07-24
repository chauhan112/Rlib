from basic import Main as ObjMaker
from timeline.t2024.generic_logger.generic_loggerV3 import Pagination
import math
from modules.Explorer.model import ExplorerUtils
from useful.ComparerDB import ComparerDB
from timeline.t2024.osExplorer import Main as OSMain
from timeline.t2024.Array import Array

def ListResultDisplayer():
    page = Pagination()
    exp = OSMain.osExplorer()
    title = "Explorer"
    showGoBackOption = True
    paginationSize = 200
    container = exp.views.container
    page.views.container.hide()
    def set_options(dirs, files):
        ddirs =dirs
        if s.process.showGoBackOption:
            ddirs = [".", ".."] + dirs
        allOps = ExplorerUtils.dirsWithIcon(ddirs) + files
        s.handlers.set_all_options(allOps)
    def set_all_options(options):
        s.process.current_list = list(map(s.handlers.labelFunc, enumerate(options)))
        tot = math.ceil(len(options)/s.process.paginationSize)
        s.process.page.handlers.update_total_pages(tot)
        if tot <= 1:
            s.process.page.views.container.hide()
        else:
            s.process.page.views.container.show()
        s.handlers.onPageClicked('1')
        s.process.exp.views.title.outputs.layout.value = s.process.title + " - " +str(len(s.process.current_list))
    def labelFunc(x):
        return x[1], x[1]
    def onPageClicked(pageNr):
        s.process.prev_selectWithVal(pageNr)
        x,y = s.handlers.pageRange(int(pageNr)-1)
        prev_onChange = s.process.exp.views.lister.handlers.handle
        s.process.exp.views.lister.handlers.handle = lambda x: x
        s.process.exp.views.lister.outputs.layout.options = s.process.current_list[x:y]
        s.process.exp.views.lister.handlers.handle = prev_onChange
        
    def set_up():
        exp = s.process.exp
        exp.views.outputDisplayer.outputs.layout.remove_class("h-600px")
        exp.views.outputDisplayer.outputs.layout.add_class("h-max-600px")
        exp.views.buttons.outputs.layout.add_class("flex-wrap")
        l = exp.views.mainSection.pop()
        ll = exp.views.mainSection.pop()
        exp.views.mainSection.append(s.process.page.views.container)
        exp.views.mainSection.append(ll)
        exp.views.mainSection.append(l)
        s.process.prev_selectWithVal = s.process.page.handlers.selectWithVal
        s.process.page.handlers.selectWithVal = s.handlers.onPageClicked
        s.process.exp.handlers.render()
    def set_show_goback_options(value):
        s.process.showGoBackOption = value
        s.process.exp.handlers.render()
    def pageRange(pageNr):
        pageSize = s.process.paginationSize
        return pageNr* pageSize, pageSize * (pageNr + 1)
    def onFiltered(w):
        dirs, files = s.process.exp.process.model.dirList()
        filteringValue = s.process.exp.views.filterSearch.outputs.layout.value
        if filteringValue != "":
            s.handlers.set_options([], list(filter(lambda x: ComparerDB.inCompare(filteringValue, x), ExplorerUtils.dirsWithIcon(dirs[2:]) + files)))
        else:
            s.handlers.set_options (dirs[2:], files) 
    def set_pagination_size(nr):
        s.process.paginationSize = nr
        s.process.exp.handlers.render()
    exp.views.filterSearch.handlers.handle = onFiltered
    s = ObjMaker.uisOrganize(locals())
    return s
