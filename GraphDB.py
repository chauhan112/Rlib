class IJupyterCodeDisplayer:
    def display(self):
        raise NotImplementedError("abstract method")

class NotebookCodeDisplayer(IJupyterCodeDisplayer):
    def display(self , content, lang="python"):
        import ipywidgets as widgets
        from IPython.display import HTML
        from jupyterDB import jupyterDB
        left = widgets.Output()
        out = widgets.Output()
        lines = content.splitlines()
        nr = "<ol><li><p style='margin:2px 0 0 0'></li>" + "<li></li>"* (len(lines)-1) +"</ol>"
        val = widgets.HBox([left,out])
        with left:
            display(HTML(nr))
        with out:
            display(jupyterDB.displayer(content, lang))
        return val

class LabCodeDisplayer(IJupyterCodeDisplayer):
    def display(self , content, lang="python"):
        from pygments import highlight
        from pygments.formatters import HtmlFormatter
        from pygments.lexers import get_lexer_by_name
        from IPython.display import IFrame, display
        import os
        from CryptsDB import CryptsDB
        from TimeDB import TimeDB
        lexer = get_lexer_by_name(lang, stripall=True)
        name = CryptsDB.generateRandomName() + ".html"
        with open(name, "w") as f:
            highlight(content, lexer, formatter = HtmlFormatter(full=True, linenos=True), outfile=f)
        display(IFrame(src=name, width="1000", height="500"))
        TimeDB.setTimer().oneTimeTimer(60, os.remove, [name])

class GraphDB:
    def plotDictionary(dic):
        GraphDB.plotNodes( GraphDB.dic2Pairs(dic) )
        
    def dic2Pairs(dic):
        pairs = []
        for key in dic:
            pairs.append(("root", key))
            if(type(dic[key]) == list):
                for val in dic[key]:
                    if(type(val) in [int, str, float]):
                        pairs.append((key, val))
                    elif(type(val) == dict):
                        for k in val:
                            pairs.append((key, k))
                            pairs += getPair(val)
            elif(type(dic[key]) in [int, str, float]):
                pairs.append((key, dic[key]))
            elif(type(dic[key] == dict)):
                for k in dic[key]:
                    pairs.append((key, k))
                    pairs += getPair(dic[key][k])
        return pairs

    def displayHtml(htmlContent):
        from IPython.core.display import display, HTML
        display(HTML(htmlContent))
    
    def graphFromEdgesNetworkx(edges):
        # 
        import networkx as nx
        from plotly.graph_objs import Scatter3d, Line, Annotation, Annotations, Marker,Layout, Data, Scene
        from plotly.graph_objs import  XAxis,YAxis,ZAxis,Margin, Scene, Font, Figure
        def visualize_graph_3d(G, node_labels, title="3d"):
            edge_trace = Scatter3d(x=[],
                               y=[],
                               z=[],
                               mode='lines',
                               line=Line(color='rgba(136, 136, 136, .8)', width=1),
                               hoverinfo='none'
                               )


            node_trace = Scatter3d(x=[],
                               y=[],
                               z=[],
                               mode='markers',
                               #name='actors',
                               marker=Marker(symbol='circle',
                                             size=[],
                                             color=[],
                                             colorscale='Jet',#'Viridis',
                                             colorbar=dict(
                                                 thickness=15,
                                                 title='Node Connections',
                                                 xanchor='left',
                                                 titleside='right'
                                             ),
                                             line=Line(color='rgb(50,50,50)', width=0.5)
                                             ),
                               text=[],
                               hoverinfo='text'
                               )

            positions = nx.fruchterman_reingold_layout(G, dim=3, k=0.5, iterations=1000)



            for edge in G.edges():
                x0, y0, z0 = positions[edge[0]]
                x1, y1, z1 = positions[edge[1]]
                edge_trace['x'] += (x0, x1, None)
                edge_trace['y'] += (y0, y1, None)
                edge_trace['z'] += (z0, z1, None)
            
            x_temp = []
            y_temp = []
            z_temp = []

            for node in G.nodes():
                x, y, z = positions[node]
                x_temp.append(x)
                y_temp.append(y)
                z_temp.append(z)
            node_trace['x'] = x_temp
            node_trace['y'] = y_temp
            node_trace['z'] = z_temp


            #for adjacencies in G.adjacency_list():
            #    node_trace['marker']['color'].append(len(adjacencies))



            text_temp = []
            for node in node_labels:
                text_temp.append(node)
            node_trace['text'] = text_temp

            axis = dict(showbackground=False,
                        showline=False,
                        zeroline=False,
                        showgrid=False,
                        showticklabels=False,
                        title=''
                        )

            layout = Layout(
                title=title,
                width=1000,
                height=1000,
                showlegend=False,
                scene=Scene(
                    xaxis=XAxis(axis),
                    yaxis=YAxis(axis),
                    zaxis=ZAxis(axis),
                ),
                margin=Margin(
                    t=100
                ),
                hovermode='closest',
                annotations=Annotations([
                    Annotation(
                        showarrow=False,
                        text="",
                        xref='paper',
                        yref='paper',
                        x=0,
                        y=0.1,
                        xanchor='left',
                        yanchor='bottom',
                        font=Font(
                            size=14
                        )
                    )
                ]), )

            data = Data([node_trace, edge_trace])
            fig = Figure(data=data, layout=layout)
            fig.show()

        graph = nx.DiGraph() 
        graph.add_edges_from(edges)
        visualize_graph_3d(graph, graph.nodes(), title="3D visualization")

    def directedGraphPlotFromEdgeList(g1):
        import numpy as np
        g1 = np.array(g1).reshape((int(len(g1)/2), 2))
        GraphDB.plotDirectedGraph(g1[1:])

    def plotDirectedGraph(edges):
        import networkx as nx
        graph1 = nx.DiGraph()
        graph1.add_edges_from(edges)
        nx.draw(graph1, with_labels = True)

    def plotNodes(jgraphNodesOrDic):
        import jgraph
        jgraph.draw(jgraphNodesOrDic)

    def jgraphGraph(jgraphNodesOrDic):
        GraphDB.plotNodes(jgraphNodesOrDic)

    def plotX(dic, title=''):
        import matplotlib.pyplot as plt
        if(len(dic) != 1):
            raise IOError("Invalid inputs! Give your inputs as {'x_name':list}, title = 'sth'")
        keys = list(dic.keys())
        plt.plot(dic[keys[0]])
        plt.xlabel(keys[0])
        plt.title(title)
    
    def plotXY(dic, title = ''):
        import matplotlib.pyplot as plt
        if(len(dic) != 2):
            raise IOError("Invalid inputs! Give your inputs as {'x_name':list, 'y_name': list), title = 'sth'")
        keys = list(dic.keys())
        plt.plot(dic[keys[0]],dic[keys[1]])
        plt.title(title)
        plt.xlabel(keys[0])
        plt.ylabel(keys[1])
        plt.show()

    def bar():
        class Temp:
            def plotly(x, y):
                import plotly.graph_objects as go
                fig = go.Figure([go.Bar(x=x, y=y)])
                fig.show()
                
            def matplotFewParams(dic, title=''):
                if(len(dic) != 2):
                    raise IOError("Invalid inputs! Give your inputs as {'x_name':list, 'y_name': list}, title = 'sth'")
                import matplotlib.pyplot as plt
                keys = list(dic.keys())
                fig = plt.figure()
                ax = fig.add_axes([0,0,1,1])
                if( title != ""):
                    fig.title(title)
                x = dic[keys[0]]
                y = dic[keys[1]]
                ax.bar(x,y)
                plt.xlabel(keys[0])
                plt.ylabel(keys[1])
                plt.show()
                
            def matPlotManyParams(dic, sortDic = False, rotate = 0, xLabel= "", yLabel ="", 
                   barLabel = False, filterFunc = lambda x: True, changeFigSize = False):
                import matplotlib.pyplot as plt
                from ListDB import ListDB
                dic = {key: dic[key] for key in dic if filterFunc(key)}
                if(sortDic):
                    dic = ListDB.sortDicBasedOnValue(dic)
                if(changeFigSize):
                    plt.rcParams["figure.figsize"] = (20,10)
                fig, ax = plt.subplots()
                vals = dic.values()
                bar = ax.bar(dic.keys(), vals)
                x = plt.xticks(rotation= rotate)
                plt.xlabel(xLabel, fontsize=18)
                if(barLabel):
                    for i, v in enumerate(vals):
                        ax.text(i-.25, v, str(v))
                plt.ylabel(yLabel, fontsize=18)
                plt.rcParams["figure.figsize"] = plt.rcParamsDefault["figure.figsize"]

    def frequencyPlot(dic, title = "freq plot", xAxis = "x", yAxis = "y"):
        return GraphDB.barPlot({xAxis:list(dic.keys()), yAxis: list(dic.values())}, title=title)

    def showTableEditor(arr):
        from texttable import Texttable
        t = Texttable()
        for row in arr:
            t.add_row(row)
        print(t.draw())

    def displayCode():
        class Temp:
            def smallNrOfLines(code, lang= "python", displayer= NotebookCodeDisplayer()):
                from IPython.display import display
                display(displayer.display(code, lang))
                
            def manyLines(codes,lang='python'):
                pass

            def folding(codes, lang='python'):
                pass
        return Temp

    def linePlot():
        import plotly.graph_objects as go
        class LinePlot:
            def oneD():
                class Temp:
                    def plotly(arr, label="yLabel"):
                        fig = go.Figure()
                        fig.update_layout(
                            title=label,
                            font=dict(
                                family="Courier New, monospace",
                                size=18,
                                color="#7f7f7f"
                            )
                        )
                        fig.add_trace(go.Scatter(y=arr, mode='lines'))
                        fig.show()

                    def matplot(arr):
                        pass
                return Temp

            def twoD():
                class Temp:
                    def plotly(xArr,yArr):
                        pass
                    def matplot(xArr,yArr):
                        pass
                return Temp

            def threeD():
                class Temp:
                    def plotly(xArr, yArr, zArr):
                        pass
                    def matplot(xArr, yArr, zArr):
                        pass
                return Temp
        return LinePlot