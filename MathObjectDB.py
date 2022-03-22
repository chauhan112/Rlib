class MathObjectDB:
    @staticmethod
    def getRange(a,b):
        if(type(a) == int and type(b) == int):
            return Range(a,b)
        raise IOError("parameters must be int")


class Range:
    def __init__(self, left, right):
        self.left = left
        self.right = right 
    
    def merge(self, anotherRange):
        if(self.left > anotherRange.left):
            self.left = anotherRange.left
        if(self.right < anotherRange.right ):
            self.right = anotherRange.right
    
    def intersects(self, anotherRange):
        return self.calcDistance(anotherRange) <= 0
    
    def calcDistance(self, anotherRange):
        if(anotherRange.right >= self.right):
            return anotherRange.left - self.right
        return self.left - anotherRange.right

    def __str__(self):
        return f"({self.left}, {self.right})"

class OpenRange(Range):
    def intersects(self,anotherRange):
        return self.calcDistance(anotherRange) < 0

class RangeTest:
    def intersectsTest():
        r = Range(0,1)
        r2 = Range(2,3)
        r3 = Range(0,5)
        r4 = Range(1,2)
        assert(r.intersects(r2) == False)
        assert(r.intersects(r3) == True)
        assert(r.intersects(r) == True)
        assert(r2.intersects(r) == False)
        assert(r.intersects(r4) == True)
        assert(r4.intersects(r) == True)
        assert(r3.intersects(r) == True)

class SympyDB:
    def plotSympyFunc(symExpression,variables ="x", defaultRange= None):
        from sympy import plot, var
        var(variables)
        if(defaultRange is not None):
            exec(f"plot({symExpression}, ({variable}, {str(defaultRange).strip('(')})")
        else:
            exec(f"plot({symExpression}) ")
        
    def solveTheExpression(exp, varibales = "x y z", solveForVariable = "x"):
        # exp equals zero
        # variables = "x y z"
        from sympy.solvers import solve
        from sympy import var
        var(varibales)
        txtEx = f"p = solve({exp}, {solveForVariable})"
        exec(txtEx, globals())
        return p