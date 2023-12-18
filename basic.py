class NameSpace:
    pass
class BasicController:
    def __init__(self) -> None:
        self.controllers = NameSpace()
        self.views = NameSpace()
    def set_model(self, model):
        self._model = model
    def set_scope(self, scope):
        self._scope = scope