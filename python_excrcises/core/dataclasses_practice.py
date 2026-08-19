from dataclasses import dataclass, field, fields
from typing import ClassVar


@dataclass
class Animal:
    name: str
    children: list = field(default_factory=list)
    some_attr: ClassVar[int] = 3
    
    def __post_init__(self):
        self.original_name = self.name
        
    @classmethod
    def from_file(cls, filename: str) -> "Animal":
        """Create an Animal from a file."""
        with open(filename) as f:
            name = f.read().strip()
        return cls(name)
    
    @staticmethod
    def is_animal(obj) -> bool:
        """Return True if the object is an Animal."""
        return isinstance(obj, Animal)
    


a = Animal("cat")
b = Animal("dog")

print(a)                    # Animal(name='cat', children=[]) - some_attr is absent
print([f.name for f in fields(Animal)])   # ['name', 'children'] - not a field

print(a.some_attr)          # 3 - readable through any instance
print(Animal.some_attr)     # 3 - and through the class itself

Animal.some_attr = 99       # change it once, everyone sees it
print(a.some_attr, b.some_attr)   # 99 99