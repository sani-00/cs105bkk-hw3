"""HW3 · report.py: add up the steps and save a report as JSON. Practises Session 7 (writing
and reading JSON) and Session 9 (a context manager)."""

import json
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import TextIO

from walks import Walk, good_walks, read_rows


def steps_per_day(walks: Iterable[Walk]) -> dict[str, int]:
    """Total steps for each date, with the dates in order, earliest first."""
    raise NotImplementedError("core: add up the steps for each date, earliest date first")


def best_day(totals: dict[str, int]) -> str:
    """The date with the most steps. On a tie, the earliest of those dates."""
    raise NotImplementedError("core: the date with the most steps, the earliest on a tie")


@contextmanager
def saved_safely(path: Path) -> Iterator[TextIO]:
    """Write to a new file, and put it in place of `path` only if the with block ends without an error."""
    raise NotImplementedError("core: write to a .tmp file, then replace path only if nothing failed")


def write_report(path: Path, walks: Iterable[Walk]) -> dict:
    """Save the week's report to a JSON file, and return it as a dict."""
    raise NotImplementedError("core: build the report dict, save it with saved_safely, return it")


def load_report(path: Path) -> dict | None:
    """The report saved last time, or None if there is no file or it is not valid JSON."""
    raise NotImplementedError("core: load the saved report, or None if it is missing or broken")


if __name__ == "__main__":
    # Provided: runs only with `python report.py`, not on import.
    here = Path(__file__).parent
    last_time = load_report(here / "report.json")
    report = write_report(here / "report.json", good_walks(read_rows(here / "walks.csv")))
    print(f"{report['total_steps']} steps this week. Best day: {report['best_day']}.")
    if last_time is not None:
        print(f"Last time you saved {last_time['total_steps']} steps.")
