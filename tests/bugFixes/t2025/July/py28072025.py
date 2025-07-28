#%%
from useful.jupyterDB import jupyterDB
jupyterDB._params = globals()
from useful.CSS import Main as CSSMain
CSSMain.loadInCssComponent()
#%%
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

# %%
import os
#%%
from timeline.t2024.generic_logger.generic_logger_v6 import GenericLoggerV6
from useful.LibsDB import LibsDB
filename = os.sep.join([LibsDB.cloudPath(), 'timeline', '2024', '10_Oct', "abc.sqlite"])
gl = GenericLoggerV6(filename)
#%%
gl.views.container.outputs.layout
# %%
vg = gl.process.oldLogger.process.loggerDataView.process.rendered_forms["DomainOperations"].process.viewGenerator 
# %%
vg
# %%
vg._key_view_map["moreInfo"].state.process.keyVal.views.opsList.outputs.layout
# %%
vg._key_view_map["moreInfo"].state.process.keyVal.views
# %%
vg._key_view_map["moreInfo"].state.process.keyVal.views.metaOpsList.outputs.layout
# %%
from timeline.t2024.ui_lib.refactored_key_value_adder import Main as KVMain
kvm = KVMain.key_val_with_search_and_sort()
kvm.process.container.views.container.outputs.layout

# %%

# %%
from timeline.t2024.generic_logger.generic_loggerV4 import SqliteDictDB
from timeline.t2024.generic_logger.generic_logger_v6 import GenericLoggerV6
from useful.LibsDB import LibsDB
import os
filename = os.sep.join([LibsDB.cloudPath(), 'timeline', '2024', '10_Oct', "abc.sqlite"])
sqdb = SqliteDictDB()
sqdb.handlers.set_file(filename)
sqdb.handlers.set_table_name("logger")
data = sqdb.handlers.read(["data", "ea7cddbca91945fd9ce756b85c25bed7"])
d34 = data[34]
mi =d34["moreInfo"]
kvm.process.container.handlers.set_dictionary(mi)
kvm.process.container.handlers.render_and_update_ops_comp()
# %%
cc =kvm.process.container.views.container.outputs.layout.children[2].children[1].children[1]
# %%
cc.children[0].click()
# %%
op = kvm.process.container.views.container.outputs.layout.children[3].children[1].children[0].children[0]
# %%
op.value = "delete"