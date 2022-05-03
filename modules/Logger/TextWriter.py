from modules.Logger.Interfaces import IDumperWriter
from FileDatabase import File
import os
class IParser:
    def read(self):
        raise NotImplementedError("abstract method")
    def write(self):
        raise NotImplementedError("abstract method")

class IContentParser:
    def parse(self, txt):
        raise NotImplementedError("abstract method")

class OverwritableSameKeyContentParser(IContentParser):
    def parse(self, txt):
        from WordDB import WordDB
        elementList = WordDB.regexSplit("===+", txt)
        res = {}
        for ele in elementList:
            if ele.strip() == "":
                continue
            head, content = WordDB.regexSplit("\-\-\-\-+", ele)
            res[head.strip()] = content.strip()
        return res

class DuplicatableSameKeyContentParser(IContentParser):
    def parse(self, txt):
        from WordDB import WordDB
        elementList = WordDB.regexSplit("===+", txt)
        res = {}
        for i, ele in enumerate(elementList):
            if ele.strip() == "":
                continue
            head, content = WordDB.regexSplit("\-\-\-\-+", ele)
            head = head.strip()
            if head in res:
                head += "-" + str(i)
            res[head] = content.strip()
        return res

class YamlParser(IParser):
    def __init__(self, filePath):
        self.path = filePath
        self.content = self.read()
        if self.content is None:
            self.content = {}
    def read(self):
        import yaml
        content = File.getFileContent(self.path)
        return yaml.load(content, Loader=yaml.FullLoader)
    def write(self):
        import yaml
        File.overWrite(self.path, yaml.dump(self.content))

class TextParser(IParser):
    def __init__(self, filePath):
        self.path  = filePath
        self.set_content_parser(OverwritableSameKeyContentParser())
        self.content = self.read()
    def read(self):
        return self._parser.parse(File.getFileContent(self.path))
    def write(self):
        txt = ""
        for ke in self.content:
            cont = f'{ke}\n{"-"*15}\n {self.content[ke]}\n'
            txt += f'{"="*15}\n{cont}'
        txt = txt.strip("=")
        txt = txt.strip()
        File.overWrite(self.path, txt)
    def set_content_parser(self, parser: IContentParser):
        self._parser = parser

class TextWriter(IDumperWriter):
    def set_parser(self, parser:IParser):
        self.parser = parser

    def add(self, key, value, overwrite = False):
        if key in self.parser.content:
            if not overwrite:
                print("value already exists")
                return
        self.parser.content[key.strip()] = value
        self.parser.write()

    def read(self, key):
        if key in self.parser.content:
            return self.parser.content[key]
        print("key does not exist")
    def delete(self, key):
        if key in self.parser.content:
            del self.parser.content[key]
        self.parser.write()
    def readAll(self):
        return self.parser.read()
