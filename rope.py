from itertools import combinations_with_replacement
from reprlib import recursive_repr


class Rope:

    def __init__(self, data, left=None, right=None):
        self._data = data
        self._weight = 0
        if data is not None:
            self._weight += len(data)
        if left is not None:
            self._weight += len(left)
        if right is not None:
            self._weight += len(right)
        self._left = left
        self._right = right

    @property
    def is_leaf(self):
        return self._left is None

    @property
    def weight(self):
        return self._weight

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def __len__(self):
        return len(self._data)

    def concat(self, other):
        if self._data is None:
            return other
        if other._data is None:
            return self
        return Rope(data=None, left=self, right=other)

    def delete(self, start, length):
       return 

    def split(self, index):
        return NotImplemented

    def insert(self, index, string):
        return NotImplemented

    def report(self, index, length):
        return NotImplemented

    def index(self, index):
        if (index < 0) or (index > self.weight):
            raise Exception("index is out of bounds")

        if self.is_leaf:
            return self._data[index]

        if index > self.left.weight:
            return self.right.index(self.weight - index)
        return self.left.index(index)

    @recursive_repr()
    def __repr__(self):
        it = [str(self._data) if self._data is not None else ""]
        if self._left is not None:
            it.append(str(self._left))
        if self._right is not None:
            it.append(str(self._right))
        return "".join(it)
