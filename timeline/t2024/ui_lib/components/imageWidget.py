import anywidget
import traitlets

class ImageWidget(anywidget.AnyWidget):
    _esm = """export function render({ model, el }) {
    
    let container = document.createElement("div");
    let imgTag = document.createElement("img");
    let updateImage = () => {
        let imgPropeties = model.get("imageProperties")
        for (let prop in imgPropeties) {
            imgTag[prop] = imgPropeties[prop];
        }
    }
    
    updateImage()

    let updateCss = () => {
        let cssStyles = model.get("cssDict")
        if (cssStyles.hasOwnProperty("container")) {
            container.style.cssText = cssStyles.container
        }
        if (cssStyles.hasOwnProperty("img")) {
            imgTag.style.cssText = cssStyles.container
        }
    };

    container.appendChild (imgTag)
    updateCss()
    
    model.on("change:imagePropertiesTrigger", () => {
        updateImage()
    });
    model.on("change:cssDictTriggerChange", () => {
        updateCss()
    });
    el.appendChild(container);
    }

    """
    imageProperties = traitlets.Dict(default_value={}).tag(sync=True)
    imagePropertiesTrigger = traitlets.Int(0).tag(sync = True)
    cssDict = traitlets.Dict(default_value={}).tag(sync = True)
    cssDictTriggerChange = traitlets.Int(0).tag(sync = True)
    styleSheet = traitlets.Unicode(default_value="").tag(sync=True)
    
    helpText = """
    imageProperties = {"src": "", "alt": "", "width":"", "height":""}
    cssDict = {"container": "color:red;...", "img": ""}
    structure = "<div><img/></div>"
    """.strip()

class Main:
    def imageWithCss(imgPath="https://getbootstrap.com/docs/5.3/assets/brand/bootstrap-logo-shadow.png", clsName="img-101", cssText= "" ):
        from timeline.t2024.ui_lib.components.cssAdder import AddCSSWidget
        import ipywidgets as widgets
        iw = ImageWidget()
        iw.add_class(clsName)
        iw.imageProperties = {
            "src": imgPath
        }
        acw = AddCSSWidget()
        acw.content = cssText
        if cssText == "":
            acw.content = """
            .img-101 img{
                width: 100px;
                transition: all .3s;
            }
            .img-101 img:hover{
                width: 105px;
                background-color: red;
            }
            """
        return widgets.HBox([acw, iw])
