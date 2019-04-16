from model import *
from functools import wraps


class Orm:
    class __Decorators(object):

        @classmethod
        def validate_input_model(cls, func):

            def check(obj):
                if isinstance(obj, type):
                    if issubclass(obj, Model):
                        return True
                    else:
                        raise ValueError(f'{obj} is not a subclass of Model')
                elif issubclass(obj.__class__, Model):
                    return True
                else:
                    raise ValueError(f'{obj.__class__} is not a subclass of Model')

            @wraps(func)
            def wrapper(self, *args, **kwargs):
                print(self, args, kwargs)
                if not kwargs.get('model_class', None):
                    for obj in args:
                        if check(obj):
                            return func(self, obj, **kwargs)
                else:
                    if check(kwargs.get('model_class')):
                        return func(self, **kwargs)
            return wrapper

    def __init__(self, database_name: str):
        if not isinstance(database_name, str):
            raise TypeError(f'Database name should be string')
        self.__database_name__ = str(database_name)
        self.__storage___ = []


    @__Decorators.validate_input_model
    def push(self, model_object):
        self.__storage___.append(model_object)
        return model_object

    @__Decorators.validate_input_model
    def get(self, model_class, **kwargs):
        copy = self.__storage___.copy()
        for n, item in enumerate(copy):
            if isinstance(item, model_class):
                for_trigger = len(kwargs)
                counter = 0
                for attr, value in kwargs.items():
                    if getattr(item, attr, None) == value:
                        counter += 1
                if for_trigger == counter:
                    return item
        return None

    @__Decorators.validate_input_model
    def filter(self, model_class, **kwargs):
        found = []
        copy = self.__storage___.copy()
        for n, item in enumerate(copy):
            if isinstance(item, model_class):
                for_trigger = len(kwargs)
                counter = 0
                for attr, value in kwargs.items():
                    if getattr(item, attr, None) == value:
                        counter += 1
                if for_trigger == counter:
                    found.append(item)
        return found

    @__Decorators.validate_input_model
    def delete(self, node_class, **kwargs):
        for item in self.filter(node_class, **kwargs):
            ind = self.__storage___.index(item)
            self.__storage___.pop(ind)
        return True

    def drop(self):
        self.__storage___ = []
        return self.__storage___

