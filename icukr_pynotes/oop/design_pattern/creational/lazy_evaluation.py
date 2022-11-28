"""
Lazily-evaluated property pattern in Python.

when first read the attribite, will excute the function
    second, will get attr directly
"""

import functools
from typing import Callable
import time



class lazy_property:
    def __init__(self, function):
        self.function = function
        # update function attribute to self object.
        functools.update_wrapper(self, function)
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        val = self.function(instance)
        instance.__dict__[self.function.__name__] = val
        return val


def lazy_property_func(func: Callable):
    """A lazy property decorator."""
    attr = f"_lazy_{func.__name__}"

    @property
    def _lazy_property(self):
        if not hasattr(self, attr):
            setattr(self, attr, func(self))
        return getattr(self, attr)

    return _lazy_property


class Person:
    def __init__(self, name, occupation):
        self.name = name
        self.occupation = occupation
        self.call_count2 = 0
    
    @lazy_property
    def relatives(self):
        print("run relatives method...")
        return "get relative from db. need net io."
    
    @lazy_property_func
    def parents(self):
        print("run parents method...")
        self.call_count2 += 1
        return "fetch parents from database."




def main():
    """
    >>> Jhon = Person('Jhon', 'Coder')
    >>> Jhon.name
    'Jhon'
    >>> Jhon.occupation
    'Coder'
    # Before we access `relatives`
    >>> sorted(Jhon.__dict__.items())
    [('call_count2', 0), ('name', 'Jhon'), ('occupation', 'Coder')]
    >>> Jhon.relatives
    'Many relatives.'
    # After we've accessed `relatives`
    >>> sorted(Jhon.__dict__.items())
    [('call_count2', 0), ..., ('relatives', 'Many relatives.')]
    >>> Jhon.parents
    'Father and mother'
    >>> sorted(Jhon.__dict__.items())
    [('_lazy__parents', 'Father and mother'), ('call_count2', 1), ..., ('relatives', 'Many relatives.')]
    >>> Jhon.parents
    'Father and mother'
    >>> Jhon.call_count2
    1
    """
    
if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
    
    
    