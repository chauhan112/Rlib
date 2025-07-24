from useful.StorageSystem import StorageSystem
class Exercise:
    idx = "86604c9fbbf44301b93a527bd526a980"
    def suggest():
        class Suggestion:
            def naive(exerciseList):
                import random
                return random.choice(exerciseList)
        return Suggestion.naive(Exercise.exerciseList)
    def addExercise(name, cate):
        pkl = Exercise._read()
        pkl.add(["exercises", name],cate )
    def removeExercise(name):
        pkl = Exercise._read()
        pkl.delete(["exercises", name])
    def _read():
        return StorageSystem.dataStructureForIndex(Exercise.idx)
    def exercisesList():
        pkl = Exercise._read()
        return list(pkl.read(["exercises"]).keys())

from enum import Enum
ExerciseCategory = Enum("ExerciseCategory","Arm WholeBody Leg Face")

class ExerciseLogger:
    idx = "ba2af43253424d8e99013425e613a32d"
    def logInterface():
        import ipywidgets as widgets
        from useful.WidgetsDB import WidgetsDB
        class Lyout:
            def __init__(self):
                layout = self.mainLayout()
                display(layout)

            def mainLayout(self):
                self._exesW = WidgetsDB.dropdown(Exercise.exercisesList(),sizeInPercent=20)
                self._valW = widgets.Text(placeholder ="add val", layout=widgets.Layout(width=f"20%"))
                self._valLabelW = widgets.Text(placeholder="set value label", value ="times",
                                               layout=widgets.Layout(width=f"10%"))
                self._notify = widgets.Label(value =":")
                row1 =  widgets.HBox([self._exesW,self._valLabelW,self._valW, WidgetsDB.button("log",
                                        callbackFunc=self.logIt)])
                return widgets.VBox([row1, self._notify])

            def logIt(self, wi):
                name = self._exesW.value
                valLabel = self._valLabelW.value
                times = self._valW.value
                val = 0
                try:
                    val = int(times)
                except:
                    self.notifyUser("invalid times value")
                    return 
                if(val == 0):
                    self.notifyUser("times is zero")
                    return 
                ExerciseLogger.log(name, val, valLabel)
                self.notifyUser("logged " + name)

            def notifyUser(self, msg):
                self._notify.value = ": "+ msg
        return Lyout()

    def log(name, val, valLabel = "times"):
        from useful.TimeDB import TimeDB
        date, time = TimeDB.today()
        pkl = ExerciseLogger._read()
        try: 
            dayContent = pkl.read(list(date))
        except:
            dayContent = []
        dayContent.append([time, name, valLabel, val])
        pkl.add(list(date), dayContent, overwrite = True)

    def _read():
        return StorageSystem.dataStructureForIndex(ExerciseLogger.idx)
