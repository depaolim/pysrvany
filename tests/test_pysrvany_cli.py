import unittest
from unittest import mock

import pysrvany_cli


@mock.patch("pysrvany_cli.get_win_service")
class TestCliInstall(unittest.TestCase):
    def test_install_exe(self, mock_gws):
        pysrvany_cli.main(
            "install_exe", "the_service_name",
            "python", "/sample_script.py", "hello it is me", "/tmp/sample_script.out")
        self.assertEqual(mock_gws.mock_calls, [mock.call(), mock.call().install(
            "pysrvany.services.Executable", "the_service_name",
            ["python", "/sample_script.py", "hello it is me", "/tmp/sample_script.out"]
        )])

    def test_install_exe_with_cwd(self, mock_gws):
        pysrvany_cli.main(
            "install_exe", "the_service_name",
            "python", "/sample_script.py", "hello it is me", "/tmp/sample_script.out",
            '--pysrvany-cwd', '/root/home/pippo'
        )
        self.assertEqual(mock_gws.mock_calls, [mock.call(), mock.call().install(
            "pysrvany.services.Executable", "the_service_name",
            ["python", "/sample_script.py", "hello it is me", "/tmp/sample_script.out"],
            cwd='/root/home/pippo'
        )])

    def test_install_class(self, mock_gws):
        pysrvany_cli.main(
            "install_class", "the_service_name",
            "pysrvany.samples.MockService", "hello", "I'm a serialized argument", "list")
        self.assertEqual(mock_gws.mock_calls, [mock.call(), mock.call().install(
            "pysrvany.samples.MockService", "the_service_name",
            "hello", "I\'m a serialized argument", "list"
        )])

    def test_dexd(self, mock_gws):
        pysrvany_cli.main(
            "install_exe", "DexD_pysrvany", "DexD.exe", "5001", "-i", "DexD.ini", "-o", "logs\\DexD_pysrvany.log",
            "--pysrvany-cwd", "c:\\Dex"
        )
        self.assertEqual(mock_gws.mock_calls, [mock.call(), mock.call().install(
            "pysrvany.services.Executable", "DexD_pysrvany", [
                'DexD.exe', '5001', '-i', 'DexD.ini', '-o', 'logs\\DexD_pysrvany.log'],
            cwd='c:\\Dex'
        )])
