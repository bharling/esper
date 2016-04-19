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
        self.kill_switch = multiprocessing.Event()
        self.process_switch = multiprocessing.Event()
        self.queue = multiprocessing.Queue()

    def process(self, *args):
        raise NotImplementedError

    def run(self):
        print("Starting {},  pid: {}".format(self.name, self.pid))
        while not self.kill_switch.is_set():
            # FIXME: skip processing if still busy.
            self.process_switch.wait()
            self.world._entities, self.world._components = self.queue.get()
            self.process()
            self.queue.put((self.world._entities, self.world._components))
            self.process_switch.clear()

        print("{} process ended".format(self.name))
