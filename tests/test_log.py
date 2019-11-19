import unittest

from .config import *


class TestLog(unittest.TestCase):
    def tearDown(self):
        log_clean()

    def test(self):
        self.assertFalse(log_read())
        log("START")
        self.assertIn("START", log_read())
