# `patch` — מה זה ולמה צריך

**שורה תחתונה:** `patch` = "החלף לי זמנית את X במשהו מזויף, ותחזיר אותו כשנגמר הטסט".

## האנלוגיה

תארי לעצמך שאת בודקת מכונית, ויש בה כפתור שמפעיל צופר אמיתי ורועש. את לא רוצה צופר אמיתי בכל בדיקה. אז את מנתקת את הצופר, מחברת במקומו נורה קטנה, בודקת שהכפתור מדליק את הנורה — ובסוף מחזירה את הצופר.

`patch` זה הניתוק והחיבור מחדש. אוטומטית.

## למה בכלל צריך

בתרגיל הקודם הזרקנו `api` דרך הבנאי:

```python
client = WeatherClient(api_mock)   # easy - we chose what goes in
```

אבל `time.sleep` לא עובר דרך הבנאי. הקוד פשוט קורא לו:

```python
time.sleep(2.0)   # nobody asked us
```

אין דרך "להעביר" משהו אחר. הדרך היחידה היא ללכת לזיכרון של פייתון ולהחליף את מה שהשם `sleep` מצביע עליו. זה `patch`.

## הצורה הראשונה — `with` (הכי קלה להבנה)

```python
def test_something():
    with patch("weather_client.time.sleep") as mock_sleep:
        # inside here, time.sleep is fake and does nothing
        client.get_temperature("Tel Aviv")
    # outside - time.sleep is real again

    assert mock_sleep.call_count == 3
```

קראי את זה כך:

- `patch("...")` — מה מחליפים
- `as mock_sleep` — תני לי את המזויף בשם הזה, כדי שאוכל לבדוק אותו אחר כך
- הכל בתוך ה־`with` רץ עם המזויף
- ברגע שיצאנו — הכל חזר לקדמותו

**זו הצורה שאני ממליץ לך להתחיל איתה.** הכי ברור מה קורה ואיפה.

## הצורה השנייה — decorator (קיצור)

בדיוק אותו דבר, אבל על כל הפונקציה:

```python
@patch("weather_client.time.sleep")
def test_something(mock_sleep):
    client.get_temperature("Tel Aviv")
    assert mock_sleep.call_count == 3
```

ההבדל היחיד: אין `with`, וה־mock מגיע כ**פרמטר** של הטסט. pytest לא נותן לך אותו — `patch` נותן.

**המלכודת:** אם יש כמה `@patch`, הפרמטרים מגיעים **מלמטה למעלה**:

```python
@patch("weather_client.time.sleep")     # top - arrives second
@patch("weather_client.requests.get")   # bottom - arrives first
def test_something(mock_get, mock_sleep):
    ...
```

הכי קרוב לפונקציה = הכי ראשון בפרמטרים. זו שאלת ראיון נפוצה.

## הצורה השלישית — `patch.object` (כשיש לך את האובייקט ביד)

בשתי הצורות הקודמות נתת **מחרוזת** — שם. כאן את נותנת את האובייקט עצמו:

```python
with patch.object(client, "get_temperature") as mock_get:
    mock_get.return_value = 25.0
    result = client.is_freezing("Tel Aviv")
```

"קחי את האובייקט `client` הזה, והחליפי בו את המתודה `get_temperature`."

מתי זה עדיף: כשאת רוצה לזייף מתודה אחת של אובייקט ולהשאיר את השאר אמיתי. כאן למשל בדקנו את `is_freezing` בלי לגעת ב־API בכלל.

## הצורה הרביעית — `monkeypatch` (של pytest)

fixture מובנית, לא צריך import:

```python
def test_something(monkeypatch):
    monkeypatch.setattr("weather_client.time.sleep", lambda seconds: None)
```

"החלף את זה בפונקציה שלא עושה כלום."

**ההבדל החשוב:** ה־`lambda` היא לא MagicMock — היא לא זוכרת כלום. אז אם את רק רוצה **להשתיק** משהו, `monkeypatch` מעולה. אם את רוצה גם **לבדוק** שהוא נקרא ובמה — צריך `patch`.

`monkeypatch` גם נוח במיוחד למשתני סביבה:

```python
monkeypatch.setenv("DEVICE_IP", "127.0.0.1")
```

## מה עושים עם ה־mock אחרי שקיבלת אותו

זה החלק שהופך את זה מ"השתקה" ל"בדיקה":

```python
mock_sleep.assert_not_called()        # never called
mock_sleep.assert_called_once()       # exactly once
mock_sleep.call_count                 # how many times
mock_sleep.call_args_list             # every call and its arguments
mock_sleep.assert_called_with(2.0)    # the last call had this argument
```

## סיכום בשורה אחת כל אחד

| צורה | מתי |
|---|---|
| `with patch("...")` | ברירת המחדל שלך. ברור ומדויק |
| `@patch("...")` | כשכל הטסט צריך את זה — קצר יותר |
| `patch.object(obj, "name")` | כשיש לך את האובייקט ולא רק שם |
| `monkeypatch` | משתני סביבה, והשתקה פשוטה בלי אימות |

**ההמלצה שלי:** תשתמשי רק ב־`with patch(...)` לעת עתה. תעשי איתו את משימות 2-5, ורק כשזה יושב טוב — תעברי לצורות האחרות. אין שום דבר שהן עושות שהוא לא יכול.
