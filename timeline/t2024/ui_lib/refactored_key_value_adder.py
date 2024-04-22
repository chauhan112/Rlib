from timeline.t2024.ui_lib.IpyComponents import IpywidgetsComponentsEnum, Utils, ComponentsLib
from basic import NameSpace, addToNameSpace
from timeline.t2024.experiments.namespace_generic_logger import DictionaryCRUD
class DicListCRUD(DictionaryCRUD):
    def write(self, key, value, overwrite = False):
        curVal = self.readAll()
        if type(curVal) == list:
            if overwrite and type(key) == int:
                curVal[key] = value
            else:
                curVal.append(value)
        else:
            super().write(key, value, overwrite)
    def delete(self, key):
        vals = self.readAll()
        del vals[key]
def OpsComponent():
    def _temp(state):
        opsType = Utils.get_comp({"options": ["add", "delete"]}, IpywidgetsComponentsEnum.Dropdown, className="fit")
        multiLineValues = Utils.get_comp({"placeholder": "content"}, IpywidgetsComponentsEnum.Textarea, bind=False, className="w-100 textarea-h-150px p0")
        keyInp = Utils.get_comp({"placeholder": "key"},IpywidgetsComponentsEnum.Text, bind=False, className="w-120px")
        textInp = Utils.get_comp({"placeholder": "value"},IpywidgetsComponentsEnum.Text, bind=False, className="w-250px")
        inpType = Utils.get_comp({"options": ["text", "var", "textarea", "list", "dict", "bool"]}, IpywidgetsComponentsEnum.Dropdown, className="fit")
        boolVal = Utils.get_comp({"description":"boolValue","indent": False}, IpywidgetsComponentsEnum.Checkbox, bind=False, className="w-auto")
        overwriteBox = Utils.get_comp({"description":"overwrite","indent": False}, IpywidgetsComponentsEnum.Checkbox, className="w-auto")
        okBtn = Utils.get_comp({"description": "ok"}, IpywidgetsComponentsEnum.Button, className="w-auto")
        container = Utils.container([Utils.container([opsType, keyInp, inpType, textInp,boolVal, overwriteBox, okBtn]), multiLineValues],
                                    className="flex flex-column w-100")
        multiLineValues.hide()
        boolVal.hide()
        def ops_changed(wid):
            opsTypeValue = opsType.outputs.layout.value
            if opsTypeValue == "delete":
                overwriteBox.hide()
                valueHide()
            else:
                overwriteBox.show()
                valueShow()
        def inpType_changed(wid):
            inpTypeValue = inpType.outputs.layout.value
            if inpTypeValue in ["text", "var"]:
                textInp.show()
                boolVal.hide()
                multiLineValues.hide()
            elif inpTypeValue == "textarea":
                multiLineValues.show()
                textInp.hide()
                boolVal.hide()
            elif inpTypeValue in ["list", "dict"]:
                multiLineValues.hide()
                textInp.hide()
                boolVal.hide()
            else:
                textInp.hide()
                boolVal.show()
                multiLineValues.hide()
        def valueHide():
            inpType.hide()
            textInp.hide()
            boolVal.hide()
            multiLineValues.hide()
        def valueShow():
            inpType.show()
            textInp.show()
            boolVal.show()
            multiLineValues.show()
            inpType_changed(1)
        def get_key_value():
            valType = inpType.outputs.layout.value
            key = keyInp.outputs.layout.value
            value = None
            if valType == "text":
                value = textInp.outputs.layout.value
            elif valType == "var":
                value = state.global_state[textInp.outputs.layout.value]
            elif valType == "textarea":
                value = multiLineValues.outputs.layout.value
            elif valType == "list":
                value = []
            elif valType == "dict":
                value = {}
            else:
                value = boolVal.outputs.layout.value
            return key, value
        def clearFields():
            keyInp.outputs.layout.value =""
            inpTyp = inpType.outputs.layout.value
            if inpTyp in ["text", "var"]:
                textInp.outputs.layout.value = ""
            elif inpTyp =="textarea":
                multiLineValues.outputs.layout.value = ""
        def overwriteChecked(wid):
            pass
        overwriteBox.handlers.handle = overwriteChecked
        opsType.handlers.handle = ops_changed
        inpType.handlers.handle = inpType_changed
        addToNameSpace(state, locals(), ["state"])
    state = NameSpace()
    _temp(state)
    return state
def KeyValueSetter():
    def _temp(state):
        from generic_loggerV3 import ResultDisplayers
        classes = """
        .w-30px{
            width: 30px;
        }
        .fit{
            width:fit-content;
        }
        .w-250px{
            width:250px
        }
        .w-100px{
            width:100px
        }
        .w-150px{
            width:150px
        }
        .w-120px{
            width:120px
        }
        .min-height-200px{
            min-height: 200px;
        }
        .border-2px-burlywood{
            border: solid 2px Burlywood;
        }
        """

        fileLabel = Utils.get_comp({"value": "File:"}, IpywidgetsComponentsEnum.Label, bind=False, className="w-30px")
        pathText = Utils.get_comp({"value": "dictionary explorer", "disabled": True}, IpywidgetsComponentsEnum.Text, bind=False)
        opsCheckbox = Utils.get_comp({"description":"ops","indent": False}, IpywidgetsComponentsEnum.Checkbox,className="w-auto")
        fileOpsRow = Utils.container([fileLabel, pathText, opsCheckbox])
        locLabel = Utils.get_comp({"value": "Loc:"}, IpywidgetsComponentsEnum.Label, bind=False, className="w-30px")
        locInput = Utils.get_comp({"value": "/", "disabled": True}, IpywidgetsComponentsEnum.Text, bind=False)
        goBackBtn = Utils.get_comp({"icon": "arrow-circle-left"}, IpywidgetsComponentsEnum.Button, bind=False, className="w-auto")
        locRow = Utils.container([locLabel, locInput, goBackBtn])

        keyLabel = Utils.get_comp({"value": "keys:"}, IpywidgetsComponentsEnum.Label, bind=False, className="w-30px")
        keysDisplayer = ResultDisplayers()
        keysRow = Utils.container([keyLabel, keysDisplayer.views.layout])

        opsLabel = Utils.get_comp({"value": "ops:"}, IpywidgetsComponentsEnum.Label, bind=False, className="w-30px")
        opsComp = OpsComponent()
        opsRow = Utils.container([opsLabel, opsComp.views.container])

        cssCompon = Utils.get_comp({}, ComponentsLib.CSSAdder, customCss= classes)
        outputArea = Utils.get_comp({}, IpywidgetsComponentsEnum.Output)
        container = Utils.container([fileOpsRow, locRow, keysRow, opsRow,outputArea, cssCompon],
                                    className="flex flex-column min-height-200px border-2px-burlywood")

        model = DicListCRUD()
        def update_loc():
            loc = "/".join(map(str, model._baseloc))
            if loc == "":
                loc = "."
            state.views.locInput.outputs.layout.value = loc
        def initialize():
            update_loc()
            render_keys()
        def ok_func(btn):
            btn.description = "confirm"
            state.process.opsComp.views.okBtn.handlers.handle = confirm_func
        def confirm_func(btn):
            btn.description = "ok"
            key, val = state.process.opsComp.handlers.get_key_value()
            overwriteIt = state.process.opsComp.views.overwriteBox.outputs.layout.value
            modelVals = model.readAll()
            if type(modelVals) == list:
                if key != "" and overwriteIt:
                    key = int(key)
            elif key.strip() == "":
                raise IOError("Can not add since the key is empty")
            model.write(key, val, overwrite=overwriteIt)
            state.process.opsComp.handlers.clearFields()
            state.process.opsComp.views.okBtn.handlers.handle = ok_func
            render_keys()
        def render_keys():
            modelVals = model.readAll()
            if type(modelVals) == list:
                keys = list(map(str, range(len(modelVals))))
                state.process.opsComp.views.keyInp.outputs.layout.placeholder ="index"
                if state.process.opsComp.views.overwriteBox.outputs.layout.value:
                    state.process.opsComp.views.keyInp.show()
                else:
                    state.process.opsComp.views.keyInp.hide()
            else:
                keys = list(modelVals.keys())
                state.process.opsComp.views.keyInp.outputs.layout.placeholder ="key"
                state.process.opsComp.views.keyInp.show()
            state.process.keysDisplayer.handlers.set_results(keys, state.process.keysDisplayer.process.pageNr)
        def btn_clicked(tn):
            key = state.process.keysDisplayer.process.data[tn._parent.state.index]
            state.process.opsComp.views.keyInp.outputs.layout.value = key
            curVals = state.process.model.readAll()
            if type(curVals) == list:
                key = int(key)
            val = state.process.model.read(key)
            if type(val) in [list, dict]:
                state.process.model._baseloc.append(key)
                state.handlers.render_keys()
                state.handlers.update_loc()
            else:
                print(val)
        def goBackFunc(btn):
            if len(state.process.model._baseloc):
                state.process.model._baseloc.pop()
                state.handlers.render_keys()
                state.handlers.update_loc()
        def name_gtter(x):
            return x
        def ops_checkbox_checked(wid):
            selectedValue = opsCheckbox.outputs.layout.value
            if selectedValue:
                opsRow.show()
            else:
                opsRow.hide()
        def overwriteChecked(wid):
            checkd = state.process.opsComp.views.overwriteBox.outputs.layout.value
            curVals = state.process.model.readAll()
            if type(curVals) == list:
                if checkd:
                    state.process.opsComp.views.keyInp.show()
                else:
                    state.process.opsComp.views.keyInp.hide()
        def delete_clicked(wid):
            wid.description = "confirm"
            state.process.opsComp.views.okBtn.handlers.handle = delete_confirm
        def delete_confirm(btn):
            btn.description = "ok"
            key, val = state.process.opsComp.handlers.get_key_value()
            modelVals = state.process.model.readAll()
            if type(modelVals) == list:
                if key != "":
                    key = int(key)
            elif key.strip() == "":
                raise IOError("Can not add since the key is empty")
            state.process.model.delete(key)
            state.process.opsComp.handlers.clearFields()
            state.process.opsComp.views.okBtn.handlers.handle = delete_clicked
            state.handlers.render_keys()
        def opsChangedV2(wid):
            state.process.opsComp.handlers.defs.ops_changed(wid)
            ops = state.process.opsComp.views.opsType.outputs.layout.value
            if ops == "add":
                state.process.opsComp.views.okBtn.handlers.handle = state.handlers.defs.ok_func

            else:
                state.process.opsComp.views.okBtn.handlers.handle = delete_clicked
        opsComp.views.opsType.handlers.handle = opsChangedV2
        opsComp.views.overwriteBox.handlers.handle = overwriteChecked
        goBackBtn.handlers.handle = goBackFunc
        keysDisplayer.views.btns.handlers.handle = btn_clicked
        opsComp.views.okBtn.handlers.handle = ok_func
        opsCheckbox.handlers.handle = ops_checkbox_checked
        keysDisplayer.views.layout.outputs.layout
        keysDisplayer.handlers.name_getter = name_gtter
        opsRow.hide()
        addToNameSpace(state, locals(), ["state"])
        initialize()
    state = NameSpace()
    _temp(state)
    return state
