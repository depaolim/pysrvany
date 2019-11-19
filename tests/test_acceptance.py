import sys
import unittest

from .config import *


@unittest.skipIf(sys.platform != 'win32', 'only on win32 platform')
class TestAcceptance(unittest.TestCase):
    def setUp(self):
        with open("sample_script.py", "w") as f:
            f.write("""
import sys

with open(sys.argv[2], "a") as f:
    f.write("#".join(sys.argv))
""")

    def tearDown(self):
        subprocess_check_call(["sc", "stop", "Test_PYSRVANY"], ignore_errors=True)
        time.sleep(1)
        subprocess_check_call(["sc", "delete", "Test_PYSRVANY"], ignore_errors=True)
        file_remove("sample_script.py")
        file_remove("sample_script.out")
        log_clean()

    def test_executable(self):
        subprocess_check_call([
            "python", "pysrvany_cli.py", "install_exe", "Test_PYSRVANY",
            "python", "sample_script.py", "hello it is me", "sample_script.out",
            "--pysrvany-cwd", os.path.dirname(os.path.abspath("sample_script.py"))
        ])
        subprocess_check_call(["sc", "start", "Test_PYSRVANY"])
        time.sleep(1)
        with open("sample_script.out") as fo:
            content = fo.read()
        self.assertIn("sample_script.py#hello it is me", content)

    def test_custom_class(self):
        subprocess_check_call([
            "python", "pysrvany_cli.py", "install_class", "Test_PYSRVANY",
            "pysrvany.samples.MockService", LOG_FILE, "arg2"
        ])
        subprocess_check_call(["sc", "start", "Test_PYSRVANY"])
        self.assertIn("__init__", log_read())
        time.sleep(.1)
        self.assertIn("START", log_read())
        time.sleep(.1)
        self.assertIn("RUN step", log_read())
        subprocess_check_call(["sc", "stop", "Test_PYSRVANY"], ignore_errors=True)
        time.sleep(.1)
        self.assertIn("STOP begin", log_read())
        self.assertIn("STOP end", log_read())
