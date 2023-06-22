class IParser:
    def parse(self):
        raise NotImplementedError('abstract method')

class ICodeElement:
    def get_name(self):
        raise NotImplementedError('abstract method')
    def get_range(self):
        raise NotImplementedError('abstract method')
    def get_content(self):
        raise NotImplementedError('abstract method')

class IAdvancOps:
    def get_complexity(self):
        raise NotImplementedError('abstract method')
    def get_dependency(self):
        raise NotImplementedError('abstract method')

class IFunction(ICodeElement):
    def get_params(self):
        raise NotImplementedError('abstract method')

class IClass(ICodeElement):
    def get_methods(self) -> list[IFunction]:
        raise NotImplementedError('abstract method')

class ICodeParser:
    def get_funcs(self) -> list[IFunction]:
        raise NotImplementedError('abstract method')
    def classes(self) -> list[IClass]:
        raise NotImplementedError('abstract method')
