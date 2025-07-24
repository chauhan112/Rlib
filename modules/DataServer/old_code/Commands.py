class ICommand:
    def serialize(self):
        raise NotImplementedError("abstract method")
    def run(self):
        raise NotImplementedError("abstract method")
    def load(self, serializedContent):
        raise NotImplementedError("abstract method")
        

class CopyContentToServerClipboard(ICommand):
    def __init__(self, text):
        self.content = text
    def serialize(self) -> tuple:
        return (commands.Copy2Clipboard.name, self.content)
    def run(self):
        from useful.FileDatabase import File
        File.createFile('clipboard.txt', self.content)
    def load(self, content):
        self.content = content[1]

class SyncCommand(ICommand):
    pass

