class RangeTuple:
    def __init__(self, value= 0, included=True):
        self.value = value
        self.included = included
    def touches(self, other):
        assert isinstance(other, RangeTuple), "must be same type as RangeTuple"
        return self.value == other.value and self.included and other.included
    def isLess(self, other):
        assert isinstance(other, RangeTuple), "must be same type as RangeTuple"
        return not self.touches(other) and self.value < other.value
class Range:
    def __init__(self, start=None, end=None):
        if start is None:
            start = RangeTuple(0)
        if end is None:
            end = RangeTuple(start.value +1)
        assert start.value <= end.value
        self.start = start
        self.end = end
    def isLess(self, other):
        assert isinstance(other, Range)
        return self.end.isLess(other.start)
    def isGreater(self, other):
        assert isinstance(other, Range)
        return self.start.isLess(other.end)
    def intersects(self, other):
        assert isinstance(other, Range)
        return not self.isLess(other) and not self.isGreater(other)