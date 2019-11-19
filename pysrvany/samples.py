import os
import threading
import time

from . import utils


class MockService:
    """ Simple Service, just for test and documentation"""
    def __init__(self, log_path, *args):
        self._log_path = log_path
        self._trace("__init__", log_path, *args)
        self.is_running = threading.Event()

    def _trace(self, *msgs):
        with open(self._log_path, "a") as fo:
            fo.write("{}.{}: {}\n".format(os.getpid(), threading.get_ident(), " - ".join(msgs)))

    def run(self):
        self._trace("START")
        self.is_running.set()
        self._trace("RUN begin")
        while self.is_running.is_set():
            # do some work...
            time.sleep(.1)
            self._trace("RUN step")
        self._trace("RUN end")

    def stop(self):
        # clean up...
        self.is_running.clear()
        self._trace("STOP begin")
        time.sleep(.1)
        self._trace("STOP end")


class Framework:
    """ Simple Framework, just for test and documentation"""
    SERVICE_SHELL = utils.Shell

    def __init__(self):
        self._storage = None
        self._service = None
        self._thread = None

    def install(self, service_class_path, *args, **kwargs):
        self._storage = service_class_path, self.SERVICE_SHELL.serialize_args(*args, **kwargs)

    def run(self):
        self._service = self.SERVICE_SHELL.create(*self._storage)
        self._thread = threading.Thread(target=self._service.run)
        self._thread.start()

    def stop(self):
        self._service.stop()
        self._thread.join()
