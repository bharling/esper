import multiprocessing


class Processor:
    def __init__(self):
        self.world = None

    def process(self, *args):
        raise NotImplementedError


class ParallelProcessor(multiprocessing.Process):
    def __init__(self):
        super().__init__()
        self.world = None
        self._local_ent = None
        self._local_comp = None
        self.kill_switch = multiprocessing.Event()
        self.process_switch = multiprocessing.Event()
        self.sync_switch = multiprocessing.Event()
        self.queue = multiprocessing.SimpleQueue()

    def process(self, *args):
        raise NotImplementedError

    def run(self):
        print("Starting {},  pid: {}".format(self.name, self.pid))

        self._local_ent = self.world._entities
        self._local_comp = self.world._components

        while not self.kill_switch.is_set():
            # FIXME: skip processing if still busy.
            self.process_switch.wait()
            self.process()
            self.process_switch.clear()
