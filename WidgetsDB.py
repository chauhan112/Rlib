import ipywidgets as widgets
from IPython.display import display

class ButtonWithIdentifier(widgets.Button):
    def __init__(self,key, **kwargs):
        super().__init__(**kwargs)
        self._key = key

class WidgetsDB:
    def progressBar(maxValue= 100):
        f = widgets.IntProgress(min=0, max=maxValue)
        display(f)
        return f
    
    def dropdown(options, callback= None, sizeInPercent= None):
        def on_change(change):
            if change['type'] == 'change' and change['name'] == 'value':
                callback(change)
        w = widgets.Dropdown(options = options)
        if(sizeInPercent is not None):
            w = widgets.Dropdown(options = options, layout=widgets.Layout(width=f"{sizeInPercent}%"))
        if(callback is not None):
            w.observe(on_change)
        return w
    
    def button(name, callbackFunc = None, tooltip = ''):
        b = widgets.Button(description=name, tooltip= str(tooltip))
        if(callbackFunc is not None):
            b.on_click(callbackFunc)
        return b
    
    def mButton(name, identifier, callbackFunc = None):
        b = ButtonWithIdentifier(identifier, description=name)
        if(callbackFunc is not None):
            b.on_click(callbackFunc)
        return b
        
    def getGrid(cols, widgetsList = [], displayIt = True):
        class Grid:
            def __init__(self, no_of_columns):
                self._declareAllWidgets()
                self.mainLayout = self._createMainLayout()
                self.cols = no_of_columns
                if(displayIt):
                    display(self.mainLayout)
            def _createMainLayout(self):
                return widgets.VBox([self._vbox, self.output])
            
            def _declareAllWidgets(self):
                self._vbox = widgets.VBox([widgets.HBox()])
                self.output = widgets.Output(layout=widgets.Layout(width='auto'))
            
            def clearGrid(self):
                self._vbox.children = (widgets.HBox([]), )
            
            def append(self, widget):
                if(len(self._vbox.children[-1].children) % self.cols == 0):
                    self._vbox.children += (widgets.HBox([widget]), )
                    return
                self._vbox.children[-1].children += (widget,)

        ly = Grid(cols)
        for w in widgetsList:
            ly.append(w)
        return ly
    
    def buttonClickEventExample():
        b = widgets.Button(description="Click Me!")
        button = widgets.HBox([b, widgets.Label(value = "raja")])
        output = widgets.Output()

        display(button, output)

        def on_button_clicked(b):
            with output:
                print("Button clicked.")
                print(b.description)

        b.on_click(on_button_clicked)
    
    def searchEngine():
        # search for TempDic(DicSearchEngine for uses
        class Temp:
            def resultWidget():
                class _OutWidget: 
                    def __init__(self):
                        self.searchRes = widgets.Output()
                        self.buttonRes = widgets.Output()
                    def display(self):
                        display(widgets.VBox([self.searchRes, self.buttonRes]))
                return _OutWidget()
        return Temp

    def outArea(displayAlready = True):
        class OutArea:
            def __init__(self):
                self.out = widgets.Output()
                if(displayAlready):
                    display(self.out)
                
            def clear(self):
                self.out.clear_output()
            
            def add2Output(self, widget):
                with self.out:
                    display(widget)
        return OutArea()
    
    def selection(options = None, title = 'selection'):
        class SelectWidget:
            def __init__(self, options = None, title = 'selection'):
                self.sel = widgets.Select(rows=15, layout=widgets.Layout(width='auto', grid_area=title))
                display(self.sel)
                if(options is not None):
                    self.addOptions(options)
            def addOptions(self, options):
                if(type(options) == str):
                    options = [options]
                self.sel.options = options
        return SelectWidget(options, title)

    def _basicFileExplorerIO():
        selection = widgets.Select(rows=15, layout=widgets.Layout(width='auto', grid_area='dircontent'))
        text = widgets.Text(placeholder='output filename', layout=widgets.Layout(width='auto', grid_area='filename'))
        dropdown = widgets.Dropdown(description="", layout=widgets.Layout(grid_area='pathlist'))
        outputDisplay = widgets.Output(layout=widgets.Layout(width='auto', max_height="400px", overflow='auto'))
        title = widgets.HTML(value='title')
        return title, dropdown, text, selection, outputDisplay

    def fileExplorerLayout():
        title, dropdown, text, selection, outputDisplay = WidgetsDB._basicFileExplorerIO()
        b1 = widgets.Button(description='Select', layout=widgets.Layout(width='auto'))
        b2 = widgets.Button(description='Cancel', layout=widgets.Layout(width='auto'))
        logOut = widgets.HTML(value='output:')
        footer = widgets.HBox([b1,b2, logOut])

        top = widgets.HBox(children=[dropdown, text], layout = widgets.Layout(width = 'auto'))
        topWithSelc = widgets.VBox([title,top, selection, footer], 
                            layout = widgets.Layout(width = 'auto', min_width = "484px", top="0px"))
        display(widgets.HBox([topWithSelc, outputDisplay]))
        return title, dropdown, text, selection, b1,b2, logOut, outputDisplay
        
    def ioArea(displayLayout= True):
        title, dropdown, text, selection, outputDisplay = WidgetsDB._basicFileExplorerIO()
        top = widgets.HBox(children=[dropdown, text], layout = widgets.Layout(width = 'auto'))
        b1 = widgets.Button(description='copy path', layout=widgets.Layout(width='auto'))
        b2 = widgets.Button(description='open', layout=widgets.Layout(width='auto'))
        fileOps = widgets.HBox([b1,b2])
        inputs = widgets.VBox([title,top, selection, fileOps], layout = widgets.Layout(width = 'auto',min_width = "484px"))
        layout = widgets.HBox([inputs, outputDisplay])
        if displayLayout:
            display(layout)
        from DataStructure import DataStructure
        k = {
            'title': title,
            'pathsList': dropdown,
            'filename': text,
            'dirList': selection,
            'b1': b1,
            'b2': b2,
            'fileOps': fileOps,
            'layout': layout
        }
        return DataStructure.nestedNamespace(k), outputDisplay

    def audioRelated():
        class Temp:
            def playing():
                class Te:
                    def progress():
                        return widgets.SelectionSlider(
                            options=list(range(300)),
                            value=0,
                            description='name',
                            continuous_update=False,
                        #     layout={'width': 300}
                        )

                    def tools():
                        play = widgets.Play(
                            value=50,
                            min=0,
                            max=100,
                            step=1,
                            interval=500,
                            description="Press play",
                            disabled=False
                        )
                        slider = widgets.IntSlider()
                        widgets.jslink((play, 'value'), (slider, 'value'))
                        return widgets.HBox([play, slider])
                return Te
            def editing():
                import datetime
                dates = [datetime.date(2015, i, 1) for i in range(1, 13)]
                options = [(i.strftime('%b'), i) for i in dates]
                ssl = widgets.SelectionRangeSlider(
                    options=range(1, 13),
                    index=(0, 11),
                    description='2015',
                    disabled=False,
                    layout=widgets.Layout(width='80%')
                    )
                return ssl
        return Temp
        
    def functionWidget(buttonName = "button", textPlaceholder = "", horizontal = True, callbackFunc =lambda x: print(x)):
        button = WidgetsDB.mButton(buttonName, buttonName + "I",callbackFunc=callbackFunc )
        params = widgets.Text(placeholder =textPlaceholder)
        wList = [params, button]
        if(horizontal):
            return widgets.HBox(wList)
        return widgets.VBox(wList)
    def hide(wid):
        wid.layout.display = 'none'
    def show(wid):
        wid.layout.display = None

class WidgetType:
    Text     = "text"
    TextArea = "textarea"
    Dropdown = "dropdown"
    Checkbox = "checkbox"
    Filters  = "filter"
    Date = "date"
    DateTime = "datetime"
    Button = "btn"
class NewWidgetSet:
    def _add_update(dic, **newdic):
        dic.update(newdic)
    def button(des, func = None,**kwargs):
        NewWidgetSet._add_update(kwargs, description=des,layout = {"width": "auto"})
        sbc = widgets.Button(**kwargs)
        if func is not None:
            sbc.on_click(func)
        return sbc
    def dropdown(**kwargs):
        NewWidgetSet._add_update(kwargs, layout = {"width": "auto"})
        return widgets.Dropdown( **kwargs)
    def textarea(placeholder, **kwargs):
        NewWidgetSet._add_update(kwargs, placeholder = placeholder, layout = {'width': "auto", 'height': "100px"})
        return widgets.Textarea(**kwargs)
    def date(label, **kwargs):
        NewWidgetSet._add_update(kwargs, layout = {"width": "auto"}, description=label)
        return widgets.DatePicker(**kwargs)
    def datetime(label, **kwargs):
        NewWidgetSet._add_update(kwargs, layout = {"width": "auto"}, description=label)
        return widgets.NaiveDatetimePicker(**kwargs)
    def tags(**kwargs):
        NewWidgetSet._add_update(kwargs, allow_duplicates=False)
        return widgets.TagsInput(**kwargs)
    def text(place, **kwargs):
        NewWidgetSet._add_update(kwargs, placeholder = place, layout={'width':"auto"})
        return widgets.Text(**kwargs)
    def checkbox(des, **kwargs):
        NewWidgetSet._add_update(kwargs, description =des, indent=False, layout={'width':"auto"})
        return widgets.Checkbox(**kwargs)
    def make_layout(arr):
        pass
    def make_form(arr):
        res = []
        for row in arr:
            roro = []
            for vl in row:
                roro.append(vl)
            res.append(widgets.HBox(roro))
        return widgets.VBox(res)
    def make_wid(widType: WidgetType, **kwargs):
        if widType ==  WidgetType.Checkbox:
            return NewWidgetSet.checkbox(des= kwargs['description'], **kwargs)
        elif widType ==  WidgetType.Text:
            return NewWidgetSet.text(place = kwargs['placeholder'], **kwargs)
        elif widType ==  WidgetType.TextArea:
            return NewWidgetSet.textarea(placeholder = kwargs['placeholder'], **kwargs)
        elif widType ==  WidgetType.Filters:
            return NewWidgetSet.tags(**kwargs)
        elif widType ==  WidgetType.Dropdown:
            return NewWidgetSet.dropdown(**kwargs)
        elif widType ==  WidgetType.Date:
            return NewWidgetSet.date(label = kwargs['description'], **kwargs)
        elif widType ==  WidgetType.DateTime:
            return NewWidgetSet.datetime(label = kwargs['description'], **kwargs)
        elif widType ==  WidgetType.Button:
            fnucn = None
            if "func" in kwargs:
                fnucn = kwargs['func']
            return NewWidgetSet.button(des = kwargs['description'], func=fnucn, **kwargs)
        raise