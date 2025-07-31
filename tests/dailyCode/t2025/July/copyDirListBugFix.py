#%%
import sys 
sys.path.insert(0,"../../../..")

# %%
from useful.jupyterDB import jupyterDB
jupyterDB._params = globals()
from useful.CSS import Main as CSSMain
CSSMain.loadInCssComponent()
# %%
import os
from timeline.t2024.generic_logger.generic_logger_v6 import GenericLoggerV6
from useful.LibsDB import LibsDB
filename = os.sep.join([LibsDB.cloudPath(), 'timeline', '2024', '10_Oct', "abc.sqlite"])
gl = GenericLoggerV6(filename)
gl.views.container.outputs.layout
# %%
