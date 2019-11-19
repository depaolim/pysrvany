import json
import pickle
import pydoc


class Call:
    def __init__(self):
        self.name = None
        self.constructor = None
        self.args = []
        self.kwargs = {}

    def append_arg(self, arg):
        self.args.append(arg)

    def append_kwarg(self, name, value):
        self.kwargs[name] = value


class Install:
    PREFIX = "--pysrvany-"

    def __init__(self, call):
        self.call = call

    def parse_constructor(self, constructor):
        self.call.constructor = constructor

    def parse_arguments(self, *args):
        if not args:
            return
        arg = args[0]
        try:
            pre_prefix, name = arg.split(self.PREFIX)
            assert not pre_prefix
            self.call.append_kwarg(name, args[1])
            args = args[2:]
        except ValueError:
            self.call.append_arg(arg)
            args = args[1:]
        self.parse_arguments(*args)


class InstallClass(Install):
    NAME = "install_class"

    def parse(self, constructor, *args):
        self.parse_constructor(constructor)
        self.parse_arguments(*args)


class Parser:
    def __init__(self, call):
        self.call = call
        self.actions = {}
        self.register_action(InstallClass)
        self.action = None

    def register_action(self, cls):
        self.actions[cls.NAME] = cls

    def parse_action(self, token):
        self.action = self.actions[token](self.call)

    def parse_name(self, token):
        self.call.name = token

    def parse(self, action, name, *args):
        self.parse_action(action)
        self.parse_name(name)
        self.action.parse(*args)


class ClassPath:
    @staticmethod
    def serialize(class_object):
        module_name = pickle.whichmodule(class_object, class_object.__name__)
        return module_name + "." + class_object.__name__

    @staticmethod
    def locate(class_path):
        return pydoc.locate(class_path)


class Shell:
    @staticmethod
    def _args_join(args_list):
        return json.dumps(args_list)

    @staticmethod
    def _args_split(args_str):
        return json.loads(args_str)

    @classmethod
    def serialize_class(cls, service_class):
        return ClassPath.serialize(service_class)

    @classmethod
    def serialize_args(cls, *args, **kwargs):
        return cls._args_join({'args': args, 'kwargs': kwargs})

    @classmethod
    def create(cls, service_class_path, service_class_args):
        service_class = ClassPath.locate(service_class_path)
        init = cls._args_split(service_class_args)
        return service_class(*init['args'], **init['kwargs'])
