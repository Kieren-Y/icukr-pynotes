from typing import List
from dataclasses import dataclass, field
from dis import dis
import inspect

class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def __repr__(self):
        return "User(name='%s', age=%d)"%(self.name, self.age)
    

    def __eq__(self, other):
        return self.name == other.name and self.age == other.age


@dataclass(order=True)
class EUser:
    name: str = field(compare=False)
    age: int



if __name__ == "__main__":
    namu = EUser("Manu", 32)
    other_namu = EUser("Manu", 18)
    kieren = EUser("kieren", 26)
    origin_namu = User("Manu", 17)
    print(namu, kieren)
    print(namu == other_namu)
    print(kieren > namu)
    # print(dis(EUser))
    print(inspect.getmembers(origin_namu))