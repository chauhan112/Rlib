from enum import IntEnum
class TaskStatus(IntEnum):
    NotDone = 1
    Done = 2
    SeeComment = 3

class TaskManager:
    def __init__(self, name):
        self.name = name
        self.clear()
        self._load()

    def summary(self):
        print(f"Total number of tasks: {len(self.tasks)}")
        print(f"Number of done tasks: {self._doneTask['nr']}")
        print(f"Number of undone tasks: {len(self._taskNames) - self._doneTask['nr']}")

    def done(self, taskNr, comment= ""):
        self._doneTask['nr'] += 1
        self.tasks[taskNr-1]['status'] = TaskStatus.Done
        self.tasks[taskNr-1]['comment'] = comment
        self.archive(True)

    def undo(self, taskNr):
        self._doneTask['nr'] -= 1
        self.tasks[taskNr-1]['status'] = TaskStatus.NotDone

    def notDoneTaskSummary(self):
        for i, val in enumerate(self.tasks):
            name = val['name']
            comment = val['comment']
            if(val['status'] != TaskStatus.Done):
                print("{:>3d}. {} is not done".format(i, name))

    def setTasks(self, totalNr = -1, taskNames = []):
        if(len(self.tasks) != 0):
              print("there are some tasks running. Clear them first")
              return
        if(len(taskNames) != 0 and totalNr == -1):
            totalNr = len(taskNames)
        if(totalNr == -1):
            print("Give total number of tasks you are doing")
            return
        if(len(taskNames) == 0):
            taskNames = [f"Task {i+1}" for i in range(totalNr)]
        for name in taskNames:
            self.tasks.append({'name': name, 'comment': "", "status": TaskStatus.NotDone})
        self._taskNames = taskNames

    def _load(self):
        from DataStorageSystem import NotesTable
        nt  = NotesTable("task manager")
        try:
            val = nt.getContentOfThisTable()
            if ( self.name in val ):
                print(f"loading task {self.name} from archive")
                self.tasks = val[self.name]['tasks']
                self._doneTask = val[self.name]['doneTask']
                self._taskNames = val[self.name]['taskNames']
        except:
            pass

    def clear(self):
        self.tasks = [] # {'name': "", "comment": "", "status": TaskStatus.NotDone}
        self._doneTask = {'nr': 0}
        self._taskNames = {}

    def archive(self, override = False):
        from DataStorageSystem import NotesTable
        nt = NotesTable("task manager")
        try:
            if(not override and self.name in nt.getContentOfThisTable()):
                print(f"{self.name} already exists.")
                return
        except:
              pass
        tasks = self.tasks.copy()
        for val in tasks:
            val['status'] = int(val['status'])
        nt.add(self.name, {'tasks': tasks, 'doneTask': self._doneTask, 'taskNames': self._taskNames}, overwrite=True)