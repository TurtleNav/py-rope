
class _Rope

class Rope:

    def __init__(self, data, left=None, right=None):
        self._data = data if data else ""
        self._length = len(data) 
        self._left = left
        self._right = right

    @property
    def is_leaf(self):
        return self._left is None
    
    @property
    def length(self):
        return self._length

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


