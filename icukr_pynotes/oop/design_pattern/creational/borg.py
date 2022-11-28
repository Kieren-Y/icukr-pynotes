"""
*source url: 
https://github.com/faif/python-patterns/blob/master/patterns/creational/borg.py
sington behavior, but instead of having only one instance of a class.
multiple instances share the same state.
"""

from typing import Dict

class Borg:
    _shared_states: Dict[str, str] = {}
    
    def __init__(self) -> None:
        self.__dict__ = self._shared_states

class YourBorg(Borg):
    def __init__(self, state: str = None) -> None:
        super().__init__()
        if state:
            self.state = state
        if not hasattr(self, "state"):
            self.state = "Init"
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(state={self.state})"
    

def main():
    rb1 = YourBorg("Idle")
    rb2 = YourBorg("Running")
    print("rb1", rb1)
    print("rb2", rb2)


if __name__ == "__main__":
    main()
        