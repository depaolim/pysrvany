import os
import subprocess
import time
import threading

LOG_FILE = os.path.join(os.path.dirname(__file__), "log.log")


def file_remove(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


def subprocess_check_call(args, ignore_errors=False):
    try:
        subprocess.check_call(args)
        time.sleep(0.5)
    except subprocess.CalledProcessError:
        if not ignore_errors:
            raise


def log(*msgs):
    with open(LOG_FILE, "a") as fo:
        fo.write("{}.{}: {}\n".format(os.getpid(), threading.get_ident(), " - ".join(msgs)))


def log_read():
    try:
        with open(LOG_FILE) as fi:
            return fi.read()
    except FileNotFoundError:
        pass


def log_clean():
    file_remove(LOG_FILE)
