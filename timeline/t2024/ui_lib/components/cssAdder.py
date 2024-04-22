import anywidget
import traitlets

class AddCSSWidget(anywidget.AnyWidget):
    _esm = """export function render({ model, el }) {

    let styleSheet = document.createElement("style");
    styleSheet.innerHTML = model.get("content")
    model.on("change:content", () => {
        styleSheet.innerHTML = model.get("content")
    });
    el.appendChild(styleSheet);
    }
    """
    content = traitlets.Unicode(default_value="").tag(sync=True)
    
    helpText = """
    content = ".clasnm{abc: abcVal;..}"
    """.strip()
