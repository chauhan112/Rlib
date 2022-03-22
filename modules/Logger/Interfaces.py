class IDumperWriter:
    def add(self, key, val, overwrite = False):
        raise NotImplementedError("abstract method")
    def read(self, key):
        raise NotImplementedError("abstract method")
    def delete(self, key):
        raise NotImplementedError("abstract method")
    def readAll(self):
        raise NotImplementedError("abstract method")

class ILogger:
    def log(self):
        raise NotImplementedError("abstract method")
    def setWriter(self, writer:IDumperWriter):
        self.writer = writer
