import subprocess
import threading
import time


class Executable:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.is_running = threading.Event()
        self.p = None

    def run(self):
        self.is_running.set()
        while self.is_running.is_set():
            self.p = subprocess.Popen(*self.args, **self.kwargs)
            self.p.wait()
            time.sleep(1)

    def stop(self):
        assert self.p
        self.is_running.clear()
        self.p.kill()
