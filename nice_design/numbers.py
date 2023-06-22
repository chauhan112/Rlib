class ICountingSystem:
    def add(self, val):
        pass
    def get(self):
        pass
class IComparable:
    def compare(self, val) -> int:
        # 0 for same
        # 1 for greater than self
        # -1 for smaller than self
        pass
class BinarySystem(ICountingSystem):
    pass
class DecimalSystem(ICountingSystem):
    pass

class NTupleNSystem(ICountingSystem, IComparable):
    def __init__(self, upper_limit):
        self._upper = upper_limit
        self.set_zeros()
    def set_zeros(self):
        self._current = [0 for i in self._upper]
    def add(self, val):
        if type(val) == tuple:
            self._add_tuple(val)
        elif type(val) == int:
            self._add(len(self._upper)-1, val)    
    def _add(self, index, val):
        self._current[index] += val
        if self._current[index] >= self._upper[index]:
            carry = self._current[index] // self._upper[index]
            self._current[index] = self._current[index] % self._upper[index]
            index -= 1
            if index >= 0:
                self._add(index, carry)
            else:
                raise IOError("Overflow")
    def _add_tuple(self, tupl):
        for i, val in enumerate(tupl):
            self._add(i, val)
    def get(self):
        return self._current
    def compare(self, val: tuple):
        pass
    def _validity_check(self, val: tuple) -> bool:
        pass