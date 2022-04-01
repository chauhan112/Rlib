class KeyManager:
    def __init__(self, keys):
        self.keys = keys
        self.currentIndex = 0
        self.currentPageIndex = 1
        self.nrPerPage = 20
    
    def setCurrentPageIndex(self, val):
        self.currentPageIndex = val
        
    def getButtonIndices(self):
        n = self.totalNrOfPages()
        i = self.currentPageIndex
        if(n < 6):
            return list(range(1, n+1))
        if(self.currentPageIndex < 4):
            return [1,2,3,4,5]
        if(self.currentPageIndex >= (n -2)):
            return [n-4, n-3,n-2,n-1,n]
        return [i-2, i-1, i, i+1, i +2]
    
    def getKeysForCurrentPageIndex(self):
        l = self.currentPageIndex-1
        return self.keys[self.nrPerPage*l: self.nrPerPage*self.currentPageIndex]
    
    def totalNrOfPages(self):
        return 1 + len(self.keys) // self.nrPerPage
    
    def set_limit_per_page(self, val):
        self.nrPerPage = val