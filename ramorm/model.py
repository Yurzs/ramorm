from ramorm.fields import *
import re


class Model:
    class Meta:
        unique_together = list()

    def __init__(self, **kwargs):
        self.__fields__ = {}
        for attr, item in self.__class__.__dict__.items():
            if not re.match('__[A-z]+__', attr) and issubclass(item.__class__, Field):
                self.__fields__[attr] = item
                if isinstance(item, ForeignKey):
                    setattr(self, attr, item.set(kwargs.get(attr), attr))
                    setattr(self, attr + '__id', kwargs.get(attr))
                else:
                    setattr(self, attr, item.set(kwargs.get(attr), attr))

    @property
    def pk(self):
        for fname, field in self.__fields__.items():
            if field.primary_key:
                return getattr(self, fname)
        return
