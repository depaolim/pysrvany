from io import FileIO
import json
import unittest

from pysrvany.utils import ClassPath, Shell


class TestClassPath(unittest.TestCase):
    def test_serialize(self):
        path = ClassPath.serialize(ClassPath)
        self.assertEqual(path, "pysrvany.utils.ClassPath")

    def test_locate(self):
        cls = ClassPath.locate("pysrvany.utils.ClassPath")
        self.assertEqual(cls, ClassPath)


class TestShell(unittest.TestCase):
    def test_serialize_class(self):
        service_class_path = Shell.serialize_class(Shell)
        self.assertEqual(service_class_path, "pysrvany.utils.Shell")

    def test_serialize_args(self):
        service_class_args = Shell.serialize_args(
            ["python", "/sample_script.py", "hello it is me", "/tmp/sample_script.out"])
        self.assertEqual(service_class_args, (
            '{"args": [["python", "/sample_script.py", "hello it is me", "/tmp/sample_script.out"]], "kwargs": {}}'
        ))

    def test_serialize_args_and_kwargs(self):
        service_class_args = Shell.serialize_args(
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
        self.assertRaises(TypeError, Shell.serialize_args, "arg1", Shell)

    def test_create(self):
        obj = Shell.create("io.FileIO", json.dumps({'args': [__file__], 'kwargs': {}}))
        obj.close()
        self.assertEqual(obj.__class__, FileIO)
        self.assertIn("test_utils.py", obj.name)  # yes, it's me!

    def test_idempotent(self):
        obj = Shell.create("io.FileIO", Shell.serialize_args(__file__))
        obj.close()
        self.assertEqual(obj.__class__, FileIO)
        self.assertIn("test_utils.py", obj.name)  # yes, it's me!
