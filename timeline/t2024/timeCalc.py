from timeline.t2024.experiments.morphism.withCIT.morphismWithCIT import BaseComponent, Utils, IpywidgetsComponentsEnum
from useful.basic import NameSpace
from datetime import datetime
class HourCalculator(BaseComponent):
    def render(self):
        self.outputs.components = NameSpace()
        self.outputs.components.total = Utils.get_ipy_omni("label", {"value": "total hour: "}, IpywidgetsComponentsEnum.Label, bind = False)
        self.outputs.components.count =  Utils.get_ipy_omni("count", {"value": "x"}, IpywidgetsComponentsEnum.Label, bind = False)
        self.outputs.components.start = Utils.get_ipy_omni("abc", {"description": "start time"}, IpywidgetsComponentsEnum.DatetimePicker)
        self.outputs.components.end = Utils.get_ipy_omni("abc1", {"description": "end time"}, IpywidgetsComponentsEnum.DatetimePicker, bind = False)
        self.outputs.components.add = Utils.get_ipy_omni("abc3", {"icon": "plus"}, IpywidgetsComponentsEnum.Button)
        self.outputs.components.reset = Utils.get_ipy_omni("abc3", {"description": "reset"}, IpywidgetsComponentsEnum.Button)
        self.outputs.components.prev = Utils.get_ipy_omni("abc3", {"description": "prev"}, IpywidgetsComponentsEnum.Button)
        vals = Utils.get_repeater_omni("sss", [Utils.get_repeater_omni("asa", [self.outputs.components.total,
                                                                               self.outputs.components.count]), 
                                               Utils.get_repeater_omni("asa", [self.outputs.components.start, 
                                                                               self.outputs.components.end, 
                                                                               self.outputs.components.add, 
                                                                               self.outputs.components.reset, 
                                                                               self.outputs.components.prev])])
        vals.set_global_state(self.gstate)
        self.outputs.instance = vals
        self.outputs.instance.render()
        self.bind()
        self.gstate.cssManager.cssAdder.content = """
        .sss {
            flex-direction: column;
        }
        .abc3{
            width: auto;
        }
        """
    def bind(self):
        count = self.outputs.components.count
        count.state.min = 0
        count.state.history = []
        count.state.hour = 0
        self.outputs.components.add.handlers.handle = self.addVals
        self.outputs.components.reset.handlers.handle = self.resetCallback
        self.outputs.components.start.handlers.handle = self.updateEnd
        self.gstate.logger.set_level(10000)
    def addVals(self,info):
        count = self.outputs.components.count
        start = self.outputs.components.start
        end = self.outputs.components.end
        startDate = start.outputs.layout.value
        endDate = end.outputs.layout.value
        if not (startDate and endDate):
            return
        ts = datetime.timestamp(start.outputs.layout.value)
        ts2 = datetime.timestamp(end.outputs.layout.value)
        minval = (ts2-ts) / 60

        count.state.min += minval
        count.state.hour += (count.state.min//60)
        count.state.min = (count.state.min % 60)
        count.outputs.layout.value = f"{count.state.hour} hr {count.state.min} min"
    def resetCallback(self, info):
        count = self.outputs.components.count
        count.state.min = 0
        count.state.hour = 0
        count.outputs.layout.value = f"0 hr {0} min"
    def updateEnd(self, info):
        start = self.outputs.components.start
        end = self.outputs.components.end
        end.outputs.layout.value = start.outputs.layout.value
class Main:
    def hourCalc():
        from timeline.t2024.experiments.morphism.withCIT.morphismWithCIT import GlobalStructure
        hc = HourCalculator()
        hc.set_global_state(GlobalStructure())
        hc.render()
        return hc