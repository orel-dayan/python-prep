# מעבדת בדיקות מיניאטורית – לקוח מול "רדיו"

שלד עובד שמדמה אפליקציה שמדברת עם רדיו דרך UDP, בלי צורך בחומרה.
20 בדיקות עוברות, הקוד נקי ב-ruff.

## הרצה

```powershell
cd radio_test
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pytest ruff
pytest -v
ruff check .
```

## מה יש כאן

| קובץ | תפקיד | המקבילה בעולם האמיתי |
|---|---|---|
| `radio_sim.py` | סימולטור UDP של ממשק ניהול הרדיו | הרדיו / ה-Test Bench |
| `radio_client.py` | שכבת הפשטה להתקן: `get_status()`, `set_tx_power()` | האפליקציה הנבדקת |
| `conftest.py` | fixtures – הקמה וניקוי של סביבה נקייה לכל בדיקה | ניהול מעבדה |
| `test_radio_client.py` | הבדיקות עצמן, מחולקות לפי סוג | סוויטת הרגרסיה |

## הרעיון המרכזי

`FaultProfile` מאפשר להזריק תקלות בצורה **חוזרת ומדידה**:

```python
radio_factory(drop_rate=0.5, seed=1)   # 50% איבוד חבילות, דטרמיניסטי
radio_factory(extra_delay=0.4)         # רדיו איטי
radio_factory(malformed=True)          # תשובה לא חוקית
radio_factory(seq_offset=-1)           # תשובה מאוחרת של בקשה קודמת
```

זה בדיוק מה שקשה לייצר מול חומרה אמיתית, ובדיוק מה שמפיל אפליקציות בשטח.

## תרגילים להרחבה

1. הוסיפי פקודה `GET_LINK_QUALITY` לסימולטור, ולקוח + בדיקות עבורה.
2. הוסיפי תקלה `duplicate=True` (שליחת אותה תשובה פעמיים) – האם הלקוח עמיד?
3. הוסיפי בדיקת עומס: 1000 בקשות ברצף, ומדדי זמן תגובה (p50 / p95).
4. הוסיפי fixture שמקליטה pcap עם `tshark` במקביל לכל בדיקה.
5. הוסיפי מונה `requests_seen` לאימות מספר השידורים החוזרים בכל תרחיש.
6. עטפי הכל ב-GitHub Actions / Jenkins שירוץ על כל commit.
