from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from basic import Main as ObjMaker

def BreadCrumb():
    css = """
        .bcrumb:before {
            display: inline-block;
            padding-right: .5rem;
            padding-left: .5rem;
            color: #6c757d;
            content: "/";
        }
        
        .bcrumb{
            all:revert;
            padding: 0px;
            margin: 0;
            background: unset;
            color: #0056b3;
            text-decoration-line: underline;
            border: 0;
            padding-right: .25rem;
            cursor: pointer;
            font-size: var(--jp-widgets-font-size);
            line-height: var(--jp-widgets-inline-height);
            display: inline;
            min-width: 50px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, 
                "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
            text-overflow: ellipsis;
        }
        .bcrumb:active{
            box-shadow: unset;
            color: var(--jp-ui-font-color1);
            background-color: unset;
        }
        
        .bcrumb:hover:enabled{
            box-shadow: unset;
        }
        
        .bcrumb:focus:enabled{
            outline: 0px solid var(--jp-widgets-input-focus-border-color);
        }
        .bcrumb:focus-visible {
            outline: 0px solid var(--jp-accept-color-active, var(--jp-brand-color1));
            outline-offset: unset;
        }
        
        
        """
    wcss = Utils.get_comp({},ComponentsLib.CSSAdder, className = "w-auto bcrumb", customCss= css)
    label = Utils.get_comp({"value": "location : "}, IpywidgetsComponentsEnum.Label, className = "w-auto")
    dotDotBtn = Utils.get_comp({"icon": "arrow-circle-left"}, IpywidgetsComponentsEnum.Button, className="w-auto")
    btns = [Utils.get_comp({"description":"add"},IpywidgetsComponentsEnum.Button, className = "w-auto bcrumb", index=i) for i in range(10)]
    btnWid = Utils.container(btns)
    container = Utils.container([label, dotDotBtn, btnWid, wcss])
    debug = None
    def goBack(w):
        pass
    def onClick(w):
        s.process.debug = w
    def set_location(loc):
        for i, btn in enumerate(s.process.btns):
            if i < len(loc):
                btn.show()
                btn.outputs.layout.description = loc[i]
            else:
                btn.hide()
    btnWid.handlers.handle = onClick
    dotDotBtn.handlers.handle = goBack
    s = ObjMaker.uisOrganize(locals())
    return s