class IFunc:
    def get_key(self):
        pass
    def get_result(self):
        pass
    def set_data(self, data):
        pass
class ContentFunc(IFunc):
    def set_data(self, data):
        self._data = data
    def get_result(self):
        return self._data
    def set_key_function(self, func):
        self._func = func
    def get_key(self):
        return self._func(self._data)
class IGrouper:
    def get(self):
        pass
    def set_grouping_function(self, func:IFunc):
        pass
class IResetable:
    def reset(self):
        pass
class INextable:
    def has_next(self):
        pass
    def move_forward(self):
        pass
class IPreviousable:
    def has_prev(self):
        pass
    def get_prev(self):
        pass
    def move_back(self):
        pass
class IDicIterableStrategy:
    def get_key(self):
        pass
    def get_value(self):
        pass
class IIterable(INextable, IPreviousable):
    def get(self):
        pass
class INode:
    def get_children(self) -> list:
        pass
    def get_value(self):
        pass
    def get_parent(self):
        pass
class DicBreadthFirstSearch(IDicIterableStrategy, IIterable, IResetable):
    pass
class DicDepthFirstSearch(IDicIterableStrategy, IIterable, IResetable):
    pass
class FirstLevelIterator(IDicIterableStrategy, IIterable, IResetable):
    def __init__(self, dic={}):
        self.set_dic(dic)
        self._keys = dic.keys()
        self._current_index = 0
    def set_dic(self, dic):
        self._dic = dic
    def get_key(self):
        return self._keys[self._current_index]
    def move_forward(self):
        self._current_index += 1
    def get_value(self):
        return self._dic[self.get_key()]
    def has_next(self):
        return self._current_index < len(self._keys)
    def move_back(self):
        self._current_index -= 1
    def has_prev(self):
        return self._current_index -1 >= 0
    def get(self):
        return self.get_key()
class DicIterator(IIterable):
    def __init__(self, dic):
        self.set_dic(dic)
        self.set_strategy(FirstLevelIterator())
    def has_next(self):
        return self._strategy.has_next()
    def get_next(self):
        key = self._strategy.get_key()
        val = self._strategy.get_value()
        self._strategy.goto_next()
        return key, val
    def set_dic(self, dic):
        self._dic = dic
        self._strategy.set_dic(self._dic)
    def set_strategy(self, strategy: IDicIterableStrategy):
        self._strategy = strategy
    def reset(self):
        self._strategy._current_index = 0
    def get_prev(self):
        self._strategy.goto_next()
class GroupContainer(IGrouper):
    def get(self):
        gr = {}
        while self._iterable.has_next():
            val = self._iterable.get_next()
            self._func.set_data(val)
            key = self._func.get_key()
            if key not in gr:
                gr[key] = []
            gr[key].append(self._func.get_value())
        return gr
    def set_container(self, container: IIterable):
        self._iterable = container
    def set_grouping_function(self, func: IFunc):
        self._func = func

class ISorterStrategy:
    def get_res(self):
        pass
    def add_to_res(self, val):
        pass
    def compare_key(self, x):
        pass
    def get_container(self, data):
        pass
class ISort:
    def do(self):
        pass
    def set_sorter(self, sorter: ISorterStrategy):
        pass
class GeneralSorter(ISort):
    def __init__(self, reverse= False):
        self._reverse = reverse
    def do(self):
        res = sorted(self._sorter.get_container(), key = self._sorter.compare_key)
        if self._reverse:
            res = res[::-1]
        for val in res:
            self._sorter.add_to_res(val)
        return self._sorter.get_res()
    def set_sorter(self, sorter:ISorterStrategy):
        self._sorter = sorter
class GeneralSorterStrategy(ISorterStrategy):
    def __init__(self, container_bag = None):
        self._res = container_bag
        self.set_key(lambda state, x:x)
    def set_key(self, func):
        self._func = func
    def compare_key(self, val):
        return self._func(self, val)
    def get_res(self):
        return self._res
    def add_to_res(self, val):
        self._res_add_func(self,val)
    def set_container(self, data):
        self._data = data
    def get_container(self):
        return self._data
    def set_res_container_add_func(self, func):
        self._res_add_func = func
class Node(INode):
    def __init__(self, idd):
        self.value = idd
        self.children = []
        self.parent = None
        self.extra_info = EmptyClass()
    def get_value(self):
        return self.value
    def get_children(self):
        return self.children
    def get_parent(self):
        return self.parent
class AnySizeList(IIterable, IResetable):
    def __init__(self):
        self._current = None
    def set_data(self, data):
        self._data = data
        self._dimension  = self._get_shape(self.data)
        self._num_system = NTupleNSystem(self._dimension)
        self.reset()
    def get(self):
        pos = self._num_system.get()
        val = self._data
        for index in pos:
            val = val[index]
        return val
    def has_next(self):
        try:
            self._num_system.add(1)
            self._num_system.add(-1)
            return True
        except:
            return False
    def has_prev(self):
        pass
    def reset(self):
        self._num_system.set_zeros()
    def get_index_of_current_element(self):
        return self._current
    def _get_shape(self, data):
        import numpy as np
        return np.array(data).shape