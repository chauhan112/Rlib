import anywidget
import traitlets

class ButtonWidget(anywidget.AnyWidget):
    _esm = """export function render({ model, el }) {
        let button = document.createElement("button");
        button.innerHTML = model.get("name");
        button.addEventListener("click", () => {
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
        model.on("change:name", () => {
            button.innerHTML = model.get("name");
        });
        el.appendChild(button);
    }"""
    eventType = traitlets.Unicode().tag(sync=True)
    name = traitlets.Unicode(default_value="Button").tag(sync=True)
