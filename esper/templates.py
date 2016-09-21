import multiprocessing
import pickle


class Processor:
    def __init__(self):
        self.world = None
        self.parallel = False

    def process(self, *args):
        raise NotImplementedError


class ParallelProcessor:
    def __init__(self):
        self.world = None
        self.parallel = True

    def process(self, *args):
        raise NotImplementedError


class SharedDict:

    __slots__ = ("size", "_shared_array", "_internal_dict")

    def __init__(self, size=80960):
        self.size = size
        self._internal_dict = {}
        self._shared_array = multiprocessing.Array('c', size)
        self._shared_array.raw = pickle.dumps(self._internal_dict)

    def __setitem__(self, key, item):
        self._internal_dict[key] = item
        try:
            self._shared_array.raw = pickle.dumps(self._internal_dict)
        except ValueError("Buffer is too small to hold the dictionary."):
            pass

    def __getitem__(self, key):
        temp_dict = pickle.loads(self._shared_array.raw)
        return temp_dict[key]

    def __iter__(self):
        return self._internal_dict.__iter__()

    def __repr__(self):
        temp_dict = pickle.loads(self._shared_array.raw)
        return repr(temp_dict)

    def __len__(self):
        return len(self._internal_dict)

    def __delitem__(self, key):
        del self._internal_dict[key]

    def clear(self):
        return self._internal_dict.clear()

    def copy(self):
        temp_dict = pickle.loads(self._shared_array.raw)
        return temp_dict.copy()

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

    def sync(self):
        try:
            self._shared_array.raw = pickle.dumps(self._internal_dict)
        except ValueError("Buffer is too small to hold the dictionary."):
            pass
