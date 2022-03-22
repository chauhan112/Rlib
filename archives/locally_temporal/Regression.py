class Regression:
    def matrix_method(X,y):
        if(len(X.shape) == 1):
            X = X.reshape((len(X), 1))
        X_new = np.hstack( (np.ones( (len(X), 1) ) , X) )
        xt = X_new.T.dot(X_new)
        return np.linalg.inv(xt).dot(X_new.T).dot(y)
    
    def matrix_method_with_regulaization(X,y, l):
        if(len(X.shape) == 1):
            X = X.reshape((len(X), 1))
        X_new = np.hstack( (np.ones( (len(X), 1) ) , X) )
        xt = X_new.T.dot(X_new)
        xt = xt + l* np.identity(xt.shape[0])
        return np.linalg.inv(xt).dot(X_new.T).dot(y)


class Matrix:
    def addOneBeforeRows( mat,val = 1):
        return np.hstack((np.ones((len(mat),1)), mat))
    
class MatrixTest:
    def addOneBeforeRowsTest():
        val = np.array([[1, 2],
                       [3, 4]])
        res = np.array([[1,1,2],[1,3,4]])
        print(Matrix.addOneBeforeRows(val) == res)

class RegressionWithTransformation:
    def __init__(self, X, y):
        self.weight = None
        self.X = X
        self.y = y
        self.fitted = False
    
    def get_final_g(self, x):
        x = self._transformX(x)
        x = Matrix.addOneBeforeRows(x)
        res = x.dot(self.weight)
        if(type(x) == int):
            return res[0]
        return res.flatten()
    
    def plot(self, funcs = {}, minV = None, maxV = None, xLabel = "", yLabel = ""):
        if(minV is None):
            minV = np.amin(X)
        if(maxV is None):
            maxV = np.amax(X)
        plot = Visualizer.scatterPlot().matPlot(self.X,self.y, xLabel,yLabel)
        for funcName in funcs:
            Visualizer.addFunc(plot, funcs[funcName], np.arange(minV, maxV, 0.1), name = funcName)
        if(self.fitted):
            Visualizer.addFunc(plot, self.get_final_g, np.arange(minV, maxV, 0.1), name = "Hypothesis function")
        plot.legend()
    
    def fit(self):
        self.weight = Regression.matrix_method(self._transformX(self.X), self.y)
        self.fitted = True
    
    def phiX(self, x):
        raise IOError("not implemented yet")
    
    def _transformX(self, xArrOrVal):
        if(type(xArrOrVal) == int):
            xArrOrVal = np.array([xArrOrVal])
        return np.array([list(self.phiX(val)) for val in xArrOrVal])

    def predict(self, xValid):
        return self.get_final_g(xValid)
    
    def e_out(self, xs, ys):
        y1 = self.get_final_g(xs)
        ys = ys.flatten()
        val = np.sum((y1-ys)**2)/len(y1)
        return val
    
class RegWithTransOfOrder4(RegressionWithTransformation):
    def phiX(self,x):
        return np.array([x, x*x, x**3, x**4])

class RegWithTransWithRegularization(RegWithTransOfOrder4):
    def __init__(self, X, y, l):
        super().__init__(X, y)
        self.lambd = l
        
    def fit(self):
        self.weight = Regression.matrix_method_with_regulaization(self._transformX(self.X), self.y, self.lambd)
        self.fitted = True
        
class RegrWithTraOrd8WithRegularization(RegWithTransWithRegularization):
    def phiX(self,x):
        func = generic_polynomial(8)
        return func(x)

def generic_polynomial(order):
    return lambda x: x**np.arange(1,order+1)
