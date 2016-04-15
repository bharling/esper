import multiprocessing


class Processor:
    def __init__(self):
        self.world = None

    def process(self, *args):
        raise NotImplementedError


class ParallelProcessor(multiprocessing.Process):
    def __init__(self, daemon=False):
        super().__init__()
        self.world = None
        self.daemon = daemon
        self._kill_switch = multiprocessing.Event()
        self._process_now = multiprocessing.Event()

    def process(self, *args):
        raise NotImplementedError

    def run(self):
        print("Starting {},  pid: {}".format(self.name, self.pid))
        while not self._kill_switch.is_set():
            self._process_now.wait()
            self.process()
            self._process_now.clear()

        print("{} process ended".format(self.name))
