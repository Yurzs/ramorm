from fields import *
import re


class Model:
    class Meta:
        pass

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

