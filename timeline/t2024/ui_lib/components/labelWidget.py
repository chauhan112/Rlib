import anywidget
import traitlets

class TextWidget(anywidget.AnyWidget):
    _esm = """export function render({ model, el }) {
    const textNode = document.createTextNode(model.get("name"));
    let container = document.createElement("div");
    container.appendChild (textNode)

    container.style.cssText = model.get("cssText")
    model.on("change:name", () => {
        container.innerHTML = model.get("name");
    });
    model.on("change:cssText", () => {
        container.style.cssText = model.get("cssText");
    });
    el.appendChild(container);
    }
    """
    name = traitlets.Unicode(default_value="Button").tag(sync=True)
    cssText = traitlets.Unicode(default_value="").tag(sync=True)


class TextWidgetWithClick(anywidget.AnyWidget):
    _esm = """export function render({ model, el }) {
    const textNode = document.createTextNode(model.get("name"));
    let container = document.createElement("div");
    container.appendChild (textNode)
    let a = new Set(model.get("events"))
    if (a.has("click")){
        container.addEventListener("click", () => {
            let val = model.get("eventType")
            let words = val.split("-")
            let count = 0
            if (words.length > 1){
                count = Number(words[1])
            }
            count += 1
            model.set("eventType", `clicked-${count}`);
            model.save_changes();
        });
    }
    container.style.cssText = model.get("cssText")
    model.on("change:name", () => {
        container.innerHTML = model.get("name");
    });
    model.on("change:cssText", () => {
        container.style.cssText = model.get("cssText");
    });
    el.appendChild(container);
    }
    """
    eventType = traitlets.Unicode().tag(sync=True)
    name = traitlets.Unicode(default_value="Button").tag(sync=True)
    cssText = traitlets.Unicode(default_value="").tag(sync=True)
    state = None
    events = traitlets.List(default_value=[]).tag(sync = True)

class BreadCrumb:
    def __init__(self):
        self._layout = None
        self._css_text = ""
    def set_array_of_string(self, arr):
        self._data = [(val, i) for i, val in enumerate(arr)]
    def set_array_of_dic(self, dic):
        """arr = [{"label": val}]"""
        self._data = [(key, dic[key]) for key in dic]
    def set_array_of_tuple(self, arr):
        """arr = [("label", val)]"""
        self._data = [(label, val) for label, val in arr]
    def get_layout(self):
        if self._layout is None:
            wids = []
            prefix = ""
            for label, val in self._data:
                wid = Main.text(prefix + label, ["click"])
                wid.state = [label, val]
                wid.css_txt = self._css_text
                wid.observe(self._clicked, ["eventType"])
                wids.append(wid)
                prefix = "/"
            self._layout = widgets.HBox(wids)
        return self._layout
    def add(self, label, val):
        pass
    def _clicked(self, state):
        self._emitter.emit("clicked", state)
    def set_emitter(self, emitter):
        self._emitter = emitter
    def set_css_txt(self, css_txt):
        self._css_text = css_txt

class Main:
    def text(label, events = None):
        tw = TextWidget()
        if events:
            tw.events = events
        tw.name = label
        return tw
    def breadCrumbExample():
        from pymitter import EventEmitter
        ee = EventEmitter()
        bc = BreadCrumb()
        bc.set_array_of_string(["a", "bas"])
        bc.set_css_txt("display:block;min-width:50px;color:red") # this is not working
        bc.set_emitter(ee)
        bc.get_layout()

        ee.on("clicked", lambda x: print(x["owner"].state))
