import unittest

from pysrvany import samples

from .config import *


class TestFramework(unittest.TestCase):
    def setUp(self):
        self.sf = samples.Framework()

    def tearDown(self):
        self.sf.stop()
        log_clean()

    def test(self):
        self.sf.install("pysrvany.samples.MockService", LOG_FILE, "234")
        self.sf.run()
        time.sleep(.1)
        self.assertIn("__init__", log_read())
        time.sleep(.1)
        self.assertIn("START", log_read())
        time.sleep(.1)
        self.assertIn("RUN step", log_read())
        self.sf.stop()
        time.sleep(.1)
        self.assertIn("STOP begin", log_read())
        self.assertIn("STOP end", log_read())
