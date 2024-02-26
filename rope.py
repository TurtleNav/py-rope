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
        if not self.is_leaf:
            yield from self.left
            yield from self.right
        else:
            yield self

    """
    Common design pattern required for any rope implementation of a string
    method where a copy is returned with data slightly manipulated.
    """
    def _new_rope_from_method(self, method, *args, **kwargs):
        node = Rope()
        if self.is_leaf:
            node.data = getattr(self.data, method)(*args, **kwargs)
        else:
            node.left = getattr(self.left, method)(*args, **kwargs)
            node.right = getattr(self.right, method)(*args, **kwargs)
        return node

    def capitalize(self):
        return self._new_rope_from_method("capitalize")
    
    def casefold(self):
        return self._new_rope_from_method("casefold")
    
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

    def encode(self, encoding="utf-8", errors="strict"):
        return self._new_rope_from_method("encode", encoding, errors)
    
    # TODO
    def endswith(suffix, start=0, end=-1):
        if not isinstance(suffix, (str, tuple)):
            raise TypeError("endsiwth first arg must be str or a tuple of str, not int")
    
    def expandtabs(self, tabsize=8):
        return self._new_rope_from_method(tabsize)

    # TODO
    def find(self, sub, start=0, end=-1):
        pass

    # TODO
    def format(self, *args, **kwargs):
        pass

    # TODO
    def format_map(self, mapping):
        pass

    # TODO
    def index(self, sub, start=0, end=-1):
        pass

    """
    Wrapper for each isX string methods. All must iterate through each child
    rope and call the corresponding str.X on that rope's data.
    """
    def _is_x(self, x):
        res = True
        for node in self:
            res &= getattr(node.data, x)()
            if not res:
                break
        return res

    # ================== The isX block of string methods ======================

    def isalnum(self): return self._is_x("isalnum")
    def isalpha(self): return self._is_x("isalpha")
    def isascii(self): return self._is_x("isascii")
    def isdecimal(self): return self._is_x("isdecimal")
    def isdigit(self): return self._is_x("isdigit")
    def isidentifier(self): return self._is_x("isidentifier")
    def islower(self): return self._is_x("islower")
    def isnumeric(self): return self._is_x("isnumeric")
    def isprintable(self): return self._is_x("isprintable")
    def isspace(self): return self._is_x("isspace")
    def istitle(self): return self._is_x("istitle")
    def isupper(self): return self._is_x("isupper")

    # TODO
    def join(self, iterable):
        pass

    # TODO
    def ljust(self, width, fillchar=" "):
        pass

    # TODO
    def lstrip(self, chars=None):
        pass

    # TODO
    def maketrans(self, x, y=None, z=None):
        pass

    # TODO
    def partition(self, sep):
        pass

    # TODO
    def removeprefix(prefix):
        pass

    # TODO
    def removesuffix(suffix):
        pass

    # TODO
    def replace(self, old, new, count=None):
        pass

    # TODO
    def rfind(self, sub, start=0, end=-1):
        pass

    # TODO
    def rindex(self, sub, start=0, end=-1):
        pass

    # TODO
    def rjust(self, width, fillchar=" "):
        pass

    # TODO
    def rpartition(self, sep):
        pass

    # TODO
    def rsplit(self, sep=None, maxsplit=-1):
        pass

    # TODO
    def rstrip(self, chars=None):
        pass

    # TODO
    def split(self, sep=None, maxsplit=-1):
        pass

    # TODO
    def splitlines(keepends=False):
        pass

    # TODO
    def startswith(self, prefix, start=0, end=-1):
        pass

    # TODO
    def strip(self, chars=None):
        pass

    def swapcase(self):
        return self._new_rope_from_method("swap")
    
    def title(self):
        return self._new_rope_from_method("title")

    def translate(self, table):
        return self._new_rope_from_method("translate", table)

    def upper(self):
        return self._new_rope_from_method("upper")
    
    def zfill(self, width):
        return self._new_rope_from_method("zfill", width)