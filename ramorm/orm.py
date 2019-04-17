from ramorm.model import *
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
        self.__storage__ = []
        self.__indexer__ = {}

    def __check_ai__(self, model_object):
        """
        Replace AutoIncreasement field to int value
        :param model_object: Model object
        :return: Model object
        """
        for fname, field in model_object.__fields__.items():
            if field.ai:
                try:
                    next_val = field.ai(self.__indexer__[model_object.__class__.__name__][fname])
                    setattr(model_object, fname, field.ai(self.__indexer__[model_object.__class__.__name__][fname]))
                    self.__indexer__[model_object.__class__.__name__][fname] = next_val
                except KeyError:
                    setattr(model_object, fname, 0)
                    self.__indexer__[model_object.__class__.__name__][fname] = 0
        return model_object

    def __single_pk__(self, model_object):
        """
        Check Model object for single Primary Key field
        :param model_object: Model object
        :return: Model object
        """
        pk_count = 0
        for fname, field in model_object.__fields__.items():
            if field.primary_key:
                pk_count += 1
        if pk_count > 1:
            raise AttributeError('Multiple PK fields')
        return model_object

    @__Decorators.validate_input_model
    def push(self, model_object):
        """
        Add objects to database
        :param model_object: Model object
        :return: Model object
        """
        try:
            self.__indexer__[model_object.__class__.__name__]
        except KeyError:
            self.__indexer__[model_object.__class__.__name__] = {}
        self.__check_ai__(model_object)
        self.__single_pk__(model_object)
        self.__storage__.append(model_object)
        return model_object

    @__Decorators.validate_input_model
    def get(self, model_class, **kwargs) -> 'Model':
        """
        Get single first found object in database which falls under params passed in kwargs
        :param model_class: Model
        :param kwargs: model field values
        :return: Model object
        """
        copy = self.__storage__.copy()
        for n, item in enumerate(copy):
            if isinstance(item, model_class):
                for_trigger = len(kwargs)
                counter = 0
                for attr, value in kwargs.items():
                    if getattr(item, attr, None) == value:
                        counter += 1
                    elif len(attr.split('__')) > 1:
                        if attr.split('__')[-1] == 'gt':
                            if getattr(item, '__'.join(attr.split('__')[:-1]), None) > value:
                                counter += 1
                        elif attr.split('__')[-1] == 'lt':
                            if getattr(item, '__'.join(attr.split('__')[:-1]), None) < value:
                                counter += 1
                        elif attr.split('__')[-1] == 'gte':
                            if getattr(item, '__'.join(attr.split('__')[:-1]), None) >= value:
                                counter += 1
                        elif attr.split('__')[-1] == 'lte':
                            if getattr(item, '__'.join(attr.split('__')[:-1]), None) <= value:
                                counter += 1
                if for_trigger == counter:
                    return item
        return None

    @__Decorators.validate_input_model
    def filter(self, model_class, **kwargs) -> list:
        """
        Receive list of objects found in database according params passed
        :param model_class: Model
        :param kwargs: filter parameters
        :return: list of model objects
        """
        found = []
        copy = self.__storage__.copy()
        for n, item in enumerate(copy):
            if isinstance(item, model_class):
                for_trigger = len(kwargs)
                counter = 0
                for attr, value in kwargs.items():
                    if getattr(item, attr, None) == value:
                        counter += 1
                    elif len(attr.split('__')) > 1:
                        if attr.split('__')[-1] == 'gt':
                            if getattr(item, '__'.join(attr.split('__')[:-1]), None) > value:
                                counter += 1
                        elif attr.split('__')[-1] == 'lt':
                            if getattr(item, '__'.join(attr.split('__')[:-1]), None) < value:
                                counter += 1
                        elif attr.split('__')[-1] == 'gte':
                            if getattr(item, '__'.join(attr.split('__')[:-1]), None) >= value:
                                counter += 1
                        elif attr.split('__')[-1] == 'lte':
                            if getattr(item, '__'.join(attr.split('__')[:-1]), None) <= value:
                                counter += 1
                if for_trigger == counter:
                    found.append(item)
        return found

    @__Decorators.validate_input_model
    def delete(self, node_class, **kwargs):
        """
        Delete objects in database according to Model and params
        :param node_class: Model
        :param kwargs: params
        :return:
        """
        changes_made = False
        for item in self.filter(node_class, **kwargs):
            ind = self.__storage__.index(item)
            self.__storage__.pop(ind)
            changes_made = True
        return changes_made

    def drop(self):
        """
        Delete all data in database
        :return:
        """
        self.__storage__ = []
        return self.__storage__

