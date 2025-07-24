class ISearchSystem:
    def wordSearch(self, word, case = False):
        raise NotImplementedError("ISearchSystem.word")
    def pattern(self, patt):
        raise NotImplementedError("ISearchSystem.pattern")
    def function(self, func):
        raise NotImplementedError("ISearchSystem.function")
    def search(self, word, case=False, reg=False):
        if(reg):
            return self.pattern(word)
        return self.wordSearch(word,case)

class EmptyClass:
    def __init__(self):
        pass