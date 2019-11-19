import json
import pickle
import pydoc


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
