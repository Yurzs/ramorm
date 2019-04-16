from primitives import *


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
    def __init__(self, null=False, blank=False, primary_key=False, default=None, **kwargs):
        self.default = default
        self.null = null
        self.blank = blank
        self.primary_key = primary_key
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs.get(kwarg))

    type = object

    def validate(self, value):
        return

    def set(self, value, field_name):
        if self.default and not value:
            return self.default
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

    def __int__(self):
        return self

    def __eq__(self, other):
        return self == other

    def __gt__(self, other):
        return self > other

    def __lt__(self, other):
        return self < other


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


class EmailField(Field):
    type = email
