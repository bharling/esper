import multiprocessing
import pickle


class Processor:
    def __init__(self):
        self.world = None

    def process(self, *args):
        raise NotImplementedError


class ParallelProcessor(multiprocessing.Process):
    def __init__(self):
        super().__init__()
        self.world = None
        # self._local_ent = None
        # self._local_comp = None
        self.kill_switch = multiprocessing.Event()
        self.process_switch = multiprocessing.Event()
        self.sync_switch = multiprocessing.Event()
        self.queue = multiprocessing.SimpleQueue()

    def process(self, *args):
        raise NotImplementedError

    def run(self):
        print("Starting {},  pid: {}".format(self.name, self.pid))

        # self._local_ent = self.world._entities
        # self._local_comp = self.world._components

        while not self.kill_switch.is_set():
            # FIXME: skip processing if still busy.
            self.process_switch.wait()
            self.process()
            self.process_switch.clear()


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
