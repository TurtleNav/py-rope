
class _Rope

class Rope:

    def __init__(self, value, weight, length):
        self._value = value
        self._weight = weight
        self._length = length

        self._left = None
        self._right = None

    @property
    def is_leaf(self):
        return self._left is None
    
    @property
    def length(self):
        return self._length or 0

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, v):
        self._value = v

    @classmethod
    def concat(self, other):
        return NotImplemented

    def delete(self, start, length):
        return NotImplemented

    def split(self, index):
        return NotImplemented

    def insert(self, index, string):
        return NotImplemented
    
    def report(self, index, length):
        return NotImplemented

    def index(self, index):
        return NotImplemented


