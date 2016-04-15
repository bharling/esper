import os
import time
import ctypes
import multiprocessing


class Remote(multiprocessing.Process):
    def __init__(self, pill=None):
        super().__init__()
        self.x = 0
        self._kill_switch = multiprocessing.Event()
        self._process_now = multiprocessing.Event()

    def process(self, n):
        def fib(num):
            if num < 2:
                return num
            return fib(num - 2) + fib(num - 1)
        return fib(n)

    def run(self):
        while not self._kill_switch.is_set():
            self._process_now.wait()
            print(self.name, "processing now...")
            print(self.name, self.pid, "result:", self.process(36))
            self._process_now.clear()

        print("{} process ended".format(self.name))


if __name__ == "__main__":
    # multiprocessing.set_start_method("spawn")

    local = multiprocessing.current_process()
    print(local.name, local.pid)

    remote = Remote()
    remote2 = Remote()
    remote.start()
    remote2.start()

    remote._process_now.set()
    remote2._process_now.set()

    time.sleep(5)

    remote._kill_switch.set()
    remote2._kill_switch.set()
