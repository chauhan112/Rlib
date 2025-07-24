from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from useful.basic import Main as ObjMaker
from timeline.t2024.generic_logger.generic_loggerV3 import TabComponent
from modules.SearchSystem.modular import HideableWidget
from timeline.t2023.newInstructionTable import NewInstructionTable
import os
from LibsDB import LibsDB

def Tabbar():
    btns = Utils.container([], className="flex flex-wrap")
    container = btns
    
    def addAndGetNewTab(title, onClickFunc=None):
        tc = TabComponent()
        tc.process = ObjMaker.namespace()
        tc.views.closeBtn.state.parent = tc
        tc.views.tabTitle.state.parent = tc
        tc.views.tabTitle.outputs.layout.description = title
        tc.views.tabTitle.outputs.layout.add_class("w-auto")
        tc.views.tabTitle.outputs.layout.add_class("w-min-100px")
        if onClickFunc is None:
            tc.views.tabTitle.handlers.handle = s.handlers._clicked_on_tab
        else:
            tc.views.tabTitle.handlers.handle = onClickFunc
        tc.views.closeBtn.handlers.handle = s.handlers.removeTab
        s.views.container.append(tc.views.tabElement)
        return tc
    def removeTab(w):
        w._parent.state.parent.views.tabElement.state.removeIt = True
        s.handlers.refresh()
    def refresh():
        s.views.btns.outputs.renderedStates = list(filter(lambda x: not hasattr(x.state, "removeIt"), s.views.btns.outputs.renderedStates))
        s.views.btns.outputs.layout.children = [ele.outputs.layout for ele in s.views.btns.outputs.renderedStates]
    def onTabClick(w):
        pass
    def _clicked_on_tab(w):
        s.handlers.onTabClick(w)
    s = ObjMaker.uisOrganize(locals())
    return s
def RlibItWithTabs():
    tabbar = Tabbar()
    addTabButtton = Utils.get_comp(dict(icon="plus"), IpywidgetsComponentsEnum.Button, className="w-auto")
    addedMap =  set()
    container = Utils.container([Utils.container([addTabButtton, tabbar.views.container])], 
        className = "flex flex-column")
    prev_func = ObjMaker.namespace()
    def onAddTabClicked(w):
        if s.process.it._current_btn is None:
            return
        desc = s.process.it._current_btn.description
        if desc in s.process.addedMap:
            return
        s.process.addedMap.add(desc)
        s.process.tabbar.handlers.addAndGetNewTab(desc, s.handlers.onBtnClick)
    def newRemoveTab(w):
        s.process.prev_func.removeTab(w)
        tc = w._parent.state.parent
        desc = tc.views.tabTitle.outputs.layout.description
        s.process.addedMap.remove(desc)
    def onBtnClick(w):
        s.process.tabbar.views.btns.state.selected = w
        s.process.it._run_content(w)
        HideableWidget.showIt(s.process.it._searchView.layout)
    def set_up(it, filePath = None):
        if filePath is None:
            filePath = os.sep.join([LibsDB.cloudPath(), "timeline","2023","10. oct","opsGroup.pkl"])
        s.process.filePath = filePath
        s.process.it = it
        s.process.prev_func.removeTab = s.process.tabbar.handlers.removeTab
        s.process.tabbar.handlers.removeTab = s.handlers.newRemoveTab
        s.views.container.append(Utils.get_comp({}, ComponentsLib.IpyWrapper, value = it.get_group_view(filePath)))
        v = ["gen-log-v6","copyReloadSearch", "header", "start up"]
        for i in v:
            s.process.addedMap.add(i)
            s.process.tabbar.handlers.addAndGetNewTab(i, s.handlers.onBtnClick)
    addTabButtton.handlers.handle = onAddTabClicked
    s = ObjMaker.uisOrganize(locals())
    return s
class Main:
    def newRlibIt(scope= {}, filePath = None):
        it = NewInstructionTable()
        it.set_scope(scope)
        trlib = RlibItWithTabs()
        trlib.handlers.set_up(it, filePath)
        
        return trlib