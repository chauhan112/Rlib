import json
from .tools import ArrayTools, Labels
from .Fields import Field

class Reader:
    def __init__(self, path):
        with open(path, "r") as f:
            self.data = json.load(f)

class ArcQuestion:
    def __init__(self, question):
        self.question = question
    def shape(self,idx=0, inputOrOutput= Labels.input):
        return ArrayTools.shape(self.question[Labels.train][idx][inputOrOutput])
    def get(self,idx=0, inputOrOutput= Labels.input):
        return self.question[Labels.train][idx][inputOrOutput]
    def verify(self, solver):
        assert len(self.question[Labels.train]) >= 1
        for ob in self.question[Labels.train]:
            res = solver(ob[Labels.input])
            assert res.isEqual(Field(ob[Labels.output])), (ob[Labels.output], res.get())
    def getTestOutput(self, solver):
        return [{"output": solver(ob[Labels.input]).arr} for ob in self.question[Labels.test]]