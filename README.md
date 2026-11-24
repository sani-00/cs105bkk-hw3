# HW3: a step counter's weekly report

**Worth 10% of your grade.** HW3 covers Sessions 7, 9 and 10. You will read a fitness watch's step log from a CSV file, skip the broken rows, save a weekly report as JSON without ever losing the old one, and write your own tests.

**Released:** Fri 20 Nov. **Due:** Wed 25 Nov, 23:59. Wednesday is also the oral exam, so plan to finish before it.

**Late work:** each day late costs 10% of the mark. You can hand in up to 3 days late; after that, HW3 is not accepted.

## 1. Get your own copy

1. On this repository's GitHub page, click **Use this template** → **Create a new repository**.
2. Owner: your own account. Name: `cs105bkk-hw3`. Click **Create repository**.
3. Clone **your** new repository and open the folder in VS Code:

   ```
   git clone https://github.com/<your-username>/cs105bkk-hw3.git
   ```

## 2. Set up and see red

From the repository folder:

```
python -m venv .venv
```

Activate it. On macOS: `source .venv/bin/activate`. On Windows: `.venv\Scripts\activate`.

```
python -m pip install pytest
python -m pytest
```

Every test fails with `NotImplementedError`. That is the starting point. Each error message names the part you still have to write.

## 3. The story

Your fitness watch counts your steps and saves every walk to a CSV file, `walks.csv`: the date, the number of steps, and where you walked. The watch has bugs of its own, so some rows are broken: a missing date, or steps written as `abc`, `12.5` or `-300`. You will skip the broken rows, add up your steps for each day, find your best day, and save the week's report as a JSON file.

| File | Its job |
|---|---|
| `walks.csv` | The watch's log for one week. Read it, but don't change it: the tests use it. |
| `walks.py` | Reads the log and keeps only the good rows. |
| `report.py` | Adds up the steps, and saves and loads the report. It imports `walks.py`. |
| `test_my_walks.py` | Your own tests (part 10). |

Every function whose body is `raise NotImplementedError(...)` is yours to write. Parts marked **Provided** are already done; read them, but don't change them. Don't change any names or signatures either, because the tests use them.

The examples below run in the Python shell, started from the repository folder, after `from pathlib import Path`, `import json`, and importing the functions you need.

## 4. Write the code

Work through the parts in this order. Run `python -m pytest` after each one.

### `walks.py`: read the log and keep the good rows

`Walk` is a provided dataclass with a `date`, a number of `steps` and a `place`.

1. **`parse_walk(row)`** turns one row of the CSV file, a dict of text, into a `Walk`. A row is bad, and `parse_walk` raises `ValueError`, when:
   - the date is empty once you strip the spaces around it;
   - the steps are not a whole number: empty, `abc` and `12.5` are all bad. Spaces around the number are fine: `int(" 3100 ")` already ignores them;
   - the steps are below 0. Zero steps is a good row: a rainy day at home.

   Strip the spaces around the date and the place too. Don't change the row itself. The error message is up to you.

   ```python
   >>> parse_walk({"date": "2026-11-16", "steps": " 3100 ", "place": " campus "})
   Walk(date='2026-11-16', steps=3100, place='campus')
   >>> parse_walk({"date": "2026-11-19", "steps": "-300", "place": "campus"})
   ValueError: steps is below 0: -300
   ```

2. **`none_on_error(func)`** is a decorator, as in Session 9: it returns a new function, the wrapper, that calls `func` with the same arguments (`*args, **kwargs`) and returns its result. When `func` raises `ValueError`, the wrapper returns `None` instead. Any other error goes on as it is: catch `ValueError` and nothing else (Session 6).

   ```python
   >>> @none_on_error
   ... def to_int(text):
   ...     return int(text)
   ...
   >>> to_int("42"), to_int("abc")
   (42, None)
   ```

3. **`read_rows(path)`** is a generator function (Session 9). It opens the CSV file with `encoding="utf-8", newline=""` (Session 7), reads it with `csv.DictReader`, and **yields** the rows one at a time. Write the `yield` inside the `with` block: the file stays open while the rows are handed out, and closes after the last one. The log has a place name in Thai, so the encoding matters, above all on Windows.

   ```python
   >>> rows = read_rows(Path("walks.csv"))
   >>> next(rows)
   {'date': '2026-11-16', 'steps': '4200', 'place': 'Lumphini Park'}
   ```

4. **`good_walks(rows)`** is a generator function too. For each row it yields a `Walk`, and it skips the bad rows. A decorator is just a function, so `none_on_error(parse_walk)` gives you a parser that returns `None` for a bad row instead of raising. Use it.

   Like `read_rows`, it hands out one walk at a time and never builds a list, so it would work on a log of a whole year.

   ```python
   >>> walks = list(good_walks(read_rows(Path("walks.csv"))))
   >>> len(walks)
   9
   >>> walks[1]
   Walk(date='2026-11-16', steps=3100, place='campus')
   ```

### `report.py`: the weekly report

5. **`steps_per_day(walks)`** returns a dict that maps each date to its total steps. Some dates appear more than once in the log, and the log is not in date order. Put the dates in order, earliest first: dates written as `YYYY-MM-DD` sort as text in the right order, so `sorted` works on them. `walks` can be a generator, so go through it only once.

   ```python
   >>> steps_per_day(walks)
   {'2026-11-16': 7300, '2026-11-17': 8300, '2026-11-18': 2500, '2026-11-19': 7350, '2026-11-20': 9100, '2026-11-21': 0, '2026-11-22': 3900}
   ```

6. **`best_day(totals)`** returns the date with the most steps. On a tie, it returns the earliest of the tied dates, even when the dict is not in date order. With no days at all, it raises `ValueError`.

   ```python
   >>> best_day(steps_per_day(walks))
   '2026-11-20'
   >>> best_day({"2026-11-20": 5000, "2026-11-18": 5000})
   '2026-11-18'
   ```

7. **`saved_safely(path)`** is a context manager, already marked `@contextmanager`, so you write it as a generator with one `yield` (Session 9). It solves a real problem: if the program crashes halfway through writing `report.json`, the old report is gone and the new one is only half there. So `saved_safely` never writes to `path` itself:
   - it opens a new file next to it, `path.with_name(path.name + ".tmp")`, for writing in UTF-8, and yields that open file to the `with` block;
   - if the `with` block ends without an error, it puts the new file in place of the old one with the `.tmp` path's `replace(path)` method;
   - if the `with` block raises an error, it deletes the `.tmp` file with its `unlink()` method, and then lets the same error go on: `raise` on its own does that. `path` is not changed at all.

   ```python
   >>> with saved_safely(Path("goal.json")) as file:
   ...     json.dump({"steps_a_day": 8000}, file)
   ...
   >>> with saved_safely(Path("goal.json")) as file:
   ...     json.dump({"steps_a_day": 10000}, file)
   ...     raise OSError("the battery died")
   ...
   OSError: the battery died
   >>> Path("goal.json").read_text(encoding="utf-8")
   '{"steps_a_day": 8000}'
   ```

8. **`write_report(path, walks)`** builds the report as a dict with three keys: `"total_steps"` (all the steps of the week), `"best_day"` and `"days"` (the dict from `steps_per_day`). It saves the report to `path` as JSON with `json.dump(report, file, indent=2)`, inside `with saved_safely(path) as file:`, and returns the dict. As in part 5, `walks` can be a generator, and it is one when `python report.py` runs, so go through it only once. With no walks, `best_day` raises `ValueError`, and the old report must stay as it was.

   ```python
   >>> report = write_report(Path("report.json"), walks)
   >>> report["total_steps"], report["best_day"]
   (38450, '2026-11-20')
   ```

9. **`load_report(path)`** reads the report back with `json.load` and returns it as a dict. It returns `None` when there is no file yet (`FileNotFoundError`), or when the file is not valid JSON (`json.JSONDecodeError`). Catch those two errors and nothing else.

   ```python
   >>> load_report(Path("report.json"))["best_day"]
   '2026-11-20'
   >>> print(load_report(Path("no_such_report.json")))
   None
   ```

When you are done, run `python report.py` twice. Its provided `if __name__ == "__main__":` block reads `walks.csv`, prints the week's total and best day, and saves `report.json`. The second time, it also tells you what the report said last time. `report.json` is in `.gitignore`, so it is not committed.

Run `python -m pytest` until every test passes. The tests you see are not all the tests: grading also runs more tests on cases these rules describe, such as the limits, an empty file, the bad rows, and "nothing changes after an error". Read each rule above carefully, and try those cases yourself.

## 5. Write your own tests

10. Until now, the tests came with the homework. In Session 10 you learned to write your own, so this part is yours. In `test_my_walks.py`, write tests for `parse_walk` below the provided example:
    - Use the provided fixture `good_row` in your tests: each test gets its own new copy of a good row. Change one value in it, then call `parse_walk`.
    - Write at least one test with `@pytest.mark.parametrize` that checks several bad rows with `pytest.raises(ValueError)`.
    - Cover every rule of part 1, including its limits. Use plain `assert`, and name each test `test_` plus what it checks.

    Run only your tests with `python -m pytest test_my_walks.py`.

    We grade your tests by running them against a correct `walks.py`, where every one of them must pass, and against several versions of `walks.py` with a bug planted in `parse_walk`, where at least one of your tests should fail. A bug your tests let through costs marks, and so does a test that fails on correct code.

**When a test fails and you can't see why,** debug it as in Session 10: read the traceback from the bottom up, then put `breakpoint()` on the line before the problem (or set a breakpoint in VS Code) and look at the values. Take `breakpoint()` out again before you push.

## 6. Fill in NOTES.md

Answer the three questions in `NOTES.md`. A few honest sentences each are enough.

## 7. Commit, push, and check Actions

Commit as you go, not only at the end. When you are done:

```
git add walks.py report.py test_my_walks.py NOTES.md
git commit -m "Finish HW3"
git push
```

On your repository's GitHub page, open the **Actions** tab. GitHub runs the tests on every push, your own tests included. A green tick means they all passed there too. That result is feedback for you, not your grade. Don't change `test_walks.py`, `test_report.py`, `walks.csv` or the workflow file: changes to them are flagged.

## 8. Upload to Google Classroom

Upload a `.zip` of your repository and paste its link in the HW3 assignment on Google Classroom. Your GitHub repository at the deadline is the copy that is graded. *(Proposal O13)*
