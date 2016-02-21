import multiprocessing


class Processor:
    def __init__(self):
        self.world = None

    def process(self, *args):
        raise NotImplementedError


# TODO: inherrit from proper MultiProcessing class.
class ParallelProcessor(multiprocessing.Process):
    def __init__(self):
        super().__init__()
        self.world = None

    def process(self, *args):
        raise NotImplementedError
