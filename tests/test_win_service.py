import sys
import unittest

try:
    import winreg
    WIN_OS = True
except ModuleNotFoundError:
    WIN_OS = False

try:
    from pysrvany import win_service
except ModuleNotFoundError:
    if WIN_OS:
        raise

from .config import *


@unittest.skipIf(not WIN_OS, "only on Windows")
class TestCliInstall(unittest.TestCase):
    SERVICE_NAME = "Test_PYSRVANY"

    def tearDown(self):
        subprocess_check_call(["sc", "delete", self.SERVICE_NAME], ignore_errors=True)

    def test_install_compose_command_line(self):
        subprocess_check_call([
            sys.executable, "pysrvany_cli.py", "install_exe", self.SERVICE_NAME,
            "python", "dummy_script.py", "other_param", "param with space"
        ])
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        with winreg.OpenKey(reg, "SYSTEM\CurrentControlSet\Services\Test_PYSRVANY\Parameters") as key:
            value, value_type = winreg.QueryValueEx(key, "class_args")
        self.assertEqual(value, (
            '{"args": [["python", "dummy_script.py", "other_param", "param with space"]], "kwargs": {}}'
        ))


@unittest.skipIf(not WIN_OS, "only on Windows")
class TestWinServiceInstallStartStop(unittest.TestCase):
    def assertLogged(self, msg):
        self.assertIn(msg, log_read())

    def tearDown(self):
        subprocess_check_call(["sc", "stop", "Test_PYSRVANY"], ignore_errors=True)
        subprocess_check_call(["sc", "delete", "Test_PYSRVANY"], ignore_errors=True)
        log_clean()

    def test_install(self):
        win_service.WinService.install("pysrvany.samples.MockService", "Test_PYSRVANY", LOG_FILE)
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        with winreg.OpenKey(reg, "SYSTEM\CurrentControlSet\Services\Test_PYSRVANY\Parameters") as key:
            value, value_type = winreg.QueryValueEx(key, "class_path")
        self.assertEqual(value, "pysrvany.samples.MockService")

    def test_start(self):
        win_service.WinService.install("pysrvany.samples.MockService", "Test_PYSRVANY", LOG_FILE)
        subprocess_check_call(["sc", "start", "Test_PYSRVANY"])
        time.sleep(.5)
        self.assertLogged("START\n")

    def test_stop(self):
        win_service.WinService.install("pysrvany.samples.MockService", "Test_PYSRVANY", LOG_FILE)
        subprocess_check_call(["sc", "start", "Test_PYSRVANY"])
        subprocess_check_call(["sc", "stop", "Test_PYSRVANY"])
        self.assertLogged("STOP begin\n")
        self.assertLogged("RUN end\n")
        self.assertLogged("STOP end\n")
