from ramorm.primitives import *

class ValidationError(Exception):
    pass


class Action:
    pass


class Cascade(Action):
    pass


class SetNull(Action):
    pass


class SetDefault(Action):
    pass


class Field:
    def __init__(self, null=False, blank=False, primary_key=False, default=None, ai=False,  **kwargs):
        self.default = default
        self.null = null
        self.blank = blank
        self.primary_key = primary_key
        if ai:
            self.ai = 1
        else:
            self.ai = 0
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs.get(kwarg))

    type = object

    def validate(self, value):
        return value

    def set(self, value, field_name):
        if self.default and not value:
            return self.default
        elif self.ai and not value:
            return self.ai
        elif not self.null and not value:
            raise ValueError(f'{field_name} = {self.__class__.__name__}(null={self.null}) but value is None')
        elif not self.blank and value == '':
            raise ValueError(f'{field_name} = {self.__class__.__name__}(blank={self.blank}) but value is ""')
        elif self.null and not value:
            return None
        elif self.blank and not value:
            return ''
        elif value:
            self.validate(value)
            return self.type(value)


class IntegerField(Field):
    type = int


class TextField(Field):
    type = str


class BooleanField(Field):
    type = bool


class NullBooleanField(Field):
    type = bool


class CharField(Field):
    type = str


class JSONField(Field):
    type = dict


class ImageField(Field):
    type = bytes


class FileField(Field):
    type = bytes


class NullField(Field):
    type = None


class ForeignKey(Field):
    type = obj_link

    def __init__(self, to_model, on_delete, null=False, blank=False):
        self.to_model = to_model
        self.on_delete = on_delete
        self.null = null
        self.blank = blank

    def set(self, value, field_name):
        if not self.null and value is None:
            raise ValueError(f'{field_name} = {self.__class__.__name__}(null={self.null}) but value is None')
        elif not self.blank and value == '':
            raise ValueError(f'{field_name} = {self.__class__.__name__}(blank={self.blank}) but value is ""')
        elif self.null and value is None:
            return None
        elif self.blank and value is None:
            return ''
        elif value:
            print(value)
            return self.type(value)


class EmailField(Field):
    type = email
