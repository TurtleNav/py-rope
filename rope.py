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
    
    """count substrings found in each rope in the rope tree"""
    def _count(self, sub, start, end):
        if self.is_leaf:
            return self.data.count(sub, start, end+1)

        # worst case scenario: sub is longer than the rope node.
        # we could:
        #   * concatenate as many nodes as required
        #   * split sub at the index equivalent to available length of
        #     current node and pass the new sub to the next node
        #
        if len(sub) > (self.left.weight):
            # print("ellooo")
            sub1, sub2 = sub[:self.left.weight], sub[self.left.weight:]
            x = self.left._count(sub1, start, self.left.weight)
            y = self.right._count(sub2, start, end - self.left.weight)
            return (
                x & y
                )
        
        count = 0
        if start < self.left.weight:
            count += self.left._count(sub, start, end - self.right.weight)

        if end >= self.left.weight:
            count += self.right._count(sub, start - self.left.weight, end - self.left.weight)
        return count

    """Special case + error handling wrapper around _count"""
    def count(self, sub, start=0, end=-1):
        if not isinstance(sub, str):
            raise TypeError(f"must be str, not {type(sub)}")

        # implement the bounds found on classic strings
        if start < 0:
            start += self.weight
        if (start < 0) or (start >= self.weight):
            raise IndexError("string index out of range")

        if end < 0:
            end += self.weight
        if (end < 0) or (end >= self.weight):
            raise IndexError("string index out of range")
        
        # Not sure why but the behavior of string.count when start >= end is merely to return 0
        if (start >= end):
            return 0
        
        if not sub:
            return end - start + 1
        # Finally, we can work through our rope
        return self._count(sub, start, end)

