
from typing import T, Callable, Dict


class Dog:
    def __init__(self) -> None:
        self.name = "dog"
    
    def bark(self) -> str:
        return "woof!"


class Cat:
    def __init__(self) -> None:
        self.name = "cat"
    
    def meow(self):
        return "meow!"


class Human:
    def __init__(self) -> None:
        self.name = "human"
    
    def speak(self) -> str:
        return "hello world!"


class Car:
    def __init__(self) -> None:
        self.name = "car"
    
    def make_noise(self, octane_level: int) -> str:
        return f"vroom{'!' * octane_level}"


class Adapter:
    def __init__(self, obj: T, **adapter_methods: Dict[str, Callable]):
        self.obj = obj
        self.__dict__.update(adapter_methods)
    
    def __getattr__(self, attr: str):
        """All non-adapted calls are passed to the object."""
        return getattr(self.obj, attr)
    
    def original_dict(self) -> Dict:
        return self.obj.__dict__
    

def main():
    objects = []
    dog = Dog()
    print(dog.__dict__)
    
    objects.append(Adapter(dog, make_noise=dog.bark))
    print(objects[0].__dict__['obj'], objects[0].__dict__['make_noise'])
    print(objects[0].original_dict())
    
    cat = Cat()
    objects.append(Adapter(cat, make_noise=cat.meow))
    human = Human()
    objects.append(Adapter(human, make_noise=human.speak))
    car = Car()
    objects.append(Adapter(car, make_noise=lambda: car.make_noise(3)))
    for obj in objects:
        print("A {0} goes {1}".format(obj.name, obj.make_noise()))
        

if __name__ == "__main__":
    main()