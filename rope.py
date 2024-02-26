from itertools import combinations_with_replacement
from reprlib import recursive_repr


class Rope:

    def __init__(self, data=None, left=None, right=None):
        self._weight = 0
        self.data = data
        self.left = left
        self.right = right
    
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, data):
        self._data = data
        if data is not None:
            self._weight += len(data)

    @property
    def is_leaf(self):
        return self._left is None

    @property
    def weight(self):
        return self._weight

    @property
    def left(self):
        return self._left
    
    @left.setter
    def left(self, left):
        self._left = left
        if left is not None:
            self._weight += len(left)

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, right):
        self._right = right
        if right is not None:
            self._weight += len(right)

    def __len__(self):
        return self.weight

    def concat(self, other):
        if self._data is None:
            return other
        if other._data is None:
            return self
        return Rope(data=None, left=self, right=other)

    def delete(self, start, length):
       return 

    """
    Splitting the rope requires consideration of special cases and recursion
    """
    def split(self, index):

        if index == 0:
            return None, self
        
        if index == self.weight:
            return self, None

        if index == self.left.weight:
            return self.left, self.right

        if index < self.left.weight:



            re_left = Rope(self.left.data[:index])




            if self.left.isleaf:
                re_left = Rope(self.left._data[:index])
                re_right = self.right.concat()
            new_left = Rope(self._data[:index])
            return Rope(self._data[:index]), self.concat(self.right)

        if index - 1 == self.weight:
            # If the requested split index is at the final index of the rope,
            # we either return the root rope / left and right
            if self.is_leaf:
                return self, self.right
            
            return self.left, self.right
        
        rope = Rope()

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
    
    def __iter__(self):
        yield self

        if not self.is_leaf:
            yield from self.left
            yield from self.right
    
    def _copy(self, cb):
        node = Rope()
        if self.is_leaf:
            node.data = cb(self.data)
        else:
            node.left = cb(self.left)
            node.right = cb(self.right)

    def capitalize(self):
        node = Rope()
        if self.is_leaf:
            node.data = self.data.capitalize()
        else:
            node.left = self.left.capitalize()
            node.right = self.right.capitalize()
        return node
    
    def casefold(self):
        node = Rope()
        if self.is_leaf:
            node.data = self.data.casefold()
        else:
            node.left = self.left.casefold()
            node.right = self.right.casefold()
        return node
    
    def center(self, width, fillchar=" "):
        if width <= self.weight:
            return self  # TODO: return copy??
        
        new_root = Rope()

        new_root.left = Rope(
            left=Rope(fillchar * ((width - self.weight + 1) // 2)),
            right=self.left
            )
        
        new_root.right = Rope(
            left=self.right,
            right=Rope(fillchar * ((width - self.weight) // 2))
        )
        
        return new_root