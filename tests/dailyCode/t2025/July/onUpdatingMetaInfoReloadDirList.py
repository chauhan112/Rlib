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
gl.views.container.outputs.layout.children
# %%
keyVal = gl.views.container.outputs.layout.children[4].children[0].children[0].children[-3]
# %%
opsSelc = keyVal.children[1].children[0].children[2]
# %%

opsSelc.value = "metaOps"
# %%
doF = gl.process.oldLogger.process.loggerDataView.process.rendered_forms["DomainOperations"]
# %%
kv = doF.handlers.fieldUi("moreInfo")

# %%
kv
# %%
kv.__dict__
# %%
kv._widget
# %%
kv.state.process.keyVal.process.container.local_states

# %%
metaKeyValue
#%%

# %%
kvs = kv.state.process.keyVal
# %%

# %%
mkv = kvs.process.kvapwm.process.metaKeyValue.views.container.outputs.layout
# %%
btn = mkv.children[1].children[1]
# %%
btn.click()
# %%
