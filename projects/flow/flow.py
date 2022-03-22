from FileDatabase import File
from SerializationDB import SerializationDB

class ILevel:
    def get_value(self):
        pass
class FlowGridLevel(ILevel):
    def __init__(self, value = None):
        self._dimension = None
        self.set_value(value)
    def set_value(self, value: list):
        self._value = value
    def load(self, file):
        content = File.getFileContent(file)
        vals= content.split()
        x, y= list(map(int,vals[:2]))
        self._dimension = x,y
        arr = np.zeros((x,y))
        arr = arr.flatten()
        n = int(vals[2])
        i = 3
        count = 0
        while True:
            arr[int(vals[i])-1] = int(vals[i+1])
            count += 1
            i += 2
            if count == n:
                break
        self._value = arr.reshape((x,y))
    def get_value(self):
        return self._value
    def load_from_pickle(self, pkl):
        self._value = SerializationDB.readPickle(pkl)