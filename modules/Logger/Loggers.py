from modules.Logger.Interfaces import ILogger
from useful.CryptsDB import CryptsDB

class FoodEatingLogger(ILogger):
    def __init__(self, timeOfEating=0, light=True, content =[], misc=None, drinks=[]):
        from useful.TimeDB import TimeDB
        self.timeOfEating = timeOfEating
        if(type(timeOfEating) == int):
            (y, m, day), (h, mi, sec) =TimeDB.today()
            self.timeOfEating = ((y,m,day), (h+timeOfEating, mi,sec))
        self.light = light
        self.content = content 
        self.misc=misc
        self.drinks = drinks
        self.writer = None
    def log(self):
        self.writer.add(list(self.timeOfEating),
                {'content': self.content, 'light': self.light, 
                 'misc':self.misc, 'drinks': self.drinks})
 
class StatusLogger(ILogger):
    def __init__(self,time=0, sleep='7:00 hr', weight=69.5, productivityInPer=60, 
                 spiritedInPercent=85, happinessInPercent=85, health=60):
        from useful.TimeDB import TimeDB
        self.when = TimeDB.getTimeStamp(time)
        self.sleep = sleep
        self.weight = weight
        self.productivity = productivityInPer
        self.spirit = spiritedInPercent
        self.happyness = happinessInPercent
        self.health = health
    def log(self):
        self.writer.add(self.when, {'sleep': self.sleep, 'weight':self.weight, 'productivity':self.productivity, 
          'health': self.health,
                                    'spirit': self.spirit,'happiness': self.happyness})

class StuffsLogger(ILogger):
  def __init__(self, name, pos, misc={}):
    self.name = name
    self.position = pos
    self.miscInfo = misc
  def log(self):
    self.writer.add(CryptsDB.generateUniqueId(),{'name': self.name, 'position':self.position, 'misc':self.miscInfo})