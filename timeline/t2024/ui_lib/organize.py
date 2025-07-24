from timeline.t2024.ui_lib.IpyComponents import Utils
from useful.basic import Main as ObjMaker
def Container(params, **kv):
    views = ObjMaker.namespace()
    elements = []
    for name, param, typ, moreKv in params:
        if typ is not None:
            ele = Utils.get_comp(param,typ, **moreKv)
        else:
            ele = param
        elements.append(ele)
        if name != "":
            setattr(views, name, ele)
    views.container = Utils.container(elements)
    return views
def Row(params):
    """params = [(name, param, typ, moreKv)]"""
    return Container(params)
def Column(params):
    """params = [(name, param, typ, moreKv)]"""
    return Container(params, className= "flex flex-column")