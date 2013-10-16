class Cache:
    '''
    This class encapsulates a map with three operations: has,
    get and set. It is just a wrapper around dict operations.
    '''
    def __init__(self):
        self.store = dict()

    def has(self, n) :
        return n in self.store.keys()

    def get(self, n) :
        return self.store[n]

    def set(self, n, v) :
        self.store[n] = v
