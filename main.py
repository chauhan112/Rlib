#%%
from useful.jupyterDB import jupyterDB
jupyterDB._params = globals()
from timeline.t2025.Jan.newrlib import NewRlibItTools
from basic import Main as ObjMaker

rlib = ObjMaker.namespace()
rlib.kvstools = NewRlibItTools()
rlib.kvstools.handlers.set_up()
rlib.kvs = rlib.kvstools.process.kvs
rlib.itLayout = rlib.kvs.views.container.outputs.layout

#%%
rlib.itLayout
# %%
from useful.CSS import Main as CSSMain
CSSMain.loadInCssComponent()
# %%
