import sys
import unittest

from pysrvany import services

from .config import *


class TestExecutable(unittest.TestCase):
    def setUp(self):
        with open("sample_script.py", "w") as f:
            f.write("""
import os
import time

while True:
    with open("sample_script.out", "w") as f:
        f.write("starting...")
    with open("sample_script.in") as fi:
        content = fi.read()
    if content == "STOP":
        break  # SIMULATE CRASH!!!
    with open("sample_script.out", "w") as f:
        f.write("running...")
    time.sleep(0.1)
""")
        with open("sample_script.in", "w") as f:
            f.write("EMPTY")
        with open("sample_script.out", "w") as f:
            f.write("EMPTY")

    def tearDown(self):
        file_remove("sample_script.py")
        file_remove("sample_script.in")
        file_remove("sample_script.out")

    def test_no_crash(self):
        s = services.Executable([sys.executable, "sample_script.py"])
        th = threading.Thread(target=s.run)
        th.start()
        time.sleep(2)
        s.stop()
        th.join()
        with open("sample_script.out") as fo:
            content = fo.read()
        self.assertIn("running...", content)

    def test_crash(self):
        s = services.Executable([sys.executable, "sample_script.py"])
        th = threading.Thread(target=s.run)
        th.start()
        time.sleep(0.2)
        with open("sample_script.in", "w") as f:
            f.write("STOP")
        time.sleep(0.1)
        with open("sample_script.in", "w") as f:
            f.write("EMPTY")
        time.sleep(2)
        with open("sample_script.out") as fo:
            content = fo.read()
        # ... respawned!
        self.assertIn("running...", content)
        s.stop()
        th.join()
