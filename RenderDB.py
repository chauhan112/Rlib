from WordDB import WordDB

class MatrixCalculate:
    def __init__(self):
        self.steps = []
        self.maxHeight = 0
    
    def render(self):
        line = 1
        
        while (line != self.maxHeight):
            for i, val in enumerate(self.steps):
                step, k = val
                rend = (self.maxHeight - k ) / 2
                p = line - int(rend)
                if( i >= rend and i < (rend+len(step))):
                    print(step[p], end = "")

                if(i % 3 ==0 ):
                    print()
            line += 1

    def wordFormat(nr, spaceNr):
        k = spaceNr - len(str(nr))
        if(k <1):
            return str(nr)
        return " "*k + str(nr)
    
    def getMatrix(matStr, size = 3):
        k = [" ".join([MatrixCalculate.wordFormat(val[i:j], size) for i, j in 
                WordDB.searchWordWithRegex("[0-9\-\+]+", val)]) for val in matStr]
        return k
    
    def step(self, string, matrix = False):
        stringList = string.strip().split("\n")
        if(matrix):
            stringList = MatrixCalculate.getMatrix(stringList)
        if(self.maxHeight < len(stringList)):
            self.maxHeight = len(stringList)
            
        self.steps.append((stringList, len(stringList)))
        self.render()