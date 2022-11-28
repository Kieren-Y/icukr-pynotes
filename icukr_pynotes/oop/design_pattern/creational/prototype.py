
from __future__ import annotations

from typing import Dict, Any

class Prototype:
    
    def __init__(self, value: str = "default", **attr):
        self.value = value
        self.__dict__.update(attr)
    
    def clone(self, **attrs: Dict):
        new_object = self.__class__(**self.__dict__)
        new_object.__dict__.update(attrs)
        return new_object
        

class PrototypeDispatcher:
    def __init__(self):
        self.objects = {}
    
    def register(self, name: str, obj: Any) -> None:
        self.objects[name] = obj
    
    def unregister(self, name: str) -> None:
        del self.objects[name]
    
    def get_objects(self) -> Dict[str, Any]:
        return self.objects


def main():
    dispatcher = PrototypeDispatcher()
    prototype = Prototype()
    d = prototype.clone()
    a = prototype.clone(value='a-value', category='a')
    b = a.clone(value='b-value', is_checked=True)
    dispatcher.register('objecta', a)
    dispatcher.register('objectb', b)
    dispatcher.register('objectd', d)
    print([{n: p.value} for n, p in dispatcher.get_objects().items()])
    print(b.category, b.is_checked)


if __name__ == "__main__":
    main()