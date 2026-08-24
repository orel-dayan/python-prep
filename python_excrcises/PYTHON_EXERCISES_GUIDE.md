# Python Exercises Guide

מסמך זה מסביר את נושאי הליבה של התיקייה `python_excrcises` (ראו גם `README.md`
לרשימת כל הקבצים ב-`core/` וב-`automation_examples/`):

- context managers
- decorators
- retry logic
- subprocess calls
- safe/portable patterns
- OOP (classes, inheritance, abstraction)

---

## 1) Context managers

Context manager מאפשר לנו להגדיר setup ו-teardown סביב בלוק קוד:

```python
with open("example.txt", "w") as f:
    f.write("hello")
```

בפנים, Python קורא אוטומטית ל:

- `__enter__()` לפני הכניסה לבלוק
- `__exit__()` אחרי יציאה מהבלוק, גם אם יש חריגה

### דוגמה טובה

```python
from contextlib import contextmanager


@contextmanager
def temporary_override(config, key, temp_value):
    had_key = key in config
    original = config.get(key)
    config[key] = temp_value
    try:
        yield config
    finally:
        if had_key:
            config[key] = original
        else:
            config.pop(key, None)
```

(המימוש המלא, כולל דוגמה נוספת ל-context manager שסוגר חיבור DB, נמצא ב-
`core/context_managers.py`.)

### למה זה חשוב?

- מבטיח ניקוי משאבים
- מונע דליפות זיכרון / פתיחת קבצים
- מאפשר rollback של מצב

### דוגמה שימוש

```python
settings = {"timeout": 30}

with temporary_override(settings, "timeout", 5):
    print(settings["timeout"])  # 5

print(settings["timeout"])  # 30
```

---

## 2) Decorators

Decorator הוא פונקציה שמקבלת פונקציה אחרת ומחזירה פונקציה חדשה.

### דוגמה בסיסית

```python
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)

    return wrapper
```

### שימוש

```python
@log_calls
def greet(name):
    return f"Hello {name}"


print(greet("Alice"))
```

### למה decorators שימושיים?

- logging
- retries
- validation
- rate limiting
- caching
- access control

### דוגמה מפתחת: retry

```python
import time


def retry(times=3, delay=0.2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_error = exc
                    if attempt == times:
                        raise
                    time.sleep(delay)
            raise last_error

        return wrapper

    return decorator
```

זה שימושי לרשת, API, חיבורי תקשורת, ופעולות שיכולות להיכשל זמנית.

הדוגמה למעלה היא הגרסה הפשוטה, להבנת העיקרון. הגרסה בפועל בקוד
(`automation_examples/utils/decorators.py`) מוסיפה `exponential backoff`,
בחירת חריגות ספציפיות (`exceptions=...`), ו-`functools.wraps` כדי לשמר את
שם/תיעוד הפונקציה המקורית — וגם דקורטורים נוספים: `timer`, `rate_limit`,
`max_calls`, `log_exceptions`, `cached`.

---

## 3) subprocess

`subprocess` משמש להרצת תהליכים חיצוניים, למשל:

- ping
- systemctl
- ls
- curl
- python script אחר

### דוגמה תקנית

```python
import subprocess

result = subprocess.run(
    ["ping", "-c", "2", "8.8.8.8"],
    capture_output=True,
    text=True,
    timeout=10,
    check=False,
)
print(result.returncode)
print(result.stdout)
```

### למה זה חשוב?

- ביצוע פקודות מערכת בצורה בטוחה
- אפשר לשלוט על timeout
- שימוש ב-list מונע בעיות של shell injection

### דוגמה לא בטוחה

```python
subprocess.run("rm -rf /", shell=True)
```

זה מסוכן כי ה-shell מפרש את הפקודה, ואפשר להכניס תווים מיוחדים.

### דוגמה בטוחה

```python
subprocess.run(["rm", "-rf", "/tmp/test_dir"], shell=False)
```

הדוגמאות למעלה כתובות ל-Linux/macOS (`ping -c`). הגרסה בקוד
(`core/subprocess_basics.py`) פורטבילית — בוחרת את הפרמטר הנכון לפי
`platform.system()` (`-n` ב-Windows מול `-c` ב-Linux), וגם עוטפת
`FileNotFoundError`/`TimeoutExpired` בבדיקת סטטוס שירות.

---

## 4) Retry logic

בפיתוח אוטומציה, חלק מהפעולות מתאפסות זמנית:

- חיבור רשת
- שירות לא זמין
- timeout
- API שהחזיר 500

לכן אנחנו רוצים retry, אבל לא אינסוף פעמים.

### עקרון בסיסי

```python
for attempt in range(1, max_attempts + 1):
    try:
        do_work()
        break
    except Exception:
        if attempt == max_attempts:
            raise
        time.sleep(delay)
```

### למה delay חשוב?

אם נחזור מיד, נעמיס עוד על השרת. יש חשיבות ל-backoff:

```python
delay *= 2
```

---

## 5) Example: combined pattern

```python
import subprocess
import time


def retry_command(command, retries=3, delay=1.0):
    for attempt in range(1, retries + 1):
        try:
            result = subprocess.run(
                command, capture_output=True, text=True, check=False
            )
            if result.returncode == 0:
                return result.stdout
            raise RuntimeError(result.stderr)
        except Exception as exc:
            if attempt == retries:
                raise
            time.sleep(delay)
```

### שימוש

```python
output = retry_command(["ping", "-c", "2", "8.8.8.8"])
print(output)
```

זה מחבר בין:

- subprocess
- error handling
- retry strategy
- clean automation pattern

השורות עצמן הן דוגמה ממחישה בלבד (אין לה קובץ תואם בפרויקט) — אבל שני
הרכיבים שמרכיבים אותה קיימים בנפרד, וניתן לחבר ביניהם באמצעות `@retry`
כדקורטור מעל פונקציה שקוראת ל-`ping_host`: `ping_host`/`check_service_status`
ב-`core/subprocess_basics.py`, והדקורטור `retry` (עם exponential backoff) ב-
`automation_examples/utils/decorators.py`.

---

## 6) OOP -- תכנות מונחה עצמים (classes, inheritance, abstraction)

תכנות מונחה עצמים (OOP) בנוי על ארבעה עקרונות מרכזיים (ה-"four pillars"):

- **Encapsulation** (הכמסה) -- עוטפים data + methods יחד בתוך class, ומגנים על
  ה-state הפנימי (`_x`) מאחורי `@property`, כדי לשלוט על איך קוראים ניגשים אליו.
- **Inheritance** (ירושה) -- class יורש מ-class אחר, וממחזר (וממשיך) את ההתנהגות
  שלו: `class Circle(Shape)`.
- **Polymorphism** (פולימורפיזם) -- קריאה לאותה מתודה (למשל `shape.area()`)
  מתנהגת אחרת בהתאם ל-subclass בפועל, בלי שהקוד הקורא צריך לדעת איזה subclass זה.
- **Abstraction** (הפשטה) -- מגדירים *מה* class יודע לעשות, בלי לחייב *איך*,
  באמצעות abstract base class.

### Abstract class -- כל הכללים

Python מממש abstract classes דרך מודול `abc`:

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...
```

הכללים:

1. class הופך ל-abstract כשהוא יורש מ-`ABC` (או משתמש ב-`metaclass=ABCMeta`).
2. `@abstractmethod` מסמן מתודה ש-subclass **חייב** לממש.
3. אי אפשר ליצור instance של class שיש בו abstract methods שלא מומשו --
   `Shape()` זורק `TypeError` באמת (runtime), לא רק אזהרה של linter.
4. subclass הופך ל"קונקרטי" (ניתן ליצירת instance) רק לאחר שהוא ממש **את כל**
   ה-abstract methods שהוגדרו למעלה בהיררכיה.
5. ל-abstract class מותר להכיל גם מתודות רגילות (concrete), כולל `__init__` --
   subclasses יורשים אותן כרגיל, בלי צורך לממש מחדש.
6. אפשר גם abstract property: `@property` מוגדר מעל `@abstractmethod`.
7. abstract class הוא לא class שנועד ליצירת instances -- הוא מגדיר "חוזה"
   (contract / interface) ש-subclasses מתחייבים אליו.

### דוגמה מלאה

```python
from abc import ABC, abstractmethod


class Shape(ABC):
    def __init__(self, name: str):
        self._name = name  # encapsulation

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def area(self) -> float: ...

    @abstractmethod
    def perimeter(self) -> float: ...

    def describe(self) -> str:  # concrete method, זמין לכל subclass
        return f"{self.name}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"


class Circle(Shape):  # inheritance
    def __init__(self, radius: float):
        super().__init__("Circle")
        self._radius = radius

    def area(self) -> float:
        return 3.14159 * self._radius ** 2

    def perimeter(self) -> float:
        return 2 * 3.14159 * self._radius


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        super().__init__("Rectangle")
        self._width, self._height = width, height

    def area(self) -> float:
        return self._width * self._height

    def perimeter(self) -> float:
        return 2 * (self._width + self._height)
```

### דוגמה שימוש (polymorphism)

```python
shapes: list[Shape] = [Circle(3), Rectangle(4, 5)]

for shape in shapes:
    print(shape.describe())  # אותה קריאה, מימוש שונה לכל shape

Shape("x")  # TypeError: Can't instantiate abstract class Shape...
```

המימוש המלא, כולל ה-`try/except` שתופס את ה-`TypeError` בפועל, נמצא ב-
`core/oop_abstract_classes.py`.

---

## 7) Best practices for Python automation

- use lists for subprocess arguments
- prefer `with` for resource management
- avoid `shell=True` unless absolutely necessary
- keep functions small and focused
- log errors with context
- use clear names for variables and functions
- handle exceptions explicitly
- test simple examples before production use

---

## 8) Summary

הקבצים בתיקייה `python_excrcises` נועדו להדגים מושגים בסיסיים של אוטומציה ו-OOP ב-Python.

הנושאים המרכזיים הם:

- `context managers` לניהול משאבים
- `decorators` להוספת התנהגות חוזרת
- `subprocess` להרצת תהליכים של מערכת
- `retry` לטיפול בטעויות זמניות
- `safe coding` כדי להימנע מבעיות אמינות ובטיחות
- `OOP` -- encapsulation, inheritance, polymorphism, abstraction (abstract classes)

לרשימה המלאה של קבצים לפי נושא (generators, typing, concurrency, dataclasses,
pathlib ועוד) — ראו `README.md`.
