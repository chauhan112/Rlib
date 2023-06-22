class Visualizer:
    def scatterPlot():
        class Temp:
            def matPlot(X,y , x_label, y_label, color="b"):
                import matplotlib.pyplot as plt 
                plt.scatter(X, y, c= color)
                plt.xlabel(x_label)
                plt.ylabel(y_label)
                return plt
            def plotlyPlot(X, y, x_label, y_label):
                pass

            def manyPlots(dataSets):
                """
                one set = (X, y, label, color)
                """
                import matplotlib.pyplot as plt 
                for x,y ,label, color in dataSets:
                    plt.scatter(x,y, label = label, color = color)

                plt.legend()
                return plt

        return Temp

    def addFunc(plot, func, _range,name ="" ):
        if(name == ""):
            plot.plot(_range, func(_range))
        else:
            plot.plot(_range, func(_range), label = name)
            
   
    def boxCompare(seriesList, kind = "box"):
        plt.rcParams["figure.figsize"] = [10, 7]
        fig, ax = plt.subplots(1,len(seriesList), sharey='row')
        for i in range(len(seriesList)):
            seriesList[i].plot(ax = ax[i], kind=kind, subplots=True, figsize=(16,10))
        plt.show()