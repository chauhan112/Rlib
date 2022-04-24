class IDatabaseGUI:
    def display(self):
        raise NotImplementedError("abstract method")

class IAbout:
    def display_info(self):
        raise NotImplementedError("abstract method")