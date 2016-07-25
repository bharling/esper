import pickle
from multiprocessing import Array


class _SharedDict:

    __slots__ = ("size", "_shared_array", "_internal_dict")

    def __init__(self, size=80960):
        self.size = size
        self._shared_array = Array('c', size)
        self._internal_dict = {}

    def __setitem__(self, key, item):
        print("set item")
        self._internal_dict[key] = item
        try:
            self._shared_array.raw = pickle.dumps(self._internal_dict)
        except ValueError("Buffer is too small to hold the dictionary."):
            pass

    def __getitem__(self, key):
        print("get item")
        self._internal_dict = pickle.loads(self._shared_array.raw)
        return self._internal_dict[key]

    def __repr__(self):
        return repr(self._internal_dict)

    def __len__(self):
        return len(self._internal_dict)

    def __delitem__(self, key):
        del self._internal_dict[key]

    def clear(self):
        return self._internal_dict.clear()

    def copy(self):
        return self._internal_dict.copy()

    def pop(self, key, d=None):
        return self._internal_dict.pop(key, d)

    def get(self, key, default=None):
        return self._internal_dict.get(key, default)

    def update(self, *args, **kwargs):
        return self._internal_dict.update(*args, **kwargs)

    def keys(self):
        return self._internal_dict.keys()

    def values(self):
        return self._internal_dict.values()
