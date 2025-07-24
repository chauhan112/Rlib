from useful.TimeDB import TimeDB
from useful.WordDB import WordDB
class PlanningDB:
    def copyTemporalPlanDataStructure():
        class Tem:
            def waterFall(big = True):
                from useful.jupyterDB import jupyterDB
                jupyterDB.treeTool().waterFall(big)
                
            def statusLogger():
                from useful.jupyterDB import jupyterDB
                name = "TreeCRUD"
                k = jupyterDB.pickle().read(name)
                val = WordDB.replace().replace("8oiAQrjl6QbD", TimeDB.getTimeStamp(), k['brain status'])
                jupyterDB.clip().copy(val)
                
            def weekDataStructure(nextWeek = 0):
                from useful.jupyterDB import jupyterDB
                from useful.WordDB import WordDB
                import datetime
                val = jupyterDB.pickle().read("TreeCRUD")["week plan"]
                l = datetime.datetime.now().weekday() + 1
                wordIdentifierInText = "8oiAQrjl6QbD"
                jupyterDB.clip().copy(WordDB.replace().withContainers(wordIdentifierInText, 
                                    [TimeDB.getTimeStamp(i) for i in range(7*nextWeek-l, 7*(nextWeek + 1)-l, 1)], val))
            
            def monthDataStructure(deltaM = 0):
                from useful.TimeDB import TimeDB
                from useful.jupyterDB import jupyterDB
                import datetime
                from useful.RegexDB import RegexDB
                name = TimeDB.names().ofMonth()[TimeDB.month()+ deltaM-1]
                class MonthdateReplacer:
                    def __init__(self, dates):
                        self.val = 0
                        self.container = dates

                    def __call__(self, txt):
                        p = self.val
                        self.val += 1
                        return self.container[p]

                    def setList(dates):
                        self.container = dates
                        
                    def thisMonthDays(deltaM = 0):
                        y, m,_ = TimeDB.today()[0]
                        m += deltaM
                        d = datetime.datetime(y,m ,1 )
                        dates = []
                        for i in range(d.weekday()):
                            dates.append('..')
                        while (d.month == m):
                            dates.append(str(d.day))
                            d = d + datetime.timedelta(days = 1)

                        for i in range(35-len(dates)):
                            dates.append("..")
                        return dates
                    
                val = jupyterDB.pickle().read("TreeCRUD")['month']
                repl = MonthdateReplacer.thisMonthDays(deltaM)
                jupyterDB.clip().copy(RegexDB.replace("xasd", val, MonthdateReplacer(repl)).replace("asdaMonthName",name))
        return Tem
    
    def convoAdd():
        class Temp:
            def addNewConv(title, conv):
                pass
            
            def view():
                pass
            
        return Temp
    
    def ideasDumper():
        pass
    
    def foodDumper():
        pass
    
    def peopleManager():
        pass