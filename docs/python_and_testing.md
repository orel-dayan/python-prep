# Python לאוטומציה + סוגי בדיקות

שני חלקים: מה צריך לדעת ב-Python לתפקיד אוטומציה, וכל סוגי הבדיקות מוסברים. מותאם לראיון ברפאל.

---

# חלק א — Python לאוטומציה

מסודר לפי שכבות. **חובה** = הכרחי לראיון ראשון. השאר לפי הזמן והדגש של התפקיד.

## שכבה 1 — יסודות השפה (חובה)

### Comprehensions
דרך תמציתית ליצור רשימות/מילונים/קבוצות. שאלה נפוצה בראיון.
```python
squares = [x**2 for x in range(10)]                  # list
evens = [x for x in range(20) if x % 2 == 0]         # with condition
word_len = {w: len(w) for w in words}                # dict comprehension
unique = {x % 3 for x in nums}                        # set comprehension
```

### Generators
מחזירים ערכים אחד-אחד (lazy), חוסכים זיכרון. חשוב לקבצים גדולים / streams.
```python
def read_large_file(path):
    with open(path) as f:
        for line in f:
            yield line.strip()                       # one line at a time, not all in memory
```
**ההבדל מ-list:** list בונה הכל בזיכרון; generator מייצר on-demand. `yield` הוא הסימן.

### Exceptions
טיפול בשגיאות. `finally` תמיד רץ.
```python
try:
    result = risky_operation()
except ValueError as e:
    log.error(f"bad value: {e}")
except (KeyError, IndexError):                        # multiple types
    handle()
else:
    process(result)                                  # runs if no exception
finally:
    cleanup()                                        # always runs
```

### Context Managers (`with`)
פתיחה וסגירה אוטומטית של משאבים. זה ה-RAII של Python.
```python
with open("file.txt") as f:                          # auto-closes, even on exception
    data = f.read()

# custom context manager:
from contextlib import contextmanager
@contextmanager
def timer():
    start = time.time()
    yield
    print(f"took {time.time() - start}s")
```

## שכבה 2 — OOP ב-Python

### Dunder methods (magic methods)
מתודות עם `__` שמגדירות התנהגות מובנית.
```python
class Vector:
    def __init__(self, x, y):                        # constructor
        self.x, self.y = x, y
    def __repr__(self):                              # printable representation
        return f"Vector({self.x}, {self.y})"
    def __eq__(self, other):                         # == operator
        return self.x == other.x and self.y == other.y
    def __add__(self, other):                        # + operator
        return Vector(self.x + other.x, self.y + other.y)
    def __len__(self):                               # len()
        return 2
```

### @property
הופך מתודה לגישה כמו שדה, עם בקרה.
```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def fahrenheit(self):                            # accessed as obj.fahrenheit (no parens)
        return self._celsius * 9/5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self._celsius = (value - 32) * 5/9
```

### @dataclass
מבטל boilerplate — מייצר `__init__`, `__repr__`, `__eq__` אוטומטית.
```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int
    label: str = "origin"                            # default value
# auto-generates __init__, __repr__, __eq__
```

### @staticmethod מול @classmethod
```python
class Pizza:
    def __init__(self, size):
        self.size = size

    @classmethod
    def margherita(cls):                             # alternative constructor — gets cls
        return cls(size="medium")

    @staticmethod
    def is_valid_size(size):                         # no self/cls — just a namespaced function
        return size in ("small", "medium", "large")
```

## שכבה 3 — ספריות לאוטומציה (לפי הדגש)

- **os / pathlib** — עבודה עם קבצים ונתיבים. `pathlib.Path` מודרני יותר מ-`os.path`.
- **subprocess** — הרצת פקודות shell מתוך Python. בסיס לאוטומציית תהליכים.
- **logging** — לוגים מקצועיים (לא `print`). רמות: DEBUG/INFO/WARNING/ERROR.
- **argparse** — פרסור ארגומנטים משורת הפקודה. לכלי CLI.
- **re (regex)** — חיפוש והתאמת תבניות בטקסט.
- **json / yaml** — קריאה/כתיבה של קבצי קונפיגורציה ונתונים.
- **threading / multiprocessing** — מקביליות. threading ל-I/O, multiprocessing ל-CPU.
- **requests** — קריאות HTTP (אם יש API).

## שכבה 4 — בדיקות ב-Python (קריטי לתפקיד אוטומציה!)

### pytest — הפריימוורק הנפוץ
```python
def test_addition():
    assert add(2, 3) == 5                            # simple assert

def test_raises():
    with pytest.raises(ValueError):                  # expect an exception
        parse("invalid")
```

### Fixtures — הכנה ושיתוף לטסטים
```python
@pytest.fixture
def db_connection():
    conn = create_connection()                       # setup
    yield conn                                       # provide to test
    conn.close()                                     # teardown after test

def test_query(db_connection):                       # fixture injected by name
    assert db_connection.query("SELECT 1") == 1
```

### Parametrize — אותו טסט, קלטים שונים
```python
@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square(input, expected):
    assert square(input) == expected                 # runs 3 times
```

### Mocking — בידוד מתלויות חיצוניות
```python
from unittest.mock import patch, MagicMock

def test_api_call():
    with patch("module.requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"status": "ok"}
        result = fetch_data()                        # uses the mock, not real network
        assert result["status"] == "ok"
```
**הרעיון:** מחליפים תלות אמיתית (DB, רשת, API) ב-mock — הטסט בודק את הלוגיקה שלך בלבד, מהיר ודטרמיניסטי.

## שכבה 5 — לחומרה / מערכות מוטמעות (רלוונטי לרפאל)

- **struct** — פרסור נתונים בינאריים. pack/unpack לפי פורמט (big/little endian). קריטי לנתונים מחיישנים וחומרה.
```python
import struct
# unpack 4 bytes as big-endian unsigned int + 2 bytes short
value, flag = struct.unpack(">IH", raw_bytes)
```
- **pyserial** — תקשורת serial עם חומרה (RS-232/485).
- **socket** — תקשורת רשת ברמה נמוכה (TCP/UDP).
- **asyncio** — מקביליות אסינכרונית (async/await) לטיפול בהרבה חיבורים.

## מה הכי חשוב ל-9 ימים
אם זמן מוגבל: **comprehensions, generators, context managers, dunder methods, @property, @dataclass, ו-pytest בסיסי (assert, fixture, parametrize, mock)**. אלה הכי נפוצים בראיון אוטומציה.

---

# חלק ב — סוגי בדיקות

הבנת ההבדלים בין סוגי הבדיקות היא שאלה כמעט ודאית בראיון אוטומציה/QA. הנה כל אחד — מה זה, מתי, ודוגמה.

## טבלת על — מבט מהיר

| בדיקה | מה בודקת | רמה | מתי |
|---|---|---|---|
| **Unit** | יחידת קוד בודדת (פונקציה/מחלקה) | הכי נמוכה | בכל commit |
| **Integration** | אינטראקציה בין רכיבים | בינונית | אחרי שילוב מודולים |
| **E2E** | זרימה מלאה מקצה לקצה | הכי גבוהה | לפני release |
| **Sanity** | בדיקה מהירה שהבסיס עובד | רדודה | אחרי build/fix |
| **Regression** | שתיקונים לא שברו דברים קיימים | רחבה | אחרי כל שינוי |
| **Smoke** | האם הבנייה בכלל ניתנת לבדיקה | רדודה מאוד | מיד אחרי build |
| **Load** | ביצועים תחת עומס צפוי | non-functional | לפני production |
| **Stress** | התנהגות מעבר לגבול | non-functional | לבדיקת עמידות |

## 1. Unit Test (בדיקת יחידה)
**מה:** בודקת **יחידה אחת מבודדת** — פונקציה או מחלקה בודדת, בלי תלויות חיצוניות (DB, רשת מוחלפים ב-mock).

**מאפיינים:** מהירה, דטרמיניסטית, רצה בכל commit. אם נכשלת — יודעים בדיוק איפה הבעיה.

**דוגמה:** בדיקה שפונקציית `calculate_discount(100, 0.2)` מחזירה 80. רק הלוגיקה, בלי DB.

**הקשר:** זה מה שדיברנו עליו בשאלת ה-JUnit עם DB — הופכים אותו ל-unit test ע"י mocking.

## 2. Integration Test (בדיקת אינטגרציה)
**מה:** בודקת ש**כמה רכיבים עובדים יחד** נכון. למשל — הקוד שלך + ה-DB האמיתי, או שני שירותים שמדברים ביניהם.

**ההבדל מ-unit:** unit מבודד רכיב אחד; integration בודק את ה**חיבורים** ביניהם.

**דוגמה:** בדיקה ש-`save_user()` באמת כותב ל-DB ו-`get_user()` קורא אותו בחזרה נכון.

## 3. E2E Test (End-to-End, מקצה לקצה)
**מה:** בודקת **זרימה שלמה** כפי שמשתמש אמיתי חווה אותה, דרך כל השכבות.

**דוגמה:** משתמש נכנס → מתחבר → מוסיף פריט לעגלה → משלם → מקבל אישור. כל המסע, דרך UI, שרת, DB.

**מאפיינים:** הכי קרובה למציאות, אבל איטית ושברירית. מעטות ויקרות — בראש פירמידת הבדיקות.

## 4. Sanity Test (בדיקת שפיות)
**מה:** בדיקה **מהירה וממוקדת** שפונקציונליות ספציפית עובדת אחרי שינוי קטן או תיקון. "האם התיקון עבד והגיוני?"

**דוגמה:** תיקנו באג בכפתור login — sanity test בודק שה-login עובד, בלי לבדוק את כל המערכת.

**ההבדל מ-smoke:** sanity ממוקד וצר (פיצ'ר ספציפי אחרי שינוי); smoke רחב ורדוד (האם הבסיס בכלל עובד).

## 5. Smoke Test (בדיקת עשן)
**מה:** בדיקה **רדודה מאוד** מיד אחרי build — האם הדברים הקריטיים בכלל עובדים, או שהבנייה "עולה בעשן". "האם בכלל שווה להמשיך לבדוק?"

**דוגמה:** האפליקציה נטענת? אפשר להתחבר? הדף הראשי עולה? אם לא — לא טורחים לבדוק עוד.

**הקשר לשם:** מהנדסים שהדליקו חומרה חדשה — אם עלה עשן, נכשל מיד.

## 6. Regression Test (בדיקת רגרסיה)
**מה:** בדיקה שש**ינויים חדשים לא שברו פונקציונליות קיימת** שעבדה. רצים מחדש טסטים ישנים אחרי כל שינוי.

**דוגמה:** הוספנו פיצ'ר חדש — regression suite מריץ את כל הטסטים הקיימים לוודא ששום דבר ישן לא נשבר.

**מאפיינים:** רחבה, לרוב אוטומטית (כי ידנית זה בלתי אפשרי לחזור על הכל). זה **לב האוטומציה** — בדיוק התפקיד.

## 7. Load Test (בדיקת עומס)
**מה:** בודקת ביצועים תחת **עומס צפוי/מציאותי**. האם המערכת עומדת בכמות המשתמשים/בקשות הצפויה.

**דוגמה:** 1000 משתמשים בו-זמנית — זמן התגובה נשאר סביר? אין קריסות?

**מודדים:** זמן תגובה, throughput, שימוש במשאבים.

## 8. Stress Test (בדיקת לחץ)
**מה:** בודקת התנהגות **מעבר לגבול** — דוחפים את המערכת עד שהיא נשברת, כדי לראות *איך* היא נשברת ואם היא מתאוששת.

**ההבדל מ-load:** load בודק עומס *צפוי*; stress דוחף *מעבר* לצפוי בכוונה.

**דוגמה:** מעלים את העומס ל-10,000 משתמשים (פי 10 מהצפוי) — האם המערכת קורסת בחן (graceful) או מתרסקת? מתאוששת אחרי שהעומס יורד?

**מה מחפשים:** נקודת השבירה, התנהגות תחת כשל, יכולת התאוששות.

## פירמידת הבדיקות
```
        /\
       /E2E\          ← מעט, איטי, יקר (כל המערכת)
      /------\
     /Integr. \       ← בינוני (חיבורים)
    /----------\
   /   Unit     \     ← הרבה, מהיר, זול (יחידות)
  /--------------\
```
**העיקרון:** הרבה unit tests (בסיס רחב), פחות integration, מעט E2E. ככל שעולים — איטי ויקר יותר, אז פחות.

## איך לענות בראיון
שאלה נפוצה: "מה ההבדל בין X ל-Y?" — תמיד דרך ההבחנה:
- **unit מול integration:** מבודד רכיב אחד מול בדיקת חיבורים.
- **sanity מול smoke:** ממוקד וצר אחרי שינוי מול רחב ורדוד אחרי build.
- **load מול stress:** עומס צפוי מול דחיפה מעבר לגבול.

---

# סיכום — מה הכי חשוב

**Python:** comprehensions, generators, context managers, OOP (dunders, property, dataclass), ו-pytest (assert, fixture, parametrize, mock).

**בדיקות:** הכי נפוצות בראיון — unit מול integration, regression (לב האוטומציה), ו-load מול stress. אם תזכרי את שלוש ההבחנות בסוף — את מכוסה.

הקשר: כל מה שתרגלת ב-fault analysis וב-QA (3 השלבים, worst-thing-first) משלים את זה — שם זו חשיבת *בדיקה*, פה זה *סוגי* הבדיקות.
