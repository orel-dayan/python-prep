
from dataclasses import dataclass, field


class MyClass:
    def __init__(self, var1: str, var2:int):
        self.var1 = var1
        self.var2 = var2
        
    def __repr__(self):
        # The __repr__ method should return a string that, when passed to eval(), would recreate the object.
        return f"MyClass(var1={self.var1!r}, var2={self.var2!r})"
    
    def __eq__(self, other):
        # The __eq__ method checks if two objects are equal based on their attributes.
        if not isinstance(other, MyClass):
            return NotImplemented
        return self.var1 == other.var1 and self.var2 == other.var2
    
    
@dataclass
class MyDataClass:
    var1: str
    var2: int

my_dataclass_instance = MyDataClass("hello", 1)

@dataclass
class Point:
    x: int
    y: int

# Python generates this for you:
# def __init__(self, x: int, y: int):
#     self.x = x
#     self.y = y

p = Point(3, 4)
print(Point(3, 4))   # Point(x=3, y=4)

assert Point(1, 2) == Point(1, 2)   # True

@dataclass(repr=False)
class Raw:
    x: int

print(Raw(3)) 

# @dataclass
# class Base:
#     name: str
#     timeout: int = 30      # has a default

# @dataclass
# class Child(Base):
#     retries: int           # no default - comes AFTER a defaulted field
# # TypeError: non-default argument 'retries' follows default argument

# # fix
# @dataclass(kw_only=True)
# class Base:
#     name: str
#     timeout: int = 30

# @dataclass(kw_only=True)
# class Child(Base):
#     retries: int = field(kw_only=True)  # no default - comes AFTER a defaulted field
    
# def __init__(self, *, name, timeout=30, retries):    # note the * separator


# Child(name="api-suite", retries=3)             # OK
# Child(retries=3, name="api-suite")             # also OK - order irrelevant
# Child(name="api-suite", retries=3, timeout=60) # OK

# Child("api-suite", 3)    # TypeError - positional arguments not allowed anymore

@dataclass
class Base:
    name: str
    timeout: int = 30

@dataclass
class Child(Base):
    retries: int = field(kw_only=True)

# generated:
# def __init__(self, name, timeout=30, *, retries): ...

Child("api-suite", 60, retries=3)          # OK - positional still works
Child("api-suite", retries=3)              # OK - timeout uses its default
Child(name="api-suite", retries=3)         # OK - keyword works too
#Child("api-suite", 60, 3)                  # TypeError - retries must be named

def demo(a, b=2, *, c):
    return a, b, c

demo(1, 2, c=3)    # OK
demo(1, c=3)       # OK
demo(1, 2, 3)      # TypeError - same error, no dataclass involved

# tags: list[str] = field(default_factory=list)
# token: str = field(default="", repr=False)
# created: datetime = field(default_factory=datetime.now, compare=False)
# retries: int = field(kw_only=True)

# repr=False: exclude from the generated __repr__ method