

class Rope:
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


