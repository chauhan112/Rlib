
# searching in the code. for example: if i want to search in the rlib some function, i could use this function
def codeSearch():
    key = "codeSearch"
    from modules.rlib_notebook_tools.instructions_tool import GElement, GNotebookLayoutController
    from jupyterDB import jupyterDB
    from IPython.display import display
    if key in GNotebookLayoutController.instances:
        display(GNotebookLayoutController.instances[key])
        return
    from modules.Explorer.personalizedWidgets import Main as GUIMaker
    from Database import Database
    GNotebookLayoutController.instances[key] = GUIMaker.gui_for_db(Database.moduleDB())
    display(GNotebookLayoutController.instances[key])

# used for copying the application names: For example: this contains all the names of apps i created in the TLCAp and i want to search them, here i can find them all and onclicking
# it copies the name of the application
def apps():
    from IPython.display import display
    from LibPath import getPath
    from modules.rlib_notebook_tools.instructions_tool import GElement, GNotebookLayoutController
    from jupyterDB import  jupyterDB
    import os
    names = jupyterDB.pickle().read("temps")['2023']['app names']
    dic = {v: v for v in names}
    eles = []
    for na in dic:
        ele=GElement(na, jupyterDB.clip().copy)
        ele.setData(dic[na])
        eles.append(ele)
    display(GNotebookLayoutController().get(eles))
