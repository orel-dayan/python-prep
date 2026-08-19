# Python Cheat Sheet לראיונות

<div dir="rtl">


מסמך עזר לראיונות פייתון — פיתוח, QA ואוטומציה.
כל דוגמאות הקוד באנגלית, ההסברים בעברית.

---

# חלק א' — תחביר ומבני נתונים

## 1. Built-ins חיוניים

הפונקציות שפייתון נותנת "בחינם", בלי `import`. אלה שחייבים לדעת בעל-פה:

| פונקציה | מה עושה | דוגמה |
|---|---|---|
| `len(x)` | אורך | `len("abc")` → 3 |
| `sorted(x)` | רשימה ממוינת **חדשה** | `sorted([3,1,2])` → `[1,2,3]` |
| `reversed(x)` | איטרטור הפוך | `list(reversed([1,2,3]))` → `[3,2,1]` |
| `min(x)` / `max(x)` | מינימום / מקסימום | `max([1,5,3])` → 5 |
| `sum(x)` | סכום | `sum([1,2,3])` → 6 |
| `abs(x)` | ערך מוחלט | `abs(-5)` → 5 |
| `round(x, n)` | עיגול | `round(3.14159, 2)` → 3.14 |
| `enumerate(x)` | אינדקס + ערך | `for i, v in enumerate(lst)` |
| `zip(a, b)` | איטרציה מקבילה | `for x, y in zip(a, b)` |
| `any(x)` | האם **לפחות אחד** True | `any([False, True])` → True |
| `all(x)` | האם **כולם** True | `all([True, False])` → False |
| `isinstance(x, T)` | בדיקת טיפוס | `isinstance(5, int)` → True |
| `range(a, b, step)` | טווח — **b לא נכלל** | `range(1, 10, 2)` → 1,3,5,7,9 |
| `map(f, x)` | מפעיל פונקציה על כל איבר | `list(map(str, [1,2]))` → `['1','2']` |
| `filter(f, x)` | מסנן לפי תנאי | `list(filter(lambda n: n>2, [1,3]))` → `[3]` |

**`sorted` עם `key` — הכי נשאל:**

```python
words = ["banana", "kiwi", "apple"]

sorted(words)                    # alphabetical: ['apple', 'banana', 'kiwi']
sorted(words, key=len)           # by length:    ['kiwi', 'apple', 'banana']
sorted(words, reverse=True)      # descending
```

`key` מקבל פונקציה שמופעלת על כל איבר, והמיון נעשה לפי **התוצאה** שלה. `key=len` אומר "מיין לפי האורך של כל מילה".

**`enumerate` ו-`zip` — מחליפים לולאות מכוערות:**

```python
names = ["Dana", "Avi"]
scores = [90, 85]

# instead of: for i in range(len(names))
for i, name in enumerate(names):
    print(i, name)               # 0 Dana / 1 Avi

for i, name in enumerate(names, start=1):
    print(i, name)               # 1 Dana / 2 Avi

# iterate two lists together
for name, score in zip(names, scores):
    print(f"{name}: {score}")    # Dana: 90 / Avi: 85
```

**מלכודת חשובה:** `sorted(lst)` מחזיר רשימה **חדשה** ולא נוגע במקור. `lst.sort()` ממיין **במקום** ומחזיר `None`. `lst = lst.sort()` הוא באג — הרשימה תהפוך ל-`None`.

## 2. מספרים ואופרטורים

```python
7 / 2      # 3.5   true division - always float
7 // 2     # 3     floor division - rounds DOWN
7 % 2      # 1     modulo - remainder
2 ** 10    # 1024  power
divmod(7, 2)   # (3, 1)  - quotient and remainder together

-7 // 2    # -4  !!  floors toward negative infinity, NOT toward zero
-7 % 2     # 1   !!  result takes the sign of the divisor

int("42")      # string to int
int(3.9)       # 3 - truncates, doesn't round
float("3.14")
bin(10)        # '0b1010'
hex(255)       # '0xff'
int("ff", 16)  # 255 - parse hex

float('inf')       # infinity - useful as a starting value for min-finding
float('-inf')
```

**למה `-7 // 2 == -4` ולא `-3`?** כי floor division תמיד מעגלת **כלפי מטה** על ציר המספרים, וכלפי מטה מ-3.5- זה 4-. זו שאלת ראיון קלאסית.

## 3. מחרוזות (str)

מחרוזות ב-Python הן **immutable** — כל מתודה מחזירה מחרוזת חדשה, המקור נשאר.

| מתודה | מה עושה | דוגמה |
|---|---|---|
| `s.split(sep)` | פיצול לרשימה | `"a,b".split(",")` → `['a','b']` |
| `sep.join(lst)` | איחוד רשימה למחרוזת | `"-".join(['a','b'])` → `"a-b"` |
| `s.strip()` | הסרת רווחים מהקצוות | `"  hi  ".strip()` → `"hi"` |
| `s.lstrip()` / `s.rstrip()` | רק משמאל / רק מימין | |
| `s.lower()` / `s.upper()` | אותיות קטנות / גדולות | `"Hi".lower()` → `"hi"` |
| `s.title()` | אות ראשונה בכל מילה | `"a b".title()` → `"A B"` |
| `s.replace(a, b)` | החלפה | `"aaa".replace("a","b")` → `"bbb"` |
| `s.startswith(x)` | מתחיל ב- | `"hello".startswith("he")` → True |
| `s.endswith(x)` | נגמר ב- | `"a.py".endswith(".py")` → True |
| `s.isdigit()` | רק ספרות? | `"123".isdigit()` → True |
| `s.isalpha()` | רק אותיות? | `"abc".isalpha()` → True |
| `s.isalnum()` | אותיות/ספרות? | `"a1".isalnum()` → True |
| `s.find(x)` | אינדקס ראשון, או **1-** אם לא נמצא | `"hello".find("l")` → 2 |
| `s.index(x)` | כמו find, אבל **זורק שגיאה** אם לא נמצא | |
| `s.count(x)` | ספירת מופעים | `"hello".count("l")` → 2 |
| `s.partition(x)` | פיצול לשלושה חלקים | `"a=b".partition("=")` → `('a','=','b')` |
| `s.zfill(n)` | ריפוד באפסים | `"7".zfill(3)` → `"007"` |
| `s.center(n, c)` | מרכוז | `"hi".center(6,"*")` → `"**hi**"` |
| `s[::-1]` | היפוך | `"abc"[::-1]` → `"cba"` |

**`split` מול `partition`:**

```python
log = "ERROR: disk full: /dev/sda1"

log.split(":")           # ['ERROR', ' disk full', ' /dev/sda1']  - all splits
log.split(":", 1)        # ['ERROR', ' disk full: /dev/sda1']     - max 1 split
log.partition(":")       # ('ERROR', ':', ' disk full: /dev/sda1') - always 3 parts
```

ב-parsing של לוגים `partition` בטוח יותר — הוא תמיד מחזיר בדיוק שלושה חלקים, גם אם המפריד לא קיים.

**המרות ו-encoding:**

```python
chars = list("hello")        # ['h','e','l','l','o']
word  = "".join(chars)       # back to "hello"

"abc".encode("utf-8")        # str -> bytes:  b'abc'
b"abc".decode("utf-8")       # bytes -> str:  'abc'

ord('a')       # 97   character -> number
chr(97)        # 'a'  number -> character
ord(ch) - ord('a')    # letter index 0-25 - common in interview questions
```

**עברית ו-encoding — נקודה שמפילה בפועל:**

```python
len("שלום")                     # 4   - characters
len("שלום".encode("utf-8"))     # 8   - bytes! Hebrew is 2 bytes per char

open("f.txt", encoding="utf-8")     # ALWAYS specify encoding explicitly
```

בלי `encoding="utf-8"` פייתון משתמשת בברירת המחדל של מערכת ההפעלה — ובחלונות זה לא UTF-8, מה שיוצר בדיוק את שגיאות ה-`?` והג'יבריש בעברית.

## 4. רשימות (list) ו-slicing

| מתודה | מה עושה | סיבוכיות |
|---|---|---|
| `lst.append(x)` | הוספה לסוף | O(1) |
| `lst.extend(other)` | הוספת כל איברי רשימה אחרת | O(k) |
| `lst.pop()` | הוצאה מהסוף | O(1) |
| `lst.pop(i)` | הוצאה מאינדקס | **O(n)** |
| `lst.insert(i, x)` | הכנסה באינדקס | **O(n)** |
| `lst.remove(x)` | הסרת המופע **הראשון** של ערך | O(n) |
| `lst.index(x)` | אינדקס של ערך | O(n) |
| `lst.count(x)` | ספירת מופעים | O(n) |
| `lst.sort()` | מיון **במקום** | O(n log n) |
| `lst.reverse()` | היפוך **במקום** | O(n) |
| `x in lst` | בדיקת שייכות | **O(n)** ← להשתמש ב-set |
| `lst.copy()` | העתקה רדודה | O(n) |
| `lst.clear()` | ריקון | O(1) |

**Slicing — `lst[start:stop:step]`:**

```python
lst = [0, 1, 2, 3, 4, 5]

lst[2:5]      # [2, 3, 4]      - stop NOT included
lst[:3]       # [0, 1, 2]      - from the beginning
lst[3:]       # [3, 4, 5]      - to the end
lst[-2:]      # [4, 5]         - last two
lst[:-1]      # [0,1,2,3,4]    - everything except the last
lst[::2]      # [0, 2, 4]      - every second element
lst[::-1]     # [5,4,3,2,1,0]  - reversed COPY
lst[1:5:2]    # [1, 3]         - with step

lst[1:3] = ['a', 'b', 'c']     # slice assignment - can change length!
```

**Slicing תמיד מחזיר עותק חדש** ולא זורק שגיאה על גבולות חורגים:

```python
lst[10:20]    # []  - no IndexError, just empty
lst[10]       # IndexError!  - direct indexing DOES raise
```

## 5. Tuples — כמו רשימה, אבל immutable

```python
t = (1, 2, 3)
t = 1, 2, 3           # parentheses are optional
single = (1,)         # ONE element needs a trailing comma!
empty = ()

t[0]                  # 1  - indexing works
t.count(1), t.index(2)   # only these two methods
t[0] = 5              # TypeError - cannot modify

# Unpacking
x, y = (10, 20)
a, b = b, a                  # swap - this is tuple unpacking
first, *rest = [1, 2, 3, 4]  # first=1, rest=[2,3,4]
*init, last = [1, 2, 3, 4]   # init=[1,2,3], last=4
```

**מתי tuple ולא list?**
1. כשהנתונים לא אמורים להשתנות — הגנה מפני באגים
2. כ**מפתח במילון** או איבר בסט — רשימה לא יכולה (היא לא hashable)
3. כערך חזרה מפונקציה שמחזירה כמה דברים

```python
d = {(1, 2): "point A"}      # tuple key - works
d = {[1, 2]: "fail"}         # TypeError: unhashable type: 'list'

def get_stats(nums):
    return min(nums), max(nums), sum(nums)   # returns a tuple

low, high, total = get_stats([1, 5, 3])      # unpacked on the way out
```

## 6. מילונים (dict)

| מתודה | מה עושה |
|---|---|
| `d[k]` | גישה — **זורק KeyError** אם חסר |
| `d.get(k, default)` | גישה **בטוחה** — מחזיר default |
| `d[k] = v` | הוספה או עדכון |
| `d.pop(k, default)` | הוצאה בטוחה |
| `d.keys()` / `d.values()` / `d.items()` | מפתחות / ערכים / זוגות |
| `k in d` | בדיקת מפתח — **O(1)** |
| `d.setdefault(k, default)` | מחזיר ערך, ויוצר אותו אם חסר |
| `d.update(other)` | מיזוג מילון אחר |
| `d.clear()` | ריקון |

```python
d = {'a': 1, 'b': 2}

for key, value in d.items():
    print(key, value)

# The counting pattern - memorize this
counts = {}
for ch in text:
    counts[ch] = counts.get(ch, 0) + 1

# Merging (3.9+)
merged = d1 | d2
d1 |= d2            # in-place
```

**`d[k]` מול `d.get(k)` — זו החלטת עיצוב, לא רק סגנון:**

```python
value = d['missing']          # KeyError - crashes here, loudly
value = d.get('missing')      # None - continues silently
value = d.get('missing', 0)   # 0 - explicit fallback
```

השימוש ב-`.get()` נכון כשחסר מפתח הוא מצב **לגיטימי**. אם חסר מפתח הוא **באג**, עדיף `d[k]` שיתפוצץ מיד — קריסה מוקדמת עדיפה על נתון שגוי שממשיך במערכת.

## 7. סטים (set)

אוסף **ללא כפילויות** ו**ללא סדר**, עם בדיקת שייכות ב-O(1).

```python
s = {1, 2, 3}
s = set([1, 2, 2, 3])    # {1, 2, 3} - duplicates removed
empty = set()            # NOT {} - that's an empty dict!

s.add(4)
s.remove(4)      # KeyError if missing
s.discard(4)     # silent if missing
s.pop()          # removes an arbitrary element

x in s           # O(1)  <- the whole point

a, b = {1,2,3}, {2,3,4}
a & b            # {2, 3}     intersection - in both
a | b            # {1,2,3,4}  union - in either
a - b            # {1}        difference - in a but not b
a ^ b            # {1, 4}     symmetric difference - in exactly one
a <= b           # is a a subset of b?
```

**השימוש הכי נפוץ בראיונות:**

```python
unique = list(set(items))                  # remove duplicates
has_duplicates = len(items) != len(set(items))
common = set(list1) & set(list2)           # shared elements
```

**מלכודת:** סט מאבד את הסדר. אם צריך גם ייחודיות וגם סדר מקורי:

```python
unique_ordered = list(dict.fromkeys(items))   # dicts preserve insertion order
```

## 8. collections — הכוכב של ראיונות

```python
from collections import Counter, defaultdict, deque, namedtuple
```

**`Counter` — פותר עשרות שאלות לבד:**

```python
c = Counter("mississippi")
# Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})

c['i']                    # 4  - missing keys return 0, no KeyError
c.most_common(2)          # [('i', 4), ('s', 4)]
c.most_common()[-1]       # least common
sum(c.values())           # total count

Counter(a) == Counter(b)  # anagram check in one line!

c1 + c2                   # add counts
c1 - c2                   # subtract counts
```

**`defaultdict` — בלי KeyError לעולם:**

```python
# Grouping - the classic use
groups = defaultdict(list)
for word in ["eat", "tea", "tan"]:
    key = "".join(sorted(word))      # anagram signature
    groups[key].append(word)         # no need to check if key exists
# {'aet': ['eat', 'tea'], 'ant': ['tan']}

counts = defaultdict(int)
for ch in text:
    counts[ch] += 1                  # starts at 0 automatically
```

**`deque` — תור דו-כיווני, O(1) בשני הקצוות:**

```python
q = deque([1, 2, 3])
q.append(4)          # add right     O(1)
q.appendleft(0)      # add left      O(1)
q.pop()              # remove right  O(1)
q.popleft()          # remove left   O(1)  <- list.pop(0) is O(n)!
q.rotate(1)          # shift elements

q = deque(maxlen=100)   # fixed size - old items drop off automatically
```

`maxlen` שימושי מאוד באוטומציה — למשל להחזיק את 100 שורות הלוג האחרונות בלי לצרוך זיכרון אינסופי.

**`namedtuple` — tuple עם שמות:**

```python
Point = namedtuple('Point', ['x', 'y'])
p = Point(3, 4)
p.x, p.y          # 3, 4  - readable
p[0]              # 3     - still works like a tuple
```

היום `dataclass` בדרך כלל עדיף (סעיף 23), אבל namedtuple קל יותר ו-immutable.

## 9. Comprehensions

הדרך הפייתונית לבנות אוסף מתוך אוסף אחר.

```python
# Basic:      [expression for item in iterable]
[x**2 for x in range(5)]                    # [0, 1, 4, 9, 16]

# With filter: [expression for item in iterable if condition]
[x for x in nums if x % 2 == 0]             # only evens

# With ternary (note: the if comes BEFORE the for here)
[x if x > 0 else 0 for x in nums]           # replace negatives with 0

# Nested loops - read them left to right, like nested for loops
[(i, j) for i in range(2) for j in range(2)]   # [(0,0),(0,1),(1,0),(1,1)]

# Dict comprehension
{name: len(name) for name in names}
{k: v for k, v in d.items() if v > 10}      # filter a dict

# Set comprehension
{word.lower() for word in words}            # unique, lowercased
```

**ההבדל בין שני התחבירים של `if`:**

```python
[x for x in nums if x > 0]        # FILTER - keeps only some items
[x if x > 0 else 0 for x in nums] # TRANSFORM - keeps all, changes some
```

**מתי לא להשתמש:** אם ה-comprehension לא נקרא בשורה אחת בנוחות — לולאה רגילה קריאה יותר. קריאות מנצחת "חוכמה".

## 10. itertools ו-math

```python
from itertools import combinations, permutations, product, chain, groupby

list(combinations([1,2,3], 2))   # [(1,2),(1,3),(2,3)]      order does NOT matter
list(permutations([1,2,3], 2))   # [(1,2),(2,1),(1,3),...]  order DOES matter
list(product([1,2], ['a','b']))  # [(1,'a'),(1,'b'),(2,'a'),(2,'b')]  cartesian
list(chain([1,2], [3,4]))        # [1,2,3,4]  flatten several iterables
list(product([0,1], repeat=3))   # all 3-bit combinations - useful for test matrices
```

`product` שימושי במיוחד לאוטומציה — יצירת **מטריצת בדיקות** מכל שילוב פרמטרים:

```python
for browser, os_name in product(["chrome", "firefox"], ["win", "linux"]):
    run_test(browser, os_name)      # 4 combinations
```

```python
import math

math.floor(3.7)     # 3
math.ceil(3.2)      # 4
math.sqrt(16)       # 4.0
math.gcd(12, 18)    # 6
math.inf            # infinity
math.isclose(0.1 + 0.2, 0.3)   # True - the RIGHT way to compare floats
```

**`isclose` חשוב:** `0.1 + 0.2 == 0.3` הוא `False` בגלל ייצוג בינארי של שברים. אף פעם לא להשוות floats עם `==`.

## 11. random

| פונקציה | מחזיר | חזרות? | משנה מקור? |
|---|---|---|---|
| `random.shuffle(lst)` | `None` — **in-place** | — | כן |
| `random.choice(seq)` | איבר **אחד** | — | לא |
| `random.choices(seq, k=n)` | רשימה של n | **כן** | לא |
| `random.sample(seq, k=n)` | רשימה של n | **לא** | לא |
| `random.randint(a, b)` | int בטווח [a, b] — **כולל שניהם** | — | — |
| `random.randrange(n)` | int בטווח [0, n) — **בלי n** | — | — |
| `random.random()` | float בטווח [0, 1) | — | — |
| `random.uniform(a, b)` | float בטווח [a, b] | — | — |

```python
random.seed(42)      # reproducible results - essential for debugging tests
```

**ההבדל הקריטי `choices` מול `sample`:**

```python
random.choices(['A','K','Q'], k=3)   # might return ['A','A','A'] - repeats allowed
random.sample(['A','K','Q'], k=3)    # always 3 different cards
```

לחלוקת קלפים תמיד `sample` (או `shuffle`). `choices` מתאים לסימולציה של הטלת קובייה חוזרת.

**`randint` מול `randrange`** — `randint(1,6)` יכול להחזיר 6, `randrange(6)` לא יחזיר 6 לעולם (רק 0-5). זה מקור נפוץ ל-off-by-one.

---

# חלק ב' — ליבת השפה

## 12. פונקציות ופרמטרים

```python
def greet(name, greeting="Hello", *args, **kwargs):
    ...
```

**ארבעת סוגי הפרמטרים:**

```python
def f(a, b=2, *args, **kwargs):
    print(a)         # positional - required
    print(b)         # default - optional
    print(args)      # tuple of extra positional arguments
    print(kwargs)    # dict of extra keyword arguments

f(1, 5, 6, 7, x=10, y=20)
# a=1, b=5, args=(6, 7), kwargs={'x': 10, 'y': 20}
```

**Unpacking בקריאה לפונקציה:**

```python
nums = [1, 2, 3]
print(*nums)                    # same as print(1, 2, 3)

config = {"host": "localhost", "port": 8080}
connect(**config)               # same as connect(host="localhost", port=8080)
```

**`*` ריק — כפיית keyword-only:**

```python
def create_user(*, name: str, age: int):
    ...

create_user("Dana", 25)             # TypeError!
create_user(name="Dana", age=25)    # OK
```

הכוכבית הריקה אומרת "כל מה שאחריי חייב להיקרא בשם". זה מונע את הבאג הקלאסי של החלפת סדר בין שני פרמטרים מאותו טיפוס — `create_user(25, "Dana")` לא יכול לקרות. **זהו כלי secure code ישיר:** ככל שיש יותר פרמטרים, כך גדל הסיכוי לטעות בסדר, וה-`*` מבטל אותו.

**`/` — positional-only (3.8+):**

```python
def f(a, b, /, c):
    ...
f(1, 2, c=3)      # a and b MUST be positional
```

פחות נפוץ, אבל שווה להכיר — משמש בעיקר בספריות שרוצות חופש לשנות שמות פרמטרים בעתיד.

## 13. Scope, closures ו-`global`

```python
x = "global"

def outer():
    x = "enclosing"

    def inner():
        print(x)      # finds "enclosing" - looks outward
    inner()
```

**כלל LEGB** — פייתון מחפשת משתנה בסדר הזה: **L**ocal → **E**nclosing → **G**lobal → **B**uilt-in.

```python
counter = 0

def increment():
    counter += 1      # UnboundLocalError! assignment makes it local

def increment_fixed():
    global counter    # explicit: use the module-level variable
    counter += 1

def outer():
    count = 0
    def inner():
        nonlocal count    # use the ENCLOSING function's variable
        count += 1
    inner()
    return count
```

**Closure — פונקציה שזוכרת את הסביבה שבה נוצרה:**

```python
def make_multiplier(factor):
    def multiply(x):
        return x * factor     # remembers 'factor' after make_multiplier returned
    return multiply

double = make_multiplier(2)
double(5)      # 10
```

זה בדיוק המנגנון שעליו בנויים **decorators** (סעיף 19).

**מלכודת ידועה — closure בלולאה:**

```python
# BAD - all three functions capture the SAME variable i
funcs = [lambda: i for i in range(3)]
[f() for f in funcs]        # [2, 2, 2]  - not [0, 1, 2]!

# GOOD - bind the current value as a default argument
funcs = [lambda i=i: i for i in range(3)]
[f() for f in funcs]        # [0, 1, 2]
```

## 14. Mutable מול Immutable — ואיך פייתון מעבירה ארגומנטים

| Immutable | Mutable |
|---|---|
| `int`, `float`, `bool` | `list` |
| `str` | `dict` |
| `tuple` | `set` |
| `frozenset` | אובייקטים מותאמים |

```python
def modify(lst, num):
    lst.append(4)      # MUTATES the caller's list
    num += 1           # rebinds a LOCAL name - caller sees nothing

my_list, my_num = [1, 2, 3], 10
modify(my_list, my_num)
print(my_list, my_num)     # [1, 2, 3, 4]   10
```

**התשובה לשאלה "פייתון היא pass by value או pass by reference?"** — אף אחד מהם. היא **pass by object reference**: הפונקציה מקבלת הפניה לאותו אובייקט. אם האובייקט mutable, אפשר לשנות אותו והשינוי נראה בחוץ. אם הוא immutable, כל "שינוי" יוצר אובייקט חדש שמחובר לשם המקומי בלבד.

**רק immutable יכול להיות מפתח במילון או איבר בסט** — כי הוא צריך hash יציב:

```python
{(1, 2): "ok"}      # tuple - hashable
{[1, 2]: "fail"}    # TypeError: unhashable type: 'list'
```

**מלכודת mutable default argument:**

```python
# BAD - the default list is created ONCE and reused across all calls
def add_card(card, deck=[]):
    deck.append(card)
    return deck

add_card("A")    # ['A']
add_card("K")    # ['A', 'K']  <- the same list!

# GOOD
def add_card(card, deck=None):
    if deck is None:
        deck = []
    deck.append(card)
    return deck
```

## 15. העתקה — shallow מול deep

```python
import copy

original = [[1, 2], [3, 4]]

alias   = original                 # NOT a copy - same object, two names
shallow = original.copy()          # new OUTER list, SAME inner lists
deep    = copy.deepcopy(original)  # everything new, recursively

original[0].append(99)

print(alias)      # [[1, 2, 99], [3, 4]]   changed
print(shallow)    # [[1, 2, 99], [3, 4]]   ALSO changed!
print(deep)       # [[1, 2], [3, 4]]       safe
```

**הכלל:** `copy()` משכפל רק את הרמה החיצונית. אם יש אובייקטים מקוננים — הם משותפים. `deepcopy` משכפל הכל רקורסיבית (ולכן איטי יותר).

**דרכים להעתקה רדודה:** `lst.copy()`, `lst[:]`, `list(lst)`, `copy.copy(lst)` — כולן שקולות.

## 16. חריגות (Exceptions)

```python
try:
    risky_operation()
except ValueError as e:
    logger.error(f"Bad value: {e}")
except (KeyError, IndexError) as e:      # several types at once
    logger.error(f"Lookup failed: {e}")
except Exception as e:
    logger.exception("Unexpected failure")   # logs the full traceback
    raise                                     # re-raise after logging
else:
    logger.info("Succeeded")     # runs ONLY if no exception was raised
finally:
    cleanup()                    # ALWAYS runs - even on exception or return
```

**היררכיית החריגות** — חשוב לתפוס מהספציפי לכללי, כי הראשון שמתאים הוא זה שתופס:

```
BaseException
 └── Exception
      ├── ValueError      wrong value    (int("abc"))
      ├── TypeError       wrong type     (1 + "a")
      ├── KeyError        missing dict key
      ├── IndexError      list index out of range
      ├── AttributeError  no such attribute
      ├── FileNotFoundError
      ├── TimeoutError
      └── ZeroDivisionError
```

**חריגה מותאמת — סימן לקוד בוגר:**

```python
class DeviceNotReadyError(Exception):
    """Raised when the device under test does not respond in time."""

class InvalidCardError(ValueError):      # inherit from the closest built-in
    """Raised when a card is not in the deck."""

raise DeviceNotReadyError(f"Device {device_id} timed out after {timeout}s")
```

**אנטי-פאטרן שמראיינים מחפשים:**

```python
# BAD - swallows EVERYTHING, including typos and KeyboardInterrupt
try:
    process(data)
except:
    pass

# GOOD - specific type, logged, re-raised
try:
    process(data)
except ValueError as e:
    logger.error(f"Invalid data: {e}")
    raise
```

`except: pass` יוצר באגים בלתי-ניתנים-לאיתור — הקוד "עובד" אבל שותק על כשלים.

**`raise ... from` — שרשור סיבות:**

```python
try:
    value = config['port']
except KeyError as e:
    raise ConfigError("Missing required setting") from e   # preserves the chain
```

## 17. Context managers — `with`

```python
with open("data.txt", encoding="utf-8") as f:
    data = f.read()
# f.close() happens automatically - even if read() raised
```

**כל הרעיון:** הניקוי מובטח, גם כשיש חריגה. בלי `with`, קובץ יישאר פתוח אם משהו נכשל באמצע.

```python
# Several at once
with open("in.txt") as fin, open("out.txt", "w") as fout:
    fout.write(fin.read())
```

**לכתוב context manager משלך — שתי דרכים:**

```python
# Way 1: a class with __enter__ / __exit__
class Timer:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"took {time.time() - self.start:.2f}s")
        return False       # False = don't suppress the exception

# Way 2: a generator with @contextmanager - shorter
from contextlib import contextmanager

@contextmanager
def timer(label):
    start = time.time()
    try:
        yield                      # the with-block runs here
    finally:
        print(f"{label}: {time.time() - start:.2f}s")

with timer("API call"):
    requests.get(url)
```

הכל לפני ה-`yield` הוא setup, הכל אחריו הוא teardown. זה **בדיוק** אותו רעיון כמו fixture ב-pytest (סעיף 32).

## 18. Generators — `yield`

```python
# Regular function - builds the entire list in memory
def get_squares(n):
    return [i ** 2 for i in range(n)]

# Generator - produces one value at a time, lazily
def gen_squares(n):
    for i in range(n):
        yield i ** 2
```

```python
g = gen_squares(1_000_000)   # instant - nothing computed yet
next(g)                      # 0
next(g)                      # 1
for value in gen_squares(5): # consumed one at a time
    print(value)
```

**generator expression** — כמו comprehension אבל עצלה:

```python
squares = (i ** 2 for i in range(1_000_000))     # ( ) instead of [ ]
total = sum(i ** 2 for i in range(1_000_000))    # no list ever built
```

**השימוש האמיתי — קבצים ולוגים גדולים:**

```python
def read_errors(path):
    """Works on a 10GB log file - only one line in memory at a time."""
    with open(path, encoding="utf-8") as f:
        for line in f:
            if "ERROR" in line:
                yield line.strip()

for error in read_errors("huge.log"):
    process(error)
```

**המחיר:** גנרטור נצרך **פעם אחת בלבד**. אחרי שעברת עליו הוא ריק:

```python
g = gen_squares(3)
list(g)      # [0, 1, 4]
list(g)      # []  <- exhausted!
```

**`yield from`** — האצלה לגנרטור אחר:

```python
def combined():
    yield from gen_squares(3)
    yield from gen_squares(2)
```

## 19. Decorators

דקורטור הוא פונקציה שמקבלת פונקציה, עוטפת אותה, ומחזירה פונקציה חדשה.

```python
import functools
import time

def timer(func):
    @functools.wraps(func)        # preserves __name__ and __doc__ of the original
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start:.3f}s")
        return result
    return wrapper


@timer
def slow_function():
    time.sleep(1)

slow_function()      # slow_function took 1.001s
```

**`@timer` הוא בסך הכל קיצור ל-** `slow_function = timer(slow_function)`.

**`functools.wraps` הוא חובה** — בלעדיו `slow_function.__name__` יהפוך ל-`"wrapper"`, וזה שובר דיבאגינג, לוגים, ו-pytest.

**דקורטור עם ארגומנטים — שכבה נוספת:**

```python
def retry(times: int = 3, delay: float = 1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == times - 1:
                        raise
                    logger.warning(f"Attempt {attempt+1} failed: {e}, retrying")
                    time.sleep(delay)
        return wrapper
    return decorator


@retry(times=5, delay=2)
def flaky_api_call():
    ...
```

`@retry` הוא **הפתרון הישיר לטסטים flaky** — נושא שנשאל כמעט תמיד בראיון אוטומציה.

**למה זה קריטי לאוטומציה:** `@pytest.fixture`, `@pytest.mark.parametrize`, `@patch`, `@property` — כולם דקורטורים. הבנת המנגנון מסבירה את כל הפריימוורק.

**דקורטורים מובנים שכדאי להכיר:**

```python
@functools.lru_cache(maxsize=128)    # caches results - huge speedup for recursion
def fibonacci(n):
    return n if n < 2 else fibonacci(n-1) + fibonacci(n-2)

@functools.cached_property           # computed once per instance
def expensive_value(self):
    ...
```

## 20. מחלקות (OOP) — הבסיס

```python
class Card:
    # Class attribute - shared by ALL instances
    suits = ['hearts', 'spades', 'diamonds', 'clubs']

    def __init__(self, rank: str, value: int):
        # Instance attributes - unique per object
        self.rank = rank
        self.value = value
        self._internal = None      # single _ : "private by convention"
        self.__mangled = None      # double _ : name mangling (rarely needed)

    def __str__(self) -> str:
        """For humans - what print() shows."""
        return self.rank

    def __repr__(self) -> str:
        """For developers - what the debugger and REPL show."""
        return f"Card(rank='{self.rank}', value={self.value})"

    def __eq__(self, other) -> bool:
        """Defines what == means for this class."""
        if not isinstance(other, Card):
            return NotImplemented
        return self.value == other.value

    def __hash__(self):
        """Required if __eq__ is defined AND you want to use the object in a set."""
        return hash(self.value)

    def __lt__(self, other) -> bool:
        """Defines < , which makes sorted() work on Card objects."""
        return self.value < other.value
```

**`__str__` מול `__repr__` — שאלה קלאסית:**
`__str__` למשתמש הסופי, `__repr__` למפתח. אם מגדירים רק אחד — תגדירי `__repr__`, כי פייתון נופלת אליו כברירת מחדל גם ב-`print`. כלל אצבע: `__repr__` אמור להיראות כמו קוד שיוצר את האובייקט מחדש.

**Dunder methods שכדאי להכיר:**

| מתודה | מפעילה |
|---|---|
| `__init__` | יצירת אובייקט |
| `__str__` / `__repr__` | `print()` / `repr()` |
| `__eq__` / `__lt__` / `__gt__` | `==` / `<` / `>` |
| `__hash__` | שימוש ב-set או כמפתח dict |
| `__len__` | `len(obj)` |
| `__getitem__` | `obj[key]` |
| `__contains__` | `x in obj` |
| `__iter__` / `__next__` | לולאת for |
| `__call__` | `obj()` — אובייקט שמתנהג כפונקציה |
| `__enter__` / `__exit__` | `with obj:` |

**Class attribute מול instance attribute — מלכודת:**

```python
class Deck:
    cards = []          # SHARED by all instances - usually a bug!

    def add(self, card):
        self.cards.append(card)

d1, d2 = Deck(), Deck()
d1.add('A')
print(d2.cards)     # ['A']  <- d2 sees it too!
```

התיקון: לאתחל ב-`__init__` (`self.cards = []`) כדי שכל אובייקט יקבל רשימה משלו.

## 21. ירושה, ABC, ו-composition

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError("Subclass must implement speak()")


class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)     # call the parent's __init__ - don't skip this
        self.breed = breed

    def speak(self):               # override
        return "Woof"
```

**`super()`** מפנה למחלקת האב לפי סדר ה-MRO. תמיד להשתמש בו במקום `Animal.__init__(self, name)` — הוא עובד נכון גם בירושה מרובה.

**Abstract Base Class — לאכוף מימוש:**

```python
from abc import ABC, abstractmethod

class TestRunner(ABC):
    @abstractmethod
    def setup(self): ...

    @abstractmethod
    def run(self): ...

    def execute(self):             # concrete method - shared by all subclasses
        self.setup()
        return self.run()


class SerialTestRunner(TestRunner):
    def setup(self):
        self.port = serial.Serial("/dev/ttyUSB0")

    def run(self):
        return self.port.readline()


TestRunner()          # TypeError - cannot instantiate an abstract class
```

היתרון על `NotImplementedError`: השגיאה קופצת **בזמן יצירת האובייקט**, לא כשמישהו קורא למתודה החסרה בייצור.

**MRO — סדר החיפוש בירושה מרובה:**

```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

D.__mro__      # D -> B -> C -> A -> object
D.mro()        # same, as a list
```

פייתון מחפשת מתודה לפי הסדר הזה ועוצרת בראשונה שנמצאה. זה נקרא C3 linearization.

**Composition מול Inheritance — שאלת עיצוב שנשאלת הרבה:**

```python
# Inheritance: "is-a"     - a Dog IS AN Animal
class Dog(Animal): ...

# Composition: "has-a"    - a TestRunner HAS A logger and HAS A connection
class TestRunner:
    def __init__(self, connection, logger):
        self.connection = connection      # injected, not inherited
        self.logger = logger
```

**הכלל המקובל: להעדיף composition.** ירושה יוצרת צימוד הדוק — שינוי במחלקת האב שובר את כל היורשות. composition מאפשרת להחליף רכיב (למשל connection אמיתי ב-mock בטסטים) בלי לגעת בקוד. זו גם הסיבה ש-**dependency injection** מקל כל כך על בדיקות.

**`__slots__` — חיסכון בזיכרון:**

```python
class Point:
    __slots__ = ('x', 'y')      # no __dict__ - saves memory, forbids new attributes

    def __init__(self, x, y):
        self.x, self.y = x, y

p = Point(1, 2)
p.z = 3        # AttributeError - not in __slots__
```

רלוונטי כשיוצרים מיליוני אובייקטים קטנים. בראיון מספיק לדעת שזה קיים ולמה.

## 22. property, classmethod, staticmethod

```python
class Temperature:
    def __init__(self, celsius: float):
        self._celsius = celsius

    @property
    def fahrenheit(self) -> float:
        """Computed on access - called WITHOUT parentheses."""
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float):
        if value < -459.67:
            raise ValueError("Below absolute zero")   # validation on assignment!
        self._celsius = (value - 32) * 5 / 9


t = Temperature(25)
t.fahrenheit          # 77.0   <- no ()
t.fahrenheit = 100    # calls the setter, which validates
```

**למה `@property` ולא getter/setter כמו ב-Java:** אפשר להתחיל עם attribute רגיל (`self.value`), ואם מאוחר יותר צריך validation או חישוב — להפוך אותו ל-property **בלי לשבור שום קוד קיים** שכבר כותב `obj.value`. זה החיסכון ב-boilerplate שפייתון מציעה.

```python
class Deck:
    REQUIRED_SIZE = 10

    def __init__(self, cards):
        self.cards = cards

    @classmethod
    def create_random(cls):
        """Alternative constructor - receives the CLASS as cls."""
        return cls(random.sample(list(card_values), k=cls.REQUIRED_SIZE))

    @classmethod
    def from_file(cls, path):
        """Another alternative constructor - a very common pattern."""
        return cls(Path(path).read_text().split())

    @staticmethod
    def is_valid_rank(rank: str) -> bool:
        """Utility - needs neither self nor cls."""
        return rank in card_values
```

| דקורטור | מקבל | מתי להשתמש |
|---|---|---|
| מתודה רגילה | `self` | פעולה על אובייקט ספציפי |
| `@classmethod` | `cls` | constructor חלופי, פעולה ברמת המחלקה |
| `@staticmethod` | כלום | פונקציית עזר ששייכת לוגית למחלקה |

`@classmethod` עדיף על `@staticmethod` ל-constructors, כי `cls` עובד נכון גם במחלקות יורשות.

## 23. dataclass

```python
from dataclasses import dataclass, field, asdict

@dataclass
class Card:
    rank: str
    value: int
    tags: list = field(default_factory=list)   # NOT tags: list = []

# __init__, __repr__, __eq__ are generated automatically
c = Card('A', 14)
print(c)                     # Card(rank='A', value=14, tags=[])
c == Card('A', 14)           # True
asdict(c)                    # {'rank': 'A', 'value': 14, 'tags': []}
```

בלי `@dataclass` היית צריכה לכתוב ידנית `__init__`, `__repr__` ו-`__eq__` — כ-15 שורות boilerplate לכל מחלקה.

**אפשרויות חשובות:**

```python
@dataclass(frozen=True)      # immutable - and therefore hashable (usable as dict key)
class Point:
    x: int
    y: int

@dataclass(order=True)       # generates __lt__, __le__, __gt__, __ge__ for sorting
class Score:
    points: int

@dataclass
class Config:
    host: str
    port: int = 8080         # fields with defaults must come AFTER those without
```

**`field(default_factory=list)`** היא הגרסה של dataclass לבעיית mutable default argument — היא יוצרת רשימה חדשה לכל אובייקט. כתיבת `tags: list = []` תזרוק שגיאה, ובצדק.

## 24. Enum

```python
from enum import Enum, auto, IntEnum

class TestStatus(Enum):
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"

class Priority(IntEnum):     # comparable with < >  and usable as an int
    LOW = 1
    HIGH = 3
```

```python
status = TestStatus.PASSED

status.name        # 'PASSED'
status.value       # 'passed'
list(TestStatus)   # all members
TestStatus("passed")        # lookup by value
TestStatus["PASSED"]        # lookup by name

if status is TestStatus.FAILED:      # use 'is' for enum comparison
    ...
```

**למה Enum ולא מחרוזות:**

```python
# BAD - a typo passes silently and the bug hides for weeks
if result == "faild":
    ...

# GOOD - a wrong name raises AttributeError immediately
if result is TestStatus.FAILD:      # AttributeError!
    ...
```

זו בדיוק חשיבת secure code: להפוך טעות שקטה לשגיאה רועשת ומיידית.

## 25. Type hints

```python
from typing import Optional, Union, Callable, Any, TypeVar

def f(items: list[str]) -> dict[str, int]: ...        # 3.9+
def g(x: int | None = None): ...                      # 3.10+ (was Optional[int])
def h(x: int | str): ...                              # (was Union[int, str])
def k(point: tuple[int, int]): ...
def m(callback: Callable[[int], str]): ...            # takes int, returns str

# Variables and class attributes
count: int = 0
names: list[str] = []

# Old syntax - still seen in existing code
from typing import List, Dict, Optional
def f(items: List[str]) -> Optional[Dict[str, int]]: ...
```

**חשוב מאוד להבנה:** type hints הן **תיעוד בלבד**. פייתון **לא אוכפת** אותן בזמן ריצה — אפשר להעביר מחרוזת לפרמטר שמסומן `int` והכל ירוץ. האכיפה נעשית בכלי חיצוני:

```bash
pip install mypy
mypy myfile.py        # catches type errors before runtime
```

בפרויקטים מקצועיים `mypy` רץ כחלק מה-CI, לצד הטסטים. זה מה שהופך את ה-hints משימושיים לבעלי ערך אמיתי.

## 26. מודולים, imports ופרויקטים

```python
import math                      # whole module
import numpy as np               # with an alias
from math import sqrt, pi        # specific names
from math import *               # BAD - pollutes the namespace, hides conflicts
```

**מבנה חבילה (package):**

```
myproject/
├── src/
│   └── mypackage/
│       ├── __init__.py        # marks this directory as a package
│       ├── devices.py
│       └── utils/
│           ├── __init__.py
│           └── parsing.py
└── tests/
    └── test_devices.py
```

```python
# Absolute import - preferred, clear and unambiguous
from mypackage.utils.parsing import parse_log

# Relative import - only inside a package
from .utils.parsing import parse_log      # one level: same package
from ..devices import Device              # two levels up
```

**`__init__.py`** הופך תיקייה לחבילה. הוא יכול להיות ריק, או לחשוף API נוח:

```python
# mypackage/__init__.py
from .devices import Device      # now: from mypackage import Device
```

**השגיאה הכי נפוצה — `ModuleNotFoundError`:**

פייתון מחפשת מודולים ב-`sys.path`, שכולל את תיקיית הסקריפט הראשי והחבילות המותקנות — **אבל לא בהכרח את שורש הפרויקט**. פתרונות, מהטוב לפחות:

```bash
# BEST: install your project in editable mode
pip install -e .          # needs pyproject.toml or setup.py

# OK: run as a module from the project root
python -m mypackage.main

# LAST RESORT: patch sys.path (fragile, avoid in real projects)
import sys; sys.path.insert(0, "/path/to/project")
```

**`if __name__ == "__main__":`**

```python
def main():
    ...

if __name__ == "__main__":
    main()
```

`__name__` שווה `"__main__"` כשהקובץ **מורץ ישירות**, ולשם המודול כשהוא **מיובא**. בלי השורה הזאת, כל `import` של הקובץ יריץ גם את הקוד שבתחתיתו — מה שישבור את קובץ הטסטים שמייבא אותו.

**סביבה וירטואלית — תמיד:**

```bash
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows

pip install -r requirements.txt
pip freeze > requirements.txt   # save the exact versions
deactivate
```

בלי venv, ספריות של פרויקטים שונים מתנגשות ביניהן, ואי אפשר לשחזר סביבה במחשב אחר או ב-CI.

## 27. f-strings

```python
name, score = "Dana", 87.4567

f"{name} scored {score}"       # Dana scored 87.4567
f"{score:.2f}"                 # 87.46       two decimal places
f"{score:>10}"                 # right-aligned within 10 chars
f"{score:<10}"                 # left-aligned
f"{score:^10}"                 # centered
f"{1234567:,}"                 # 1,234,567   thousands separator
f"{0.856:.1%}"                 # 85.6%       percentage
f"{255:b}" , f"{255:x}"        # 11111111 , ff
f"{name=}"                     # name='Dana'   <- debug syntax (3.8+)

from datetime import datetime
f"{datetime.now():%Y-%m-%d %H:%M}"     # date formatting inline
```

**`f"{name=}"` הוא טריק דיבאג מצוין** — מדפיס גם את שם המשתנה וגם את הערך, בלי לכתוב את השם פעמיים.

**שימי לב:** בתוך f-string לא ניתן להשתמש באותם גרשיים שעוטפים אותה (עד 3.12):

```python
f"{d['key']}"      # OK - different quote types
f"{d["key"]}"      # SyntaxError before Python 3.12
```

---

# חלק ג' — Best Practices, מלכודות וביצועים

## 28. מלכודות נפוצות — לקרוא לפני כל ראיון

**1. מתודות שמשנות במקום ומחזירות `None`**

```python
lst = [3, 1, 2]
lst = lst.sort()          # BAD - lst is now None!
lst.sort()                # GOOD

random.shuffle(deck)      # returns None - same trap
lst.reverse(), lst.append(), lst.clear()    # all return None
```

**2. השמה לא מעתיקה רשימה**

```python
b = a          # same object, two names
b = a.copy()   # actual copy (shallow)
```

**3. שינוי אוסף תוך כדי איטרציה עליו**

```python
# BAD - the indices shift and elements get skipped
for n in nums:
    if n % 2 == 0:
        nums.remove(n)

# GOOD - build a new list
nums = [n for n in nums if n % 2 != 0]
```

**4. `range` לא כולל את הסוף, `randint` כן**

```python
range(1, 10)             # 1..9
random.randint(1, 10)    # 1..10  <- includes 10!
```

**5. `d[key]` זורק, `d.get(key)` לא**

**6. mutable default argument** — `def f(lst=[])` (סעיף 14)

**7. `is` מול `==`**

```python
if x == None:    # BAD
if x is None:    # GOOD - None is a singleton

a = [1,2]; b = [1,2]
a == b           # True  - same content
a is b           # False - different objects
```

**8. חלוקה שלמה של שליליים** — `-7 // 2` הוא `-4` ולא `-3`

**9. השוואת floats**

```python
0.1 + 0.2 == 0.3                    # False!
math.isclose(0.1 + 0.2, 0.3)        # True
```

**10. `{}` הוא dict ריק, לא set ריק** — סט ריק הוא `set()`

**11. חיבור מחרוזות בלולאה** — O(n²), להשתמש ב-`"".join()`

**12. גנרטור נצרך פעם אחת** — קריאה שנייה תחזיר ריק

## 29. Best Practices — BAD מול GOOD

**פחות פרמטרים — קבוצה במקום רשימה ארוכה**

```python
# BAD - seven positional parameters, easy to swap by mistake
def create_user(name, age, email, address, phone, role, is_active):
    ...

# GOOD - one validated object
@dataclass
class UserData:
    name: str
    age: int
    email: str
    role: str

def create_user(user: UserData):
    ...
```

**Single Responsibility — פונקציה עושה דבר אחד**

```python
# BAD - fetches, parses, validates, saves, and emails
def process_order(order_id): ...

# GOOD - each step is testable on its own
def fetch_order(order_id): ...
def validate_order(order): ...
def save_order(order): ...
```

הסימן המובהק שפונקציה עושה יותר מדי: קשה לתת לה שם בלי "and".

**Input validation מפורש**

```python
def create_deck(size: int = REQUIRED_DECK_SIZE) -> list[str]:
    if size != REQUIRED_DECK_SIZE:
        raise ValueError(f"Deck size must be exactly {REQUIRED_DECK_SIZE}, got {size}")
    return random.sample(list(card_values), k=size)
```

**Defense in depth:** גם פונקציה שמקבלת קלט מפונקציה "שלנו" מוודאת אותו — כי אין ערובה שהקורא הבא יהיה מי שציפינו לו.

**Magic number מול קבוע בעל שם**

```python
# BAD - what is 10? and it appears in four other places
if len(deck) != 10:
    raise ValueError("wrong size")

# GOOD - one source of truth
REQUIRED_DECK_SIZE = 10
if len(deck) != REQUIRED_DECK_SIZE:
    raise ValueError(f"Deck size must be {REQUIRED_DECK_SIZE}")
```

**flags בוליאניים — red flag**

```python
# BAD - what does process(data, True, False, True) even mean?
def process(data, validate=True, log=False, retry=True): ...

# GOOD - an enum, or separate functions
def process(data, mode: ProcessMode): ...
```

כל flag בוליאני מכפיל את מספר מסלולי הריצה. ארבעה flags = 16 שילובים, שרובם לא נבדקו מעולם.

**enumerate במקום range(len(...))**

```python
for i in range(len(names)):     # BAD
    print(i, names[i])

for i, name in enumerate(names):   # GOOD
    print(i, name)
```

**set במקום list לבדיקות שייכות חוזרות**

```python
if card in card_list:      # O(n) every time
card_set = set(card_list)
if card in card_set:       # O(1)
```

**Comprehension במקום לולאת append**

```python
evens = []                          # BAD
for n in nums:
    if n % 2 == 0:
        evens.append(n)

evens = [n for n in nums if n % 2 == 0]     # GOOD
```

**`with` במקום פתיחה וסגירה ידנית** (סעיף 17)

**PEP 8 — סגנון**

| נושא | כלל |
|---|---|
| הזחה | 4 רווחים, לא טאבים |
| פונקציות ומשתנים | `snake_case` |
| מחלקות | `PascalCase` |
| קבועים | `UPPER_CASE` |
| "פרטי" | `_leading_underscore` |
| אורך שורה | עד 79-99 תווים |
| שורות ריקות | 2 בין פונקציות ברמה עליונה, 1 בין מתודות |

```bash
pip install ruff
ruff check .          # linting - catches style and logic issues
ruff format .         # auto-formatting
```

`ruff` הוא הכלי המודרני (מחליף flake8 + black + isort) והוא מהיר מאוד. בפרויקט מקצועי הוא רץ ב-CI ופוסל PR שלא עובר.

## 30. סיבוכיות — הטבלה שצריך לזכור

| פעולה | סיבוכיות | הערה |
|---|---|---|
| `lst[i]` | O(1) | |
| `lst.append(x)` | O(1) | amortized |
| `lst.pop()` | O(1) | מהסוף |
| `lst.pop(0)` / `lst.insert(0,x)` | **O(n)** | כל האיברים זזים ← `deque` |
| `x in lst` | **O(n)** | ← `set` |
| `lst.sort()` | O(n log n) | Timsort |
| `lst[a:b]` | O(k) | יוצר עותק |
| `d[key]` / `key in d` | O(1) | ממוצע |
| `x in set` | O(1) | ממוצע |
| `set` union / intersection | O(n) | |
| `deque.appendleft` / `popleft` | O(1) | |
| `heapq.heappush` / `heappop` | O(log n) | |
| `str += str` בלולאה | **O(n²)** | ← `"".join()` |

```python
# BAD - a new string object is allocated on every iteration
result = ""
for word in words:
    result += word

# GOOD - one allocation
result = "".join(words)
```

**המיון בפייתון הוא stable** — איברים עם אותו מפתח שומרים על סדרם המקורי. זה מאפשר מיון רב-שלבי:

```python
people.sort(key=lambda p: p["name"])    # first by name
people.sort(key=lambda p: p["age"])     # then by age; ties keep name order
```

**מיון מתקדם:**

```python
sorted(people, key=lambda p: (p["age"], p["name"]))     # two keys via tuple
sorted(people, key=lambda p: (-p["age"], p["name"]))    # age desc, name asc

from operator import itemgetter, attrgetter
sorted(people, key=itemgetter("age"))       # faster than a lambda
sorted(cards, key=attrgetter("value"))      # for objects

max(people, key=lambda p: p["age"])         # max/min take key too
```

## 31. דיבאגינג

**`breakpoint()` — הדרך המודרנית:**

```python
def process(data):
    breakpoint()          # execution stops here and opens an interactive debugger
    result = transform(data)
    return result
```

פקודות בתוך ה-debugger:

| פקודה | מה עושה |
|---|---|
| `n` (next) | השורה הבאה, בלי להיכנס לפונקציות |
| `s` (step) | נכנס לתוך הפונקציה |
| `c` (continue) | ממשיך עד ה-breakpoint הבא |
| `l` (list) | מציג את הקוד סביב המיקום |
| `p x` / `pp x` | מדפיס משתנה / מדפיס יפה |
| `w` (where) | stack trace נוכחי |
| `q` (quit) | יציאה |

**קריאת traceback — לקרוא מלמטה למעלה:**

```
Traceback (most recent call last):
  File "main.py", line 10, in <module>      <- where it started
    result = process(data)
  File "main.py", line 5, in process
    return card_values[card]
KeyError: 'X'                                <- the actual error, READ THIS FIRST
```

השורה האחרונה היא סוג השגיאה והערך הבעייתי. השורות מעליה הן שרשרת הקריאות — **התחתונה היא המקום שבו זה קרה בפועל**.

**דיבאג בטסטים:**

```bash
pytest -x                  # stop at the first failure
pytest --pdb               # drop into the debugger on failure
pytest -s                  # show print() output (pytest captures it by default)
pytest --lf                # rerun only the tests that failed last time
pytest -vv                 # show full diff on assertion failure
```

**לוגים במקום print** (סעיף 39) — `print` נעלם בריצת CI, לוג נשמר.

---

# חלק ד' — טסטים ואוטומציה

## 32. pytest — הליבה של תפקיד אוטומציה

**המבנה הבסיסי** — קבצים ופונקציות שמתחילים ב-`test_`, ו-`assert` רגיל:

```python
# test_war.py
from war import create_deck

def test_deck_has_correct_size():
    deck = create_deck()             # Arrange
    result = len(deck)               # Act
    assert result == 10              # Assert
```

זה מבנה **AAA — Arrange, Act, Assert**: הכנה, ביצוע, בדיקה. שווה להזכיר את המונח בראיון.

**בדיקת חריגות:**

```python
import pytest

def test_negative_size_raises():
    with pytest.raises(ValueError):
        create_deck(-1)

def test_error_message_is_helpful():
    with pytest.raises(ValueError, match="must be exactly"):
        create_deck(5)               # also checks the message text
```

זו הדרך לבדוק שה-validation שכתבת באמת עובד — בדיקה שהקוד **נכשל כשצריך**, לא רק שהוא מצליח כשצריך.

**Fixtures — הכנה משותפת:**

```python
@pytest.fixture
def sample_deck():
    """Runs before every test that asks for it."""
    return create_deck()

def test_deck_size(sample_deck):     # just name it as a parameter
    assert len(sample_deck) == 10

def test_no_duplicates(sample_deck): # gets a FRESH deck, not the same one
    assert len(sample_deck) == len(set(sample_deck))
```

**Fixture עם setup ו-teardown:**

```python
@pytest.fixture
def serial_connection():
    port = serial.Serial("/dev/ttyUSB0", 9600)    # setup
    yield port                                     # the test runs here
    port.close()                                   # teardown - ALWAYS runs
```

ה-teardown רץ **גם אם הטסט נכשל** — בדיוק כמו `finally`. זה אותו רעיון של context manager (סעיף 17).

**Scope — כמה פעמים ה-fixture נוצר:**

```python
@pytest.fixture(scope="function")   # default - a new one per test
@pytest.fixture(scope="class")      # once per test class
@pytest.fixture(scope="module")     # once per file
@pytest.fixture(scope="session")    # once for the entire run
```

חיבור יקר (מסד נתונים, מכשיר חומרה) → `session`. נתונים שהטסט משנה → `function`, אחרת טסטים ידלפו זה לזה ותאבד **test isolation**.

**Parametrize — אותו טסט על הרבה קלטים:**

```python
@pytest.mark.parametrize("size", [-1, 0, 5, 11, 100])
def test_invalid_sizes_raise(size):
    with pytest.raises(ValueError):
        create_deck(size)

@pytest.mark.parametrize("card,expected", [
    ('2', 2),
    ('J', 11),
    ('A', 14),
])
def test_card_values(card, expected):
    assert card_values[card] == expected
```

כל שורה היא טסט נפרד בדוח — אם אחד נכשל, רואים בדיוק איזה קלט הפיל אותו.

**Markers — תיוג וסינון:**

```python
@pytest.mark.smoke
def test_device_responds(): ...

@pytest.mark.slow
def test_full_regression(): ...

@pytest.mark.skip(reason="feature not implemented yet")
@pytest.mark.skipif(sys.platform == "win32", reason="Linux only")
@pytest.mark.xfail(reason="known bug BUG-1234")
```

```bash
pytest -m smoke              # run only smoke tests
pytest -m "not slow"         # skip the slow ones
```

**`conftest.py`** — fixtures משותפים לכל הטסטים בתיקייה, בלי import:

```python
# tests/conftest.py
import pytest

@pytest.fixture(scope="session")
def config():
    return {"host": "192.168.1.10", "timeout": 30}
```

**פקודות הרצה:**

| פקודה | מה עושה |
|---|---|
| `pytest` | מריץ הכל |
| `pytest -v` | verbose — שם כל טסט ותוצאה |
| `pytest -k "deck"` | רק טסטים ששמם מכיל "deck" |
| `pytest -m smoke` | רק לפי marker |
| `pytest -x` | עוצר בכישלון הראשון |
| `pytest --lf` | רק מה שנכשל בפעם הקודמת |
| `pytest -s` | מציג `print` |
| `pytest --tb=short` | traceback מקוצר |
| `pytest --cov=mypackage` | דוח כיסוי (`pytest-cov`) |
| `pytest -n 4` | הרצה מקבילה (`pytest-xdist`) |
| `pytest --html=report.html` | דוח HTML (`pytest-html`) |

**`pytest.ini`:**

```ini
[pytest]
testpaths = tests
markers =
    smoke: quick sanity tests
    slow: long-running tests
addopts = -v --tb=short --strict-markers
```

`--strict-markers` פוסל marker שלא הוגדר — תופס שגיאות כתיב בתיוג.

## 33. unittest — הספרייה המובנית

pytest פופולרי יותר, אבל `unittest` מגיע בתוך פייתון ונמצא בהרבה קוד קיים בתעשייה — שווה לזהות אותו.

```python
import unittest

class TestDeck(unittest.TestCase):

    def setUp(self):                 # runs before EACH test
        self.deck = create_deck()

    def tearDown(self):              # runs after EACH test
        self.deck = None

    @classmethod
    def setUpClass(cls):             # runs ONCE before all tests in the class
        cls.connection = connect()

    def test_deck_size(self):
        self.assertEqual(len(self.deck), 10)

    def test_no_duplicates(self):
        self.assertEqual(len(self.deck), len(set(self.deck)))

    def test_invalid_size_raises(self):
        with self.assertRaises(ValueError):
            create_deck(-1)


if __name__ == "__main__":
    unittest.main()
```

**מתודות ה-assert הנפוצות:**

| unittest | pytest |
|---|---|
| `assertEqual(a, b)` | `assert a == b` |
| `assertTrue(x)` | `assert x` |
| `assertIn(a, b)` | `assert a in b` |
| `assertIsNone(x)` | `assert x is None` |
| `assertRaises(E)` | `pytest.raises(E)` |
| `assertAlmostEqual(a, b)` | `math.isclose(a, b)` |

**ההבדל המרכזי** הוא ה-boilerplate: unittest דורש class, ירושה מ-`TestCase`, ומתודות assert מיוחדות. pytest מסתפק בפונקציה ו-`assert` רגיל. **pytest יכול להריץ טסטים של unittest** — אז אפשר לעבור בהדרגה.

## 34. mock — לבודד את מה שבודקים

```python
from unittest.mock import Mock, MagicMock, patch

# A Mock object accepts any call and records it
mock_device = Mock()
mock_device.read.return_value = b"OK\n"

result = mock_device.read()          # b"OK\n"
mock_device.read.assert_called_once()
mock_device.read.assert_called_with(timeout=5)
mock_device.read.call_count          # how many times
```

**`patch` — החלפה זמנית של תלות אמיתית:**

```python
@patch("mymodule.requests.get")
def test_api_call(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"id": 1}

    result = fetch_user(1)

    assert result["id"] == 1
    mock_get.assert_called_once()
```

**כלל הזהב של `patch`:** מחליפים את המקום שבו הפונקציה **נמצאת בשימוש**, לא את המקום שבו היא מוגדרת. אם `mymodule.py` כתב `import requests`, ה-patch הוא על `"mymodule.requests.get"` — לא על `"requests.get"`.

**`side_effect` — התנהגות מורכבת:**

```python
mock.side_effect = ConnectionError("device offline")   # raise an exception
mock.side_effect = [1, 2, 3]                           # different value per call
mock.side_effect = lambda x: x * 2                     # custom logic
```

`side_effect` עם רשימה מצוין לסימולציית חומרה: קריאה ראשונה מחזירה "לא מוכן", השנייה "מוכן".

**`monkeypatch` — החלופה המובנית של pytest:**

```python
def test_with_monkeypatch(monkeypatch):
    monkeypatch.setattr(random, "randint", lambda a, b: 5)   # deterministic
    monkeypatch.setenv("API_KEY", "fake-key")
    monkeypatch.chdir("/tmp")
```

**מתי משתמשים ב-mock:** רשת, מסד נתונים, זמן, רנדומליות, **חומרה** — כל מה שאיטי, לא יציב, או לא זמין בסביבת הפיתוח.

**עיקרון חשוב:** לפעמים עדיף **לא** למקק אלא לבנות נתונים דטרמיניסטיים:

```python
# Instead of mocking random, just build a predictable deck
def test_player1_wins():
    assert play_round(['A'], ['2']) == "Player 1"
```

קוד שקל לבדוק בלי mocks הוא בדרך כלל קוד מעוצב טוב. שימוש כבד ב-mocks לעיתים קרובות מסמן צימוד הדוק מדי — שם ה-composition (סעיף 21) עוזרת.

## 35. requests — בדיקות API

```python
import requests

r = requests.get("https://api.example.com/users", timeout=5)
r = requests.post(url, json={"name": "test"}, headers={"Authorization": "Bearer x"})
r = requests.put(url, data=payload)
r = requests.delete(url)

r.status_code        # 200
r.json()             # parsed body
r.text               # raw body
r.headers
r.elapsed            # response time - useful for performance assertions
r.ok                 # True if status < 400
r.raise_for_status() # raises HTTPError on 4xx/5xx
```

**Session — חיבור ו-cookies משותפים:**

```python
with requests.Session() as s:
    s.headers.update({"Authorization": "Bearer token"})
    s.get(url1)          # reuses the TCP connection - much faster
    s.get(url2)
```

**`timeout=` הוא חובה בכל בקשה.** בלעדיו, בקשה שנתקעת תולה את כל ה-suite לנצח. זו הערת code review קלאסית.

```python
# Full pattern with error handling
try:
    r = requests.get(url, timeout=5)
    r.raise_for_status()
    data = r.json()
except requests.Timeout:
    logger.error("Request timed out")
except requests.HTTPError as e:
    logger.error(f"HTTP {e.response.status_code}")
except requests.RequestException as e:
    logger.error(f"Request failed: {e}")
```

## 36. sockets — תקשורת רשת

רלוונטי לבדיקת מערכות שמדברות ב-TCP/UDP ישירות.

```python
import socket

# TCP client
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(5)                       # ALWAYS set a timeout
    s.connect(("192.168.1.10", 8080))
    s.sendall(b"STATUS\n")
    response = s.recv(1024)               # up to 1024 bytes
    print(response.decode())

# TCP server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 8080))
    server.listen(5)
    conn, addr = server.accept()
    with conn:
        data = conn.recv(1024)
        conn.sendall(b"ACK\n")

# UDP - connectionless
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.settimeout(2)
    s.sendto(b"PING", ("192.168.1.10", 9000))
    data, addr = s.recvfrom(1024)
```

| | TCP (`SOCK_STREAM`) | UDP (`SOCK_DGRAM`) |
|---|---|---|
| חיבור | דורש `connect`/`accept` | ללא חיבור |
| אמינות | מובטח, לפי סדר | ללא הבטחה |
| מהירות | איטי יותר | מהיר יותר |
| שימוש | קבצים, HTTP, פקודות | טלמטריה, שידור, זמן-אמת |

**`recv` לא מבטיח לקרוא הכל.** TCP הוא זרם בייטים בלי גבולות הודעה — צריך ללולאה עד שמתקבלת הודעה שלמה:

```python
def recv_until(sock, delimiter=b"\n"):
    """Read until the delimiter - TCP does not preserve message boundaries."""
    buffer = b""
    while delimiter not in buffer:
        chunk = sock.recv(1024)
        if not chunk:
            raise ConnectionError("Connection closed by peer")
        buffer += chunk
    return buffer
```

זו טעות נפוצה מאוד ומקור לבאגים לא יציבים.

## 37. pyserial — ממשק סריאלי (חומרה)

```python
import serial

with serial.Serial(
    port="/dev/ttyUSB0",        # Windows: "COM3"
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=2,                  # read timeout in seconds
) as ser:
    ser.write(b"AT+STATUS\r\n")
    response = ser.readline()          # reads until \n or timeout
    print(response.decode().strip())
```

```python
ser.write(data)          # send bytes - must be bytes, not str
ser.read(n)              # read exactly n bytes (or fewer on timeout)
ser.readline()           # read until newline
ser.read_all()           # everything in the buffer right now
ser.in_waiting           # how many bytes are waiting
ser.reset_input_buffer() # clear stale data - do this before a new command
ser.flush()              # wait until everything is actually sent

# List available ports
from serial.tools import list_ports
for port in list_ports.comports():
    print(port.device, port.description)
```

**נקודות שחשוב להכיר לתפקיד עם חומרה:**

1. **תמיד `bytes`, לא `str`** — `ser.write("hi")` נכשל; צריך `b"hi"` או `"hi".encode()`.
2. **`timeout` חובה** — בלעדיו `readline()` יכול להיתקע לנצח אם המכשיר לא עונה.
3. **לנקות buffer לפני פקודה** — שאריות מפקודה קודמת יגרמו לקריאה של תשובה לא נכונה.
4. **baudrate חייב להתאים בשני הצדדים** — אחרת מקבלים ג'יבריש, לא שגיאה.

**בדיקה בלי חומרה — mock של הפורט:**

```python
@patch("mymodule.serial.Serial")
def test_device_status(mock_serial):
    mock_port = mock_serial.return_value.__enter__.return_value
    mock_port.readline.return_value = b"STATUS: OK\r\n"

    result = get_device_status()

    assert result == "OK"
    mock_port.write.assert_called_with(b"AT+STATUS\r\n")
```

ככה בודקים לוגיקת תקשורת **בלי מכשיר פיזי** — בדיוק מה שנדרש כשאין מעבדה זמינה.

## 38. selenium ו-playwright — אוטומציית דפדפן

```python
# Selenium - the veteran, very widespread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
try:
    driver.get("https://example.com/login")

    driver.find_element(By.ID, "username").send_keys("user")
    driver.find_element(By.NAME, "password").send_keys("pass")
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()

    # ALWAYS use explicit waits - never time.sleep
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "dashboard"))
    )
    assert "Welcome" in element.text
finally:
    driver.quit()
```

```python
# Playwright - the modern alternative, auto-waits built in
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://example.com/login")

    page.fill("#username", "user")
    page.fill("#password", "pass")
    page.click("button[type=submit]")

    page.wait_for_selector("#dashboard")     # usually implicit
    assert page.text_content("#dashboard")
    browser.close()
```

**Page Object Model** — התבנית הסטנדרטית ל-UI automation:

```python
class LoginPage:
    """Each page is a class - test logic separate from selectors."""

    def __init__(self, driver):
        self.driver = driver

    def login(self, username: str, password: str):
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
        return DashboardPage(self.driver)


def test_valid_login(driver):
    dashboard = LoginPage(driver).login("user", "pass")
    assert dashboard.is_loaded()
```

**היתרון:** כשה-UI משתנה, מתקנים סלקטור **במקום אחד** ולא ב-50 טסטים. זו התשובה לשאלה "איך שומרים על suite של UI לאורך זמן".

**explicit wait מול sleep** — הגורם מספר אחת לטסטים flaky ב-UI:

```python
time.sleep(5)                                    # BAD - slow AND unreliable
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locator))   # GOOD
```

## 39. Robot Framework — בדיקות מבוססות מילות מפתח

נפוץ מאוד בבדיקות מערכת בתעשייה הביטחונית, כי אנשי בדיקות לא-מתכנתים יכולים לקרוא ולכתוב טסטים.

```robotframework
*** Settings ***
Library    SerialLibrary
Library    MyDeviceLibrary.py

*** Variables ***
${PORT}        /dev/ttyUSB0
${TIMEOUT}     5

*** Test Cases ***
Device Responds To Status Command
    Open Serial Port    ${PORT}    115200
    Send Command        AT+STATUS
    ${response}=        Read Response    timeout=${TIMEOUT}
    Should Contain      ${response}      OK
    [Teardown]          Close Serial Port
```

**הרעיון:** הטסטים כתובים במילות מפתח קריאות, והמימוש נמצא בספרייה בפייתון:

```python
# MyDeviceLibrary.py
from robot.api.deco import keyword

class MyDeviceLibrary:

    @keyword("Send Command")
    def send_command(self, command: str):
        self.port.write(f"{command}\r\n".encode())

    @keyword("Read Response")
    def read_response(self, timeout: int = 5) -> str:
        return self.port.readline().decode().strip()
```

```bash
robot tests/            # run, produces log.html and report.html automatically
robot -i smoke tests/   # only tests tagged 'smoke'
```

**מתי Robot ומתי pytest:** Robot כשהטסטים נכתבים או נקראים גם על ידי לא-מתכנתים ורוצים דוחות מובנים; pytest כשהצוות מתכנתים ורוצים גמישות מלאה בפייתון.

## 40. paramiko — SSH לשרתים ומכשירים

```python
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect("192.168.1.10", username="user", key_filename="~/.ssh/id_rsa",
                   timeout=10)

    stdin, stdout, stderr = client.exec_command("systemctl status myservice")
    output = stdout.read().decode()
    exit_code = stdout.channel.recv_exit_status()      # 0 = success

    # File transfer
    sftp = client.open_sftp()
    sftp.get("/var/log/device.log", "local_copy.log")
    sftp.put("config.yaml", "/etc/myapp/config.yaml")
    sftp.close()
finally:
    client.close()
```

**הערת אבטחה:** `AutoAddPolicy` מקבל כל מפתח שרת ללא בדיקה — נוח למעבדה, אבל בסביבת ייצור זו פרצה ל-man-in-the-middle. שם משתמשים ב-`load_system_host_keys()`.

## 41. os, pathlib ו-subprocess

```python
from pathlib import Path

p = Path("/home/user/data.txt")
p.exists(), p.is_file(), p.is_dir()
p.name          # 'data.txt'
p.stem          # 'data'
p.suffix        # '.txt'
p.parent        # Path('/home/user')
p.absolute()

p.read_text(encoding="utf-8")
p.write_text("content", encoding="utf-8")

Path("logs").mkdir(parents=True, exist_ok=True)
list(Path("logs").glob("*.log"))          # in this directory
list(Path("logs").rglob("*.log"))         # recursive

new_path = Path("logs") / "today" / "run.log"     # / joins paths, cross-platform
```

`pathlib` עדיף על `os.path` — קריא יותר, עובד בכל מערכת הפעלה, ופחות שגיאות של מפרידי נתיב.

```python
import os

os.environ.get("API_KEY", "default")     # safe env access
os.getcwd()
os.listdir(".")
```

**`subprocess` — הרצת פקודות מערכת:**

```python
import subprocess

result = subprocess.run(
    ["ping", "-c", "4", "192.168.1.10"],   # a LIST, never a single string
    capture_output=True,
    text=True,                              # decode to str instead of bytes
    timeout=30,
    check=False,                            # True = raise on non-zero exit
)

result.returncode      # 0 = success
result.stdout
result.stderr
```

**אזהרת אבטחה — command injection:**

```python
# DANGEROUS - if filename is "; rm -rf /" the shell will execute it
subprocess.run(f"cat {filename}", shell=True)

# SAFE - arguments are passed directly, no shell interpretation
subprocess.run(["cat", filename])
```

לעולם לא `shell=True` עם קלט שמגיע מבחוץ. זו אחת הפרצות הנפוצות ביותר וגם שאלת ראיון ב-secure code.

## 42. logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("automation.log", encoding="utf-8"),
        logging.StreamHandler(),          # also to the console
    ],
)
logger = logging.getLogger(__name__)
```

```python
logger.debug("detailed info, off in production")
logger.info("normal flow: test started")
logger.warning("unexpected but recoverable: retrying")
logger.error("operation failed")
logger.critical("system is down")

try:
    ...
except Exception:
    logger.exception("Failed to read device")    # logs the full traceback
```

| רמה | מתי |
|---|---|
| `DEBUG` | פרטי דיבאג — כבוי בייצור |
| `INFO` | זרימה תקינה |
| `WARNING` | חריג אבל ניתן להתאוששות |
| `ERROR` | פעולה נכשלה |
| `CRITICAL` | המערכת לא מתפקדת |

**למה לא `print`:** אין רמות לסינון, אין חותמת זמן, לא נשמר לקובץ, ונעלם בריצת CI. כששואלים בראיון "איך תדעי מה נכשל בריצה של 3 בבוקר?" — התשובה היא logging עם רמות וקובץ.

## 43. re — ביטויים רגולריים

```python
import re

re.search(pattern, text)      # first match ANYWHERE -> Match or None
re.match(pattern, text)       # match at the START only
re.fullmatch(pattern, text)   # the entire string must match
re.findall(pattern, text)     # list of all matches
re.finditer(pattern, text)    # iterator of Match objects
re.sub(pattern, repl, text)   # replace
re.split(pattern, text)
```

```python
log = "2026-08-10 14:23:01 ERROR device_7 timeout after 30s"

m = re.search(r"(\d{4}-\d{2}-\d{2}) (\w+) (\w+) .* (\d+)s", log)
if m:
    m.group(0)     # the whole match
    m.group(1)     # '2026-08-10'   first capture group
    m.groups()     # all groups as a tuple

# Named groups - much more readable
m = re.search(r"(?P<level>ERROR|WARN) (?P<device>\w+)", log)
m.group("level")     # 'ERROR'
m.groupdict()        # {'level': 'ERROR', 'device': 'device_7'}

# Compile once, reuse in a loop - faster
ERROR_PATTERN = re.compile(r"ERROR (\w+)")
for line in log_lines:
    if match := ERROR_PATTERN.search(line):      # walrus operator
        print(match.group(1))
```

| ביטוי | משמעות |
|---|---|
| `\d` `\w` `\s` | ספרה / תו מילה / רווח |
| `\D` `\W` `\S` | ההפך |
| `.` | כל תו (חוץ מ-newline) |
| `*` `+` `?` | 0+ / 1+ / 0 או 1 |
| `{n}` `{n,m}` | בדיוק n / בין n ל-m |
| `^` `$` | תחילת / סוף מחרוזת |
| `[abc]` `[^abc]` | אחד מ- / לא אחד מ- |
| `(...)` | capture group |
| `(?:...)` | קיבוץ בלי capture |
| `\|` | או |
| `\b` | גבול מילה |

**`*?` — greedy מול lazy:**

```python
re.search(r"<(.*)>", "<a><b>").group(1)     # 'a><b'  - greedy, takes the most
re.search(r"<(.*?)>", "<a><b>").group(1)    # 'a'     - lazy, takes the least
```

**תמיד raw string** — `r"\d+"` ולא `"\d+"`, אחרת פייתון מפרשת את ה-`\` כתו בריחה.

## 44. JSON, CSV ו-YAML

```python
import json

data = json.loads(json_string)                    # str -> dict
text = json.dumps(data, indent=2, ensure_ascii=False)   # dict -> str

with open("config.json", encoding="utf-8") as f:
    config = json.load(f)                         # from a file

with open("out.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

**`ensure_ascii=False` קריטי לעברית** — בלעדיו מקבלים `\u05e9\u05dc\u05d5\u05dd` במקום "שלום".

```python
import csv

with open("data.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)          # each row is a dict keyed by column name
    for row in reader:
        print(row["device_id"], row["status"])

with open("out.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["device_id", "status"])
    writer.writeheader()
    writer.writerows(rows)
```

**`newline=""` חובה** — בלעדיו מקבלים שורות ריקות כפולות בחלונות.

```python
import yaml            # pip install pyyaml

with open("config.yaml", encoding="utf-8") as f:
    config = yaml.safe_load(f)         # ALWAYS safe_load, never load()
```

**`yaml.load()` יכול להריץ קוד שרירותי** מקובץ זדוני. `safe_load` הוא היחיד שמותר. זו עוד שאלת secure code.

## 45. זמן, המתנות ו-polling

```python
import time
from datetime import datetime, timedelta

start = time.time()
elapsed = time.time() - start
time.perf_counter()          # higher precision, for measuring durations

now = datetime.now()
now.strftime("%Y-%m-%d %H:%M:%S")
datetime.strptime("2026-01-15", "%Y-%m-%d")
tomorrow = now + timedelta(days=1)
(end - start).total_seconds()
```

**הנקודה החשובה ביותר באוטומציה — sleep מול polling:**

```python
# BAD - either too slow, or flaky when the device is late
time.sleep(10)
assert device.is_ready()

# GOOD - returns as soon as the condition holds, fails fast on timeout
def wait_until(condition, timeout=10, interval=0.5):
    """Poll a condition until it is True or the timeout expires."""
    end = time.time() + timeout
    while time.time() < end:
        if condition():
            return True
        time.sleep(interval)
    return False

assert wait_until(device.is_ready, timeout=10), "Device never became ready"
```

זו התשובה המלאה לשאלה "איך מטפלים בטסטים flaky?" — המתנה קבועה מוחלפת ב-polling עם timeout. אותו עיקרון בדיוק כמו `WebDriverWait` ב-selenium.

## 46. threading, multiprocessing וה-GIL

```python
# I/O-bound (network, files, serial) - threads help
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(fetch_url, urls))

# CPU-bound (heavy computation) - processes, not threads
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor() as executor:
    results = list(executor.map(heavy_calc, data))
```

```python
import threading

lock = threading.Lock()
counter = 0

def increment():
    global counter
    with lock:              # protects the critical section
        counter += 1

t = threading.Thread(target=increment)
t.start()
t.join()                    # wait for it to finish
```

**ה-GIL — שאלת ראיון קלאסית:** ב-CPython יש נעילה גלובלית שמאפשרת רק thread אחד להריץ bytecode בכל רגע. לכן threads **לא** מאיצים חישובים כבדים, אבל **כן** עוזרים ל-I/O — כי ה-GIL משתחרר בזמן המתנה לרשת, לדיסק או לפורט סריאלי. לחישוב מקבילי אמיתי צריך processes, שלכל אחד מהם GIL משלו.

**כלל אצבע:** I/O-bound ← threads או async. CPU-bound ← processes.

## 47. מבנה פרויקט אוטומציה ו-CI

```
project/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── devices.py
│       └── protocols.py
├── tests/
│   ├── conftest.py          # shared fixtures
│   ├── test_devices.py
│   └── test_protocols.py
├── config/
│   └── config.yaml
├── requirements.txt
├── pytest.ini
├── pyproject.toml
└── README.md
```

**GitHub Actions — CI בסיסי:**

```yaml
# .github/workflows/tests.yml
name: tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: ruff check .
      - run: pytest --cov=src --cov-report=xml
```

**Jenkins** נפוץ מאוד בתעשייה הביטחונית (מערכות סגורות בלי גישה לענן). הרעיון זהה: על כל commit — התקנה, lint, טסטים, דוח. מספיק להכיר את המושג pipeline ואת השלבים.

## 48. מונחים שיישאלו בראיון

| מונח | מה זה |
|---|---|
| **Flaky test** | טסט שלפעמים עובר ולפעמים נכשל בלי שינוי בקוד — בד"כ תזמון או תלות בין טסטים |
| **Test isolation** | כל טסט עצמאי — לא תלוי בסדר ההרצה או בתוצאות של אחרים |
| **Smoke test** | סט קצר שבודק שהמערכת בכלל עלתה ומגיבה |
| **Regression test** | סט מלא שמוודא ששינוי לא שבר משהו קיים |
| **Sanity test** | בדיקה ממוקדת אחרי תיקון ספציפי |
| **Test coverage** | אחוז הקוד שהטסטים עוברים בו — מדד לכמות, **לא** לאיכות |
| **Fixture** | הכנה וניקוי משותפים לטסטים |
| **Mock / Stub / Fake** | תחליף לתלות חיצונית: mock מאמת קריאות, stub מחזיר ערך קבוע, fake הוא מימוש פשוט אמיתי |
| **AAA** | Arrange-Act-Assert — מבנה של טסט טוב |
| **TDD** | כותבים טסט **לפני** הקוד |
| **BDD** | טסטים בשפה עסקית (Given-When-Then) |
| **Page Object Model** | כל מסך הוא מחלקה — מפריד לוגיקת טסט מסלקטורים |
| **HIL** | Hardware In the Loop — בדיקה עם חומרה אמיתית בלולאה |
| **CI/CD** | הרצה אוטומטית של בנייה וטסטים על כל commit |
| **Shift left** | להזיז בדיקות מוקדם ככל האפשר בתהליך הפיתוח |

## 49. ספריות — מפת דרכים

| ספרייה | לְמה | סעיף |
|---|---|---|
| `pytest` | פריימוורק הטסטים המרכזי | 32 |
| `unittest` | הפריימוורק המובנה | 33 |
| `unittest.mock` | mocking | 34 |
| `pytest-cov` | דוחות כיסוי | 32 |
| `pytest-xdist` | הרצה מקבילה | 32 |
| `pytest-html` / `allure-pytest` | דוחות | 32 |
| `pytest-asyncio` | בדיקת קוד async | 61 |
| `requests` | בדיקות HTTP/API | 35 |
| `httpx` / `aiohttp` | HTTP אסינכרוני | 60 |
| `socket` | TCP/UDP גולמי | 36 |
| `pyserial` | תקשורת סריאלית UART | 37 |
| `scapy` | בניית וניתוח חבילות רשת | — |
| `selenium` / `playwright` | אוטומציית דפדפן | 38 |
| `robotframework` | בדיקות מבוססות מילות מפתח | 39 |
| `paramiko` | SSH ו-SFTP | 40 |
| `pandas` | ניתוח תוצאות ונתונים טבלאיים | — |
| `faker` | יצירת נתוני בדיקה סינתטיים | — |
| `ruff` | lint ופורמט | 29 |
| `mypy` | בדיקת טיפוסים סטטית | 25 |
| `pydantic` | אימות config ונתונים חיצוניים | 79 |
| `hypothesis` | בדיקות מבוססות תכונות | 80 |
| `tenacity` | retry עם backoff | 81 |
| `httpx` | HTTP סינכרוני ואסינכרוני | 82 |
| `rich` / `typer` | פלט טרמינל ו-CLI | 83 |
| `loguru` | לוגינג בלי הגדרות | 84 |
| `freezegun` / `responses` | מוקינג זמן ו-HTTP | 85 |
| `numpy` / `pandas` | ניתוח נתוני מדידה ותוצאות | 87 |
| `uv` / `poetry` | ניהול תלויות ונעילת גרסאות | 88 |

---

# חלק ה' — asyncio

## 50. מה זה async ולמה הוא קיים

תוכנית שמדברת עם רשת, דיסק או חומרה מבזבזת את רוב זמנה ב**המתנה**. `async` מאפשר לה לעשות דברים אחרים בזמן ההמתנה — **בלי thread נוסף**.

```python
# Synchronous: 3 requests, 1 second each = 3 seconds
for url in urls:
    requests.get(url)          # blocks - nothing else can happen

# Asynchronous: the same 3 requests = ~1 second
await asyncio.gather(*[fetch(url) for url in urls])
```

**איך זה עובד:** יש **event loop** — לולאה שמנהלת תור משימות. כשמשימה מגיעה ל-`await`, היא אומרת ללולאה "אני ממתינה, קחי מישהו אחר". הלולאה מריצה משימה אחרת, וכשהתשובה מגיעה היא חוזרת לראשונה. הכל ב-**thread אחד**.

| | threading | asyncio |
|---|---|---|
| מי מחליף משימות | מערכת ההפעלה (preemptive) | הקוד עצמו ב-`await` (cooperative) |
| מספר threads | הרבה | אחד |
| עלות מעבר | יקר (context switch) | זול מאוד |
| נקודות החלפה | בכל מקום — צריך locks | רק ב-`await` — פחות race conditions |
| כמות משימות סבירה | מאות | עשרות אלפים |

**המשפט לראיון:** async נותן **concurrency** (משימות מתקדמות לסירוגין) ולא **parallelism** (משימות רצות ממש בו-זמנית). מושלם ל-I/O, לא עוזר בכלל ל-CPU.

## 51. `async def` ו-`await`

```python
import asyncio

async def say_hello():           # a COROUTINE FUNCTION
    print("start")
    await asyncio.sleep(1)       # yields control back to the event loop
    print("end")

coro = say_hello()               # nothing printed! just a coroutine object
asyncio.run(coro)                # NOW it runs
```

**שלושה כללים:**

1. `await` מותר **רק** בתוך `async def`.
2. קריאה ל-`async def` בלי `await` לא מריצה כלום — פייתון תזהיר `coroutine was never awaited`.
3. `await` אפשרי רק על **awaitable**: coroutine, Task או Future.

```python
async def main():
    say_hello()          # WRONG - RuntimeWarning, nothing happens
    await say_hello()    # RIGHT
```

## 52. `asyncio.run` — נקודת הכניסה

```python
async def main():
    await do_something()

asyncio.run(main())      # creates the loop, runs, closes it cleanly
```

קוראים לו **פעם אחת** בתוכנית, מהקוד הסינכרוני. זו הדרך המודרנית — `get_event_loop()` ו-`run_until_complete()` הם סגנון ישן שיצא משימוש.

## 53. `gather` — הפונקציה הכי חשובה

מריצה כמה coroutines **במקביל** ומחכה לכולן.

```python
async def fetch(n):
    await asyncio.sleep(n)
    return f"done in {n}s"

async def main():
    results = await asyncio.gather(fetch(1), fetch(2), fetch(3))
    print(results)     # ['done in 1s', 'done in 2s', 'done in 3s']  - total 3s, not 6s
```

**התוצאות חוזרות בסדר שנקראו**, לא בסדר שהסתיימו.

```python
tasks = [fetch(url) for url in urls]
results = await asyncio.gather(*tasks)              # note the *

# By default, one exception cancels everything and propagates
results = await asyncio.gather(*tasks, return_exceptions=True)
for r in results:
    if isinstance(r, Exception):
        logger.error(f"Task failed: {r}")           # exceptions come back AS results
```

**המלכודת הכי נפוצה — זה לא מקבילי:**

```python
# WRONG - awaiting one at a time is SEQUENTIAL: 6 seconds
for n in [1, 2, 3]:
    await fetch(n)

# RIGHT - 3 seconds
await asyncio.gather(*[fetch(n) for n in [1, 2, 3]])
```

זה באג שקט — הקוד עובד נכון, רק לאט, ואף אחד לא מקבל שגיאה.

## 54. Tasks — `create_task`

`gather` מתאים כשמחכים לכולם יחד. `create_task` מתאים כשרוצים **להתחיל** משימה ולהמשיך.

```python
async def main():
    task = asyncio.create_task(fetch(2))     # starts running IMMEDIATELY

    print("doing other work meanwhile...")
    await do_something_else()

    result = await task                       # collect the result when needed
```

**ההבדל:**
- coroutine (`fetch(2)`) — מתכון. לא רץ עד ש-`await` נוגע בו.
- Task (`create_task(fetch(2))`) — כבר רץ ברקע מרגע היצירה.

```python
task.done()          # has it finished?
task.result()        # the return value (raises if not done)
task.cancel()        # request cancellation
task.exception()     # the exception, if it failed
```

**אזהרה:** תמיד לשמור הפניה ל-Task במשתנה. אחרת ה-garbage collector עלול לאסוף אותה באמצע הריצה.

## 55. TaskGroup — הדרך המודרנית (3.11+)

```python
async def main():
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(fetch(1))
        t2 = tg.create_task(fetch(2))
    # exiting the block waits for ALL tasks automatically
    print(t1.result(), t2.result())
```

היתרון על `gather`: אם משימה נכשלת, **כל השאר מבוטלות אוטומטית** והשגיאות נאספות יחד. זה הסטנדרט החדש, שנקרא structured concurrency.

## 56. timeout

```python
# Python 3.11+
try:
    async with asyncio.timeout(5):
        await slow_operation()
except TimeoutError:
    logger.error("Operation timed out")

# Older versions
try:
    result = await asyncio.wait_for(slow_operation(), timeout=5)
except asyncio.TimeoutError:
    logger.error("Operation timed out")
```

בקוד אוטומציה זה **חובה** — בלי timeout, פעולה תקועה תולה את כל ה-suite. בדיוק כמו `timeout=` ב-`requests` וב-`pyserial`.

## 57. `sleep` — ולמה `time.sleep` הורס הכל

```python
await asyncio.sleep(1)     # CORRECT - yields control, other tasks keep running
time.sleep(1)              # WRONG - freezes the ENTIRE event loop
```

זו הטעות הנפוצה ביותר ב-async. **כל** פעולה חוסמת — `time.sleep`, `requests.get`, קריאת קובץ סינכרונית, `ser.readline()`, חישוב כבד — עוצרת את הלולאה כולה, ואז אין שום יתרון ל-async.

```python
# If you MUST call blocking code, push it to a thread
result = await asyncio.to_thread(blocking_function, arg1, arg2)
```

## 58. טבלת פונקציות `asyncio`

| פונקציה | מה עושה |
|---|---|
| `asyncio.run(coro)` | מריץ תוכנית async מההתחלה |
| `asyncio.gather(*coros)` | מריץ במקביל, מחזיר את כל התוצאות |
| `asyncio.create_task(coro)` | מתחיל משימה ברקע מיד |
| `asyncio.sleep(n)` | המתנה לא-חוסמת |
| `asyncio.wait_for(coro, timeout)` | מגביל זמן לפעולה |
| `asyncio.timeout(n)` | אותו דבר כ-context manager (3.11+) |
| `asyncio.TaskGroup()` | ניהול קבוצת משימות (3.11+) |
| `asyncio.wait(tasks, return_when=...)` | המתנה עם תנאי עצירה |
| `asyncio.as_completed(tasks)` | תוצאות **בסדר הסיום** |
| `asyncio.to_thread(func, *args)` | מריץ פונקציה חוסמת ב-thread |
| `asyncio.shield(coro)` | מגן על משימה מביטול |
| `asyncio.current_task()` | ה-Task הנוכחי |
| `asyncio.all_tasks()` | כל המשימות הפעילות |

```python
# as_completed - handle each result the moment it arrives
for coro in asyncio.as_completed(tasks):
    result = await coro
    print(f"got: {result}")          # fastest first

# wait - stop at the first completion
done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
for task in pending:
    task.cancel()
```

## 59. כלי סנכרון

```python
# Lock - one task at a time in the critical section
lock = asyncio.Lock()
async with lock:
    shared_counter += 1

# Semaphore - limit how many run at once
sem = asyncio.Semaphore(10)
async def fetch_limited(url):
    async with sem:                  # at most 10 concurrent requests
        return await fetch(url)

# Event - one task signals, others wait
event = asyncio.Event()
await event.wait()       # blocks until...
event.set()              # ...someone sets it

# Queue - producer/consumer
queue = asyncio.Queue()
await queue.put(item)
item = await queue.get()
queue.task_done()
await queue.join()       # wait until the queue is fully processed
```

**`Semaphore` הוא הכלי הכי שימושי מהרשימה** — בלעדיו 10,000 בקשות בו-זמנית יפילו את השרת, את הרשת, או את המכשיר שנבדק.

## 60. async context managers, iterators וגנרטורים

```python
# async with - when setup/teardown are themselves async
class AsyncConnection:
    async def __aenter__(self):
        self.conn = await connect()
        return self.conn

    async def __aexit__(self, exc_type, exc, tb):
        await self.conn.close()

async with AsyncConnection() as conn:
    await conn.query("SELECT 1")

# async for - iterating an async source
async for line in stream:
    process(line)

# async generator
async def fetch_pages(urls):
    for url in urls:
        yield await fetch(url)

async for page in fetch_pages(urls):
    print(page)
```

**דוגמה מלאה — סורק URL-ים עם כל העקרונות:**

```python
import asyncio
import aiohttp          # pip install aiohttp - the async equivalent of requests


async def fetch_status(session, url, sem):
    """Fetch one URL and return its status, never hanging or crashing the batch."""
    async with sem:                                   # limit concurrency
        try:
            async with asyncio.timeout(10):           # never hang
                async with session.get(url) as resp:
                    return url, resp.status
        except TimeoutError:
            return url, "TIMEOUT"
        except Exception as e:
            return url, f"ERROR: {e}"


async def check_all(urls, max_concurrent=10):
    sem = asyncio.Semaphore(max_concurrent)
    async with aiohttp.ClientSession() as session:    # one shared session
        tasks = [fetch_status(session, url, sem) for url in urls]
        return await asyncio.gather(*tasks)


if __name__ == "__main__":
    results = asyncio.run(check_all(["https://example.com"] * 100))
    for url, status in results:
        print(f"{status}: {url}")
```

## 61. בדיקת קוד async ב-pytest

```python
# pip install pytest-asyncio

import pytest

@pytest.mark.asyncio
async def test_fetch_returns_data():
    result = await fetch("https://example.com")
    assert result is not None


@pytest.mark.asyncio
async def test_timeout_is_raised():
    with pytest.raises(TimeoutError):
        async with asyncio.timeout(0.1):
            await asyncio.sleep(10)


@pytest_asyncio.fixture
async def client():
    async with aiohttp.ClientSession() as session:
        yield session
```

## 62. מלכודות async — לקרוא לפני ראיון

1. **`time.sleep` במקום `await asyncio.sleep`** — מקפיא את כל הלולאה.
2. **`requests` במקום `aiohttp`** — `requests` חוסמת. הספריות ה-async: `aiohttp`, `httpx`, `aiofiles`, `asyncpg`.
3. **`await` בלולאה במקום `gather`** — הופך מקבילי לסדרתי. הבאג הכי שקט.
4. **שכחת `await`** — הפונקציה פשוט לא רצה, בלי שגיאה בולטת.
5. **לא שומרים הפניה ל-Task** — עלולה להיאסף על ידי ה-GC.
6. **חישוב CPU כבד ב-async** — ה-loop לא עוזר. זה מקרה ל-`ProcessPoolExecutor`.
7. **בלי `Semaphore`** — עומס בו-זמני מפיל את היעד.
8. **בלי timeout** — משימה תקועה תולה את הכל.

---

# חלק ו' — תבניות קוד לראיון

## 63. תבניות שחוזרות בשאלות אלגוריתמיקה

```python
# Two pointers - sorted arrays, palindromes, pair sums
left, right = 0, len(arr) - 1
while left < right:
    if arr[left] + arr[right] == target:
        return left, right
    elif arr[left] + arr[right] < target:
        left += 1
    else:
        right -= 1


# Sliding window - subarrays of fixed size
window_sum = sum(arr[:k])
best = window_sum
for i in range(k, len(arr)):
    window_sum += arr[i] - arr[i - k]     # add new, remove old - O(1) per step
    best = max(best, window_sum)


# Frequency map - anagrams, duplicates, most common
from collections import Counter
freq = Counter(items)
most = freq.most_common(1)[0][0]


# Grouping by a computed key
from collections import defaultdict
groups = defaultdict(list)
for word in words:
    groups["".join(sorted(word))].append(word)     # anagram signature


# BFS - shortest path, level order
from collections import deque
queue = deque([start])
visited = {start}
while queue:
    node = queue.popleft()
    for neighbor in graph[node]:
        if neighbor not in visited:
            visited.add(neighbor)
            queue.append(neighbor)


# DFS - recursive
def dfs(node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, visited)
    return visited


# Binary search
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

import bisect
bisect.bisect_left(sorted_arr, x)        # built-in, use it when allowed
```

## 64. טריקים קצרים

```python
a, b = b, a                              # swap
result = "yes" if condition else "no"    # ternary
first, *rest = [1, 2, 3, 4]              # unpacking

if not lst:            # pythonic empty check, instead of len(lst) == 0
if lst:

best = float('inf')    # starting value for a minimum search
best = float('-inf')   # for a maximum

# Walrus operator - assign and test in one expression (3.8+)
if (match := pattern.search(line)) is not None:
    print(match.group(1))

while (chunk := f.read(1024)):
    process(chunk)

# Chained comparison
if 0 <= x <= 100:      # instead of x >= 0 and x <= 100

# Multiple return values
def stats(nums):
    return min(nums), max(nums), sum(nums) / len(nums)
low, high, avg = stats(data)
```


---

# חלק ז' — חומרה, פרוטוקולים וכלים

## 65. bytes, ביטים ו-endianness

עבודה מול חומרה היא עבודה מול **בייטים**, לא מחרוזות.

```python
b = b"\x01\x02\xFF"        # bytes literal - immutable
ba = bytearray(b)          # mutable version
ba[0] = 0x99               # can be modified in place

b"abc".hex()               # '616263'
bytes.fromhex("616263")    # b'abc'
list(b"abc")               # [97, 98, 99] - each byte as an int
b[0]                       # 97 - indexing a bytes gives an INT, not bytes
b[0:1]                     # b'a' - slicing gives bytes
```

**המרות int ↔ bytes:**

```python
(1024).to_bytes(2, "big")           # b'\x04\x00'   - big-endian
(1024).to_bytes(2, "little")        # b'\x00\x04'   - little-endian
int.from_bytes(b"\x04\x00", "big")  # 1024
```

**Endianness — סדר הבייטים:**

| | סדר | מי משתמש |
|---|---|---|
| **big-endian** | הבייט המשמעותי ראשון | פרוטוקולי רשת ("network byte order"), MIL-STD-1553 |
| **little-endian** | הבייט הפחות משמעותי ראשון | x86, ARM (רוב המעבדים) |

המספר `0x1234` נשלח כ-`12 34` ב-big-endian וכ-`34 12` ב-little-endian. **התאמה שגויה של endianness היא מקור באגים ענק** בעבודה מול חומרה — הנתונים מתקבלים אבל הערכים חסרי היגיון.

**פעולות על ביטים:**

```python
a & b        # AND  - masking: which bits are set in both
a | b        # OR   - setting bits
a ^ b        # XOR  - toggling, and simple checksums
~a           # NOT
a << 2       # shift left  = multiply by 4
a >> 2       # shift right = divide by 4

# Common patterns
value & 0xFF              # keep only the low byte
value & (1 << 3)          # is bit 3 set?
value | (1 << 3)          # set bit 3
value & ~(1 << 3)         # clear bit 3
value ^ (1 << 3)          # toggle bit 3
(value >> 4) & 0x0F       # extract bits 4-7

bin(0b1010 & 0b0110)      # '0b10'
format(value, "08b")      # '00001010' - padded binary string
```

**Checksum פשוט — מופיע כמעט בכל פרוטוקול סריאלי:**

```python
def xor_checksum(data: bytes) -> int:
    """Many serial protocols use a simple XOR of all bytes."""
    checksum = 0
    for byte in data:
        checksum ^= byte
    return checksum

def verify(frame: bytes) -> bool:
    return xor_checksum(frame[:-1]) == frame[-1]
```

## 66. struct — פרוטוקולים בינאריים

הספרייה שממירה בין בייטים גולמיים לערכים בפייתון. **חיונית לכל פרוטוקול בינארי.**

```python
import struct

# pack: values -> bytes
data = struct.pack(">HBI", 1024, 5, 999999)     # 2+1+4 = 7 bytes

# unpack: bytes -> tuple of values
msg_id, status, timestamp = struct.unpack(">HBI", data)

struct.calcsize(">HBI")      # 7 - how many bytes this format needs
```

**תווי הפורמט:**

| תו | טיפוס | גודל |
|---|---|---|
| `b` / `B` | int8 / uint8 | 1 |
| `h` / `H` | int16 / uint16 | 2 |
| `i` / `I` | int32 / uint32 | 4 |
| `q` / `Q` | int64 / uint64 | 8 |
| `f` / `d` | float / double | 4 / 8 |
| `s` | מחרוזת bytes | `10s` = 10 בייטים |
| `x` | בייט ריפוד | 1 |
| `?` | bool | 1 |

**קידומת ה-endianness — קריטית:**

| קידומת | משמעות |
|---|---|
| `>` | big-endian, בלי ריפוד |
| `<` | little-endian, בלי ריפוד |
| `!` | network order (זהה ל-`>`) |
| `=` | סדר המערכת, בלי ריפוד |
| ללא | סדר המערכת **עם ריפוד** ← נמנעים מזה |

**תמיד לציין קידומת מפורשת.** בלעדיה פייתון מוסיפה ריפוד יישור (alignment padding) שישבור את הפרוטוקול.

**דוגמה מלאה — פריקת frame של מכשיר:**

```python
import struct
from dataclasses import dataclass

FRAME_FORMAT = ">BHIfB"        # sync, msg_id, timestamp, value, checksum
FRAME_SIZE = struct.calcsize(FRAME_FORMAT)     # 12 bytes
SYNC_BYTE = 0xAA


@dataclass
class TelemetryFrame:
    msg_id: int
    timestamp: int
    value: float


def parse_frame(raw: bytes) -> TelemetryFrame:
    """Parse and validate one telemetry frame."""
    if len(raw) != FRAME_SIZE:
        raise ValueError(f"Frame must be {FRAME_SIZE} bytes, got {len(raw)}")

    sync, msg_id, timestamp, value, checksum = struct.unpack(FRAME_FORMAT, raw)

    if sync != SYNC_BYTE:
        raise ValueError(f"Bad sync byte: expected {SYNC_BYTE:#x}, got {sync:#x}")

    if xor_checksum(raw[:-1]) != checksum:
        raise ValueError("Checksum mismatch - frame corrupted")

    return TelemetryFrame(msg_id, timestamp, value)


def build_frame(msg_id: int, timestamp: int, value: float) -> bytes:
    """Build a frame with a correct checksum."""
    body = struct.pack(">BHIf", SYNC_BYTE, msg_id, timestamp, value)
    return body + bytes([xor_checksum(body)])
```

זו דוגמה שמשלבת struct, checksum, validation ו-dataclass — בדיוק מה שנראה בקוד אמיתי של בדיקת חומרה, ודוגמה מצוינת להביא לראיון.

**`iter_unpack` — לפרסר זרם של frames:**

```python
for frame in struct.iter_unpack(">HBI", stream_bytes):
    process(frame)
```

## 67. pyvisa — מכשירי מדידה (SCPI)

התקן לשליטה באוסילוסקופים, ספקי כוח, מחוללי אותות ומודדים — דרך USB, GPIB, LAN או סריאלי.

```python
import pyvisa

rm = pyvisa.ResourceManager()
print(rm.list_resources())
# ('USB0::0x0957::0x1798::MY12345::INSTR', 'TCPIP0::192.168.1.50::INSTR')

with rm.open_resource("TCPIP0::192.168.1.50::INSTR") as scope:
    scope.timeout = 5000                # milliseconds

    print(scope.query("*IDN?"))         # identify the instrument
    scope.write("*RST")                 # reset to a known state
    scope.write("CHAN1:SCAL 0.5")       # set vertical scale
    voltage = float(scope.query("MEAS:VPP? CHAN1"))
    print(f"Peak-to-peak: {voltage} V")
```

**שלוש הפעולות היחידות שצריך:**

| פעולה | מה עושה |
|---|---|
| `inst.write(cmd)` | שולח פקודה, לא מצפה לתשובה |
| `inst.read()` | קורא תשובה |
| `inst.query(cmd)` | write + read יחד — הכי נפוץ |

**SCPI — שפת הפקודות התקנית:**

```
*IDN?              identify: manufacturer, model, serial, firmware
*RST               reset to defaults
*CLS               clear status and error queue
*OPC?              operation complete? - blocks until the device is ready
SYST:ERR?          read the next error from the queue
MEAS:VOLT:DC?      measure DC voltage
```

**כלל: פקודה שנגמרת ב-`?` היא שאילתה** (משתמשים ב-`query`), אחרת היא פקודה (`write`).

```python
# Standard safe pattern
def measure_voltage(inst) -> float:
    inst.write("*CLS")
    inst.write("MEAS:VOLT:DC?")
    inst.query("*OPC?")                        # wait until ready
    value = float(inst.read())

    error = inst.query("SYST:ERR?")             # ALWAYS check the error queue
    if not error.startswith("+0"):
        raise InstrumentError(f"Instrument reported: {error}")
    return value
```

**נקודה שמפילה:** אחרי כל פקודה כדאי לבדוק `SYST:ERR?`. מכשירים לרוב **לא מתלוננים** על פקודה שגויה — הם פשוט מתעלמים, ואת מקבלת מדידה מהמצב הקודם בלי לדעת.

**בדיקה בלי מכשיר — mock:**

```python
@patch("mymodule.pyvisa.ResourceManager")
def test_measure(mock_rm):
    mock_inst = mock_rm.return_value.open_resource.return_value
    mock_inst.query.side_effect = ["1", "3.14", "+0,\"No error\""]

    assert measure_voltage(mock_inst) == 3.14
```

## 68. python-can — CAN bus

```python
import can

with can.Bus(interface="socketcan", channel="can0", bitrate=500000) as bus:

    # Send
    msg = can.Message(arbitration_id=0x123, data=[0x01, 0x02, 0x03], is_extended_id=False)
    bus.send(msg, timeout=1.0)

    # Receive one message
    received = bus.recv(timeout=5.0)
    if received:
        print(f"ID={received.arbitration_id:#x} data={received.data.hex()}")

    # Listen continuously
    for msg in bus:
        if msg.arbitration_id == 0x123:
            process(msg.data)
```

**מושגים:**

| מונח | מה זה |
|---|---|
| `arbitration_id` | מזהה ההודעה — קובע גם **עדיפות** (נמוך = עדיף) |
| `data` | עד 8 בייטים (64 ב-CAN FD) |
| `is_extended_id` | 11 ביט (סטנדרטי) מול 29 ביט (מורחב) |
| `bitrate` | חייב להיות זהה בכל הצמתים |
| `dbc` | קובץ שמתאר איך לפרש את הבייטים לאותות |

```python
# Virtual bus - test CAN logic with no hardware at all
with can.Bus(interface="virtual", channel="test") as bus:
    bus.send(can.Message(arbitration_id=0x1, data=[1, 2]))
```

ה-`virtual` interface מאפשר לפתח ולבדוק לוגיקת CAN בלי מעבדה — בדיוק כמו mock, רק שזה מנגנון מובנה של הספרייה.

## 69. scapy — בניית וניתוח חבילות רשת

```python
from scapy.all import IP, TCP, ICMP, Ether, send, sr1, sniff, rdpcap, wrpcap

# Build a packet layer by layer with /
packet = IP(dst="192.168.1.10") / TCP(dport=80, flags="S")

response = sr1(packet, timeout=2)      # send and receive one reply
if response:
    response.show()

# Ping
reply = sr1(IP(dst="8.8.8.8") / ICMP(), timeout=2)

# Capture traffic
packets = sniff(filter="tcp port 80", count=10, timeout=30)
for pkt in packets:
    if pkt.haslayer(TCP):
        print(pkt[IP].src, "->", pkt[IP].dst)

# pcap files - open them in Wireshark afterwards
wrpcap("capture.pcap", packets)
packets = rdpcap("capture.pcap")
```

**למה זה שימושי בבדיקות:** אפשר לשלוח חבילות **פגומות בכוונה** ולבדוק שהמערכת מטפלת בהן נכון — שדה באורך שגוי, checksum שבור, דגלים לא חוקיים. זו בדיקת robustness שאי אפשר לעשות עם socket רגיל.

`filter=` משתמש בתחביר BPF — אותו תחביר כמו ב-Wireshark ו-tcpdump.

## 70. argparse — כלי שורת פקודה

```python
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Run device verification tests",
    )
    parser.add_argument("port", help="Serial port, e.g. /dev/ttyUSB0")
    parser.add_argument("-b", "--baudrate", type=int, default=115200)
    parser.add_argument("-t", "--timeout", type=float, default=5.0)
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--mode", choices=["fast", "full"], default="fast")
    parser.add_argument("--tests", nargs="+", help="Specific tests to run")

    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    run_tests(args.port, args.baudrate, args.mode)


if __name__ == "__main__":
    main()
```

```bash
python run_tests.py /dev/ttyUSB0 --baudrate 9600 --mode full -v
python run_tests.py --help        # generated automatically
```

| פרמטר | מה עושה |
|---|---|
| שם ללא `-` | ארגומנט חובה, לפי מיקום |
| `-x` / `--name` | אופציונלי |
| `type=int` | המרה ואימות אוטומטיים |
| `action="store_true"` | דגל בוליאני |
| `choices=[...]` | מגביל לערכים מותרים |
| `nargs="+"` | אוסף כמה ערכים לרשימה |
| `required=True` | הופך אופציונלי לחובה |

היתרון: `--help` ואימות הקלט נוצרים לבד. זה גם **input validation בחינם** — `type=int` יפסול קלט לא תקין לפני שהוא מגיע ללוגיקה.

## 71. SQL ו-sqlite3

```python
import sqlite3

with sqlite3.connect("results.db") as conn:
    conn.row_factory = sqlite3.Row          # access columns by name
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS test_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            status TEXT NOT NULL,
            duration REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # NEVER use f-strings here - always parameters
    cur.execute(
        "INSERT INTO test_runs (device_id, status, duration) VALUES (?, ?, ?)",
        ("device_7", "PASSED", 12.4),
    )
    cur.executemany("INSERT INTO test_runs (device_id, status) VALUES (?, ?)", rows)
    conn.commit()

    cur.execute("SELECT * FROM test_runs WHERE status = ?", ("FAILED",))
    for row in cur.fetchall():
        print(row["device_id"], row["duration"])
```

**SQL injection — שאלת secure code כמעט מובטחת:**

```python
# CATASTROPHIC - if device_id is "x'; DROP TABLE test_runs; --"
cur.execute(f"SELECT * FROM test_runs WHERE device_id = '{device_id}'")

# SAFE - the driver escapes the value; it can never become code
cur.execute("SELECT * FROM test_runs WHERE device_id = ?", (device_id,))
```

הפרמטר נשלח **בנפרד** מהשאילתה, ולכן לעולם לא מתפרש כפקודה. זה ההסבר שרוצים לשמוע, לא רק "משתמשים ב-?".

**SQL בסיסי שנשאל בראיונות:**

```sql
SELECT device_id, COUNT(*) AS failures
FROM test_runs
WHERE status = 'FAILED'
GROUP BY device_id
HAVING COUNT(*) > 3
ORDER BY failures DESC
LIMIT 10;

-- JOIN: combine rows from two tables
SELECT r.device_id, d.model
FROM test_runs r
JOIN devices d ON r.device_id = d.id;          -- INNER: only matching rows
LEFT JOIN devices d ON r.device_id = d.id;     -- keeps all rows from the left

UPDATE test_runs SET status = 'RETRY' WHERE id = 5;
DELETE FROM test_runs WHERE created_at < '2026-01-01';
```

**`WHERE` מול `HAVING`:** `WHERE` מסנן **שורות לפני** הקיבוץ, `HAVING` מסנן **קבוצות אחרי** הקיבוץ. שאלה קלאסית.

**סדר הביצוע האמיתי** (לא סדר הכתיבה): `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`. זה מסביר למה אי אפשר להשתמש ב-alias מ-`SELECT` בתוך `WHERE`.

---

# חלק ח' — תיאוריה: QA, עיצוב ומודל הזיכרון

## 72. פירמידת הבדיקות

```
        /\        E2E  - few, slow, brittle, but closest to the real user
       /  \
      /----\      Integration - moderate count, tests components together
     /      \
    /--------\    Unit - many, fast, isolated, cheap to maintain
```

| רמה | מה נבדק | מהירות | כמות |
|---|---|---|---|
| **Unit** | פונקציה או מחלקה בבידוד | מילישניות | מאות-אלפים |
| **Integration** | כמה רכיבים יחד (קוד + DB, קוד + מכשיר) | שניות | עשרות |
| **E2E / System** | המערכת כולה מקצה לקצה | דקות | בודדים |

**למה פירמידה ולא ריבוע:** טסטי E2E איטיים, שבירים, וקשה לאבחן מהם מה נשבר. טסט יחידה שנכשל מצביע על שורה; טסט E2E שנכשל אומר "משהו במערכת". לכן הרוב למטה.

**אנטי-פאטרן — "גביע גלידה" הפוך:** הרבה E2E וכמעט אין unit. התוצאה: suite שרץ שעתיים, נכשל אקראית, ואף אחד לא סומך עליו.

**מונחים נלווים:**

| מונח | מה זה |
|---|---|
| **HIL** | Hardware In the Loop — המערכת נבדקת מול חומרה אמיתית בלולאה סגורה |
| **SIL** | Software In the Loop — החומרה מדומה בתוכנה |
| **Sanity** | בדיקה ממוקדת אחרי תיקון ספציפי |
| **Smoke** | בדיקה קצרה שהמערכת בכלל עלתה |
| **Acceptance** | הלקוח מאשר שהדרישות מתקיימות |

## 73. איך בוחרים מה לבדוק

זו התיאוריה שמבדילה בין "כתבתי טסטים" ל"כיסיתי את הסיכונים". נשאל בראיונות QA.

**Equivalence Partitioning — חלוקה למחלקות שקילות**

מחלקים את מרחב הקלט לקבוצות שמתנהגות אותו דבר, ובודקים **נציג אחד מכל קבוצה**.

```
Deck size, valid range 1-13:
  invalid low:   -5, 0     -> one test is enough
  valid:         7         -> one test represents 1..13
  invalid high:  20        -> one test is enough
```

במקום 13 טסטים — שלושה. אותו כיסוי סיכון, עשירית העבודה.

**Boundary Value Analysis — ערכי גבול**

באגים מתחבאים בקצוות, לא באמצע. לכל גבול בודקים שלוש נקודות: **מתחת, על, ומעל**.

```python
@pytest.mark.parametrize("size,valid", [
    (0,  False),   # just below the boundary
    (1,  True),    # ON the boundary
    (2,  True),    # just above
    (12, True),    # just below the upper boundary
    (13, True),    # ON the upper boundary
    (14, False),   # just above
])
def test_deck_size_boundaries(size, valid):
    ...
```

**off-by-one הוא הבאג הנפוץ ביותר בתוכנה**, ו-BVA נועד בדיוק לתפוס אותו.

**Decision Table — טבלת החלטה**

כשיש כמה תנאים שמשפיעים יחד:

| מחובר | מאומת | הרשאה | תוצאה צפויה |
|---|---|---|---|
| לא | — | — | שגיאת חיבור |
| כן | לא | — | שגיאת אימות |
| כן | כן | לא | שגיאת הרשאה |
| כן | כן | כן | הצלחה |

הטבלה מבטיחה שלא שכחת שילוב. כל שורה הופכת ל-parametrize אחד.

**State Transition Testing**

למערכות עם מצבים (מכשיר, חיבור, מכונת מצבים):

```
IDLE --connect--> CONNECTING --ok--> READY --command--> BUSY
                       |                                  |
                       +--timeout--> ERROR <--fail--------+
```

בודקים גם מעברים חוקיים **וגם מעברים לא חוקיים** — למשל שליחת פקודה במצב `IDLE` צריכה להיכשל בצורה מסודרת, לא לקרוס. זה בדיוק סוג הבדיקה שרלוונטי למערכות משובצות.

**Positive מול Negative testing**

- Positive: המערכת עושה מה שצריך עם קלט תקין
- Negative: המערכת **נכשלת נכון** עם קלט לא תקין

מתחילים תמיד עם negative בראיון — זה מה שמראה בגרות. רוב המפתחים בודקים רק את המסלול המאושר.

## 74. SOLID

חמישה עקרונות עיצוב. שווה לדעת להסביר כל אחד במשפט **עם דוגמה**.

**S — Single Responsibility:** למחלקה יש סיבה אחת להשתנות.

```python
# BAD - changes if the protocol changes, OR if the log format changes
class Device:
    def send_command(self): ...
    def write_log_file(self): ...

# GOOD
class Device:
    def send_command(self): ...

class TestLogger:
    def write(self): ...
```

**O — Open/Closed:** פתוח להרחבה, סגור לשינוי.

```python
# BAD - every new device type means editing this function
def run_test(device_type):
    if device_type == "serial": ...
    elif device_type == "can": ...

# GOOD - a new device is a new class, existing code untouched
class DeviceTest(ABC):
    @abstractmethod
    def run(self): ...

class SerialTest(DeviceTest): ...
class CanTest(DeviceTest): ...
```

**L — Liskov Substitution:** אפשר להחליף מחלקת אב ביורשת בלי לשבור כלום.

```python
# VIOLATION - the subclass breaks the parent's contract
class Bird:
    def fly(self): ...

class Penguin(Bird):
    def fly(self):
        raise NotImplementedError    # callers of Bird.fly() now crash
```

**I — Interface Segregation:** עדיף כמה ממשקים קטנים על אחד גדול.

```python
# BAD - a read-only device is forced to implement write()
class Device(ABC):
    def read(self): ...
    def write(self): ...
    def calibrate(self): ...

# GOOD
class Readable(ABC):
    def read(self): ...

class Writable(ABC):
    def write(self): ...
```

**D — Dependency Inversion:** תלות בהפשטה, לא במימוש קונקרטי.

```python
# BAD - impossible to test without a real serial port
class TestRunner:
    def __init__(self):
        self.port = serial.Serial("/dev/ttyUSB0")

# GOOD - inject the dependency; tests pass a mock
class TestRunner:
    def __init__(self, connection):
        self.connection = connection
```

**זו הנקודה שמחברת SOLID לבדיקות:** dependency injection הופך קוד לניתן לבדיקה. אם קשה לך לכתוב טסט לפונקציה — בדרך כלל זו בעיית עיצוב, לא בעיית טסט.

## 75. Design Patterns בפייתון

**Factory — יצירת אובייקטים לפי פרמטר**

```python
class DeviceFactory:
    _devices = {"serial": SerialDevice, "can": CanDevice, "tcp": TcpDevice}

    @classmethod
    def create(cls, kind: str, **config):
        if kind not in cls._devices:
            raise ValueError(f"Unknown device type: {kind}")
        return cls._devices[kind](**config)

device = DeviceFactory.create("serial", port="/dev/ttyUSB0")
```

**Strategy — אלגוריתם מוחלף בזמן ריצה**

```python
class ChecksumStrategy(ABC):
    @abstractmethod
    def compute(self, data: bytes) -> int: ...

class XorChecksum(ChecksumStrategy):
    def compute(self, data): return functools.reduce(operator.xor, data, 0)

class SumChecksum(ChecksumStrategy):
    def compute(self, data): return sum(data) & 0xFF

class Protocol:
    def __init__(self, checksum: ChecksumStrategy):
        self.checksum = checksum          # swappable without touching Protocol
```

**Singleton — מופע יחיד**

```python
class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

בפייתון בדרך כלל **מודול הוא כבר singleton** — הוא נטען פעם אחת ומשותף. לרוב זה מספיק, וזו תשובה טובה בראיון.

**Observer — הודעה לכמה מאזינים**

```python
class EventBus:
    def __init__(self):
        self._subscribers = defaultdict(list)

    def subscribe(self, event: str, callback):
        self._subscribers[event].append(callback)

    def publish(self, event: str, data):
        for callback in self._subscribers[event]:
            callback(data)
```

**Adapter — התאמת ממשק קיים לממשק נדרש**

```python
class LegacyDeviceAdapter:
    """Wraps an old API so it fits the modern Device interface."""
    def __init__(self, legacy):
        self._legacy = legacy

    def read(self) -> bytes:
        return self._legacy.get_data_v1().encode()
```

**Context Manager ו-Decorator** הם דפוסים מובנים בשפה עצמה (סעיפים 17, 19) — שווה לציין את זה בראיון.

## 76. מודל הזיכרון של פייתון

**הכל בפייתון הוא אובייקט**, ומשתנה הוא **שם שמצביע** לאובייקט, לא תא שמכיל ערך.

```python
a = [1, 2, 3]
b = a                # b points to the SAME object
id(a) == id(b)       # True - same memory address
a is b               # True

c = [1, 2, 3]
a == c               # True  - same content
a is c               # False - different objects
```

**Reference counting:** לכל אובייקט יש מונה הפניות. כשהוא מגיע ל-0, הזיכרון משתחרר מיד.

```python
import sys
x = [1, 2, 3]
sys.getrefcount(x)      # count of references (getrefcount itself adds one)
```

**Garbage collector:** reference counting לבדו לא מטפל ב**מחזורים** — אובייקטים שמצביעים זה על זה ואף אחד חיצוני לא מצביע עליהם. לכן יש GC נוסף שמזהה ומשחרר מחזורים.

```python
import gc
gc.collect()        # force a collection cycle
```

**Interning — פייתון ממחזרת אובייקטים קטנים:**

```python
a, b = 256, 256
a is b        # True  - small ints (-5..256) are cached

a, b = 257, 257
a is b        # False in some contexts - NOT cached
```

**זו בדיוק הסיבה להשתמש ב-`==` ולא ב-`is` להשוואת ערכים.** `is` בודק זהות בזיכרון, שהיא פרט מימוש שמשתנה בין גרסאות. היוצא מן הכלל היחיד: `is None`, כי `None` הוא singleton מובטח.

## 77. EAFP מול LBYL

שני סגנונות לטיפול במקרים שעלולים להיכשל — ופייתון מעדיפה בבירור את הראשון.

```python
# LBYL - Look Before You Leap
if "key" in d:
    value = d["key"]

if os.path.exists(path):
    with open(path) as f:       # the file might be deleted in between!
        ...

# EAFP - Easier to Ask Forgiveness than Permission  <- pythonic
try:
    value = d["key"]
except KeyError:
    value = default

try:
    with open(path) as f:
        ...
except FileNotFoundError:
    ...
```

**למה EAFP עדיף:**

1. **אין race condition** — בין הבדיקה לפעולה המצב יכול להשתנות (קובץ נמחק, חיבור נופל). EAFP מבצע ובודק בפעולה אחת.
2. **מהיר יותר במקרה הרגיל** — אם החריגה נדירה, אין עלות בדיקה בכל קריאה.
3. **קורא נקי יותר** — הלוגיקה העיקרית לא קבורה תחת שכבות `if`.

**מתי כן LBYL:** כשהכישלון **צפוי ושכיח** (אז חריגות יקרות), או כשהבדיקה זולה וברורה — למשל `if not lst`.

זה מונח שמראיין פייתון מנוסה ישמח לשמוע ממך בשמו.

## 78. Iterables, iterators וה-for loop

**ההבדל:**
- **Iterable** — משהו שאפשר לעבור עליו. מממש `__iter__`.
- **Iterator** — משהו שזוכר איפה הוא עומד. מממש `__iter__` **ו-**`__next__`.

```python
lst = [1, 2, 3]          # iterable, but NOT an iterator
it = iter(lst)           # now it's an iterator
next(it)                 # 1
next(it)                 # 2
next(it)                 # 3
next(it)                 # StopIteration
```

**מה הלולאה באמת עושה:**

```python
for x in lst:
    print(x)

# is exactly equivalent to:
it = iter(lst)
while True:
    try:
        x = next(it)
    except StopIteration:
        break
    print(x)
```

זה מסביר שני דברים: למה גנרטור נצרך פעם אחת (הוא **הוא** האיטרטור, ואין לו דרך לחזור להתחלה), ולמה שינוי רשימה תוך כדי לולאה משבש אותה (האיטרטור מחזיק אינדקס פנימי).

**לכתוב איטרטור משלך:**

```python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self              # I am my own iterator

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1


for n in Countdown(3):
    print(n)        # 3, 2, 1
```

בפועל, **גנרטור עושה את אותו דבר בשלוש שורות** — ולכן זו כמעט תמיד הבחירה הנכונה:

```python
def countdown(start):
    while start > 0:
        yield start
        start -= 1
```

**מחלקה שניתן לעבור עליה כמה פעמים** — `__iter__` מחזירה איטרטור **חדש** בכל קריאה:

```python
class Deck:
    def __init__(self, cards):
        self.cards = cards

    def __iter__(self):
        return iter(self.cards)      # a fresh iterator every time

    def __len__(self):
        return len(self.cards)

    def __contains__(self, card):
        return card in self.cards
```

שלוש המתודות האלה הופכות את `Deck` לאובייקט שמתנהג כמו אוסף מובנה: `for card in deck`, `len(deck)`, `'A' in deck`. זו דוגמה מצוינת ל-**Pythonic design** להראות בראיון.

---

# חלק ט' — ספריות מודרניות

הספריות בחלק הזה אינן חלק מפייתון עצמה, אבל הן מה שצוותים מקצועיים משתמשים בו היום. כל סעיף מסביר **איזו בעיה הספרייה פותרת** ולא רק איך קוראים לה — כי זו התשובה שמראיין מחפש כששואל "למה בחרת בזה?".

## 79. pydantic — אימות נתונים מובנה

**הבעיה שהיא פותרת:** קובץ config או תשובת API מגיעים כ-dict. אין שום ערובה שהשדות קיימים, שהטיפוסים נכונים, או שהערכים בטווח הגיוני. בלי אימות, `config["timeout"]` יכול להיות המחרוזת `"5"` במקום מספר, והבאג יתגלה רק שלוש שכבות מאוחר יותר, במקום שנראה לגמרי לא קשור.

הדרך הידנית היא לכתוב עשרות `if` בכניסה לכל פונקציה. pydantic עושה את זה מהצהרת טיפוסים אחת.

```python
from pydantic import BaseModel, Field, field_validator
from pathlib import Path
import yaml


class DeviceConfig(BaseModel):
    port: str
    baudrate: int = 115200
    timeout: float = Field(default=5.0, gt=0, le=60)   # must be 0 < x <= 60
    retries: int = Field(default=3, ge=0)
    tags: list[str] = []

    @field_validator("port")
    @classmethod
    def port_must_look_valid(cls, v: str) -> str:
        if not (v.startswith("/dev/") or v.startswith("COM")):
            raise ValueError(f"Port must be a device path, got {v!r}")
        return v


raw = yaml.safe_load(Path("config.yaml").read_text(encoding="utf-8"))
config = DeviceConfig(**raw)      # validates EVERYTHING here, once

config.timeout        # guaranteed to be a float in (0, 60]
config.port           # guaranteed to look like a device path
```

**מה קורה כשמשהו לא תקין:**

```python
DeviceConfig(port="/dev/ttyUSB0", timeout=-1)
# ValidationError: 1 validation error for DeviceConfig
# timeout
#   Input should be greater than 0 [type=greater_than, input_value=-1]
```

השגיאה מדויקת: איזה שדה, מה הכלל שהופר, ומה הערך שהתקבל. זה בדיוק **fail fast עם הודעה שימושית** — העיקרון שחזר לאורך כל הקובץ.

**המרה אוטומטית:** pydantic ממירה `"115200"` ל-`115200` אם הטיפוס המוצהר הוא `int`. זה נוח, אבל שווה לדעת שזה קורה — במצבים שבהם רוצים אכיפה קפדנית יש מצב `strict`.

**מה ההבדל מ-`dataclass`?**

| | `dataclass` | `pydantic.BaseModel` |
|---|---|---|
| מקור | ספריית תקן | חיצונית (`pip install pydantic`) |
| type hints | **תיעוד בלבד** | **נאכפים בזמן ריצה** |
| אימות ערכים | ידני | מובנה (`Field`, validators) |
| המרה מ-JSON/dict | ידנית | מובנית |
| מהירות | מהירה מאוד | מהירה (הליבה ב-Rust) |

**הכלל:** `dataclass` למבני נתונים פנימיים שאת שולטת בהם. `pydantic` לכל נתון שמגיע **מבחוץ** — קובץ config, API, קלט משתמש, תשובה ממכשיר. זה גבול האמון של המערכת, ובדיוק שם צריך אימות.

**גם למשתני סביבה:**

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str                    # read from the API_KEY env var
    debug: bool = False

settings = Settings()               # fails loudly if API_KEY is missing
```

## 80. hypothesis — בדיקות מבוססות תכונות

**הבעיה:** בטסט רגיל **את** בוחרת את הקלטים. אבל את בוחרת את הקלטים שחשבת עליהם — והבאגים מתחבאים דווקא בקלטים שלא חשבת עליהם. מחרוזת ריקה, אמוג'י, מספר ענק, רשימה עם איבר אחד.

hypothesis הופכת את הכיוון: במקום לכתוב דוגמאות, את מצהירה על **תכונה שתמיד נכונה**, והספרייה מייצרת מאות קלטים ומנסה לשבור אותה.

```python
from hypothesis import given, strategies as st


@given(st.lists(st.integers()))
def test_sorting_preserves_length(lst):
    """A property: sorting never adds or removes elements."""
    assert len(sorted(lst)) == len(lst)


@given(st.text())
def test_encode_decode_roundtrip(s):
    """A property: encoding then decoding returns the original."""
    assert s.encode("utf-8").decode("utf-8") == s


@given(st.integers(min_value=1, max_value=13))
def test_valid_deck_sizes_never_raise(size):
    create_deck(size)      # should never raise for any size in range
```

**מה שמייחד אותה — shrinking.** כשהיא מוצאת קלט שמפיל את הטסט, היא **מכווצת** אותו אוטומטית לדוגמה המינימלית שעדיין נכשלת. במקום דיווח על רשימה של 400 מספרים אקראיים, תקבלי:

```
Falsifying example: test_parse_frame(data=b'\x00')
```

זה חוסך שעות דיבאג.

```python
# Strategies - the building blocks
st.integers(min_value=0, max_value=255)
st.floats(allow_nan=False, allow_infinity=False)
st.text(min_size=1)
st.binary(min_size=4, max_size=4)       # exactly 4 bytes - great for protocols
st.lists(st.integers(), min_size=1)
st.dictionaries(st.text(), st.integers())
st.sampled_from(["PASSED", "FAILED", "SKIPPED"])
st.builds(DeviceConfig, port=st.just("/dev/ttyUSB0"))   # build whole objects
```

**למה זה חזק במיוחד לבדיקת פרוטוקולים:**

```python
@given(st.binary(min_size=12, max_size=12))
def test_parser_never_crashes_on_garbage(raw):
    """Any 12-byte input must either parse or raise ValueError - never crash."""
    try:
        parse_frame(raw)
    except ValueError:
        pass          # a controlled, expected failure is fine
```

הטסט הזה בודק **robustness**: שהפרסר אף פעם לא זורק `IndexError`, `struct.error` או קורס על קלט פגום. זו בדיוק בדיקת negative testing (סעיף 73), רק שהמכונה מייצרת את הקלטים.

**המגבלה:** צריך לחשוב במונחי תכונות, וזה לא תמיד טבעי. hypothesis משלימה טסטים רגילים, לא מחליפה אותם.

## 81. tenacity — retry מקצועי

**הבעיה:** בסעיף 19 כתבנו דקורטור `@retry` ידני. הוא עובד, אבל חסרים בו דברים שמתגלים רק בייצור: השהיה מעריכית בין ניסיונות, retry רק על סוגי שגיאה מסוימים, ולוג של כל ניסיון.

```python
from tenacity import (
    retry, stop_after_attempt, stop_after_delay,
    wait_exponential, wait_fixed, retry_if_exception_type, before_sleep_log,
)
import logging

logger = logging.getLogger(__name__)


@retry(
    stop=stop_after_attempt(5),                       # give up after 5 tries
    wait=wait_exponential(multiplier=1, max=30),      # 1s, 2s, 4s, 8s, 16s
    retry=retry_if_exception_type(ConnectionError),   # ONLY on this error
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True,                                     # raise the original error
)
def read_device_status():
    return device.query("STATUS?")
```

**למה exponential backoff ולא השהיה קבועה:** אם המכשיר או השרת עמוסים, ניסיונות חוזרים בקצב קבוע רק מחמירים את העומס. הכפלת ההמתנה נותנת לצד השני זמן להתאושש. זו תשובה טובה בראיון.

**למה `retry_if_exception_type` קריטי:** retry על **כל** חריגה הוא מסוכן. אם הקוד זרק `ValueError` בגלל באג לוגי, חמישה ניסיונות נוספים לא יעזרו — הם רק יסתירו את הבאג ויאריכו את זמן הכישלון. חוזרים רק על שגיאות **חולפות**: תקלת רשת, timeout, מכשיר עסוק.

```python
# Fine-grained control
@retry(
    stop=(stop_after_attempt(3) | stop_after_delay(60)),   # whichever comes first
    wait=wait_fixed(2),
)
def poll_until_ready(): ...
```

**מתי דווקא לא להשתמש:** בתוך טסט, retry עלול להסתיר בעיית תזמון אמיתית במוצר. שם עדיף `wait_until` עם polling (סעיף 45), שבודק תנאי במקום לחזור על פעולה עיוורת.

## 82. httpx — requests המודרני

**הבעיה:** `requests` מצוינת אבל סינכרונית בלבד. קוד שצריך גם סינכרוני וגם אסינכרוני נאלץ להחזיק שתי ספריות עם שני APIs.

`httpx` היא בעלת API כמעט זהה ל-requests, אבל תומכת בשניהם ובנוסף ב-HTTP/2.

```python
import httpx

# Synchronous - identical to requests
r = httpx.get("https://api.example.com/status", timeout=5)
r.status_code, r.json()

# Asynchronous - same API, with await
async def check(url):
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url)
        return r.status_code

# Client = the equivalent of requests.Session
with httpx.Client(base_url="https://api.example.com",
                  headers={"Authorization": "Bearer x"},
                  timeout=10) as client:
    client.get("/users")           # base_url is prepended
    client.post("/users", json={"name": "test"})
```

**שני הבדלים שחשוב להכיר:**

1. **`timeout` הוא ברירת מחדל, לא אופציה.** ב-`requests`, שכחת `timeout=` פירושה המתנה אינסופית. ב-`httpx` יש timeout ברירת מחדל של 5 שניות. זו החלטת עיצוב נכונה יותר.
2. **`raise_for_status()` לא מופעל אוטומטית** — עדיין צריך לקרוא לו, או להשתמש ב-`event_hooks`.

**מתי להישאר עם requests:** בפרויקט קיים שכולו סינכרוני ועובד. אין סיבה להחליף רק בשביל להחליף. `httpx` היא הבחירה לפרויקט חדש, במיוחד אם יש בו async.

## 83. rich ו-typer — פלט וממשק CLI

**rich — פלט טרמינל קריא**

**הבעיה:** דוח בדיקות ב-`print` הוא קיר טקסט. חשוב שיהיה קל לראות מה נכשל בסריקה מהירה.

```python
from rich.console import Console
from rich.table import Table
from rich.progress import track

console = Console()

console.print("[bold green]PASSED[/bold green] device_7")
console.print("[bold red]FAILED[/bold red] device_9", style="on white")

table = Table(title="Test Results")
table.add_column("Device")
table.add_column("Status")
table.add_column("Duration", justify="right")

table.add_row("device_7", "[green]PASSED[/green]", "12.4s")
table.add_row("device_9", "[red]FAILED[/red]", "3.1s")
console.print(table)

for item in track(devices, description="Testing devices..."):
    run_test(item)          # renders a live progress bar

console.print_exception()   # a beautifully formatted traceback
```

```python
from rich.logging import RichHandler

logging.basicConfig(handlers=[RichHandler()], format="%(message)s")
```

זה משדרג את הלוגים לפלט צבעוני עם חותמות זמן, בלי לשנות שורה אחת של קוד לוגינג.

**typer — CLI מודרני**

**הבעיה:** `argparse` (סעיף 70) עובד, אבל דורש הצהרה ידנית של כל ארגומנט. typer בונה את הכל **מ-type hints של הפונקציה**.

```python
import typer

app = typer.Typer()


@app.command()
def run(
    port: str,
    baudrate: int = 115200,
    verbose: bool = False,
    mode: str = typer.Option("fast", help="Test mode: fast or full"),
):
    """Run device verification tests."""
    typer.echo(f"Testing {port} at {baudrate}")


@app.command()
def calibrate(port: str):
    """Calibrate the device."""
    ...


if __name__ == "__main__":
    app()
```

```bash
python cli.py run /dev/ttyUSB0 --baudrate 9600 --verbose
python cli.py calibrate /dev/ttyUSB0
python cli.py --help              # generated from the docstrings and hints
```

ה-type hints הופכים לאימות אוטומטי: `baudrate: int` פוסל קלט לא-מספרי לפני שהוא מגיע ללוגיקה. typer בנויה מעל `click` ומשתמשת ב-rich לעיצוב ה-help.

## 84. loguru — לוגינג בלי הגדרות

**הבעיה:** `logging` המובנה עוצמתי אבל מסורבל — handlers, formatters, ו-loggers שצריך לחבר ידנית. loguru עושה את הדברים הנפוצים בשורה אחת.

```python
from loguru import logger

logger.info("Test started")
logger.warning("Device slow to respond")
logger.error("Test failed")

# File rotation, retention and compression in ONE line
logger.add("automation_{time}.log",
           rotation="10 MB",         # new file every 10 MB
           retention="7 days",       # delete files older than a week
           compression="zip",
           encoding="utf-8",
           level="DEBUG")

# Automatic exception context - shows variable values in the traceback
@logger.catch
def risky_operation():
    ...

# Structured context
logger.bind(device="device_7", run_id=42).info("Starting test")
```

**היתרון הגדול:** `@logger.catch` מדפיס traceback שכולל את **ערכי המשתנים** בכל פריים — לא רק את שמות הפונקציות. בדיבאג של כישלון שקרה בלילה זה ההבדל בין לשחזר לבין לנחש.

**מתי להישאר עם `logging`:** ספריות ופרויקטים שאחרים משתמשים בהם — `logging` הוא התקן, וכל כלי מכיר אותו. loguru מצוינת לאפליקציות וכלי אוטומציה שאת שולטת בהם.

## 85. mocking מתקדם — freezegun, responses, testcontainers

**freezegun — שליטה בזמן**

**הבעיה:** איך בודקים קוד שתלוי בתאריך? למשל "רישיון פג אחרי 30 יום". להמתין חודש זו לא אופציה.

```python
from freezegun import freeze_time

@freeze_time("2026-01-15 10:00:00")
def test_license_valid():
    assert is_license_valid(expiry="2026-02-01")

@freeze_time("2026-03-01")
def test_license_expired():
    assert not is_license_valid(expiry="2026-02-01")


# Moving time forward inside a test
with freeze_time("2026-01-01") as frozen:
    start_timer()
    frozen.tick(delta=timedelta(hours=25))
    assert timer_expired()          # instantly, no waiting
```

`freeze_time` מחליפה את `datetime.now()`, `time.time()` וחבריהם. זה הופך טסטים תלויי-זמן מ**איטיים ולא יציבים** ל**מיידיים ודטרמיניסטיים**.

**responses / respx — מוקינג HTTP**

```python
import responses

@responses.activate
def test_fetch_device_list():
    responses.add(
        responses.GET,
        "https://api.example.com/devices",
        json={"devices": ["device_7"]},
        status=200,
    )

    result = fetch_devices()

    assert result == ["device_7"]
    assert len(responses.calls) == 1      # verify it was actually called
```

היתרון על `@patch` ידני: מדמים את **שכבת ה-HTTP**, לא את הפונקציה. הטסט בודק שהקוד בונה URL נכון, שולח כותרות נכונות, ומטפל נכון בסטטוסים — דברים ש-mock של `requests.get` מדלג עליהם. (`respx` היא המקבילה ל-`httpx`.)

**testcontainers — טסטי אינטגרציה אמיתיים**

```python
from testcontainers.postgres import PostgresContainer

def test_results_are_persisted():
    with PostgresContainer("postgres:16") as postgres:
        url = postgres.get_connection_url()
        db = ResultsDatabase(url)

        db.save_result("device_7", "PASSED")

        assert db.get_results("device_7")[0].status == "PASSED"
    # the container is destroyed automatically
```

מריצה מסד נתונים אמיתי ב-Docker לזמן הטסט. זה פותר את הדילמה הישנה: mock של DB מהיר אבל לא בודק SQL אמיתי, ו-DB משותף יוצר תלות בין טסטים. testcontainers נותנת DB נקי לכל הרצה.

## 86. תוספי pytest שכדאי להכיר

```bash
pip install pytest-timeout pytest-repeat pytest-randomly pytest-benchmark pytest-mock
```

| תוסף | מה פותר |
|---|---|
| `pytest-timeout` | טסט תקוע לא תולה את כל ה-suite |
| `pytest-repeat` | הרצה חוזרת — **הכלי לאיתור טסטים flaky** |
| `pytest-randomly` | סדר הרצה אקראי — חושף תלות סמויה בין טסטים |
| `pytest-benchmark` | מדידת ביצועים עם השוואה להרצות קודמות |
| `pytest-mock` | ה-fixture `mocker` — נוח יותר מ-`@patch` מקונן |
| `pytest-sugar` | פלט התקדמות קריא יותר |

```bash
pytest --timeout=30                    # fail any test that runs over 30s
pytest --count=50 test_flaky.py        # run it 50 times - does it always pass?
pytest -p no:randomly                  # disable random ordering when debugging
```

**`pytest-randomly` הוא הכלי הכי חשוב מהרשימה** מבחינה מושגית: אם הטסטים עוברים בסדר אחד ונכשלים באחר, יש ביניהם **תלות סמויה** — טסט שמשאיר מצב שהבא מסתמך עליו. זו הפרה של test isolation, ולרוב היא נשארת נסתרת עד שהיא מתפוצצת ב-CI.

```python
# pytest-mock: cleaner than nested @patch decorators
def test_device_read(mocker):
    mock_serial = mocker.patch("mymodule.serial.Serial")
    mock_serial.return_value.readline.return_value = b"OK\n"

    assert read_status() == "OK"
```

## 87. numpy ו-pandas — ניתוח תוצאות

**numpy — מערכים מספריים**

רלוונטי לניתוח נתוני מדידה מחומרה: דגימות מאוסילוסקופ, טלמטריה, אותות.

```python
import numpy as np

samples = np.array([1.2, 3.4, 2.1, 5.6, 0.9])

samples.mean(), samples.std(), samples.max(), samples.min()
np.percentile(samples, 95)              # 95th percentile - common in SLA checks

# Vectorized operations - no Python loop, runs in C
normalized = (samples - samples.mean()) / samples.std()
above = samples[samples > 2.0]          # boolean mask filtering

# Comparing floats in test assertions
np.allclose(measured, expected, rtol=1e-3)     # relative tolerance
```

**`np.allclose` הוא הכלי הנכון לבדיקת מדידות.** מדידה מחומרה לעולם לא תהיה שווה בדיוק לערך הצפוי — יש רעש. השוואה עם סובלנות היא הדרך היחידה שלא תיצור טסט flaky.

**pandas — טבלאות ותוצאות**

```python
import pandas as pd

df = pd.read_csv("test_results.csv")

df.head(), df.info(), df.describe()
df[df["status"] == "FAILED"]                       # filter rows
df.groupby("device_id")["duration"].mean()         # aggregate
df.sort_values("duration", ascending=False).head(10)
df["duration"].quantile(0.95)

# Failure rate per device - a realistic automation report
summary = df.groupby("device_id").agg(
    total=("status", "count"),
    failures=("status", lambda s: (s == "FAILED").sum()),
)
summary["failure_rate"] = summary["failures"] / summary["total"]

summary.to_csv("summary.csv")
summary.to_excel("summary.xlsx")
```

`pandas` הופכת דוח תוצאות מסקריפט לולאות לשלוש שורות. שווה גם לדעת על **`polars`** — חלופה מודרנית ומהירה יותר עם API דומה, שצוברת פופולריות לקבצים גדולים.

## 88. ניהול תלויות מודרני — uv ו-poetry

**הבעיה עם `pip` + `requirements.txt`:** הקובץ מפרט מה ביקשת, אבל לא בהכרח את **הגרסאות המדויקות של התלויות של התלויות**. שתי התקנות באותו requirements יכולות להניב סביבות שונות — וזה מקור קלאסי ל"אצלי זה עובד".

```toml
# pyproject.toml - the modern standard, replaces setup.py
[project]
name = "device-automation"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "pytest>=8.0",
    "pyserial>=3.5",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = ["ruff", "mypy", "pytest-cov"]

[tool.ruff]
line-length = 99

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"
```

הקובץ הזה מחליף את `setup.py`, `requirements.txt`, `pytest.ini` ו-`.flake8` — הכל בקובץ אחד תקני.

**`uv` — מנהל החבילות המהיר (הסטנדרט המתהווה):**

```bash
pip install uv

uv venv                          # create a virtual environment
uv pip install -r requirements.txt
uv add pytest pyserial           # add a dependency to pyproject.toml
uv sync                          # install exactly what the lock file says
uv run pytest                    # run inside the environment, no activation
```

`uv` כתובה ב-Rust ומהירה פי עשרות מ-`pip`. היא מייצרת **lock file** שמקבע את הגרסאות המדויקות של כל התלויות — כך שהסביבה במחשב שלך, אצל עמית, וב-CI זהות לחלוטין. זו התשובה ל"אצלי זה עובד".

**`poetry`** עושה דבר דומה, ותיקה יותר ונפוצה בפרויקטים קיימים. מספיק לדעת שהשתיים פותרות את אותה בעיה.

**מה להגיד בראיון:** הבעיה היא **reproducibility** — היכולת לשחזר סביבה זהה. `requirements.txt` פשוט אבל לא נעול; lock file מבטיח זהות. בסביבות מנותקות רשת (כמו בתעשייה הביטחונית) זה קריטי כפליים, כי מתקינים מ-mirror פנימי וכל הבדל גרסה מתגלה מאוחר.

</div>
