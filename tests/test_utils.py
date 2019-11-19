from io import FileIO
import json
import unittest
from unittest import mock

from pysrvany import utils


class TestInstall(unittest.TestCase):
    def test_init(self):
        call = mock.Mock()
        utils.Install(call)
        self.assertFalse(call.mock_calls)

    def test_ctor(self):
        call = mock.Mock()
        ins = utils.Install(call)
        ins.parse_constructor("sample_ctor")
        self.assertEqual(call.constructor, "sample_ctor")

    def test_args(self):
        call = mock.Mock(args=[])
        ins = utils.Install(call)
        ins.parse_arguments("arg1", "arg2")
        self.assertEqual(call.mock_calls, [mock.call.append_arg('arg1'), mock.call.append_arg('arg2')])

    def test_kwargs(self):
        call = mock.Mock(kwargs={})
        ins = utils.Install(call)
        ins.parse_arguments("--pysrvany-myname", "myvalue")
        self.assertEqual(call.mock_calls, [mock.call.append_kwarg('myname', 'myvalue')])

    def test_arguments(self):
        call = mock.Mock(args=[], kwargs={})
        ins = utils.Install(call)
        ins.parse_arguments("arg1", "--pysrvany-myname", "myvalue", "arg2")
        self.assertEqual(call.mock_calls, [
            mock.call.append_arg('arg1'), mock.call.append_kwarg('myname', 'myvalue'), mock.call.append_arg('arg2')
        ])


class MockAction(utils.Install):
    NAME = "install_mock"

    def parse(self, *args):
        super().parse_constructor("my_packg.ctor")
        super().parse_arguments(*args)


class TestArgumentsParse(unittest.TestCase):
    def test_custom(self):
        call = utils.Call()
        parser = utils.Parser(call)
        parser.register_action(MockAction)
        parser.parse(
            "install_class", "sample_name", "class_path", "arg1", "-i", "--pysrvany-cwd", "base_dir")
        self.assertEqual(call.name, "sample_name")
        self.assertEqual(call.constructor, "class_path")
        self.assertSequenceEqual(call.args, ("arg1", "-i", ))
        self.assertEqual(call.kwargs, {"cwd": "base_dir"})

    def test_exe_minimal(self):
        call = utils.Call()
        parser = utils.Parser(call)
        parser.register_action(MockAction)
        parser.parse("install_mock", "sample_name", "exe_path", "arg1")
        self.assertEqual(call.name, "sample_name")
        self.assertEqual(call.constructor, "my_packg.ctor")
        self.assertSequenceEqual(call.args, ("exe_path", "arg1", ))
        self.assertFalse(call.kwargs)

    def test_exe_cwd(self):
        call = utils.Call()
        parser = utils.Parser(call)
        parser.register_action(MockAction)
        parser.parse("install_mock", "sample_name", "exe_path", "arg1", "-i", "--pysrvany-cwd", "base_dir")
        self.assertEqual(call.name, "sample_name")
        self.assertEqual(call.constructor, "my_packg.ctor")
        self.assertSequenceEqual(call.args, ("exe_path", "arg1", "-i", ))
        self.assertEqual(call.kwargs, {"cwd": "base_dir"})


class TestClassPath(unittest.TestCase):
    def test_serialize(self):
        path = utils.ClassPath.serialize(utils.ClassPath)
        self.assertEqual(path, "pysrvany.utils.ClassPath")

    def test_locate(self):
        cls = utils.ClassPath.locate("pysrvany.utils.ClassPath")
        self.assertEqual(cls, utils.ClassPath)


class TestShell(unittest.TestCase):
    def test_serialize_class(self):
        service_class_path = utils.Shell.serialize_class(utils.Shell)
        self.assertEqual(service_class_path, "pysrvany.utils.Shell")

    def test_serialize_args(self):
        service_class_args = utils.Shell.serialize_args(
            ["python", "/sample_script.py", "hello it is me", "/tmp/sample_script.out"])
        self.assertEqual(service_class_args, (
            '{"args": [["python", "/sample_script.py", "hello it is me", "/tmp/sample_script.out"]], "kwargs": {}}'
        ))

    def test_serialize_args_and_kwargs(self):
        service_class_args = utils.Shell.serialize_args(
            ["python", "/sample_script.py", "hello it is me", "/tmp/sample_script.out"],
            cwd='sample_dir'
        )
        self.assertEqual(service_class_args, (
            '{'
            '"args": [["python", "/sample_script.py", "hello it is me", "/tmp/sample_script.out"]], '
            '"kwargs": {"cwd": "sample_dir"}'
            '}'
        ))

    def test_serialize_args_problem(self):
        self.assertRaises(TypeError, utils.Shell.serialize_args, "arg1", utils.Shell)

    def test_create(self):
        obj = utils.Shell.create("io.FileIO", json.dumps({'args': [__file__], 'kwargs': {}}))
        obj.close()
        self.assertEqual(obj.__class__, FileIO)
        self.assertIn("test_utils.py", obj.name)  # yes, it's me!

    def test_idempotent(self):
        obj = utils.Shell.create("io.FileIO", utils.Shell.serialize_args(__file__))
        obj.close()
        self.assertEqual(obj.__class__, FileIO)
        self.assertIn("test_utils.py", obj.name)  # yes, it's me!
